(() => {
  const root = document.querySelector('.x-home');
  if (!root) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const animations = new Set();
  function reveal(element, delay = 0, duration = 550) {
    if (!element?.animate) return;
    element.getAnimations().forEach(a => a.cancel());
    const animation = element.animate(reduced.matches ? [{opacity: 0}, {opacity: 1}] :
      [{opacity: 0, transform: 'translateY(18px)'}, {opacity: 1, transform: 'none'}],
    {duration: reduced.matches ? 140 : duration, delay: reduced.matches ? 0 : delay,
      easing: 'cubic-bezier(.16,1,.3,1)', fill: 'backwards'});
    animations.add(animation);
    animation.finished.then(() => animations.delete(animation), () => animations.delete(animation));
  }
  if (!location.hash) {
    ['.x-signature', '.x-hero h1', '.x-hero-description', '.x-hero-actions'].forEach((selector, i) => reveal(root.querySelector(selector), i * 80, 650));
  }
  reduced.addEventListener('change', () => {
    animations.forEach(a => a.cancel());
    animations.clear();
  });
  const tabs = [...root.querySelectorAll('.x-preview-tabs a')];
  const panels = [...root.querySelectorAll('.x-product-screen')];
  const tablist = root.querySelector('.x-preview-tabs');
  tablist.setAttribute('role', 'tablist');
  let selected = -1;
  function select(index, focus = false) {
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    if (selected >= 0 && selected !== index) reveal(panels[index], 0, 240);
    selected = index;
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].setAttribute('aria-labelledby', tab.id);
    panels[i].tabIndex = 0;
    tab.addEventListener('click', event => {event.preventDefault();select(i)});
    tab.addEventListener('keydown', event => {
      const keys = {ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1, ' ': i};
      if (event.key in keys) {event.preventDefault();select(keys[event.key], true)}
    });
  });
  function fromHash() {
    const index = panels.findIndex(panel => '#' + panel.id === location.hash);
    if (index >= 0) select(index);
    return index;
  }
  if (fromHash() < 0) select(0);
  addEventListener('hashchange', fromHash);

  // A finite, on-demand canvas scene: no library, network request, or perpetual loop.
  const sculpture = root.querySelector('[data-sculpture]');
  const canvas = sculpture.querySelector('canvas');
  const ctx = canvas.getContext('2d');
  if (!ctx) return; // The authored SVG remains the static fallback.
  let width = 0, height = 0, frame = 0, visible = true, lastTime = 0;
  let yaw = -.9, pitch = -.23, targetYaw = -.38, targetPitch = -.18;
  let turns = 0, spin = null, structure = 0, targetStructure = 0;
  const baseYaw = -.38, basePitch = -.18;
  const shape = [[-1,-1],[-.38,-1],[0,-.37],[.38,-1],[1,-1],[.39,0],[1,1],[.38,1],[0,.37],[-.38,1],[-1,1],[-.39,0]];
  function rotate([x,y,z], ry = yaw, rx = pitch) {
    const xx = x * Math.cos(ry) + z * Math.sin(ry);
    const zz = -x * Math.sin(ry) + z * Math.cos(ry);
    const yy = y * Math.cos(rx) - zz * Math.sin(rx);
    const zzz = y * Math.sin(rx) + zz * Math.cos(rx);
    const roll = -.12;
    return [xx * Math.cos(roll) - yy * Math.sin(roll), xx * Math.sin(roll) + yy * Math.cos(roll), zzz];
  }
  function project(point) {
    const scale = Math.min(width * .32, height * .345);
    const perspective = 5.8 / (5.8 - point[2]);
    return [width * .53 + point[0] * scale * perspective, height * .47 + point[1] * scale * perspective];
  }
  function polygon(points) {
    ctx.beginPath();
    points.forEach((p,i) => {const [x,y]=project(p);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)});
    ctx.closePath();
  }
  function line(points, color, size = 1) {
    ctx.beginPath();points.forEach((p,i)=>{const [x,y]=project(p);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)});
    ctx.strokeStyle=color;ctx.lineWidth=size;ctx.stroke();
  }
  function draw() {
    ctx.clearRect(0,0,width,height);
    const shadow = ctx.createRadialGradient(width*.54,height*.85,0,width*.54,height*.85,width*.34);
    shadow.addColorStop(0,'rgba(34,96,194,.15)');shadow.addColorStop(.48,'rgba(63,128,220,.055)');shadow.addColorStop(1,'rgba(63,128,220,0)');
    ctx.save();ctx.translate(0,height*.53);ctx.scale(1,.38);ctx.fillStyle=shadow;ctx.fillRect(0,0,width,height*1.5);ctx.restore();
    // Perspective construction grid behind the object; purposeful spatial context.
    for(let i=-5;i<=5;i++) {
      const q=i*.43;
      line([rotate([q,1.43,-2],-.38,.27),rotate([q,1.43,2],-.38,.27)],'rgba(79,126,192,.10)',.7);
      line([rotate([-2.15,1.43,q],-.38,.27),rotate([2.15,1.43,q],-.38,.27)],'rgba(79,126,192,.10)',.7);
    }
    // A few offset construction outlines make the depth legible even at rest.
    for (let layer=3;layer>0;layer--) {
      const points=shape.map(([x,y])=>rotate([x*1.03,y*1.03,-.24-layer*.13]));
      polygon(points);ctx.strokeStyle=`rgba(37,111,219,${.055+layer*.018})`;ctx.lineWidth=.8;ctx.stroke();
    }
    const front=shape.map(([x,y])=>rotate([x,y,.23]));
    const back=shape.map(([x,y])=>rotate([x,y,-.23]));
    const faces=[];
    for(let i=0;i<shape.length;i++) {const j=(i+1)%shape.length;faces.push({points:[front[i],front[j],back[j],back[i]],side:true,index:i})}
    faces.push({points:back,side:false,rear:true},{points:front,side:false,rear:false});
    faces.sort((a,b)=>a.points.reduce((s,p)=>s+p[2],0)/a.points.length-b.points.reduce((s,p)=>s+p[2],0)/b.points.length);
    for(const face of faces) {
      polygon(face.points);
      const gradient=ctx.createLinearGradient(width*.25,height*.15,width*.76,height*.78);
      if(face.side) {
        const light=face.index%3===0;
        gradient.addColorStop(0,light?'#91ceff':'#267fea');gradient.addColorStop(.5,light?'#246bd4':'#124bbe');gradient.addColorStop(1,'#0a3597');
      } else {
        gradient.addColorStop(0,'#d8f4ff');gradient.addColorStop(.23,'#88cfff');gradient.addColorStop(.48,'#429af6');gradient.addColorStop(.72,'#1265e9');gradient.addColorStop(1,'#0644c2');
      }
      ctx.globalAlpha=1-structure*.92;ctx.fillStyle=gradient;ctx.fill();ctx.globalAlpha=1;ctx.strokeStyle=structure>.5?'rgba(7,89,237,.65)':face.side?'rgba(179,220,255,.3)':'rgba(225,246,255,.85)';ctx.lineWidth=face.side?.8:1.25;ctx.stroke();
      if(!face.side&&!face.rear&&structure<.5) {
        ctx.save();ctx.clip();
        const shine=ctx.createLinearGradient(0,0,width,height*.65);
        shine.addColorStop(0,'rgba(255,255,255,0)');shine.addColorStop(.38,'rgba(255,255,255,0)');shine.addColorStop(.5,'rgba(232,248,255,.48)');shine.addColorStop(.52,'rgba(255,255,255,.04)');shine.addColorStop(1,'rgba(255,255,255,0)');
        ctx.fillStyle=shine;ctx.fillRect(0,0,width,height);
        ctx.restore();
      }
    }
    // Small precision ticks and distant anchor points, not an animated particle field.
    [[-1.6,-.8,-.5],[1.5,.55,-.5],[.9,-1.25,-.7]].forEach(p=>{
      const [x,y]=project(rotate(p));ctx.strokeStyle='#8eacd8';ctx.lineWidth=.7;
      ctx.beginPath();ctx.moveTo(x-4,y);ctx.lineTo(x+4,y);ctx.moveTo(x,y-4);ctx.lineTo(x,y+4);ctx.stroke();
    });
    canvas.dataset.rendered='true';
  }
  function tick(time) {
    frame=0;
    const delta=Math.min(time-lastTime||16,32);lastTime=time;
    const lerp=1-Math.exp(-delta/140);
    if(spin) {
      const t=Math.min(1,(time-spin.start)/1600);
      const eased=t*t*(3-2*t);
      yaw=spin.from+(spin.to-spin.from)*eased;
      if(t===1){spin=null;sculpture.querySelector('[data-art-turn]').disabled=false}
    } else yaw+=(targetYaw-yaw)*lerp;
    pitch+=(targetPitch-pitch)*lerp;
    structure+=(targetStructure-structure)*lerp;
    draw();
    if(visible&&!document.hidden&&!reduced.matches&&(spin||Math.abs(targetYaw-yaw)>.0006||Math.abs(targetPitch-pitch)>.0006||Math.abs(targetStructure-structure)>.001)) frame=requestAnimationFrame(tick);
    else {yaw=targetYaw;pitch=targetPitch;structure=targetStructure;draw();canvas.dataset.moving='false'}
  }
  function schedule() {
    if(reduced.matches||!visible||document.hidden) {stop();yaw=targetYaw;pitch=targetPitch;structure=targetStructure;draw();return}
    if(!frame) {lastTime=performance.now();canvas.dataset.moving='true';frame=requestAnimationFrame(tick)}
  }
  function stop() {if(frame)cancelAnimationFrame(frame);frame=0;spin=null;sculpture.querySelector('[data-art-turn]').disabled=false;canvas.dataset.moving='false'}
  canvas.hidden=false;
  sculpture.querySelector('.x-art-fallback').setAttribute('hidden', '');
  const controls=sculpture.querySelector('.x-art-controls');controls.hidden=false;
  function resize() {
    const box=canvas.parentElement.getBoundingClientRect();
    width=box.width;height=box.height;
    const dpr=Math.min(devicePixelRatio||1,2);
    canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);schedule();
  }
  if('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas.parentElement);else addEventListener('resize',resize);
  resize();
  let bounds;
  canvas.addEventListener('pointerenter',()=>{bounds=canvas.getBoundingClientRect()});
  canvas.addEventListener('pointermove',event=>{
    if(reduced.matches||spin||event.pointerType!=='mouse'||!bounds)return;
    targetYaw=baseYaw+turns*Math.PI*2+((event.clientX-bounds.left)/bounds.width-.5)*.6;
    targetPitch=basePitch+((event.clientY-bounds.top)/bounds.height-.5)*.3;schedule();
  });
  canvas.addEventListener('pointerleave',()=>{if(spin)return;targetYaw=baseYaw+turns*Math.PI*2;targetPitch=basePitch;schedule()});
  controls.querySelector('[data-art-turn]').addEventListener('click',()=>{
    if(reduced.matches) {yaw=baseYaw+.6;targetYaw=yaw;draw();return}
    visible=true;turns++;targetYaw=baseYaw+turns*Math.PI*2;spin={start:performance.now(),from:yaw,to:targetYaw};controls.querySelector('[data-art-turn]').disabled=true;schedule();
  });
  controls.querySelector('[data-art-structure]').addEventListener('click',event=>{targetStructure=targetStructure?0:1;event.currentTarget.setAttribute('aria-pressed',String(!!targetStructure));schedule()});
  controls.querySelector('[data-art-reset]').addEventListener('click',()=>{stop();targetStructure=0;controls.querySelector('[data-art-structure]').setAttribute('aria-pressed','false');turns=0;yaw=((yaw-baseYaw)%(Math.PI*2))+baseYaw;targetYaw=baseYaw;targetPitch=basePitch;schedule()});
  reduced.addEventListener('change',()=>{stop();turns=0;targetYaw=baseYaw;targetPitch=basePitch;yaw=baseYaw;pitch=basePitch;structure=targetStructure;draw()});
  document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();else schedule()});
  if('IntersectionObserver' in window) new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible)schedule();else stop()},{threshold:0}).observe(sculpture);
})();
