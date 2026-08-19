"""NetGraph Studio presentation layer.

UI-only helpers: no City2Graph computation is performed here.
"""

import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
<style>
:root { --ng-radius: 14px; }
.block-container { max-width: 1480px; padding-top: 1rem; padding-bottom: 2.5rem; }
.ng-shell { animation: ngFade .28s ease-out; }
@keyframes ngFade { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
.ng-header { display:flex; align-items:center; justify-content:space-between; gap:18px; padding:16px 20px; margin-bottom:16px; border:1px solid rgba(128,128,128,.20); border-radius:var(--ng-radius); background:linear-gradient(120deg, rgba(128,128,128,.08), rgba(128,128,128,.025)); }
.ng-brand { font-size:1.55rem; font-weight:800; letter-spacing:-.035em; }
.ng-sub { color:rgba(128,128,128,.92); font-size:.86rem; margin-top:3px; }
.ng-badge { border:1px solid rgba(128,128,128,.28); border-radius:999px; padding:6px 11px; font-size:.74rem; white-space:nowrap; }
.ng-section { font-size:.94rem; font-weight:750; margin:12px 0 7px; }
.ng-help { color:rgba(128,128,128,.9); font-size:.82rem; margin:0 0 10px; }
.ng-step { display:inline-flex; align-items:center; justify-content:center; min-width:27px; height:27px; margin-right:7px; border:1px solid rgba(128,128,128,.28); border-radius:50%; font-size:.72rem; font-weight:800; }
.ng-status { display:flex; align-items:center; gap:7px; padding:8px 11px; border:1px solid rgba(128,128,128,.18); border-radius:10px; font-size:.78rem; }
.ng-dot { width:8px; height:8px; border-radius:50%; background:currentColor; animation: ngPulse 1.6s ease-in-out infinite; }
@keyframes ngPulse { 0%,100% { opacity:.35; transform:scale(.9); } 50% { opacity:1; transform:scale(1); } }
div[data-testid="stMetric"] { padding:11px 13px; border:1px solid rgba(128,128,128,.18); border-radius:12px; }
.stButton > button { border-radius:10px; min-height:2.55rem; font-weight:700; transition:transform .15s ease, box-shadow .15s ease; }
.stButton > button:hover { transform:translateY(-1px); box-shadow:0 5px 16px rgba(0,0,0,.08); }
[data-testid="stFileUploader"] { border:1px dashed rgba(128,128,128,.40); border-radius:12px; padding:5px; transition:border-color .18s ease, background .18s ease; }
[data-testid="stFileUploader"]:hover { background:rgba(128,128,128,.035); }
</style>
""",
        unsafe_allow_html=True,
    )


def header() -> None:
    st.markdown(
        """
<div class="ng-shell"><div class="ng-header">
  <div>
    <div class="ng-brand">🕸️ NetGraph Studio</div>
    <div class="ng-sub">No-code spatial network analysis powered by City2Graph</div>
  </div>
  <div class="ng-status"><span class="ng-dot"></span> Ready · City2Graph 1.0.0</div>
</div></div>
""",
        unsafe_allow_html=True,
    )


def step(number: int, title: str, help_text: str | None = None) -> None:
    suffix = f'<div class="ng-help">{help_text}</div>' if help_text else ""
    st.markdown(
        f'<div class="ng-section"><span class="ng-step">{number}</span>{title}</div>{suffix}',
        unsafe_allow_html=True,
    )
