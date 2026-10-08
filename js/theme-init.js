// Apply an explicit preference before paint; CSS handles system preference.
try {
  const saved = localStorage.getItem('theme');
  if (saved === 'light' || saved === 'dark') document.documentElement.dataset.theme = saved;
} catch { /* Storage is optional. */ }
