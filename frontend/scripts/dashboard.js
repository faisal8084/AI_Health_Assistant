/* ============================================================
   DASHBOARD
   Everything here is derived from assessments completed on this
   device (stored in localStorage) — nothing is fabricated. If the
   user hasn't run an assessment yet, that card/metric is omitted.

   NOTE: the score ring and the metrics chart are built with plain
   inline SVG / CSS (see buildRingHTML + animateRing in forms.js,
   and renderMetricBars below) — there is no external charting
   library involved, so this always renders, online or offline.
   ============================================================ */

const RESULTS_KEY = 'ahs_results';

function getStoredResults() {
  return Store.get(RESULTS_KEY, {});
}

function saveResultToDashboard(condition, apiResponse, inputData) {
  const results = getStoredResults();
  const result = apiResponse.result;
  const isTreatment = condition === 'treatment';

  results[condition] = {
    category: isTreatment ? (result === 1 ? 'Moderate Risk' : 'Low Risk') : result.risk_category,
    probability: isTreatment ? null : result.probability_percent,
    prediction: isTreatment ? result : result.prediction,
    timestamp: Date.now(),
    inputData,
  };

  Store.set(RESULTS_KEY, results);
}

function computeHealthScore(results) {
  const scored = [];
  if (results.diabetes) scored.push(100 - results.diabetes.probability);
  if (results.heart) scored.push(100 - results.heart.probability);
  if (results.treatment) scored.push(results.treatment.prediction === 1 ? 55 : 92);
  if (!scored.length) return null;
  return Math.round(scored.reduce((a, b) => a + b, 0) / scored.length);
}

function renderDashboard() {
  const results = getStoredResults();
  const hasAny = Object.keys(results).length > 0;
  const mount = document.getElementById('dashboardMount');

  if (!hasAny) {
    mount.innerHTML = `
      <div class="card empty-state">
        <div class="icon-wrap">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M4 19V5M4 19h16M4 15l4-5 3 3 5-7 4 5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <h3>No assessments yet</h3>
        <p>Complete a Health Check or chat with the AI Assistant to see your personalized dashboard here.</p>
        <button class="btn btn-primary" data-nav="check">Start Health Check</button>
      </div>`;
    return;
  }

  const score = computeHealthScore(results);
  const scoreColor = score === null ? 'var(--accent)' : score >= 75 ? 'var(--risk-low)' : score >= 50 ? 'var(--risk-moderate)' : 'var(--risk-high)';

  const riskDefs = [
    { key: 'diabetes', emoji: '🩸', label: 'Diabetes Risk' },
    { key: 'heart', emoji: '❤️', label: 'Heart Risk' },
    { key: 'treatment', emoji: '💊', label: 'Treatment Status' },
  ];

  mount.innerHTML = `
    <div class="dash-top stagger">
      <div class="card score-card tilt3d">
        <div class="score-ring-wrap">
          ${buildRingHTML('healthScoreRing', 148, 12, scoreColor)}
          <div class="score-ring-num">
            <div class="n mono">${score === null ? '—' : score}</div>
            <div class="d">/ 100</div>
          </div>
        </div>
        <h4 style="margin-bottom:4px;">Health Score</h4>
        <p style="font-size:0.82rem;">Derived from your completed assessments</p>
      </div>

      <div class="card metrics-card tilt3d">
        <h4>Health Metrics</h4>
        <div class="sub">Vitals recorded from your assessments</div>
        <div class="chart-wrap">${renderMetricBars(results)}</div>
      </div>
    </div>

    <div class="risk-cards stagger">
      ${riskDefs.map(rd => {
        const r = results[rd.key];
        if (!r) {
          return `<div class="card risk-card risk-neutral tilt3d">
            <div class="top"><span class="emoji-bubble">${rd.emoji}</span><span class="badge badge-neutral">Not assessed</span></div>
            <h4>${rd.label}</h4>
            <p style="font-size:0.82rem; margin-top:6px;">Run this assessment to see results here.</p>
          </div>`;
        }
        const rClass = riskClass(r.category);
        const pct = r.probability !== null ? Math.round(r.probability) : (r.prediction === 1 ? 65 : 15);
        return `<div class="card risk-card risk-${rClass} tilt3d">
          <div class="top"><span class="emoji-bubble">${rd.emoji}</span><span class="badge badge-${rClass}">${r.category}</span></div>
          <h4>${rd.label}</h4>
          <div class="val" style="color:${riskColor(rClass)};">${r.probability !== null ? Math.round(r.probability) + '%' : (r.prediction === 1 ? 'Indicated' : 'Not Indicated')}</div>
          <div class="mini-bar"><span data-target-width="${pct}%" style="background:${riskColor(rClass)}; color:${riskColor(rClass)};"></span></div>
        </div>`;
      }).join('')}
    </div>
  `;

  requestAnimationFrame(() => {
    if (score !== null) animateRing('healthScoreRing', score);
    mount.querySelectorAll('.mini-bar span, .metric-bar-fill').forEach(el => {
      requestAnimationFrame(() => { el.style.width = el.dataset.targetWidth; });
    });
    enableTilt(mount);
  });
}

/* ---- reasonable clinical ranges used purely to size each bar ---- */
const METRIC_RANGES = {
  bmi: { min: 10, max: 50, unit: '', label: 'BMI' },
  blood_glucose_level: { min: 60, max: 300, unit: ' mg/dL', label: 'Glucose' },
  HbA1c_level: { min: 3, max: 15, unit: '%', label: 'HbA1c' },
  resting_bp_s: { min: 50, max: 250, unit: ' mmHg', label: 'Resting BP' },
  cholesterol: { min: 90, max: 450, unit: ' mg/dL', label: 'Cholesterol' },
  max_heart_rate: { min: 70, max: 220, unit: ' bpm', label: 'Max Heart Rate' },
};

function renderMetricBars(results) {
  const d = results.diabetes && results.diabetes.inputData;
  const h = results.heart && results.heart.inputData;

  const rows = [];
  const push = (source, key, color) => {
    if (!source || source[key] == null) return;
    const val = source[key];
    const range = METRIC_RANGES[key];
    const pct = Math.max(4, Math.min(100, Math.round(((val - range.min) / (range.max - range.min)) * 100)));
    rows.push({ label: range.label, value: `${val}${range.unit}`, pct, color });
  };

  push(d, 'bmi', 'var(--primary)');
  push(d, 'blood_glucose_level', 'var(--primary)');
  push(d, 'HbA1c_level', 'var(--primary)');
  push(h, 'resting_bp_s', 'var(--accent)');
  push(h, 'cholesterol', 'var(--accent)');
  push(h, 'max_heart_rate', 'var(--accent)');

  if (!rows.length) {
    return `<p class="metric-bars-empty">No vitals recorded yet. Complete a Diabetes or Heart Disease assessment to populate this chart.</p>`;
  }

  return `
    <div class="metric-bars">
      ${rows.map((r, i) => `
        <div class="metric-bar-row" style="animation: slideUp 500ms ${0.05 * i}s both;">
          <div class="metric-bar-label">${r.label}</div>
          <div class="metric-bar-track">
            <div class="metric-bar-fill" data-target-width="${r.pct}%" style="width:0%; background:${r.color}; color:${r.color};"></div>
          </div>
          <div class="metric-bar-value mono">${r.value}</div>
        </div>
      `).join('')}
    </div>
  `;
}
