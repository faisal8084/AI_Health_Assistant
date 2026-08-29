/* ============================================================
   API LAYER
   Talks to the existing FastAPI backend. No API keys live here —
   the Gemini key stays server-side (see backend/.env).
   ============================================================ */

const Store = {
  get(key, fallback) {
    try {
      const v = localStorage.getItem(key);
      return v === null ? fallback : JSON.parse(v);
    } catch { return fallback; }
  },
  set(key, val) {
    try { localStorage.setItem(key, JSON.stringify(val)); } catch {}
  },
  del(key) { try { localStorage.removeItem(key); } catch {} }
};

/* ---------------- Auth token storage ---------------- */
const Auth = {
  TOKEN_KEY: 'ahs_token',
  USER_KEY: 'ahs_user',

  getToken() { return Store.get(this.TOKEN_KEY, null); },
  setToken(token) { Store.set(this.TOKEN_KEY, token); },
  clearToken() { Store.del(this.TOKEN_KEY); },

  getUser() { return Store.get(this.USER_KEY, null); },
  setUser(user) { Store.set(this.USER_KEY, user); },
  clearUser() { Store.del(this.USER_KEY); },

  isAuthenticated() { return !!this.getToken(); },

  logoutLocal() {
    this.clearToken();
    this.clearUser();
  }
};

const API = {
  base: Store.get('ahs_api_base', 'https://ai-health-assistant-j1mk.onrender.com'),

  setBase(url) {
    this.base = url.replace(/\/+$/, '');
    Store.set('ahs_api_base', this.base);
  },

  async _request(path, options = {}) {
    const url = `${this.base}${path}`;
    const headers = { 'Content-Type': 'application/json' };

    if (options.auth !== false) {
      const token = Auth.getToken();
      if (token) headers['Authorization'] = `Bearer ${token}`;
    }

    let res;
    try {
      res = await fetch(url, {
        method: options.method || 'GET',
        headers,
        body: options.body ? JSON.stringify(options.body) : undefined,
      });
    } catch (err) {
      throw new ApiError(
        'Unable to connect to health service. Check that the backend is running and the API URL in settings is correct.',
        0
      );
    }

    let payload = null;
    try { payload = await res.json(); } catch {}

    if (res.status === 401 && options.auth !== false) {
      // Token missing/expired/invalid — send the user back to login.
      Auth.logoutLocal();
      if (!/\/(login|register)\.html$/.test(window.location.pathname)) {
        window.location.href = 'login.html';
      }
    }

    if (!res.ok) {
      const detail =
        (payload && (payload.detail || payload.message || payload.error)) ||
        'Something went wrong. Please try again.';
      const msg = Array.isArray(detail)
        ? detail.map(d => d.msg || JSON.stringify(d)).join(' ')
        : (typeof detail === 'string' ? detail : JSON.stringify(detail));
      throw new ApiError(msg, res.status);
    }

    return payload;
  },

  predictDiabetes(data) { return this._request('/predict/diabetes', { method: 'POST', body: data }); },
  predictHeart(data) { return this._request('/predict/heartDieses', { method: 'POST', body: data }); },
  predictTreatment(data) { return this._request('/predict/treatment', { method: 'POST', body: data }); },

  chat(sessionId, message) {
    return this._request('/chat', { method: 'POST', body: { session_id: sessionId, message } });
  },
  chatReset(sessionId) {
    return this._request('/chat/reset', { method: 'POST', body: { session_id: sessionId } });
  },

  /* ---------------- Auth endpoints ---------------- */
  register(data) {
    return this._request('/auth/register', { method: 'POST', body: data, auth: false });
  },
  login(email, password) {
    return this._request('/auth/login', { method: 'POST', body: { email, password }, auth: false });
  },
  me() {
    return this._request('/auth/me', { method: 'GET' });
  },
  logout() {
    return this._request('/auth/logout', { method: 'POST' }).catch(() => {});
  },
};

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

/* ---------------- Toasts ---------------- */
function showToast(message, type = 'info') {
  const stack = document.getElementById('toastStack');
  if (!stack) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.textContent = message;
  stack.appendChild(el);
  setTimeout(() => {
    el.style.transition = 'opacity 300ms ease';
    el.style.opacity = '0';
    setTimeout(() => el.remove(), 320);
  }, 4200);
}
