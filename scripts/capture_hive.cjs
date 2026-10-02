// Render the real Hive UI against a disposable, loopback-only demo hub.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const {spawn} = require('node:child_process');
const {randomBytes} = require('node:crypto');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname,'..');
const hive = path.resolve(process.env.HIVE_SOURCE || path.join(root,'../xdev-hive'));
const work = fs.mkdtempSync(path.join(os.tmpdir(),'hive-showcase-'));
const out = path.join(root,'src/assets/hive');
const base = 'http://127.0.0.1:7799';
const token = randomBytes(32).toString('hex');
let browser;
const server = spawn(process.execPath,['src/server.ts'],{cwd:path.join(hive,'apps/web'),env:{...process.env,NODE_ENV:'production',HIVE_PORT:'7799',HIVE_HOST:'127.0.0.1',HIVE_DB:path.join(work,'hub.db'),HIVE_BOOTSTRAP_TOKEN:token,HIVE_ADMIN_USER:'showcase'},stdio:'ignore'});
const pause = ms=>new Promise(r=>setTimeout(r,ms));
async function rpc(method,input) {
 const r=await fetch(base+'/api/rpc',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+token},body:JSON.stringify({method,input})});
 const data=await r.json(); if(data.error) throw Error(method+': '+data.error.message); return data.result;
}
(async()=>{
 let ready=false;for(let i=0;i<100;i++){ready=await fetch(base+'/api/health').then(r=>r.ok,()=>false);if(ready)break;await pause(100)}
 if(!ready)throw Error('Demo hub did not start');
 for(const [key,title,content] of [
  ['org/coding-style','Coding standards','# Coding standards\n\n- Use the project conventions.\n- Explain why in comments.\n- Run typecheck and tests before review.'],
  ['project/atlas/agents','Atlas / Agent protocol','# Atlas — Agent protocol\n\n## Before you start\nRead shared memory. Claim a task. Work on a separate branch.\n\n## Before review\nRun the checks. Record decisions. Submit results for human review.'],
  ['project/atlas/architecture','Atlas / Architecture','# Atlas — Architecture\n\n```mermaid\nflowchart LR\n  UI[Web app] --> API[API service]\n  API --> DB[(Database)]\n```\n\nKeep business rules in the service layer.'],
  ['org/skills/code-review','Code review','---\nname: code-review\ndescription: Review a change for correctness, security and regression risk.\n---\n\nRead the task and diff. Check boundary cases. Report actionable findings with file references.'],
  ['project/atlas/skills/verify-change','Verify a change','---\nname: verify-change\ndescription: Validate an Atlas change before review.\n---\n\nRun typecheck and tests. Record what passed and any limitations.']
 ])await rpc('docs.save',{key,title,content,baseVersion:0});
 for(const [id,title]of [['AT-101','Add project onboarding'],['AT-102','Review the authentication flow'],['AT-103','Document API retry behavior'],['AT-104','Verify the release build']])await rpc('tasks.create',{id,project:'atlas',title});
 await rpc('tasks.claim',{id:'AT-102'});await rpc('tasks.update',{id:'AT-103',status:'review',note:'Tests passed. Ready for review.'});await rpc('tasks.update',{id:'AT-104',status:'done',note:'Build verified.'});
 for(const [kind,content]of [['decision','Keep validation in the service layer so desktop and web follow the same rules.'],['gotcha','Retry requests with the same idempotency key. A duplicate operation returns the original result.'],['convention','Run typecheck and focused tests before requesting review.']])await rpc('memory.write',{project:'atlas',kind,content,files:[]});
 await rpc('proposals.create',{docKey:'project/atlas/agents',baseVersion:1,content:'# Atlas — Agent protocol\n\nRead memory, claim a task, and use a separate branch.\n\nRun typecheck, unit tests and the release build before review.\n',reason:'Include release build verification in the project protocol.'});
 browser=await chromium.launch({executablePath:process.env.CHROME_PATH||'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 fs.mkdirSync(out,{recursive:true});
 for(const locale of ['vi','en']){
  const page=await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:1});
  await page.addInitScript(({token,locale})=>{localStorage.setItem('xdev-hive.token',token);localStorage.setItem('xdev-hive.locale',locale);localStorage.setItem('theme','light')},{token,locale});
  for(const [name,route]of [['docs','admin/docs'],['memory','admin/memory'],['skills','admin/skills'],['tasks','tasks'],['review','admin/review'],['context','admin/context']]){
   await page.goto(base+'/#/'+route);await page.waitForLoadState('networkidle');await pause(450);await page.evaluate(()=>document.fonts.ready);
   const text=await page.locator('body').innerText();if(text.includes('Invalid token')||text.includes('token không hợp lệ'))throw Error('Demo sign-in failed');
   await page.screenshot({path:path.join(out,`${name}.${locale}.png`)});console.log(locale,name);
  }
  await page.close();
 }
 fs.writeFileSync(path.join(root,'docs/hive/capture.json'),JSON.stringify({source:'Adjacent xdev-hive working tree',capturedAt:new Date().toISOString(),dimensions:[1440,1000],screens:['docs','memory','skills','tasks','review','context'],data:'Synthetic Atlas project in a disposable loopback hub; no customer data or credentials are included.'},null,2)+'\n');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{if(browser)await browser.close();server.kill();});
