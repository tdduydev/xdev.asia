// Freeze actual animation timelines and profile the finite interaction in Chrome.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH || '/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const url=(process.env.SITE_PREVIEW || 'http://127.0.0.1:4321')+'/vi/ai-studio/';
 await page.goto(url); await page.locator('.workflow-canvas').scrollIntoViewIfNeeded();
 // Freeze actual WAAPI animation objects, rather than use timer-based screenshots.
 for(const [name,time] of [['start',0],['mid',.3],['end',1]]){
  await page.goto(url); await page.locator('.workflow-canvas').scrollIntoViewIfNeeded();
  await page.evaluate(t=>document.querySelectorAll('.studio-landing *').forEach(n=>n.getAnimations().forEach(a=>{a.pause();a.currentTime=t*1000})),time);
  await page.screenshot({path:`/tmp/studio-motion-${name}.png`});
 }
 await page.goto(url); await page.waitForTimeout(1100);
 const cdp=await page.context().newCDPSession(page);
 await page.locator('.workflow-canvas').scrollIntoViewIfNeeded();
 await page.waitForTimeout(280);
 const events=[];cdp.on('Tracing.dataCollected',event=>events.push(...event.value));
 const done=new Promise(resolve=>cdp.once('Tracing.tracingComplete',resolve));
 await cdp.send('Tracing.start',{categories:'devtools.timeline,blink.user_timing',transferMode:'ReportEvents'});
 await page.evaluate(()=>console.timeStamp('motion-start'));
 await page.waitForTimeout(300);
 await page.evaluate(()=>console.timeStamp('motion-end'));
 await cdp.send('Tracing.end');await done;
 const marks=events.filter(e=>e.name==='TimeStamp');
 const start=marks.find(e=>e.args?.data?.message==='motion-start')?.ts;
 const end=marks.find(e=>e.args?.data?.message==='motion-end')?.ts;
 assert(start&&end,'Missing profiling markers');
 const costs=events.filter(e=>e.ts>start+20000&&e.ts<end&&['Layout','Paint'].includes(e.name));
 fs.writeFileSync('/tmp/studio-motion-trace.json',JSON.stringify({traceEvents:events}));
 console.log('Mid-flight SVG/connector trace (after startup):',JSON.stringify({layout:costs.filter(e=>e.name==='Layout').length,paint:costs.filter(e=>e.name==='Paint').length,durationMs:(end-start)/1000}));
 await page.waitForFunction(()=>document.querySelector('.workflow-canvas').dataset.stage==='6');
 await page.waitForTimeout(350);
 await page.screenshot({path:'/tmp/studio-motion-complete.png'});
 await page.locator('.studio-tab').nth(2).click();
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.waitForTimeout(30);
 assert(await page.evaluate(()=>document.getAnimations().filter(a=>a.playState==='running').every(a=>a.effect.getKeyframes().every(f=>!f.transform||f.transform==='none'))),'Live reduced-motion kept displacement');
 await page.locator('.studio-tab').nth(1).click();
 const reducedFrames=await page.locator('.studio-screen:visible').evaluate(n=>n.getAnimations().flatMap(a=>a.effect.getKeyframes()));
 assert(reducedFrames.length>0,'Reduced mode should preserve short opacity feedback');
 assert(reducedFrames.every(f=>!f.transform));
 await page.waitForTimeout(200);
 await page.screenshot({path:'/tmp/studio-motion-reduced.png'});
 await page.emulateMedia({reducedMotion:'no-preference'});
 await page.locator('.studio-tab').first().click();
 await page.waitForTimeout(300);
 const first=await page.locator('.studio-tab').first().boundingBox();
 const indicator=await page.locator('.studio-tab-indicator').boundingBox();
 assert(Math.abs(first.x-indicator.x)<1 && Math.abs(first.width-indicator.width)<1,'Underline target mismatch');
 await browser.close();
 console.log('PASS: deterministic start/mid/end screenshots; SVG final state; live reduced-motion cancellation; opacity feedback retained; indicator geometry.');
})().catch(e=>{console.error(e);process.exit(1)});
