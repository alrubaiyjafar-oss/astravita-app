"""
ui_theme.py - ASTRAVITA visual identity (UI team file)
-----------------------------------------------------------
Theme: "Mission Professional" - formal, calm, data-first.
Deep navy, white text, one calm blue accent. Red / amber only for alerts.
Contains:
    apply_theme()          -> injects the custom CSS
    brand()                -> animated ASTRAVITA logo for the top bar
                              (uses images/logo_mark.png)
-----------------------------------------------------------
"""

import base64
from pathlib import Path

import streamlit as st

# Mission Professional palette
NAVY = "#070B14"
PANEL = "#0E1526"
LINE = "rgba(255, 255, 255, 0.08)"
ACCENT = "#4C8DFF"
TEXT = "#E7ECF5"
MUTED = "#8B95A8"
ALERT_RED = "#FF5A5F"
ALERT_AMBER = "#F5B942"

# app.py uses this name for the chart line color
BRIGHT_BLUE = ACCENT


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* ---------- Calm deep-navy background with a faint glow ---------- */
.stApp {{
    isolation: isolate;
    background:
        radial-gradient(ellipse at 50% -10%, rgba(76, 141, 255, 0.12) 0%, transparent 55%),
        {NAVY};
}}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {{
    background: transparent !important;
}}

/* ---------- Very faint, static star field ---------- */
.stApp::before {{
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: -1;
    opacity: 0.35;
    background-image:
        radial-gradient(1px 1px at 40px 60px, #fff, transparent),
        radial-gradient(1px 1px at 220px 140px, #fff, transparent),
        radial-gradient(1px 1px at 380px 40px, #fff, transparent),
        radial-gradient(1px 1px at 520px 260px, #fff, transparent),
        radial-gradient(1px 1px at 140px 320px, #fff, transparent);
    background-size: 600px 380px;
}}

/* ---------- No sidebar, no default header: we use a top bar ---------- */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stExpandSidebarButton"],
[data-testid="stHeader"] {{
    display: none !important;
}}
[data-testid="stMainBlockContainer"] {{
    padding-top: 1.2rem !important;
}}

/* ---------- Top navigation bar ---------- */
.st-key-topbar {{
    position: sticky;
    top: 0.6rem;
    z-index: 1000;
    background: rgba(14, 21, 38, 0.92);
    backdrop-filter: blur(10px);
    border: 1px solid {LINE};
    border-radius: 14px;
    padding: 10px 18px;
    margin-bottom: 0.5rem;
}}
.st-key-topbar [data-testid="stButtonGroup"] {{
    justify-content: center;
}}

/* ---------- Typography ---------- */
h1, h2, h3, .astra-brand,
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
    font-family: 'Inter', sans-serif !important;
}}
h1 {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
    letter-spacing: -0.5px;
}}
h3 {{
    color: {TEXT} !important;
    font-weight: 500 !important;
    border-left: 3px solid {ACCENT};
    padding-left: 12px !important;
}}
[data-testid="stCaptionContainer"] {{ color: {MUTED} !important; }}

/* ---------- Metric cards ---------- */
[data-testid="stMetric"] {{
    background: {PANEL};
    border: 1px solid {LINE};
    border-radius: 12px;
    padding: 18px 20px;
    transition: border-color 0.2s ease;
}}
[data-testid="stMetric"]:hover {{
    border-color: rgba(76, 141, 255, 0.55);
}}
[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.78rem !important;
}}
[data-testid="stMetricValue"] {{
    color: #FFFFFF !important;
    font-weight: 600 !important;
}}

/* ---------- Hide the small link icon next to titles ---------- */
[data-testid="stHeaderActionElements"] {{ display: none; }}

/* ---------- Avatar ---------- */
.astra-avatar {{
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    background: #13203A;
    border: 2px solid {ACCENT};
    color: #FFFFFF;
    font-family: 'Inter', sans-serif;
    font-weight: 600;
}}
[data-testid="stImage"] img {{
    border-radius: 50%;
    border: 2px solid {ACCENT};
}}

/* ---------- Logo: quiet orbit mark ---------- */
.astra-logo {{ display: flex; align-items: center; gap: 12px; }}
.astra-mark {{
    position: relative; width: 36px; height: 36px; flex-shrink: 0;
    border-radius: 50%; border: 1.5px solid rgba(255, 255, 255, 0.35);
}}
.astra-mark::before {{
    content: ""; position: absolute; inset: 11px; border-radius: 50%;
    background: {ACCENT};
}}
.astra-orbit {{
    position: absolute; inset: -1.5px; border-radius: 50%;
    animation: astra-spin 8s linear infinite;
}}
.astra-orbit::after {{
    content: ""; position: absolute; top: -3px; left: 50%;
    width: 6px; height: 6px; margin-left: -3px; border-radius: 50%;
    background: #FFFFFF;
}}
@keyframes astra-spin {{ to {{ transform: rotate(360deg); }} }}
.astra-brand {{
    font-size: 1.35rem; font-weight: 600; letter-spacing: 3px; color: #FFFFFF;
}}
.astra-tagline {{ color: {MUTED}; font-size: 0.78rem; }}
.astra-tag {{
    display: inline-block; margin-left: 4px;
    font-size: 0.7rem; letter-spacing: 1px; color: {MUTED};
    padding: 3px 8px; border-radius: 6px; border: 1px solid {LINE};
}}

/* ---------- Animated logo mark (images/logo_mark.png) ---------- */
.astra-logo-img {{
    position: relative; width: 62px; height: 44px; flex-shrink: 0;
    animation: astra-enter 1.1s cubic-bezier(.2,.7,.2,1) both;
}}
.astra-logo-img img {{
    width: 100%; height: 100%; object-fit: contain; display: block;
    border: none !important; border-radius: 0 !important;
    animation: astra-glow 4s ease-in-out infinite, astra-float 6s ease-in-out infinite;
}}
/* light sweep that passes across the letter A */
.astra-shine {{
    position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(105deg, transparent 35%,
                rgba(150, 190, 255, 0.95) 50%, transparent 65%);
    background-size: 300% 100%;
    animation: astra-sweep 5.5s ease-in-out infinite, astra-float 6s ease-in-out infinite;
}}
/* twinkling star on the right of the A */
.astra-star {{
    position: absolute; left: 91.3%; top: 30.4%;
    width: 14px; height: 14px; margin: -7px 0 0 -7px; pointer-events: none;
    background: radial-gradient(circle, #FFFFFF 0%, rgba(140, 185, 255, 0.85) 25%, transparent 70%);
    border-radius: 50%;
    animation: astra-twinkle 2.8s ease-in-out infinite, astra-float 6s ease-in-out infinite;
}}
.astra-brand {{ animation: astra-letters 1.4s ease-out both; }}
@keyframes astra-enter {{
    from {{ opacity: 0; transform: translateY(8px) scale(0.85); }}
    to   {{ opacity: 1; transform: none; }}
}}
@keyframes astra-float {{
    0%, 100% {{ translate: 0 0; }}
    50%      {{ translate: 0 -2px; }}
}}
@keyframes astra-glow {{
    0%, 100% {{ filter: drop-shadow(0 0 2px rgba(76, 141, 255, 0.25)); }}
    50%      {{ filter: drop-shadow(0 0 9px rgba(76, 141, 255, 0.75)); }}
}}
@keyframes astra-sweep {{
    0%, 55% {{ background-position: 100% 0; }}
    100%    {{ background-position: 0% 0; }}
}}
@keyframes astra-twinkle {{
    0%, 100% {{ opacity: 0.25; transform: scale(0.6); }}
    50%      {{ opacity: 1;    transform: scale(1.5); }}
}}
@keyframes astra-letters {{
    from {{ opacity: 0; letter-spacing: 10px; }}
    to   {{ opacity: 1; letter-spacing: 3px; }}
}}

/* ---------- Hide the "Deploy" button ---------- */
.stAppDeployButton {{ display: none; }}

/* ---------- Responsive: metric numbers never get cut ("65 b...") ---------- */
[data-testid="stMetricValue"] {{
    font-size: clamp(1.25rem, 2.1vw, 2.1rem) !important;
}}
[data-testid="stMetricValue"] [data-testid="stMarkdownContainer"],
[data-testid="stMetricValue"] p {{
    overflow: visible !important;
    text-overflow: clip !important;
    white-space: nowrap;
}}

/* ---------- Responsive: menu buttons wrap to a 2nd line instead of being cut ---------- */
.st-key-topbar [data-testid="stButtonGroup"] > div {{
    flex-wrap: wrap;
    overflow: visible !important;
    row-gap: 6px;
    justify-content: center;
}}

/* Laptops / projectors */
@media (max-width: 1280px) {{
    .astra-brand {{ font-size: 1.05rem; letter-spacing: 2px; }}
    .astra-tagline {{ display: none; }}
    .astra-logo-img {{ width: 48px; height: 34px; }}
    .st-key-topbar [data-testid="stButtonGroup"] button {{
        padding-left: 10px; padding-right: 10px;
    }}
    .st-key-topbar [data-testid="stButtonGroup"] button p {{ font-size: 0.82rem; }}
}}
/* Small laptops / tablets: the logo alone, without the word */
@media (max-width: 1100px) {{
    .astra-logo .astra-brand {{ display: none; }}
    .astra-logo-img {{ width: 58px; height: 41px; }}
}}
/* Phones: everything stacks; the top bar scrolls away */
@media (max-width: 640px) {{
    .astra-logo .astra-brand {{ display: block; }}
    .st-key-topbar {{ position: static; }}
    [data-testid="stMetricValue"] {{ font-size: 1.6rem !important; }}
    h1 {{ font-size: 1.7rem !important; }}
}}

@media (prefers-reduced-motion: reduce) {{
    .astra-orbit, .astra-logo-img, .astra-logo-img img, .astra-shine,
    .astra-star, .astra-brand {{ animation: none !important; }}
}}
</style>
"""


LOGO_PATH = Path(__file__).parent / "images" / "logo_mark.png"


@st.cache_data
def _logo_data_uri():
    """Read the logo once and turn it into text the browser can show."""
    if not LOGO_PATH.exists():
        return None
    encoded = base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return f"data:image/png;base64,{encoded}"


def apply_theme():
    """Inject the ASTRAVITA custom CSS. Call once, right after set_page_config."""
    st.markdown(CSS, unsafe_allow_html=True)
    logo = _logo_data_uri()
    if logo:
        # The light sweep only shines on the shape of the logo
        st.markdown(
            f"<style>.astra-shine {{ -webkit-mask: url('{logo}') center / contain no-repeat;"
            f" mask: url('{logo}') center / contain no-repeat; }}</style>",
            unsafe_allow_html=True,
        )


def brand():
    """Animated ASTRAVITA logo for the top bar.
    Uses images/logo_mark.png. If the file is missing, shows the simple orbit mark."""
    logo = _logo_data_uri()
    if logo:
        mark = f"""
            <div class="astra-logo-img">
                <img src="{logo}" alt="ASTRAVITA logo">
                <div class="astra-shine"></div>
                <div class="astra-star"></div>
            </div>"""
    else:
        mark = '<div class="astra-mark"><div class="astra-orbit"></div></div>'

    mark = " ".join(line.strip() for line in mark.splitlines() if line.strip())
    st.markdown(
        f"""
        <div class="astra-logo">
            {mark}
            <div>
                <div class="astra-brand">ASTRAVITA</div>
                <div class="astra-tagline">Astronaut Health Monitoring
                    <span class="astra-tag">SIMULATED</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
