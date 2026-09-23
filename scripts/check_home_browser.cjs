// Build and serve dist; exercises the bilingual homepage and finite canvas scene.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const origin=process.env.SITE_PREVIEW || 'http://127.0.0.1:4321';
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 await page.addInitScript(()=>{const original=requestAnimationFrame;window.frameCalls=0;window.requestAnimationFrame=callback=>original(time=>{window.frameCalls++;callback(time)})});
 for(const locale of ['en','vi']){
  const path=locale==='vi'?'/vi/':'/';
  for(const width of [1440,1024,768,390,320]){
   await page.setViewportSize({width,height:1000});
   assert.equal((await page.goto(origin+path)).status(),200);
   await page.waitForFunction(()=>document.querySelector('.x-canvas').dataset.rendered==='true');
   assert.equal(await page.locator('html').getAttribute('lang'),locale);
   assert(!(await page.locator('.x-art-fallback').isVisible()), 'Static fallback overlaps live sculpture');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${locale} ${width} overflow`);
   for(let i=0;i<3;i++){
    await page.locator('.x-preview-tabs a').nth(i).click();
    assert.equal(await page.locator('.x-product-screen:visible').count(),1);
    const shot=page.locator('.x-product-screen:visible img');
    await shot.evaluate(n=>n.decode());
    assert((await shot.getAttribute('src')).endsWith(`.${locale}.png`));
   }
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
  await page.locator('.x-preview-tabs a').first().focus();await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('.x-preview-tabs a').nth(1).getAttribute('aria-selected'),'true');
  await page.keyboard.press('End');assert.equal(await page.locator('.x-preview-tabs a').nth(2).getAttribute('aria-selected'),'true');
  await page.keyboard.press('Home');assert.equal(await page.locator('.x-preview-tabs a').first().getAttribute('aria-selected'),'true');
  await page.locator('[data-art-turn]').click();
  await page.waitForFunction(()=>document.querySelector('.x-canvas').dataset.moving==='false');
  assert(!(await page.locator('[data-art-turn]').isDisabled()));
  await page.locator('[data-art-structure]').click();
  assert.equal(await page.locator('[data-art-structure]').getAttribute('aria-pressed'),'true');
  await page.waitForFunction(()=>document.querySelector('.x-canvas').dataset.moving==='false');
  await page.locator('[data-art-reset]').click();
  assert.equal(await page.locator('[data-art-structure]').getAttribute('aria-pressed'),'false');
  await page.waitForFunction(()=>document.querySelector('.x-canvas').dataset.moving==='false');
  const idleFrames=await page.evaluate(()=>window.frameCalls);await page.waitForTimeout(350);
  assert.equal(await page.evaluate(()=>window.frameCalls),idleFrames,'Canvas still renders while idle');
  await page.locator(`.language-switch a[lang="${locale==='en'?'vi':'en'}"]`).click();
  assert.equal(await page.locator('html').getAttribute('lang'),locale==='en'?'vi':'en');
 }
 await page.setViewportSize({width:1440,height:1000});await page.goto(origin+'/vi/');
 await page.waitForTimeout(1800);
 await page.screenshot({path:'/tmp/xdev-home-desktop.png',fullPage:true});
 await page.locator('[data-art-structure]').click();await page.waitForTimeout(1200);
 await page.screenshot({path:'/tmp/xdev-home-structure.png'});
 await page.locator('[data-art-turn]').click();
 await page.emulateMedia({reducedMotion:'reduce'});await page.waitForTimeout(200);
 assert.equal(await page.locator('.x-canvas').getAttribute('data-moving'),'false');
 assert(!(await page.locator('[data-art-turn]').isDisabled()));
 await page.locator('[data-art-turn]').click();
 assert.equal(await page.locator('.x-canvas').getAttribute('data-moving'),'false');
 await page.locator('.x-preview-tabs a').nth(1).click();
 const frames=await page.locator('.x-product-screen:visible').evaluate(n=>n.getAnimations().flatMap(a=>a.effect.getKeyframes()));
 assert(frames.length>0&&frames.every(f=>!f.transform),'Reduced mode must keep fade without translation');
 await page.setViewportSize({width:390,height:1000});await page.goto(origin+'/vi/');await page.waitForTimeout(200);
 await page.screenshot({path:'/tmp/xdev-home-mobile.png',fullPage:true});
 await page.locator('.x-workbench-heading a').click();
 assert.equal(new URL(page.url()).pathname,'/vi/ai-studio/');
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:1000}});
 for(const path of ['/','/vi/']){
  await nojs.goto(origin+path);
  assert(await nojs.locator('.x-art-fallback').isVisible());
  assert.equal(await nojs.locator('.x-product-screen:visible').count(),3);
  assert(!(await nojs.locator('.x-art-controls').isVisible()));
  await nojs.locator('.x-preview-tabs a').nth(2).click();assert.equal(new URL(nojs.url()).hash,'#x-screen-2');
  assert(await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 }
 const fallback=await browser.newPage();
 await fallback.addInitScript(()=>{HTMLCanvasElement.prototype.getContext=()=>null});
 await fallback.goto(origin);
 assert(await fallback.locator('.x-art-fallback').isVisible());
 assert(!(await fallback.locator('.x-art-controls').isVisible()));
 assert.deepEqual(errors,[]);
 await browser.close();
 console.log('PASS: home EN/VI at 320/390/768/1024/1440; localized product images; keyboard tabs; sculpture rotate/structure/reset; no idle frame loop; live reduced motion; no-JS and canvas fallback; local product navigation; zero browser errors.');
})().catch(error=>{console.error(error);process.exit(1)});
