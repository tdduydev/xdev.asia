const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const {pages}=require('../src/studio.en.json');
const origin=process.env.SITE_PREVIEW || 'http://127.0.0.1:4321';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/usr/bin/google-chrome',args:['--no-sandbox']});
 const page=await browser.newPage({javaScriptEnabled:false});
 for(const prefix of ['', '/vi']){
  for(const width of [1440,1024,768,390,320]){
   await page.setViewportSize({width,height:1000});
   await page.goto(`${origin}${prefix}/ai-studio/docs/`);
   assert.equal(await page.locator('.docs-topic').count(),8);
   assert.equal(await page.locator('.docs-topic-links a').count(),pages.length);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(width===1440)await page.screenshot({path:`/tmp/xdev-docs-index${prefix?'-vi':''}.png`,fullPage:true});
   await page.goto(`${origin}${prefix}/ai-studio/docs/workflows/`);
   const nav=width<=850?'.mobile-doc-nav':'.desktop-doc-nav';
   if(width<=850)await page.locator('.mobile-doc-nav > summary').click();
   assert.equal(await page.locator(`${nav} .docs-group[open]`).count(),1);
   assert.equal(await page.locator(`${nav} [aria-current=page]`).textContent(),prefix?'Thiết kế workflow trực quan':'Design visual workflows');
   const summary=page.locator(`${nav} .docs-group[open] > summary`);
   await summary.focus();await page.keyboard.press('Enter');
   assert.equal(await page.locator(`${nav} .docs-group[open]`).count(),0);
   await page.keyboard.press('Enter');
   assert.equal(await page.locator(`${nav} .docs-group[open]`).count(),1);
   if(width<=850)await page.locator('.mobile-doc-nav > summary').click();
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   assert(await page.locator('.article-toc').isVisible());
   await page.goto(`${origin}${prefix}/ai-studio/docs/workflow-nodes/`);
   if(width<=850)await page.locator('.mobile-doc-nav > summary').click();
   assert(await page.locator(`${nav} .docs-family[open] [aria-current=page]`).isVisible());
   for(const child of await page.locator(`${nav} .docs-family[open] a`).all())assert(await child.isVisible());
   if(width<=850)await page.locator('.mobile-doc-nav > summary').click();
   await page.locator('.docs-breadcrumb a').last().click();
   assert.equal(new URL(page.url()).hash,'#topic-build');
  }
  for(const entry of pages){
   await page.goto(`${origin}${prefix}/ai-studio/docs/${entry.slug}/`);
   assert.equal(await page.locator('.desktop-doc-nav .docs-group[open] [aria-current=page]').count(),1);
  }
 }
 await page.setViewportSize({width:1440,height:1000});await page.goto(`${origin}/vi/ai-studio/docs/quickstart/`);
 await page.screenshot({path:'/tmp/xdev-docs-article-vi.png'});
 await browser.close();console.log('PASS: EN/VI topic inventory; all active article groups; keyboard collapse/expand; topic breadcrumbs; visible TOC and no overflow at five widths, without JavaScript.');
})().catch(e=>{console.error(e);process.exitCode=1});
