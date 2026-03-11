import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Seminar/Home.py
STYLE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

:root {
    --bg:       #0f0f0f;
    --surface:  #1a1a1a;
    --border:   #2e2e2e;
    --accent:   #ff5c00;
    --accent2:  #ffb347;
    --text:     #e8e8e8;
    --muted:    #888;
    --success:  #3ecf8e;
    --mono:     'IBM Plex Mono', monospace;
    --display:  'Syne', sans-serif;
    --body:     'DM Sans', sans-serif;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--body) !important;
}

h1, h2, h3, h4 {
    font-family: var(--display) !important;
    color: var(--text) !important;
    letter-spacing: -0.5px;
}

[data-testid="stSidebar"] {
    background-color: #141414 !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
.stAlert p { color: #0f0f0f !important; }

.hero {
    border-top: 4px solid var(--accent);
    background: var(--surface);
    padding: 48px 52px;
    border-radius: 4px;
    margin-bottom: 40px;
}
.hero-label {
    font-family: var(--mono);
    font-size: 12px;
    color: var(--accent);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.hero-title {
    font-family: var(--display);
    font-size: 64px;
    font-weight: 800;
    color: var(--text);
    line-height: 1;
    margin: 0 0 16px 0;
}
.hero-sub {
    font-size: 17px;
    color: #aaa;
    max-width: 600px;
    line-height: 1.6;
}

.sec-header {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--accent);
    margin: 44px 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}

.stat-row {
    display: flex;
    gap: 14px;
    margin-top: 16px;
    flex-wrap: wrap;
}
.stat-pill {
    background: #1f1f1f;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 12px 20px;
    text-align: center;
    min-width: 110px;
}
.stat-pill .sv {
    font-family: var(--display);
    font-size: 26px;
    color: var(--accent);
    line-height: 1;
}
.stat-pill .sl {
    font-family: var(--mono);
    font-size: 10px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 4px;
}

.upload-prompt {
    border: 1.5px dashed #3a3a3a;
    border-radius: 6px;
    padding: 32px;
    text-align: center;
    color: #666;
    font-size: 15px;
    margin: 16px 0;
}
.upload-prompt strong { color: var(--accent); }

.ok-banner {
    background: #0f2a1e;
    border: 1px solid #1e5c3a;
    border-left: 4px solid var(--success);
    border-radius: 4px;
    padding: 18px 24px;
    color: #a8eecb;
    font-size: 15px;
    line-height: 1.6;
}
.ok-banner strong { color: var(--success); }
</style>
"""

# ── App setup ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Productivity Dashboard",
    layout="wide"
)
st.markdown(STYLE_CSS, unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">AI Productivity</div>
    <div class="hero-title">AI Productivity<br>Dashboard</div>
    <div class="hero-sub">
        Upload a CSV with job roles, AI tool usage, productivity scores and more.
        Explore metrics, filter by role and pressure level, and view interactive charts.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Data loading ───────────────────────────────────────────────────
st.markdown('<div class="sec-header">Dataset Preview</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload a CSV file",
    type=["csv"],
    help="Upload your AI productivity dataset (CSV)"
)

if uploaded_file is None:
    st.markdown(
        '<div class="upload-prompt">Upload a <strong>CSV file</strong> to get started</div>',
        unsafe_allow_html=True
    )
    st.stop()

df = pd.read_csv(uploaded_file)
st.dataframe(df.head(10), use_container_width=True)

# ── Metrics section ─────────────────────────────────────────────────
st.markdown('<div class="sec-header">Metrics</div>', unsafe_allow_html=True)

total_records = len(df)
avg_productivity = df["productivity_score"].mean() if "productivity_score" in df.columns else 0
avg_ai_hours = df["ai_tool_usage_hours_per_week"].mean() if "ai_tool_usage_hours_per_week" in df.columns else 0

st.markdown(f"""
<div class="stat-row">
    <div class="stat-pill"><div class="sv">{total_records}</div><div class="sl">Total records</div></div>
    <div class="stat-pill"><div class="sv">{avg_productivity:.1f}</div><div class="sl">Avg productivity score</div></div>
    <div class="stat-pill"><div class="sv">{avg_ai_hours:.1f}</div><div class="sl">Avg AI hours/week</div></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar filters ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### Filters")
    st.markdown("---")

    job_roles = df["job_role"].unique().tolist() if "job_role" in df.columns else []
    selected_roles = st.multiselect(
        "Job role",
        options=job_roles,
        default=job_roles,
        help="Select one or more job roles"
    )

    pressure_options = ["All"] + (
        df["deadline_pressure_level"].astype(str).unique().tolist()
        if "deadline_pressure_level" in df.columns else []
    )
    selected_pressure = st.selectbox(
        "Deadline pressure level",
        options=pressure_options,
        help="Filter by deadline pressure level"
    )

df_filtered = df.copy()
if "job_role" in df_filtered.columns and selected_roles:
    df_filtered = df_filtered[df_filtered["job_role"].isin(selected_roles)]
if "deadline_pressure_level" in df_filtered.columns and selected_pressure != "All":
    df_filtered = df_filtered[df_filtered["deadline_pressure_level"].astype(str) == selected_pressure]

# ── Key Insights ──────────────────────────────────────────────────
st.markdown('<div class="sec-header">Key Insights</div>', unsafe_allow_html=True)

insight_col1, insight_col2, insight_col3, insight_col4 = st.columns(4)

with insight_col1:
    avg_burnout = df_filtered["burnout_risk_score"].mean() if "burnout_risk_score" in df_filtered.columns else 0
    st.metric("Average burnout risk score", f"{avg_burnout:.1f}")

with insight_col2:
    avg_focus = df_filtered["focus_hours_per_day"].mean() if "focus_hours_per_day" in df_filtered.columns else 0
    st.metric("Average focus hours per day", f"{avg_focus:.1f}")

with insight_col3:
    avg_tasks_auto = df_filtered["tasks_automated_percent"].mean() if "tasks_automated_percent" in df_filtered.columns else 0
    st.metric("Average tasks automated %", f"{avg_tasks_auto:.1f}%")

with insight_col4:
    avg_wlb = df_filtered["work_life_balance_score"].mean() if "work_life_balance_score" in df_filtered.columns else 0
    st.metric("Average work-life balance score", f"{avg_wlb:.1f}")

if "ai_tool_usage_hours_per_week" in df_filtered.columns and "productivity_score" in df_filtered.columns:
    corr = df_filtered["ai_tool_usage_hours_per_week"].corr(df_filtered["productivity_score"])
    st.markdown(f"**Correlation between AI usage and productivity:** {corr:.2f}")

# ── Productivity by Job Role (Plotly) ─────────────────────────────
st.markdown('<div class="sec-header">Productivity by Job Role</div>', unsafe_allow_html=True)

if "job_role" in df_filtered.columns and "productivity_score" in df_filtered.columns:
    avg_by_role = (
        df_filtered.groupby("job_role", as_index=False)["productivity_score"]
        .mean()
        .sort_values("productivity_score", ascending=False)
    )
    fig_bar = px.bar(
        avg_by_role,
        x="job_role",
        y="productivity_score",
        title="Average productivity score by job role",
        labels={"job_role": "Job role", "productivity_score": "Average productivity score"},
        color="productivity_score",
        color_continuous_scale=["#1a1a1a", "#ff5c00"]
    )
    fig_bar.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15,15,15,1)",
        plot_bgcolor="rgba(26,26,26,1)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="#2e2e2e"),
        yaxis=dict(gridcolor="#2e2e2e"),
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Dataset must contain 'job_role' and 'productivity_score' for this chart.")

# ── Productivity Distribution (Matplotlib) ────────────────────────
st.markdown('<div class="sec-header">Productivity Distribution</div>', unsafe_allow_html=True)

if "productivity_score" in df_filtered.columns:
    fig_hist, ax = plt.subplots(figsize=(10, 5))
    ax.hist(
        df_filtered["productivity_score"].dropna(),
        bins=20,
        color="#ff5c00",
        edgecolor="#2e2e2e",
        alpha=0.85
    )
    ax.set_xlabel("Productivity score", color="#e8e8e8", fontsize=12)
    ax.set_ylabel("Frequency", color="#e8e8e8", fontsize=12)
    ax.set_title("Distribution of productivity score", color="#e8e8e8", fontsize=14)
    ax.tick_params(colors="#888")
    ax.spines["bottom"].set_color("#2e2e2e")
    ax.spines["top"].set_color("#2e2e2e")
    ax.spines["left"].set_color("#2e2e2e")
    ax.spines["right"].set_color("#2e2e2e")
    fig_hist.patch.set_facecolor("#0f0f0f")
    ax.set_facecolor("#1a1a1a")
    plt.tight_layout()
    st.pyplot(fig_hist)
    plt.close()
else:
    st.warning("Dataset must contain 'productivity_score' for this chart.")

# ── AI Usage vs Productivity (Plotly scatter) ──────────────────────
st.markdown('<div class="sec-header">AI Usage vs Productivity</div>', unsafe_allow_html=True)

if all(c in df_filtered.columns for c in ["ai_tool_usage_hours_per_week", "productivity_score", "job_role"]):
    fig_scatter_ai = px.scatter(
        df_filtered,
        x="ai_tool_usage_hours_per_week",
        y="productivity_score",
        color="job_role",
        title="AI Usage vs Productivity",
        labels={
            "ai_tool_usage_hours_per_week": "AI tool usage (hours/week)",
            "productivity_score": "Productivity score",
            "job_role": "Job role"
        }
    )
    fig_scatter_ai.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15,15,15,1)",
        plot_bgcolor="rgba(26,26,26,1)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="#2e2e2e"),
        yaxis=dict(gridcolor="#2e2e2e")
    )
    st.plotly_chart(fig_scatter_ai, use_container_width=True)
else:
    st.warning("Dataset must contain 'ai_tool_usage_hours_per_week', 'productivity_score', and 'job_role' for this chart.")

# ── Burnout vs Productivity (Plotly scatter) ──────────────────────
st.markdown('<div class="sec-header">Burnout vs Productivity</div>', unsafe_allow_html=True)

if all(c in df_filtered.columns for c in ["burnout_risk_score", "productivity_score", "deadline_pressure_level"]):
    fig_scatter_burnout = px.scatter(
        df_filtered,
        x="burnout_risk_score",
        y="productivity_score",
        color="deadline_pressure_level",
        title="Burnout Risk vs Productivity",
        labels={
            "burnout_risk_score": "Burnout risk score",
            "productivity_score": "Productivity score",
            "deadline_pressure_level": "Deadline pressure"
        }
    )
    fig_scatter_burnout.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(15,15,15,1)",
        plot_bgcolor="rgba(26,26,26,1)",
        font=dict(color="#e8e8e8"),
        xaxis=dict(gridcolor="#2e2e2e"),
        yaxis=dict(gridcolor="#2e2e2e")
    )
    st.plotly_chart(fig_scatter_burnout, use_container_width=True)
else:
    st.warning("Dataset must contain 'burnout_risk_score', 'productivity_score', and 'deadline_pressure_level' for this chart.")
