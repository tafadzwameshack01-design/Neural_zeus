"""
╔══════════════════════════════════════════════════════════════════════╗
║     ZEUS ⚡ NEURAL FOOTBALL INTELLIGENCE SYSTEM v3.0                 ║
║  Multi-Line: OVER 0.5/1.5/2.5 · BTTS · Home Win · Away Win         ║
║  Adaptive AI Self-Learning · Multi-API: ESPN + TheSportsDB          ║
║  75+ World Leagues · Full Self-Automation · Zero Human Needed       ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import requests
import sqlite3
import json
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Tuple, Any
import time
import hashlib

st.set_page_config(
    page_title="ZEUS ⚡ Neural Football AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={"About": "ZEUS Neural Football AI v3.0 — Adaptive Learning · Multi-Bet · 75+ Leagues"},
)

# ═══════════════════════════════════════════════════════════════════════
#  CSS — Stadium-at-Night (v3 – multi-bet palette)
# ═══════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@400;500&display=swap');

:root {
  --bg:       #040b04;
  --surface:  #0a160a;
  --card:     #0d1b0d;
  --border:   #183018;
  --green:    #39ff14;
  --green2:   #00c853;
  --gold:     #ffb300;
  --gold2:    #ff8f00;
  --cyan:     #00e5ff;
  --red:      #ff1744;
  --purple:   #ea80fc;
  --orange:   #ff6d00;
  --text:     #d4f0d4;
  --muted:    #4e724e;
}

html, body, .stApp { background: var(--bg) !important; font-family: 'Barlow', sans-serif; }

.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(57,255,20,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(57,255,20,0.02) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridMove 30s linear infinite;
  pointer-events: none; z-index: 0;
}
@keyframes gridMove { 100% { background-position: 60px 60px, 60px 60px; } }

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1300px; position: relative; z-index: 1; }

/* ── Hero ─── */
.zeus-hero { text-align: center; padding: 22px 0 8px; }
.zeus-logo {
  font-family: 'Bebas Neue', cursive; font-size: 5.5rem; letter-spacing: 12px; line-height: 1;
  background: linear-gradient(135deg, #39ff14 0%, #69ff47 40%, #ffb300 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  animation: logoGlow 4s ease-in-out infinite;
}
@keyframes logoGlow {
  0%,100% { filter: drop-shadow(0 0 8px rgba(57,255,20,0.4)); }
  50%      { filter: drop-shadow(0 0 28px rgba(57,255,20,0.9)); }
}
.zeus-tagline { font-family:'Barlow Condensed',sans-serif; font-size:0.78rem; letter-spacing:4px; text-transform:uppercase; color:var(--muted); margin-top:4px; }
.zeus-version { font-family:'Barlow Condensed',sans-serif; font-size:0.66rem; letter-spacing:3px; text-transform:uppercase; color:var(--cyan); margin-top:2px; opacity:0.75; }
.zeus-bar { width:80px; height:2px; background:linear-gradient(90deg,transparent,var(--green),transparent); margin:12px auto 0; animation:barPulse 2s ease-in-out infinite; }
@keyframes barPulse { 0%,100%{width:80px;opacity:.6;} 50%{width:200px;opacity:1;} }

/* ── Metrics ─── */
.metrics-row { display:flex; gap:10px; margin:14px 0; flex-wrap:wrap; }
.metric-box { flex:1; min-width:90px; background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:12px 14px; text-align:center; transition:border-color .3s; }
.metric-box:hover { border-color:var(--green); }
.metric-val { font-family:'Bebas Neue',cursive; font-size:2rem; color:var(--green); line-height:1; display:block; }
.metric-val.gold   { color:var(--gold); }
.metric-val.cyan   { color:var(--cyan); }
.metric-val.purple { color:var(--purple); }
.metric-val.red    { color:var(--red); }
.metric-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.67rem; color:var(--muted); text-transform:uppercase; letter-spacing:1.5px; }

/* ── Scan line ─── */
.scan-line { font-family:'Barlow Condensed',sans-serif; font-size:0.78rem; color:var(--green); letter-spacing:3px; text-transform:uppercase; text-align:center; padding:8px; animation:scanFade .9s ease-in-out infinite; }
@keyframes scanFade { 0%,100%{opacity:1;} 50%{opacity:0.2;} }

/* ── Pick cards ─── */
.pick-card {
  background:var(--card); border:1px solid var(--border); border-radius:18px; padding:22px 26px; margin:14px 0;
  position:relative; overflow:hidden; opacity:0;
  animation:cardReveal .5s ease forwards; transition:transform .25s, box-shadow .25s;
}
.pick-card:hover { transform:translateY(-4px); box-shadow:0 14px 44px rgba(57,255,20,.14); }
.pick-card:nth-child(1){animation-delay:.04s} .pick-card:nth-child(2){animation-delay:.12s}
.pick-card:nth-child(3){animation-delay:.20s} .pick-card:nth-child(4){animation-delay:.28s}
.pick-card:nth-child(5){animation-delay:.36s} .pick-card:nth-child(6){animation-delay:.44s}
.pick-card:nth-child(7){animation-delay:.52s}
@keyframes cardReveal { from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }

/* Bet type colours */
.pick-card.elite  { border-color:var(--gold);   background:linear-gradient(135deg,#0d1b0d 0%,#1a1400 100%); animation:cardReveal .5s ease forwards,eliteGlow 3s ease-in-out infinite; }
.pick-card.strong { border-color:var(--green2); }
.pick-card.btts   { border-color:var(--purple); }
.pick-card.result { border-color:var(--cyan);   }
@keyframes eliteGlow { 0%,100%{box-shadow:0 0 16px rgba(255,179,0,.1);} 50%{box-shadow:0 0 44px rgba(255,179,0,.32);} }

.rank-badge { position:absolute; top:14px; right:20px; font-family:'Bebas Neue',cursive; font-size:4rem; line-height:1; color:rgba(57,255,20,.05); pointer-events:none; user-select:none; }

.card-league { font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; color:var(--muted); margin-bottom:6px; }
.card-teams { font-family:'Bebas Neue',cursive; font-size:2rem; letter-spacing:3px; color:var(--text); line-height:1.1; margin-bottom:10px; }
.card-vs { color:var(--muted); font-size:1rem; padding:0 8px; }

/* Bet label colours by type */
.card-bet { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.5rem; letter-spacing:1px; margin-bottom:12px; }
.bet-over05  { color:var(--cyan);   }
.bet-over15  { color:var(--green);  }
.bet-over25  { color:var(--gold);   }
.bet-btts    { color:var(--purple); }
.bet-home    { color:var(--green2); }
.bet-away    { color:var(--orange); }

.conf-track { background:rgba(255,255,255,.06); border-radius:999px; height:6px; margin:8px 0 10px; overflow:hidden; }
.conf-fill  { height:100%; border-radius:999px; animation:fillBar 1.2s cubic-bezier(.22,1,.36,1) forwards; transform-origin:left; }
.conf-fill.elite  { background:linear-gradient(90deg,var(--gold2),var(--gold)); }
.conf-fill.strong { background:linear-gradient(90deg,var(--green2),var(--green)); }
.conf-fill.btts   { background:linear-gradient(90deg,#7b1fa2,var(--purple)); }
.conf-fill.result { background:linear-gradient(90deg,#006064,var(--cyan)); }
@keyframes fillBar { from{width:0 !important;} }

.conf-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; }
.conf-pct { font-family:'Bebas Neue',cursive; font-size:1.6rem; letter-spacing:2px; }
.conf-pct.elite  { color:var(--gold); }
.conf-pct.strong { color:var(--green); }
.conf-pct.btts   { color:var(--purple); }
.conf-pct.result { color:var(--cyan); }

.tier-chip { font-family:'Barlow Condensed',sans-serif; font-size:0.7rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; padding:3px 10px; border-radius:999px; }
.tier-chip.elite  { background:rgba(255,179,0,.15);  color:var(--gold);   border:1px solid rgba(255,179,0,.4); }
.tier-chip.strong { background:rgba(57,255,20,.1);   color:var(--green);  border:1px solid rgba(57,255,20,.3); }
.tier-chip.btts   { background:rgba(234,128,252,.1); color:var(--purple); border:1px solid rgba(234,128,252,.3); }
.tier-chip.result { background:rgba(0,229,255,.1);   color:var(--cyan);   border:1px solid rgba(0,229,255,.3); }

.pills-row { display:flex; gap:6px; flex-wrap:wrap; margin-top:10px; }
.pill { font-family:'Barlow Condensed',sans-serif; font-size:0.73rem; letter-spacing:1px; padding:3px 9px; border-radius:6px; white-space:nowrap; }
.pill-time  { background:rgba(57,255,20,.08);  color:var(--green);  border:1px solid rgba(57,255,20,.2); }
.pill-xg    { background:rgba(255,179,0,.08);  color:var(--gold);   border:1px solid rgba(255,179,0,.2); }
.pill-pois  { background:rgba(0,229,255,.08);  color:var(--cyan);   border:1px solid rgba(0,229,255,.2); }
.pill-btts  { background:rgba(41,182,246,.08); color:#29b6f6;       border:1px solid rgba(41,182,246,.2); }
.pill-form  { background:rgba(234,128,252,.08);color:var(--purple); border:1px solid rgba(234,128,252,.2); }
.pill-h2h   { background:rgba(255,64,64,.08);  color:#ff6464;       border:1px solid rgba(255,64,64,.2); }
.pill-games { background:rgba(255,255,255,.04);color:var(--muted);  border:1px solid rgba(255,255,255,.08); }
.pill-learn { background:rgba(0,200,83,.08);   color:#00c853;       border:1px solid rgba(0,200,83,.2); }

.ai-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin-top:10px; }
.ai-factor { background:rgba(57,255,20,.04); border:1px solid rgba(57,255,20,.1); border-radius:8px; padding:6px 8px; text-align:center; }
.ai-factor-val { font-family:'Bebas Neue',cursive; font-size:1.1rem; color:var(--green); display:block; line-height:1; }
.ai-factor-val.gold   { color:var(--gold); }
.ai-factor-val.cyan   { color:var(--cyan); }
.ai-factor-val.purple { color:var(--purple); }
.ai-factor-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.62rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; }

.card-reason { font-family:'Barlow',sans-serif; font-size:0.8rem; color:var(--muted); margin-top:10px; line-height:1.55; border-left:2px solid var(--border); padding-left:10px; }
.countdown { font-family:'Bebas Neue',cursive; font-size:0.85rem; letter-spacing:2px; color:var(--green); }
.no-picks { text-align:center; padding:52px 24px; font-family:'Barlow Condensed',sans-serif; font-size:1.1rem; color:var(--muted); letter-spacing:2px; }
.no-picks-icon { font-size:3rem; display:block; margin-bottom:12px; }
.learn-badge { display:inline-block; background:rgba(0,200,83,.1); border:1px solid rgba(0,200,83,.3); border-radius:8px; padding:4px 10px; font-family:'Barlow Condensed',sans-serif; font-size:0.72rem; color:#00c853; letter-spacing:2px; text-transform:uppercase; }

hr { border-color:rgba(57,255,20,.08) !important; }
.stTabs [data-baseweb="tab-list"] { background:var(--surface); border-radius:12px; padding:4px; gap:2px; border:1px solid var(--border); }
.stTabs [data-baseweb="tab"] { border-radius:8px; font-family:'Barlow Condensed',sans-serif; letter-spacing:1px; color:var(--muted); font-size:.9rem; }
.stTabs [aria-selected="true"] { background:rgba(57,255,20,.12) !important; color:var(--green) !important; }

/* ── Live Match Cards ─── */
.live-pulse {
  display:inline-block; width:9px; height:9px; background:var(--red);
  border-radius:50%; margin-right:7px;
  animation:livePulse 1.1s ease-in-out infinite;
  box-shadow:0 0 0 0 rgba(255,23,68,.7);
}
@keyframes livePulse {
  0%  { transform:scale(1);   box-shadow:0 0 0 0   rgba(255,23,68,.7); }
  60% { transform:scale(1.15);box-shadow:0 0 0 8px rgba(255,23,68,0);  }
  100%{ transform:scale(1);   box-shadow:0 0 0 0   rgba(255,23,68,0);  }
}
.live-header {
  display:flex; align-items:center; justify-content:space-between;
  margin-bottom:16px;
}
.live-badge {
  font-family:'Barlow Condensed',sans-serif; font-size:0.72rem; font-weight:700;
  letter-spacing:3px; text-transform:uppercase; padding:3px 10px; border-radius:999px;
  background:rgba(255,23,68,.15); color:var(--red); border:1px solid rgba(255,23,68,.4);
}
.live-clock {
  font-family:'Bebas Neue',cursive; font-size:1.1rem; letter-spacing:3px; color:var(--red);
}
.live-score-block {
  display:flex; align-items:center; justify-content:center;
  gap:18px; padding:16px 0 12px;
}
.live-team-name {
  font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:1.05rem;
  letter-spacing:1px; text-transform:uppercase; color:var(--text); max-width:120px;
  text-align:center; word-break:break-word;
}
.live-score {
  font-family:'Bebas Neue',cursive; font-size:3.8rem; letter-spacing:6px; color:var(--green);
  line-height:1; text-shadow:0 0 20px rgba(57,255,20,.5);
}
.live-sep { font-family:'Bebas Neue',cursive; font-size:2rem; color:var(--border); }

.live-card {
  background:var(--card); border:1px solid rgba(255,23,68,.25); border-radius:18px;
  padding:20px 24px; margin:14px 0; overflow:hidden; position:relative;
  animation:cardReveal .45s ease forwards;
  transition:transform .25s, box-shadow .25s;
}
.live-card:hover { transform:translateY(-3px); box-shadow:0 12px 40px rgba(255,23,68,.12); }
.live-card::before {
  content:''; position:absolute; top:0; left:0; right:0; height:2px;
  background:linear-gradient(90deg,transparent,var(--red),transparent);
  animation:scanLine 3s linear infinite;
}
@keyframes scanLine { 0%{background-position:-200px 0;} 100%{background-position:200px 0;} }

.pred-grid {
  display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:12px 0;
}
.pred-cell {
  background:rgba(0,0,0,.3); border-radius:10px; padding:8px 6px; text-align:center;
  border:1px solid var(--border); transition:border-color .2s;
}
.pred-cell.hit  { border-color:var(--green2); background:rgba(0,200,83,.07); }
.pred-cell.live-edge { border-color:var(--gold); background:rgba(255,179,0,.07); }
.pred-val {
  font-family:'Bebas Neue',cursive; font-size:1.3rem; display:block;
  line-height:1; margin-bottom:2px;
}
.pred-lbl { font-family:'Barlow Condensed',sans-serif; font-size:0.62rem; color:var(--muted); text-transform:uppercase; letter-spacing:1px; }
.live-reason { font-family:'Barlow',sans-serif; font-size:0.79rem; color:var(--muted); margin-top:10px; line-height:1.55; border-left:2px solid rgba(255,23,68,.3); padding-left:10px; }
.live-empty { text-align:center; padding:52px 24px; font-family:'Barlow Condensed',sans-serif; font-size:1rem; color:var(--muted); letter-spacing:2px; }
.live-metrics { display:flex; gap:10px; margin:14px 0; flex-wrap:wrap; }
.halftime-chip {
  font-family:'Barlow Condensed',sans-serif; font-size:0.72rem; font-weight:700;
  letter-spacing:3px; padding:3px 10px; border-radius:999px;
  background:rgba(255,179,0,.15); color:var(--gold); border:1px solid rgba(255,179,0,.4);
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════════════════
ESPN_SOCCER  = "https://site.api.espn.com/apis/site/v2/sports/soccer"
TSDB_BASE    = "https://www.thesportsdb.com/api/v1/json/3"  # free key=3
CAT_OFFSET   = timedelta(hours=2)   # UTC+2
WINDOW_HOURS = 24
MIN_GAMES    = 5
HISTORY_GAMES= 38
TOP_N        = 20
LEARNING_RATE= 0.004  # adaptive weight nudge per graded pick

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept": "application/json",
}

# ── Bet type registry ─────────────────────────────────────────────────
# gate = minimum composite confidence% required to be shown
BET_TYPES: Dict[str, Dict] = {
    "OVER_05":  {"label": "OVER 0.5 Goals",      "line": 0.5,  "gate": 88.0, "css": "over05",  "emoji": "⚡"},
    "OVER_15":  {"label": "OVER 1.5 Goals",      "line": 1.5,  "gate": 78.0, "css": "over15",  "emoji": "⚽"},
    "OVER_25":  {"label": "OVER 2.5 Goals",      "line": 2.5,  "gate": 65.0, "css": "over25",  "emoji": "🔥"},
    "BTTS_YES": {"label": "Both Teams Score",     "line": None, "gate": 70.0, "css": "btts",    "emoji": "🎯"},
    "HOME_WIN": {"label": "Home Win",             "line": None, "gate": 74.0, "css": "home",    "emoji": "🏠"},
    "AWAY_WIN": {"label": "Away Win",             "line": None, "gate": 74.0, "css": "away",    "emoji": "✈️"},
}

# Default factor weights per bet type (sum = 1.0)
DEFAULT_WEIGHTS: Dict[str, Dict[str, float]] = {
    "OVER_05": {
        "poisson_p":  0.50, "hist_rate":  0.20, "form":    0.10,
        "streak":     0.10, "btts":       0.05, "h2h":     0.05,
    },
    "OVER_15": {
        "poisson_p":  0.42, "hist_rate":  0.26, "xg_norm": 0.14,
        "form":       0.08, "btts":       0.05, "h2h":     0.05,
    },
    "OVER_25": {
        "poisson_p":  0.35, "hist_rate":  0.25, "xg_norm": 0.20,
        "btts":       0.10, "form":       0.05, "h2h":     0.05,
    },
    "BTTS_YES": {
        "poisson_btts": 0.40, "hist_btts": 0.35, "xg_balance": 0.10,
        "form":         0.10, "h2h":       0.05,
    },
    "HOME_WIN": {
        "poisson_hw":  0.45, "hist_hw":   0.25, "form_diff": 0.15,
        "xg_diff":     0.10, "h2h":       0.05,
    },
    "AWAY_WIN": {
        "poisson_aw":  0.45, "hist_aw":   0.25, "form_diff": 0.15,
        "xg_diff":     0.10, "h2h":       0.05,
    },
}

# ── 75-League universe ────────────────────────────────────────────────
LEAGUES: List[Tuple[str, str, str]] = [
    # Top 5 Europe
    ("eng.1","Premier League","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.2","Championship","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.3","League One","🏴󠁧󠁢󠁥󠁮󠁧󠁿"), ("eng.4","League Two","🏴󠁧󠁢󠁥󠁮󠁧󠁿"),
    ("esp.1","La Liga","🇪🇸"), ("esp.2","Segunda División","🇪🇸"),
    ("ger.1","Bundesliga","🇩🇪"), ("ger.2","2. Bundesliga","🇩🇪"), ("ger.3","3. Liga","🇩🇪"),
    ("ita.1","Serie A","🇮🇹"), ("ita.2","Serie B","🇮🇹"),
    ("fra.1","Ligue 1","🇫🇷"), ("fra.2","Ligue 2","🇫🇷"),
    # Wider Europe
    ("ned.1","Eredivisie","🇳🇱"), ("ned.2","Eerste Divisie","🇳🇱"),
    ("por.1","Primeira Liga","🇵🇹"), ("por.2","Liga Portugal 2","🇵🇹"),
    ("sco.1","Scottish Premiership","🏴󠁧󠁢󠁳󠁣󠁴󠁿"), ("sco.2","Scottish Championship","🏴󠁧󠁢󠁳󠁣󠁴󠁿"),
    ("tur.1","Süper Lig","🇹🇷"), ("tur.2","TFF First League","🇹🇷"),
    ("bel.1","Belgian Pro League","🇧🇪"), ("gre.1","Super League Greece","🇬🇷"),
    ("ukr.1","Ukrainian Premier","🇺🇦"), ("den.1","Superligaen","🇩🇰"),
    ("swe.1","Allsvenskan","🇸🇪"), ("nor.1","Eliteserien","🇳🇴"),
    ("aut.1","Austrian Bundesliga","🇦🇹"), ("sui.1","Swiss Super League","🇨🇭"),
    ("cze.1","Czech First League","🇨🇿"), ("pol.1","Ekstraklasa","🇵🇱"),
    ("rou.1","Liga 1 Romania","🇷🇴"), ("srb.1","Serbian SuperLiga","🇷🇸"),
    ("hun.1","OTP Bank Liga","🇭🇺"), ("bul.1","First Professional League","🇧🇬"),
    ("cro.1","HNL Croatia","🇭🇷"), ("svk.1","Fortuna Liga Slovakia","🇸🇰"),
    ("fin.1","Veikkausliiga","🇫🇮"), ("isr.1","Israeli Premier","🇮🇱"),
    ("rus.1","Russian Premier","🇷🇺"),
    # Americas
    ("usa.1","MLS","🇺🇸"), ("usa.2","USL Championship","🇺🇸"),
    ("mex.1","Liga MX","🇲🇽"), ("mex.2","Ascenso MX","🇲🇽"),
    ("bra.1","Brasileirão","🇧🇷"), ("bra.2","Série B","🇧🇷"),
    ("arg.1","Primera División","🇦🇷"), ("col.1","Liga Betplay","🇨🇴"),
    ("chi.1","Primera Chile","🇨🇱"), ("ecu.1","Liga Pro Ecuador","🇪🇨"),
    ("per.1","Liga 1 Peru","🇵🇪"), ("uru.1","Uruguay Primera","🇺🇾"),
    ("ven.1","Liga Futve","🇻🇪"), ("par.1","División Profesional","🇵🇾"),
    # Asia / Pacific
    ("jpn.1","J1 League","🇯🇵"), ("jpn.2","J2 League","🇯🇵"),
    ("kor.1","K League 1","🇰🇷"), ("chn.1","Chinese Super League","🇨🇳"),
    ("aus.1","A-League","🇦🇺"), ("ind.1","Indian Super League","🇮🇳"),
    ("tha.1","Thai League 1","🇹🇭"), ("mys.1","Super League Malaysia","🇲🇾"),
    # Middle East / Africa
    ("sau.1","Saudi Pro League","🇸🇦"), ("uae.1","UAE Pro League","🇦🇪"),
    ("egy.1","Egyptian Premier","🇪🇬"), ("rsa.1","PSL South Africa","🇿🇦"),
    ("mar.1","Botola Pro Morocco","🇲🇦"), ("nga.1","NPFL Nigeria","🇳🇬"),
    ("qat.1","Qatar Stars League","🇶🇦"),
    # Continental / Cups
    ("uefa.champions","Champions League","🏆"), ("uefa.europa","Europa League","🟠"),
    ("uefa.europaconference","Conference League","🟢"),
    ("conmebol.libertadores","Copa Libertadores","🏆"),
    ("concacaf.champions","CONCACAF Champions","🌎"),
]


# ═══════════════════════════════════════════════════════════════════════
#  POISSON MATHEMATICS ENGINE
# ═══════════════════════════════════════════════════════════════════════

def _pois_pmf(k: int, lam: float) -> float:
    if lam <= 0:
        return 1.0 if k == 0 else 0.0
    try:
        return (lam ** k) * math.exp(-lam) / math.factorial(k)
    except Exception:
        return 0.0


def poisson_over_line(lam_home: float, lam_away: float, line: float) -> float:
    """P(total goals > line)"""
    p_under = 0.0
    for h in range(13):
        for a in range(13):
            if (h + a) <= line:
                p_under += _pois_pmf(h, max(0.01, lam_home)) * _pois_pmf(a, max(0.01, lam_away))
    return max(0.0, min(1.0, 1.0 - p_under))


def poisson_btts(lam_home: float, lam_away: float) -> float:
    """P(home ≥ 1 AND away ≥ 1)"""
    p_home_0 = _pois_pmf(0, max(0.01, lam_home))
    p_away_0 = _pois_pmf(0, max(0.01, lam_away))
    return max(0.0, min(1.0, (1 - p_home_0) * (1 - p_away_0)))


def poisson_home_win(lam_home: float, lam_away: float) -> float:
    """P(home goals > away goals)"""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if h > a:
                p += _pois_pmf(h, max(0.01, lam_home)) * _pois_pmf(a, max(0.01, lam_away))
    return max(0.0, min(1.0, p))


def poisson_away_win(lam_home: float, lam_away: float) -> float:
    """P(away goals > home goals)"""
    p = 0.0
    for h in range(13):
        for a in range(13):
            if a > h:
                p += _pois_pmf(h, max(0.01, lam_home)) * _pois_pmf(a, max(0.01, lam_away))
    return max(0.0, min(1.0, p))


def safe_mean(lst: list) -> float:
    return float(np.mean(lst)) if lst else 0.0


# ═══════════════════════════════════════════════════════════════════════
#  DATABASE — full schema + auto-migration
# ═══════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect("zeus_v3.db", check_same_thread=False)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_cache (
            cache_key TEXT PRIMARY KEY, data TEXT, ts REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS picks_log (
            id           TEXT PRIMARY KEY,
            match        TEXT,
            league       TEXT,
            league_id    TEXT,
            bet          TEXT,
            bet_type     TEXT DEFAULT 'OVER_25',
            xg_total     REAL,
            confidence   REAL,
            kickoff      TEXT,
            result       TEXT DEFAULT 'pending',
            home_score   INTEGER DEFAULT -1,
            away_score   INTEGER DEFAULT -1,
            factors_json TEXT DEFAULT '{}',
            logged_at    TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS model_weights (
            bet_type TEXT,
            factor   TEXT,
            weight   REAL,
            wins     INTEGER DEFAULT 0,
            losses   INTEGER DEFAULT 0,
            updates  INTEGER DEFAULT 0,
            PRIMARY KEY (bet_type, factor)
        )
    """)

    # Auto-migrate older picks_log if needed
    for col, defval in [
        ("bet_type","'OVER_25'"), ("home_score","-1"),
        ("away_score","-1"), ("factors_json","'{}'"),
    ]:
        try:
            conn.execute(f"ALTER TABLE picks_log ADD COLUMN {col} TEXT DEFAULT {defval}")
        except Exception:
            pass

    conn.commit()
    _init_weights(conn)
    return conn


def _init_weights(conn: sqlite3.Connection):
    """Seed default weights if not yet stored."""
    for bet_type, factors in DEFAULT_WEIGHTS.items():
        for factor, w in factors.items():
            conn.execute(
                "INSERT OR IGNORE INTO model_weights (bet_type,factor,weight) VALUES (?,?,?)",
                (bet_type, factor, w)
            )
    conn.commit()


def get_weights(bet_type: str) -> Dict[str, float]:
    conn = get_db()
    rows = conn.execute(
        "SELECT factor, weight FROM model_weights WHERE bet_type=?", (bet_type,)
    ).fetchall()
    if not rows:
        return DEFAULT_WEIGHTS.get(bet_type, {})
    w = {r[0]: r[1] for r in rows}
    # Normalize to sum to 1.0
    total = sum(w.values())
    if total > 0:
        w = {k: v / total for k, v in w.items()}
    return w


def update_weights(bet_type: str, factors: Dict[str, float], won: bool):
    """
    Online gradient update — nudge weights based on which factors
    contributed most to a winning / losing pick.
    """
    conn = get_db()
    current = get_weights(bet_type)
    signal = 1.0 if won else -0.5   # learn more from wins (asymmetric)

    new_w = {}
    for factor, val in factors.items():
        if factor not in current:
            continue
        # If factor value was high (>0.6) and we WON → increase its weight
        contribution = (val - 0.5)   # centred: positive = factor was bullish
        delta = LEARNING_RATE * signal * contribution
        new_w[factor] = max(0.02, min(0.70, current[factor] + delta))

    # Re-normalise
    total = sum(new_w.values())
    if total > 0:
        new_w = {k: v / total for k, v in new_w.items()}

    for factor, weight in new_w.items():
        result_col = "wins" if won else "losses"
        conn.execute(
            f"""UPDATE model_weights
                SET weight=?, {result_col}={result_col}+1, updates=updates+1
                WHERE bet_type=? AND factor=?""",
            (weight, bet_type, factor)
        )
    conn.commit()


# ── Cache helpers ─────────────────────────────────────────────────────
def cache_get(key: str, ttl: int) -> Optional[Any]:
    try:
        conn = get_db()
        row = conn.execute("SELECT data, ts FROM api_cache WHERE cache_key=?", (key,)).fetchone()
        if row and (time.time() - row[1]) < ttl:
            return json.loads(row[0])
    except Exception:
        pass
    return None


def cache_set(key: str, data: Any):
    try:
        conn = get_db()
        conn.execute("INSERT OR REPLACE INTO api_cache VALUES (?,?,?)",
                     (key, json.dumps(data, default=str), time.time()))
        conn.commit()
    except Exception:
        pass


def save_pick(pick: Dict):
    try:
        pid = hashlib.md5(f"{pick['match']}{pick['kickoff_utc']}{pick['bet_type']}".encode()).hexdigest()[:12]
        conn = get_db()
        conn.execute("""
            INSERT OR IGNORE INTO picks_log
            (id,match,league,league_id,bet,bet_type,xg_total,confidence,kickoff,factors_json,logged_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """, (
            pid, pick["match"], pick["league"], pick.get("league_id",""),
            pick["bet"], pick["bet_type"], pick["xg_total"], pick["confidence"],
            pick["kickoff_utc"], json.dumps(pick.get("factors",{})),
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        ))
        conn.commit()
    except Exception:
        pass


# ═══════════════════════════════════════════════════════════════════════
#  TIME HELPERS
# ═══════════════════════════════════════════════════════════════════════

def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def to_cat(utc_str: str) -> str:
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return (dt + CAT_OFFSET).strftime("%d %b · %H:%M CAT")
    except Exception:
        return "—"


def parse_utc(utc_str: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
    except Exception:
        return None


def in_window(utc_str: str) -> bool:
    dt = parse_utc(utc_str)
    if not dt:
        return False
    n = now_utc()
    return n <= dt <= n + timedelta(hours=WINDOW_HOURS)


def minutes_to_kickoff(utc_str: str) -> int:
    dt = parse_utc(utc_str)
    if not dt:
        return 9999
    return max(0, int((dt - now_utc()).total_seconds() / 60))


# ═══════════════════════════════════════════════════════════════════════
#  API HELPERS
# ═══════════════════════════════════════════════════════════════════════

def safe_get(url: str, params: Dict = None, timeout: int = 10) -> Optional[Dict]:
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def _parse_score(raw) -> int:
    if raw is None:
        return 0
    if isinstance(raw, dict):
        raw = raw.get("value", raw.get("displayValue", 0))
    try:
        return int(float(str(raw)))
    except (ValueError, TypeError):
        return 0


# ═══════════════════════════════════════════════════════════════════════
#  ESPN DATA FETCHERS
# ═══════════════════════════════════════════════════════════════════════

def fetch_scoreboard(league_id: str) -> List[Dict]:
    result = []
    for delta in [0, 1]:
        date_str = (now_utc() + timedelta(days=delta)).strftime("%Y%m%d")
        key = f"sb_{league_id}_{date_str}"
        cached = cache_get(key, ttl=300)
        if cached is not None:
            result.extend(cached)
            continue
        data = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str})
        if not data:
            continue
        events = []
        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            status_type = comp.get("status", {}).get("type", {})
            events.append({
                "event_id":  ev.get("id", ""),
                "date":      ev.get("date", ""),
                "home_id":   str(home_c.get("team", {}).get("id", "")),
                "home_name": home_c.get("team", {}).get("displayName", ""),
                "away_id":   str(away_c.get("team", {}).get("id", "")),
                "away_name": away_c.get("team", {}).get("displayName", ""),
                "status":    status_type.get("name", ""),
                "completed": status_type.get("completed", False),
                "league_id": league_id,
            })
        cache_set(key, events)
        result.extend(events)
    return result


def fetch_team_schedule_espn(league_id: str, team_id: str) -> List[Dict]:
    date_tag = now_utc().strftime("%Y%m%d")
    key = f"sched_{league_id}_{team_id}_{date_tag}"
    cached = cache_get(key, ttl=3600)
    if cached is not None:
        return cached

    data = safe_get(f"{ESPN_SOCCER}/{league_id}/teams/{team_id}/schedule")
    if not data:
        return []

    games = []
    for ev in data.get("events", []):
        comps = ev.get("competitions", [])
        if not comps:
            continue
        comp = comps[0]
        if not comp.get("status", {}).get("type", {}).get("completed", False):
            continue
        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue
        home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
        hs = _parse_score(home_c.get("score"))
        as_ = _parse_score(away_c.get("score"))
        games.append({
            "date":       ev.get("date", ""),
            "home_name":  home_c.get("team", {}).get("displayName", ""),
            "away_name":  away_c.get("team", {}).get("displayName", ""),
            "home_score": hs,
            "away_score": as_,
            "total":      hs + as_,
        })

    games.sort(key=lambda g: g["date"])
    games = games[-HISTORY_GAMES:]
    cache_set(key, games)
    return games


def fetch_tsdb_team_last15(team_name: str) -> List[Dict]:
    """
    TheSportsDB free tier — search team then pull last events.
    Used as supplementary data when ESPN schedule is thin.
    """
    key = f"tsdb_{hashlib.md5(team_name.encode()).hexdigest()[:8]}"
    cached = cache_get(key, ttl=7200)
    if cached is not None:
        return cached

    # Step 1: find team ID
    sr = safe_get(f"{TSDB_BASE}/searchteams.php", params={"t": team_name}, timeout=6)
    if not sr or not sr.get("teams"):
        return []
    team_id = sr["teams"][0].get("idTeam", "")
    if not team_id:
        return []

    # Step 2: last 15 events
    er = safe_get(f"{TSDB_BASE}/eventslast15.php", params={"id": team_id}, timeout=6)
    if not er or not er.get("results"):
        return []

    games = []
    for ev in er["results"]:
        try:
            hs  = int(ev.get("intHomeScore", 0) or 0)
            as_ = int(ev.get("intAwayScore", 0) or 0)
            home = ev.get("strHomeTeam", "")
            away = ev.get("strAwayTeam", "")
            date = ev.get("dateEvent", "")
            if not home or not away:
                continue
            games.append({
                "date": date,
                "home_name":  home,
                "away_name":  away,
                "home_score": hs,
                "away_score": as_,
                "total":      hs + as_,
            })
        except Exception:
            pass

    cache_set(key, games)
    return games


def fetch_team_schedule(league_id: str, team_id: str, team_name: str) -> List[Dict]:
    """
    Multi-API fetch: ESPN primary → TheSportsDB supplement.
    Returns combined de-duplicated history sorted by date.
    """
    espn_games = fetch_team_schedule_espn(league_id, team_id)

    if len(espn_games) >= MIN_GAMES:
        return espn_games

    # Supplement with TheSportsDB
    tsdb_games = fetch_tsdb_team_last15(team_name)
    if not tsdb_games:
        return espn_games

    # Deduplicate by approximate date+teams key
    seen = set()
    combined = []
    for g in espn_games + tsdb_games:
        k = f"{g['date'][:10]}_{g.get('home_name','')}_{g.get('away_name','')}"
        if k not in seen:
            seen.add(k)
            combined.append(g)

    combined.sort(key=lambda g: g.get("date", ""))
    return combined[-HISTORY_GAMES:]


# ═══════════════════════════════════════════════════════════════════════
#  ZEUS STATISTICS ENGINE v3.0
# ═══════════════════════════════════════════════════════════════════════

def team_stats(games: List[Dict], team_name: str) -> Optional[Dict]:
    completed = [g for g in games
                 if g.get("total", 0) >= 0
                 and (g.get("home_score", -1) >= 0 or g.get("away_score", -1) >= 0)]

    if len(completed) < MIN_GAMES:
        return None

    home_games = [g for g in completed if g.get("home_name", "") == team_name]
    away_games = [g for g in completed if g.get("away_name", "") == team_name]

    def _split_stats(gl, scored_key, conceded_key):
        if not gl:
            return None, None, None, None
        sc  = [g[scored_key]   for g in gl]
        co  = [g[conceded_key] for g in gl]
        tot = [s + c for s, c in zip(sc, co)]
        n   = len(gl)
        return (
            safe_mean(sc),
            safe_mean(co),
            sum(1 for t in tot if t > 0.5) / n,  # over 0.5
            sum(1 for s, c in zip(sc, co) if s > 0 and c > 0) / n,  # btts
        )

    h_sc, h_co, h_over05, h_btts = _split_stats(home_games, "home_score", "away_score")
    a_sc, a_co, a_over05, a_btts = _split_stats(away_games, "away_score", "home_score")

    # ── Overall stats ────────────────────────────────────────────
    all_sc, all_co, all_tot = [], [], []
    for g in completed:
        is_home = g.get("home_name", "") == team_name
        sc  = g["home_score"] if is_home else g["away_score"]
        co  = g["away_score"] if is_home else g["home_score"]
        all_sc.append(sc); all_co.append(co); all_tot.append(sc + co)

    n = len(completed)
    avg_sc     = safe_mean(all_sc)
    avg_co     = safe_mean(all_co)
    avg_tot    = safe_mean(all_tot)

    over05_r   = sum(1 for t in all_tot if t > 0.5) / n
    over15_r   = sum(1 for t in all_tot if t > 1.5) / n
    over25_r   = sum(1 for t in all_tot if t > 2.5) / n
    btts_r     = sum(1 for s, c in zip(all_sc, all_co) if s > 0 and c > 0) / n
    cs_r       = sum(1 for c in all_co if c == 0) / n   # clean sheet rate
    wins_r     = sum(1 for s, c in zip(all_sc, all_co) if s > c) / n

    # Form (last 5 vs rest)
    recent5    = all_tot[-5:] if n >= 5 else all_tot
    older      = all_tot[:-5] if n > 5 else all_tot
    form_score = max(0.0, min(1.0, 0.5 + (safe_mean(recent5) - safe_mean(older)) / 4.0))
    last3_avg  = safe_mean(all_tot[-3:]) if n >= 3 else avg_tot

    # Streak counters
    streak_over05 = streak_over15 = streak_over25 = streak_btts = 0
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        t = s + c
        if t > 0.5: streak_over05 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        t = s + c
        if t > 1.5: streak_over15 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        t = s + c
        if t > 2.5: streak_over25 += 1
        else: break
    for s, c in zip(reversed(all_sc), reversed(all_co)):
        if s > 0 and c > 0: streak_btts += 1
        else: break

    return {
        "n": n, "n_home": len(home_games), "n_away": len(away_games),
        "avg_scored":  avg_sc, "avg_conceded": avg_co, "avg_total": avg_tot,
        "over05_rate": over05_r, "over15_rate": over15_r,
        "over25_rate": over25_r, "btts_rate": btts_r,
        "cs_rate": cs_r, "wins_rate": wins_r,
        # Venue splits (home at home)
        "home_avg_scored":   h_sc   if h_sc   is not None else avg_sc,
        "home_avg_conceded": h_co   if h_co   is not None else avg_co,
        "home_over05_rate":  h_over05 if h_over05 is not None else over05_r,
        "home_btts_rate":    h_btts if h_btts is not None else btts_r,
        # Venue splits (away away)
        "away_avg_scored":   a_sc   if a_sc   is not None else avg_sc,
        "away_avg_conceded": a_co   if a_co   is not None else avg_co,
        "away_over05_rate":  a_over05 if a_over05 is not None else over05_r,
        "away_btts_rate":    a_btts if a_btts is not None else btts_r,
        # Form
        "form_score": form_score, "last3_avg": last3_avg,
        # Streaks
        "streak_over05": streak_over05, "streak_over15": streak_over15,
        "streak_over25": streak_over25, "streak_btts": streak_btts,
    }


def get_h2h_stats(home_sched, away_sched, home_name, away_name):
    """Returns dict of H2H rates (None if < 3 meetings)."""
    seen, totals, home_wins, away_wins, bttss = set(), [], [], [], []
    for g in home_sched + away_sched:
        gk = f"{g.get('date','')[:10]}_{g.get('home_name','')}_{g.get('away_name','')}"
        if gk in seen:
            continue
        seen.add(gk)
        names = {g.get("home_name", ""), g.get("away_name", "")}
        if {home_name, away_name} != names:
            continue
        hs, as_ = g.get("home_score", 0), g.get("away_score", 0)
        t = hs + as_
        totals.append(t)
        home_wins.append(1 if hs > as_ else 0)
        away_wins.append(1 if as_ > hs else 0)
        bttss.append(1 if hs > 0 and as_ > 0 else 0)

    if len(totals) < 3:
        return None
    n = len(totals)
    return {
        "over05": sum(1 for t in totals if t > 0.5) / n,
        "over15": sum(1 for t in totals if t > 1.5) / n,
        "over25": sum(1 for t in totals if t > 2.5) / n,
        "btts":   sum(bttss) / n,
        "home_w": sum(home_wins) / n,
        "away_w": sum(away_wins) / n,
        "count":  n,
    }


# ═══════════════════════════════════════════════════════════════════════
#  CONFIDENCE ENGINES — per bet type (uses adaptive weights)
# ═══════════════════════════════════════════════════════════════════════

def _xg(home_st, away_st):
    xg_h = 0.55 * home_st["home_avg_scored"] + 0.45 * away_st["away_avg_conceded"]
    xg_a = 0.55 * away_st["away_avg_scored"] + 0.45 * home_st["home_avg_conceded"]
    return max(0.05, xg_h), max(0.05, xg_a)


def compute_over_confidence(
    home_st: Dict, away_st: Dict, line: float,
    h2h: Optional[Dict], bet_type: str
) -> Tuple[float, Dict[str, float], str]:
    """Returns (confidence%, factor_values_dict, reasoning)."""
    xg_h, xg_a = _xg(home_st, away_st)
    total_xg = xg_h + xg_a

    # Factor: Poisson
    pois_p = poisson_over_line(xg_h, xg_a, line)

    # Factor: Historical rate (venue split)
    rate_key = {0.5: "over05_rate", 1.5: "over15_rate", 2.5: "over25_rate"}.get(line, "over25_rate")
    home_rate_key = {0.5: "home_over05_rate", 1.5: "home_over05_rate"}.get(line, "home_over05_rate")
    hist_combined = (
        home_st.get("home_over05_rate" if line <= 0.5 else "over15_rate" if line <= 1.5 else "over25_rate", home_st["over05_rate"]) * 0.5 +
        away_st.get("away_over05_rate" if line <= 0.5 else "over15_rate" if line <= 1.5 else "over25_rate", away_st["over05_rate"]) * 0.5
    )

    # Factor: xG normalised (higher line = higher scale)
    xg_min = {0.5: 0.3, 1.5: 0.8, 2.5: 1.5}.get(line, 1.5)
    xg_max = {0.5: 2.0, 1.5: 3.5, 2.5: 5.0}.get(line, 5.0)
    xg_norm = max(0.0, min(1.0, (total_xg - xg_min) / (xg_max - xg_min)))

    # Factor: BTTS
    btts_combined = (home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2

    # Factor: Form momentum
    form_combined = (home_st["form_score"] + away_st["form_score"]) / 2

    # Factor: Streak
    streak_key = {0.5: "streak_over05", 1.5: "streak_over15", 2.5: "streak_over25"}.get(line, "streak_over25")
    streak_h   = min(1.0, home_st.get(streak_key, 0) / 5.0)
    streak_a   = min(1.0, away_st.get(streak_key, 0) / 5.0)
    streak_val = (streak_h + streak_a) / 2

    # Factor: H2H
    h2h_key = {0.5: "over05", 1.5: "over15", 2.5: "over25"}.get(line, "over25")
    h2h_val = h2h[h2h_key] if h2h else hist_combined

    factors = {
        "poisson_p":  pois_p,
        "hist_rate":  hist_combined,
        "xg_norm":    xg_norm,
        "form":       form_combined,
        "btts":       btts_combined,
        "streak":     streak_val,
        "h2h":        h2h_val,
    }

    weights = get_weights(bet_type)
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))

    reasoning = (
        f"Poisson P(OVER {line}): {pois_p*100:.1f}% · xG {xg_h:.2f}+{xg_a:.2f}={total_xg:.2f} · "
        f"Hist OVER {line}: {hist_combined*100:.0f}% · BTTS: {btts_combined*100:.0f}%"
    )
    if home_st.get(streak_key, 0) >= 3:
        reasoning += f" · Home {home_st[streak_key]}-game OVER streak 🔥"
    if away_st.get(streak_key, 0) >= 3:
        reasoning += f" · Away {away_st[streak_key]}-game OVER streak 🔥"
    if h2h:
        reasoning += f" · H2H({h2h['count']}g) OVER {line}: {h2h[h2h_key]*100:.0f}%"

    return round(confidence, 1), factors, reasoning


def compute_btts_confidence(
    home_st: Dict, away_st: Dict, h2h: Optional[Dict]
) -> Tuple[float, Dict[str, float], str]:
    xg_h, xg_a = _xg(home_st, away_st)

    pois_btts   = poisson_btts(xg_h, xg_a)
    hist_btts   = (home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2
    xg_balance  = min(xg_h, xg_a) / max(xg_h, xg_a) if max(xg_h, xg_a) > 0 else 0.5
    form_comb   = (home_st["form_score"] + away_st["form_score"]) / 2
    h2h_btts    = h2h["btts"] if h2h else hist_btts
    streak_btts = min(1.0, (home_st.get("streak_btts", 0) + away_st.get("streak_btts", 0)) / 6.0)

    factors = {
        "poisson_btts": pois_btts,
        "hist_btts":    hist_btts,
        "xg_balance":   xg_balance,
        "form":         form_comb,
        "h2h":          h2h_btts,
        "streak":       streak_btts,
    }

    weights = get_weights("BTTS_YES")
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))

    reasoning = (
        f"Poisson BTTS: {pois_btts*100:.1f}% · Hist BTTS: {hist_btts*100:.0f}% · "
        f"xG balance: {xg_balance:.2f} · xG {xg_h:.2f} vs {xg_a:.2f}"
    )
    if h2h:
        reasoning += f" · H2H BTTS: {h2h['btts']*100:.0f}%"

    return round(confidence, 1), factors, reasoning


def compute_result_confidence(
    home_st: Dict, away_st: Dict, h2h: Optional[Dict], side: str
) -> Tuple[float, Dict[str, float], str]:
    xg_h, xg_a = _xg(home_st, away_st)

    if side == "HOME":
        pois_p    = poisson_home_win(xg_h, xg_a)
        hist_rate = home_st["wins_rate"] * 0.6 + (1 - away_st["wins_rate"]) * 0.4
        form_diff = max(0.0, min(1.0, 0.5 + (home_st["form_score"] - away_st["form_score"]) / 2))
        xg_diff   = max(0.0, min(1.0, (xg_h - xg_a + 3) / 6))
        h2h_val   = h2h["home_w"] if h2h else hist_rate
        bt        = "HOME_WIN"
    else:
        pois_p    = poisson_away_win(xg_h, xg_a)
        hist_rate = away_st["wins_rate"] * 0.6 + (1 - home_st["wins_rate"]) * 0.4
        form_diff = max(0.0, min(1.0, 0.5 + (away_st["form_score"] - home_st["form_score"]) / 2))
        xg_diff   = max(0.0, min(1.0, (xg_a - xg_h + 3) / 6))
        h2h_val   = h2h["away_w"] if h2h else hist_rate
        bt        = "AWAY_WIN"

    factors = {
        f"poisson_{'hw' if side=='HOME' else 'aw'}": pois_p,
        f"hist_{'hw' if side=='HOME' else 'aw'}":    hist_rate,
        "form_diff": form_diff,
        "xg_diff":   xg_diff,
        "h2h":       h2h_val,
    }

    weights = get_weights(bt)
    # Remap factor keys to match the weights dict
    fmap = {"poisson_hw": "poisson_hw", "poisson_aw": "poisson_aw",
            "hist_hw": "hist_hw", "hist_aw": "hist_aw",
            "form_diff": "form_diff", "xg_diff": "xg_diff", "h2h": "h2h"}
    confidence = sum(factors.get(k, 0.5) * w for k, w in weights.items()) * 100
    confidence = max(0.0, min(99.9, confidence))

    dom_team = home_st if side == "HOME" else away_st
    team_label = "Home" if side == "HOME" else "Away"
    reasoning = (
        f"Poisson {team_label} Win: {pois_p*100:.1f}% · "
        f"Hist Win Rate: {hist_rate*100:.0f}% · "
        f"xG {xg_h:.2f} vs {xg_a:.2f} · Form {team_label}: {dom_team['form_score']:.2f}"
    )
    if h2h:
        hw_key = "home_w" if side == "HOME" else "away_w"
        reasoning += f" · H2H Win: {h2h[hw_key]*100:.0f}%"

    return round(confidence, 1), factors, reasoning


# ═══════════════════════════════════════════════════════════════════════
#  ZEUS MULTI-BET SCANNER v3.0
# ═══════════════════════════════════════════════════════════════════════

def get_card_tier(conf: float, bet_type: str) -> Tuple[str, str]:
    if bet_type in ("BTTS_YES",):
        if conf >= 80: return "elite", "🎯 ELITE BTTS"
        if conf >= 70: return "btts",  "🎯 BTTS LOCK"
        return "btts", "🎯 BTTS"
    if bet_type in ("HOME_WIN", "AWAY_WIN"):
        if conf >= 82: return "elite", f"{'🏠' if bet_type=='HOME_WIN' else '✈️'} ELITE"
        if conf >= 74: return "result", f"{'🏠' if bet_type=='HOME_WIN' else '✈️'} STRONG"
        return "result","RESULT"
    # Goals bets
    if conf >= 80: return "elite",  "🔥 ELITE"
    if conf >= 70: return "strong", "⚡ STRONG"
    return "strong", "✅ CONFIDENT"


@st.cache_data(ttl=300, show_spinner=False)
def scan_all_leagues() -> Tuple[List[Dict], int, int, int]:
    candidates: List[Dict] = []
    leagues_hit = games_eval = data_pts = 0

    for league_id, league_name, flag in LEAGUES:
        events = fetch_scoreboard(league_id)
        if not events:
            continue

        window_games = [
            e for e in events
            if not e.get("completed", False) and in_window(e.get("date", ""))
        ]
        if not window_games:
            continue

        leagues_hit += 1

        for ev in window_games:
            home_sched = fetch_team_schedule(league_id, ev["home_id"], ev["home_name"])
            away_sched = fetch_team_schedule(league_id, ev["away_id"], ev["away_name"])
            data_pts  += len(home_sched) + len(away_sched)

            home_st = team_stats(home_sched, ev["home_name"])
            away_st = team_stats(away_sched, ev["away_name"])
            if home_st is None or away_st is None:
                continue

            games_eval += 1
            h2h = get_h2h_stats(home_sched, away_sched, ev["home_name"], ev["away_name"])
            xg_h, xg_a = _xg(home_st, away_st)
            total_xg    = round(xg_h + xg_a, 2)

            base = {
                "match":       f"{ev['home_name']} vs {ev['away_name']}",
                "home":        ev["home_name"],
                "away":        ev["away_name"],
                "league":      f"{flag} {league_name}",
                "league_id":   league_id,
                "kickoff_utc": ev["date"],
                "kickoff_cat": to_cat(ev["date"]),
                "mins_away":   minutes_to_kickoff(ev["date"]),
                "xg_total":    total_xg,
                "xg_home":     round(xg_h, 2),
                "xg_away":     round(xg_a, 2),
                "home_n":      home_st["n"],
                "away_n":      away_st["n"],
                "home_form":   home_st["form_score"],
                "away_form":   away_st["form_score"],
                "home_btts":   round(home_st["home_btts_rate"] * 100),
                "away_btts":   round(away_st["away_btts_rate"] * 100),
                "h2h_count":   h2h["count"] if h2h else 0,
            }

            # ── Evaluate each bet type ─────────────────────────────
            for bet_type, bt_meta in BET_TYPES.items():
                gate = bt_meta["gate"]

                if bet_type in ("OVER_05", "OVER_15", "OVER_25"):
                    line = bt_meta["line"]
                    conf, factors, reasoning = compute_over_confidence(
                        home_st, away_st, line, h2h, bet_type
                    )
                    pois_p = poisson_over_line(xg_h, xg_a, line)
                    over_rate = (
                        home_st["over05_rate"] if line == 0.5 else
                        home_st["over15_rate"] if line == 1.5 else
                        home_st["over25_rate"]
                    )
                    extra = {
                        "poisson_p":  round(pois_p, 4),
                        "over_rate":  round(over_rate * 100),
                        "streak_val": home_st.get(
                            "streak_over05" if line==0.5 else
                            "streak_over15" if line==1.5 else "streak_over25", 0
                        ),
                    }

                elif bet_type == "BTTS_YES":
                    conf, factors, reasoning = compute_btts_confidence(home_st, away_st, h2h)
                    pois_p = poisson_btts(xg_h, xg_a)
                    extra = {
                        "poisson_p":  round(pois_p, 4),
                        "btts_hist":  round((home_st["home_btts_rate"] + away_st["away_btts_rate"]) / 2 * 100),
                    }

                elif bet_type in ("HOME_WIN", "AWAY_WIN"):
                    side = "HOME" if bet_type == "HOME_WIN" else "AWAY"
                    conf, factors, reasoning = compute_result_confidence(
                        home_st, away_st, h2h, side
                    )
                    pois_p = (poisson_home_win(xg_h, xg_a)
                              if side == "HOME" else poisson_away_win(xg_h, xg_a))
                    extra = {
                        "poisson_p":  round(pois_p, 4),
                        "win_hist":   round((home_st["wins_rate"] if side == "HOME"
                                             else away_st["wins_rate"]) * 100),
                    }

                else:
                    continue

                if conf < gate:
                    continue

                tier, tier_label = get_card_tier(conf, bet_type)

                candidates.append({
                    **base,
                    "bet_type":    bet_type,
                    "bet":         f"{bt_meta['emoji']} {bt_meta['label']}",
                    "confidence":  conf,
                    "tier":        tier,
                    "tier_label":  tier_label,
                    "reasoning":   reasoning,
                    "factors":     factors,
                    **extra,
                })

    # Sort by confidence, deduplicate same match (keep best bet per match)
    candidates.sort(key=lambda x: x["confidence"], reverse=True)
    seen_matches = set()
    top_picks    = []
    for c in candidates:
        mkey = c["match"]
        if mkey not in seen_matches:
            seen_matches.add(mkey)
            top_picks.append(c)
        if len(top_picks) >= TOP_N:
            break

    for i, p in enumerate(top_picks, 1):
        p["rank"] = i
        save_pick(p)

    return top_picks, leagues_hit, games_eval, data_pts


# ═══════════════════════════════════════════════════════════════════════
#  AUTO-GRADER + ADAPTIVE LEARNER
# ═══════════════════════════════════════════════════════════════════════

def grade_and_learn() -> int:
    """
    1. Grade all pending picks against real ESPN scoreboard results.
    2. For each newly graded pick, run adaptive weight update.
    Returns count of newly graded picks.
    """
    conn = get_db()
    try:
        pending = conn.execute(
            "SELECT id, match, league_id, kickoff, bet_type, factors_json FROM picks_log WHERE result='pending'"
        ).fetchall()
    except Exception:
        return 0

    updated = 0
    for row_id, match, league_id, kickoff, bet_type, factors_json_str in pending:
        ko = parse_utc(kickoff)
        if not ko or (now_utc() - ko).total_seconds() < 6000:
            continue
        if not league_id:
            continue

        parts = match.split(" vs ")
        if len(parts) != 2:
            continue
        home_name, away_name = parts[0].strip(), parts[1].strip()

        date_str = ko.strftime("%Y%m%d")
        data = safe_get(f"{ESPN_SOCCER}/{league_id}/scoreboard", params={"dates": date_str})
        if not data:
            continue

        for ev in data.get("events", []):
            comps = ev.get("competitions", [])
            if not comps:
                continue
            comp = comps[0]
            if not comp.get("status", {}).get("type", {}).get("completed", False):
                continue
            competitors = comp.get("competitors", [])
            if len(competitors) < 2:
                continue
            names = {c.get("team", {}).get("displayName", "") for c in competitors}
            if home_name not in names and away_name not in names:
                continue

            home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
            away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])
            hs  = _parse_score(home_c.get("score"))
            as_ = _parse_score(away_c.get("score"))
            tot = hs + as_

            # Grade per bet type
            result = "LOST"
            if not bet_type or bet_type == "OVER_25":
                result = "WON" if tot > 2.5 else "LOST"
            elif bet_type == "OVER_05":
                result = "WON" if tot > 0.5 else "LOST"
            elif bet_type == "OVER_15":
                result = "WON" if tot > 1.5 else "LOST"
            elif bet_type == "BTTS_YES":
                result = "WON" if hs > 0 and as_ > 0 else "LOST"
            elif bet_type == "HOME_WIN":
                result = "WON" if hs > as_ else "LOST"
            elif bet_type == "AWAY_WIN":
                result = "WON" if as_ > hs else "LOST"

            conn.execute(
                "UPDATE picks_log SET result=?,home_score=?,away_score=? WHERE id=?",
                (result, hs, as_, row_id)
            )
            updated += 1

            # ── Adaptive learning ─────────────────────────────────
            try:
                factors = json.loads(factors_json_str or "{}")
                if factors and bet_type:
                    update_weights(bet_type, factors, won=(result == "WON"))
            except Exception:
                pass
            break

    if updated:
        conn.commit()
    return updated


# ═══════════════════════════════════════════════════════════════════════
#  COUNTDOWN HTML
# ═══════════════════════════════════════════════════════════════════════

def countdown_html(kickoff_utc: str, pick_id: str) -> str:
    return f"""
<div id="cd_{pick_id}" class="countdown" style="color:#39ff14;font-size:.85rem;letter-spacing:2px;">
  ⏱ Calculating...
</div>
<script>
(function(){{
  var target = new Date("{kickoff_utc}");
  var el = document.getElementById("cd_{pick_id}");
  function tick(){{
    var now = new Date(), diff = target - now;
    if(diff<=0){{ el.innerHTML="🔴 LIVE NOW"; el.style.color="#ff1744"; return; }}
    var h=Math.floor(diff/3600000), m=Math.floor((diff%3600000)/60000), s=Math.floor((diff%60000)/1000);
    var parts=[]; if(h>0) parts.push(h+"h"); parts.push(("0"+m).slice(-2)+"m"); parts.push(("0"+s).slice(-2)+"s");
    el.innerHTML="⏱ KICKOFF IN "+parts.join(" ");
  }}
  tick(); setInterval(tick,1000);
}})();
</script>
"""


# ═══════════════════════════════════════════════════════════════════════
#  PICK CARD RENDERER v3.0
# ═══════════════════════════════════════════════════════════════════════

def _form_label(score: float) -> str:
    if score >= 0.65: return "🔥 HOT"
    if score <= 0.35: return "❄️ COLD"
    return "➡️ STABLE"


def render_pick_card(pick: Dict):
    tier      = pick["tier"]
    conf      = pick["confidence"]
    bet_type  = pick["bet_type"]
    bt_meta   = BET_TYPES.get(bet_type, BET_TYPES["OVER_25"])
    pick_id   = hashlib.md5(f"{pick['match']}{bet_type}".encode()).hexdigest()[:6]
    bar_w     = min(99, int(conf))
    pois_pct  = pick.get("poisson_p", 0) * 100

    # Bet label CSS class
    bet_css   = f"bet-{bt_meta['css']}"

    # Card tier CSS
    card_css  = f"pick-card {tier}"

    h2h_html  = ""
    if pick.get("h2h_count", 0) > 0 and "h2h" in pick.get("factors", {}):
        h2h_html = f'<span class="pill pill-h2h">H2H({pick["h2h_count"]}g)</span>'

    # Streak pill
    streak_key = {"OVER_05":"streak_over05","OVER_15":"streak_over15","OVER_25":"streak_over25","BTTS_YES":"streak_btts"}.get(bet_type,"")
    streak_html = ""
    if streak_key:
        pass  # streaks embedded in reasoning

    # Learn badge: show if weights have been updated
    conn = get_db()
    updates_row = conn.execute(
        "SELECT SUM(updates) FROM model_weights WHERE bet_type=?", (bet_type,)
    ).fetchone()
    total_updates = int(updates_row[0] or 0) if updates_row else 0
    learn_html = f'<span class="pill pill-learn">🧠 AI LEARNT {total_updates} PICKS</span>' if total_updates > 0 else ""

    card_html = f"""
<div class="{card_css}">
  <div class="rank-badge">#{pick['rank']}</div>
  <div class="card-league">{pick['league']}</div>
  <div class="card-teams">{pick['home']} <span class="card-vs">vs</span> {pick['away']}</div>
  <div class="card-bet {bet_css}">{pick['bet']}</div>

  <div class="conf-row">
    <span class="conf-pct {tier}">{conf:.1f}%</span>
    <span class="tier-chip {tier}">{pick['tier_label']}</span>
  </div>
  <div class="conf-track">
    <div class="conf-fill {tier}" style="width:{bar_w}%;"></div>
  </div>

  <div class="ai-grid">
    <div class="ai-factor">
      <span class="ai-factor-val cyan">{pois_pct:.1f}%</span>
      <div class="ai-factor-lbl">Poisson P</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val gold">{pick['xg_total']:.2f}</span>
      <div class="ai-factor-lbl">xG Total</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val">{pick['home_btts']:.0f}/{pick['away_btts']:.0f}%</span>
      <div class="ai-factor-lbl">BTTS%</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val">{_form_label(pick['home_form'])}</span>
      <div class="ai-factor-lbl">Home Form</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val">{_form_label(pick['away_form'])}</span>
      <div class="ai-factor-lbl">Away Form</div>
    </div>
    <div class="ai-factor">
      <span class="ai-factor-val purple">{pick['home_n']}+{pick['away_n']}</span>
      <div class="ai-factor-lbl">Games Data</div>
    </div>
  </div>

  <div class="pills-row">
    <span class="pill pill-time">{pick['kickoff_cat']}</span>
    <span class="pill pill-xg">xG: {pick['xg_home']:.2f}+{pick['xg_away']:.2f}</span>
    {h2h_html}
    {learn_html}
  </div>

  <div class="card-reason">{pick['reasoning']}</div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)
    # Countdown timer (use st.html as replacement for deprecated components.v1.html)
    try:
        st.html(countdown_html(pick["kickoff_utc"], pick_id))
    except Exception:
        try:
            import streamlit.components.v1 as components
            components.html(countdown_html(pick["kickoff_utc"], pick_id), height=28)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════
#  LIVE MATCH ENGINE
# ═══════════════════════════════════════════════════════════════════════

# ESPN status names for in-progress games
_LIVE_STATUSES = {"STATUS_IN_PROGRESS", "in", "STATUS_HALFTIME", "STATUS_END_PERIOD",
                  "STATUS_OVERTIME", "2nd Half", "1st Half", "Half Time", "HT",
                  "in progress", "In Progress"}

def fetch_live_scoreboard(league_id: str) -> List[Dict]:
    """
    Fetch currently LIVE (in-progress) games for a league from ESPN API.
    Returns enriched event dicts with current score + game clock.
    """
    date_str = now_utc().strftime("%Y%m%d")
    data = safe_get(
        f"{ESPN_SOCCER}/{league_id}/scoreboard",
        params={"dates": date_str},
        timeout=8,
    )
    if not data:
        return []

    live_events = []
    for ev in data.get("events", []):
        comps = ev.get("competitions", [])
        if not comps:
            continue
        comp = comps[0]
        status_obj  = comp.get("status", {})
        status_type = status_obj.get("type", {})
        status_name = status_type.get("name", "")
        status_desc = status_type.get("shortDetail", status_obj.get("displayClock", ""))
        completed   = status_type.get("completed", False)
        state       = status_type.get("state", "")          # pre / in / post

        # Accept "in" state OR known live status names
        is_live = (
            state == "in"
            or status_name in _LIVE_STATUSES
            or any(s in status_name for s in ("PROGRESS", "HALF", "PERIOD", "OVERTIME"))
        )
        if not is_live or completed:
            continue

        competitors = comp.get("competitors", [])
        if len(competitors) < 2:
            continue

        home_c = next((c for c in competitors if c.get("homeAway") == "home"), competitors[0])
        away_c = next((c for c in competitors if c.get("homeAway") == "away"), competitors[1])

        hs  = _parse_score(home_c.get("score"))
        as_ = _parse_score(away_c.get("score"))

        # Game clock — ESPN embeds in displayClock or status detail
        clock       = status_obj.get("displayClock", "")
        period      = status_obj.get("period", 0)
        is_halftime = "HALF" in status_name.upper() or "HT" in status_name

        live_events.append({
            "event_id":    ev.get("id", ""),
            "date":        ev.get("date", ""),
            "home_id":     str(home_c.get("team", {}).get("id", "")),
            "home_name":   home_c.get("team", {}).get("displayName", ""),
            "away_id":     str(away_c.get("team", {}).get("id", "")),
            "away_name":   away_c.get("team", {}).get("displayName", ""),
            "home_score":  hs,
            "away_score":  as_,
            "total_goals": hs + as_,
            "clock":       clock,
            "period":      period,
            "is_halftime": is_halftime,
            "status_name": status_name,
            "status_desc": status_desc,
            "league_id":   league_id,
        })
    return live_events


def _in_game_over_confidence(
    pre_conf: float,
    goals_scored: int,
    line: float,
    clock: str,
    period: int,
    is_halftime: bool,
) -> Tuple[float, str]:
    """
    Adjust pre-match Over confidence based on current in-game state.
    Returns (adjusted_confidence%, edge_note).
    """
    # Already hit
    if goals_scored > line:
        return 99.9, f"✅ ALREADY {goals_scored} goals scored — BET LANDED"

    goals_needed = int(line - goals_scored) + 1   # e.g. Over 2.5 needs 3 total

    # Estimate minutes played from clock / period
    try:
        mins_played = int(float(clock.replace("'", "").strip())) if clock and clock not in ("", "0:00") else 0
    except Exception:
        mins_played = 45 if is_halftime else (45 if period == 1 else 70 if period == 2 else 0)

    mins_remaining = max(1, 90 - mins_played)

    # Rough Poisson rate: ~2.7 goals/90min on avg → rate per minute
    base_rate = pre_conf / 100           # pre-match probability used as proxy
    time_left  = mins_remaining / 90.0

    # Bayesian-ish update: P(≥k more goals | time_left, base_rate)
    if goals_needed <= 0:
        adj = 99.9
        note = "BET ALREADY WON"
    else:
        # Approximate: scale probability by remaining time fraction raised by goals needed
        scaling = time_left ** goals_needed
        adj = min(99.9, max(1.0, pre_conf * scaling * (1 + goals_scored * 0.15)))
        note = (
            f"Need {goals_needed} more goal(s) · ~{mins_remaining}' remaining · "
            f"Pre-match model: {pre_conf:.0f}%"
        )

    return round(adj, 1), note


@st.cache_data(ttl=30, show_spinner=False)   # 30-second cache for live data
def scan_live_matches() -> Tuple[List[Dict], int]:
    """
    Scan all leagues for currently live games.
    Returns (live_match_predictions, live_match_count).
    """
    live_results: List[Dict] = []
    total_live = 0

    for league_id, league_name, flag in LEAGUES:
        live_events = fetch_live_scoreboard(league_id)
        if not live_events:
            continue

        total_live += len(live_events)

        for ev in live_events:
            # Fetch team history for predictions
            home_sched = fetch_team_schedule(league_id, ev["home_id"], ev["home_name"])
            away_sched = fetch_team_schedule(league_id, ev["away_id"], ev["away_name"])

            home_st = team_stats(home_sched, ev["home_name"]) if home_sched else None
            away_st = team_stats(away_sched, ev["away_name"]) if away_sched else None

            h2h     = get_h2h_stats(home_sched, away_sched, ev["home_name"], ev["away_name"]) \
                      if home_sched and away_sched else None

            # Compute pre-match predictions (reuse full engine)
            predictions: List[Dict] = []
            if home_st and away_st:
                xg_h, xg_a = _xg(home_st, away_st)
                total_xg   = round(xg_h + xg_a, 2)

                for bet_type, bt_meta in BET_TYPES.items():
                    if bet_type in ("OVER_05", "OVER_15", "OVER_25"):
                        line = bt_meta["line"]
                        pre_conf, factors, reasoning = compute_over_confidence(
                            home_st, away_st, line, h2h, bet_type
                        )
                        adj_conf, edge_note = _in_game_over_confidence(
                            pre_conf, ev["total_goals"], line,
                            ev["clock"], ev["period"], ev["is_halftime"]
                        )
                        already_hit = ev["total_goals"] > line
                        predictions.append({
                            "bet_type":   bet_type,
                            "label":      bt_meta["label"],
                            "emoji":      bt_meta["emoji"],
                            "css":        bt_meta["css"],
                            "pre_conf":   pre_conf,
                            "live_conf":  adj_conf,
                            "already_hit": already_hit,
                            "edge_note":  edge_note,
                            "reasoning":  reasoning,
                        })

                    elif bet_type == "BTTS_YES":
                        pre_conf, factors, reasoning = compute_btts_confidence(home_st, away_st, h2h)
                        # BTTS already done if both scored
                        already_hit = ev["home_score"] > 0 and ev["away_score"] > 0
                        # One team scored — still needs other
                        one_scored  = (ev["home_score"] > 0) != (ev["away_score"] > 0)
                        try:
                            mins_played = int(float(ev["clock"].replace("'","").strip())) if ev["clock"] else 0
                        except Exception:
                            mins_played = 45 if ev["is_halftime"] else 70
                        mins_remaining = max(1, 90 - mins_played)
                        if already_hit:
                            adj_conf = 99.9
                            edge_note = "✅ BOTH TEAMS SCORED — BET LANDED"
                        elif one_scored:
                            # One team scored; need the other in remaining time
                            adj_conf = round(min(99.9, pre_conf * (mins_remaining / 90) * 1.4), 1)
                            edge_note = f"1 team scored ✓ · Other needs to score · ~{mins_remaining}' left"
                        else:
                            adj_conf = round(min(99.9, pre_conf * (mins_remaining / 90) ** 2 * 1.2), 1)
                            edge_note = f"No goals yet · Need 2 teams to score · ~{mins_remaining}' left"

                        predictions.append({
                            "bet_type":    "BTTS_YES",
                            "label":       bt_meta["label"],
                            "emoji":       bt_meta["emoji"],
                            "css":         "btts",
                            "pre_conf":    pre_conf,
                            "live_conf":   adj_conf,
                            "already_hit": already_hit,
                            "edge_note":   edge_note,
                            "reasoning":   reasoning,
                        })

                    elif bet_type in ("HOME_WIN", "AWAY_WIN"):
                        side = "HOME" if bet_type == "HOME_WIN" else "AWAY"
                        pre_conf, factors, reasoning = compute_result_confidence(
                            home_st, away_st, h2h, side
                        )
                        hs, as_ = ev["home_score"], ev["away_score"]
                        currently_winning = (side == "HOME" and hs > as_) or (side == "AWAY" and as_ > hs)
                        try:
                            mins_played = int(float(ev["clock"].replace("'","").strip())) if ev["clock"] else 0
                        except Exception:
                            mins_played = 45 if ev["is_halftime"] else 70
                        mins_remaining = max(1, 90 - mins_played)
                        time_factor = mins_remaining / 90

                        if currently_winning:
                            # Winning: confidence increases as game nears end
                            adj_conf = round(min(99.9, pre_conf + (1 - time_factor) * (99.9 - pre_conf) * 0.55), 1)
                            edge_note = f"{'🏠' if side=='HOME' else '✈️'} Currently WINNING · {mins_remaining}' left"
                        elif (side == "HOME" and as_ > hs) or (side == "AWAY" and hs > as_):
                            # Losing
                            adj_conf = round(max(1.0, pre_conf * time_factor * 0.6), 1)
                            edge_note = f"Currently LOSING · {mins_remaining}' remaining"
                        else:
                            # Draw
                            adj_conf = round(min(99.9, pre_conf * (0.7 + time_factor * 0.3)), 1)
                            edge_note = f"Score level · {mins_remaining}' remaining · Outcome open"

                        predictions.append({
                            "bet_type":    bet_type,
                            "label":       bt_meta["label"],
                            "emoji":       bt_meta["emoji"],
                            "css":         "result" if bet_type == "HOME_WIN" else "away",
                            "pre_conf":    pre_conf,
                            "live_conf":   adj_conf,
                            "already_hit": False,
                            "edge_note":   edge_note,
                            "reasoning":   reasoning,
                        })
            else:
                xg_h = xg_a = total_xg = 0.0

            # Sort predictions by live_conf descending
            predictions.sort(key=lambda p: p["live_conf"], reverse=True)

            live_results.append({
                **ev,
                "league":      f"{flag} {league_name}",
                "league_id":   league_id,
                "predictions": predictions,
                "xg_home":     round(xg_h, 2) if home_st and away_st else 0.0,
                "xg_away":     round(xg_a, 2) if home_st and away_st else 0.0,
                "xg_total":    total_xg if home_st and away_st else 0.0,
                "has_model":   home_st is not None and away_st is not None,
            })

    # Sort by total goals (most goals first), then by live_conf of top prediction
    live_results.sort(
        key=lambda x: (
            x["total_goals"],
            x["predictions"][0]["live_conf"] if x["predictions"] else 0
        ),
        reverse=True,
    )
    return live_results, total_live


def render_live_card(match: Dict, idx: int):
    """Render a single live match card with score + AI predictions."""
    hs          = match["home_score"]
    as_         = match["away_score"]
    clock       = match.get("clock", "")
    is_halftime = match.get("is_halftime", False)
    has_model   = match.get("has_model", False)

    # Clock display
    if is_halftime:
        clock_html = '<span class="halftime-chip">⏸ HALF TIME</span>'
    elif clock:
        clock_html = f'<span class="live-clock">⏱ {clock}</span>'
    else:
        clock_html = '<span class="live-clock">🔴 LIVE</span>'

    # Top predictions to show (max 3 bet cells)
    preds = match.get("predictions", [])
    pred_cells_html = ""
    if preds:
        shown = preds[:3]
        for p in shown:
            hit_class  = "hit" if p["already_hit"] else ""
            edge_class = "live-edge" if p["live_conf"] >= 70 and not p["already_hit"] else ""
            cell_class = hit_class or edge_class
            color_map  = {
                "over05": "var(--cyan)", "over15": "var(--green)", "over25": "var(--gold)",
                "btts":   "var(--purple)", "result": "var(--cyan)", "away": "var(--orange)",
                "home":   "var(--green2)",
            }
            color = color_map.get(p["css"], "var(--green)")
            val_display = "✅ HIT" if p["already_hit"] else f"{p['live_conf']:.0f}%"
            pred_cells_html += f"""
<div class="pred-cell {cell_class}">
  <span class="pred-val" style="color:{color};">{val_display}</span>
  <div class="pred-lbl">{p['emoji']} {p['label']}</div>
</div>"""
    else:
        pred_cells_html = '<div style="color:var(--muted);font-size:.8rem;padding:8px;">No model data — insufficient team history</div>'

    # Full prediction rows for top pick
    top_edge_note = preds[0]["edge_note"] if preds else ""
    top_reasoning = preds[0]["reasoning"] if preds else "Insufficient data to model this match."

    card_id = f"live_{idx}"
    card_html = f"""
<div class="live-card" id="{card_id}">
  <div class="live-header">
    <div>
      <span class="live-pulse"></span>
      <span style="font-family:'Barlow Condensed',sans-serif;font-size:.72rem;color:var(--muted);letter-spacing:2px;text-transform:uppercase;">{match['league']}</span>
    </div>
    <div style="display:flex;gap:8px;align-items:center;">
      {clock_html}
      <span class="live-badge">🔴 LIVE</span>
    </div>
  </div>

  <div class="live-score-block">
    <div class="live-team-name">{match['home_name']}</div>
    <span class="live-score">{hs} <span class="live-sep">-</span> {as_}</span>
    <div class="live-team-name">{match['away_name']}</div>
  </div>

  <div style="text-align:center;margin-bottom:10px;">
    <span style="font-family:'Barlow Condensed',sans-serif;font-size:.72rem;color:var(--muted);letter-spacing:2px;">
      {'🎯 ZEUS AI MODEL ACTIVE' if has_model else '⚠️ LIVE SCORE ONLY — INSUFFICIENT HISTORY FOR MODEL'}
    </span>
  </div>

  <div class="pred-grid">
    {pred_cells_html}
  </div>

  {'<div class="live-reason">🤖 <strong>Live Edge:</strong> ' + top_edge_note + '<br>' + top_reasoning + '</div>' if has_model else ''}
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
#  MAIN APP
# ═══════════════════════════════════════════════════════════════════════

def main():
    # ── Auto-refresh every 60 seconds (fully automated) ───────────────
    try:
        from streamlit_autorefresh import st_autorefresh
        count = st_autorefresh(interval=60_000, key="zeus_v3_refresh")
    except ImportError:
        count = 0

    # ── Hero ──────────────────────────────────────────────────────────
    st.markdown("""
<div class="zeus-hero">
  <span class="zeus-logo">⚡ ZEUS</span>
  <div class="zeus-tagline">Neural Football Intelligence · Multi-Bet · Adaptive AI Learning</div>
  <div class="zeus-version">
    v3.0 · OVER 0.5/1.5/2.5 · BTTS · Home/Away Win · 75+ Leagues · Multi-API · Self-Learning
  </div>
  <div class="zeus-bar"></div>
</div>
""", unsafe_allow_html=True)

    # ── Auto-grade + learn on every refresh ───────────────────────────
    newly_graded = grade_and_learn()

    # ── Tabs ──────────────────────────────────────────────────────────
    tab_picks, tab_live, tab_results, tab_brain, tab_about = st.tabs([
        "🎯 Top Picks",
        "🔴 Live Matches",
        "🏆 Results",
        "🧠 AI Brain",
        "🌍 System",
    ])

    # ══════════════════════════════════════════════════════════════════
    #  TAB 1 — TOP PICKS
    # ══════════════════════════════════════════════════════════════════
    with tab_picks:
        now_cat = (now_utc() + CAT_OFFSET).strftime("%d %b %Y · %H:%M CAT")
        st.caption(
            f"🕐 {now_cat} &nbsp;·&nbsp; Scanning games in the next {WINDOW_HOURS}h "
            f"&nbsp;·&nbsp; Auto-refresh every 60s &nbsp;·&nbsp; Scan #{count or '—'}"
        )
        if newly_graded:
            st.toast(f"🧠 Zeus learned from {newly_graded} graded pick(s)!", icon="⚡")

        with st.spinner(""):
            st.markdown(
                '<div class="scan-line">⚡ ZEUS v3.0 SCANNING 75+ LEAGUES — MULTI-BET INTELLIGENCE ⚡</div>',
                unsafe_allow_html=True
            )
            picks, leagues_hit, games_eval, data_pts = scan_all_leagues()

        # Metrics
        elite_cnt  = sum(1 for p in picks if p["tier"] == "elite")
        goals_cnt  = sum(1 for p in picks if "OVER" in p.get("bet_type", ""))
        btts_cnt   = sum(1 for p in picks if p.get("bet_type") == "BTTS_YES")
        result_cnt = sum(1 for p in picks if p.get("bet_type") in ("HOME_WIN", "AWAY_WIN"))

        st.markdown(f"""
<div class="metrics-row">
  <div class="metric-box"><span class="metric-val">{len(picks)}</span><div class="metric-lbl">Picks Today</div></div>
  <div class="metric-box"><span class="metric-val gold">{elite_cnt}</span><div class="metric-lbl">🔥 Elite</div></div>
  <div class="metric-box"><span class="metric-val">{goals_cnt}</span><div class="metric-lbl">⚽ Goals</div></div>
  <div class="metric-box"><span class="metric-val purple">{btts_cnt}</span><div class="metric-lbl">🎯 BTTS</div></div>
  <div class="metric-box"><span class="metric-val cyan">{result_cnt}</span><div class="metric-lbl">🏠✈️ Result</div></div>
  <div class="metric-box"><span class="metric-val">{leagues_hit}</span><div class="metric-lbl">Leagues Hit</div></div>
  <div class="metric-box"><span class="metric-val">{games_eval}</span><div class="metric-lbl">Games Eval</div></div>
  <div class="metric-box"><span class="metric-val cyan">{data_pts:,}</span><div class="metric-lbl">Data Points</div></div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        if not picks:
            st.markdown("""
<div class="no-picks">
  <span class="no-picks-icon">⏳</span>
  No games meet Zeus's confidence thresholds in the next 24 hours.<br>
  Zeus only shows picks with <strong>90%+ confidence</strong> for OVER 0.5 · 
  <strong>78%+</strong> for OVER 1.5 · <strong>65%+</strong> for OVER 2.5 · 
  <strong>70%+</strong> for BTTS · <strong>74%+</strong> for Match Result.<br>
  Continuously scanning — check back as fixtures enter the window.
</div>
""", unsafe_allow_html=True)
        else:
            cols = st.columns(3)
            cols[0].markdown(
                '<span style="font-family:Barlow Condensed;color:#ffb300;font-size:.85rem;">'
                '🔥 ELITE — Exceptional multi-model edge</span>', unsafe_allow_html=True)
            cols[1].markdown(
                '<span style="font-family:Barlow Condensed;color:#39ff14;font-size:.85rem;">'
                '⚡ STRONG — Clear statistical signal</span>', unsafe_allow_html=True)
            cols[2].markdown(
                '<span style="font-family:Barlow Condensed;color:#ea80fc;font-size:.85rem;">'
                '🎯 BTTS / ✈️ RESULT — Loophole bets (high confidence only)</span>',
                unsafe_allow_html=True)
            st.markdown("---")
            for pick in picks:
                render_pick_card(pick)

    # ══════════════════════════════════════════════════════════════════
    #  TAB 2 — LIVE MATCHES
    # ══════════════════════════════════════════════════════════════════
    with tab_live:
        now_cat_live = (now_utc() + CAT_OFFSET).strftime("%d %b %Y · %H:%M CAT")
        st.caption(
            f"🕐 {now_cat_live} &nbsp;·&nbsp; "
            "Live scores & AI predictions updated every 30s &nbsp;·&nbsp; "
            "All 75+ leagues monitored"
        )

        st.markdown(
            '<div class="scan-line">🔴 ZEUS LIVE INTELLIGENCE — IN-PLAY SCORE + AI PREDICTION ENGINE 🔴</div>',
            unsafe_allow_html=True,
        )

        with st.spinner(""):
            live_matches, total_live = scan_live_matches()

        # ── Live metrics ──────────────────────────────────────────────
        goals_live   = sum(m["total_goals"] for m in live_matches)
        hit_cnt      = sum(
            1 for m in live_matches
            for p in m.get("predictions", [])
            if p.get("already_hit")
        )
        edge_cnt     = sum(
            1 for m in live_matches
            if m.get("predictions") and m["predictions"][0]["live_conf"] >= 70
        )

        st.markdown(f"""
<div class="metrics-row">
  <div class="metric-box"><span class="metric-val red">{len(live_matches)}</span><div class="metric-lbl">🔴 Live Games</div></div>
  <div class="metric-box"><span class="metric-val gold">{goals_live}</span><div class="metric-lbl">⚽ Goals Scored</div></div>
  <div class="metric-box"><span class="metric-val">{hit_cnt}</span><div class="metric-lbl">✅ Bets Landed</div></div>
  <div class="metric-box"><span class="metric-val cyan">{edge_cnt}</span><div class="metric-lbl">⚡ Live Edges 70%+</div></div>
  <div class="metric-box"><span class="metric-val purple">{total_live}</span><div class="metric-lbl">Total Live Found</div></div>
</div>
""", unsafe_allow_html=True)

        st.markdown("---")

        # ── Legend ────────────────────────────────────────────────────
        c1, c2, c3 = st.columns(3)
        c1.markdown(
            '<span style="font-family:Barlow Condensed;color:#ff1744;font-size:.82rem;">'
            '🔴 LIVE — Game currently in progress</span>', unsafe_allow_html=True)
        c2.markdown(
            '<span style="font-family:Barlow Condensed;color:#39ff14;font-size:.82rem;">'
            '✅ HIT — Bet condition already met in-game</span>', unsafe_allow_html=True)
        c3.markdown(
            '<span style="font-family:Barlow Condensed;color:#ffb300;font-size:.82rem;">'
            '⚡ LIVE EDGE — Zeus sees 70%+ live confidence</span>', unsafe_allow_html=True)
        st.markdown("---")

        # ── Auto-refresh note ─────────────────────────────────────────
        st.info(
            "ℹ️ Live data refreshes every 30 seconds automatically. "
            "Predictions are adjusted in real-time based on current score, "
            "game clock, and Zeus's pre-match statistical model. "
            "**Green bordered cells = live edge ≥70% · Gold cells = already HIT.**",
            icon="⚡",
        )

        if not live_matches:
            st.markdown("""
<div class="live-empty">
  <span style="font-size:3rem;display:block;margin-bottom:12px;">📡</span>
  No live games detected across 75+ leagues right now.<br>
  Zeus continuously monitors all leagues — check back when matches are in progress.<br>
  <span style="font-size:.8rem;margin-top:8px;display:block;opacity:.6;">
    Live detection requires ESPN API to report in-progress status.
  </span>
</div>
""", unsafe_allow_html=True)
        else:
            # Group by league
            leagues_seen: Dict[str, List[Dict]] = {}
            for m in live_matches:
                lg = m["league"]
                leagues_seen.setdefault(lg, []).append(m)

            for league_name, matches in leagues_seen.items():
                st.markdown(
                    f'<div style="font-family:Barlow Condensed;font-size:.78rem;'
                    f'letter-spacing:3px;text-transform:uppercase;color:var(--muted);'
                    f'margin:18px 0 4px;border-bottom:1px solid var(--border);'
                    f'padding-bottom:4px;">{league_name}</div>',
                    unsafe_allow_html=True,
                )
                for idx, match in enumerate(matches):
                    render_live_card(match, idx)

    # ══════════════════════════════════════════════════════════════════
    #  TAB 3 — RESULTS
    # ══════════════════════════════════════════════════════════════════
    with tab_results:
        st.subheader("🏆 Zeus Pick Results — Auto-Graded")
        if newly_graded:
            st.success(f"✅ {newly_graded} new pick(s) graded & learned from this refresh.")

        try:
            conn = get_db()
            rows = conn.execute("""
                SELECT match, league, bet, bet_type, xg_total, confidence,
                       kickoff, result, home_score, away_score, logged_at
                FROM picks_log ORDER BY logged_at DESC LIMIT 500
            """).fetchall()

            if not rows:
                st.info("No picks logged yet — visit 🎯 Top Picks to generate predictions.")
            else:
                df = pd.DataFrame(rows, columns=[
                    "Match","League","Bet","Bet Type","xG","Conf%",
                    "Kickoff UTC","Result","Home Score","Away Score","Logged"
                ])
                df["Conf%"] = df["Conf%"].apply(lambda x: f"{x:.1f}%")
                df["xG"]    = df["xG"].apply(lambda x: f"{x:.2f}")

                won   = df[df["Result"] == "WON"]
                lost  = df[df["Result"] == "LOST"]
                pend  = df[df["Result"] == "pending"]
                tot   = len(won) + len(lost)
                wr    = f"{len(won)/tot*100:.1f}%" if tot > 0 else "—"

                c1,c2,c3,c4,c5 = st.columns(5)
                c1.metric("✅ Won",       len(won))
                c2.metric("❌ Lost",      len(lost))
                c3.metric("⏳ Pending",   len(pend))
                c4.metric("Total Graded", tot)
                c5.metric("Win Rate",     wr)

                # Win rate per bet type
                if tot > 0:
                    st.markdown("**Win Rate by Bet Type**")
                    graded = df[df["Result"].isin(["WON","LOST"])]
                    for bt in BET_TYPES.keys():
                        bdf = graded[graded["Bet Type"] == bt]
                        if bdf.empty:
                            continue
                        bw  = len(bdf[bdf["Result"] == "WON"])
                        bwr = f"{bw/len(bdf)*100:.0f}%"
                        st.markdown(
                            f"**{BET_TYPES[bt]['emoji']} {BET_TYPES[bt]['label']}**: "
                            f"{bw}/{len(bdf)} won ({bwr})",
                            unsafe_allow_html=True
                        )

                st.divider()
                st.markdown("### ✅ Correct Picks")
                if won.empty:
                    st.info("No graded wins yet — picks auto-graded ~100 min after kickoff.")
                else:
                    for _, r in won.iterrows():
                        score_str = (f" | Score: {int(r['Home Score'])}-{int(r['Away Score'])}"
                                     if r['Home Score'] >= 0 else "")
                        st.markdown(
                            f"⚽ **{r['Match']}** · {r['League']} · **{r['Bet']}** · "
                            f"xG: {r['xG']} · Conf: **{r['Conf%']}**{score_str} · "
                            f"<span style='color:#39ff14;font-weight:700;'>WON ✅</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                st.markdown("### ❌ Missed Picks")
                if lost.empty:
                    st.info("No missed picks yet.")
                else:
                    for _, r in lost.iterrows():
                        score_str = (f" | Score: {int(r['Home Score'])}-{int(r['Away Score'])}"
                                     if r['Home Score'] >= 0 else "")
                        st.markdown(
                            f"⚽ **{r['Match']}** · {r['League']} · **{r['Bet']}** · "
                            f"xG: {r['xG']} · Conf: **{r['Conf%']}**{score_str} · "
                            f"<span style='color:#ff1744;font-weight:700;'>MISSED ❌</span>",
                            unsafe_allow_html=True
                        )
                        st.divider()

                if not pend.empty:
                    with st.expander(f"⏳ Pending — {len(pend)} picks awaiting results"):
                        st.dataframe(
                            pend[["Match","League","Bet","Conf%","Kickoff UTC"]],
                            hide_index=True, width="stretch"
                        )
        except Exception as e:
            st.info(f"Results log unavailable: {e}")

    # ══════════════════════════════════════════════════════════════════
    #  TAB 4 — AI BRAIN
    # ══════════════════════════════════════════════════════════════════
    with tab_brain:
        st.subheader("🧠 Zeus Adaptive Intelligence — Live Weight Tracker")
        st.markdown(
            "Zeus automatically adjusts its prediction weights after every graded pick. "
            "Winning picks reinforce high-contributing factors. Losing picks reduce them. "
            "The model evolves continuously — no human input required."
        )

        try:
            conn = get_db()
            rows = conn.execute(
                "SELECT bet_type, factor, weight, wins, losses, updates FROM model_weights ORDER BY bet_type, weight DESC"
            ).fetchall()
            if rows:
                df_w = pd.DataFrame(rows, columns=["Bet Type","Factor","Weight","Wins","Losses","Updates"])
                df_w["Weight"] = df_w["Weight"].apply(lambda x: f"{x*100:.1f}%")

                for bt in BET_TYPES.keys():
                    bdf = df_w[df_w["Bet Type"] == bt]
                    if bdf.empty:
                        continue
                    total_upd = bdf["Updates"].astype(int).sum()
                    total_w   = bdf["Wins"].astype(int).sum()
                    total_l   = bdf["Losses"].astype(int).sum()
                    with st.expander(
                        f"{BET_TYPES[bt]['emoji']} {BET_TYPES[bt]['label']} — "
                        f"{total_upd} total updates · {total_w}W / {total_l}L"
                    ):
                        st.dataframe(
                            bdf[["Factor","Weight","Wins","Losses","Updates"]],
                            hide_index=True, width="stretch"
                        )
            else:
                st.info("No weight data yet — weights initialize on first scan.")
        except Exception as e:
            st.info(f"Weight data unavailable: {e}")

        st.divider()
        st.markdown("**Confidence Gates (minimum to be shown)**")
        for bt, meta in BET_TYPES.items():
            st.markdown(f"**{meta['emoji']} {meta['label']}**: ≥ {meta['gate']}%")

        st.divider()
        st.markdown("**Learning Parameters**")
        st.markdown(f"- Learning rate: `{LEARNING_RATE}` (nudge per graded pick)")
        st.markdown("- Signal: `+1.0` for WON · `-0.5` for LOST (asymmetric — learn more from wins)")
        st.markdown("- Weights auto-normalized to sum to 1.0 after each update")
        st.markdown("- Updates fire automatically every refresh cycle")

    # ══════════════════════════════════════════════════════════════════
    #  TAB 5 — SYSTEM INFO
    # ══════════════════════════════════════════════════════════════════
    with tab_about:
        st.subheader("🌍 Zeus Neural System v3.0 — Architecture")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Prediction Engine — v3.0**

**Multi-Bet Coverage:**
- OVER 0.5 Goals (gate: 88%+) — near-certainty there will be at least 1 goal
- OVER 1.5 Goals (gate: 78%+) — high confidence 2+ goals
- OVER 2.5 Goals (gate: 65%+) — strong case for open game
- BTTS (gate: 70%+) — both teams likely to score
- Home Win (gate: 74%+) — dominant home advantage
- Away Win (gate: 74%+) — dominant away team

**Statistical Models:**
- Bivariate Poisson Distribution
- Dixon-Coles xG (venue-split)
- Historical Rate Analysis (home-at-home / away-away)
- Head-to-Head Extraction
- Form Momentum (last 3/5/full)
- Streak Detection (consecutive OVER / BTTS)

**Data Sources:**
- ESPN Soccer API (primary, free, no key)
- TheSportsDB (supplement for thin leagues, free key)
- 75+ leagues worldwide

**Automation:**
- Auto-scan every 60 seconds
- Auto-grade ~100 min after kickoff
- Auto-learn from every graded pick
- Zero human interaction required
""")
        with col2:
            st.markdown("**Bet Confidence Gates**")
            for bt, meta in BET_TYPES.items():
                st.markdown(f"**{meta['emoji']} {meta['label']}**: ≥ {meta['gate']}%")
            st.divider()
            st.markdown("**OVER Thresholds vs Base Rates**")
            st.markdown("OVER 0.5: ~75% base rate → Zeus shows ≥88% only")
            st.markdown("OVER 1.5: ~60% base rate → Zeus shows ≥78% only")
            st.markdown("OVER 2.5: ~50% base rate → Zeus shows ≥65% only")
            st.markdown("BTTS: ~50% base rate → Zeus shows ≥70% only")
            st.markdown("1X2: ~45%/27%/28% → Zeus shows ≥74% only")

        st.divider()
        st.subheader("75+ Leagues Monitored")
        league_data = []
        for lid, lname, flag in LEAGUES:
            region = lid.split(".")[0].upper()
            league_data.append({"Flag": flag, "League": lname, "Region": region, "ID": lid})
        st.dataframe(pd.DataFrame(league_data), hide_index=True, width="stretch")


if __name__ == "__main__":
    main()
