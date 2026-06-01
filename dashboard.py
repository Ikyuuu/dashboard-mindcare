import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# KONFIGURASI HALAMAN
st.set_page_config(
    page_title="MindCare Analytics",
    page_icon="MC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# TEMA & WARNA
COLORS = {
    "primary":    "#1565C0",
    "secondary":  "#1976D2",
    "accent":     "#42A5F5",
    "light":      "#90CAF9",
    "pos":        "#2E7D32",
    "neg":        "#C62828",
    "warn":       "#E65100",
    "journaling": "#1565C0",
    "membaca":    "#1976D2",
    "olahraga":   "#42A5F5",
    "bg_card":    "#F8FAFF",
}

PALETTE_ACT    = ["#1565C0", "#1976D2", "#42A5F5"]
PALETTE_STRESS = ["#E3F2FD", "#90CAF9", "#42A5F5", "#1976D2", "#0D47A1"]

# GLOBAL CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display:ital@0;1&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main .block-container {
    padding: 1.8rem 2.2rem 3rem 2.2rem;
    max-width: 1440px;
}

/* ── Hide default Streamlit chrome ── */
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
.stDeployButton { display: none; }
header[data-testid="stHeader"] { background: transparent; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F1F5F9; }
::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94A3B8; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1B3E 0%, #1565C0 100%);
    border-right: none;
    box-shadow: 4px 0 24px rgba(21,101,192,0.18);
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown div {
    color: #CBD5E1 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label,
section[data-testid="stSidebar"] .stSlider label {
    font-size: 0.70rem !important;
    font-weight: 600 !important;
    color: #93C5FD !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div,
section[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: white !important;
}
section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {
    margin-top: 0.2rem;
}

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 12px rgba(15,23,42,0.06);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #1565C0, #42A5F5);
    border-radius: 4px 0 0 4px;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(21,101,192,0.12);
}
.kpi-icon-wrap {
    margin-bottom: 0.55rem;
    display: block;
    line-height: 1;
    opacity: 0.7;
}
.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.3rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1.1;
    letter-spacing: -0.02em;
}
.kpi-value-blue { color: #1565C0; }
.kpi-value-warn { color: #DC2626; }
.kpi-sub {
    font-size: 0.72rem;
    color: #94A3B8;
    margin-top: 0.3rem;
    font-weight: 400;
}

/* ── Section Header ── */
.section-hd {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1rem;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid #E2E8F0;
}
.section-hd-badge {
    background: linear-gradient(135deg, #1565C0, #42A5F5);
    color: white;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    white-space: nowrap;
}
.section-hd-title {
    font-size: 0.88rem;
    font-weight: 700;
    color: #1E293B;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* ── Insight Box ── */
.insight-box {
    background: linear-gradient(135deg, #EFF6FF 0%, #F0F9FF 100%);
    border: 1px solid #BFDBFE;
    border-left: 3px solid #1565C0;
    border-radius: 0 10px 10px 0;
    padding: 0.85rem 2.8rem 0.85rem 1.1rem;
    font-size: 0.83rem;
    color: #1E3A5F;
    line-height: 1.65;
    margin-top: 0.6rem;
    position: relative;
}
.insight-box::before {
    content: '';
    position: absolute;
    top: 0.9rem;
    right: 1rem;
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%231565C0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='12' cy='12' r='10'/%3E%3Cline x1='12' y1='16' x2='12' y2='12'/%3E%3Cline x1='12' y1='8' x2='12.01' y2='8'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    opacity: 0.45;
}

/* ── Tab Styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: #F8FAFC;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #E2E8F0;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.80rem;
    font-weight: 600;
    padding: 0.55rem 1.1rem;
    border-radius: 8px;
    color: #64748B;
    letter-spacing: 0.02em;
    border: none !important;
    background: transparent;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    color: white !important;
    background: linear-gradient(135deg, #1565C0, #1976D2) !important;
    box-shadow: 0 2px 8px rgba(21,101,192,0.3) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── Chart Container ── */
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1rem 0.8rem 1rem;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 8px rgba(15,23,42,0.05);
    margin-bottom: 0.8rem;
}

/* ── Summary Finding Card ── */
.finding-item {
    background: white;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.6rem;
    box-shadow: 0 1px 4px rgba(15,23,42,0.04);
}
.finding-bq {
    font-size: 0.67rem;
    font-weight: 700;
    color: #1565C0;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}
.finding-key {
    font-size: 0.92rem;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 0.4rem;
}
.finding-desc {
    font-size: 0.82rem;
    color: #475569;
    line-height: 1.65;
}

/* ── Divider ── */
.div-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, #E2E8F0 20%, #E2E8F0 80%, transparent);
    margin: 1.4rem 0;
}

/* ── Stat chips ── */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: #EFF6FF;
    color: #1565C0;
    border: 1px solid #BFDBFE;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    font-weight: 600;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    font-size: 0.86rem !important;
    font-weight: 600 !important;
    color: #1E293B !important;
}
.streamlit-expanderContent {
    border-top: 1px solid #F1F5F9 !important;
    padding-top: 0.75rem !important;
}

/* ── Warning / Error ── */
.stAlert {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# LOAD DATA
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df

DATA_PATH = "data_cleaned.csv"
try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(
        f"File '{DATA_PATH}' tidak ditemukan. "
        "Pastikan `data_cleaned.csv` berada di folder yang sama dengan `dashboard.py`."
    )
    st.stop()

# ==== HELPER FUNCTIONS START ====
def kpi_card(icon_svg: str, label: str, value: str, sub: str = "", color_class: str = "kpi-value-blue") -> str:
    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon-wrap">{icon_svg}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {color_class}">{value}</div>
        {sub_html}
    </div>
    """

def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def section_header(badge: str, title: str):
    st.markdown(
        f'<div class="section-hd">'
        f'<span class="section-hd-badge">{badge}</span>'
        f'<span class="section-hd-title">{title}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

def divider():
    st.markdown('<div class="div-line"></div>', unsafe_allow_html=True)

# Plotly default layout
PLOTLY_LAYOUT = dict(
    font=dict(family="DM Sans, Arial, sans-serif", size=12, color="#334155"),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=16, r=16, t=44, b=16),
    title_font=dict(size=13, color="#0F172A", family="DM Sans, Arial, sans-serif"),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E2E8F0",
        font_size=12,
        font_family="DM Sans, Arial, sans-serif",
    ),
)

def apply_grid(fig):
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", gridwidth=1, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", gridwidth=1, zeroline=False)
    return fig

# ==== HELPER FUNCTIONS END ====

# ==== SIDEBAR START ====
SIDEBAR_USE_LOGO  = True       
SIDEBAR_LOGO_PATH = "logo.png"  

SIDEBAR_LOGO = None
if SIDEBAR_USE_LOGO:
    try:
        from PIL import Image as _PILImage
        SIDEBAR_LOGO = _PILImage.open(SIDEBAR_LOGO_PATH)
    except Exception:
        SIDEBAR_LOGO = None

with st.sidebar:
    # ── Brand Header ──
    if SIDEBAR_LOGO is not None:
        st.image(SIDEBAR_LOGO, width=160)
    else:
        st.markdown("""
        <div style="text-align:center; padding: 0.6rem 0 1.4rem 0;">
            <div style="font-size:1.2rem; font-weight:700; color:white; letter-spacing:-0.01em;
                        font-family:'DM Serif Display',Georgia,serif; line-height:1.2;">
                MindCare
            </div>
            <div style="font-size:0.65rem; color:#93C5FD; font-weight:500; letter-spacing:0.12em;
                        text-transform:uppercase; margin-top:0.2rem;">
                Analytics Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)


    # ── Separator ──
    st.markdown("""
    <div style="height:1px; background:rgba(255,255,255,0.12); margin-bottom:1.3rem;"></div>
    """, unsafe_allow_html=True)

    # ── Filter Label ──
    st.markdown("""
    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:1rem;">
        <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24"
             fill="none" stroke="#93C5FD" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
        </svg>
        <span style="font-size:0.68rem; font-weight:700; color:#93C5FD;
                     text-transform:uppercase; letter-spacing:0.12em;">Filter Data</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Stress Level (dropdown) ──
    stress_opts = sorted(df["stress_level_1_5"].unique())
    stress_label_map = {lvl: f"Level {lvl}" for lvl in stress_opts}
    stress_label_map_inv = {v: k for k, v in stress_label_map.items()}
    stress_dropdown_opts = ["Semua Level"] + [f"Level {lvl}" for lvl in stress_opts]

    sel_stress_label = st.selectbox(
        "Stress Level",
        options=stress_dropdown_opts,
        index=0,
    )
    stress_sel = stress_opts if sel_stress_label == "Semua Level" else [stress_label_map_inv[sel_stress_label]]

    # ── Jenis Kelamin (dropdown) ──
    gender_opts = df["jenis_kelamin"].unique().tolist()
    gender_dropdown_opts = ["Semua Gender"] + gender_opts

    sel_gender_label = st.selectbox(
        "Jenis Kelamin",
        options=gender_dropdown_opts,
        index=0,
    )
    gender_sel = gender_opts if sel_gender_label == "Semua Gender" else [sel_gender_label]

    # ── Penyebab Stres (dropdown) ──
    cause_opts = df["penyebab_stres"].unique().tolist()
    cause_dropdown_opts = ["Semua Penyebab"] + cause_opts

    sel_cause_label = st.selectbox(
        "Penyebab Stres",
        options=cause_dropdown_opts,
        index=0,
    )
    cause_sel = cause_opts if sel_cause_label == "Semua Penyebab" else [sel_cause_label]

    # ── Rentang Usia (slider) ──
    st.markdown("""
    <div style="font-size:0.70rem; font-weight:600; color:#93C5FD;
                text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.1rem; margin-top:0.3rem;">
        Rentang Usia
    </div>
    """, unsafe_allow_html=True)
    age_min, age_max = int(df["umur"].min()), int(df["umur"].max())
    age_range = st.slider("Rentang Usia", age_min, age_max, (age_min, age_max), label_visibility="collapsed")

    # ── Separator + Footer ──
    st.markdown("""
    <div style="height:1px; background:rgba(255,255,255,0.12); margin: 1.3rem 0 1rem 0;"></div>
    <div style="text-align:center; line-height:1.8;">
        <div style="font-size:0.72rem; color:#93C5FD; font-weight:600;">Coding Camp 2026</div>
        <div style="font-size:0.68rem; color:rgba(255,255,255,0.45);">DBS Foundation</div>
        <div style="font-size:0.65rem; color:rgba(255,255,255,0.3);">CC26-PSU148</div>
    </div>
    """, unsafe_allow_html=True)

# TERAPKAN FILTER
mask = (
    df["stress_level_1_5"].isin(stress_sel) &
    df["jenis_kelamin"].isin(gender_sel) &
    df["penyebab_stres"].isin(cause_sel) &
    df["umur"].between(age_range[0], age_range[1])
)
dff = df[mask].copy()

if dff.empty:
    st.warning("Tidak ada data yang sesuai dengan filter yang dipilih.")
    st.stop()

# ==== HEADER UTAMA ====
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown("""
    <div style="margin-bottom: 0.1rem;">
        <div style="font-family:'DM Serif Display',Georgia,serif; font-size:2rem;
                    color:#0F172A; line-height:1.15; letter-spacing:-0.02em;">
            MindCare
            <span style="font-style:italic; color:#1565C0;"> Analytics</span>
        </div>
        <div style="font-size:0.85rem; color:#64748B; margin-top:0.3rem; font-weight:400;">
            Dashboard Analitik Kesehatan Mental &nbsp;·&nbsp;
            Coding Camp 2026 powered by DBS Foundation
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_badge:
    filter_count = len(dff)
    st.markdown(f"""
    <div style="text-align:right; padding-top:0.5rem;">
        <div style="display:inline-block; background:linear-gradient(135deg,#EFF6FF,#DBEAFE);
                    border:1px solid #BFDBFE; border-radius:10px; padding:0.5rem 0.9rem;">
            <div style="font-size:0.62rem; color:#1565C0; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.08em;">Data Aktif</div>
            <div style="font-size:1.3rem; font-weight:700; color:#1565C0;
                        letter-spacing:-0.02em;">{filter_count:,}</div>
            <div style="font-size:0.65rem; color:#94A3B8;">responden</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="margin: 1rem 0 0.6rem 0; height:2px; background:linear-gradient(90deg,#1565C0 0%,#42A5F5 50%,transparent 100%); border-radius:2px;"></div>', unsafe_allow_html=True)
# ==== HEADER UTAMA END ====

# ==== KPI ROW ====
avg_stress      = dff["stress_level_1_5"].mean()
pct_high_stress = (dff["stress_level_1_5"] >= 4).mean() * 100
avg_anxiety     = dff["anxiety_score"].mean()
avg_sleep       = dff["kualitas_tidur_1_5"].mean()
top_act         = dff["aktivitas_dipilih"].value_counts().idxmax()
top_act_pct     = dff["aktivitas_dipilih"].value_counts(normalize=True).max() * 100

k1, k2, k3, k4, k5 = st.columns(5)

# Feather SVG icons untuk setiap KPI card
SVG_USERS   = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
SVG_ACTIVITY= '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>'
SVG_ALERT   = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'
SVG_BRAIN   = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>'
SVG_STAR    = '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

with k1:
    st.markdown(kpi_card(SVG_USERS, "Total Responden", f"{len(dff):,}", f"dari {len(df):,} total data"), unsafe_allow_html=True)
with k2:
    st.markdown(kpi_card(SVG_ACTIVITY, "Rata-rata Stress Level", f"{avg_stress:.2f}", "Skala 1–5"), unsafe_allow_html=True)
with k3:
    color = "kpi-value-warn" if pct_high_stress > 30 else "kpi-value-blue"
    st.markdown(kpi_card(SVG_ALERT, "Stres Tinggi (≥ Level 4)", f"{pct_high_stress:.1f}%", "Proporsi responden", color), unsafe_allow_html=True)
with k4:
    st.markdown(kpi_card(SVG_BRAIN, "Rata-rata Anxiety Score", f"{avg_anxiety:.1f}", "Skala 0–21"), unsafe_allow_html=True)
with k5:
    st.markdown(kpi_card(SVG_STAR, "Aktivitas Dominan", top_act.title(), f"{top_act_pct:.1f}% dari total"), unsafe_allow_html=True)

st.markdown('<div style="margin-top:1.2rem;"></div>', unsafe_allow_html=True)

# ==== KPI ROW END ====

# ==== TAB NAVIGASI ====
tab1, tab2, tab3, tab4 = st.tabs([
    "Profil & Demografi",
    "Faktor Psikologis & Gaya Hidup",
    "Rekomendasi Aktivitas",
    "Ringkasan Temuan",
])

# ==== TAB 1 — PROFIL & DEMOGRAFI ====
with tab1:

    row1_l, row1_r = st.columns(2)

    # ── Distribusi Stress Level ──
    with row1_l:
        section_header("DEMOGRAFI", "Distribusi Tingkat Stres")
        stress_dist = dff["stress_level_1_5"].value_counts().sort_index().reset_index()
        stress_dist.columns = ["Stress Level", "Jumlah"]
        stress_dist["Label"] = stress_dist["Stress Level"].map(
            {1: "Sangat Rendah", 2: "Rendah", 3: "Sedang", 4: "Tinggi", 5: "Sangat Tinggi"}
        )
        fig = px.bar(
            stress_dist, x="Stress Level", y="Jumlah",
            color="Jumlah", color_continuous_scale=["#DBEAFE", "#1565C0"],
            text="Jumlah",
            custom_data=["Label"],
        )
        fig.update_traces(
            texttemplate="%{y:,}",
            textposition="outside",
            hovertemplate="<b>Level %{x} — %{customdata[0]}</b><br>Jumlah: %{y:,}<extra></extra>",
            marker_line_width=0,
        )
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Persebaran Responden per Stress Level",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Tingkat Stres (1=Sangat Rendah · 5=Sangat Tinggi)",
            yaxis_title="Jumlah Responden",
            height=300,
        )
        apply_grid(fig)
        st.plotly_chart(fig, use_container_width=True)
        insight(
            "Konsentrasi terbesar berada di <b>Level 3–4</b>, menunjukkan mayoritas responden mengalami "
            "stres menengah hingga tinggi. Level 5 (sangat tinggi) ditemukan pada "
            f"<b>{(dff['stress_level_1_5']==5).sum():,} responden</b> dalam data yang difilter."
        )

    # ── Distribusi Penyebab Stres ──
    with row1_r:
        section_header("DEMOGRAFI", "Penyebab Stres Utama")
        cause_dist = dff["penyebab_stres"].value_counts().reset_index()
        cause_dist.columns = ["Penyebab", "Jumlah"]
        cause_dist["Persen"] = (cause_dist["Jumlah"] / cause_dist["Jumlah"].sum() * 100).round(1)
        fig2 = px.bar(
            cause_dist.sort_values("Jumlah"),
            x="Jumlah", y="Penyebab",
            orientation="h",
            color="Jumlah", color_continuous_scale=["#BFDBFE", "#1565C0"],
            text="Persen",
        )
        fig2.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Jumlah: %{x:,}<extra></extra>",
            marker_line_width=0,
        )
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title="Distribusi Penyebab Stres",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Jumlah Responden",
            yaxis_title="",
            height=300,
        )
        apply_grid(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        top_cause = cause_dist.iloc[0]
        insight(
            f"<b>{top_cause['Penyebab']}</b> menjadi penyebab stres paling dominan "
            f"({top_cause['Persen']}%). Faktor pekerjaan dan keuangan mengikuti di posisi selanjutnya, "
            "mencerminkan tekanan multidimensional yang dihadapi responden."
        )

    divider()

    row2_l, row2_r = st.columns(2)

    # ── Stress per Pekerjaan ──
    with row2_l:
        section_header("PROFIL", "Rata-rata Stress Level per Pekerjaan")
        job_stress = (
            dff.groupby("pekerjaan")["stress_level_1_5"]
            .mean()
            .sort_values(ascending=True)
            .reset_index()
        )
        job_stress.columns = ["Pekerjaan", "Avg Stress"]
        fig3 = px.bar(
            job_stress, x="Avg Stress", y="Pekerjaan",
            orientation="h",
            color="Avg Stress",
            color_continuous_scale=["#DBEAFE", "#1565C0"],
            text="Avg Stress",
        )
        fig3.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Rata-rata: %{x:.2f}<extra></extra>",
            marker_line_width=0,
        )
        fig3.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Stress Level per Profesi",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Rata-rata Stress Level",
            xaxis_range=[0, 5.5],
            yaxis_title="",
            height=420,
        )
        apply_grid(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Distribusi Usia per Stress Level ──
    with row2_r:
        section_header("PROFIL", "Distribusi Usia per Tingkat Stres")
        fig4 = go.Figure()
        palette_stress = ["#DBEAFE", "#93C5FD", "#3B82F6", "#1D4ED8", "#1E3A8A"]
        for i, lvl in enumerate(sorted(dff["stress_level_1_5"].unique())):
            subset = dff[dff["stress_level_1_5"] == lvl]["umur"]
            fig4.add_trace(go.Box(
                y=subset,
                name=f"Level {lvl}",
                marker_color=palette_stress[i % len(palette_stress)],
                boxmean=True,
                hovertemplate=f"<b>Level {lvl}</b><br>%{{y}} tahun<extra></extra>",
                line_color="#1565C0",
                line_width=1.5,
            ))
        fig4.update_layout(
            **PLOTLY_LAYOUT,
            title="Distribusi Usia per Stress Level",
            yaxis_title="Usia (tahun)",
            xaxis_title="Tingkat Stres",
            showlegend=False,
            height=420,
        )
        apply_grid(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    insight(
        "Tidak terdapat pola usia yang konsisten dan linier terhadap tingkat stres — stres tinggi "
        "dijumpai di hampir seluruh kelompok usia, menunjukkan bahwa stres bersifat <b>lintas generasi</b> "
        "dan lebih dipengaruhi oleh faktor konteks (pekerjaan, akademik, sosial)."
    )

    divider()

    # ── Gender Breakdown ──
    section_header("PROFIL", "Breakdown Gender")
    gc1, gc2 = st.columns(2)

    with gc1:
        gender_stress = dff.groupby("jenis_kelamin")["stress_level_1_5"].mean().reset_index()
        gender_stress.columns = ["Gender", "Avg Stress"]
        fig_g1 = px.bar(
            gender_stress, x="Gender", y="Avg Stress",
            color="Gender",
            color_discrete_map={"Male": "#1565C0", "Female": "#42A5F5"},
            text="Avg Stress",
        )
        fig_g1.update_traces(
            texttemplate="%{y:.2f}",
            textposition="outside",
            marker_line_width=0,
        )
        fig_g1.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Stress Level per Gender",
            showlegend=False,
            yaxis_range=[0, 5],
            xaxis_title="",
            yaxis_title="Rata-rata Stress Level",
        )
        apply_grid(fig_g1)
        st.plotly_chart(fig_g1, use_container_width=True)

    with gc2:
        gender_act = dff.groupby(["jenis_kelamin", "aktivitas_dipilih"]).size().reset_index(name="n")
        gender_act["pct"] = gender_act.groupby("jenis_kelamin")["n"].transform(lambda x: x / x.sum() * 100)
        fig_g2 = px.bar(
            gender_act, x="jenis_kelamin", y="pct", color="aktivitas_dipilih",
            color_discrete_map={
                "journaling": "#1565C0",
                "membaca":    "#1976D2",
                "olahraga":   "#42A5F5",
            },
            text="pct",
            barmode="group",
        )
        fig_g2.update_traces(
            texttemplate="%{y:.1f}%",
            textposition="outside",
            marker_line_width=0,
        )
        fig_g2.update_layout(
            **PLOTLY_LAYOUT,
            title="Preferensi Aktivitas per Gender",
            xaxis_title="",
            yaxis_title="Proporsi (%)",
            legend_title="Aktivitas",
            yaxis_range=[0, 75],
        )
        apply_grid(fig_g2)
        st.plotly_chart(fig_g2, use_container_width=True)

# ==== TAB 2 — FAKTOR PSIKOLOGIS & GAYA HIDUP ====
with tab2:

    # ── BQ1: Skor Psikologis ──
    section_header("BQ1", "Faktor Psikologis vs Tingkat Stres")

    p1, p2, p3 = st.columns(3)
    psych_metrics = [
        ("anxiety_score",     "Anxiety Score",     "Skala 0–21",  p1, "#1565C0"),
        ("depression_score",  "Depression Score",  "Skala 0–27",  p2, "#1976D2"),
        ("self_esteem_score", "Self-Esteem Score", "Skala 0–30",  p3, "#42A5F5"),
    ]

    for col, label, skala, container, color in psych_metrics:
        agg = dff.groupby("stress_level_1_5")[col].mean().reset_index()
        agg.columns = ["Stress Level", "Nilai"]
        with container:
            fig = px.line(
                agg, x="Stress Level", y="Nilai",
                markers=True,
                color_discrete_sequence=[color],
            )
            fig.update_traces(
                line_width=2.5,
                marker_size=9,
                marker_symbol="circle",
                marker_line_color="white",
                marker_line_width=2,
                hovertemplate="<b>Level %{x}</b><br>Rata-rata: %{y:.2f}<extra></extra>",
            )
            # Shaded area under line
            fig.add_traces(go.Scatter(
                x=agg["Stress Level"].tolist() + agg["Stress Level"].tolist()[::-1],
                y=agg["Nilai"].tolist() + [0]*len(agg),
                fill="toself",
                fillcolor=f"rgba(21,101,192,0.07)",
                line_color="rgba(255,255,255,0)",
                showlegend=False,
                hoverinfo="skip",
            ))
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=f"{label}<br><sup style='color:#94A3B8;font-size:11px;'>{skala}</sup>",
                xaxis_title="Stress Level",
                yaxis_title="Rata-rata Skor",
                height=280,
            )
            apply_grid(fig)
            st.plotly_chart(fig, use_container_width=True)

    insight(
        "<b>Anxiety Score</b> menunjukkan kenaikan paling tajam seiring meningkatnya stress level "
        "(effect size η² tertinggi). Depression score bergerak paralel, sedangkan Self-Esteem "
        "turun secara konsisten — mengkonfirmasi bahwa stres tinggi berkaitan erat dengan "
        "penurunan rasa percaya diri."
    )

    divider()

    # ── BQ2: Gaya Hidup ──
    section_header("BQ2", "Gaya Hidup vs Tingkat Stres")
    b2l, b2r = st.columns(2)

    with b2l:
        sleep_stress = dff.groupby("kualitas_tidur_1_5")["stress_level_1_5"].mean().reset_index()
        sleep_stress.columns = ["Kualitas Tidur", "Avg Stress"]
        fig_sl = px.bar(
            sleep_stress, x="Kualitas Tidur", y="Avg Stress",
            color="Avg Stress",
            color_continuous_scale=["#1565C0", "#DBEAFE"],
            text="Avg Stress",
        )
        fig_sl.update_traces(
            texttemplate="%{y:.2f}",
            textposition="outside",
            marker_line_width=0,
        )
        fig_sl.update_layout(
            **PLOTLY_LAYOUT,
            title="Kualitas Tidur vs Rata-rata Stress Level",
            xaxis_title="Kualitas Tidur (1=Buruk · 5=Sangat Baik)",
            yaxis_title="Rata-rata Stress Level",
            yaxis_range=[0, 5.5],
            coloraxis_showscale=False,
        )
        apply_grid(fig_sl)
        st.plotly_chart(fig_sl, use_container_width=True)

    with b2r:
        act_stress = dff.groupby("stress_level_1_5")["aktivitas_fisik_mnt"].mean().reset_index()
        act_stress.columns = ["Stress Level", "Avg Aktivitas (mnt)"]
        fig_af = px.bar(
            act_stress, x="Stress Level", y="Avg Aktivitas (mnt)",
            color="Avg Aktivitas (mnt)",
            color_continuous_scale=["#DBEAFE", "#1565C0"],
            text="Avg Aktivitas (mnt)",
        )
        fig_af.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            marker_line_width=0,
        )
        fig_af.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Aktivitas Fisik per Stress Level",
            xaxis_title="Stress Level",
            yaxis_title="Aktivitas Fisik (menit/hari)",
            coloraxis_showscale=False,
        )
        apply_grid(fig_af)
        st.plotly_chart(fig_af, use_container_width=True)

    insight(
        "<b>Korelasi negatif jelas:</b> semakin buruk kualitas tidur → semakin tinggi stress level. "
        "Responden dengan kualitas tidur = 1 memiliki rata-rata stress level 4.27, sementara "
        "kualitas tidur = 5 turun ke 2.04. Pola serupa berlaku pada aktivitas fisik — kelompok "
        "dengan stres tinggi rata-rata berolahraga lebih sedikit per hari."
    )

    divider()

    # ── Durasi Tidur ──
    section_header("LIFESTYLE", "Pola Durasi Tidur per Tingkat Stres")
    fig_sleep_dur = go.Figure()
    for i, lvl in enumerate(sorted(dff["stress_level_1_5"].unique())):
        subset = dff[dff["stress_level_1_5"] == lvl]["durasi_tidur_jam"]
        fig_sleep_dur.add_trace(go.Violin(
            y=subset,
            name=f"Level {lvl}",
            box_visible=True,
            meanline_visible=True,
            fillcolor=PALETTE_STRESS[i % 5],
            opacity=0.85,
            line_color="#1565C0",
            line_width=1.5,
        ))
    fig_sleep_dur.update_layout(
        **PLOTLY_LAYOUT,
        title="Distribusi Durasi Tidur per Stress Level",
        yaxis_title="Durasi Tidur (jam)",
        xaxis_title="Stress Level",
        showlegend=False,
        height=340,
    )
    apply_grid(fig_sleep_dur)
    st.plotly_chart(fig_sleep_dur, use_container_width=True)

# ==== TAB 3 — REKOMENDASI AKTIVITAS ====
with tab3:

    # ── BQ3: Distribusi Aktivitas ──
    section_header("BQ3", "Distribusi Aktivitas per Tingkat Stres")
    cross = (
        pd.crosstab(dff["stress_level_1_5"], dff["aktivitas_dipilih"], normalize="index") * 100
    ).round(1).reset_index()
    cross_melt = cross.melt(id_vars="stress_level_1_5", var_name="Aktivitas", value_name="Proporsi (%)")
    cross_melt["Stress Level"] = "Level " + cross_melt["stress_level_1_5"].astype(str)

    fig_cross = px.bar(
        cross_melt, x="Stress Level", y="Proporsi (%)", color="Aktivitas",
        color_discrete_map={
            "journaling": "#1565C0",
            "membaca":    "#42A5F5",
            "olahraga":   "#90CAF9",
        },
        text="Proporsi (%)",
        barmode="stack",
    )
    fig_cross.update_traces(
        texttemplate="%{y:.1f}%",
        textposition="inside",
        textfont_size=11,
        marker_line_width=0,
    )
    fig_cross.update_layout(
        **PLOTLY_LAYOUT,
        title="Proporsi Aktivitas yang Dipilih per Stress Level",
        xaxis_title="",
        yaxis_title="Proporsi (%)",
        legend_title="Aktivitas",
        yaxis_range=[0, 105],
    )
    apply_grid(fig_cross)
    st.plotly_chart(fig_cross, use_container_width=True)
    insight(
        "<b>Pergeseran pola aktivitas seiring kenaikan stres sangat signifikan:</b><br>"
        "• Level 1–2: Olahraga dominan (~40–44%) — pengguna aktif secara fisik.<br>"
        "• Level 3: Membaca mengambil alih posisi dominan (~60%).<br>"
        "• Level 4–5: Journaling melonjak hingga 43–71% — mencerminkan kebutuhan pemrosesan emosi mendalam "
        "pada stres tinggi."
    )

    divider()

    a3_l, a3_r = st.columns(2)

    # ── BQ4: Profil Psikologis per Aktivitas ──
    with a3_l:
        section_header("BQ4", "Profil Psikologis per Aktivitas")
        psych_by_act = dff.groupby("aktivitas_dipilih")[
            ["anxiety_score", "depression_score", "self_esteem_score"]
        ].mean().reset_index()
        psych_melt = psych_by_act.melt(id_vars="aktivitas_dipilih", var_name="Metrik", value_name="Rata-rata")
        psych_melt["Metrik"] = psych_melt["Metrik"].map({
            "anxiety_score":     "Anxiety",
            "depression_score":  "Depression",
            "self_esteem_score": "Self-Esteem",
        })
        fig_psych = px.bar(
            psych_melt, x="aktivitas_dipilih", y="Rata-rata", color="Metrik",
            barmode="group",
            color_discrete_sequence=["#1565C0", "#1976D2", "#42A5F5"],
            text="Rata-rata",
        )
        fig_psych.update_traces(
            texttemplate="%{y:.1f}",
            textposition="outside",
            marker_line_width=0,
        )
        fig_psych.update_layout(
            **PLOTLY_LAYOUT,
            title="Skor Psikologis Rata-rata per Aktivitas",
            xaxis_title="Aktivitas",
            yaxis_title="Rata-rata Skor",
            legend_title="Metrik",
        )
        apply_grid(fig_psych)
        st.plotly_chart(fig_psych, use_container_width=True)
        insight(
            "Pengguna yang memilih <b>journaling</b> memiliki anxiety (12.05) dan depression (12.64) "
            "tertinggi, serta self-esteem terendah (16.25). <b>Olahraga</b> dipilih oleh responden "
            "dengan kondisi psikologis paling sehat — mengkonfirmasi journaling sebagai intervensi "
            "untuk kondisi psikologis yang lebih berat."
        )

    # ── BQ5: Durasi Aktivitas ──
    with a3_r:
        section_header("BQ5", "Durasi Rekomendasi per Aktivitas")
        dur_by_act = dff.groupby("aktivitas_dipilih")["durasi_menit"].mean().reset_index()
        dur_by_act.columns = ["Aktivitas", "Durasi Rata-rata (mnt)"]
        fig_dur = px.bar(
            dur_by_act, x="Aktivitas", y="Durasi Rata-rata (mnt)",
            color="Aktivitas",
            color_discrete_map={
                "journaling": "#1565C0",
                "membaca":    "#42A5F5",
                "olahraga":   "#90CAF9",
            },
            text="Durasi Rata-rata (mnt)",
        )
        fig_dur.update_traces(
            texttemplate="%{y:.1f} mnt",
            textposition="outside",
            marker_line_width=0,
        )
        fig_dur.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Durasi Rekomendasi per Aktivitas",
            xaxis_title="",
            yaxis_title="Durasi (menit)",
            showlegend=False,
            yaxis_range=[0, 60],
        )
        apply_grid(fig_dur)
        st.plotly_chart(fig_dur, use_container_width=True)

        # Waktu luang threshold
        dff2 = dff.copy()
        dff2["Waktu Luang"] = dff2["waktu_luang_mnt"].apply(
            lambda x: "> 90 mnt" if x > 90 else "≤ 90 mnt"
        )
        dur_wl = dff2.groupby("Waktu Luang")["durasi_menit"].mean().reset_index()
        dur_wl.columns = ["Waktu Luang", "Durasi Rata-rata (mnt)"]
        fig_wl = px.bar(
            dur_wl, x="Waktu Luang", y="Durasi Rata-rata (mnt)",
            color="Waktu Luang",
            color_discrete_sequence=["#1976D2", "#90CAF9"],
            text="Durasi Rata-rata (mnt)",
        )
        fig_wl.update_traces(
            texttemplate="%{y:.1f} mnt",
            textposition="outside",
            marker_line_width=0,
        )
        fig_wl.update_layout(
            **PLOTLY_LAYOUT,
            title="Pengaruh Waktu Luang terhadap Durasi Rekomendasi",
            showlegend=False,
            yaxis_range=[0, 55],
            xaxis_title="",
            yaxis_title="Durasi (menit)",
        )
        apply_grid(fig_wl)
        st.plotly_chart(fig_wl, use_container_width=True)
        insight(
            "Waktu luang <b>&gt; 90 menit</b> secara konsisten menghasilkan rekomendasi durasi lebih panjang. "
            "Ini mengindikasikan sistem rekomendasi MindCare menyesuaikan intensitas intervensi "
            "dengan ketersediaan waktu pengguna."
        )

    divider()

    # ── Heatmap Aktivitas & Tujuan ──
    section_header("ANALISIS", "Tujuan Utama per Jenis Aktivitas")
    heat_data = (
        pd.crosstab(dff["aktivitas_dipilih"], dff["tujuan_utama"], normalize="index") * 100
    ).round(1)
    fig_heat = px.imshow(
        heat_data,
        color_continuous_scale=["#EFF6FF", "#DBEAFE", "#1565C0"],
        text_auto=".1f",
        aspect="auto",
    )
    fig_heat.update_layout(
        **PLOTLY_LAYOUT,
        title="Proporsi Tujuan Utama per Aktivitas (%)",
        xaxis_title="",
        yaxis_title="",
        coloraxis_showscale=False,
        height=260,
    )
    st.plotly_chart(fig_heat, use_container_width=True)

# ==== TAB 4 — RINGKASAN TEMUAN ====
with tab4:

    section_header("RINGKASAN", "Business Questions & Temuan Kunci")

    findings = [
        ("BQ1", "Faktor Psikologis", "Anxiety Score",
         "Prediktor terkuat tingkat stres (η² tertinggi). Naik secara konsisten dari level 1 → 5. "
         "Depression score bergerak paralel; self-esteem turun linear.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>'),
        ("BQ2", "Gaya Hidup", "Tidur & Aktivitas Fisik",
         "Kualitas tidur rendah (≤2) berkorelasi dengan stress level ≥4. "
         "Responden stres tinggi berolahraga lebih sedikit per hari.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 18a5 5 0 0 0-10 0"/><line x1="12" y1="2" x2="12" y2="9"/><line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/><line x1="2" y1="18" x2="4" y2="18"/><line x1="20" y1="18" x2="22" y2="18"/><line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/><line x1="23" y1="22" x2="1" y2="22"/><polyline points="8 6 12 2 16 6"/></svg>'),
        ("BQ3", "Distribusi Aktivitas", "Stress Level vs Aktivitas",
         "Olahraga dominan di level rendah (1–2). Journaling meningkat drastis di level 4–5 "
         "(hingga 70.9%), menggantikan membaca dan olahraga.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'),
        ("BQ4", "Intervensi Psikologis", "Journaling sebagai Intervensi",
         "Pengguna journaling memiliki anxiety (12.05) dan depression (12.64) tertinggi, "
         "mengkonfirmasi journaling sebagai intervensi untuk kondisi psikologis berat.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>'),
        ("BQ5", "Durasi & Komitmen", "Waktu Luang > 90 Menit",
         "Rekomendasi durasi lebih panjang secara konsisten pada kelompok waktu luang > 90 menit, "
         "menunjukkan penyesuaian sistem terhadap ketersediaan waktu.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>'),
        ("BQ6", "Feature Selection", "Fitur Preferensi + Psikologis",
         "Kolom preferensi (olahraga, baca, jurnal) dan skor psikologis memiliki korelasi |r| ≥ 0.15 "
         "terhadap target — fitur paling relevan untuk model KNN.",
         '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>'),
    ]

    col_a, col_b = st.columns(2)
    for i, (bq, kategori, key, desc, icon_svg) in enumerate(findings):
        target_col = col_a if i % 2 == 0 else col_b
        with target_col:
            st.markdown(f"""
            <div class="finding-item">
                <div style="display:flex; align-items:flex-start; gap:0.8rem;">
                    <div style="padding-top:0.1rem; opacity:0.85; flex-shrink:0;">{icon_svg}</div>
                    <div style="flex:1;">
                        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.3rem;">
                            <span class="section-hd-badge">{bq}</span>
                            <span style="font-size:0.68rem; color:#94A3B8; font-weight:500;">{kategori}</span>
                        </div>
                        <div class="finding-key">{key}</div>
                        <div class="finding-desc">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    divider()

    # ── Statistik Kualitas Dataset ──
    section_header("DATASET", "Statistik Kualitas & Pembersihan Data")

    cols = st.columns(4)
    SVG_BOX    = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>'
    SVG_CHECK  = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>'
    SVG_TRASH  = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#DC2626" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>'
    SVG_SHIELD = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
    stats_items = [
        (SVG_BOX,    "Data Raw",        "11.200", "baris awal",               "kpi-value-blue"),
        (SVG_CHECK,  "Data Cleaned",    "10.716", "setelah dedup & cleaning",  "kpi-value-blue"),
        (SVG_TRASH,  "Duplikat Dihapus","359",    "3.21% dari total",          "kpi-value-warn"),
        (SVG_SHIELD, "Missing Values",  "0",      "setelah imputasi penuh",    "kpi-value-blue"),
    ]
    for col_st, (icon, lbl, val, sub, color) in zip(cols, stats_items):
        with col_st:
            st.markdown(kpi_card(icon, lbl, val, sub, color), unsafe_allow_html=True)

    divider()

    # ── Distribusi Sumber Dataset ──
    section_header("DATASET", "Distribusi Sumber Dataset")

    src_dist = dff["source"].value_counts().reset_index()
    src_dist.columns = ["Sumber", "Jumlah"]
    src_dist["Persen"] = (src_dist["Jumlah"] / src_dist["Jumlah"].sum() * 100).round(1)

    pie_col, info_col = st.columns([1.2, 1])
    with pie_col:
        # Horizontal bar chart — menggantikan pie agar label panjang tidak terpotong
        fig_src = go.Figure()
        bar_colors = ["#1565C0", "#1976D2", "#42A5F5"]
        for i, row in src_dist.iterrows():
            fig_src.add_trace(go.Bar(
                x=[row["Persen"]],
                y=[row["Sumber"]],
                orientation="h",
                name=row["Sumber"],
                marker_color=bar_colors[i % len(bar_colors)],
                marker_line_width=0,
                text=f'{row["Persen"]}%  ({row["Jumlah"]:,})',
                textposition="outside",
                hovertemplate=f'<b>{row["Sumber"]}</b><br>{row["Jumlah"]:,} responden ({row["Persen"]}%)<extra></extra>',
                showlegend=False,
            ))
        fig_src.update_layout(
            **PLOTLY_LAYOUT,
            title="Komposisi Sumber Data",
            xaxis_title="Proporsi (%)",
            yaxis_title="",
            xaxis_range=[0, src_dist["Persen"].max() * 1.35],
            barmode="overlay",
            height=240,
            yaxis=dict(autorange="reversed"),
        )
        apply_grid(fig_src)
        st.plotly_chart(fig_src, use_container_width=True)

    with info_col:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        SVG_GRAD  = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'
        SVG_BOOK  = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>'
        SVG_MOON  = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1565C0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>'
        source_descriptions = [
            (SVG_GRAD, "StudentCopingMechanisms",
             "Fokus pada mekanisme coping dan beban akademik mahasiswa."),
            (SVG_BOOK, "StudentStressFactors",
             "Faktor stres akademik, sosial, dan ekonomi pada populasi pelajar."),
            (SVG_MOON, "SleepHealthLifestyle",
             "Pola tidur, kesehatan, dan gaya hidup dari populasi umum."),
        ]
        for icon_svg, name, desc in source_descriptions:
            st.markdown(f"""
            <div style="background:white; border:1px solid #E2E8F0; border-radius:10px;
                        padding:0.85rem 1rem; margin-bottom:0.6rem;
                        box-shadow:0 1px 4px rgba(15,23,42,0.04);">
                <div style="display:flex; gap:0.7rem; align-items:flex-start;">
                    <div style="margin-top:0.1rem; opacity:0.85; flex-shrink:0;">{icon_svg}</div>
                    <div>
                        <div style="font-size:0.78rem; font-weight:700; color:#1565C0; margin-bottom:0.25rem;">{name}</div>
                        <div style="font-size:0.78rem; color:#475569; line-height:1.55;">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    insight(
        "MindCare mengembangkan sistem rekomendasi mental wellness activity yang dipersonalisasi "
        "berdasarkan profil psikologis, kondisi gaya hidup, dan preferensi pengguna. Proses integrasi "
        "dataset dari tiga sumber menghasilkan 11.200 sampel awal yang kemudian melalui tahapan data "
        "cleaning hingga tersisa 10.716 data berkualitas tinggi, sehingga layak digunakan untuk tahap "
        "pemodelan lebih lanjut oleh tim AI Engineer. Hasil Exploratory Data Analysis (EDA) menunjukkan "
        "bahwa struktur data yang diperoleh cukup representatif, informatif, dan mendukung pembangunan "
        "sistem rekomendasi berbasis data.<br><br>"
        "<b>Temuan Utama EDA:</b><br>"
        "<b>1. Feature Engineering</b> — Fitur rekayasa <i>psychological_score</i> dan <i>activity_score</i> "
        "memiliki korelasi terhadap target yang kompetitif dibanding fitur asli, mengindikasikan keberhasilan "
        "menangkap pola laten pada variabel mentah.<br>"
        "<b>2. Distribusi Stres</b> — Mayoritas pengguna berada pada tingkat Stres Sedang hingga Tinggi, "
        "memperkuat relevansi MindCare sebagai platform intervensi bagi kelompok yang memiliki kebutuhan "
        "nyata terhadap rekomendasi wellness.<br>"
        "<b>3. Pola Aktivitas</b> — Journaling dominan pada Stres Tinggi; membaca lebih sering pada Stres "
        "Rendah; olahraga terdistribusi merata. Rekomendasi tidak dapat generik — personalisasi berdasarkan "
        "kondisi psikologis diperlukan.<br>"
        "<b>4. Psychological Score</b> — Pengguna journaling cenderung memiliki skor psikologis lebih tinggi "
        "dibanding pengguna olahraga, memvalidasi kemampuan diskriminatif fitur engineered dalam membedakan "
        "pola kebutuhan antar pengguna.<br>"
        "<b>5. Wellbeing Index</b> — Pengguna olahraga memiliki rata-rata wellbeing index lebih tinggi "
        "(kondisi lebih stabil), sementara pengguna journaling menunjukkan kebutuhan refleksi psikologis "
        "lebih dominan — validasi empiris bahwa indeks ini menjadi sinyal penting dalam personalisasi.<br>"
        "<b>6. A/B Testing</b> — Performa Model A dan Model B saling bersilangan antar-fold tanpa dominasi "
        "konsisten. H₀ tidak ditolak (p = 0,1058), delta F1 = −0,07% — tidak terdapat perbedaan signifikan "
        "secara statistik maupun praktis.<br><br>"
        "Secara keseluruhan, dataset MindCare memiliki kualitas baik, pola hubungan antarvariabel yang "
        "bermakna, serta indikasi kuat bahwa personalisasi berbasis kondisi psikologis dan gaya hidup "
        "memang diperlukan. Feature engineering terbukti memberikan nilai tambah, sementara heterogenitas "
        "kebutuhan antar kategori stres memberikan landasan kuat untuk pengembangan model rekomendasi "
        "yang lebih adaptif, akurat, dan relevan."
    )

    # ==== Footer ====
    st.markdown("""
    <div style="margin-top:2.5rem; padding:1.2rem 1.5rem;
                background:linear-gradient(135deg,#0D1B3E,#1565C0);
                border-radius:14px; text-align:center;">
        <div style="font-size:1rem; font-weight:700; color:white; letter-spacing:-0.01em;
                    font-family:'DM Serif Display',Georgia,serif; margin-bottom:0.3rem;">
            MindCare Analytics Dashboard
        </div>
        <div style="font-size:0.75rem; color:#93C5FD; font-weight:400;">
            Coding Camp 2026 powered by DBS Foundation &nbsp;·&nbsp;
            CC26-PSU148 &nbsp;·&nbsp;
            Iqbal Nurul Fadli &amp; Raihan Putra Permana
        </div>
    </div>
    """, unsafe_allow_html=True)
