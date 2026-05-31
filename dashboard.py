"""
MindCare — Dashboard Analitik
Coding Camp 2026 powered by DBS Foundation | CC26-PSU148
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MindCare Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# TEMA & STYLE
# ─────────────────────────────────────────────────────────────────────────────
COLORS = {
    "primary":   "#1565C0",
    "secondary": "#1976D2",
    "accent":    "#42A5F5",
    "light":     "#90CAF9",
    "pos":       "#2E7D32",
    "neg":       "#C62828",
    "warn":      "#E65100",
    "journaling":"#1565C0",
    "membaca":   "#1976D2",
    "olahraga":  "#42A5F5",
    "bg_card":   "#F8FAFF",
}

PALETTE_ACT = ["#1565C0", "#1976D2", "#42A5F5"]
PALETTE_STRESS = ["#E3F2FD", "#90CAF9", "#42A5F5", "#1976D2", "#0D47A1"]

st.markdown("""
<style>
    /* Global */
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    h1, h2, h3 { font-family: 'Georgia', serif; }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border: 1px solid #E3E8F0;
        border-left: 4px solid #1565C0;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #1565C0;
        line-height: 1;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
    }
    
    /* Section headers */
    .section-header {
        border-bottom: 2px solid #1565C0;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
        color: #1565C0;
        font-size: 1rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Insight box */
    .insight-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.85rem;
        color: #1E3A5F;
        line-height: 1.6;
        margin-top: 0.5rem;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #F0F4FF;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label {
        font-size: 0.78rem;
        font-weight: 600;
        color: #374151;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 2px solid #E5E7EB;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.82rem;
        font-weight: 600;
        padding: 0.5rem 1rem;
        color: #6B7280;
    }
    .stTabs [aria-selected="true"] {
        color: #1565C0 !important;
        border-bottom: 2px solid #1565C0 !important;
    }
    
    /* Hide default streamlit footer */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
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


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────
def card(label: str, value: str, sub: str = "") -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {"<div class='metric-sub'>" + sub + "</div>" if sub else ""}
    </div>
    """

def insight(text: str):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def section_header(text: str):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    font=dict(family="Arial, sans-serif", size=12),
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20, r=20, t=40, b=20),
    title_font=dict(size=13, color="#1E3A5F"),
)


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTER GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### MindCare Analytics")
    st.markdown("---")
    st.markdown("**Filter Data**")

    # Stress level
    stress_opts = sorted(df["stress_level_1_5"].unique())
    stress_sel  = st.multiselect(
        "Stress Level",
        options=stress_opts,
        default=stress_opts,
        format_func=lambda x: f"Level {x}",
    )

    # Gender
    gender_opts = df["jenis_kelamin"].unique().tolist()
    gender_sel  = st.multiselect(
        "Jenis Kelamin",
        options=gender_opts,
        default=gender_opts,
    )

    # Penyebab stres
    cause_opts = df["penyebab_stres"].unique().tolist()
    cause_sel  = st.multiselect(
        "Penyebab Stres",
        options=cause_opts,
        default=cause_opts,
    )

    # Usia
    age_min, age_max = int(df["umur"].min()), int(df["umur"].max())
    age_range = st.slider("Rentang Usia", age_min, age_max, (age_min, age_max))

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.72rem; color:#6B7280;'>"
        "Coding Camp 2026 — DBS Foundation<br>"
        "CC26-PSU148</div>",
        unsafe_allow_html=True
    )

# Terapkan filter
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


# ─────────────────────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='color:#1565C0; font-size:1.7rem; margin-bottom:0.1rem;'>"
    "MindCare — Dashboard Analitik Kesehatan Mental"
    "</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color:#6B7280; font-size:0.85rem; margin-bottom:1.2rem;'>"
    "Analisis data berbasis 10.716 responden dari tiga sumber dataset | "
    "Coding Camp 2026 powered by DBS Foundation"
    "</p>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)

avg_stress = dff["stress_level_1_5"].mean()
pct_high_stress = (dff["stress_level_1_5"] >= 4).mean() * 100
avg_anxiety = dff["anxiety_score"].mean()
avg_sleep   = dff["kualitas_tidur_1_5"].mean()
top_act     = dff["aktivitas_dipilih"].value_counts().idxmax()
top_act_pct = dff["aktivitas_dipilih"].value_counts(normalize=True).max() * 100

with k1:
    st.markdown(card("Total Responden", f"{len(dff):,}", f"dari {len(df):,} data"), unsafe_allow_html=True)
with k2:
    st.markdown(card("Rata-rata Stress Level", f"{avg_stress:.2f}", "Skala 1–5"), unsafe_allow_html=True)
with k3:
    st.markdown(card("Stres Tinggi (≥4)", f"{pct_high_stress:.1f}%", "Proporsi responden"), unsafe_allow_html=True)
with k4:
    st.markdown(card("Rata-rata Anxiety Score", f"{avg_anxiety:.1f}", "Skala 0–21"), unsafe_allow_html=True)
with k5:
    st.markdown(card("Aktivitas Dominan", top_act.title(), f"{top_act_pct:.1f}% dari total"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB NAVIGASI
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Profil & Demografi",
    "Faktor Psikologis & Gaya Hidup",
    "Rekomendasi Aktivitas",
    "Ringkasan Temuan",
])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — PROFIL & DEMOGRAFI
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    row1_l, row1_r = st.columns(2)

    # --- Distribusi Stress Level ---
    with row1_l:
        section_header("Distribusi Tingkat Stres")
        stress_dist = dff["stress_level_1_5"].value_counts().sort_index().reset_index()
        stress_dist.columns = ["Stress Level", "Jumlah"]
        stress_dist["Label"] = stress_dist["Stress Level"].map(
            {1: "Sangat Rendah", 2: "Rendah", 3: "Sedang", 4: "Tinggi", 5: "Sangat Tinggi"}
        )
        fig = px.bar(
            stress_dist, x="Stress Level", y="Jumlah",
            color="Jumlah", color_continuous_scale=["#E3F2FD", "#1565C0"],
            text="Jumlah",
            custom_data=["Label"],
        )
        fig.update_traces(
            texttemplate="%{y:,}",
            textposition="outside",
            hovertemplate="<b>Level %{x}</b>: %{customdata[0]}<br>Jumlah: %{y:,}<extra></extra>",
        )
        fig.update_layout(
            **PLOTLY_LAYOUT,
            title="Stress Level Responden",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Tingkat Stres (1 = Sangat Rendah, 5 = Sangat Tinggi)",
            yaxis_title="Jumlah Responden",
        )
        st.plotly_chart(fig, width="stretch")
        insight(
            "Konsentrasi terbesar berada di <b>level 3–4</b>, menunjukkan mayoritas responden "
            "mengalami stres menengah hingga tinggi. Level 5 (sangat tinggi) ditemukan pada "
            f"<b>{(dff['stress_level_1_5']==5).sum():,} responden</b> dalam data yang difilter."
        )

    # --- Distribusi Penyebab Stres ---
    with row1_r:
        section_header("Penyebab Stres")
        cause_dist = dff["penyebab_stres"].value_counts().reset_index()
        cause_dist.columns = ["Penyebab", "Jumlah"]
        cause_dist["Persen"] = (cause_dist["Jumlah"] / cause_dist["Jumlah"].sum() * 100).round(1)
        fig2 = px.bar(
            cause_dist.sort_values("Jumlah"),
            x="Jumlah", y="Penyebab",
            orientation="h",
            color="Jumlah", color_continuous_scale=["#90CAF9", "#1565C0"],
            text="Persen",
        )
        fig2.update_traces(
            texttemplate="%{text}%",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Jumlah: %{x:,}<extra></extra>",
        )
        fig2.update_layout(
            **PLOTLY_LAYOUT,
            title="Distribusi Penyebab Stres",
            showlegend=False,
            coloraxis_showscale=False,
            xaxis_title="Jumlah Responden",
            yaxis_title="",
        )
        st.plotly_chart(fig2, width="stretch")
        top_cause = cause_dist.iloc[0]
        insight(
            f"<b>{top_cause['Penyebab']}</b> menjadi penyebab stres paling dominan "
            f"({top_cause['Persen']}%). Faktor pekerjaan dan keuangan mengikuti di posisi selanjutnya, "
            "mencerminkan tekanan multidimensional yang dihadapi responden."
        )

    row2_l, row2_r = st.columns(2)

    # --- Stres Berdasarkan Pekerjaan ---
    with row2_l:
        section_header("Rata-rata Stress Level per Pekerjaan")
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
            color_continuous_scale=["#E3F2FD", "#1565C0"],
            text="Avg Stress",
        )
        fig3.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Rata-rata: %{x:.2f}<extra></extra>",
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
        st.plotly_chart(fig3, width="stretch")

    # --- Distribusi Usia per Stress Level ---
    with row2_r:
        section_header("Distribusi Usia per Tingkat Stres")
        fig4 = go.Figure()
        palette_stress = ["#E3F2FD", "#90CAF9", "#42A5F5", "#1976D2", "#0D47A1"]
        for i, lvl in enumerate(sorted(dff["stress_level_1_5"].unique())):
            subset = dff[dff["stress_level_1_5"] == lvl]["umur"]
            fig4.add_trace(go.Box(
                y=subset,
                name=f"Level {lvl}",
                marker_color=palette_stress[i % len(palette_stress)],
                boxmean=True,
                hovertemplate=f"<b>Level {lvl}</b><br>%{{y}} tahun<extra></extra>",
            ))
        fig4.update_layout(
            **PLOTLY_LAYOUT,
            title="Distribusi Usia per Stress Level",
            yaxis_title="Usia (tahun)",
            xaxis_title="Tingkat Stres",
            showlegend=False,
            height=420,
        )
        st.plotly_chart(fig4, width="stretch")

    insight(
        "Tidak terdapat pola usia yang konsisten dan linier terhadap tingkat stres — stres tinggi "
        "dijumpai di hampir seluruh kelompok usia, menunjukkan bahwa stres bersifat lintas generasi "
        "dan lebih dipengaruhi oleh faktor konteks (pekerjaan, akademik, sosial)."
    )

    # --- Gender breakdown ---
    section_header("Profil Gender")
    gc1, gc2 = st.columns(2)
    with gc1:
        gender_stress = dff.groupby("jenis_kelamin")["stress_level_1_5"].mean().reset_index()
        gender_stress.columns = ["Gender", "Avg Stress"]
        fig_g1 = px.bar(
            gender_stress, x="Gender", y="Avg Stress",
            color="Gender",
            color_discrete_map={"Male": "#1976D2", "Female": "#42A5F5"},
            text="Avg Stress",
        )
        fig_g1.update_traces(texttemplate="%{y:.2f}", textposition="outside")
        fig_g1.update_layout(
            **PLOTLY_LAYOUT, title="Rata-rata Stress per Gender",
            showlegend=False, yaxis_range=[0, 5],
        )
        st.plotly_chart(fig_g1, width="stretch")

    with gc2:
        gender_act = dff.groupby(["jenis_kelamin", "aktivitas_dipilih"]).size().reset_index(name="n")
        gender_act["pct"] = gender_act.groupby("jenis_kelamin")["n"].transform(lambda x: x / x.sum() * 100)
        fig_g2 = px.bar(
            gender_act, x="jenis_kelamin", y="pct", color="aktivitas_dipilih",
            color_discrete_map={"journaling": "#1565C0", "membaca": "#1976D2", "olahraga": "#42A5F5"},
            text="pct",
            barmode="group",
        )
        fig_g2.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
        fig_g2.update_layout(
            **PLOTLY_LAYOUT, title="Preferensi Aktivitas per Gender",
            xaxis_title="", yaxis_title="Proporsi (%)",
            legend_title="Aktivitas", yaxis_range=[0, 75],
        )
        st.plotly_chart(fig_g2, width="stretch")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — FAKTOR PSIKOLOGIS & GAYA HIDUP
# ═════════════════════════════════════════════════════════════════════════════
with tab2:

    # --- BQ1: Skor Psikologis vs Stress Level ---
    section_header("BQ1 — Faktor Psikologis vs Tingkat Stres")
    p1, p2, p3 = st.columns(3)

    psych_metrics = [
        ("anxiety_score",     "Anxiety Score (0–21)",     p1),
        ("depression_score",  "Depression Score (0–27)",  p2),
        ("self_esteem_score", "Self-Esteem Score (0–30)", p3),
    ]

    for col, label, container in psych_metrics:
        agg = dff.groupby("stress_level_1_5")[col].mean().reset_index()
        agg.columns = ["Stress Level", "Nilai"]
        with container:
            fig = px.line(
                agg, x="Stress Level", y="Nilai",
                markers=True,
                color_discrete_sequence=["#1565C0"],
            )
            fig.update_traces(
                line_width=2.5,
                marker_size=8,
                hovertemplate="<b>Level %{x}</b><br>Rata-rata: %{y:.2f}<extra></extra>",
            )
            fig.update_layout(
                **PLOTLY_LAYOUT,
                title=label,
                xaxis_title="Stress Level",
                yaxis_title="Rata-rata Skor",
                height=280,
            )
            st.plotly_chart(fig, width="stretch")

    insight(
        "<b>Anxiety Score</b> menunjukkan kenaikan paling tajam seiring meningkatnya stress level "
        "(effect size η² tertinggi). Depression score bergerak paralel, sedangkan self-esteem "
        "turun secara konsisten — mengkonfirmasi bahwa stres tinggi berkaitan erat dengan penurunan "
        "rasa percaya diri."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BQ2: Kualitas Tidur & Aktivitas Fisik ---
    section_header("BQ2 — Gaya Hidup vs Tingkat Stres")
    b2l, b2r = st.columns(2)

    with b2l:
        sleep_stress = dff.groupby("kualitas_tidur_1_5")["stress_level_1_5"].mean().reset_index()
        sleep_stress.columns = ["Kualitas Tidur", "Avg Stress"]
        fig_sl = px.bar(
            sleep_stress, x="Kualitas Tidur", y="Avg Stress",
            color="Avg Stress", color_continuous_scale=["#1565C0", "#E3F2FD"],
            text="Avg Stress",
        )
        fig_sl.update_traces(texttemplate="%{y:.2f}", textposition="outside")
        fig_sl.update_layout(
            **PLOTLY_LAYOUT,
            title="Kualitas Tidur vs Rata-rata Stress Level",
            xaxis_title="Kualitas Tidur (1 = Buruk, 5 = Sangat Baik)",
            yaxis_title="Rata-rata Stress Level",
            yaxis_range=[0, 5.5],
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_sl, width="stretch")

    with b2r:
        # Scatter: aktivitas fisik vs stress level
        act_stress = dff.groupby("stress_level_1_5")["aktivitas_fisik_mnt"].mean().reset_index()
        act_stress.columns = ["Stress Level", "Avg Aktivitas (mnt)"]
        fig_af = px.bar(
            act_stress, x="Stress Level", y="Avg Aktivitas (mnt)",
            color="Avg Aktivitas (mnt)", color_continuous_scale=["#E3F2FD", "#1565C0"],
            text="Avg Aktivitas (mnt)",
        )
        fig_af.update_traces(texttemplate="%{y:.1f}", textposition="outside")
        fig_af.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Aktivitas Fisik per Stress Level",
            xaxis_title="Stress Level",
            yaxis_title="Aktivitas Fisik (menit/hari)",
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_af, width="stretch")

    insight(
        "<b>Korelasi negatif jelas</b>: semakin buruk kualitas tidur → semakin tinggi stress level. "
        "Responden dengan kualitas tidur = 1 memiliki rata-rata stress level 4.27, sementara "
        "kualitas tidur = 5 turun ke 2.04. Pola serupa berlaku pada aktivitas fisik — kelompok "
        "dengan stres tinggi rata-rata berolahraga lebih sedikit per hari."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Durasi Tidur ---
    section_header("Pola Durasi Tidur per Tingkat Stres")
    fig_sleep_dur = go.Figure()
    for i, lvl in enumerate(sorted(dff["stress_level_1_5"].unique())):
        subset = dff[dff["stress_level_1_5"] == lvl]["durasi_tidur_jam"]
        fig_sleep_dur.add_trace(go.Violin(
            y=subset,
            name=f"Level {lvl}",
            box_visible=True,
            meanline_visible=True,
            fillcolor=PALETTE_STRESS[i % 5],
            opacity=0.8,
            line_color="#1565C0",
        ))
    fig_sleep_dur.update_layout(
        **PLOTLY_LAYOUT,
        title="Distribusi Durasi Tidur per Stress Level",
        yaxis_title="Durasi Tidur (jam)",
        xaxis_title="",
        showlegend=False,
        height=320,
    )
    st.plotly_chart(fig_sleep_dur, width="stretch")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — REKOMENDASI AKTIVITAS
# ═════════════════════════════════════════════════════════════════════════════
with tab3:

    # --- BQ3: Distribusi Aktivitas per Stress Level ---
    section_header("BQ3 — Distribusi Aktivitas per Tingkat Stres")
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
    fig_cross.update_traces(texttemplate="%{y:.1f}%", textposition="inside", textfont_size=11)
    fig_cross.update_layout(
        **PLOTLY_LAYOUT,
        title="Proporsi Aktivitas yang Dipilih per Stress Level",
        xaxis_title="",
        yaxis_title="Proporsi (%)",
        legend_title="Aktivitas",
        yaxis_range=[0, 105],
    )
    st.plotly_chart(fig_cross, width="stretch")
    insight(
        "<b>Pergeseran pola aktivitas seiring kenaikan stres sangat signifikan:</b><br>"
        "Level 1–2: Olahraga dominan (~40–44%) — pengguna aktif secara fisik.<br>"
        "Level 3: Membaca mengambil alih posisi dominan (~60%).<br>"
        "Level 4–5: Journaling melonjak hingga 43–71% — mencerminkan kebutuhan pemrosesan emosi mendalam "
        "pada stres tinggi."
    )

    st.markdown("<br>", unsafe_allow_html=True)
    a3_l, a3_r = st.columns(2)

    # --- BQ4: Profil Psikologis per Aktivitas ---
    with a3_l:
        section_header("BQ4 — Profil Psikologis per Aktivitas")
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
        fig_psych.update_traces(texttemplate="%{y:.1f}", textposition="outside")
        fig_psych.update_layout(
            **PLOTLY_LAYOUT,
            title="Skor Psikologis Rata-rata per Aktivitas",
            xaxis_title="Aktivitas",
            yaxis_title="Rata-rata Skor",
            legend_title="Metrik",
        )
        st.plotly_chart(fig_psych, width="stretch")
        insight(
            "Pengguna yang memilih <b>journaling</b> memiliki anxiety (12.05) dan depression (12.64) "
            "tertinggi, serta self-esteem terendah (16.25). <b>Olahraga</b> dipilih oleh responden "
            "dengan kondisi psikologis paling sehat — mengkonfirmasi journaling sebagai intervensi "
            "untuk kondisi psikologis yang lebih berat."
        )

    # --- BQ5: Durasi Aktivitas ---
    with a3_r:
        section_header("BQ5 — Durasi Rekomendasi per Aktivitas")
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
        fig_dur.update_traces(texttemplate="%{y:.1f} mnt", textposition="outside")
        fig_dur.update_layout(
            **PLOTLY_LAYOUT,
            title="Rata-rata Durasi Rekomendasi per Aktivitas",
            xaxis_title="",
            yaxis_title="Durasi (menit)",
            showlegend=False,
            yaxis_range=[0, 60],
        )
        st.plotly_chart(fig_dur, width="stretch")

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
        fig_wl.update_traces(texttemplate="%{y:.1f} mnt", textposition="outside")
        fig_wl.update_layout(
            **PLOTLY_LAYOUT,
            title="Pengaruh Waktu Luang terhadap Durasi Rekomendasi",
            showlegend=False,
            yaxis_range=[0, 55],
        )
        st.plotly_chart(fig_wl, width="stretch")
        insight(
            "Waktu luang <b>> 90 menit</b> secara konsisten menghasilkan rekomendasi durasi lebih panjang. "
            "Ini mengindikasikan sistem rekomendasi MindCare menyesuaikan intensitas intervensi "
            "dengan ketersediaan waktu pengguna."
        )

    # --- Heatmap Aktivitas x Tujuan ---
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Tujuan Utama per Jenis Aktivitas")
    heat_data = (
        pd.crosstab(dff["aktivitas_dipilih"], dff["tujuan_utama"], normalize="index") * 100
    ).round(1)
    fig_heat = px.imshow(
        heat_data,
        color_continuous_scale=["white", "#1565C0"],
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
    st.plotly_chart(fig_heat, width="stretch")


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — RINGKASAN TEMUAN
# ═════════════════════════════════════════════════════════════════════════════
with tab4:

    section_header("Ringkasan Business Questions & Temuan Kunci")

    findings = [
        ("BQ1 — Faktor Psikologis",
         "Anxiety Score",
         "Prediktor terkuat tingkat stres (η² tertinggi). Naik secara konsisten dari level 1 → 5. "
         "Depression score bergerak paralel; self-esteem turun linear."),
        ("BQ2 — Gaya Hidup",
         "Tidur & Aktivitas Fisik",
         "Kualitas tidur rendah (≤2) berkorelasi dengan stress level ≥4. "
         "Responden stres tinggi berolahraga lebih sedikit per hari."),
        ("BQ3 — Distribusi Aktivitas",
         "Stress Level vs Aktivitas",
         "Olahraga dominan di level rendah (1–2). Journaling meningkat drastis di level 4–5 "
         "(hingga 70.9%), menggantikan membaca dan olahraga."),
        ("BQ4 — Intervensi Psikologis",
         "Journaling sebagai Intervensi",
         "Pengguna journaling memiliki anxiety (12.05) dan depression (12.64) tertinggi, "
         "mengkonfirmasi journaling sebagai intervensi untuk kondisi psikologis berat."),
        ("BQ5 — Durasi & Komitmen",
         "Waktu Luang > 90 Menit",
         "Rekomendasi durasi lebih panjang secara konsisten pada kelompok waktu luang > 90 menit, "
         "menunjukkan penyesuaian sistem terhadap ketersediaan waktu."),
        ("BQ6 — Feature Selection",
         "Fitur Preferensi + Psikologis",
         "Kolom preferensi (olahraga, baca, jurnal) dan skor psikologis memiliki korelasi |r| ≥ 0.15 "
         "terhadap target — fitur paling relevan untuk model KNN."),
    ]

    for bq, key, desc in findings:
        with st.expander(f"{bq} — {key}", expanded=True):
            st.markdown(
                f"<div style='font-size:0.875rem; line-height:1.7; color:#374151;'>{desc}</div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Statistik Kualitas Dataset")

    cols = st.columns(4)
    stats_items = [
        ("Data Raw", "11.200", "baris awal"),
        ("Data Cleaned", "10.716", "setelah dedup & cleaning"),
        ("Duplikat Dihapus", "359", "3.21% dari total"),
        ("Missing Values", "0", "setelah imputasi"),
    ]
    for col_st, (lbl, val, sub) in zip(cols, stats_items):
        with col_st:
            st.markdown(card(lbl, val, sub), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Distribusi Sumber Dataset")

    src_dist = dff["source"].value_counts().reset_index()
    src_dist.columns = ["Sumber", "Jumlah"]
    src_dist["Persen"] = (src_dist["Jumlah"] / src_dist["Jumlah"].sum() * 100).round(1)
    fig_src = px.pie(
        src_dist, values="Jumlah", names="Sumber",
        color_discrete_sequence=["#1565C0", "#1976D2", "#42A5F5"],
        hole=0.5,
    )
    fig_src.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value:,} responden (%{percent})<extra></extra>",
    )
    fig_src.update_layout(
        **PLOTLY_LAYOUT,
        title="Komposisi Sumber Data",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        height=320,
    )
    st.plotly_chart(fig_src, width="stretch")

    insight(
        "Dataset MindCare menggabungkan tiga sumber dengan karakteristik berbeda: "
        "<b>StudentCopingMechanisms</b> (fokus coping & beban akademik), "
        "<b>StudentStressFactors</b> (faktor stres akademik, sosial, ekonomi), dan "
        "<b>SleepHealthLifestyle</b> (pola tidur & gaya hidup). "
        "Keberagaman sumber memperkuat generalisasi temuan."
    )

    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#9CA3AF; font-size:0.78rem; padding:0.5rem;'>"
        "MindCare Analytics Dashboard — Coding Camp 2026 powered by DBS Foundation | "
        "CC26-PSU148 — Iqbal Nurul Fadli & Raihan Putra Permana"
        "</div>",
        unsafe_allow_html=True
    )
