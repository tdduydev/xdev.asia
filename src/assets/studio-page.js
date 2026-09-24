(() => {
  const root = document.querySelector('.studio-landing');
  if (!root) return;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const motion = new Set();
  const easeOut = 'cubic-bezier(0.16, 1, 0.3, 1)';
  // Keep final DOM states independent of animations: cancellation never hides content.
  function animate(element, frames, options = {}) {
    if (!element.animate) return null;
    const animation = element.animate(frames, {duration: 220, easing: easeOut, ...options});
    motion.add(animation);
    animation.finished.then(() => motion.delete(animation), () => motion.delete(animation));
    return animation;
  }
  function enter(element, {delay = 0, duration = 450, distance = 12} = {}) {
    element.getAnimations().forEach(animation => animation.cancel());
    const frames = reducedMotion.matches
      ? [{opacity: 0}, {opacity: 1}]
      : [{opacity: 0, transform: `translateY(${distance}px)`}, {opacity: 1, transform: 'none'}];
    return animate(element, frames, {
      duration: reducedMotion.matches ? 140 : duration,
      delay: reducedMotion.matches ? 0 : delay, fill: 'backwards',
    });
  }
  reducedMotion.addEventListener('change', () => {
    // OS preference changes take effect during an in-flight interaction too.
    motion.forEach(animation => animation.cancel());
    motion.clear();
  });

  const tabList = root.querySelector('.studio-tabs');
  const tabs = [...tabList.querySelectorAll('.studio-tab')];
  const panels = [...root.querySelectorAll('.studio-panel')];
  const indicator = document.createElement('span');
  indicator.className = 'studio-tab-indicator';
  indicator.setAttribute('aria-hidden', 'true');
  tabList.append(indicator);
  tabList.classList.add('has-motion-indicator');
  tabList.setAttribute('role', 'tablist');
  let activeIndex = -1;
  function moveIndicator(index, shouldAnimate) {
    // Batch geometry reads before changing styles; never measure on animation frames.
    const previous = getComputedStyle(indicator).transform;
    const listBox = tabList.getBoundingClientRect();
    const tabBox = tabs[index].getBoundingClientRect();
    const x = tabBox.left - listBox.left + tabList.scrollLeft;
    const target = `translateX(${x}px) scaleX(${tabBox.width})`;
    indicator.getAnimations().forEach(animation => animation.cancel());
    indicator.style.transform = target;
    if (shouldAnimate) {
      animate(indicator, reducedMotion.matches
        ? [{opacity: .25}, {opacity: 1}]
        : [{transform: previous}, {transform: target}],
      {duration: reducedMotion.matches ? 120 : 240});
    }
  }
  function selectTab(index, focus = false) {
    const changed = activeIndex >= 0 && activeIndex !== index;
    moveIndicator(index, changed);
    tabs.forEach((tab, i) => {
      tab.setAttribute('aria-selected', String(i === index));
      tab.tabIndex = i === index ? 0 : -1;
      panels[i].hidden = i !== index;
    });
    activeIndex = index;
    if (changed) {
      enter(panels[index].querySelector('.studio-panel-copy'), {duration: 200, distance: 6});
      enter(panels[index].querySelector('.studio-screen'), {duration: 240, distance: 10});
    }
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, i) => {
    tab.setAttribute('role', 'tab');
    tab.setAttribute('aria-controls', panels[i].id);
    panels[i].setAttribute('role', 'tabpanel');
    panels[i].tabIndex = 0;
    tab.addEventListener('click', event => {
      event.preventDefault();
      selectTab(i);
    });
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (i - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (event.key === ' ') next = i;
      if (next !== undefined) {
        event.preventDefault();
        selectTab(next, true);
      }
    });
  });
  function selectFromHash() {
    const index = panels.findIndex(panel => '#' + panel.id === location.hash);
    if (index >= 0) selectTab(index);
    return index;
  }
  if (selectFromHash() < 0) selectTab(0);
  addEventListener('hashchange', selectFromHash);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver(() => moveIndicator(activeIndex, false));
    tabs.forEach(tab => observer.observe(tab));
  }

  const nodes = [...root.querySelectorAll('[data-node]')];
  const edges = [...root.querySelectorAll('[data-edge]')];
  // A single short entrance sequence; never loop or hijack scrolling.
  if (!location.hash) {
    enter(root.querySelector('.studio-hero-copy'), {duration: 540});
    enter(root.querySelector('.studio-blueprint'), {duration: 600, delay: 90});
    nodes.forEach((node, i) => enter(node, {delay: 170 + i * 100, duration: 400, distance: 9}));
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        enter(root.querySelector('.studio-panel:not([hidden]) .studio-screen'), {duration: 480, distance: 14});
        observer.disconnect();
      }
    }, {threshold: .2});
    observer.observe(root.querySelector('.studio-panels'));
  }

  const status = root.querySelector('[data-demo-status]');
  const progress = root.querySelector('.studio-demo-progress>span');
  const states = [...root.querySelectorAll('[data-state]')];
  const result = root.querySelector('[data-result]').textContent;
  const scenario = root.querySelector('[data-scenario]');
  const input = root.querySelector('[data-sample-input]');
  const output = root.querySelector('[data-workflow-result]');
  const pauseButton = root.querySelector('[data-flow-pause]');
  const canvas = root.querySelector('.workflow-canvas');
  const svg = root.querySelector('.workflow-wires');
  const particles = Array.from({length: 3}, (_, i) => {
    const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    dot.setAttribute('r', String(5 - i));
    dot.setAttribute('class', 'workflow-data-particle');
    dot.style.opacity = '0';
    svg.append(dot);
    return dot;
  });
  const lengths = edges.map(edge => edge.getTotalLength());
  const stepDuration = 1450;
  const runDuration = nodes.length * stepDuration;
  const cycleDuration = runDuration + 2600;
  let elapsed = 0, previous = null, frame = null, visible = false, paused = false;
  let lastStage = -2;
  // The visible status is updated per stage, not repeatedly announced by screen readers.
  status.setAttribute('aria-live', 'off');
  scenario.disabled = false;
  function render() {
    const stage = Math.min(nodes.length, Math.floor(elapsed / stepDuration));
    if (stage !== lastStage) {
      nodes.forEach((node, i) => {
        node.classList.toggle('is-active', i === stage);
        node.classList.toggle('is-complete', i < stage);
      });
      edges.forEach((edge, i) => edge.classList.toggle('is-traversed', i < stage));
      progress.style.transform = `scaleX(${stage / nodes.length})`;
      status.textContent = stage < nodes.length ? states[stage].textContent : result;
      output.hidden = stage < nodes.length;
      root.querySelector('[data-output-text]').textContent = scenario.selectedOptions[0].dataset.scenarioResult;
      canvas.dataset.stage = String(stage);
      lastStage = stage;
    }
    particles.forEach((dot, i) => {
      const t = (elapsed % stepDuration) / stepDuration - i * .12;
      if (reducedMotion.matches || stage >= edges.length || t < 0) {
        dot.style.opacity = '0';
        return;
      }
      const point = edges[stage].getPointAtLength(lengths[stage] * t);
      dot.setAttribute('cx', point.x);
      dot.setAttribute('cy', point.y);
      dot.style.opacity = String(1 - i * .25);
    });
  }
  function tick(now) {
    frame = null;
    if (!visible || paused || document.hidden || reducedMotion.matches) return;
    if (previous !== null) elapsed = (elapsed + Math.min(now - previous, 100)) % cycleDuration;
    previous = now;
    render();
    frame = requestAnimationFrame(tick);
  }
  function sync() {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null;
    previous = null;
    pauseButton.hidden = reducedMotion.matches;
    if (reducedMotion.matches) {
      elapsed = runDuration;
      render();
    } else if (visible && !paused && !document.hidden) frame = requestAnimationFrame(tick);
  }
  scenario.addEventListener('change', () => {
    input.textContent = scenario.selectedOptions[0].dataset.input;
    elapsed = reducedMotion.matches ? runDuration : 0;
    lastStage = -2;
    render();
    sync();
  });
  pauseButton.addEventListener('click', () => {
    paused = !paused;
    pauseButton.textContent = paused ? pauseButton.dataset.resume : pauseButton.dataset.pause;
    pauseButton.setAttribute('aria-pressed', String(paused));
    sync();
  });
  document.addEventListener('visibilitychange', sync);
  reducedMotion.addEventListener('change', () => { elapsed = 0; lastStage = -2; sync(); });
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      sync();
    }, {threshold: 0});
    observer.observe(canvas);
  } else visible = true;
  render();
  sync();
})();

// Native playback remains available without JavaScript; chapter buttons add seeking.
const tour = document.querySelector('#studio-tour');
if (tour) document.querySelectorAll('[data-video-seek]').forEach(button => {
  button.hidden = false;
  button.addEventListener('click', () => {
    tour.currentTime = Number(button.dataset.videoSeek);
    tour.play().catch(() => {});
  });
});

const story = document.querySelector('#studio-story');
if(story) document.querySelectorAll('[data-story-seek]').forEach(button=>{
 button.hidden=false;
 button.addEventListener('click',()=>{story.currentTime=Number(button.dataset.storySeek);story.play().catch(()=>{});});
});
// Keep narration intelligible when moving between the two films.
document.querySelectorAll('video').forEach(video=>video.addEventListener('play',()=>{
 document.querySelectorAll('video').forEach(other=>{if(other!==video)other.pause();});
}));
