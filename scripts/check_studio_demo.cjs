const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');const assert=require('node:assert/strict');
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});const p=await b.newPage({viewport:{width:1440,height:1000}});const origin=process.env.SITE_PREVIEW||'http://127.0.0.1:4321';const errors=[];p.on('pageerror',e=>errors.push(e.message));
for(const locale of ['en','vi']){
 await p.goto(origin+(locale==='vi'?'/vi':'')+'/ai-studio/');
 assert.equal(await p.locator('[data-demo-run]').count(),0);
 await p.locator('.workflow-canvas').scrollIntoViewIfNeeded();
 const dot=p.locator('.workflow-data-particle').first();
 await p.waitForFunction(()=>Number(document.querySelector('.workflow-data-particle').style.opacity)>0);
 const position=()=>dot.evaluate(n=>[n.getAttribute('cx'),n.getAttribute('cy')].join(','));
 const before=await position();await p.waitForTimeout(250);assert.notEqual(await position(),before);
 await p.locator('[data-flow-pause]').click();const paused=await position();await p.waitForTimeout(250);assert.equal(await position(),paused);
 await p.locator('[data-flow-pause]').click();await p.locator('.workflow-canvas').scrollIntoViewIfNeeded();
 await p.waitForFunction(()=>document.querySelector('.workflow-canvas').dataset.stage==='6');
 assert.equal(await p.locator('.studio-node.is-complete').count(),6);
 assert.equal(await p.locator('[data-edge].is-traversed').count(),5);
 await p.waitForFunction(()=>document.querySelector('.workflow-canvas').dataset.stage==='0');
 await p.locator('footer').scrollIntoViewIfNeeded();await p.waitForTimeout(200);const hiddenPosition=await position();await p.waitForTimeout(300);assert.equal(await position(),hiddenPosition);
 await p.emulateMedia({reducedMotion:'reduce'});
 for(let i=0;i<3;i++){await p.locator('[data-scenario]').selectOption(String(i));assert.equal(await p.locator('[data-output-text]').textContent(),await p.locator('[data-scenario] option').nth(i).getAttribute('data-scenario-result'));}
 assert(!await p.locator('[data-flow-pause]').isVisible());assert.equal(await dot.evaluate(n=>n.style.opacity),'0');
 assert.equal(await p.locator('.studio-booking-contact a').getAttribute('href'),'https://www.facebook.com/duydev/');
 for(const width of [1440,768,390,320]){await p.setViewportSize({width,height:1000});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));const box=await p.locator('.workflow-canvas').boundingBox();assert(Math.abs(box.width/box.height-16/9)<.01);}
 await p.emulateMedia({reducedMotion:'no-preference'});await p.setViewportSize({width:1440,height:1000});
}
assert.deepEqual(errors,[]);await b.close();console.log('PASS: EN/VI autoplay, moving data particles, pause/resume, completion and loop, offscreen stop, reduced motion, scenario results, 16:9 and responsive layouts.');})().catch(e=>{console.error(e);process.exit(1)});
