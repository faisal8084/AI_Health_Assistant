/* ============================================================
   LOGIN / REGISTER PAGE LOGIC
   ============================================================ */

// If already logged in, skip straight to the dashboard.
if (Auth.isAuthenticated()) {
  window.location.href = 'index.html';
}

function showAlert(message, type = 'error') {
  const box = document.getElementById('authAlert');
  if (!box) return;
  box.textContent = message;
  box.className = `auth-alert show ${type}`;
}

function hideAlert() {
  const box = document.getElementById('authAlert');
  if (!box) return;
  box.className = 'auth-alert';
}

function setFieldError(inputEl, errorEl, show) {
  if (!inputEl || !errorEl) return;
  inputEl.classList.toggle('invalid', !!show);
  errorEl.classList.toggle('show', !!show);
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

function wirePasswordToggle(toggleId, inputId, eyeIconId) {
  const toggle = document.getElementById(toggleId);
  const input = document.getElementById(inputId);
  const eye = document.getElementById(eyeIconId);
  if (!toggle || !input) return;

  toggle.addEventListener('click', () => {
    const isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';
    toggle.setAttribute('aria-label', isHidden ? 'Hide password' : 'Show password');
    if (eye) {
      eye.innerHTML = isHidden
        ? '<path d="M3 3l18 18M10.6 10.6a3 3 0 004.24 4.24M9.9 5.1A11 11 0 0123 12s-1.6 2.8-4.4 4.9M6.1 6.1C3.9 7.6 2 10 1 12c0 0 4 7 11 7 1.6 0 3-.3 4.3-.9" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
        : '<path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.7"/>';
    }
  });
}

function passwordScore(pw) {
  let score = 0;
  if (pw.length >= 8) score++;
  if (/[a-z]/.test(pw) && /[A-Z]/.test(pw)) score++;
  if (/\d/.test(pw)) score++;
  if (/[^A-Za-z0-9]/.test(pw) && pw.length >= 10) score++;
  return score; // 0-4
}

function passwordIsStrongEnough(pw) {
  return pw.length >= 8 && /[a-z]/.test(pw) && /[A-Z]/.test(pw) && /\d/.test(pw);
}

/* ---------------- LOGIN PAGE ---------------- */
function initLoginForm() {
  const form = document.getElementById('loginForm');
  if (!form) return;

  wirePasswordToggle('togglePassword', 'password', 'eyeIcon');

  const forgot = document.getElementById('forgotPasswordLink');
  if (forgot) {
    forgot.addEventListener('click', (e) => {
      e.preventDefault();
      showAlert('Password reset isn\u2019t available in this demo yet. Please contact support.', 'error');
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    let valid = true;
    if (!isValidEmail(email)) {
      setFieldError(emailInput, document.getElementById('emailError'), true);
      valid = false;
    } else {
      setFieldError(emailInput, document.getElementById('emailError'), false);
    }
    if (!password) {
      setFieldError(passwordInput, document.getElementById('passwordError'), true);
      valid = false;
    } else {
      setFieldError(passwordInput, document.getElementById('passwordError'), false);
    }
    if (!valid) return;

    const btn = document.getElementById('loginBtn');
    const btnText = document.getElementById('loginBtnText');
    btn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span>Logging in\u2026';

    try {
      const result = await API.login(email, password);
      Auth.setToken(result.access_token);

      const me = await API.me();
      Auth.setUser(me);

      showAlert('Login successful \u2014 redirecting\u2026', 'success');
      setTimeout(() => { window.location.href = 'index.html'; }, 500);
    } catch (err) {
      showAlert(err.message || 'Login failed. Please try again.', 'error');
      btn.disabled = false;
      btnText.textContent = 'Log in';
    }
  });
}

/* ---------------- REGISTER PAGE ---------------- */
function initRegisterForm() {
  const form = document.getElementById('registerForm');
  if (!form) return;

  wirePasswordToggle('togglePassword', 'password', 'eyeIcon');
  wirePasswordToggle('toggleConfirmPassword', 'confirmPassword', 'eyeIconConfirm');

  const passwordInput = document.getElementById('password');
  const strengthMeter = document.getElementById('strengthMeter');
  const strengthLabel = document.getElementById('strengthLabel');
  const labels = ['Very weak', 'Weak', 'Good', 'Strong'];

  passwordInput.addEventListener('input', () => {
    const score = Math.max(1, passwordScore(passwordInput.value));
    strengthMeter.className = `strength-meter strength-${passwordInput.value ? score : 0}`;
    strengthLabel.textContent = passwordInput.value
      ? labels[Math.min(score, 4) - 1]
      : 'Use 8+ characters with a mix of upper/lowercase and numbers.';
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    hideAlert();

    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const confirmInput = document.getElementById('confirmPassword');

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const confirmPassword = confirmInput.value;

    let valid = true;

    setFieldError(nameInput, document.getElementById('nameError'), name.length < 2);
    if (name.length < 2) valid = false;

    setFieldError(emailInput, document.getElementById('emailError'), !isValidEmail(email));
    if (!isValidEmail(email)) valid = false;

    const strongEnough = passwordIsStrongEnough(password);
    setFieldError(passwordInput, document.getElementById('passwordError'), !strongEnough);
    if (!strongEnough) valid = false;

    const passwordsMatch = password === confirmPassword && confirmPassword.length > 0;
    setFieldError(confirmInput, document.getElementById('confirmPasswordError'), !passwordsMatch);
    if (!passwordsMatch) valid = false;

    if (!valid) return;

    const btn = document.getElementById('registerBtn');
    const btnText = document.getElementById('registerBtnText');
    btn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span>Creating account\u2026';

    try {
      await API.register({ name, email, password, confirm_password: confirmPassword });
      showAlert('Account created \u2014 you can now log in.', 'success');
      setTimeout(() => { window.location.href = 'login.html'; }, 900);
    } catch (err) {
      showAlert(err.message || 'Registration failed. Please try again.', 'error');
      btn.disabled = false;
      btnText.textContent = 'Create account';
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initLoginForm();
  initRegisterForm();
});
