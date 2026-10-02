/* Progressive enhancement: every screenshot and chapter stays readable without JS. */
(() => {
  const tabs = [...document.querySelectorAll('.hive-tab')];
  const panels = [...document.querySelectorAll('.hive-panel')];
  const nav = document.querySelector('.hive-tabs');
  if (nav && tabs.length === panels.length) {
    nav.setAttribute('role', 'tablist');
    const activate = (index, focus = false) => {
      tabs.forEach((tab, i) => {
        tab.setAttribute('aria-selected', String(i === index));
        tab.tabIndex = i === index ? 0 : -1;
        panels[i].hidden = i !== index;
      });
      if (focus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-controls', panels[index].id);
      panels[index].setAttribute('role', 'tabpanel');
      panels[index].tabIndex = 0;
      tab.addEventListener('click', event => {event.preventDefault();activate(index);});
      tab.addEventListener('keydown', event => {
        let next;
        if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (next !== undefined) {event.preventDefault();activate(next, true);}
      });
    });
    const match = panels.findIndex(panel => '#' + panel.id === location.hash);
    activate(match >= 0 ? match : 0);
    window.addEventListener('hashchange', () => {
      const i = panels.findIndex(panel => '#' + panel.id === location.hash);
      if (i >= 0) activate(i);
    });
  }
  const film = document.querySelector('#hive-film');
  if (film) {
    document.querySelectorAll('[data-video-seek]').forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => {
        const seek = () => {
          film.currentTime = Number(button.dataset.videoSeek);
          film.play().catch(() => {});
        };
        if (film.readyState >= 1) seek();
        else {film.addEventListener('loadedmetadata', seek, {once: true});film.load();}
        film.focus();
      });
    });
  }
  const map = document.querySelector('[data-hive-map]');
  const pause = document.querySelector('[data-map-pause]');
  if (map && pause) {
    const motion = matchMedia('(prefers-reduced-motion: reduce)');
    let visible = false, paused = false;
    const update = () => {
      map.classList.toggle('is-moving', visible && !paused && !motion.matches && !document.hidden);
      pause.hidden = motion.matches;
      pause.textContent = paused ? pause.dataset.resume : pause.dataset.pause;
      pause.setAttribute('aria-pressed', String(paused));
    };
    pause.addEventListener('click', () => {paused = !paused;update();});
    new IntersectionObserver(entries => {visible = entries[0].isIntersecting;update();}).observe(map);
    document.addEventListener('visibilitychange', update);
    motion.addEventListener('change', update);
    update();
  }
})();
