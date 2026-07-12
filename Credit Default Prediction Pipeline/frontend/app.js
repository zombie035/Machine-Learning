/* ═══════════════════════════════════════════════════════
   app.js — Credit Default Predictor Frontend Logic
   ═══════════════════════════════════════════════════════ */

const API_URL = "http://localhost:5000/predict";

/* ── Quick-fill data ────────────────────────────────── */
const LOW_RISK_SAMPLE = {
  LIMIT_BAL: 200000, SEX: 1, EDUCATION: 1, MARRIAGE: 2, AGE: 30,
  PAY_0: -1, PAY_2: -1, PAY_3: -1, PAY_4: -1, PAY_5: -1, PAY_6: -1,
  BILL_AMT1: 15000, BILL_AMT2: 14000, BILL_AMT3: 12000,
  BILL_AMT4: 10000, BILL_AMT5: 9000,  BILL_AMT6: 8000,
  PAY_AMT1: 15000, PAY_AMT2: 14000, PAY_AMT3: 12000,
  PAY_AMT4: 10000, PAY_AMT5: 9000,  PAY_AMT6: 8000,
};

const HIGH_RISK_SAMPLE = {
  LIMIT_BAL: 20000, SEX: 2, EDUCATION: 3, MARRIAGE: 1, AGE: 42,
  PAY_0: 2, PAY_2: 2, PAY_3: 3, PAY_4: 3, PAY_5: 2, PAY_6: 2,
  BILL_AMT1: 19800, BILL_AMT2: 19200, BILL_AMT3: 18500,
  BILL_AMT4: 17900, BILL_AMT5: 17300, BILL_AMT6: 16700,
  PAY_AMT1: 0, PAY_AMT2: 0, PAY_AMT3: 0,
  PAY_AMT4: 0, PAY_AMT5: 0, PAY_AMT6: 0,
};

/* ── DOM refs ───────────────────────────────────────── */
const form          = document.getElementById("predict-form");
const btnPredict    = document.getElementById("btn-predict");
const errorBanner   = document.getElementById("error-banner");
const errorMsg      = document.getElementById("error-msg");
const resultPanel   = document.getElementById("result-panel");

const resultCard    = document.getElementById("result-card");
const resultIcon    = document.getElementById("result-icon");
const resultLabel   = document.getElementById("result-label");
const resultDesc    = document.getElementById("result-desc");
const gaugeFill     = document.getElementById("gauge-fill");
const gaugePct      = document.getElementById("gauge-pct");
const rbPrediction  = document.getElementById("rb-prediction");
const rbProb        = document.getElementById("rb-prob");
const rbRisk        = document.getElementById("rb-risk");

/* ── Gauge constants ────────────────────────────────── */
const CIRCUMFERENCE = 2 * Math.PI * 40; // r=40 → 251.2

/* ── Helpers ────────────────────────────────────────── */
function setGauge(pct, color) {
  const offset = CIRCUMFERENCE * (1 - pct / 100);
  gaugeFill.style.strokeDashoffset = offset;
  gaugeFill.style.stroke = color;
  gaugePct.textContent = pct.toFixed(1) + "%";
}

function hideError()  { errorBanner.classList.remove("visible"); }
function showError(m) { errorMsg.textContent = m; errorBanner.classList.add("visible"); }

function setLoading(on) {
  btnPredict.classList.toggle("loading", on);
  btnPredict.disabled = on;
}

function fillForm(data) {
  Object.entries(data).forEach(([key, val]) => {
    const el = document.getElementById(key);
    if (el) el.value = val;
  });
}

function clearForm() {
  form.querySelectorAll("input, select").forEach(el => (el.value = ""));
  hideError();
  resultPanel.classList.remove("visible");
  resultPanel.style.display = "none";
}

/* ── Quick fill buttons ─────────────────────────────── */
document.getElementById("fill-low-risk").addEventListener("click",  () => fillForm(LOW_RISK_SAMPLE));
document.getElementById("fill-high-risk").addEventListener("click", () => fillForm(HIGH_RISK_SAMPLE));
document.getElementById("clear-form").addEventListener("click", clearForm);

/* ── Validation ─────────────────────────────────────── */
function validateForm() {
  let ok = true;
  form.querySelectorAll("[required]").forEach(el => {
    const empty = el.value === "" || el.value === null;
    el.classList.toggle("error", empty);
    if (empty) ok = false;
  });
  return ok;
}

/* Clear error state on input */
form.querySelectorAll("input, select").forEach(el => {
  el.addEventListener("input", () => el.classList.remove("error"));
  el.addEventListener("change", () => el.classList.remove("error"));
});

/* ── Collect form data ──────────────────────────────── */
function collectData() {
  const FEATURES = [
    "LIMIT_BAL","SEX","EDUCATION","MARRIAGE","AGE",
    "PAY_0","PAY_2","PAY_3","PAY_4","PAY_5","PAY_6",
    "BILL_AMT1","BILL_AMT2","BILL_AMT3","BILL_AMT4","BILL_AMT5","BILL_AMT6",
    "PAY_AMT1","PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6",
  ];
  const payload = {};
  FEATURES.forEach(f => {
    payload[f] = parseFloat(document.getElementById(f).value);
  });
  return payload;
}

/* ── Render result ──────────────────────────────────── */
function renderResult(res) {
  const { prediction, probability_pct, risk_level, label } = res;

  // Determine theme
  let theme, icon, desc, gaugeColor;
  if (prediction === 0 && probability_pct < 30) {
    theme = "safe";
    icon  = "✅";
    desc  = "This customer is unlikely to default. Low repayment risk detected based on their financial history.";
    gaugeColor = "var(--accent-green)";
  } else if (prediction === 1 || probability_pct >= 60) {
    theme = "risk";
    icon  = "🚨";
    desc  = "High default risk detected. The customer shows patterns consistent with credit default based on payment history and bill amounts.";
    gaugeColor = "var(--accent-red)";
  } else {
    theme = "medium";
    icon  = "⚠️";
    desc  = "Moderate risk detected. Some payment delays or elevated balances noted. Proceed with caution.";
    gaugeColor = "var(--accent-orange)";
  }

  // Apply theme
  resultCard.className = `result-card ${theme}`;
  resultIcon.textContent = icon;
  resultLabel.textContent = label;
  resultDesc.textContent  = desc;

  // Gauge (animate after render)
  gaugeFill.style.strokeDashoffset = CIRCUMFERENCE; // reset
  gaugeFill.style.stroke = gaugeColor;
  gaugePct.textContent = "—";

  setTimeout(() => setGauge(probability_pct, gaugeColor), 50);

  // Breakdown
  rbPrediction.textContent = prediction === 0 ? "No Default" : "Default";
  rbPrediction.style.color = prediction === 0 ? "var(--accent-green)" : "var(--accent-red)";
  rbProb.textContent  = probability_pct.toFixed(1) + "%";
  rbRisk.textContent  = risk_level;
  rbRisk.style.color  = theme === "safe" ? "var(--accent-green)" : theme === "risk" ? "var(--accent-red)" : "var(--accent-orange)";

  // Show panel
  resultPanel.style.display = "block";
  resultPanel.classList.add("visible");

  // Smooth scroll to result
  setTimeout(() => resultPanel.scrollIntoView({ behavior: "smooth", block: "nearest" }), 100);
}

/* ── Form submit ────────────────────────────────────── */
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  hideError();

  if (!validateForm()) {
    showError("Please fill in all required fields before predicting.");
    return;
  }

  setLoading(true);
  const payload = collectData();

  try {
    const resp = await fetch(API_URL, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(payload),
    });

    const data = await resp.json();

    if (!resp.ok || data.error) {
      throw new Error(data.error || `Server error: ${resp.status}`);
    }

    renderResult(data);

  } catch (err) {
    showError(`Prediction failed: ${err.message}. Make sure the Flask server is running on localhost:5000.`);
    console.error(err);
  } finally {
    setLoading(false);
  }
});

/* ── Quick-btn hover styles via JS (can't add :hover via HTML style) ── */
document.querySelectorAll(".quick-btn").forEach(btn => {
  btn.addEventListener("mouseenter", () => { btn.style.transform = "translateY(-1px)"; });
  btn.addEventListener("mouseleave", () => { btn.style.transform = "translateY(0)"; });
});
