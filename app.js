'use strict';

// ============================================================
// CONFIGURATION
// ============================================================

// Year → filename mapping (years inferred from recognizable players)
const YEAR_FILES = {
  2025: 'receiving_2025.csv',
  2024: 'receiving_2024.csv',
  2023: 'receiving_2023.csv',
  2022: 'receiving_2022.csv',
  2021: 'receiving_2021.csv',
  2020: 'receiving_2020.csv',
  2019: 'receiving_2019.csv',
};

// Columns shown in the leaderboard table
const COLUMNS = [
  { key: 'player',                          label: 'Player',    type: 'str',  colorize: false },
  { key: 'team_name',                       label: 'Team',      type: 'str',  colorize: false },
  { key: 'player_game_count',               label: 'G',         type: 'int',  colorize: false },
  { key: 'targets',                         label: 'Tgt',       type: 'int',  colorize: true,  hb: true  },
  { key: 'receptions',                      label: 'Rec',       type: 'int',  colorize: true,  hb: true  },
  { key: 'yards',                           label: 'Yds',       type: 'int',  colorize: true,  hb: true  },
  { key: 'touchdowns',                      label: 'TD',        type: 'int',  colorize: true,  hb: true  },
  { key: 'first_downs',                     label: '1D',        type: 'int',  colorize: true,  hb: true  },
  { key: 'first_downs_per_route',           label: '1D/Rte',    type: 'dec3', colorize: true,  hb: true  },
  { key: 'caught_percent',                  label: 'Ctch%',     type: 'dec1', colorize: true,  hb: true  },
  { key: 'avg_depth_of_target',             label: 'aDOT',      type: 'dec1', colorize: false              },
  { key: 'drop_rate',                       label: 'Drop%',     type: 'dec1', colorize: true,  hb: false },
  { key: 'yards_per_reception',             label: 'YPR',       type: 'dec1', colorize: true,  hb: true  },
  { key: 'yards_after_catch_per_reception', label: 'YAC/R',     type: 'dec1', colorize: true,  hb: true  },
  { key: 'yprr',                            label: 'YPRR',      type: 'dec2', colorize: true,  hb: true  },
  { key: 'grades_offense',                  label: 'Off Grd',   type: 'dec1', colorize: true,  hb: true  },
  { key: 'grades_pass_route',               label: 'Rte Grd',   type: 'dec1', colorize: true,  hb: true  },
  { key: 'grades_hands_drop',               label: 'Hnd Grd',   type: 'dec1', colorize: true,  hb: true  },
  { key: 'contested_catch_rate',            label: 'CC%',       type: 'dec1', colorize: true,  hb: true  },
  { key: 'avoided_tackles',                 label: 'Avd Tkl',   type: 'int',  colorize: true,  hb: true  },
  { key: 'avoided_tackles_per_reception',   label: 'AvdTkl/R',  type: 'dec2', colorize: true,  hb: true  },
  { key: 'targeted_qb_rating',              label: 'Tgt QBR',   type: 'dec1', colorize: true,  hb: true  },
  { key: 'slot_rate',                       label: 'Slot%',     type: 'dec1', colorize: false              },
  { key: 'wide_rate',                       label: 'Wide%',     type: 'dec1', colorize: false              },
  // Man coverage splits
  { key: 'man_targets',                     label: 'Man Tgt',   type: 'int',  colorize: false              },
  { key: 'man_caught_percent',              label: 'Man Ctch%', type: 'dec1', colorize: true,  hb: true  },
  { key: 'man_yards_per_reception',         label: 'Man YPR',   type: 'dec1', colorize: true,  hb: true  },
  { key: 'man_yprr',                        label: 'Man YPRR',  type: 'dec2', colorize: true,  hb: true  },
  { key: 'man_grades_pass_route',           label: 'Man RteGrd',type: 'dec1', colorize: true,  hb: true  },
  // Zone coverage splits
  { key: 'zone_targets',                    label: 'Zn Tgt',    type: 'int',  colorize: false              },
  { key: 'zone_caught_percent',             label: 'Zn Ctch%',  type: 'dec1', colorize: true,  hb: true  },
  { key: 'zone_yards_per_reception',        label: 'Zn YPR',    type: 'dec1', colorize: true,  hb: true  },
  { key: 'zone_yprr',                       label: 'Zn YPRR',   type: 'dec2', colorize: true,  hb: true  },
  { key: 'zone_grades_pass_route',          label: 'Zn RteGrd', type: 'dec1', colorize: true,  hb: true  },
];

// Axes available in the scatter plot
const SCATTER_AXES = [
  { key: 'yprr',                            label: 'YPRR (Yards Per Route Run)'       },
  { key: 'grades_offense',                  label: 'Offense Grade'                    },
  { key: 'grades_pass_route',               label: 'Route Running Grade'              },
  { key: 'grades_hands_drop',               label: 'Hands / Drop Grade'               },
  { key: 'caught_percent',                  label: 'Catch Rate %'                     },
  { key: 'drop_rate',                       label: 'Drop Rate %'                      },
  { key: 'yards',                           label: 'Receiving Yards'                  },
  { key: 'yards_per_reception',             label: 'Yards Per Reception'              },
  { key: 'yards_after_catch_per_reception', label: 'YAC Per Reception'                },
  { key: 'avg_depth_of_target',             label: 'Avg Depth of Target (aDOT)'       },
  { key: 'targets',                         label: 'Targets'                          },
  { key: 'receptions',                      label: 'Receptions'                       },
  { key: 'touchdowns',                      label: 'Touchdowns'                       },
  { key: 'first_downs',                     label: 'First Downs'                      },
  { key: 'avoided_tackles',                 label: 'Avoided Tackles'                  },
  { key: 'avoided_tackles_per_reception',   label: 'Avoided Tackles Per Reception'    },
  { key: 'first_downs_per_route',           label: 'First Downs Per Route'            },
  { key: 'contested_catch_rate',            label: 'Contested Catch Rate %'           },
  { key: 'targeted_qb_rating',              label: 'Passer Rating When Targeted'      },
  { key: 'slot_rate',                       label: 'Slot Alignment Rate %'            },
  { key: 'wide_rate',                       label: 'Wide Alignment Rate %'            },
  { key: 'man_yprr',                        label: 'Man Coverage YPRR'                },
  { key: 'man_caught_percent',              label: 'Man Coverage Catch %'             },
  { key: 'man_yards_per_reception',         label: 'Man Coverage Yards/Rec'           },
  { key: 'man_grades_pass_route',           label: 'Man Coverage Route Grade'         },
  { key: 'zone_yprr',                       label: 'Zone Coverage YPRR'               },
  { key: 'zone_caught_percent',             label: 'Zone Coverage Catch %'            },
  { key: 'zone_yards_per_reception',        label: 'Zone Coverage Yards/Rec'          },
  { key: 'zone_grades_pass_route',          label: 'Zone Coverage Route Grade'        },
];

// Stats shown in the player modal as percentile bars
const PROFILE_STATS = [
  { key: 'grades_offense',                  label: 'Offense Grade',           hb: true  },
  { key: 'grades_pass_route',               label: 'Route Running Grade',     hb: true  },
  { key: 'grades_hands_drop',               label: 'Hands Grade',             hb: true  },
  { key: 'yprr',                            label: 'YPRR',                    hb: true  },
  { key: 'caught_percent',                  label: 'Catch Rate',              hb: true  },
  { key: 'drop_rate',                       label: 'Drop Rate',               hb: false },
  { key: 'yards_per_reception',             label: 'Yards / Reception',       hb: true  },
  { key: 'yards_after_catch_per_reception', label: 'YAC / Reception',         hb: true  },
  { key: 'avg_depth_of_target',             label: 'Avg Depth of Target',     hb: null  },
  { key: 'contested_catch_rate',            label: 'Contested Catch Rate',    hb: true  },
  { key: 'targeted_qb_rating',              label: 'Passer Rating (targeted)',hb: true  },
  { key: 'first_downs_per_route',           label: '1st Downs / Route',       hb: true  },
  { key: 'avoided_tackles_per_reception',   label: 'Avoided Tackles / Rec',   hb: true  },
];

// 2025 draft-declared players (from PFF declared filter)
const DECLARED_2025 = new Set([
  'eli heidenreich','cade harris','carnell tate','skyler bell','makai lemon',
  'tray taylor','malik benson','demarcus lacey','cameron dorner','junior vandeross iii',
  'eric mcalister','omar cooper jr.','brenen thompson','elijah sarratt','hank beatty',
  'jaden bradley','chris brazzell ii','mudia reuben','zachariah branch','eli stowers',
  'chris bell','gabriel benyard','anthony smith','ryan davis','cyrus allen',
  'damon bankston','malik rutherford','chase roberts','kc concepcion','cortez braham jr.',
  'aaron anderson','ja\'kobi lane','ted hurst','izayah cummings','joseph manjack iv',
  'devin voisin','troy omeire','jordyn tyson','kobe prentice','kris hutson',
  'kevin coleman jr.','jeff caldwell','tailique williams','camden brown','emmanuel henderson jr.',
  'jordan hudson','antonio williams','denzel boston','eli raridon','tanner koziol',
  'sean brown','dae\'quan wright','malachi fields','elijah metcalf','michael trigg',
  'keagan johnson','noah short','harrison wallace iii','bryce bohanon','brock spalding',
  'lewis bond','daedae reynolds','ben ford','keelan marion','caleb douglas',
  'will pauling','joshua meredith','matthew henry','jacob de jesus','rara thomas',
  'aaron turner','de\'zhaun stribling','eric rivers','devonte ross','justus ross-simmons',
  'boden groen','carsen ryan','cj daniels','lance mason','kenyon sadiq',
  'dallen bentley','raylen sharpe','cj williams','javin whatley','o\'mega blake',
  'kendrick law','cam ross','jeremiyah love','justin joly','jonah coleman',
  'kyre duplessis','jyrin johnson','jeff weimer','christian moss','trebor pena',
  'jaren kanak','dalen cobb','germie bernard','brandon hawkins jr.','shaleak knotts',
  'max klare','kole wilson','marcus sanders jr.','barion brown','josh cameron',
  'corey rucker','dontae mcmillan','trayvon rudolph','donaven mcculley','nick devereaux',
  'josiah freeman','jaylan sanchez','romello brinson','rj maryland','terry lockett jr.',
  'wesley grimes','tristan smith','e.j. williams jr.','zavion thomas','jake thaw',
  'le\'meke brockington','landon sims','omari kelly','joe royer','jamarien wheeler',
  'dalton stroman','chase penry','micah davis','vinny anthony ii','carl chester',
  'lake mcree','trond grizzell','marlin klein','nick degennaro','michael jackson iii',
  'myles butler','jeremiah franklin','caullin lacy','latrell caples','reggie virgil',
  'raphael williams jr.','miles kitselman','e. jai mason','cameron wright','devin gandy',
  'jalil farooq','deion burks','jamal haynes','dash luke','brady boyd',
  'dj rogers','kajiya hollawayne','kobe paysour','bryce farrell','sam roush',
  'tre williams iii','reymello murphy','dt sheffield','jacob gill','dakota thomas',
  'chamon metayer','jahmal edrine','ashtyn hawkins','dane key','j. michael sturdivant',
  'greg desrosiers jr.','peyton higgins','brock rechsteiner','andrel anthony','robert williams',
  'josh cuevas','emmett johnson','ethan conner','kenny fletcher jr.','lincoln pare',
  'tay lanier','marcus bellon','sahmir hagans','bralon brown','jordan brown',
  'dean connors','donavon greene','jack velling','levi wentz','matthew hibner',
  'bauer sharp','john michael gyllenborg','james blackstrain','keontez lewis','ej horton jr.',
  'seydou traore','terrill davis','octavian smith jr.','michael fitzgerald','dan villari',
  'pearson baldwin','titus mokiao-atimalala','matt lauter','malick meiga','pj johnson iii',
]);

// ============================================================
// STATE
// ============================================================

let currentYear        = 2025;
let allData            = [];
let filteredData       = [];
let sortKey            = 'yards';
let sortAsc            = false;
let activeTab          = 'leaderboard';
let scatterChart       = null;
let pctCache           = {};

// ============================================================
// UTILITIES
// ============================================================

function pf(val) {
  const n = parseFloat(val);
  return isNaN(n) ? null : n;
}

function fmt(val, type) {
  const n = pf(val);
  if (n === null || val === '' || val === undefined) return '-';
  switch (type) {
    case 'int':  return Math.round(n).toLocaleString();
    case 'dec1': return n.toFixed(1);
    case 'dec2': return n.toFixed(2);
    case 'dec3': return n.toFixed(3);
    case 'pct1': return n.toFixed(1) + '%';
    default:     return String(val);
  }
}

function getTypeForKey(key) {
  const col = COLUMNS.find(c => c.key === key);
  return col ? col.type : 'dec1';
}

function computePercentile(value, sortedArr) {
  if (value === null || !sortedArr || !sortedArr.length) return null;
  let lo = 0, hi = sortedArr.length;
  while (lo < hi) {
    const mid = (lo + hi) >> 1;
    if (sortedArr[mid] <= value) lo = mid + 1; else hi = mid;
  }
  return (lo / sortedArr.length) * 100;
}

function pctColor(pct) {
  if (pct === null) return '#555';
  if (pct >= 90) return '#00c896';
  if (pct >= 75) return '#4fc3f7';
  if (pct >= 55) return '#c5cae9';
  if (pct >= 35) return '#ffb74d';
  if (pct >= 15) return '#ff7043';
  return '#f44336';
}

function cellBg(pct, higherBetter) {
  if (pct === null || higherBetter === null) return '';
  const p = higherBetter ? pct : 100 - pct;
  if (p >= 90) return 'rgba(0, 200, 150, 0.80)';
  if (p >= 75) return 'rgba(0, 200, 150, 0.45)';
  if (p >= 55) return 'rgba(0, 200, 150, 0.15)';
  if (p >= 45) return '';
  if (p >= 25) return 'rgba(255, 100, 80, 0.15)';
  if (p >= 10) return 'rgba(255, 100, 80, 0.45)';
  return 'rgba(255, 100, 80, 0.75)';
}

function buildPctCache(data) {
  pctCache = {};
  const allKeys = new Set([
    ...COLUMNS.filter(c => c.colorize).map(c => c.key),
    ...PROFILE_STATS.map(s => s.key),
  ]);
  allKeys.forEach(key => {
    const vals = data.map(r => pf(r[key])).filter(v => v !== null);
    vals.sort((a, b) => a - b);
    pctCache[key] = vals;
  });
}

// ============================================================
// INIT
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  buildYearButtons();
  buildScatterAxes();
  setupListeners();
  loadYear(currentYear);
});

// ============================================================
// YEAR BUTTONS
// ============================================================

function buildYearButtons() {
  const container = document.getElementById('year-selector');
  const years = Object.keys(YEAR_FILES).map(Number).sort((a, b) => b - a);
  years.forEach(yr => {
    const btn = document.createElement('button');
    btn.className = 'year-btn' + (yr === currentYear ? ' active' : '');
    btn.textContent = yr;
    btn.title = `${yr} Season`;
    btn.addEventListener('click', () => {
      document.querySelectorAll('.year-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      loadYear(yr);
    });
    container.appendChild(btn);
  });
}

// ============================================================
// DATA LOADING
// ============================================================

const VALID_POSITIONS = new Set(['WR', 'TE', 'HB']);

async function parseCSV(filename) {
  const res = await fetch(filename);
  if (!res.ok) throw new Error(`HTTP ${res.status} — could not fetch "${filename}"`);
  const text = await res.text();
  const parsed = Papa.parse(text, {
    header: true,
    skipEmptyLines: true,
    transformHeader: h => h.trim(),
    transform: v => v.trim(),
  });
  const data = parsed.data.filter(r => VALID_POSITIONS.has((r.position || '').toUpperCase()));
  computeDerivedStats(data);
  return data;
}

async function loadYear(year) {
  currentYear = year;

  document.getElementById('loading').style.display = 'flex';
  document.getElementById('content').style.display = 'none';

  try {
    allData = await parseCSV(YEAR_FILES[year]);

    // Show/hide the declared toggle (only relevant for 2025)
    document.getElementById('declared-filter-wrap').style.display =
      year === 2025 ? '' : 'none';
    if (year !== 2025) {
      document.getElementById('declared-only').checked = false;
    }

    populatePositionFilter();
    applyFilters();

    document.getElementById('loading').style.display = 'none';
    document.getElementById('content').style.display = 'block';
  } catch (err) {
    document.getElementById('loading').textContent =
      `Error: ${err.message}. Make sure you are running a local server (e.g. python -m http.server 8000).`;
  }
}

// ============================================================
// DERIVED STATS
// ============================================================

function computeDerivedStats(data) {
  data.forEach(row => {
    const routes   = pf(row.routes);
    const rec      = pf(row.receptions);
    const fd       = pf(row.first_downs);
    const avdTkl   = pf(row.avoided_tackles);

    row.first_downs_per_route         = (routes && fd     !== null) ? fd     / routes : null;
    row.avoided_tackles_per_reception = (rec    && avdTkl !== null) ? avdTkl / rec   : null;
  });
}

// ============================================================
// FILTERING & SORTING
// ============================================================

function applyFilters() {
  const search        = document.getElementById('search').value.trim().toLowerCase();
  const minGames      = parseInt(document.getElementById('min-games').value, 10);
  const minTargets    = parseInt(document.getElementById('min-targets').value, 10);
  const position      = document.getElementById('position-filter').value;
  const declaredOnly  = document.getElementById('declared-only').checked && currentYear === 2025;

  filteredData = allData.filter(row => {
    if ((parseInt(row.player_game_count, 10) || 0) < minGames) return false;
    if ((parseInt(row.targets, 10) || 0) < minTargets) return false;
    if (position && (row.position || '').toUpperCase() !== position) return false;
    if (declaredOnly && !DECLARED_2025.has((row.player || '').trim().toLowerCase())) return false;
    if (search) {
      const name = (row.player || '').toLowerCase();
      const team = (row.team_name || '').toLowerCase();
      if (!name.includes(search) && !team.includes(search)) return false;
    }
    return true;
  });

  sortData();
}

function populatePositionFilter() {
  const sel = document.getElementById('position-filter');
  const current = sel.value;
  // keep "All" option, remove the rest
  while (sel.options.length > 1) sel.remove(1);

  const positions = [...new Set(
    allData.map(r => (r.position || '').toUpperCase()).filter(Boolean)
  )].sort();

  positions.forEach(pos => {
    const opt = document.createElement('option');
    opt.value = pos;
    opt.textContent = pos;
    sel.appendChild(opt);
  });

  // restore selection if it still exists
  if ([...sel.options].some(o => o.value === current)) sel.value = current;
}

function sortData() {
  filteredData.sort((a, b) => {
    const av = pf(a[sortKey]);
    const bv = pf(b[sortKey]);
    if (av === null && bv === null) return 0;
    if (av === null) return 1;
    if (bv === null) return -1;
    return sortAsc ? av - bv : bv - av;
  });

  buildPctCache(filteredData);

  document.getElementById('player-count').textContent =
    `${filteredData.length} players`;

  renderTable();

  if (activeTab === 'scatter') renderScatter();
}

// ============================================================
// TABLE RENDERING
// ============================================================

function renderTable() {
  const thead = document.querySelector('#stats-table thead');
  const tbody = document.querySelector('#stats-table tbody');

  // ── Header ──
  thead.innerHTML = '<tr>' + COLUMNS.map(col => {
    const isSort = col.key === sortKey;
    const arrow  = isSort ? (sortAsc ? ' &#9650;' : ' &#9660;') : '';
    const cls    = ['th-cell', isSort ? 'sort-active' : ''].filter(Boolean).join(' ');
    return `<th class="${cls}" data-key="${col.key}">${col.label}${arrow}</th>`;
  }).join('') + '</tr>';

  // ── Body ──
  tbody.innerHTML = filteredData.map((row, idx) => {
    const cells = COLUMNS.map(col => {
      if (col.type === 'str') {
        if (col.key === 'player') {
          return `<td class="player-cell" data-idx="${idx}">${row.player || '-'}</td>`;
        }
        return `<td>${row[col.key] || '-'}</td>`;
      }

      const val   = pf(row[col.key]);
      const disp  = fmt(row[col.key], col.type);
      let style   = '';

      if (col.colorize && val !== null) {
        const sortedArr = pctCache[col.key];
        const p   = computePercentile(val, sortedArr);
        const bg  = cellBg(p, col.hb);
        if (bg) style = `background-color:${bg};`;
      }

      return `<td style="${style}">${disp}</td>`;
    }).join('');

    return `<tr>${cells}</tr>`;
  }).join('');

  // ── Header sort listeners ──
  thead.querySelectorAll('th[data-key]').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.key;
      const col = COLUMNS.find(c => c.key === key);
      if (!col || col.type === 'str') return;
      sortKey = key;
      sortAsc = (key === sortKey && !sortAsc) ? true : false;
      // Re-check: if same key, toggle; otherwise default desc
      if (th.classList.contains('sort-active')) {
        sortAsc = !sortAsc;
      } else {
        sortAsc = false;
      }
      sortData();
    });
  });

  // ── Player click → modal ──
  tbody.querySelectorAll('.player-cell').forEach(td => {
    td.addEventListener('click', () => {
      showPlayerModal(filteredData[parseInt(td.dataset.idx, 10)]);
    });
  });
}

// ============================================================
// SCATTER PLOT
// ============================================================

function buildScatterAxes() {
  ['x-axis', 'y-axis'].forEach((id, i) => {
    const sel = document.getElementById(id);
    SCATTER_AXES.forEach(stat => {
      const opt = document.createElement('option');
      opt.value = stat.key;
      opt.textContent = stat.label;
      sel.appendChild(opt);
    });
    sel.value = i === 0 ? 'yprr' : 'grades_offense';
  });
}

function getScatterData() {
  const minGames = parseInt(document.getElementById('scatter-min-games').value, 10);
  return allData.filter(row =>
    (parseInt(row.player_game_count, 10) || 0) >= minGames
  );
}

function renderScatter() {
  const xKey  = document.getElementById('x-axis').value;
  const yKey  = document.getElementById('y-axis').value;
  const xMeta = SCATTER_AXES.find(s => s.key === xKey);
  const yMeta = SCATTER_AXES.find(s => s.key === yKey);

  const source = getScatterData();

  const points = source
    .filter(row => pf(row[xKey]) !== null && pf(row[yKey]) !== null)
    .map(row => ({
      x:      pf(row[xKey]),
      y:      pf(row[yKey]),
      player: row.player,
      team:   row.team_name,
      grade:  pf(row.grades_offense) || 0,
    }));

  const colors = points.map(p => {
    if (p.grade >= 85) return 'rgba(0, 200, 150, 0.88)';
    if (p.grade >= 75) return 'rgba(100, 200, 100, 0.88)';
    if (p.grade >= 65) return 'rgba(255, 200, 50,  0.88)';
    if (p.grade >= 55) return 'rgba(255, 150, 50,  0.88)';
    return 'rgba(255, 100, 100, 0.88)';
  });

  const ctx = document.getElementById('scatter-chart').getContext('2d');
  if (scatterChart) scatterChart.destroy();

  scatterChart = new Chart(ctx, {
    type: 'scatter',
    data: {
      datasets: [{
        data: points,
        backgroundColor: colors,
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1,
        pointRadius: 6,
        pointHoverRadius: 9,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => {
              const d = ctx.raw;
              const xFmt = fmt(d.x, getTypeForKey(xKey));
              const yFmt = fmt(d.y, getTypeForKey(yKey));
              return [
                `${d.player}  (${d.team})`,
                `${xMeta.label}: ${xFmt}`,
                `${yMeta.label}: ${yFmt}`,
                `Off Grade: ${d.grade || '-'}`,
              ];
            },
          },
          backgroundColor: 'rgba(13, 17, 23, 0.96)',
          bodyColor: '#e6edf3',
          borderColor: '#30363d',
          borderWidth: 1,
          bodyFont: { size: 13, family: 'Inter, sans-serif' },
          padding: 13,
          cornerRadius: 8,
          displayColors: false,
        },
      },
      scales: {
        x: {
          title: { display: true, text: xMeta.label, color: '#8b949e', font: { size: 12 } },
          grid:  { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8b949e' },
        },
        y: {
          title: { display: true, text: yMeta.label, color: '#8b949e', font: { size: 12 } },
          grid:  { color: 'rgba(255,255,255,0.06)' },
          ticks: { color: '#8b949e' },
        },
      },
    },
  });
}

// ============================================================
// PLAYER MODAL
// ============================================================

function showPlayerModal(row) {
  const modal = document.getElementById('player-modal');
  const body  = document.getElementById('modal-body');

  // Key summary stats
  const summaryStats = [
    { label: 'Rec',    val: row.receptions },
    { label: 'Tgt',    val: row.targets },
    { label: 'Yds',    val: row.yards },
    { label: 'TD',     val: row.touchdowns },
    { label: 'YPRR',   val: pf(row.yprr)?.toFixed(2) },
    { label: 'Ctch%',  val: pf(row.caught_percent)?.toFixed(1) + '%' },
    { label: 'Drop%',  val: pf(row.drop_rate)?.toFixed(1) + '%' },
  ];

  const keyStatsHtml = summaryStats.map(s =>
    `<div class="key-stat">
      <div class="key-stat-val">${s.val ?? '-'}</div>
      <div class="key-stat-label">${s.label}</div>
    </div>`
  ).join('');

  // Percentile bars
  const barsHtml = PROFILE_STATS.map(stat => {
    const val       = pf(row[stat.key]);
    const rawPct    = computePercentile(val, pctCache[stat.key]);
    // For "lower is better" stats, flip the display percentile so 100 = best
    const displayPct = rawPct === null
      ? null
      : (stat.hb === false ? 100 - rawPct : rawPct);
    const color = pctColor(displayPct);
    const pctNum = displayPct !== null ? Math.round(displayPct) : null;
    const barW   = pctNum ?? 0;
    const dispVal = fmt(row[stat.key], getTypeForKey(stat.key));

    return `
      <div class="profile-stat-row">
        <div class="profile-stat-label">${stat.label}</div>
        <div class="pct-bar-wrap">
          <div class="pct-bar-bg">
            <div class="pct-bar-fill" style="width:${barW}%; background:${color};"></div>
          </div>
          ${pctNum !== null ? `<div class="pct-dot" style="left:${barW}%; border-color:${color};"></div>` : ''}
        </div>
        <div class="pct-number" style="color:${color};">${pctNum ?? '-'}</div>
        <div class="pct-value">${dispVal}</div>
      </div>`;
  }).join('');

  // Alignment breakdown
  const slotPct  = pf(row.slot_rate)?.toFixed(0);
  const widePct  = pf(row.wide_rate)?.toFixed(0);
  const inlinePct = pf(row.inline_rate)?.toFixed(0);
  const alignHtml = `
    <div class="alignment-badges">
      <span class="modal-section-title" style="margin:0; line-height:2;">Alignment:</span>
      ${widePct   ? `<div class="badge">Wide<span>${widePct}%</span></div>`   : ''}
      ${slotPct   ? `<div class="badge">Slot<span>${slotPct}%</span></div>`   : ''}
      ${inlinePct ? `<div class="badge">Inline<span>${inlinePct}%</span></div>` : ''}
      <div class="badge">aDOT<span>${fmt(row.avg_depth_of_target, 'dec1')}</span></div>
    </div>`;

  body.innerHTML = `
    <div class="modal-player-name">${row.player || '—'}</div>
    <div class="modal-player-meta">
      ${row.team_name || ''} &bull; ${row.position || 'WR'} &bull; ${currentYear} Season &bull; ${row.player_game_count || '?'} games
    </div>
    <div class="modal-key-stats">${keyStatsHtml}</div>
    <div class="modal-section-title">Percentile Rankings (vs. current filtered players)</div>
    <div class="profile-stats">${barsHtml}</div>
    ${alignHtml}
  `;

  modal.classList.add('active');
}

// ============================================================
// EVENT LISTENERS
// ============================================================

function setupListeners() {
  document.getElementById('search').addEventListener('input', applyFilters);
  document.getElementById('min-games').addEventListener('change', applyFilters);
  document.getElementById('min-targets').addEventListener('change', applyFilters);
  document.getElementById('position-filter').addEventListener('change', applyFilters);
  document.getElementById('declared-only').addEventListener('change', applyFilters);

  document.getElementById('x-axis').addEventListener('change', renderScatter);
  document.getElementById('y-axis').addEventListener('change', renderScatter);
  document.getElementById('scatter-min-games').addEventListener('change', renderScatter);

  document.getElementById('tabs').addEventListener('click', e => {
    const btn = e.target.closest('.tab');
    if (!btn) return;
    activeTab = btn.dataset.tab;
    document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById(`${activeTab}-tab`).classList.add('active');
    if (activeTab === 'scatter') renderScatter();
  });

  const modal = document.getElementById('player-modal');
  document.querySelector('.modal-close').addEventListener('click', () =>
    modal.classList.remove('active')
  );
  modal.addEventListener('click', e => {
    if (e.target === modal) modal.classList.remove('active');
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') modal.classList.remove('active');
  });
}
