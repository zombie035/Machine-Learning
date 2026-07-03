// Handle the form submit event and call the backend `/predict` endpoint.
document.getElementById('predict-form').addEventListener('submit', async (e) => {
  // Prevent default form submission (page reload)
  e.preventDefault();

  // Reference to the form so we can read values
  const form = e.target;

  // Build the payload object expected by the Flask backend.
  // Convert numeric fields to `Number` to ensure proper types.
  const data = {
    'no_of_dependents': Number(form.no_of_dependents.value),
    'self_employed': form.self_employed.value, // expects 'Yes' or 'No'
    'income_annum': Number(form.income_annum.value),
    'loan_amount': Number(form.loan_amount.value),
    'loan_term': Number(form.loan_term.value),
    'cibil_score': Number(form.cibil_score.value),
    'commercial_assets_value': Number(form.commercial_assets_value.value),
    'luxury_assets_value': Number(form.luxury_assets_value.value),
    'bank_asset_value': Number(form.bank_asset_value.value)
  };

  try {
    // Send JSON payload to `/predict` and wait for response
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    // Parse JSON body from response
    const json = await res.json();
    const out = document.getElementById('result');

    // If HTTP 200 OK, display prediction and optional probability
    if (res.ok) {
      // show styled success or reject
      if (json.prediction === 'Approved') {
        out.className = 'result success';
        out.innerHTML = `Approved ✅<div class="prob-bar"><div class="prob-fill" style="width:${((json.probability||0)*100).toFixed(1)}%"></div></div>`;
      } else {
        out.className = 'result reject';
        out.innerHTML = `Rejected ✖️<div class="prob-bar"><div class="prob-fill" style="width:${((json.probability||0)*100).toFixed(1)}%"></div></div>`;
      }
      if (json.probability!==null && json.probability!==undefined) {
        const p = document.createElement('div');
        p.style.marginTop='8px';
        p.style.fontWeight='500';
        p.textContent = `Confidence: ${(json.probability*100).toFixed(1)}%`;
        out.appendChild(p);
      }
    } else {
      // Show error message returned by backend
      out.className = 'result reject';
      out.textContent = `Error: ${json.error}`;
    }
  } catch (err) {
    // Network or unexpected error fallback
    document.getElementById('result').textContent = `Request failed: ${err.message}`;
  }
});

// Fill sample values into form when button clicked
document.getElementById('fill-sample').addEventListener('click', () => {
  const f = document.getElementById('predict-form');
  f.no_of_dependents.value = 2;
  f.self_employed.value = 'No';
  f.income_annum.value = 8000000;
  f.loan_amount.value = 25000000;
  f.loan_term.value = 10;
  f.cibil_score.value = 750;
  f.commercial_assets_value.value = 5000000;
  f.luxury_assets_value.value = 20000000;
  f.bank_asset_value.value = 7000000;
  document.getElementById('result').textContent = 'Example values loaded.';
});
