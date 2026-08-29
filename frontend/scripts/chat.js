/* ============================================================
   AI CHAT
   Talks to the existing guided /chat endpoint (session-based
   question-by-question data collection + prediction). This is
   not a general-purpose Q&A bot — it walks the user through the
   same fields the ML models need, then returns a prediction.
   ============================================================ */

const CHAT_SESSION_KEY = 'ahs_chat_session_id';
const CHAT_HISTORY_KEY = 'ahs_chat_history';

function getSessionId() {
  let id = Store.get(CHAT_SESSION_KEY, null);
  if (!id) {
    id = 'sess_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
    Store.set(CHAT_SESSION_KEY, id);
  }
  return id;
}

function getChatHistory() { return Store.get(CHAT_HISTORY_KEY, []); }
function saveChatHistory(history) { Store.set(CHAT_HISTORY_KEY, history); }

function initChat() {
  const messagesEl = document.getElementById('chatMessages');
  const history = getChatHistory();
  messagesEl.innerHTML = '';

  if (!history.length) {
    appendMessage('bot', "Hi! I'm your AI Health Assistant. I can help assess your diabetes risk, heart disease risk, or whether treatment support may be worth exploring. What would you like to check?", false);
  } else {
    messagesEl.innerHTML = '';
    history.forEach(m => appendMessage(m.role, m.text, false));
  }
  scrollChatToBottom();
}

function appendMessage(role, text, persist = true, isError = false) {
  const messagesEl = document.getElementById('chatMessages');
  const el = document.createElement('div');
  el.className = `msg ${role === 'user' ? 'user' : 'bot'}${isError ? ' error' : ''}`;
  el.innerHTML = `
    <div class="msg-avatar">${role === 'user' ? '🧑' : '🩺'}</div>
    <div class="msg-bubble">${escapeHtml(text)}</div>
  `;
  messagesEl.appendChild(el);
  scrollChatToBottom();

  if (persist) {
    const history = getChatHistory();
    history.push({ role, text });
    saveChatHistory(history.slice(-60));
  }
}

function showTyping() {
  const messagesEl = document.getElementById('chatMessages');
  const el = document.createElement('div');
  el.className = 'msg bot';
  el.id = 'typingIndicator';
  el.innerHTML = `<div class="msg-avatar">🩺</div><div class="msg-bubble typing-bubble"><span></span><span></span><span></span></div>`;
  messagesEl.appendChild(el);
  scrollChatToBottom();
}
function hideTyping() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}

function scrollChatToBottom() {
  const messagesEl = document.getElementById('chatMessages');
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function sendChatMessage(text) {
  if (!text || !text.trim()) return;
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSendBtn');

  appendMessage('user', text);
  input.value = '';
  input.disabled = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const sessionId = getSessionId();
    const resp = await API.chat(sessionId, text);
    const result = resp.result;
    await wait(280); // brief pause so the typing indicator reads as natural, not instant
    hideTyping();

    if (result.message) appendMessage('bot', result.message);

    if (result.prediction) {
      renderChatPredictionCard(result.prediction);
      saveChatResultToDashboard(result.prediction);
    }

    if (result.conversation_ended) {
      showToast('Conversation reset. Say hello to start a new assessment.', 'success');
    }
  } catch (err) {
    hideTyping();
    appendMessage('bot', err.message || 'AI assistant is temporarily unavailable. Please try again.', true, true);
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

function renderChatPredictionCard(pred) {
  const isTreatment = pred.condition === 'treatment';
  const rClass = isTreatment ? (pred.prediction === 1 ? 'moderate' : 'low') : riskClass(pred.risk_category);
  const messagesEl = document.getElementById('chatMessages');
  const wrap = document.createElement('div');
  wrap.className = 'msg bot';
  wrap.style.maxWidth = '92%';
  wrap.innerHTML = `
    <div class="msg-avatar">🩺</div>
    <div class="card risk-${rClass}" style="padding:18px 20px; flex:1;">
      <div class="badge badge-${rClass}" style="margin-bottom:10px;">${isTreatment ? (pred.prediction === 1 ? 'TREATMENT MAY BE INDICATED' : 'TREATMENT NOT STRONGLY INDICATED') : pred.risk_category.toUpperCase()}</div>
      ${!isTreatment ? `<div style="font-family:var(--font-mono); font-size:1.4rem; font-weight:700; margin-bottom:6px;">${Math.round(pred.probability_percent)}%</div>` : ''}
      <p style="font-size:0.82rem;">${escapeHtml(pred.medical_disclaimer || '')}</p>
      <div style="margin-top:10px;">
        <button class="btn btn-secondary btn-sm" data-nav="dashboard">View Dashboard</button>
      </div>
    </div>
  `;
  messagesEl.appendChild(wrap);
  scrollChatToBottom();
}

function saveChatResultToDashboard(pred) {
  const results = getStoredResults();
  results[pred.condition] = {
    category: pred.risk_category || (pred.prediction === 1 ? 'Moderate Risk' : 'Low Risk'),
    probability: pred.probability_percent != null ? pred.probability_percent : null,
    prediction: pred.prediction,
    timestamp: Date.now(),
    inputData: null,
  };
  Store.set(RESULTS_KEY, results);
}

async function clearChat() {
  const sessionId = getSessionId();
  try {
    await API.chatReset(sessionId);
  } catch (err) {
    // Non-fatal — still clear the local view even if the backend
    // session couldn't be reached.
  }
  Store.del(CHAT_HISTORY_KEY);
  document.getElementById('chatMessages').innerHTML = '';
  initChat();
  showToast('Chat cleared', 'success');
}

function wireChat() {
  const input = document.getElementById('chatInput');
  const sendBtn = document.getElementById('chatSendBtn');
  if (input.dataset.wired === 'true') return;
  input.dataset.wired = 'true';

  sendBtn.addEventListener('click', () => sendChatMessage(input.value));
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendChatMessage(input.value);
  });

  document.getElementById('clearChatBtn').addEventListener('click', clearChat);

  document.querySelectorAll('.suggested-chip').forEach(chip => {
    chip.addEventListener('click', () => sendChatMessage(chip.textContent));
  });
}
