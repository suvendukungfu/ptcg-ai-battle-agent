// State Management
let currentReplay = null;
let currentStepIdx = 0;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  fetchStatus();
  fetchAblations();
  fetchCodex();
  initBattleSimulator();
  initReplayScrubber();
});

// Tab Navigation
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const targetId = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach(content => {
        content.classList.remove("active");
      });
      const activeContent = document.getElementById(targetId);
      if (activeContent) {
        activeContent.classList.add("active");
      }
    });
  });
}

// Fetch System Status
async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    if (!res.ok) return;
    const data = await res.json();

    document.getElementById("stat-elo").textContent = data.best_elo.toFixed(1);
    document.getElementById("stat-win-rate").textContent = `${data.win_rate_meta.toFixed(1)}%`;
    document.getElementById("stat-latency").textContent = `${data.avg_decision_time_ms.toFixed(2)} ms`;
    document.getElementById("stat-fallback").textContent = `${data.fallback_rate_pct.toFixed(2)}%`;
    document.getElementById("active-deck-name").textContent = data.deck_name;
  } catch (err) {
    console.warn("Could not fetch status:", err);
  }
}

// Fetch Ablations
async function fetchAblations() {
  try {
    const res = await fetch("/api/ablations");
    if (!res.ok) return;
    const data = await res.json();
    const tbody = document.getElementById("ablation-table-body");
    tbody.innerHTML = "";

    data.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td><strong>${item.variant}</strong></td>
        <td style="color: var(--text-muted);">${item.description}</td>
        <td style="font-weight: 700; color: var(--accent-primary);">${item.elo.toFixed(1)}</td>
        <td style="font-weight: 700; color: ${item.win_rate >= 60 ? 'var(--accent-success)' : 'var(--text-main)'};">${item.win_rate.toFixed(1)}%</td>
        <td>${item.latency_ms.toFixed(2)} ms</td>
        <td style="color: var(--accent-success);">${item.fallback_rate.toFixed(2)}%</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Could not fetch ablations:", err);
  }
}

// Fetch Card Codex
async function fetchCodex() {
  try {
    const res = await fetch("/api/codex");
    if (!res.ok) return;
    const cards = await res.json();
    const container = document.getElementById("codex-container");
    container.innerHTML = "";

    cards.forEach(c => {
      const cardEl = document.createElement("div");
      cardEl.className = "codex-card";
      cardEl.innerHTML = `
        <img class="codex-img" src="${c.img}" alt="${c.name}" loading="lazy">
        <div class="codex-body">
          <div class="codex-name">${c.name}</div>
          <div style="font-size: 0.75rem; color: var(--accent-primary); font-weight: 600;">${c.category}</div>
          ${c.hp > 0 ? `<div style="font-size: 0.8rem; margin-top: 0.25rem;">HP: ${c.hp} | Atk Dmg: ${c.damage}</div>` : ''}
          <div class="codex-role">${c.role}</div>
        </div>
      `;
      container.appendChild(cardEl);
    });
  } catch (err) {
    console.warn("Could not fetch codex:", err);
  }
}

// Battle Simulator
function initBattleSimulator() {
  const btn = document.getElementById("btn-run-battle");
  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.innerHTML = `<span>⏳ Simulating Battle...</span>`;

    const p0 = document.getElementById("arena-p0-select").value;
    const p1 = document.getElementById("arena-p1-select").value;

    try {
      const res = await fetch("/api/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ p0_agent: p0, opponent: p1 }),
      });

      if (!res.ok) throw new Error("Simulation failed");
      const replay = await res.json();
      currentReplay = replay;
      displayBattleResults(replay);
    } catch (err) {
      alert("Error during simulation: " + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>⚡ Simulate Live Battle</span>`;
    }
  });
}

function displayBattleResults(replay) {
  document.getElementById("battle-results-container").style.display = "block";
  const winnerBanner = document.getElementById("battle-winner-banner");
  winnerBanner.textContent = `VICTORY (${replay.winner})`;
  winnerBanner.style.color = replay.winner === "YOU" ? "var(--accent-success)" : "var(--accent-danger)";

  document.getElementById("battle-steps-info").textContent = `Total Steps: ${replay.total_steps} | Duration: ${replay.duration_sec}s`;
  document.getElementById("battle-opponent-info").textContent = `Opponent Archetype: ${replay.opponent_archetype}`;

  // Configure replay scrubber slider
  const slider = document.getElementById("replay-step-slider");
  slider.max = Math.max(0, replay.timeline.length - 1);
  slider.value = 0;
  updateReplayStep(0);
}

// Replay Scrubber
function initReplayScrubber() {
  const slider = document.getElementById("replay-step-slider");
  slider.addEventListener("input", (e) => {
    updateReplayStep(parseInt(e.target.value, 10));
  });

  document.getElementById("btn-replay-prev").addEventListener("click", () => {
    if (!currentReplay) return;
    const nextVal = Math.max(0, parseInt(slider.value, 10) - 1);
    slider.value = nextVal;
    updateReplayStep(nextVal);
  });

  document.getElementById("btn-replay-next").addEventListener("click", () => {
    if (!currentReplay) return;
    const nextVal = Math.min(currentReplay.timeline.length - 1, parseInt(slider.value, 10) + 1);
    slider.value = nextVal;
    updateReplayStep(nextVal);
  });
}

function updateReplayStep(stepIdx) {
  if (!currentReplay || !currentReplay.timeline || !currentReplay.timeline[stepIdx]) {
    return;
  }
  currentStepIdx = stepIdx;
  const item = currentReplay.timeline[stepIdx];

  document.getElementById("replay-step-label").textContent = `Step ${item.step} / Turn ${item.turn}`;

  // Update Replay Tab View
  const p0Active = item.your_active;
  const p1Active = item.opp_active;

  document.getElementById("r-active").textContent = p0Active ? `Card #${p0Active.id} (HP: ${p0Active.hp}/${p0Active.maxHp || 100})` : "None";
  document.getElementById("r-opp-active").textContent = p1Active ? `Card #${p1Active.id} (HP: ${p1Active.hp}/${p1Active.maxHp || 100})` : "None";
  document.getElementById("r-prizes-you").textContent = item.your_prizes;
  document.getElementById("r-prizes-opp").textContent = item.opp_prizes;
  document.getElementById("r-action-chosen").textContent = item.action ? `Selected Option(s): ${JSON.stringify(item.action)}` : "None";

  // Update Arena Board Cards
  if (p0Active) {
    document.getElementById("p0-active-name").textContent = `Card #${p0Active.id}`;
    document.getElementById("p0-active-stats").textContent = `HP: ${p0Active.hp} | Energies: ${p0Active.energies ? p0Active.energies.length : 0}`;
    const pct = Math.max(0, Math.min(100, (p0Active.hp / (p0Active.maxHp || 350)) * 100));
    document.getElementById("p0-active-hp-bar").style.width = `${pct}%`;
  }
  document.getElementById("p0-prizes").textContent = item.your_prizes;

  if (p1Active) {
    document.getElementById("p1-active-name").textContent = `Card #${p1Active.id}`;
    document.getElementById("p1-active-stats").textContent = `HP: ${p1Active.hp} | Energies: ${p1Active.energies ? p1Active.energies.length : 0}`;
    const pct1 = Math.max(0, Math.min(100, (p1Active.hp / (p1Active.maxHp || 150)) * 100));
    document.getElementById("p1-active-hp-bar").style.width = `${pct1}%`;
  }
  document.getElementById("p1-prizes").textContent = item.opp_prizes;

  // Update Explainability view if decision available
  if (currentReplay.decisions && currentReplay.decisions[stepIdx]) {
    renderDecisionExplanation(currentReplay.decisions[stepIdx]);
  }
}

function renderDecisionExplanation(dec) {
  const container = document.getElementById("explainability-options-container");
  if (!container || !dec || !dec.options) return;

  container.innerHTML = "";
  const maxVal = Math.max(...dec.options.map(o => Math.abs(o.projected_value)), 1.0);

  dec.options.forEach(opt => {
    const node = document.createElement("div");
    node.className = `option-tree-node ${opt.is_chosen ? 'chosen' : ''}`;
    const pct = Math.max(5, Math.min(100, (opt.projected_value / maxVal) * 100));

    node.innerHTML = `
      <div>
        <strong style="color: ${opt.is_chosen ? 'var(--accent-success)' : 'var(--text-muted)'};">
          ${opt.is_chosen ? '[CHOSEN]' : '[REJECTED]'} Option ${opt.index}: ${opt.name}
        </strong>
        <div style="font-size: 0.78rem; color: var(--text-muted);">
          Action Bonus: +${opt.action_bonus} | Type Code: ${opt.type}
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-weight: 800; font-size: 1.1rem; color: ${opt.is_chosen ? 'var(--accent-success)' : 'var(--text-muted)'};">
          ${opt.projected_value > 0 ? '+' : ''}${opt.projected_value}
        </div>
        <div class="confidence-bar">
          <div class="confidence-fill" style="width: ${pct}%; background: ${opt.is_chosen ? 'var(--accent-success)' : 'var(--accent-primary)'};"></div>
        </div>
      </div>
    `;
    container.appendChild(node);
  });
}
