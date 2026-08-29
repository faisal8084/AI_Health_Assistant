/* ============================================================
   APP SHELL — routing, nav, settings
   ============================================================ */

function navigate(view, opts = {}) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  const target = document.getElementById(`view-${view}`);
  if (target) target.classList.add('active');

  document.querySelectorAll('.nav-link').forEach(l => {
    const active = l.dataset.nav === view;
    l.classList.toggle('active', active);
    if (active) l.setAttribute('aria-current', 'page');
    else l.removeAttribute('aria-current');
  });

  const mobileNav = document.getElementById('mobileNav');
  const hamburger = document.getElementById('hamburgerBtn');
  mobileNav.classList.remove('show');
  hamburger.classList.remove('open');
  hamburger.setAttribute('aria-expanded', 'false');

  window.scrollTo({ top: 0, behavior: 'smooth' });

  if (view === 'check') {
    const condition = opts.condition || formState.condition || 'diabetes';
    setCheckTab(condition);
  }
  if (view === 'chat') {
    initChat();
    wireChat();
  }
  if (view === 'dashboard') {
    renderDashboard();
  }
}

function setCheckTab(condition) {
  document.querySelectorAll('.check-tab').forEach(t => {
    const active = t.dataset.condition === condition;
    t.classList.toggle('active', active);
    t.setAttribute('aria-selected', String(active));
  });
  document.getElementById('formCard').style.display = '';
  document.getElementById('analyzingCard').style.display = 'none';
  document.getElementById('resultMount').innerHTML = '';
  renderForm(condition);
}

function wireNav() {
  document.addEventListener('click', (event) => {
    const navTarget = event.target.closest('[data-nav]');
    if (navTarget) {
      navigate(navTarget.dataset.nav, { condition: navTarget.dataset.condition });
      return;
    }
    const tab = event.target.closest('.check-tab');
    if (tab) setCheckTab(tab.dataset.condition);
  });

  const hamburger = document.getElementById('hamburgerBtn');
  const mobileNav = document.getElementById('mobileNav');
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobileNav.classList.toggle('show');
    hamburger.setAttribute('aria-expanded', String(mobileNav.classList.contains('show')));
  });
}

function wireSettings() {
  const modal = document.getElementById('settingsModal');
  const input = document.getElementById('apiBaseInput');
  const dialog = modal.querySelector('[role="dialog"]');
  let lastFocused = null;

  const closeModal = () => {
    modal.style.display = 'none';
    if (lastFocused) lastFocused.focus();
  };

  document.getElementById('settingsBtn').addEventListener('click', () => {
    lastFocused = document.activeElement;
    input.value = API.base;
    modal.style.display = 'flex';
    input.focus();
  });
  document.getElementById('settingsCloseBtn').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
  document.getElementById('settingsSaveBtn').addEventListener('click', () => {
    const val = input.value.trim();
    if (val) {
      API.setBase(val);
      showToast('Backend URL saved', 'success');
    }
    closeModal();
  });
  modal.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeModal();
    if (event.key !== 'Tab') return;
    const focusable = dialog.querySelectorAll('button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  wireNav();
  wireSettings();
  navigate('home');
  enableTilt(document);
});
