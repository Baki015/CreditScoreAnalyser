const API_URL = "http://127.0.0.1:8000";

const apiStatus = document.getElementById("apiStatus");
const form = document.getElementById("companyForm");
const fileInput = document.getElementById("fileInput");
const singleResult = document.getElementById("singleResult");
const portfolioSummary = document.getElementById("portfolioSummary");
const portfolioTable = document.getElementById("portfolioTable");
const riskBars = document.getElementById("riskBars");

function zoneClass(zone) {
  if (zone === "Safe") return "safe";
  if (zone === "Grey Zone") return "grey";
  return "distress";
}

function moneyValue(id) {
  return Number(document.getElementById(id).value);
}

function getFormData() {
  return {
    company_name: document.getElementById("company_name").value,
    working_capital: moneyValue("working_capital"),
    total_assets: moneyValue("total_assets"),
    retained_earnings: moneyValue("retained_earnings"),
    ebit: moneyValue("ebit"),
    market_value_equity: moneyValue("market_value_equity"),
    total_liabilities: moneyValue("total_liabilities"),
    sales: moneyValue("sales"),
  };
}

async function checkApi() {
  try {
    await fetch(`${API_URL}/api/health`);
    apiStatus.textContent = "API aktivan";
  } catch {
    apiStatus.textContent = "API nije pokrenut";
  }
}

function renderCompany(result) {
  singleResult.innerHTML = `
    <h2>${result.company_name}</h2>
    <div class="cards">
      <div class="card"><span>Z-Score</span><strong>${result.z_score}</strong></div>
      <div class="card"><span>Zona</span><strong><span class="badge ${zoneClass(result.zone)}">${result.zone}</span></strong></div>
      <div class="card"><span>ML rizik</span><strong>${result.risk_percent}%</strong></div>
    </div>
    <p><strong>${result.risk_level}</strong></p>
    <p class="muted">${result.recommendation}</p>
    <h3>Objašnjenje</h3>
    <ul class="explain">${result.explanation.map(item => `<li>${item}</li>`).join("")}</ul>
  `;
}

function renderSummary(summary) {
  const items = [
    ["Ukupno", summary.total],
    ["Safe", summary.safe],
    ["Grey", summary.grey],
    ["Distress", summary.distress],
    ["Prosječan rizik", `${summary.average_risk}%`],
  ];
  portfolioSummary.innerHTML = items.map(item => `
    <div class="summaryItem"><span>${item[0]}</span><strong>${item[1]}</strong></div>
  `).join("");
}

function renderBars(summary) {
  const total = summary.total || 1;
  const rows = [
    ["Safe", summary.safe, "#35a86b"],
    ["Grey", summary.grey, "#d5a929"],
    ["Distress", summary.distress, "#d9534f"],
  ];
  riskBars.innerHTML = rows.map(row => {
    const percent = Math.round((row[1] / total) * 100);
    return `
      <div class="barRow">
        <span>${row[0]}</span>
        <div class="barTrack"><div class="barFill" style="width:${percent}%;background:${row[2]}"></div></div>
        <strong>${percent}%</strong>
      </div>
    `;
  }).join("");
}

function renderPortfolio(results) {
  portfolioTable.innerHTML = `
    <thead>
      <tr>
        <th>Kompanija</th>
        <th>Z-Score</th>
        <th>Zona</th>
        <th>ML rizik</th>
        <th>Nivo</th>
        <th>Preporuka</th>
      </tr>
    </thead>
    <tbody>
      ${results.map(item => `
        <tr>
          <td>${item.company_name}</td>
          <td>${item.z_score}</td>
          <td><span class="badge ${zoneClass(item.zone)}">${item.zone}</span></td>
          <td>${item.risk_percent}%</td>
          <td>${item.risk_level}</td>
          <td>${item.recommendation}</td>
        </tr>
      `).join("")}
    </tbody>
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const response = await fetch(`${API_URL}/api/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(getFormData()),
  });
  const result = await response.json();
  renderCompany(result);
});

fileInput.addEventListener("change", async () => {
  const file = fileInput.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append("file", file);
  const response = await fetch(`${API_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });
  const data = await response.json();
  if (!response.ok) {
    portfolioTable.innerHTML = `<tr><td>${data.detail}</td></tr>`;
    return;
  }
  renderSummary(data.summary);
  renderBars(data.summary);
  renderPortfolio(data.results);
});

checkApi();
