"""Optional execution events; no persistence or analysis dependencies."""

from contextlib import asynccontextmanager
from contextvars import ContextVar
from functools import wraps
from inspect import signature
from time import monotonic
from uuid import uuid4

_recorder = ContextVar("workflow_trace_recorder", default=None)
_parent = ContextVar("workflow_trace_parent", default=None)


@asynccontextmanager
async def bind_trace(recorder):
    token = _recorder.set(recorder)
    parent_token = _parent.set(None)
    try:
        yield
    finally:
        _parent.reset(parent_token)
        _recorder.reset(token)


async def trace_event(name, message="", **attributes):
    recorder = _recorder.get()
    if recorder is not None:
        await recorder.emit(
            event_type="progress", category="skill", name=name,
            message=message, span_id=_parent.get(), attributes=attributes,
        )


def result_summary(result):
    attrs = {}
    status = "completed"
    if isinstance(result, dict):
        if result.get("available") is False:
            status = "unavailable"
        failures = result.get("persist_failures") or result.get("read_errors")
        if failures:
            status = "partial"
            attrs["failed"] = len(failures)
        inventory = result.get("source_inventory") or {}
        for key in ("source_files", "selected_files", "read_successful_files"):
            if isinstance(inventory.get(key), int):
                attrs[key] = inventory[key]
        modules = result.get("modules")
        if isinstance(modules, list) and any(item.get("error") for item in modules):
            status = "partial"
        for key in ("count", "details"):
            if isinstance(result.get(key), int):
                attrs[key] = result[key]
    elif isinstance(result, str) and not result.strip():
        status = "unavailable"
    workflow_status = getattr(result, "status", None)
    if isinstance(workflow_status, str):
        attrs["workflow_status"] = workflow_status
        if workflow_status in {"WAITING_DESIGN", "WAITING_HUMAN", "PAUSED"}:
            status = "waiting"
        elif workflow_status == "FAILED":
            status = "failed"
        elif workflow_status == "CANCELED":
            status = "canceled"
    return status, attrs


@asynccontextmanager
async def trace_span(category, name, **attributes):
    recorder = _recorder.get()
    if recorder is None:
        yield None
        return
    span_id = str(uuid4())
    parent_id = _parent.get()
    await recorder.emit(event_type="span.started", category=category, name=name,
                        span_id=span_id, parent_span_id=parent_id,
                        status="running", attributes=attributes)
    token = _parent.set(span_id)
    started = monotonic()
    outcome = {"status": "completed", "attributes": {}}
    try:
        yield outcome
    except BaseException as error:
        outcome["status"] = "interrupted" if not isinstance(error, Exception) else "failed"
        outcome["attributes"] = {"error_type": type(error).__name__}
        raise
    finally:
        _parent.reset(token)
        await recorder.emit(
            event_type="span.finished", category=category, name=name,
            span_id=span_id, parent_span_id=parent_id,
            status=outcome["status"],
            duration_ms=round((monotonic() - started) * 1000),
            attributes=outcome["attributes"],
        )


def traced(category, name=None):
    """Observe the actual call, retaining its original signature and outcome."""
    def decorate(function):
        call_signature = signature(function)

        @wraps(function)
        async def wrapped(*args, **kwargs):
            if _recorder.get() is None:
                return await function(*args, **kwargs)
            bound = call_signature.bind(*args, **kwargs).arguments
            instance = bound.get("self")
            label = name or getattr(instance, "name", function.__name__)
            attrs = {key: bound[key] for key in ("file_path", "branch", "model") if bound.get(key)}
            async with trace_span(category, label, **attrs) as outcome:
                result = await function(*args, **kwargs)
                outcome["status"], outcome["attributes"] = result_summary(result)
                if category == "llm":
                    actual_model = bound.get("model") or getattr(getattr(instance, "_llm", None), "model", None)
                    if isinstance(actual_model, str):
                        outcome["attributes"]["model"] = actual_model
                return result
        return wrapped
    return decorate
