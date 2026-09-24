/* Story v2: authored people, port-anchored connectors and explicit trust boundaries. */
'use strict';
const C={ink:'#22344c',blue:'#1761de',paper:'#f6f8fc',muted:'#64758c',line:'#cbd6e5',red:'#ba414c',pale:'#e9f0ff',white:'#fff'};
const vi=STORY.language==='vi',tr=(a,b)=>vi?a:b;
const P=(t,a,b)=>clamp((t-a)/(b-a),0,1);
function text(c,s,x,y,size=29,color=C.ink,align='center',weight=500){c.save();c.fillStyle=color;c.font=`${weight} ${size}px StoryInter`;c.textAlign=align;c.fillText(s,x,y);c.restore()}
function wrap(c,s,x,y,max,size=29,color=C.ink,align='center',weight=500){c.save();c.font=`${weight} ${size}px StoryInter`;let line='',lines=[];for(const w of s.split(' ')){if(line&&c.measureText(line+w).width>max){lines.push(line.trim());line=''}line+=w+' '}lines.push(line.trim());lines.forEach((l,i)=>text(c,l,x,y+i*size*1.3,size,color,align,weight));c.restore();return lines.length}
function stroke(c,pts,p=1,seed=11,color=C.ink,w=3){c.save();c.strokeStyle=color;c.lineWidth=w;c.lineCap='round';c.lineJoin='round';selfDraw(c,pts,p,seed,.65);c.restore()}
function round(c,x,y,w,h,r=18,fill=C.white){c.fillStyle=fill;c.beginPath();c.roundRect(x,y,w,h,r);c.fill()}
function icon(c,k,x,y,s=1){c.save();c.translate(x,y);c.scale(s,s);const d=(p,z=1)=>stroke(c,p,1,21+z,C.blue,3);
 if(k==='doc'){d([[-28,38],[-28,-38],[10,-38],[28,-20],[28,38],[-28,38]]);d([[10,-38],[10,-19],[28,-19]],2);for(let i=0;i<3;i++)d([[-16,-3+i*12],[15-i*3,-3+i*12]],3+i)}
 else if(k==='model'){d([[-36,0],[-18,-32],[18,-32],[36,0],[18,32],[-18,32],[-36,0]]);d([[-18,-32],[0,0],[18,-32],[0,0],[18,32],[0,0],[-18,32]],2)}
 else if(k==='shield'){d([[0,-40],[34,-26],[30,13],[0,43],[-30,13],[-34,-26],[0,-40]]);d([[-17,0],[-2,17],[19,-13]],2)}
 else if(k==='book'){d([[-32,-28],[0,-18],[32,-28],[32,31],[0,42],[-32,31],[-32,-28]]);d([[0,-18],[0,42]],2)}
 else if(k==='gateway'){d([[-36,36],[-36,-35],[36,-35],[36,36]]);d([[-19,15],[0,-7],[19,15]],2);d([[0,-7],[0,35]],3)}
 else if(k==='code'){d([[-13,-22],[-36,0],[-13,22]]);d([[13,-22],[36,0],[13,22]],2);d([[7,-32],[-7,32]],3)}
 else if(k==='check'){d([[-29,0],[-7,27],[34,-25]])}
 else if(k==='tool'){d([[-30,31],[8,-7],[5,-25],[19,-34],[18,-13],[34,-13],[39,-30],[41,-8],[28,4],[-16,44],[-30,31]])}
 else if(k==='app'){d([[-38,-29],[38,-29],[38,30],[-38,30],[-38,-29]]);d([[-38,-12],[38,-12]],2);d([[-19,1],[-3,18],[21,-3]],3)}
 else if(k==='people'){d([[-15,-29],[-23,-16],[-16,-2],[0,1],[10,-12],[7,-28],[-15,-29]]);d([[-31,33],[-23,10],[-5,5],[16,12],[25,34]],2);d([[26,-23],[37,-16],[36,0],[28,4]],3)}
 else if(k==='chart'){d([[-33,32],[-33,-32]],1);d([[-33,32],[37,32]],2);d([[-20,15],[-4,-4],[12,3],[30,-23]],3)}
 else if(k==='lock'){d([[-28,0],[28,0],[28,35],[-28,35],[-28,0]]);d([[-18,0],[-18,-20],[-7,-31],[10,-29],[18,-18],[18,0]],2)}
 else if(k==='clock'){const pts=Array.from({length:33},(_,i)=>[Math.cos(i/32*6.283)*36,Math.sin(i/32*6.283)*36]);d(pts);d([[0,-23],[0,0],[18,13]],2)}
 else if(k==='ner'){d([[-38,-29],[-16,-29]],1);d([[17,-29],[38,-29],[38,-10]],2);d([[-38,10],[-38,29],[-17,29]],3);d([[17,29],[38,29]],4);d([[-12,1],[0,-12],[12,1],[0,16],[-12,1]],5)}
 else {d([[-32,-24],[30,-24],[30,25],[-32,25],[-32,-24]]);d([[-14,0],[13,0]],2)}c.restore()}
const rawPose=pose=>({strokes:[
 {id:'hair',points:pose==='think'?[[-28,-130],[-35,-155],[-17,-176],[12,-172],[29,-155],[27,-135]]:[[-30,-130],[-33,-151],[-17,-172],[14,-173],[32,-151],[29,-128]],width:4.8},
 {id:'face',points:[[-27,-145],[-27,-117],[-15,-100],[9,-98],[26,-117],[27,-145]],width:3.5},
 {id:'brow',points:pose==='think'?[[0,-136],[12,-140]]:[[-1,-138],[12,-137]],width:2.5},
 {id:'eye',points:[[4,-130],[7,-130]],width:3},
 {id:'nose',points:[[12,-130],[16,-121],[10,-120]],width:2},
 {id:'mouth',points:pose==='happy'?[[-5,-112],[3,-108],[11,-111]]:[[-4,-110],[9,-110]],width:2},
 {id:'neck',points:[[-15,-101],[-15,-84],[4,-73],[16,-86],[15,-101]],width:3},
 {id:'torso',points:[[-16,-85],[-48,-69],[-57,-17],[-40,27],[31,29],[47,-21],[36,-68],[17,-84]],width:4},
 {id:'collar',points:[[-16,-84],[-3,-57],[17,-83]],width:2.5},
 {id:'near-arm',points:pose==='think'?[[36,-65],[57,-35],[32,-24],[13,-69],[8,-87],[19,-94],[25,-77],[33,-55],[38,-40]]:pose==='happy'?[[36,-65],[59,-27],[80,-45],[92,-64],[102,-58],[96,-35],[65,-7],[45,-13],[26,-49]]:[[36,-65],[55,-28],[87,-23],[105,-15],[103,-8],[77,-7],[36,-14],[25,-42]],width:4},
 {id:'far-arm',points:[[-47,-65],[-30,-27],[9,-21],[26,-11],[21,-5],[-2,-8],[-45,-14],[-56,-31]],width:3},
 {id:'lap',points:[[-40,26],[-13,49],[37,51],[45,79],[45,122],[63,128],[64,137],[28,137],[23,86],[6,75],[-34,68],[-53,52],[-40,26]],width:4},
 {id:'far-leg',points:[[-34,67],[-42,112],[-42,135],[-12,136],[-13,127],[-23,119],[-8,77]],width:3},
 {id:'shirt-fold',points:[[-28,-2],[-19,11],[8,14]],width:2},
 {id:'chair',points:[[-70,-4],[-68,57],[-58,71],[19,71]],width:2.5},
 {id:'chair-leg',points:[[-59,71],[-64,134]],width:2.5}
]});
const POSES=Object.fromEntries(['work','think','happy'].map(p=>[p,compileCel(rawPose(p),{id:'employee-'+p})]));
function person(c,x,y,pose='work',scale=1){c.save();c.translate(x,y);c.scale(scale,scale);c.fillStyle=C.pale;c.beginPath();c.moveTo(-43,-64);c.lineTo(32,-65);c.lineTo(32,22);c.lineTo(-39,21);c.closePath();c.fill();drawCel(c,POSES[pose],{material:'ink',color:C.ink});stroke(c,[[52,-60],[125,-60],[104,-9],[36,-9],[52,-60]],1,71,C.blue,3);stroke(c,[[-80,-1],[137,-1],[138,8],[-80,8]],1,73,C.ink,3);stroke(c,[[115,8],[120,138]],1,74,C.ink,3);c.restore()}
function employee(c,t,pose='work'){person(c,190,680,pose,1.05);text(c,tr('Nhân viên','Employee'),195,877,26);text(c,tr('Yêu cầu mua thiết bị','Equipment request'),195,915,20,C.muted)}
function node(id,x,y,label,kind='app',w=226,h=162){return {id,x,y,label,kind,w,h}}
function port(n,s){return s==='l'?[n.x-n.w/2,n.y]:s==='r'?[n.x+n.w/2,n.y]:s==='t'?[n.x,n.y-n.h/2]:[n.x,n.y+n.h/2]}
window.STORY_GEOMETRY=[];
function connector(a,sa,b,sb,opts={}){const from=port(a,sa),to=port(b,sb);let pts;
 if(opts.via)pts=[from,...opts.via,to];else{const dx=Math.abs(to[0]-from[0])*.45;const h=Math.max(38,dx);const dirs={l:[-1,0],r:[1,0],t:[0,-1],b:[0,1]};let d=dirs[sa],e=dirs[sb],u=[from[0]+d[0]*h,from[1]+d[1]*h],v=[to[0]+e[0]*h,to[1]+e[1]*h];pts=Array.from({length:61},(_,i)=>{let t=i/60,z=1-t;return [z*z*z*from[0]+3*z*z*t*u[0]+3*z*t*t*v[0]+t*t*t*to[0],z*z*z*from[1]+3*z*z*t*u[1]+3*z*t*t*v[1]+t*t*t*to[1]]})}
 window.STORY_GEOMETRY.push({source:a.id,target:b.id,sourcePort:sa,targetPort:sb,from,to,blocked:!!opts.blocked,returning:!!opts.returning,sourceBox:[a.x,a.y,a.w,a.h],targetBox:[b.x,b.y,b.w,b.h]});
 let lengths=[0];for(let i=1;i<pts.length;i++)lengths.push(lengths[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));return {from,to,pts,lengths,length:lengths.at(-1),...opts}}
function pointAt(e,u){const d=clamp(u,0,1)*e.length;let i=1;while(i<e.lengths.length-1&&e.lengths[i]<d)i++;const q=(d-e.lengths[i-1])/(e.lengths[i]-e.lengths[i-1]||1);return [lerp(e.pts[i-1][0],e.pts[i][0],q),lerp(e.pts[i-1][1],e.pts[i][1],q)]}
function edge(c,e,t,start=1,duration=1.4){const p=P(t,start,start+duration),color=e.blocked?C.red:(e.returning||e.relationship)?C.muted:C.blue;if(!p)return;c.save();c.lineWidth=3.2;c.strokeStyle=color;c.lineJoin='round';c.lineCap='round';if(e.returning)c.setLineDash([8,7]);c.beginPath();c.moveTo(...e.from);for(let i=1;i<e.pts.length;i++){if(e.lengths[i]>p*e.length)break;c.lineTo(...e.pts[i])}c.lineTo(...pointAt(e,p));c.stroke();c.setLineDash([]);
 if(p===1&&!e.relationship){const tip=e.to,near=pointAt(e,.96),angle=Math.atan2(tip[1]-near[1],tip[0]-near[0]);if(e.blocked){stroke(c,[[tip[0]-9,tip[1]-9],[tip[0]+9,tip[1]+9]],1,34,C.red,4);stroke(c,[[tip[0]+9,tip[1]-9],[tip[0]-9,tip[1]+9]],1,35,C.red,4)}else{c.fillStyle=color;c.beginPath();c.moveTo(...tip);c.lineTo(tip[0]-15*Math.cos(angle-.44),tip[1]-15*Math.sin(angle-.44));c.lineTo(tip[0]-15*Math.cos(angle+.44),tip[1]-15*Math.sin(angle+.44));c.closePath();c.fill()}}
 if(e.label&&p>.7){const pos=e.labelAt||pointAt(e,.5);text(c,e.label,pos[0],pos[1]-20,22,color)}
 const u=(t-start-duration-.25)/1.5;if(u>=0&&u<=1&&!e.returning&&!e.relationship){const pos=pointAt(e,u);c.fillStyle=color;c.beginPath();c.arc(...pos,6,0,7);c.fill()}c.restore()}
function card(c,n,t=99,start=0){const p=P(t,start,start+.65);if(!p)return;c.save();c.globalAlpha=p;round(c,n.x-n.w/2+3,n.y-n.h/2+5,n.w,n.h,15,'#e4eaf3');round(c,n.x-n.w/2,n.y-n.h/2,n.w,n.h,15);stroke(c,[[n.x-n.w/2+12,n.y-n.h/2],[n.x+n.w/2-12,n.y-n.h/2]],1,12,C.line,2);icon(c,n.kind,n.x,n.y-25,.7);wrap(c,n.label,n.x,n.y+43,n.w-20,25);c.restore()}
function panel(c,x,y,w,h,title,red=false){c.save();round(c,x,y,w,h,24,red?'#fff0f1':'#edf3fd');c.strokeStyle=red?'#dc8e95':'#9bb6df';c.lineWidth=2;c.setLineDash([9,7]);c.strokeRect(x+1,y+1,w-2,h-2);c.setLineDash([]);text(c,title,x+20,y+38,23,red?C.red:C.blue,'left');c.restore()}
function note(c,s,x=1130,y=878,max=1310){wrap(c,s,x,y,max,24,C.muted)}
function header(c,s,index){c.fillStyle=C.paper;c.fillRect(0,0,W,H);c.fillStyle='#dce4ef';for(let x=35;x<W;x+=50)for(let y=35;y<H;y+=50){c.beginPath();c.arc(x,y,.65,0,7);c.fill()}text(c,'AI STUDIO',80,66,24,C.blue,'left',600);text(c,String(index+1).padStart(2,'0')+' / '+STORY.scenes.length,1835,66,22,C.muted,'right');wrap(c,s.title,80,155,1740,57,C.ink,'left',600);stroke(c,[[80,958],[1840,958]],1,5,C.line,1.5);text(c,['integrations','publish','memory','quality','operations','examples'].includes(s.kind)?tr('─ Nhóm tính năng, không phải luồng dữ liệu','─ Capability map, not a data flow'):tr('→ Dữ liệu / lệnh được phép','→ Allowed data / actions'),80,1000,20,C.blue,'left');text(c,tr('⇠ Kết quả / phản hồi','⇠ Result / feedback'),610,1000,20,C.muted,'left');text(c,tr('× Đường bị chặn','× Blocked route'),1110,1000,20,C.red,'left');text(c,'xdev.asia',1840,1000,20,C.muted,'right')}
function chain(c,nodes,t,{first=1,step=2.2,returned=false}={}){for(let j=0;j<nodes.length-1;j++)edge(c,connector(nodes[j],'r',nodes[j+1],'l'),t,first+j*step);nodes.forEach((n,j)=>card(c,n,t,j*.5));if(returned)edge(c,connector(nodes.at(-1),'b',nodes[0],'b',{returning:true,via:[[nodes.at(-1).x,760],[nodes[0].x,760]],label:tr('Trả kết quả','Return result'),labelAt:[1120,760]}),t,first+(nodes.length-1)*step)}
function drawScene(c,t,i,index){window.STORY_GEOMETRY=[];const s=STORY.scenes[index],L=s.labels,k=s.kind;header(c,s,index);
 if(k==='problem'){
  employee(c,t,t<4?'think':'work');const a=node('question',570,470,L[1],'doc',280),b=node('docs',1050,370,L[2],'book'),d=node('mail',1530,470,L[3],'app'),e=node('colleague',1100,720,L[4],'people',280);
  edge(c,connector(a,'r',b,'l',{label:'?',labelAt:[805,382]}),t,2);edge(c,connector(b,'r',d,'l',{label:'?'}),t,4);edge(c,connector(d,'b',e,'r',{label:'?'}),t,6);[a,b,d,e].forEach((n,j)=>card(c,n,t,j*.6));note(c,tr('Tìm đúng thông tin mới chỉ là bước đầu.','Finding the right information is only the first step.'));
 }else if(k==='usecase'){
  employee(c,t);const ns=[node('request',600,530,L[1],'app',240),node('policy',950,530,L[2],'book',240),node('draft',1300,530,L[3],'doc',240),node('review',1650,530,L[4],'people',240)];chain(c,ns,t,{returned:true});note(c,tr('Use case minh họa: trợ lý mua sắm nội bộ.','Illustrative use case: an internal purchasing assistant.'));
 }else if(k==='ingestion'){
  employee(c,t);const ns=L.map((v,j)=>node('ingest'+j,530+j*282,540,v,['doc','app','ner','doc','book'][j],204));chain(c,ns,t);panel(c,770,700,730,125,tr('Tùy chính sách và dịch vụ đã cấu hình','Depends on configured policy and services'));note(c,tr('NER hỗ trợ phát hiện; không bảo đảm phát hiện toàn bộ PII.','NER assists detection; it cannot guarantee complete PII detection.'),1130,888);
 }else if(k==='knowledge'){
  employee(c,t);const ns=[node('req',540,510,L[0],'app',190),node('access',860,510,L[1],'shield',230),node('kb',1200,510,L[2],'book',230),node('context',1620,510,L[3],'doc',270)];chain(c,ns,t);const denied=node('denied',860,766,L[4],'lock',260);edge(c,connector(ns[1],'b',denied,'t',{blocked:true}),t,7);card(c,denied,t,7);note(c,tr('Tổ chức · phòng ban · mức nhạy cảm','Organization · department · sensitivity'),1310,850,860);
 }else if(k==='custom'){
  employee(c,t);const a=node('input',530,500,tr('Đầu vào','Input'),'doc',190),b=node('branch',860,500,tr('Điều kiện','Condition'),'model',220),d=node('stepA',1210,380,tr('Xử lý A','Process A'),'tool',220),e=node('stepB',1210,660,tr('Xử lý B','Process B'),'code',220),f=node('out',1650,500,tr('Đầu ra','Output'),'app',220);
  edge(c,connector(a,'r',b,'l'),t,1);edge(c,connector(b,'t',d,'l',{label:tr('Nếu đúng','If true')}),t,3);edge(c,connector(b,'b',e,'l',{label:tr('Nếu sai','If false')}),t,5);edge(c,connector(d,'r',f,'t'),t,7);edge(c,connector(e,'r',f,'b'),t,8);[a,b,d,e,f].forEach((n,j)=>card(c,n,t,j*.3));note(c,L.join('  ·  '),1130,861,1350);text(c,tr('28 loại node · phiên bản nháp → kiểm tra → xuất bản','28 node types · draft → test → publish'),1130,922,22,C.blue);
 }else if(k==='gateway'){
  employee(c,t);panel(c,735,318,420,405,L[4]);const a=node('ctx',540,515,L[0],'doc',190),g=node('gw',945,525,L[1],'gateway',310),m=node('internal',1560,405,L[2],'model',300),e=node('external',1560,690,L[3],'model',300);
  edge(c,connector(a,'r',g,'l'),t,1);edge(c,connector(g,'r',m,'l',{label:tr('Được phép','Allowed')}),t,4);edge(c,connector(g,'b',e,'l',{label:tr('Chỉ khi chính sách cho phép','Only if policy permits'),labelAt:[1190,775]}),t,7);[a,g,m,e].forEach(n=>card(c,n,t));note(c,tr('AI Gateway: tên mô tả lớp điều phối mô hình, không phải dịch vụ riêng.','AI Gateway describes model orchestration, not a separate service.'),1130,886,1340);
 }else if(k==='security'){
  employee(c,t,'think');panel(c,440,318,965,470,tr('Ranh giới hệ thống','System boundary'));panel(c,1490,318,360,470,tr('Bên ngoài','External'),true);
  const a=node('sensitive',590,520,L[0],'doc',220),m=node('mask',915,520,L[1],'ner',260),g=node('egress',1235,520,L[2],'shield',220),ext=node('ext',1670,520,L[3],'model',280),stop=node('stop',1445,520,'','lock',0,0);
  edge(c,connector(a,'r',m,'l'),t,1);edge(c,connector(m,'r',g,'l'),t,3);edge(c,connector(g,'r',stop,'l',{blocked:true}),t,6);[a,m,g,ext].forEach(n=>card(c,n,t));text(c,L[4],1445,665,23,C.red);note(c,tr('PII masking ≠ cho phép gửi ra ngoài. Chặn nếu chính sách không cho phép.','PII masking ≠ permission to send. Block if policy does not allow it.'),1125,866,1350);
 }else if(k==='sandbox'){
  employee(c,t);panel(c,1080,310,420,420,L[2]);const ns=[node('flow',530,520,L[0],'app',220),node('code',865,520,L[1],'code',220),node('sandbox',1290,520,L[2],'code',280),node('result',1690,520,L[3],'doc',220)];chain(c,ns,t);text(c,L[4],1290,683,25,C.blue);note(c,tr('Dịch vụ riêng · chưa cấu hình → node Code bị tắt.','Separate service · not configured → Code node disabled.'),1130,835);text(c,tr('Không thay thế phân quyền hay kiểm soát egress.','Does not replace access or egress controls.'),1130,888,23,C.muted);
 }else if(k==='approval'){
  person(c,1110,535,t<7?'think':'happy',.9);const a=node('draft',550,490,L[0],'doc',270),review=node('human',1080,750,L[1],'people',270),out=node('api',1640,490,L[3],'tool',270);
  edge(c,connector(a,'r',review,'l'),t,1);edge(c,connector(review,'r',out,'l',{label:L[2],labelAt:[1430,630]}),t,8);edge(c,connector(review,'b',a,'b',{returning:true,via:[[1080,850],[550,850]],label:L[4],labelAt:[730,850]}),t,4);card(c,a,t);card(c,out,t,8);card(c,review,t);note(c,tr('Công cụ chỉ được gọi sau nhánh duyệt đã thiết kế.','The tool is called only after the designed approval gate.'),1130,885);
 }else if(['integrations','publish','memory','quality','operations','examples'].includes(k)){
  employee(c,t,k==='examples'?'happy':'work');const hub=node('hub',700,555,'AI Studio',k==='operations'?'shield':'app',240);const icons={integrations:['tool','gateway','code','shield'],publish:['app','code','people','clock'],memory:['people','book','app','model'],quality:['doc','chart','check','book'],operations:['people','shield','book','gateway'],examples:['book','people','doc','check']}[k];
  const ns=L.map((v,j)=>node('feature'+j,j<2?1160:1660,j%2?730:400,v,icons[j],300,175));
  ns.forEach((n,j)=>edge(c,connector(hub,j%2?'b':'t',n,'l',{relationship:true,via:j>1?[[700,j%2?870:280],[1460,j%2?870:280],[1460,n.y]]:undefined}),t,1+j*2));card(c,hub,t);ns.forEach((n,j)=>card(c,n,t,j*.7));
  if(k==='memory')text(c,tr('Theo mô hình và chính sách đã cấu hình','Depends on configured models and policies'),1275,900,23,C.muted);
  if(k==='quality')text(c,tr('Tinh chỉnh cần runner, tài nguyên và cấu hình phù hợp.','Fine-tuning requires a runner, resources and configuration.'),1275,900,22,C.muted);
  if(k==='operations')text(c,tr('Quản trị hệ thống tách biệt quyền workspace.','Instance administration is separate from workspace roles.'),1275,900,22,C.muted);
 }else if(k==='closing'){
  employee(c,t,'happy');const ns=L.slice(1).map((v,j)=>node('end'+j,620+j*355,575,v,['book','gateway','tool','app'][j],245));chain(c,ns,t,{returned:true});if(t>3)c.drawImage(brand,970,295,290,142);note(c,tr('Bắt đầu nhỏ → đánh giá → theo dõi → mở rộng.','Start small → evaluate → observe → expand.'),1130,883);}
 c.fillStyle=C.blue;c.fillRect(80,958,1760*((s.start+t)/STORY.duration),3);
}
const brand=new Image();brand.src=window.BRAND_DATA;
Promise.all([brand.decode(),document.fonts.load('500 29px StoryInter'),document.fonts.load('600 57px StoryInter')]).then(()=>defineFilm({format:{ar:'16:9',width:1280},fps:24,timeline:STORY.scenes.map((s,j)=>({name:s.title,dur:s.duration,fn:(c,t,i)=>drawScene(c,t,i,j)}))}));
if(!new URLSearchParams(location.search).has('bare')){const ready=setInterval(()=>{if(!window.__ready)return;clearInterval(ready);document.querySelectorAll('.bar').forEach(n=>n.remove());const audio=document.createElement('audio');audio.controls=true;audio.preload='metadata';audio.src=`narration.v2.${STORY.language}.m4a`;audio.setAttribute('aria-label',tr('Phát câu chuyện AI Studio','Play the AI Studio story'));audio.style.cssText='display:block;width:min(90%,800px);margin:20px auto';document.body.append(audio);let raf=0;const draw=()=>{window.__drawFrame(Math.min(window.__NDRAW-1,Math.floor(audio.currentTime*24)));if(!audio.paused)raf=requestAnimationFrame(draw)};audio.addEventListener('play',()=>{cancelAnimationFrame(raf);draw()});audio.addEventListener('pause',()=>cancelAnimationFrame(raf));audio.addEventListener('seeked',draw);audio.addEventListener('ended',draw)},50)}
