document.querySelectorAll('[data-language-select]').forEach(select => {
  select.addEventListener('change', () => {
    const target = new URL(select.value, location.href);
    target.search = location.search;
    target.hash = location.hash;
    location.assign(target.href);
  });
});
