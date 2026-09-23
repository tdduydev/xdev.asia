// Render branded video frames from localized, synthetic-data product screenshots.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs');const path=require('node:path');const {pathToFileURL}=require('node:url');
const root=path.resolve(__dirname,'..');
const escape=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/usr/bin/google-chrome',args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
 for(const lang of ['vi','en']){
  const slides=JSON.parse(fs.readFileSync(`${root}/docs/video/script.${lang}.json`));
  const out=`/tmp/xdev-video/${lang}`;fs.mkdirSync(out,{recursive:true});
  for(const [i,s]of slides.entries()){
   const asset=`${root}/src/assets/ai-studio/${['documents','retrieval'].includes(s.slug)?s.slug:s.image}.${lang}.png`;
   const html=`<!doctype html><meta charset="utf-8"><style>*{box-sizing:border-box}body{margin:0;background:#f4f7fc;font-family:Arial,sans-serif;color:#172b4c}header{display:flex;align-items:center;justify-content:space-between;padding:20px 38px;height:90px;border-bottom:1px solid #dae4f1}header img{width:155px;height:65px}header span{font-size:17px;color:#536984}.layout{display:grid;grid-template-columns:310px 1fr;gap:28px;padding:32px 38px 18px;height:565px}.copy{padding-top:12px}.chapter{font-size:14px;color:#0759ed;font-weight:bold;line-height:1.6}h1{font-size:32px;line-height:1.2;letter-spacing:-1px;margin:23px 0}p{font-size:18px;line-height:1.65;color:#536984}.screen{display:flex;align-items:center;justify-content:center;overflow:hidden;background:#fff;border:1px solid #d9e2ef;border-radius:12px;box-shadow:0 16px 40px #223b6210}.screen img{width:100%;height:auto;display:block}footer{padding:15px 38px;font-size:12px;color:#536984;display:flex;justify-content:space-between;border-top:1px solid #dae4f1}.progress{height:4px;background:#dbe7fa;position:absolute;bottom:0;left:0;right:0}.progress span{display:block;height:100%;background:#0759ed;width:${(i+1)/slides.length*100}%}</style><header><img src="${pathToFileURL(root+'/src/assets/brand/wordmark-v2/ai-studio-light.svg')}"><span>${lang==='vi'?'Khám phá AI Studio':'Explore AI Studio'}</span></header><div class="layout"><div class="copy"><div class="chapter">${lang==='vi'?'Chương':'Chapter'} ${s.chapter} / 7<br>${escape(s.chapter_title)}</div><h1>${escape(s.title)}</h1><p>${escape(s.description)}</p></div><div class="screen"><img src="${pathToFileURL(asset)}"></div></div><footer><span>${lang==='vi'?'Giao diện minh họa · Giọng đọc tổng hợp':'Illustrative screens · Synthetic narration'}</span><span>xdev.asia · ${String(i+1).padStart(2,'0')} / ${slides.length}</span></footer><div class="progress"><span></span></div>`;
   const file=`${out}/frame.html`;fs.writeFileSync(file,html);
   await page.goto(pathToFileURL(file).href);await page.locator('img').evaluateAll(ns=>Promise.all(ns.map(n=>n.decode())));
   if(await page.locator('.copy').evaluate(n=>n.scrollHeight>n.clientHeight))throw Error('Text overflow '+s.slug);
   await page.screenshot({path:`${out}/${String(i).padStart(2,'0')}.png`});
  }
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
