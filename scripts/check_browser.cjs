// Run after build.py with the generated site served locally.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const origin=process.env.SITE_PREVIEW || 'http://127.0.0.1:4321';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000},javaScriptEnabled:false});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));
 const entries=JSON.parse(fs.readFileSync(path.join(__dirname,'../src/studio.en.json'))).pages;
 for(const locale of ['en','vi'])for(const entry of entries){
   const prefix=locale==='vi'?'/vi':'';
   const response=await page.goto(`${origin}${prefix}/ai-studio/docs/${entry.slug}/`);
   assert.equal(response.status(),200);
   assert.equal(await page.locator('html').getAttribute('lang'),locale);
   const shots=page.locator('.guide-figure img');
   assert(await shots.count()>0);
   for(const image of await shots.all()){
     await image.scrollIntoViewIfNeeded();
     await image.evaluate(node=>node.decode());
     assert.equal(await image.evaluate(node=>node.naturalWidth),1440);
   }
   assert.equal(await page.locator('a[href*="https://ai-studio.xdev.asia"]').count(),0);
 }
 await page.goto(`${origin}/ai-studio/docs/quickstart/`);
 await page.locator('.language-switch a[lang="vi"]').click();
 assert.equal(new URL(page.url()).pathname,'/vi/ai-studio/docs/quickstart/');
 await page.locator('.article-toc a').nth(2).click();
 assert.equal(new URL(page.url()).hash,'#section-3');
 await page.waitForTimeout(700);
 await page.locator('.guide-figure a').first().scrollIntoViewIfNeeded();
 await page.waitForTimeout(700);
 const [popup]=await Promise.all([page.context().waitForEvent('page'),page.locator('.guide-figure a').first().click()]);
 await popup.waitForLoadState();assert.equal(new URL(popup.url()).origin,origin);assert(popup.url().endsWith('.vi.png'));await popup.close();
 for(const width of [1440,768,390,320]){
   await page.setViewportSize({width,height:1000});
   await page.goto(`${origin}/vi/ai-studio/docs/quickstart/`);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);
 }
 await page.locator('.mobile-doc-nav > summary').click();
 assert(await page.locator('.mobile-doc-nav').evaluate(n=>n.open));
 await page.locator('.mobile-doc-nav > summary').click();
 await page.locator('.guide-figure img').evaluateAll(nodes=>Promise.all(nodes.map(n=>{n.loading='eager';return n.decode()})));
 await page.screenshot({path:'/tmp/xdev-manual-mobile.png',fullPage:true});
 await page.setViewportSize({width:1440,height:1000});
 await page.goto(`${origin}/ai-studio/docs/quickstart/`);
 await page.locator('#section-3').scrollIntoViewIfNeeded();
 await page.locator('.guide-figure img').evaluateAll(nodes=>Promise.all(nodes.map(n=>{n.loading='eager';return n.decode()})));
 await page.waitForTimeout(700);
 await page.screenshot({path:'/tmp/xdev-manual-desktop.png'});
 await page.goto(origin);await page.locator('a[href="ai-studio/"]').first().click();
 assert.equal(new URL(page.url()).pathname,'/ai-studio/');
 assert.equal(await page.locator('a[href*="https://ai-studio.xdev.asia"]').count(),0);
 assert.deepEqual(errors,[]);
 console.log('PASS: all illustrated articles; all screenshots decoded; EN/VI same-article switch; local image zoom; table of contents; no app-domain links; 1440/768/390/320 layouts; navigation works without JavaScript.');
 await browser.close();
})().catch(error=>{console.error(error);process.exitCode=1;});
