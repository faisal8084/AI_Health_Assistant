/* ============================================================
   HEALTH CHECK FORMS
   Field lists mirror backend/schemas/*.py exactly — names, types,
   literal option sets and numeric ranges are pulled 1:1 from the
   Pydantic schemas so the payload sent to /predict/* always
   validates.
   ============================================================ */

const CHECK_ICON = '<svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.6"/><path d="M8 12l2.5 2.5L16 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>';

const FORM_CONFIG = {
  diabetes: {
    title: 'Diabetes Risk Assessment',
    endpoint: (d) => API.predictDiabetes(d),
    infoTitle: 'What this checks',
    infoItems: [
      'Estimates diabetes risk from metabolic and lifestyle indicators.',
      'Powered by a trained XGBoost classifier.',
      'Takes about a minute to complete.',
    ],
    fields: [
      { name: 'gender', label: 'Gender', type: 'select', options: ['Female', 'Male', 'Other'], group: 'Personal Information' },
      { name: 'age', label: 'Age', type: 'number', min: 0, max: 120, step: 1, unit: 'years', group: 'Personal Information' },
      { name: 'age_group', label: 'Age Group', type: 'select', options: ['Child', 'Young', 'Adult', 'Middle_age', 'Senior'], hint: 'Should match your age above', group: 'Personal Information' },
      { name: 'bmi', label: 'BMI', type: 'number', min: 0.1, max: 100, step: 0.1, unit: 'kg/m²', group: 'Vitals', tip: 'Body Mass Index = weight(kg) / height(m)²' },
      { name: 'bmi_category', label: 'BMI Category', type: 'select', options: ['Underweight', 'Normal weight', 'Overweight', 'Obesity class 1', 'Obesity class 2', 'Obesity class 3'], group: 'Vitals' },
      { name: 'HbA1c_level', label: 'HbA1c Level', type: 'number', min: 0, max: 20, step: 0.1, unit: '%', group: 'Vitals', tip: 'Average blood sugar over ~3 months' },
      { name: 'blood_glucose_level', label: 'Blood Glucose Level', type: 'number', min: 0, max: 1000, step: 1, unit: 'mg/dL', group: 'Vitals' },
      { name: 'smoking_history', label: 'Smoking History', type: 'select', options: ['never', 'No Info', 'current', 'former', 'ever', 'not current'], group: 'Lifestyle' },
      { name: 'hypertension', label: 'Hypertension', type: 'yesno', group: 'Lifestyle' },
      { name: 'heart_disease', label: 'Existing Heart Disease', type: 'yesno', group: 'Lifestyle' },
    ],
  },

  heart: {
    title: 'Heart Disease Risk Assessment',
    endpoint: (d) => API.predictHeart(d),
    infoTitle: 'What this checks',
    infoItems: [
      'Evaluates cardiac risk from clinical vitals.',
      'Powered by a trained XGBoost classifier.',
      'Have a recent ECG or checkup handy for accuracy.',
    ],
    fields: [
      { name: 'age', label: 'Age', type: 'number', min: 1, max: 100, step: 1, unit: 'years', group: 'Personal Information' },
      { name: 'sex', label: 'Sex', type: 'select', options: [{ v: 0, l: 'Female' }, { v: 1, l: 'Male' }], group: 'Personal Information' },
      { name: 'resting_bp_s', label: 'Resting Blood Pressure', type: 'number', min: 50, max: 300, step: 1, unit: 'mm Hg (systolic)', group: 'Vitals' },
      { name: 'cholesterol', label: 'Cholesterol', type: 'number', min: 90, max: 450, step: 1, unit: 'mg/dL', group: 'Vitals' },
      { name: 'max_heart_rate', label: 'Max Heart Rate', type: 'number', min: 70, max: 210, step: 1, unit: 'bpm', group: 'Vitals' },
      { name: 'fasting_blood_sugar', label: 'Fasting Blood Sugar > 120 mg/dL', type: 'yesno', group: 'Vitals' },
      { name: 'chest_pain_type', label: 'Chest Pain Type', type: 'select', options: [{ v: 1, l: '1 — Typical angina' }, { v: 2, l: '2 — Atypical angina' }, { v: 3, l: '3 — Non-anginal pain' }, { v: 4, l: '4 — Asymptomatic' }], group: 'Clinical' },
      { name: 'resting_ecg', label: 'Resting ECG Result', type: 'select', options: [{ v: 0, l: '0 — Normal' }, { v: 1, l: '1 — ST-T abnormality' }, { v: 2, l: '2 — Left ventricular hypertrophy' }], group: 'Clinical' },
      { name: 'st_slope', label: 'ST Slope', type: 'select', options: [{ v: 0, l: '0 — Upsloping' }, { v: 1, l: '1 — Flat' }, { v: 2, l: '2 — Downsloping' }], group: 'Clinical' },
      { name: 'oldpeak', label: 'Oldpeak (ST depression)', type: 'number', min: -5, max: 10, step: 0.1, group: 'Clinical' },
      { name: 'exercise_angina', label: 'Exercise-Induced Angina', type: 'yesno', group: 'Clinical' },
    ],
  },

  treatment: {
    title: 'Treatment-Need Assessment',
    endpoint: (d) => API.predictTreatment(d),
    infoTitle: 'What this checks',
    infoItems: [
      'Gauges whether workplace mental-health treatment may be indicated.',
      'Based on a workplace mental-health survey model.',
      'All answers stay on your device except for the prediction request.',
    ],
    fields: [
      { name: 'Age', label: 'Age', type: 'number', min: 0, max: 120, step: 1, unit: 'years', group: 'Personal Information' },
      { name: 'Gender', label: 'Gender', type: 'select', options: ['Female', 'Male', 'Other'], group: 'Personal Information' },
      { name: 'Country', label: 'Country', type: 'text', placeholder: 'e.g. United States', group: 'Personal Information' },
      { name: 'self_employed', label: 'Self-employed?', type: 'yesno', stringYesNo: true, group: 'Work' },
      { name: 'tech_company', label: 'Work at a tech company?', type: 'yesno', stringYesNo: true, group: 'Work' },
      { name: 'remote_work', label: 'Remote work?', type: 'yesno', stringYesNo: true, group: 'Work' },
      { name: 'no_employees', label: 'Company size', type: 'select', options: ['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000'], group: 'Work' },
      { name: 'family_history', label: 'Family history of mental illness?', type: 'yesno', stringYesNo: true, group: 'Background' },
      { name: 'work_interfere', label: 'Does mental health interfere with work?', type: 'select', options: ['Never', 'Rarely', 'Sometimes', 'Often', 'Unknown'], group: 'Background' },
      { name: 'benefits', label: 'Employer provides mental-health benefits?', type: 'select', options: ['Yes', 'No', "Don't know"], group: 'Workplace Support' },
      { name: 'care_options', label: 'Aware of mental-health care options?', type: 'select', options: ['Yes', 'No', 'Not sure'], group: 'Workplace Support' },
      { name: 'wellness_program', label: 'Employer has a wellness program?', type: 'select', options: ['Yes', 'No', "Don't know"], group: 'Workplace Support' },
      { name: 'seek_help', label: 'Employer encourages seeking help?', type: 'select', options: ['Yes', 'No', "Don't know"], group: 'Workplace Support' },
      { name: 'anonymity', label: 'Is anonymity protected if you seek treatment?', type: 'select', options: ['Yes', 'No', "Don't know"], group: 'Workplace Support' },
      { name: 'leave', label: 'How easy is mental-health leave?', type: 'select', options: ['Very easy', 'Somewhat easy', "Don't know", 'Somewhat difficult', 'Very difficult'], group: 'Workplace Support' },
      { name: 'mental_health_consequence', label: 'Negative consequence for discussing mental health?', type: 'select', options: ['Yes', 'No', 'Maybe'], group: 'Openness' },
      { name: 'phys_health_consequence', label: 'Negative consequence for discussing physical health?', type: 'select', options: ['Yes', 'No', 'Maybe'], group: 'Openness' },
      { name: 'coworkers', label: 'Comfortable discussing with coworkers?', type: 'select', options: ['Yes', 'No', 'Some of them'], group: 'Openness' },
      { name: 'supervisor', label: 'Comfortable discussing with supervisor?', type: 'select', options: ['Yes', 'No', 'Some of them'], group: 'Openness' },
      { name: 'mental_health_interview', label: 'OK to be asked about mental health in an interview?', type: 'select', options: ['Yes', 'No', 'Maybe'], group: 'Openness' },
      { name: 'phys_health_interview', label: 'OK to be asked about physical health in an interview?', type: 'select', options: ['Yes', 'No', 'Maybe'], group: 'Openness' },
      { name: 'mental_vs_physical', label: 'Employer treats mental health as seriously as physical?', type: 'select', options: ['Yes', 'No', "Don't know"], group: 'Openness' },
      { name: 'obs_consequence', label: 'Observed negative consequences for coworkers?', type: 'yesno', stringYesNo: true, group: 'Openness' },
    ],
  },
};

const formState = {
  condition: 'diabetes',
  values: {},
};

function fieldValueKey(condition, name) { return `${condition}:${name}`; }

function renderForm(condition) {
  formState.condition = condition;
  const cfg = FORM_CONFIG[condition];
  const card = document.getElementById('formCard');
  document.getElementById('resultMount').innerHTML = '';
  document.getElementById('analyzingCard').style.display = 'none';
  card.style.display = '';

  // group fields
  const groups = [];
  cfg.fields.forEach(f => {
    let g = groups.find(g => g.name === f.group);
    if (!g) { g = { name: f.group, fields: [] }; groups.push(g); }
    g.fields.push(f);
  });

  const fieldsHtml = groups.map(g => `
    <div class="field-full" style="margin-top:4px;">
      <h4 style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.04em; color:var(--ink-faint); margin-bottom:2px;">${g.name}</h4>
    </div>
    ${g.fields.map(f => renderField(condition, f)).join('')}
  `).join('');

  card.innerHTML = `
    <div class="form-progress">
      <div class="form-progress-bar"><div class="form-progress-fill" id="progressFill"></div></div>
      <div class="form-progress-text" id="progressText">0 / ${cfg.fields.length}</div>
    </div>
    <h3 style="margin-bottom:4px;">${cfg.title}</h3>
    <p style="margin-bottom:22px; font-size:0.88rem;">Fields marked required map directly to the trained model's inputs.</p>
    <form id="checkForm" novalidate>
      <div class="field-grid">${fieldsHtml}</div>
      <div class="form-footer">
        <span style="font-size:0.8rem; color:var(--ink-faint);">All fields required</span>
        <button type="submit" class="btn btn-primary" id="analyzeBtn">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/></svg>
          Analyze My Health
        </button>
      </div>
    </form>
  `;

  renderInfoPanel(condition);

  const form = document.getElementById('checkForm');
  form.addEventListener('input', () => updateProgress(condition));
  form.addEventListener('change', () => updateProgress(condition));
  form.addEventListener('submit', (e) => { e.preventDefault(); handleSubmit(condition); });

  cfg.fields.forEach(f => {
    if (f.type === 'yesno') bindYesNo(condition, f.name);
  });

  if (condition === 'diabetes') bindDiabetesAutoCategories();

  updateProgress(condition);
}

function bindDiabetesAutoCategories() {
  const ageInput = document.getElementById('f_diabetes_age');
  const bmiInput = document.getElementById('f_diabetes_bmi');
  const ageGroupSel = document.getElementById('f_diabetes_age_group');
  const bmiCatSel = document.getElementById('f_diabetes_bmi_category');

  ageInput.addEventListener('input', () => {
    const age = parseFloat(ageInput.value);
    if (Number.isNaN(age) || ageGroupSel.dataset.touched) return;
    let group = 'Adult';
    if (age < 13) group = 'Child';
    else if (age < 25) group = 'Young';
    else if (age < 45) group = 'Adult';
    else if (age < 65) group = 'Middle_age';
    else group = 'Senior';
    ageGroupSel.value = group;
  });
  ageGroupSel.addEventListener('change', () => { ageGroupSel.dataset.touched = '1'; });

  bmiInput.addEventListener('input', () => {
    const bmi = parseFloat(bmiInput.value);
    if (Number.isNaN(bmi) || bmiCatSel.dataset.touched) return;
    let cat = 'Normal weight';
    if (bmi < 18.5) cat = 'Underweight';
    else if (bmi < 25) cat = 'Normal weight';
    else if (bmi < 30) cat = 'Overweight';
    else if (bmi < 35) cat = 'Obesity class 1';
    else if (bmi < 40) cat = 'Obesity class 2';
    else cat = 'Obesity class 3';
    bmiCatSel.value = cat;
  });
  bmiCatSel.addEventListener('change', () => { bmiCatSel.dataset.touched = '1'; });
}

function renderField(condition, f) {
  const id = `f_${condition}_${f.name}`;
  const tip = f.tip ? `<i class="tip-icon" data-tip="${f.tip}">i</i>` : '';
  const label = `<label for="${id}">${f.label} ${tip} ${f.unit ? `<span class="hint">(${f.unit})</span>` : ''}</label>`;
  const errorEl = `<span class="field-error" id="${id}_err"></span>`;

  if (f.type === 'select') {
    const opts = f.options.map(o => {
      const val = typeof o === 'object' ? o.v : o;
      const lbl = typeof o === 'object' ? o.l : o;
      return `<option value="${val}">${lbl}</option>`;
    }).join('');
    return `<div class="field"><label for="${id}">${f.label} ${tip}</label>
      <select id="${id}" data-field="${f.name}" data-type="select">
        <option value="" disabled selected>Select…</option>${opts}
      </select>${errorEl}</div>`;
  }

  if (f.type === 'number') {
    return `<div class="field">${label}
      <input type="number" id="${id}" data-field="${f.name}" data-type="number" min="${f.min}" max="${f.max}" step="${f.step || 1}" placeholder="e.g. ${Math.round((f.min + f.max) / 2)}" />
      ${errorEl}</div>`;
  }

  if (f.type === 'text') {
    return `<div class="field">${label}
      <input type="text" id="${id}" data-field="${f.name}" data-type="text" placeholder="${f.placeholder || ''}" />
      ${errorEl}</div>`;
  }

  if (f.type === 'yesno') {
    return `<div class="field">${label}
      <div class="seg" id="${id}" data-field="${f.name}" data-type="yesno">
        <button type="button" data-val="0">No</button>
        <button type="button" data-val="1">Yes</button>
      </div>${errorEl}</div>`;
  }

  return '';
}

function bindYesNo(condition, name) {
  const id = `f_${condition}_${name}`;
  const seg = document.getElementById(id);
  if (!seg) return;
  seg.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      seg.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      seg.dataset.value = btn.dataset.val;
      updateProgress(condition);
    });
  });
}

function renderInfoPanel(condition) {
  const cfg = FORM_CONFIG[condition];
  document.getElementById('infoPanel').innerHTML = `
    <h4>${cfg.infoTitle}</h4>
    <ul class="info-list">
      ${cfg.infoItems.map(i => `<li><span class="dot"></span>${i}</li>`).join('')}
    </ul>
    <div class="disclaimer-box">
      <span>⚕️</span>
      <span>This tool provides informational insights only and is not a medical diagnosis.</span>
    </div>
  `;
}

function updateProgress(condition) {
  const cfg = FORM_CONFIG[condition];
  const form = document.getElementById('checkForm');
  if (!form) return;
  let filled = 0;
  cfg.fields.forEach(f => {
    if (getFieldValue(condition, f) !== null) filled++;
  });
  const pct = Math.round((filled / cfg.fields.length) * 100);
  document.getElementById('progressFill').style.width = pct + '%';
  document.getElementById('progressText').textContent = `${filled} / ${cfg.fields.length}`;
}

function getFieldValue(condition, f) {
  const id = `f_${condition}_${f.name}`;
  if (f.type === 'yesno') {
    const seg = document.getElementById(id);
    return seg && seg.dataset.value !== undefined ? seg.dataset.value : null;
  }
  const el = document.getElementById(id);
  if (!el) return null;
  const v = el.value;
  return v === '' ? null : v;
}

function validateAndCollect(condition) {
  const cfg = FORM_CONFIG[condition];
  const data = {};
  let firstInvalid = null;

  cfg.fields.forEach(f => {
    const id = `f_${condition}_${f.name}`;
    const errEl = document.getElementById(`${id}_err`);
    const raw = getFieldValue(condition, f);
    const controlEl = f.type === 'yesno' ? document.getElementById(id) : document.getElementById(id);
    let valid = raw !== null && raw !== '';
    let value = raw;

    if (valid && f.type === 'number') {
      const num = parseFloat(raw);
      value = num;
      if (Number.isNaN(num) || num < f.min || num > f.max) {
        valid = false;
        if (errEl) { errEl.textContent = `Enter a value between ${f.min} and ${f.max}.`; errEl.classList.add('show'); }
      }
    } else if (valid && (f.type === 'yesno')) {
      value = f.stringYesNo ? (raw === '1' ? 'Yes' : 'No') : parseInt(raw, 10);
    } else if (valid && f.type === 'select') {
      // keep numeric option values numeric
      const opt = f.options.find(o => (typeof o === 'object' ? String(o.v) : o) === raw);
      value = opt && typeof opt === 'object' ? opt.v : raw;
    }

    if (errEl) errEl.classList.toggle('show', !valid);
    if (controlEl) controlEl.classList.toggle('invalid', !valid);

    if (!valid) {
      if (errEl && !errEl.textContent) errEl.textContent = 'This field is required.';
      if (!firstInvalid) firstInvalid = controlEl;
    } else {
      data[f.name] = value;
    }
  });

  return { data, valid: !firstInvalid, firstInvalid };
}

async function handleSubmit(condition) {
  const { data, valid, firstInvalid } = validateAndCollect(condition);
  if (!valid) {
    showToast('Please check the highlighted fields and try again.', 'error');
    if (firstInvalid) firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return;
  }

  document.getElementById('formCard').style.display = 'none';
  document.getElementById('resultMount').innerHTML = '';
  const analyzingCard = document.getElementById('analyzingCard');
  analyzingCard.style.display = '';

  const steps = ['Validating inputs…', 'Running trained model…', 'Calculating risk score…', 'Preparing your results…'];
  let i = 0;
  const stepsEl = document.getElementById('analyzingSteps');
  const stepTimer = setInterval(() => {
    i = (i + 1) % steps.length;
    stepsEl.textContent = steps[i];
  }, 650);

  const start = Date.now();
  try {
    const cfg = FORM_CONFIG[condition];
    const res = await cfg.endpoint(data);
    const elapsed = Date.now() - start;
    await wait(Math.max(0, 900 - elapsed)); // keep the loading state feeling substantial, never instant/jarring

    saveResultToDashboard(condition, res, data);
    renderResultCard(condition, res);
  } catch (err) {
    showToast(err.message || 'Unable to complete this assessment.', 'error');
    document.getElementById('resultMount').innerHTML = renderErrorCard(err.message);
  } finally {
    clearInterval(stepTimer);
    analyzingCard.style.display = 'none';
  }
}

function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

function riskClass(category) {
  if (!category) return 'neutral';
  const c = category.toLowerCase();
  if (c.includes('very high')) return 'vhigh';
  if (c.includes('high')) return 'high';
  if (c.includes('moderate')) return 'moderate';
  return 'low';
}

function renderErrorCard(message) {
  return `
    <div class="card" style="padding:32px; text-align:center;">
      <div class="empty-state" style="padding:10px;">
        <div class="icon-wrap" style="background:var(--risk-high-bg); color:var(--risk-high);">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/></svg>
        </div>
        <h3>We couldn't complete this assessment</h3>
        <p>${escapeHtml(message || 'Please check your information and try again.')}</p>
        <button class="btn btn-primary" onclick="renderForm(formState.condition); document.getElementById('formCard').style.display='';">Try again</button>
      </div>
    </div>`;
}

function renderResultCard(condition, apiResponse) {
  const result = apiResponse.result;
  const isTreatment = condition === 'treatment';
  const prediction = isTreatment ? result : result.prediction;
  const probability = isTreatment ? null : result.probability_percent;
  const category = isTreatment
    ? (prediction === 1 ? 'Moderate Risk' : 'Low Risk')
    : result.risk_category;
  const rClass = riskClass(category);

  const titleMap = { diabetes: 'Diabetes Assessment', heart: 'Heart Health Assessment', treatment: 'Treatment Assessment' };
  const subMap = {
    diabetes: prediction === 1 ? 'Your inputs suggest an elevated diabetes risk.' : 'Your inputs suggest a lower diabetes risk.',
    heart: prediction === 1 ? 'Your inputs suggest an elevated heart disease risk.' : 'Your inputs suggest a lower heart disease risk.',
    treatment: prediction === 1 ? 'Based on your answers, treatment support may be worth exploring.' : 'Based on your answers, treatment does not appear strongly indicated.',
  };

  const ringHtml = isTreatment
    ? `<div class="result-ring"><div class="ring-center">
         <div class="ring-value">${prediction === 1 ? 'YES' : 'NO'}</div>
         <div class="ring-label">Indicated</div>
       </div></div>`
    : `<div class="result-ring">
         ${buildRingHTML('resultRingCanvas', 168, 12, riskColor(rClass))}
         <div class="ring-center">
           <div class="ring-value mono">${Math.round(probability)}%</div>
           <div class="ring-label">Risk Score</div>
         </div></div>`;

  const barHtml = isTreatment ? '' : `<div class="result-bar"><div class="result-bar-fill" id="resultBarFill"></div></div>`;

  document.getElementById('resultMount').innerHTML = `
    <div class="result-wrap">
      <div class="card result-card tilt3d risk-${rClass}">
        <div class="result-kicker">Health Assessment</div>
        ${ringHtml}
        <div class="badge badge-${rClass}" style="margin-bottom:14px;">${category.toUpperCase()}</div>
        <h3 class="result-title">${titleMap[condition]}</h3>
        <p class="result-sub">${subMap[condition]}</p>
        ${barHtml}
        <div class="result-checks">
          <div class="check-row">${CHECK_ICON} Diabetes Risk ${condition === 'diabetes' ? '— just assessed' : '— see Health Check'}</div>
          <div class="check-row">${CHECK_ICON} Heart Health ${condition === 'heart' ? '— just assessed' : '— see Health Check'}</div>
          <div class="check-row">${CHECK_ICON} Treatment Assessment ${condition === 'treatment' ? '— just assessed' : '— see Health Check'}</div>
        </div>
        <div class="result-actions">
          <button class="btn btn-secondary" onclick="renderForm(formState.condition); document.getElementById('formCard').style.display='';">New Assessment</button>
          <button class="btn btn-primary" data-nav="dashboard">View Dashboard</button>
        </div>
      </div>

      ${renderInsightsSection()}

      <div class="card actions-card tilt3d">
        <h4>Recommended Actions</h4>
        <ul>
          <li>${CHECK_ICON} Maintain a healthy, balanced diet</li>
          <li>${CHECK_ICON} Get regular physical activity</li>
          <li>${CHECK_ICON} Monitor blood pressure periodically</li>
          <li>${CHECK_ICON} Maintain a healthy weight</li>
          <li>${CHECK_ICON} Consult a healthcare professional when appropriate</li>
        </ul>
      </div>

      <div class="medical-disclaimer">
        <svg viewBox="0 0 24 24" fill="none"><path d="M12 9v4M12 17h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" stroke="currentColor" stroke-width="1.6"/></svg>
        <span>${apiResponse.result && apiResponse.result.medical_disclaimer ? apiResponse.result.medical_disclaimer : 'This AI Health Assistant provides informational insights and is not a substitute for professional medical diagnosis or treatment.'}</span>
      </div>
    </div>
  `;

  document.getElementById('formCard').style.display = 'none';

  if (!isTreatment) {
    requestAnimationFrame(() => {
      document.getElementById('resultBarFill').style.width = Math.min(100, probability) + '%';
      animateRing('resultRingCanvas', probability);
    });
  }

  enableTilt(document.getElementById('resultMount'));
}

function riskColor(rClass) {
  return { low: 'var(--risk-low)', moderate: 'var(--risk-moderate)', high: 'var(--risk-high)', vhigh: 'var(--risk-vhigh)', neutral: 'var(--accent)' }[rClass] || 'var(--accent)';
}

/* ============================================================
   RINGS — dependency-free (plain inline SVG). No external
   charting library required, so this always renders — online,
   offline, or if a CDN is blocked.
   ============================================================ */

function buildRingHTML(id, size, strokeWidth, color) {
  const r = (size - strokeWidth) / 2;
  const c = 2 * Math.PI * r;
  const center = size / 2;
  return `
    <svg id="${id}" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="--circumference:${c};">
      <circle class="ring-track" cx="${center}" cy="${center}" r="${r}"></circle>
      <circle class="ring-progress" cx="${center}" cy="${center}" r="${r}"
        style="stroke:${color}; color:${color};" stroke-dasharray="${c}" stroke-dashoffset="${c}"></circle>
    </svg>`;
}

function animateRing(id, percent) {
  const svg = document.getElementById(id);
  if (!svg) return;
  const progress = svg.querySelector('.ring-progress');
  if (!progress) return;
  const c = parseFloat(svg.style.getPropertyValue('--circumference'));
  const clamped = Math.max(0, Math.min(100, percent));
  const offset = c - (clamped / 100) * c;
  // set full first, then animate to target on next frame so the
  // CSS transition on stroke-dashoffset actually runs
  progress.style.strokeDashoffset = c;
  requestAnimationFrame(() => {
    requestAnimationFrame(() => { progress.style.strokeDashoffset = offset; });
  });
}

/* ============================================================
   3D TILT — lightweight pointer-follow tilt + glow for any
   element carrying the .tilt3d class. Re-run after each dynamic
   render since new cards keep appearing in the DOM.
   ============================================================ */

function enableTilt(root) {
  const scope = root || document;
  scope.querySelectorAll('.tilt3d').forEach(card => {
    if (card._tiltBound) return;
    card._tiltBound = true;
    card.addEventListener('pointermove', (e) => {
      if (e.pointerType === 'touch') return;
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width;
      const y = (e.clientY - rect.top) / rect.height;
      const rotX = (0.5 - y) * 7;
      const rotY = (x - 0.5) * 9;
      card.style.setProperty('--tiltX', rotX.toFixed(2) + 'deg');
      card.style.setProperty('--tiltY', rotY.toFixed(2) + 'deg');
      card.style.setProperty('--glow-x', (x * 100).toFixed(1) + '%');
      card.style.setProperty('--glow-y', (y * 100).toFixed(1) + '%');
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--tiltX', '0deg');
      card.style.setProperty('--tiltY', '0deg');
    });
  });
}

function renderInsightsSection() {
  const results = getStoredResults();
  const items = [
    { key: 'diabetes', emoji: '🩸', label: 'Diabetes' },
    { key: 'heart', emoji: '❤️', label: 'Heart Health' },
    { key: 'treatment', emoji: '💊', label: 'Treatment Assessment' },
  ];
  return `
    <div class="insights-grid">
      ${items.map(it => {
        const r = results[it.key];
        return `<div class="card insight-card tilt3d">
          <div class="row1"><span class="emoji">${it.emoji}</span>${r ? `<span class="badge badge-${riskClass(r.category)}">${r.category}</span>` : ''}</div>
          <h4>${it.label}</h4>
          <p>${r ? (r.probability !== null ? `Estimated risk: ${Math.round(r.probability)}%` : (r.prediction === 1 ? 'May need further evaluation' : 'No strong indication found')) : 'Not yet assessed'}</p>
        </div>`;
      }).join('')}
    </div>
  `;
}

function escapeHtml(str) {
  const d = document.createElement('div');
  d.textContent = str || '';
  return d.innerHTML;
}
