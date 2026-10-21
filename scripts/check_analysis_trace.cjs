/* Offline trace UI checks: long actions, cursor recovery, XSS, refresh, themes and mobile. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { spawn } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const output = path.join(root, 'test_reports');
fs.mkdirSync(output, { recursive: true });
const profile = fs.mkdtempSync(path.join(output, 'trace-browser-'));
const executable = process.argv[2] || 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
let events = [], running = false, failNext = false, actionResponse = null, createdBody = null, startedNew = false;
let status = 'WAITING_DESIGN', readsWhilePending = 0;
const unsafePath = 'src/<img src=x onerror=window.traceInjected=1>.py';
function event(type, category, name, span, parent, state, attrs = {}) {
  events.push({ event_id: `event-${events.length + 1}`, sequence: events.length + 1,
    run_id: 'trace-test', execution_id: 'execution-1', span_id: span, parent_span_id: parent,
    event_type: type, category, name, status: state, attributes: attrs,
    occurred_at: new Date().toISOString(), duration_ms: type.endsWith('finished') ? 1400 : null });
}
function run(id = 'trace-test') { return { run_id: id, status, repo_url: 'https://github.com/example/trace', progress: 20, current_node: 'design_gate', created_at: new Date().toISOString() }; }
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, 'http://localhost');
  const route = url.pathname;
  function send(data, code = 200) { res.statusCode = code; res.setHeader('Content-Type', 'application/json; charset=utf-8'); res.end(JSON.stringify(data)); }
  if (route === '/health') return send({ environment: 'Trace 验证 · 模拟数据' });
  if (route === '/api/v1/analysis' && req.method === 'POST') {
    let text = ''; for await (const chunk of req) text += chunk;
    createdBody = JSON.parse(text); status = 'CREATED';
    return send(run('new-trace'));
  }
  if (route === '/api/v1/analysis') return send([run()]);
  if (route.endsWith('/start')) { startedNew = true; status = 'WAITING_DESIGN'; return send(run('new-trace')); }
  if (route.endsWith('/approve')) {
    running = true; actionResponse = res;
    event('span.started', 'run', 'approve', 'root', null, 'running');
    event('span.started', 'node', 'plan_executor', 'node', 'root', 'running');
    event('span.started', 'skill', 'architecture_analysis', 'skill', 'node', 'running');
    event('span.started', 'file', 'read_file', 'file', 'skill', 'running', { file_path: unsafePath });
    return;
  }
  if (route.endsWith('/trace')) {
    if (failNext) { failNext = false; return send({}, 503); }
    if (running) readsWhilePending++;
    const after = Number(url.searchParams.get('after') || 0);
    const id = route.split('/')[4];
    return send({ run_id: id, events: events.filter(e => e.sequence > after),
      next_cursor: events.length || after, has_more: false,
      trace_state: events.length ? 'available' : 'not_recorded',
      execution: events.length ? { execution_id: 'execution-1', status: running ? 'running' : 'waiting', gap_count: 0 } : {} });
  }
  if (route.startsWith('/api/v1/analysis/')) return send(run(route.split('/')[4]));
  const targets = { '/': 'index.html', '/static/app.css': 'app.css', '/static/app.js': 'app.js', '/static/trace.js': 'trace.js' };
  if (targets[route]) {
    res.setHeader('Content-Type', route.endsWith('.js') ? 'text/javascript; charset=utf-8' : route.endsWith('.css') ? 'text/css; charset=utf-8' : 'text/html; charset=utf-8');
    return res.end(fs.readFileSync(path.join(root, 'app/static', targets[route])));
  }
  res.statusCode = 404; res.end();
});

async function connect(url) {
  const socket = new WebSocket(url);
  await new Promise((resolve, reject) => { socket.onopen = resolve; socket.onerror = reject; });
  let number = 0;
  const pending = new Map();
  const errors = [];
  socket.onmessage = ({ data }) => {
    const message = JSON.parse(data);
    if (message.method === 'Runtime.exceptionThrown') errors.push(message.params.exceptionDetails.text);
    const request = pending.get(message.id);
    if (!request) return;
    clearTimeout(request.timer);
    pending.delete(message.id);
    if (message.error) request.reject(new Error(JSON.stringify(message.error)));
    else request.resolve(message.result);
  };
  return {
    errors,
    close: () => socket.close(),
    call(method, params = {}) {
      return new Promise((resolve, reject) => {
        const id = ++number;
        const timer = setTimeout(() => { pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }, 12000);
        pending.set(id, { resolve, reject, timer });
        socket.send(JSON.stringify({ id, method, params }));
      });
    },
  };
}

(async () => {
  let browser, client;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    browser = spawn(executable, ['--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'], { windowsHide: true, stdio: 'ignore' });
    let port;
    for (let n = 0; n < 100; n++) { const file = path.join(profile, 'DevToolsActivePort'); if (fs.existsSync(file)) { port = fs.readFileSync(file, 'utf8').split('\n')[0]; break; } await delay(100); }
    assert(port, 'No browser debugging port');
    const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    client = await connect(targets.find(t => t.type === 'page').webSocketDebuggerUrl);
    await client.call('Page.enable'); await client.call('Runtime.enable');
    const evaluate = async expression => { const r = await client.call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }); assert(!r.exceptionDetails, JSON.stringify(r.exceptionDetails)); return r.result.value; };
    const until = async (expression, title) => { for (let n = 0; n < 100; n++) { if (await evaluate(expression)) return; await delay(100); } throw new Error(title || expression); };
    await client.call('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
    await client.call('Page.navigate', { url: `http://127.0.0.1:${server.address().port}/#/run/trace-test` });
    await until('Boolean(document.querySelector("#actions button"))', 'Approval did not render');
    await evaluate('document.querySelector("#actions button").click()');
    await until('document.querySelectorAll(".trace-item").length >= 4', 'Trace not delivered during pending approve');
    assert(actionResponse && !actionResponse.writableEnded);
    assert(readsWhilePending > 0);
    assert.equal(await evaluate('document.querySelector("#callout").classList.contains("hidden")'), true);
    assert.equal(await evaluate('document.querySelector("#node").textContent === "design_gate"'), false);
    assert.equal(await evaluate('Boolean(document.querySelector("#traceList img")) || Boolean(window.traceInjected)'), false);
    assert.equal(await evaluate(`Array.from(document.querySelectorAll('.trace-name-text')).some(n => n.textContent === ${JSON.stringify(unsafePath)})`), true);
    await evaluate('document.querySelector("[data-span=node]").open = false; document.querySelector("[data-span=node] > summary").focus()');
    event('span.finished', 'file', 'read_file', 'file', 'skill', 'unavailable', { file_path: unsafePath, error_type: 'ReadTimeout' });
    await until('document.querySelector("[data-span=file]").dataset.status === "unavailable"');
    assert.equal(await evaluate('document.querySelector("[data-span=node]").open'), false);
    assert.equal(await evaluate('document.activeElement.parentElement.dataset.span'), 'node');
    failNext = true;
    await until('document.querySelector("#traceConnection").textContent.includes("连接中断")', 'No disconnect state');
    await until('document.querySelector("#traceConnection").textContent === "已同步"', 'No reconnect');
    assert.equal(await evaluate('document.querySelectorAll("[data-span=file]").length'), 1);
    for (const entry of events) if (entry.category === 'file') entry.attributes.file_path = 'src/services/analysis.py';
    // Reload during the same pending action: no new approve/start is sent.
    await client.call('Page.reload');
    await until('document.querySelectorAll(".trace-item").length >= 4', 'Trace not restored');
    assert.equal(await evaluate('document.querySelector("#callout").classList.contains("hidden")'), true);
    await evaluate('document.querySelector("[data-span=node]").open = true; document.querySelector("[data-span=skill]").open = true');
    for (const [name, width, height] of [['desktop', 1440, 1000], ['mobile', 390, 844]]) {
      await client.call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: name === 'mobile' });
      for (const theme of ['light', 'dark']) {
        await evaluate(`document.documentElement.dataset.theme = '${theme}'; document.querySelector('#tracePanel').scrollIntoView({block:'start'})`);
        await delay(200);
        assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), true, `${name}/${theme} overflow`);
        const shot = await client.call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
        fs.writeFileSync(path.join(output, `analysis-trace-${name}-${theme}.png`), Buffer.from(shot.data, 'base64'));
      }
    }
    // Filter and return to the live tail without replacing the timeline.
    await evaluate('document.querySelector("#traceFilter").value="warning"; document.querySelector("#traceFilter").dispatchEvent(new Event("change"))');
    assert.equal(await evaluate('document.querySelector("[data-span=file]").hidden'), false);
    event('span.finished', 'skill', 'architecture_analysis', 'skill', 'node', 'partial');
    event('span.finished', 'node', 'plan_executor', 'node', 'root', 'completed');
    event('span.finished', 'run', 'approve', 'root', null, 'waiting');
    running = false; status = 'WAITING_HUMAN';
    actionResponse.setHeader('Content-Type', 'application/json'); actionResponse.end(JSON.stringify(run()));
    await until('document.querySelector("#callout").textContent.includes("批准并生成报告")', 'Gate did not reconcile after external action');
    // New run must create first and only then start with its stable ID.
    await evaluate('document.querySelector("#repo").value="https://github.com/demo/new-project"; document.querySelector("#startForm").dispatchEvent(new Event("submit", {cancelable:true,bubbles:true}))');
    for (let n = 0; n < 100 && !startedNew; n++) await delay(100);
    assert.equal(createdBody.defer_start, true); assert(startedNew);
    assert.deepEqual(client.errors, []);
    console.log('Trace browser checks passed: pending action delivery, safe text, expansion/focus, reconnect/dedup, reload, theme/mobile layout, gate reconciliation and deferred start.');
  } finally {
    if (actionResponse && !actionResponse.writableEnded) actionResponse.end('{}');
    if (client) { await client.call('Browser.close').catch(() => {}); client.close(); }
    if (browser && browser.exitCode === null) browser.kill();
    server.closeAllConnections(); server.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
