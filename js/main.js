const themeToggle = document.querySelector('[data-theme-toggle]');
const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
const currentTheme = () => document.documentElement.dataset.theme || (systemTheme.matches ? 'dark' : 'light');
const updateThemeControl = () => {
  if (!themeToggle) return;
  const dark = currentTheme() === 'dark';
  themeToggle.setAttribute('aria-pressed', String(dark));
  themeToggle.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} theme`);
  themeToggle.querySelector('[data-theme-label]').textContent = dark ? 'Dark' : 'Light';
};
updateThemeControl();
systemTheme.addEventListener('change', updateThemeControl);
if (themeToggle) themeToggle.addEventListener('click', () => {
  const next = currentTheme() === 'dark' ? 'light' : 'dark';
  document.documentElement.dataset.theme = next;
  try { localStorage.setItem('theme', next); } catch { /* Theme works without storage. */ }
  updateThemeControl();
});
document.querySelectorAll('[data-year]').forEach(element => { element.textContent = new Date().getFullYear(); });
