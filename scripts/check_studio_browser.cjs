// Build and serve dist before running this product-page interaction check.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1050}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const origin=process.env.SITE_PREVIEW || 'http://127.0.0.1:4321';
 for(const locale of ['en','vi']){
  const route=(locale==='vi'?'/vi':'')+'/ai-studio/';
  for(const width of [1440,1024,768,390,320]){
   await page.setViewportSize({width,height:1050});
   assert.equal((await page.goto(origin+route)).status(),200);
   await page.locator('[data-flow-pause]').waitFor({state:'visible'});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${locale} overflow at ${width}`);
   for(let i=0;i<4;i++){
    await page.locator('.studio-tab').nth(i).click();
    const panel=page.locator('.studio-panel').nth(i);
    assert(await panel.isVisible());
    assert.equal(await page.locator('.studio-panel:visible').count(),1);
    await panel.locator('img').evaluate(n=>n.decode());
    assert((await panel.locator('img').getAttribute('src')).endsWith(`.${locale}.png`));
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   }
   await page.locator('.studio-tab').first().click();
   if(width===1440||width===390){
    await page.evaluate(()=>scrollTo(0,0)); await page.waitForTimeout(850);
    await page.screenshot({path:`/tmp/studio-redesign-${locale}-${width}.png`,fullPage:true});
   }
  }
  await page.locator('.studio-tab').first().focus();
  await page.keyboard.press('ArrowRight');
  assert.equal(await page.locator('.studio-tab').nth(1).getAttribute('aria-selected'),'true');
  await page.keyboard.press('End');
  assert.equal(await page.locator('.studio-tab').nth(3).getAttribute('aria-selected'),'true');
  await page.keyboard.press('Home');
  assert.equal(await page.locator('.studio-tab').first().getAttribute('aria-selected'),'true');
  await page.locator('.language-switch select').selectOption({label:locale==='en'?'Tiếng Việt':'English'});
  assert.equal(await page.locator('html').getAttribute('lang'),locale==='en'?'vi':'en');
 }
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto(origin+'/vi/ai-studio/');
 assert.equal(await page.locator('.studio-blueprint').evaluate(n=>getComputedStyle(n).animationName),'none');

 assert.equal(await page.locator('.studio-node.is-complete').count(),6);
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:900}});
 for(const route of ['/ai-studio/','/vi/ai-studio/']){
  await nojs.goto(origin+route);
  assert.equal(await nojs.locator('.studio-panel:visible').count(),4);
  await nojs.locator('.studio-tab').nth(2).click();
  assert.equal(new URL(nojs.url()).hash,'#studio-panel-2');
  assert(await nojs.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 }
 assert.deepEqual(errors,[]);
 await browser.close();
 console.log('PASS: EN/VI, 5 widths (320–1440), all 4 tabs and localized images, keyboard arrows/Home/End, automatic workflow, reduced motion, no-JS anchor fallback, zero browser errors.');
})().catch(e=>{console.error(e);process.exit(1)});
