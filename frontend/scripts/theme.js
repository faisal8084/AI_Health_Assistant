/* ============================================================
   THEME (Light / Dark mode)
   The actual [data-theme] attribute is already set pre-paint by
   the inline script in <head> (see index.html / login.html /
   register.html) to avoid a flash of the wrong theme. This file
   just wires up the toggle button and keeps localStorage in sync
   across all pages.
   ============================================================ */

const Theme = {
  KEY: 'ahs_theme',

  get() {
    return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  },

  set(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem(this.KEY, theme); } catch {}
    this._updateIcon(theme);
  },

  toggle() {
    this.set(this.get() === 'dark' ? 'light' : 'dark');
  },

  _updateIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    icon.innerHTML = theme === 'dark'
      ? '<path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="4" fill="currentColor"/>'
      : '<path d="M12 3a9 9 0 109 9c0-.46-.04-.92-.1-1.36A5.4 5.4 0 0112 3z" fill="currentColor"/>';
  },

  init() {
    this._updateIcon(this.get());
    const btn = document.getElementById('themeToggle');
    if (btn) btn.addEventListener('click', () => this.toggle());
  }
};

document.addEventListener('DOMContentLoaded', () => Theme.init());
