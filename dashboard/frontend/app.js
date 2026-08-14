/* ==========================================================================
   PTCG AI LAB - AUTONOMOUS RESEARCH ENGINE UI SCRIPT
   ========================================================================== */

let currentReplay = null;
let currentStepIdx = 0;
let isAutoPlaying = false;
let autoPlayTimer = null;

document.addEventListener("DOMContentLoaded", () => {
  initTabsAndKeybindings();
  fetchStatus();
  fetchBeliefs();
  fetchMistakes();
  fetchMetaPredictions();
  fetchAblations();
  fetchCodex();
  initBattleSimulator();
  initArenaControls();
  initBenchmarkRunner();
});

/* --------------------------------------------------------------------------
   1. Tabs & Keyboard Navigation (0-9)
   -------------------------------------------------------------------------- */
function initTabsAndKeybindings() {
  const tabs = document.querySelectorAll(".tab-btn");
  const tabIds = [
    "tab-overview",
    "tab-arena",
    "tab-replay",
    "tab-explainability",
    "tab-beliefs",
    "tab-mistakes",
    "tab-meta-forecast",
    "tab-ablations",
    "tab-benchmark",
    "tab-codex",
  ];

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => switchTab(tab.getAttribute("data-tab")));
  });

  // Keyboard number shortcuts (1-9, 0 for 10th tab)
  window.addEventListener("keydown", (e) => {
    if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT" || e.target.tagName === "TEXTAREA") {
      return;
    }
    if (e.key === "0") {
      switchTab("tab-codex");
      return;
    }
    const keyNum = parseInt(e.key, 10);
    if (!isNaN(keyNum) && keyNum >= 1 && keyNum <= tabIds.length) {
      switchTab(tabIds[keyNum - 1]);
    }
  });
}

function switchTab(targetId) {
  document.querySelectorAll(".tab-btn").forEach(t => {
    if (t.getAttribute("data-tab") === targetId) {
      t.classList.add("active");
    } else {
      t.classList.remove("active");
    }
  });

  document.querySelectorAll(".view-section").forEach(sec => {
    if (sec.id === targetId) {
      sec.classList.add("active");
    } else {
      sec.classList.remove("active");
    }
  });
}

/* --------------------------------------------------------------------------
   2. System Status & Telemetry
   -------------------------------------------------------------------------- */
async function fetchStatus() {
  try {
    const res = await fetch("/api/status");
    if (!res.ok) return;
    const data = await res.json();

    document.getElementById("stat-elo").textContent = data.best_elo.toFixed(1);
    document.getElementById("stat-win-rate").textContent = `${data.win_rate_meta.toFixed(1)}%`;
    document.getElementById("stat-latency").textContent = `${data.p95_latency_ms.toFixed(2)} ms`;
    document.getElementById("stat-fallback").textContent = `${data.fallback_rate_pct.toFixed(2)}%`;
    document.getElementById("deck-title-text").textContent = data.deck_name;
  } catch (err) {
    console.warn("Could not fetch status:", err);
  }
}

/* --------------------------------------------------------------------------
   3. Opponent Belief Lab
   -------------------------------------------------------------------------- */
async function fetchBeliefs() {
  try {
    const res = await fetch("/api/beliefs");
    if (!res.ok) return;
    const data = await res.json();

    document.getElementById("belief-gust-val").textContent = `${(data.gust_probability * 100).toFixed(1)}%`;
    document.getElementById("belief-energy-val").textContent = `${(data.energy_probability * 100).toFixed(1)}%`;
    document.getElementById("belief-switch-val").textContent = `${(data.switch_probability * 100).toFixed(1)}%`;
    document.getElementById("belief-evo-val").textContent = `${(data.evolution_probability * 100).toFixed(1)}%`;
  } catch (err) {
    console.warn("Could not fetch beliefs:", err);
  }
}

/* --------------------------------------------------------------------------
   4. Mistake Mining & Critique
   -------------------------------------------------------------------------- */
async function fetchMistakes() {
  try {
    const res = await fetch("/api/mistakes");
    if (!res.ok) return;
    const data = await res.json();
    const bd = data.breakdown || {};

    document.getElementById("mistake-crit-count").textContent = bd.CRITICAL_MISTAKE || 0;
    document.getElementById("mistake-miss-count").textContent = bd.MISSED_OPPORTUNITY || 0;
    document.getElementById("mistake-tact-count").textContent = bd.TACTICAL_MISTAKE || 0;
    document.getElementById("mistake-res-count").textContent = bd.RESOURCE_MISTAKE || 0;

    const feed = document.getElementById("mistake-list-feed");
    if (data.recent_mistakes && data.recent_mistakes.length > 0) {
      feed.innerHTML = "";
      data.recent_mistakes.forEach(m => {
        const item = document.createElement("div");
        item.className = "event-feed-item";
        item.style.borderLeftColor = m.severity === "HIGH" ? "var(--rose)" : (m.severity === "MEDIUM" ? "var(--amber)" : "var(--primary)");
        item.innerHTML = `
          <div>
            <strong style="color: #fff; margin-right: 0.5rem;">[${m.category}]</strong>
            <span style="color: var(--text-muted);">${m.explanation}</span>
            <div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 0.2rem;">Chosen: ${m.chosen_action_desc} | Optimal: ${m.optimal_action_desc}</div>
          </div>
          <div style="font-family: var(--font-mono); font-size: 0.82rem; font-weight: 800; color: var(--rose);">
            ${m.score_delta > 0 ? '-' : ''}${m.score_delta}
          </div>
        `;
        feed.appendChild(item);
      });
    }
  } catch (err) {
    console.warn("Could not fetch mistakes:", err);
  }
}

/* --------------------------------------------------------------------------
   5. Meta Observatory & Robustness Rankings
   -------------------------------------------------------------------------- */
async function fetchMetaPredictions() {
  try {
    const res = await fetch("/api/meta-prediction");
    if (!res.ok) return;
    const rankings = await res.json();
    const tbody = document.getElementById("meta-rankings-body");
    tbody.innerHTML = "";

    rankings.forEach(d => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="header-col">
          <strong>${d.deck_name}</strong>
          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 0.2rem;">${d.rationale}</div>
        </td>
        <td style="font-weight: 800; color: ${d.expected_win_rate >= 60 ? 'var(--emerald)' : 'var(--text-main)'}; font-size: 1.05rem;">
          ${d.expected_win_rate.toFixed(1)}%
        </td>
        <td style="font-weight: 800; color: var(--primary); font-size: 1.05rem;">
          ${d.robustness_score.toFixed(1)}
        </td>
        <td style="font-family: var(--font-mono); font-size: 0.88rem;">${d.min_matchup_win_rate.toFixed(1)}%</td>
        <td style="font-family: var(--font-mono); font-size: 0.88rem;">${d.max_matchup_win_rate.toFixed(1)}%</td>
        <td style="font-size: 0.82rem; color: var(--text-muted); font-family: var(--font-mono);">
          [${d.confidence_interval_95[0].toFixed(1)}% - ${d.confidence_interval_95[1].toFixed(1)}%]
        </td>
        <td>
          <span class="brand-version" style="font-size: 0.75rem;">${d.recommended_tier}</span>
        </td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Could not fetch meta predictions:", err);
  }
}

/* --------------------------------------------------------------------------
   6. Live Battle Simulation Engine & Playback Controls
   -------------------------------------------------------------------------- */
function initBattleSimulator() {
  const btn = document.getElementById("btn-run-battle");
  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.innerHTML = `<span>Simulating Battle...</span>`;
    stopAutoPlay();

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
      setupArenaReplay(replay);
      fetchMistakes(); // Refresh mined mistakes feed
    } catch (err) {
      alert("Error executing battle simulation: " + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>Simulate Live Battle</span>`;
    }
  });
}

function setupArenaReplay(replay) {
  document.getElementById("arena-live-view").style.display = "block";

  // Configure Sliders
  const maxStep = Math.max(0, replay.timeline.length - 1);
  const arenaSlider = document.getElementById("arena-step-slider");
  const repSlider = document.getElementById("replay-slider");

  arenaSlider.max = maxStep;
  arenaSlider.value = 0;
  repSlider.max = maxStep;
  repSlider.value = 0;

  // Render Combat Event Feed
  const feed = document.getElementById("arena-event-feed");
  feed.innerHTML = "";
  (replay.event_log || []).forEach(evt => {
    const item = document.createElement("div");
    item.className = `event-feed-item ${evt.type}`;
    item.innerHTML = `
      <div>
        <strong style="color: #fff; margin-right: 0.5rem;">[${evt.badge}]</strong>
        <span style="color: var(--text-muted);">${evt.text}</span>
      </div>
      <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-dim);">Step ${evt.step}</div>
    `;
    item.addEventListener("click", () => renderStep(evt.step));
    feed.appendChild(item);
  });

  renderStep(0);
}

function initArenaControls() {
  const arenaSlider = document.getElementById("arena-step-slider");
  const repSlider = document.getElementById("replay-slider");

  arenaSlider.addEventListener("input", (e) => {
    stopAutoPlay();
    renderStep(parseInt(e.target.value, 10));
  });

  repSlider.addEventListener("input", (e) => {
    stopAutoPlay();
    renderStep(parseInt(e.target.value, 10));
  });

  document.getElementById("btn-arena-prev").addEventListener("click", () => {
    stopAutoPlay();
    if (currentStepIdx > 0) renderStep(currentStepIdx - 1);
  });

  document.getElementById("btn-arena-next").addEventListener("click", () => {
    stopAutoPlay();
    if (currentReplay && currentStepIdx < currentReplay.timeline.length - 1) {
      renderStep(currentStepIdx + 1);
    }
  });

  document.getElementById("btn-replay-prev-sub").addEventListener("click", () => {
    if (currentStepIdx > 0) renderStep(currentStepIdx - 1);
  });

  document.getElementById("btn-replay-next-sub").addEventListener("click", () => {
    if (currentReplay && currentStepIdx < currentReplay.timeline.length - 1) {
      renderStep(currentStepIdx + 1);
    }
  });

  document.getElementById("btn-play-pause").addEventListener("click", () => {
    if (isAutoPlaying) {
      stopAutoPlay();
    } else {
      startAutoPlay();
    }
  });
}

function startAutoPlay() {
  if (!currentReplay) return;
  isAutoPlaying = true;
  document.getElementById("play-pause-icon").textContent = "Pause Auto";
  const speed = parseInt(document.getElementById("arena-speed-select").value, 10) || 400;

  autoPlayTimer = setInterval(() => {
    if (currentStepIdx >= currentReplay.timeline.length - 1) {
      stopAutoPlay();
      return;
    }
    renderStep(currentStepIdx + 1);
  }, speed);
}

function stopAutoPlay() {
  isAutoPlaying = false;
  clearInterval(autoPlayTimer);
  const icon = document.getElementById("play-pause-icon");
  if (icon) icon.textContent = "Play Auto";
}

function renderStep(stepIdx) {
  if (!currentReplay || !currentReplay.timeline || !currentReplay.timeline[stepIdx]) {
    return;
  }
  currentStepIdx = stepIdx;
  const item = currentReplay.timeline[stepIdx];

  // Sync sliders
  document.getElementById("arena-step-slider").value = stepIdx;
  document.getElementById("replay-slider").value = stepIdx;

  const indicatorText = `Step ${item.step} / Turn ${item.turn}`;
  document.getElementById("arena-step-indicator").textContent = indicatorText;
  document.getElementById("replay-step-badge").textContent = indicatorText;

  // Render Player 0 Active & Bench
  const p0 = item.your_active;
  if (p0) {
    document.getElementById("p0-active-title").textContent = `Card #${p0.id} (${p0.id === 723 ? 'Bellibolt ex' : (p0.id === 722 ? 'Bellibolt' : 'Tadbulb')})`;
    document.getElementById("p0-active-stage").textContent = p0.id === 723 ? 'Stage 1 ex (Lightning)' : 'Basic';
    const p0Hp = p0.hp || 0;
    const p0MaxHp = p0.maxHp || (p0.id === 723 ? 350 : 150);
    document.getElementById("p0-hp-text").textContent = `${p0Hp} / ${p0MaxHp}`;

    const p0Pct = Math.max(0, Math.min(100, (p0Hp / p0MaxHp) * 100));
    const p0Bar = document.getElementById("p0-hp-bar");
    p0Bar.style.width = `${p0Pct}%`;
    p0Bar.className = `hp-bar-fill ${p0Pct < 25 ? 'critical' : (p0Pct < 55 ? 'mid' : '')}`;

    const p0Energies = p0.energies || [];
    const p0EnergyBox = document.getElementById("p0-energy-stack");
    p0EnergyBox.innerHTML = p0Energies.map(() => `<div class="energy-orb">L</div>`).join('') || '<span style="font-size: 0.75rem; color: var(--text-dim);">No energy</span>';
  }

  // Render Player 1 Active & Bench
  const p1 = item.opp_active;
  if (p1) {
    document.getElementById("p1-active-title").textContent = `Card #${p1.id}`;
    document.getElementById("p1-active-stage").textContent = 'Opponent Active';
    const p1Hp = p1.hp || 0;
    const p1MaxHp = p1.maxHp || 150;
    document.getElementById("p1-hp-text").textContent = `${p1Hp} / ${p1MaxHp}`;

    const p1Pct = Math.max(0, Math.min(100, (p1Hp / p1MaxHp) * 100));
    const p1Bar = document.getElementById("p1-hp-bar");
    p1Bar.style.width = `${p1Pct}%`;
    p1Bar.className = `hp-bar-fill ${p1Pct < 25 ? 'critical' : (p1Pct < 55 ? 'mid' : '')}`;

    const p1Energies = p1.energies || [];
    const p1EnergyBox = document.getElementById("p1-energy-stack");
    p1EnergyBox.innerHTML = p1Energies.map(() => `<div class="energy-orb" style="background:#ef4444; color:#fff;">E</div>`).join('') || '<span style="font-size: 0.75rem; color: var(--text-dim);">No energy</span>';
  }

  // Render Prize Docks
  renderPrizeDock("p0-prizes-dock", item.your_prizes);
  renderPrizeDock("p1-prizes-dock", item.opp_prizes);

  // Render Replay Tab Details
  document.getElementById("rep-active-desc").textContent = p0 ? `Card #${p0.id} (${p0.hp} HP)` : "Empty Active";
  document.getElementById("rep-opp-active-desc").textContent = p1 ? `Card #${p1.id} (${p1.hp} HP)` : "Empty Active";
  document.getElementById("rep-you-prizes").textContent = item.your_prizes;
  document.getElementById("rep-opp-prizes").textContent = item.opp_prizes;
  document.getElementById("rep-action-chosen").textContent = item.action ? `Action Selected: Option ${JSON.stringify(item.action)}` : "Turn in progress";

  // Render Decision Tree
  if (currentReplay.decisions && currentReplay.decisions[stepIdx]) {
    renderDecisionTree(currentReplay.decisions[stepIdx]);
  }
}

function renderPrizeDock(containerId, prizesLeft) {
  const container = document.getElementById(containerId);
  if (!container) return;
  let html = "";
  for (let i = 0; i < 6; i++) {
    const isTaken = i >= prizesLeft;
    html += `<div class="prize-orb ${isTaken ? 'taken' : ''}" title="${isTaken ? 'Prize Claimed' : 'Prize Available'}"></div>`;
  }
  container.innerHTML = html;
}

/* --------------------------------------------------------------------------
   7. Decision Explainability & Value Decomposition
   -------------------------------------------------------------------------- */
function renderDecisionTree(decision) {
  const container = document.getElementById("decision-tree-container");
  if (!container || !decision || !decision.options) return;

  container.innerHTML = "";
  const maxScore = Math.max(...decision.options.map(o => Math.abs(o.projected_value)), 1.0);

  decision.options.forEach((opt, idx) => {
    const node = document.createElement("div");
    const isChosen = opt.is_chosen;
    const isRunnerUp = idx === 1 && !isChosen;

    node.className = `decision-node-card ${isChosen ? 'chosen' : (isRunnerUp ? 'runner-up' : '')}`;
    const pct = Math.max(5, Math.min(100, (Math.abs(opt.projected_value) / maxScore) * 100));

    node.innerHTML = `
      <div>
        <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.35rem;">
          <span style="font-weight: 800; font-size: 1rem; color: ${isChosen ? 'var(--emerald)' : '#fff'};">
            ${isChosen ? '[CHOSEN]' : (isRunnerUp ? '[RUNNER-UP]' : '[REJECTED]')} Option ${opt.index}: ${opt.name}
          </span>
          <span class="brand-version" style="font-size: 0.7rem;">Type Code ${opt.type}</span>
        </div>
        <div style="font-size: 0.82rem; color: var(--text-muted);">
          Action Bonus: +${opt.action_bonus} | Evaluated Leaf Value: ${opt.projected_value}
        </div>
      </div>
      <div style="text-align: right;">
        <div style="font-weight: 800; font-size: 1.25rem; color: ${isChosen ? 'var(--emerald)' : (opt.projected_value > 0 ? 'var(--text-main)' : 'var(--rose)')};">
          ${opt.projected_value > 0 ? '+' : ''}${opt.projected_value}
        </div>
        <div class="tree-meter-wrap">
          <div class="tree-meter-fill" style="width: ${pct}%; background: ${isChosen ? 'var(--emerald)' : 'var(--primary)'};"></div>
        </div>
      </div>
    `;
    container.appendChild(node);
  });
}

/* --------------------------------------------------------------------------
   8. Ablation Studies Matrix
   -------------------------------------------------------------------------- */
async function fetchAblations() {
  try {
    const res = await fetch("/api/ablations");
    if (!res.ok) return;
    const ablations = await res.json();
    const tbody = document.getElementById("ablation-table-body");
    tbody.innerHTML = "";

    ablations.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td class="header-col">${item.variant}</td>
        <td style="color: var(--text-muted); font-size: 0.82rem; text-align: left;">
          <div>${item.description}</div>
          <div style="color: var(--emerald); font-size: 0.75rem; margin-top: 0.25rem;">+ ${item.advantage}</div>
        </td>
        <td style="font-weight: 800; color: var(--primary);">${item.elo.toFixed(1)}</td>
        <td style="font-weight: 800; color: ${item.win_rate >= 60 ? 'var(--emerald)' : 'var(--text-main)'};">${item.win_rate.toFixed(1)}%</td>
        <td style="font-family: var(--font-mono);">${item.latency_ms.toFixed(2)} ms</td>
        <td style="color: var(--emerald); font-weight: 700;">${item.fallback_rate.toFixed(2)}%</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.warn("Could not fetch ablations:", err);
  }
}

/* --------------------------------------------------------------------------
   9. Live Benchmark Runner
   -------------------------------------------------------------------------- */
function initBenchmarkRunner() {
  const btn = document.getElementById("btn-run-benchmark");
  btn.addEventListener("click", async () => {
    const numGames = parseInt(document.getElementById("benchmark-games-select").value, 10) || 10;
    btn.disabled = true;
    btn.innerHTML = `<span>Benchmarking ${numGames} Games...</span>`;

    try {
      const res = await fetch("/api/benchmark", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ games: numGames }),
      });

      if (!res.ok) throw new Error("Benchmark failed");
      const data = await res.json();

      document.getElementById("benchmark-metrics-grid").style.display = "grid";
      document.getElementById("bench-avg-lat").textContent = `${data.latency_avg_ms.toFixed(2)} ms`;
      document.getElementById("bench-p95-lat").textContent = `${data.latency_p95_ms.toFixed(2)} ms`;
      document.getElementById("bench-throughput").textContent = `${data.throughput_decisions_per_sec.toFixed(1)} /s`;
      document.getElementById("bench-memory").textContent = `${data.memory_end_mb.toFixed(1)} MB`;
    } catch (err) {
      alert("Error running benchmark: " + err.message);
    } finally {
      btn.disabled = false;
      btn.innerHTML = `<span>Run Benchmark</span>`;
    }
  });
}

/* --------------------------------------------------------------------------
   10. Card & Strategy Codex
   -------------------------------------------------------------------------- */
async function fetchCodex() {
  try {
    const res = await fetch("/api/codex");
    if (!res.ok) return;
    const cards = await res.json();
    const gallery = document.getElementById("codex-gallery");
    gallery.innerHTML = "";

    cards.forEach(card => {
      const wrap = document.createElement("div");
      wrap.className = "holo-card-wrap";
      wrap.innerHTML = `
        <div class="holo-card">
          <img src="${card.img}" alt="${card.name}" class="holo-card-art" loading="lazy">
          <div class="holo-card-content">
            <div class="holo-card-name">${card.name}</div>
            <div class="holo-card-meta">${card.category} (${card.element}) | ${card.copies} Copies</div>
            ${card.hp > 0 ? `<div style="font-weight: 700; font-size: 0.85rem;">HP: ${card.hp} | Atk Dmg: ${card.damage}</div>` : ''}
            <div class="holo-card-desc">${card.description}</div>
            <div class="holo-card-ai-note">AI Priority: ${card.ai_priority}</div>
          </div>
        </div>
      `;

      // 3D Parallax Tilt Effect on Mouse Move
      const cardEl = wrap.querySelector(".holo-card");
      wrap.addEventListener("mousemove", (e) => {
        const rect = wrap.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = ((y - centerY) / centerY) * -12;
        const rotateY = ((x - centerX) / centerX) * 12;

        cardEl.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
      });

      wrap.addEventListener("mouseleave", () => {
        cardEl.style.transform = `rotateX(0deg) rotateY(0deg) translateY(0)`;
      });

      gallery.appendChild(wrap);
    });
  } catch (err) {
    console.warn("Could not fetch card codex:", err);
  }
}
