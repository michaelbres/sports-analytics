/* ============================================================
   MLB — Data loading, table rendering, filtering
   ============================================================ */

const BATTING_COLS_STANDARD = [
  { key: "name",            label: "Player",   fmt: null },
  { key: "team",            label: "Team",     fmt: null },
  { key: "age",             label: "Age",      fmt: fmt.int },
  { key: "games",           label: "G",        fmt: fmt.int },
  { key: "plate_appearances", label: "PA",     fmt: fmt.int },
  { key: "home_runs",       label: "HR",       fmt: fmt.int },
  { key: "rbi",             label: "RBI",      fmt: fmt.int },
  { key: "runs",            label: "R",        fmt: fmt.int },
  { key: "stolen_bases",    label: "SB",       fmt: fmt.int },
  { key: "batting_avg",     label: "AVG",      fmt: fmt.dec3 },
  { key: "obp",             label: "OBP",      fmt: fmt.dec3 },
  { key: "slg",             label: "SLG",      fmt: fmt.dec3 },
  { key: "ops",             label: "OPS",      fmt: fmt.dec3 },
  { key: "wrc_plus",        label: "wRC+",     fmt: fmt.dec1 },
  { key: "war",             label: "WAR",      fmt: fmt.dec1 },
];

const BATTING_COLS_STATCAST = [
  { key: "name",            label: "Player",   fmt: null },
  { key: "team",            label: "Team",     fmt: null },
  { key: "plate_appearances", label: "PA",     fmt: fmt.int },
  { key: "exit_velocity",   label: "Avg EV",   fmt: fmt.dec1 },
  { key: "launch_angle",    label: "Avg LA",   fmt: fmt.dec1 },
  { key: "barrel_pct",      label: "Barrel%",  fmt: fmt.dec1 },
  { key: "hard_hit_pct",    label: "HardHit%", fmt: fmt.dec1 },
  { key: "xba",             label: "xBA",      fmt: fmt.dec3 },
  { key: "xslg",            label: "xSLG",     fmt: fmt.dec3 },
  { key: "xwoba",           label: "xwOBA",    fmt: fmt.dec3 },
  { key: "sprint_speed",    label: "Spd",      fmt: fmt.dec1 },
];

const PITCHING_COLS_STANDARD = [
  { key: "name",            label: "Pitcher",  fmt: null },
  { key: "team",            label: "Team",     fmt: null },
  { key: "age",             label: "Age",      fmt: fmt.int },
  { key: "games",           label: "G",        fmt: fmt.int },
  { key: "games_started",   label: "GS",       fmt: fmt.int },
  { key: "innings_pitched", label: "IP",       fmt: fmt.dec1 },
  { key: "wins",            label: "W",        fmt: fmt.int },
  { key: "losses",          label: "L",        fmt: fmt.int },
  { key: "strikeouts",      label: "K",        fmt: fmt.int },
  { key: "era",             label: "ERA",      fmt: fmt.dec2 },
  { key: "whip",            label: "WHIP",     fmt: fmt.dec2 },
  { key: "k_per_9",         label: "K/9",      fmt: fmt.dec1 },
  { key: "bb_per_9",        label: "BB/9",     fmt: fmt.dec1 },
  { key: "k_bb",            label: "K/BB",     fmt: fmt.dec2 },
  { key: "fip",             label: "FIP",      fmt: fmt.dec2 },
  { key: "war",             label: "WAR",      fmt: fmt.dec1 },
];

const PITCHING_COLS_STATCAST = [
  { key: "name",                  label: "Pitcher",    fmt: null },
  { key: "team",                  label: "Team",       fmt: null },
  { key: "innings_pitched",       label: "IP",         fmt: fmt.dec1 },
  { key: "era",                   label: "ERA",        fmt: fmt.dec2 },
  { key: "xera",                  label: "xERA",       fmt: fmt.dec2 },
  { key: "xfip",                  label: "xFIP",       fmt: fmt.dec2 },
  { key: "barrel_pct_against",    label: "Barrel%",    fmt: fmt.dec1 },
  { key: "hard_hit_pct_against",  label: "HardHit%",   fmt: fmt.dec1 },
  { key: "avg_velocity",          label: "Velo",       fmt: fmt.dec1 },
];

const TEAMS_COLS = [
  { key: "name",         label: "Team",      fmt: null },
  { key: "league",       label: "League",    fmt: null },
  { key: "division",     label: "Division",  fmt: null },
];

// ── State ────────────────────────────────────────────────
let allBatting = [], allPitching = [], allTeams = [];
let season = 2025;

// ── Boot ─────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  season = parseInt(document.getElementById("season-select").value);
  loadAll();

  document.getElementById("season-select").addEventListener("change", (e) => {
    season = parseInt(e.target.value);
    loadAll();
  });

  // Main tabs
  document.querySelectorAll("#main-tabs .tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll("#main-tabs .tab").forEach((b) => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach((c) => c.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById(btn.dataset.tab + "-tab").classList.add("active");
    });
  });

  // Search
  document.getElementById("batting-search").addEventListener("input", renderBatting);
  document.getElementById("pitching-search").addEventListener("input", renderPitching);
  document.getElementById("teams-search").addEventListener("input", renderTeams);

  // Filters
  document.getElementById("min-pa").addEventListener("change", renderBatting);
  document.getElementById("min-ip").addEventListener("change", renderPitching);
  document.getElementById("batting-view").addEventListener("change", renderBatting);
  document.getElementById("pitching-view").addEventListener("change", renderPitching);
  document.getElementById("league-filter").addEventListener("change", renderTeams);
});

async function loadAll() {
  setLoading(true);
  try {
    const [batting, pitching, teams] = await Promise.all([
      API.get("/mlb/batting", { season, min_pa: 0 }),
      API.get("/mlb/pitching", { season, min_ip: 0 }),
      API.get("/mlb/teams", { season }),
    ]);
    allBatting  = batting;
    allPitching = pitching;
    allTeams    = teams;
    setLoading(false);
    renderBatting();
    renderPitching();
    renderTeams();
  } catch (e) {
    document.getElementById("loading").textContent = "No data yet. Run the MLB pipeline to load data.";
  }
}

// ── Batting ──────────────────────────────────────────────
function renderBatting() {
  const query  = document.getElementById("batting-search").value;
  const minPA  = parseInt(document.getElementById("min-pa").value) || 0;
  const view   = document.getElementById("batting-view").value;
  const cols   = view === "statcast" ? BATTING_COLS_STATCAST : BATTING_COLS_STANDARD;

  let rows = allBatting.filter((r) => (r.plate_appearances || 0) >= minPA);
  if (query) rows = filterRows(rows, query, ["name", "team"]);

  document.getElementById("batting-count").textContent = `${rows.length} players`;
  buildTable(document.getElementById("batting-table"), cols, rows);
}

// ── Pitching ─────────────────────────────────────────────
function renderPitching() {
  const query = document.getElementById("pitching-search").value;
  const minIP = parseFloat(document.getElementById("min-ip").value) || 0;
  const view  = document.getElementById("pitching-view").value;
  const cols  = view === "statcast" ? PITCHING_COLS_STATCAST : PITCHING_COLS_STANDARD;

  let rows = allPitching.filter((r) => (r.innings_pitched || 0) >= minIP);
  if (query) rows = filterRows(rows, query, ["name", "team"]);

  document.getElementById("pitching-count").textContent = `${rows.length} pitchers`;
  buildTable(document.getElementById("pitching-table"), cols, rows);
}

// ── Teams ────────────────────────────────────────────────
function renderTeams() {
  const query  = document.getElementById("teams-search").value;
  const league = document.getElementById("league-filter").value;

  let rows = [...allTeams];
  if (league) rows = rows.filter((r) => r.league === league);
  if (query)  rows = filterRows(rows, query, ["name", "division"]);

  rows.sort((a, b) => (a.name || "").localeCompare(b.name || ""));
  document.getElementById("teams-count").textContent = `${rows.length} teams`;
  buildTable(document.getElementById("teams-table"), TEAMS_COLS, rows);
}
