/* ============================================================
   AUTH GUARD (for index.html — the protected app shell)
   ============================================================ */

(function () {
  if (!Auth.isAuthenticated()) {
    window.location.href = 'login.html';
  }
})();

function wireLogout() {
  const btn = document.getElementById('logoutBtn');
  if (!btn) return;
  btn.addEventListener('click', async () => {
    btn.disabled = true;
    try {
      await API.logout();
    } finally {
      Auth.logoutLocal();
      window.location.href = 'login.html';
    }
  });
}

document.addEventListener('DOMContentLoaded', wireLogout);
