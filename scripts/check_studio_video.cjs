const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');
const root=path.resolve(__dirname,'..');const origin=process.env.SITE_PREVIEW||'http://127.0.0.1:4321';
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 for(const lang of ['en','vi']){
  const route=`${lang==='vi'?'/vi':''}/ai-studio/`;
  const guides=JSON.parse(fs.readFileSync(`${root}/src/studio.${lang}.json`)).pages;
  for(const width of [1440,768,390,320]){
   await page.setViewportSize({width,height:1000});await page.goto(origin+route);
   assert.equal(await page.locator('.feature-items>a').count(),guides.length);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  }
  const video=page.locator('#studio-tour');
  assert.equal((await page.request.get(await video.evaluate(v=>v.poster))).status(),200);
  await video.scrollIntoViewIfNeeded();
  await page.waitForFunction(()=>document.querySelector('#studio-tour').readyState>=2);
  const initial=await video.evaluate(v=>({duration:v.duration,source:v.currentSrc,muted:v.muted,track:v.textTracks[0].language}));
  assert(initial.duration>=300&&initial.duration<=420,JSON.stringify(initial));
  assert(initial.source.endsWith(`ai-studio.${lang}.mp4`));assert.equal(initial.track,lang);assert(!initial.muted);
  const chapters=page.locator('[data-video-seek]');assert.equal(await chapters.count(),7);
  for(const i of [0,3,6]){
   const start=Number(await chapters.nth(i).getAttribute('data-video-seek'));
   await chapters.nth(i).click();
   await page.waitForFunction(t=>{const v=document.querySelector('#studio-tour');return !v.paused&&v.currentTime>=t&&v.currentTime<t+5},start);
   await page.waitForTimeout(400);
   assert(await video.evaluate(v=>v.webkitDecodedFrameCount>0));
   assert(await video.evaluate(v=>v.webkitAudioDecodedByteCount>0));
   await video.evaluate(v=>v.pause());
  }
  await page.waitForFunction(()=>document.querySelector('#studio-tour').textTracks[0].cues?.length>0);
  const cueState=await video.evaluate(v=>{const cues=[...v.textTracks[0].cues];return {count:cues.length,last:cues.at(-1).endTime,valid:cues.every(c=>c.endTime>c.startTime&&c.endTime<=v.duration+1)}});
  assert(cueState.valid&&cueState.count>60,JSON.stringify(cueState));
  const downloaded=page.waitForEvent('download');await page.locator('.studio-video-links a').first().click();
  assert.equal((await downloaded).suggestedFilename(),`ai-studio.${lang}.mp4`);
  await page.locator('.video-transcript summary').click();assert(await page.locator('.video-transcript section').first().isVisible());
  await page.setViewportSize({width:1440,height:1000});await page.locator('#video').scrollIntoViewIfNeeded();await page.screenshot({path:`/tmp/xdev-video-page-${lang}.png`});
 }
 const nojs=await browser.newPage({javaScriptEnabled:false});await nojs.goto(origin+'/vi/ai-studio/');assert(await nojs.locator('#studio-tour').getAttribute('controls')!==null);assert.equal(await nojs.locator('.studio-video nav noscript').count(),7);
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS: 60 feature links per locale; localized video/audio decoding, 5–7 minute duration, captions, chapter seek/play, downloads, transcripts, no-JS fallback and responsive layouts.');
})().catch(e=>{console.error(e);process.exit(1)});
