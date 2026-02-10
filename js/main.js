const themeToggle = document.querySelector('[data-theme-toggle]');
const storedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const initialTheme = storedTheme || (prefersDark ? 'dark' : 'light');

document.documentElement.setAttribute('data-theme', initialTheme);
if (themeToggle) {
  themeToggle.setAttribute('aria-pressed', initialTheme === 'dark');
}

const updateToggleLabel = (theme) => {
  if (!themeToggle) return;
  themeToggle.querySelector('[data-theme-label]').textContent =
    theme === 'dark' ? 'Dark' : 'Light';
};

updateToggleLabel(initialTheme);

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    themeToggle.setAttribute('aria-pressed', next === 'dark');
    updateToggleLabel(next);
  });
}

const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!prefersReducedMotion) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.2 }
  );

  document.querySelectorAll('[data-reveal]').forEach((element) => {
    observer.observe(element);
  });
}

const connect4Sidebar = document.querySelector('[data-connect4-sidebar]');
const connect4SidebarToggle = document.querySelector('[data-connect4-nav-toggle]');

if (connect4Sidebar && connect4SidebarToggle) {
  connect4SidebarToggle.addEventListener('click', () => {
    const isCollapsed = connect4Sidebar.classList.toggle('is-collapsed');
    connect4SidebarToggle.setAttribute('aria-expanded', String(!isCollapsed));
    connect4SidebarToggle.textContent = isCollapsed ? 'Show quick links' : 'Hide quick links';
  });
}
