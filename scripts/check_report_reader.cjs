/* Offline browser smoke check. Requires Node 22+ and a Chromium browser.
 * Usage: node scripts/check_report_reader.cjs <directory containing reader.json and reader.md> [browser.exe]
 * Serves fixture API responses only; never connects to the application database or external services.
 */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const path = require('node:path');
const { spawn } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const fixture = path.resolve(process.argv[2] || 'test_reports/reader-fixture');
const executable = process.argv[3] || process.env.BROWSER_EXECUTABLE ||
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const document = JSON.parse(fs.readFileSync(path.join(fixture, 'reader.json'), 'utf8'));
const markdown = fs.readFileSync(path.join(fixture, 'reader.md'), 'utf8');
const output = path.join(root, 'test_reports');
fs.mkdirSync(output, { recursive: true });
const profile = fs.mkdtempSync(path.join(output, 'reader-browser-'));
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const server = http.createServer((req, res) => {
  const route = new URL(req.url, 'http://localhost').pathname;
  const send = (value) => { res.setHeader('Content-Type', 'application/json; charset=utf-8'); res.end(JSON.stringify(value)); };
  if (route === '/health') return send({ environment: '界面验证 · 模拟数据' });
  if (route === '/api/v1/analysis') return send({ runs: [] });
  if (route.endsWith('/trace')) return send({ run_id: 'reader-test', events: [], next_cursor: 0, has_more: false, trace_state: 'not_recorded', execution: {} });
  if (route.endsWith('/report/json')) return send({ document });
  if (route.endsWith('/report')) return send({ report: { content: markdown } });
  if (route === '/api/v1/analysis/reader-test') return send({
    run_id: 'reader-test', status: 'COMPLETED', progress: 100, current_node: 'finalizer',
    repository_url: 'https://example.invalid/client', question: '示例数据：验证报告阅读布局',
  });
  const targets = { '/': 'index.html', '/static/app.css': 'app.css', '/static/app.js': 'app.js', '/static/trace.js': 'trace.js' };
  if (targets[route]) {
    res.setHeader('Content-Type', route.endsWith('.js') ? 'text/javascript; charset=utf-8' :
      route.endsWith('.css') ? 'text/css; charset=utf-8' : 'text/html; charset=utf-8');
    return res.end(fs.readFileSync(path.join(root, 'app/static', targets[route])));
  }
  res.statusCode = 404;
  res.end();
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
    await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
    browser = spawn(executable, ['--headless=new', '--disable-gpu', '--no-first-run',
      '--no-default-browser-check', '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'],
    { windowsHide: true, stdio: 'ignore' });
    browser.on('error', (error) => console.error(error.message));
    let port;
    for (let attempt = 0; attempt < 100; attempt++) {
      const activePort = path.join(profile, 'DevToolsActivePort');
      if (fs.existsSync(activePort)) { port = fs.readFileSync(activePort, 'utf8').split('\n')[0]; break; }
      await delay(100);
    }
    assert(port, 'Browser did not expose a debugging port');
    const targets = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
    client = await connect(targets.find((target) => target.type === 'page').webSocketDebuggerUrl);
    await client.call('Page.enable');
    await client.call('Runtime.enable');
    const evaluate = async (expression) => {
      const result = await client.call('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
      assert(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
      return result.result.value;
    };
    await client.call('Emulation.setDeviceMetricsOverride', { width: 1440, height: 1000, deviceScaleFactor: 1, mobile: false });
    // An old saved preference must be removed when upgrading the page.
    await client.call('Page.addScriptToEvaluateOnNewDocument', {
      source: 'try { localStorage.setItem("aipi-rag", "1"); } catch (e) {}',
    });
    await client.call('Page.navigate', { url: `http://127.0.0.1:${server.address().port}/#/run/reader-test` });
    let loaded = false;
    for (let attempt = 0; attempt < 100; attempt++) {
      loaded = await evaluate('Boolean(document.querySelector(".project-reader"))');
      if (loaded) break;
      await delay(100);
    }
    assert(loaded, 'Report reader did not render');
    assert.equal(await evaluate('document.querySelector("#ragToggle, #ragWarning, #ragHint")'), null);
    assert.equal(await evaluate('localStorage.getItem("aipi-rag")'), null);
    assert.equal(await evaluate('Boolean(document.querySelector("[data-module=rag]"))'), true);
    // Wait for the existing page loader's exit transition before screenshots.
    await delay(650);
    assert.equal(await evaluate('document.querySelectorAll(".reader-chapter").length'), 10);
    assert.equal(await evaluate('document.querySelector(".reader-evidence").open'), false);
    await evaluate(`document.querySelector('.reader-nav a[href="#reader-runtime"]').click()`);
    assert.equal(await evaluate('document.activeElement.id'), 'reader-runtime');
    assert.equal(await evaluate('location.hash'), '#/run/reader-test');
    await evaluate(`document.querySelector('.reader-article a[href^="#reader-e"]').click()`);
    assert.equal(await evaluate('document.querySelector(".reader-evidence").open'), true);
    assert.match(await evaluate('document.activeElement.id'), /^reader-e\d{3}$/);
    assert.equal(await evaluate('location.hash'), '#/run/reader-test');
    // Both UI and Markdown must resolve every citation and keep raw input inert.
    assert.equal(await evaluate(`Array.from(document.querySelectorAll('.reader-article a[href^="#reader-e"]'))
      .every(link => document.getElementById(link.getAttribute('href').slice(1)) !== null)`), true);
    await evaluate('document.querySelector(".reader-evidence").open = false; document.querySelector("#reader-overview").scrollIntoView()');
    await delay(200);
    for (const [name, width, height] of [['desktop', 1440, 1000], ['mobile', 390, 844]]) {
      await client.call('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: name === 'mobile' });
      await evaluate('document.querySelector(".project-reader").scrollIntoView()');
      await delay(150);
      assert.equal(await evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), true, `${name}: horizontal page overflow`);
      const screenshot = await client.call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
      fs.writeFileSync(path.join(output, `report-reader-${name}.png`), Buffer.from(screenshot.data, 'base64'));
      await evaluate('window.scrollTo(0, 0)');
      await delay(150);
      const formScreenshot = await client.call('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
      fs.writeFileSync(path.join(output, `analysis-form-${name}.png`), Buffer.from(formScreenshot.data, 'base64'));
    }
    await evaluate(`document.querySelector('#tabs [data-view="markdown"]').click()`);
    assert.equal(await evaluate(`document.querySelectorAll('#report a[href^="#e"]').length > 0`), true);
    assert.equal(await evaluate(`Array.from(document.querySelectorAll('#report a[href^="#e"]'))
      .every(link => document.getElementById(link.getAttribute('href').slice(1)) !== null)`), true);
    assert.deepEqual(client.errors, []);
    console.log('Browser checks passed: removed RAG controls/preference, retained RAG analysis, chapters, citations, disclosure, URL preservation, desktop/mobile layout and Markdown anchors.');
  } finally {
    if (client) { await client.call('Browser.close').catch(() => {}); client.close(); }
    if (browser && browser.exitCode === null) browser.kill();
    server.closeAllConnections();
    server.close();
  }
})().catch((error) => { console.error(error); process.exitCode = 1; });
