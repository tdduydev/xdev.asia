/* Progressive enhancement: the book works as ordinary links without JS. */
(() => {
  'use strict';
  const root = document.querySelector('.c4-site');
  if (!root) return;
  const tabs = [...root.querySelectorAll('[data-c4-tab]')];
  const panels = [...root.querySelectorAll('[data-c4-panel]')];
  function chooseLevel(index, moveFocus = false) {
    tabs.forEach((tab, i) => {
      const selected = i === index;
      tab.setAttribute('aria-selected', String(selected));
      tab.tabIndex = selected ? 0 : -1;
      if (moveFocus && selected) tab.focus();
    });
    panels.forEach((panel, i) => { panel.hidden = i !== index; });
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => chooseLevel(index));
    tab.addEventListener('keydown', event => {
      const dir = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
      if (dir) { event.preventDefault(); chooseLevel((index + dir + tabs.length) % tabs.length, true); }
      if (event.key === 'Home') { event.preventDefault(); chooseLevel(0, true); }
      if (event.key === 'End') { event.preventDefault(); chooseLevel(tabs.length - 1, true); }
    });
  });
  const search = root.querySelector('[data-c4-search]');
  const chapters = [...root.querySelectorAll('[data-c4-chapter]')];
  const groups = [...root.querySelectorAll('[data-c4-group]')];
  const empty = root.querySelector('[data-c4-empty]');
  if (search) {
    search.addEventListener('input', () => {
      const term = search.value.trim().toLocaleLowerCase();
      let visible = 0;
      chapters.forEach(card => {
        const matched = card.dataset.search?.includes(term) ?? false;
        card.hidden = !matched;
        if (matched) visible++;
      });
      groups.forEach(group => { group.hidden = !group.querySelector('[data-c4-chapter]:not([hidden])'); });
      if (empty) empty.hidden = visible !== 0;
    });
  }
})();
