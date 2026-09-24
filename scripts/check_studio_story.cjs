const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
const origin=process.env.SITE_PREVIEW||'http://127.0.0.1:64572';
(async()=>{
 const b=await chromium.launch({executablePath:'/usr/bin/google-chrome',args:['--no-sandbox']});
 const p=await b.newPage();const errors=[];p.on('pageerror',e=>errors.push(e.message));
 for(const lang of ['vi','en']){
  await p.goto(`${origin}/${lang==='vi'?'vi/':''}ai-studio/#story`);
  const v=p.locator('#studio-story');await v.scrollIntoViewIfNeeded();
  await p.waitForFunction(()=>document.querySelector('#studio-story').readyState>=2);
  assert(await v.evaluate(n=>n.duration>300&&n.duration<480&&n.videoWidth===1280&&n.videoHeight===720));
  assert.equal(await v.locator('track').getAttribute('srclang'),lang);
  await p.locator('.story-index > summary').click();
  const chapters=p.locator('[data-story-seek]');assert.equal(await chapters.count(),16);
  for(const i of [0,2,4,5,6,7,8,15]){
   const time=Number(await chapters.nth(i).getAttribute('data-story-seek'));await chapters.nth(i).click();
   await p.waitForFunction(t=>{let v=document.querySelector('#studio-story');return !v.paused&&v.currentTime>=t&&v.currentTime<t+3},time);
   await p.waitForTimeout(550);assert(await v.evaluate(n=>n.webkitDecodedFrameCount>0&&n.webkitAudioDecodedByteCount>0));await v.evaluate(n=>n.pause());
  }
  await p.waitForFunction(()=>document.querySelector('#studio-story').textTracks[0].cues?.length>0);
  assert(await v.evaluate(n=>[...n.textTracks[0].cues].every(c=>c.endTime>c.startTime&&c.endTime<n.duration)));
  await p.locator('.story-transcript summary').click();assert(await p.locator('.story-transcript section').last().isVisible());
  for(const width of [1440,390,320]){await p.setViewportSize({width,height:1000});assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
  await p.goto(`${origin}/assets/ai-studio/story/story.${lang}.html`);await p.waitForSelector('audio');
  const topology=await p.evaluate(()=>{
    const result={}; for(const kind of ['approval','security','sandbox','custom']){
      const s=STORY.scenes.find(s=>s.kind===kind);__drawFrame(Math.floor((s.start+12)*24));result[kind]=STORY_GEOMETRY;
    } return result;
  });
  assert(topology.approval.some(e=>e.source==='draft'&&e.target==='human'));
  assert(topology.approval.some(e=>e.source==='human'&&e.target==='api'));
  assert(!topology.approval.some(e=>e.source==='draft'&&e.target==='api'));
  assert(topology.security.some(e=>e.blocked&&e.target==='stop'));
  assert(!topology.security.some(e=>e.target==='ext'));
  assert(topology.sandbox.some(e=>e.source==='code'&&e.target==='sandbox'));
  for(const edges of Object.values(topology))for(const e of edges){
    const [x,y,w,h]=e.targetBox;const [X,Y]=e.to;
    assert(Math.abs(X-x)<=w/2+.01&&Math.abs(Y-y)<=h/2+.01);
    assert(Math.abs(Math.abs(X-x)-w/2)<.01||Math.abs(Math.abs(Y-y)-h/2)<.01);
  }
  const equal=await p.evaluate(()=>{const a=__frame(600);__frame(72);return a===__frame(600)});assert(equal);
  await p.locator('audio').evaluate(a=>a.play());await p.waitForTimeout(350);assert(await p.locator('audio').evaluate(a=>a.currentTime>0));await p.locator('audio').evaluate(a=>a.pause());
 }
 assert.deepEqual(errors,[]);await b.close();console.log('PASS: both story films, audio/video decoding, 16 chapters and key scene seeks, captions, transcript, 3 widths, deterministic Canvas seeking and narrated offline HTML.');
})().catch(e=>{console.error(e);process.exit(1)});
