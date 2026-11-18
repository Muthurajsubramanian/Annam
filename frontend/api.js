// ===== Shared API helper for the Annam frontend =====
// Talks to the Django backend in /backend. Change API_BASE if you deploy
// the backend somewhere other than your local machine.

const API_BASE = 'http://127.0.0.1:8000/api';

function getToken() {
  return localStorage.getItem('annam_token');
}
function setSession(token, user) {
  localStorage.setItem('annam_token', token);
  localStorage.setItem('annam_user', JSON.stringify(user));
}
function clearSession() {
  localStorage.removeItem('annam_token');
  localStorage.removeItem('annam_user');
}
function getCurrentUser() {
  const raw = localStorage.getItem('annam_user');
  return raw ? JSON.parse(raw) : null;
}

/**
 * Wrapper around fetch() that adds the JSON content-type header and,
 * if the person is logged in, the auth token header automatically.
 */
async function apiFetch(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers['Authorization'] = `Token ${token}`;

  const res = await fetch(`${API_BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  let data = null;
  try { data = await res.json(); } catch (_) { /* empty response body */ }

  if (!res.ok) {
    const message = (data && (data.detail || Object.values(data)[0])) || 'Something went wrong.';
    throw new Error(Array.isArray(message) ? message[0] : message);
  }
  return data;
}

// ---- Small helper to show inline success/error text under a form ----
function showFormStatus(form, message, isError = false) {
  let statusEl = form.querySelector('.form-status');
  if (!statusEl) {
    statusEl = document.createElement('p');
    statusEl.className = 'form-status';
    form.appendChild(statusEl);
  }
  statusEl.textContent = message;
  statusEl.style.color = isError ? '#c0392b' : '#2e7d32';
  statusEl.style.marginTop = '12px';
  statusEl.style.fontFamily = 'var(--font-ui)';
  statusEl.style.fontSize = '14px';
}
