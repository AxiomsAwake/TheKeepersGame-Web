// Test the shipped WebAssembly/PCK pair, rather than a separate browser port.
const { chromium } = require('playwright');
const { PNG } = require('pngjs');
const { mkdirSync, writeFileSync } = require('node:fs');
const assert = require('node:assert/strict');

function changedPixels(a, b) {
  const first = PNG.sync.read(a), second = PNG.sync.read(b);
  assert.equal(first.data.length, second.data.length);
  let changed = 0;
  for (let i = 0; i < first.data.length; i += 4) {
    if (Math.abs(first.data[i] - second.data[i]) + Math.abs(first.data[i+1] - second.data[i+1]) + Math.abs(first.data[i+2] - second.data[i+2]) > 45) changed++;
  }
  return changed;
}

(async () => {
  mkdirSync('artifacts', { recursive: true });
  const browser = await chromium.launch({ headless: true, args: [
    '--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
  ] });
  try {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('console', message => {
      if (/SCRIPT ERROR|Parse Error|Compile Error|Aborted\(|WebGL.*CONTEXT_LOST/.test(message.text())) errors.push(message.text());
    });
    await page.goto(process.env.GAME_URL || 'http://127.0.0.1:4173/', { waitUntil: 'domcontentloaded' });
    await page.locator('#status').waitFor({ state: 'hidden', timeout: 90000 });
    const canvas = page.locator('#canvas');
    await canvas.waitFor({ state: 'visible' });
    await page.waitForTimeout(800); // Allow the first rendered scene to reach the capture surface.
    assert.match(await page.locator('#release-info').innerText(), /v0\.1\.0-demo\.4/);
    const capture = async name => {
      const image = await page.screenshot();
      writeFileSync(`artifacts/${name}.png`, image);
      return image;
    };
    const briefing = await capture('web-briefing');
    await canvas.press('Enter');
    await canvas.press('q');
    await canvas.press('w');
    await canvas.press('3');
    await page.mouse.click(720, 370);
    await page.waitForTimeout(2500); // Commands resolve through the game's fixed simulation ticks.
    await page.mouse.move(10, 890);
    await capture('web-playing');
    await canvas.press('Space');
    await page.waitForTimeout(300);
    const arena = await capture('web-arena-3d');
    const badge = await page.locator('#release-info summary').boundingBox();
    assert.ok(badge.y >= 876, 'The release badge must stay below the command rail, clear of match status.');
    assert.ok(changedPixels(briefing, arena) > 10000, 'Starting the game must replace the briefing with a rendered battle.');
    await page.mouse.move(720, 325); // Projected north relay in the reset camera at 1440 × 900.
    await page.waitForTimeout(300);
    const inspection = await capture('web-relay-inspection');
    assert.ok(changedPixels(arena, inspection) > 800, 'Paused hover must reveal the relay inspection card.');
    await page.mouse.move(10, 890);
    await canvas.press('v');
    await page.waitForTimeout(300);
    const ground = await capture('web-ground-view');
    assert.ok(changedPixels(arena, ground) > 10000, 'Ground view must visibly change the 3D projection.');
    await canvas.press('Home');
    await canvas.press('i');
    await page.waitForTimeout(300);
    await capture('web-influence');
    await canvas.press('r');
    await page.waitForTimeout(300);
    const restarted = await capture('web-restarted');
    assert.ok(changedPixels(ground, restarted) > 10000, 'Restart must return from ground view to the briefing.');
    assert.deepEqual(errors, [], 'The exported game must run without script or WebGL context failures.');
    writeFileSync('artifacts/browser-result.json', JSON.stringify({
      version: 'v0.1.0-demo.4', result: 'passed', renderer: 'Chromium WebGL2 / SwiftShader',
      exercised: ['start', 'Scout and Guardian deploy', 'Assault doctrine', 'rally', 'pause', 'paused relay inspection', 'ground camera', 'camera reset', 'influence overlay', 'restart'],
      limits: 'Pixel assertions establish rendered scene changes; deterministic gameplay correctness is covered by the source repository rule and presentation tests. This is not a human playtest.'
    }, null, 2));
    console.log('Compiled 3D Web release smoke checks passed.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
