"""
Football Player Performance Analytics Dashboard
================================================
⚠️  SYNTHETIC DATA NOTICE: All player statistics in this dashboard are
    computer-generated and do NOT represent real-world football results.
    The dataset was created for demonstration and portfolio purposes only.
"""

import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ─────────────────────────────────────────────
# 1. PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Football Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# 2. THEME / CSS INJECTION
# ─────────────────────────────────────────────
ACCENT = "#00ff87"
BG_DARK = "#0e1117"
SURFACE = "#1e2329"
BORDER = "#2d3748"
TEXT = "#e2e8f0"
MUTED = "#718096"
POS_COLORS = {"GK": "#f6c90e", "DEF": "#3b82f6", "MID": "#a855f7", "FWD": "#ef4444"}

st.markdown(
    f"""
    <style>
        /* Main background */
        .stApp {{ background-color: {BG_DARK}; color: {TEXT}; }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        [data-testid="stSidebar"] * {{ color: {TEXT} !important; }}

        /* KPI cards */
        .kpi-card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-left: 4px solid {ACCENT};
            border-radius: 8px;
            padding: 16px 20px;
            text-align: center;
        }}
        .kpi-label {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: {MUTED};
            margin-bottom: 4px;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 700;
            color: {ACCENT};
            line-height: 1.2;
        }}
        .kpi-sub {{
            font-size: 11px;
            color: {MUTED};
            margin-top: 2px;
        }}

        /* Section headers */
        .section-header {{
            font-size: 18px;
            font-weight: 600;
            color: {ACCENT};
            border-bottom: 1px solid {BORDER};
            padding-bottom: 6px;
            margin: 24px 0 16px 0;
        }}

        /* Dataframe */
        [data-testid="stDataFrame"] {{ background-color: {SURFACE}; }}

        /* Radio buttons */
        [data-testid="stRadio"] label {{ color: {TEXT} !important; }}

        /* Download button */
        .stDownloadButton > button {{
            background-color: {ACCENT};
            color: #000;
            font-weight: 600;
            border: none;
            border-radius: 6px;
        }}
        .stDownloadButton > button:hover {{ opacity: 0.85; }}

        /* Synthetic data banner */
        .synthetic-banner {{
            background: #2d1f00;
            border: 1px solid #f6c90e;
            border-radius: 6px;
            padding: 10px 16px;
            font-size: 13px;
            color: #f6c90e;
            margin-bottom: 20px;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            color: {MUTED};
            font-size: 12px;
            padding: 20px 0 8px 0;
            border-top: 1px solid {BORDER};
            margin-top: 40px;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
# 3. CHART LAYOUT HELPER
# ─────────────────────────────────────────────
def dark_layout(fig, title="", height=420):
    """Apply consistent dark football theme to any Plotly figure."""
    fig.update_layout(
        title=dict(text=title, font=dict(color=TEXT, size=15), x=0),
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(color=TEXT, size=12),
        height=height,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
            bgcolor=SURFACE,
            bordercolor=BORDER,
            font=dict(color=TEXT),
        ),
        xaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=TEXT),
        ),
        yaxis=dict(
            gridcolor=BORDER,
            linecolor=BORDER,
            tickfont=dict(color=MUTED),
            title_font=dict(color=TEXT),
        ),
    )
    return fig


# ─────────────────────────────────────────────
# 4. DATA LOADING
# ─────────────────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "football_players.csv")


@st.cache_data
def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        st.error(
            f"⚠️ Dataset not found at `{CSV_PATH}`. "
            "Please ensure `football_players.csv` is in the same directory as `app.py`."
        )
        st.stop()
    df = pd.read_csv(CSV_PATH)
    # Normalise column types
    df["player_id"] = df["player_id"].astype(int)
    df["age"] = df["age"].astype(int)
    df["rating"] = df["rating"].astype(float)
    df["pass_accuracy"] = df["pass_accuracy"].astype(float)
    return df


# ─────────────────────────────────────────────
# 5. SIDEBAR — NAVIGATION & FILTERS
# ─────────────────────────────────────────────
def build_sidebar(df: pd.DataFrame):
    with st.sidebar:
        st.markdown(
            f"<div style='text-align:center; padding:12px 0;'>"
            f"<span style='font-size:36px'>⚽</span><br>"
            f"<span style='font-size:17px; font-weight:700; color:{ACCENT}'>Football Analytics</span><br>"
            f"<span style='font-size:11px; color:{MUTED}'>Performance Dashboard</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        st.markdown("---")

        page = st.radio(
            "📌 Navigation",
            ["Overview", "Player Analysis", "Team Analysis", "Position Analysis"],
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown(
            f"<span style='font-size:13px; color:{MUTED}; text-transform:uppercase; letter-spacing:1px'>Filters</span>",
            unsafe_allow_html=True,
        )

        seasons = st.multiselect(
            "📅 Season",
            options=sorted(df["season"].unique()),
            default=sorted(df["season"].unique()),
        )
        teams = st.multiselect(
            "🏟️ Team",
            options=sorted(df["team"].unique()),
            default=sorted(df["team"].unique()),
        )
        positions = st.multiselect(
            "🎽 Position",
            options=["GK", "DEF", "MID", "FWD"],
            default=["GK", "DEF", "MID", "FWD"],
        )
        players_in_filter = df[
            df["team"].isin(teams if teams else df["team"].unique()) &
            df["position"].isin(positions if positions else df["position"].unique()) &
            df["season"].isin(seasons if seasons else df["season"].unique())
        ]["player_name"].unique()
        selected_players = st.multiselect(
            "🔍 Player",
            options=sorted(players_in_filter),
            default=[],
            placeholder="All players",
        )

        st.markdown("---")
        st.markdown(
            f"<div style='font-size:11px; color:{MUTED}; padding:4px 0'>"
            f"⚠️ <b>Synthetic data.</b> Stats are computer-generated and do not "
            f"represent real-world results.</div>",
            unsafe_allow_html=True,
        )

    return page, seasons, teams, positions, selected_players


def filter_data(df, seasons, teams, positions, players):
    """Return filtered DataFrame based on sidebar selections (defaults to all)."""
    mask = pd.Series([True] * len(df), index=df.index)
    if seasons:
        mask &= df["season"].isin(seasons)
    if teams:
        mask &= df["team"].isin(teams)
    if positions:
        mask &= df["position"].isin(positions)
    if players:
        mask &= df["player_name"].isin(players)
    return df[mask].copy()


# ─────────────────────────────────────────────
# 6. KPI CARD HELPER
# ─────────────────────────────────────────────
def kpi_card(label: str, value, sub: str = ""):
    sub_html = f"<div class='kpi-sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"<div class='kpi-card'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value'>{value}</div>"
        f"{sub_html}"
        f"</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# 7. PAGE: OVERVIEW
# ─────────────────────────────────────────────
def render_overview(df: pd.DataFrame):
    st.markdown(
        "<div class='synthetic-banner'>"
        "⚠️ <b>SYNTHETIC DATA</b> — All statistics are computer-generated for demonstration purposes only. "
        "They do not represent real-world football results."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## ⚽ Overview")

    # ── KPI Cards ────────────────────────────
    total_players = df["player_id"].nunique()
    total_goals = int(df["goals"].sum())
    total_assists = int(df["assists"].sum())
    total_minutes = int(df["minutes_played"].sum())
    avg_rating = round(float(df["rating"].mean()), 2)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        kpi_card("Total Players", f"{total_players:,}", "unique players")
    with c2:
        kpi_card("Total Goals", f"{total_goals:,}", "across all matches")
    with c3:
        kpi_card("Total Assists", f"{total_assists:,}", "across all matches")
    with c4:
        kpi_card("Minutes Played", f"{total_minutes:,}", "total minutes")
    with c5:
        kpi_card("Avg Rating", f"{avg_rating}", "out of 10.0")

    st.markdown("<div class='section-header'>📊 Top 10 Goal Scorers</div>", unsafe_allow_html=True)

    # ── Top 10 Goal Scorers ───────────────────
    top_scorers = (
        df.groupby(["player_name", "team", "position"], as_index=False)["goals"]
        .sum()
        .sort_values("goals", ascending=False)
        .head(10)
    )
    fig_scorers = px.bar(
        top_scorers,
        x="goals",
        y="player_name",
        orientation="h",
        color="position",
        color_discrete_map=POS_COLORS,
        hover_data={"team": True, "goals": True, "player_name": False},
        labels={"goals": "Goals", "player_name": "Player", "position": "Position"},
    )
    fig_scorers.update_yaxes(categoryorder="total ascending")
    fig_scorers = dark_layout(fig_scorers, height=400)
    st.plotly_chart(fig_scorers, use_container_width=True)

    col_left, col_right = st.columns(2)

    # ── Season Comparison ─────────────────────
    with col_left:
        st.markdown("<div class='section-header'>📅 Goals & Assists by Season</div>", unsafe_allow_html=True)
        season_agg = (
            df.groupby("season", as_index=False)
            .agg(Goals=("goals", "sum"), Assists=("assists", "sum"))
        )
        season_melt = season_agg.melt(id_vars="season", var_name="Metric", value_name="Count")
        fig_season = px.bar(
            season_melt,
            x="season",
            y="Count",
            color="Metric",
            barmode="group",
            color_discrete_map={"Goals": ACCENT, "Assists": "#3b82f6"},
            labels={"season": "Season", "Count": "Total", "Metric": ""},
        )
        fig_season = dark_layout(fig_season, height=360)
        st.plotly_chart(fig_season, use_container_width=True)

    # ── Rating Distribution ───────────────────
    with col_right:
        st.markdown("<div class='section-header'>⭐ Player Rating Distribution</div>", unsafe_allow_html=True)
        fig_rating = px.histogram(
            df,
            x="rating",
            nbins=20,
            color_discrete_sequence=[ACCENT],
            labels={"rating": "Player Rating", "count": "Players"},
        )
        fig_rating.update_traces(marker_line_color=BORDER, marker_line_width=1)
        fig_rating = dark_layout(fig_rating, height=360)
        st.plotly_chart(fig_rating, use_container_width=True)

    # ── Stats Table & CSV Download ────────────
    render_stats_table(df)


# ─────────────────────────────────────────────
# 8. PAGE: PLAYER ANALYSIS
# ─────────────────────────────────────────────
def render_player_analysis(df: pd.DataFrame):
    st.markdown("## 🔍 Player Analysis")

    available_players = sorted(df["player_name"].unique())

    if len(available_players) < 1:
        st.warning("No players match the current filters. Adjust filters in the sidebar.")
        return

    # ── Player Comparison (Radar) ─────────────
    st.markdown("<div class='section-header'>🕸️ Player Comparison Radar</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        p1 = st.selectbox("Player 1", available_players, index=0, key="p1")
    with c2:
        default_p2_idx = min(1, len(available_players) - 1)
        p2 = st.selectbox("Player 2", available_players, index=default_p2_idx, key="p2")

    radar_cols = ["goals", "assists", "pass_accuracy", "rating", "dribbles_completed", "tackles"]
    radar_labels = ["Goals", "Assists", "Pass Acc %", "Rating", "Dribbles", "Tackles"]

    # Aggregate per-player totals across all filtered seasons
    player_agg = df.groupby("player_name")[radar_cols].agg({
        "goals": "sum",
        "assists": "sum",
        "pass_accuracy": "mean",
        "rating": "mean",
        "dribbles_completed": "sum",
        "tackles": "sum",
    })

    # Normalise 0–1 within filtered dataset
    norm_df = (player_agg - player_agg.min()) / (player_agg.max() - player_agg.min() + 1e-9)

    def player_radar_values(name):
        if name in norm_df.index:
            return norm_df.loc[name, radar_cols].tolist()
        return [0] * len(radar_cols)

    fig_radar = go.Figure()
    radar_line_colors = [ACCENT, "#ef4444"]
    radar_fill_colors = ["rgba(0,255,135,0.15)", "rgba(239,68,68,0.15)"]
    for idx, player in enumerate([p1, p2]):
        if player:
            vals = player_radar_values(player)
            vals_closed = vals + [vals[0]]
            labels_closed = radar_labels + [radar_labels[0]]
            fig_radar.add_trace(
                go.Scatterpolar(
                    r=vals_closed,
                    theta=labels_closed,
                    fill="toself",
                    name=player,
                    line=dict(color=radar_line_colors[idx], width=2),
                    fillcolor=radar_fill_colors[idx],
                    opacity=0.85,
                )
            )
    fig_radar.update_layout(
        polar=dict(
            bgcolor=SURFACE,
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color=MUTED), gridcolor=BORDER),
            angularaxis=dict(tickfont=dict(color=TEXT), gridcolor=BORDER),
        ),
        paper_bgcolor=SURFACE,
        font=dict(color=TEXT),
        height=460,
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(bgcolor=SURFACE, bordercolor=BORDER, font=dict(color=TEXT)),
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # ── Player stat summary cards ─────────────
    if p1 != p2 and p1 in player_agg.index and p2 in player_agg.index:
        st.markdown("<div class='section-header'>📋 Head-to-Head Stats</div>", unsafe_allow_html=True)
        h2h_cols = st.columns(len(radar_cols))
        for i, (col_name, label) in enumerate(zip(radar_cols, radar_labels)):
            v1 = player_agg.loc[p1, col_name]
            v2 = player_agg.loc[p2, col_name]
            with h2h_cols[i]:
                fmt = ".1f" if col_name in ("pass_accuracy", "rating") else ".0f"
                st.markdown(
                    f"<div class='kpi-card' style='border-left-color:#3b82f6'>"
                    f"<div class='kpi-label'>{label}</div>"
                    f"<div style='font-size:13px; color:{ACCENT}'>{p1.split()[0]}: <b>{v1:{fmt}}</b></div>"
                    f"<div style='font-size:13px; color:#ef4444'>{p2.split()[0]}: <b>{v2:{fmt}}</b></div>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

    col_l, col_r = st.columns(2)

    # ── Goals vs Assists Scatter ──────────────
    with col_l:
        st.markdown("<div class='section-header'>🎯 Goals vs Assists</div>", unsafe_allow_html=True)
        scatter_df = df.groupby(["player_name", "team", "position"], as_index=False).agg(
            goals=("goals", "sum"), assists=("assists", "sum")
        )
        fig_ga = px.scatter(
            scatter_df,
            x="assists",
            y="goals",
            color="position",
            color_discrete_map=POS_COLORS,
            hover_data={"player_name": True, "team": True, "goals": True, "assists": True},
            labels={"goals": "Goals", "assists": "Assists", "position": "Position"},
            size_max=12,
        )
        fig_ga.update_traces(marker=dict(size=8, line=dict(width=1, color=BG_DARK)))
        fig_ga = dark_layout(fig_ga, height=400)
        st.plotly_chart(fig_ga, use_container_width=True)

    # ── Shots vs Goals Scatter ────────────────
    with col_r:
        st.markdown("<div class='section-header'>🏹 Shots vs Goals (with Trend)</div>", unsafe_allow_html=True)
        shots_df = df.groupby(["player_name", "team", "position"], as_index=False).agg(
            goals=("goals", "sum"), shots=("shots", "sum")
        )
        try:
            fig_sg = px.scatter(
                shots_df,
                x="shots",
                y="goals",
                color="position",
                color_discrete_map=POS_COLORS,
                trendline="ols",
                trendline_scope="overall",
                trendline_color_override=ACCENT,
                hover_data={"player_name": True, "team": True},
                labels={"goals": "Goals", "shots": "Shots", "position": "Position"},
            )
        except Exception:
            # Fallback if statsmodels not installed
            fig_sg = px.scatter(
                shots_df,
                x="shots",
                y="goals",
                color="position",
                color_discrete_map=POS_COLORS,
                hover_data={"player_name": True, "team": True},
                labels={"goals": "Goals", "shots": "Shots", "position": "Position"},
            )
        fig_sg.update_traces(marker=dict(size=8, line=dict(width=1, color=BG_DARK)))
        fig_sg = dark_layout(fig_sg, height=400)
        st.plotly_chart(fig_sg, use_container_width=True)


# ─────────────────────────────────────────────
# 9. PAGE: TEAM ANALYSIS
# ─────────────────────────────────────────────
def render_team_analysis(df: pd.DataFrame):
    st.markdown("## 🏟️ Team Analysis")

    team_agg = (
        df.groupby("team", as_index=False)
        .agg(
            Goals=("goals", "sum"),
            Assists=("assists", "sum"),
            Players=("player_id", "nunique"),
            Avg_Rating=("rating", "mean"),
            Shots=("shots", "sum"),
            Pass_Accuracy=("pass_accuracy", "mean"),
        )
        .sort_values("Goals", ascending=False)
    )
    team_agg["Avg_Rating"] = team_agg["Avg_Rating"].round(2)
    team_agg["Pass_Accuracy"] = team_agg["Pass_Accuracy"].round(1)

    col_l, col_r = st.columns(2)

    # ── Goals & Assists by Team ───────────────
    with col_l:
        st.markdown("<div class='section-header'>⚽ Goals & Assists by Team</div>", unsafe_allow_html=True)
        team_melt = team_agg.melt(
            id_vars="team",
            value_vars=["Goals", "Assists"],
            var_name="Metric",
            value_name="Count",
        )
        fig_team_bar = px.bar(
            team_melt,
            x="team",
            y="Count",
            color="Metric",
            barmode="group",
            color_discrete_map={"Goals": ACCENT, "Assists": "#3b82f6"},
            labels={"team": "Team", "Count": "Total", "Metric": ""},
        )
        fig_team_bar = dark_layout(fig_team_bar, height=380)
        fig_team_bar.update_xaxes(tickangle=-20)
        st.plotly_chart(fig_team_bar, use_container_width=True)

    # ── Avg Rating by Team ────────────────────
    with col_r:
        st.markdown("<div class='section-header'>⭐ Average Player Rating by Team</div>", unsafe_allow_html=True)
        fig_rating = px.bar(
            team_agg.sort_values("Avg_Rating", ascending=False),
            x="team",
            y="Avg_Rating",
            color="Avg_Rating",
            color_continuous_scale=[[0, "#3b82f6"], [0.5, ACCENT], [1, "#ef4444"]],
            labels={"team": "Team", "Avg_Rating": "Avg Rating"},
        )
        fig_rating.update_coloraxes(showscale=False)
        fig_rating = dark_layout(fig_rating, height=380)
        fig_rating.update_xaxes(tickangle=-20)
        st.plotly_chart(fig_rating, use_container_width=True)

    # ── Team Summary Table ────────────────────
    st.markdown("<div class='section-header'>📋 Team Summary</div>", unsafe_allow_html=True)
    display_agg = team_agg.rename(columns={
        "team": "Team", "Goals": "Goals", "Assists": "Assists",
        "Players": "Unique Players", "Avg_Rating": "Avg Rating",
        "Shots": "Total Shots", "Pass_Accuracy": "Avg Pass Acc %",
    })
    st.dataframe(
        display_agg.set_index("Team"),
        use_container_width=True,
        height=260,
    )


# ─────────────────────────────────────────────
# 10. PAGE: POSITION ANALYSIS
# ─────────────────────────────────────────────
def render_position_analysis(df: pd.DataFrame):
    st.markdown("## 🎽 Position Analysis")

    pos_order = ["GK", "DEF", "MID", "FWD"]

    # ── Rating Box Plot ───────────────────────
    st.markdown("<div class='section-header'>📦 Rating Distribution by Position</div>", unsafe_allow_html=True)
    fig_box = px.box(
        df,
        x="position",
        y="rating",
        color="position",
        color_discrete_map=POS_COLORS,
        category_orders={"position": pos_order},
        labels={"position": "Position", "rating": "Rating"},
        points="all",
    )
    fig_box.update_traces(jitter=0.3, pointpos=0)
    fig_box = dark_layout(fig_box, height=420)
    st.plotly_chart(fig_box, use_container_width=True)

    col_l, col_r = st.columns(2)

    # ── Avg Stats Stacked Bar ─────────────────
    with col_l:
        st.markdown("<div class='section-header'>📊 Avg Goals, Assists, Tackles & Interceptions</div>", unsafe_allow_html=True)
        pos_agg = (
            df.groupby("position", as_index=False)
            .agg(
                Goals=("goals", "mean"),
                Assists=("assists", "mean"),
                Tackles=("tackles", "mean"),
                Interceptions=("interceptions", "mean"),
            )
        )
        pos_agg_cat = pos_agg[pos_agg["position"].isin(pos_order)].copy()
        pos_agg_cat["position"] = pd.Categorical(pos_agg_cat["position"], categories=pos_order, ordered=True)
        pos_agg_cat = pos_agg_cat.sort_values("position")

        pos_melt = pos_agg_cat.melt(id_vars="position", var_name="Metric", value_name="Avg")
        fig_stack = px.bar(
            pos_melt,
            x="position",
            y="Avg",
            color="Metric",
            barmode="stack",
            color_discrete_map={
                "Goals": ACCENT,
                "Assists": "#3b82f6",
                "Tackles": "#a855f7",
                "Interceptions": "#f6c90e",
            },
            labels={"position": "Position", "Avg": "Average per Player", "Metric": ""},
        )
        fig_stack = dark_layout(fig_stack, height=400)
        st.plotly_chart(fig_stack, use_container_width=True)

    # ── Player Count Donut ────────────────────
    with col_r:
        st.markdown("<div class='section-header'>🍩 Player Count by Position</div>", unsafe_allow_html=True)
        pos_counts = df.groupby("position")["player_id"].nunique().reset_index()
        pos_counts.columns = ["position", "count"]
        fig_donut = px.pie(
            pos_counts,
            values="count",
            names="position",
            hole=0.45,
            color="position",
            color_discrete_map=POS_COLORS,
        )
        fig_donut.update_traces(
            textposition="outside",
            textinfo="label+percent",
            marker=dict(line=dict(color=BG_DARK, width=2)),
        )
        fig_donut.update_layout(
            paper_bgcolor=SURFACE,
            font=dict(color=TEXT),
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(bgcolor=SURFACE, bordercolor=BORDER, font=dict(color=TEXT)),
            showlegend=True,
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    # ── Position Callouts ─────────────────────
    st.markdown("<div class='section-header'>🔎 Position-Specific Highlights</div>", unsafe_allow_html=True)

    def pos_highlight(pos_label, metrics, icon):
        sub = df[df["position"] == pos_label]
        if sub.empty:
            return
        vals = {m: round(sub[m].mean(), 1) for m in metrics}
        items = "".join(
            f"<div style='font-size:13px; margin:3px 0'><b style='color:{ACCENT}'>{v}</b> avg {m.replace('_',' ')}</div>"
            for m, v in vals.items()
        )
        st.markdown(
            f"<div class='kpi-card'>"
            f"<div style='font-size:22px'>{icon}</div>"
            f"<div class='kpi-label' style='color:{POS_COLORS.get(pos_label, ACCENT)}'>{pos_label}</div>"
            f"{items}"
            f"</div>",
            unsafe_allow_html=True,
        )

    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1:
        pos_highlight("GK", ["saves", "clean_sheets"], "🧤")
    with pc2:
        pos_highlight("DEF", ["tackles", "interceptions"], "🛡️")
    with pc3:
        pos_highlight("MID", ["key_passes", "assists"], "🎮")
    with pc4:
        pos_highlight("FWD", ["goals", "shots"], "🎯")


# ─────────────────────────────────────────────
# 11. STATS TABLE & CSV DOWNLOAD
# ─────────────────────────────────────────────
def render_stats_table(df: pd.DataFrame):
    st.markdown("<div class='section-header'>📋 Player Statistics Table</div>", unsafe_allow_html=True)

    search = st.text_input("🔍 Search player name…", key="player_search", placeholder="e.g. James Smith")
    display_df = df.copy()
    if search.strip():
        display_df = display_df[display_df["player_name"].str.contains(search.strip(), case=False, na=False)]

    st.dataframe(
        display_df.sort_values(["goals", "rating"], ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=380,
    )

    # Dynamic filename
    seasons_part = "_".join(df["season"].unique()) if len(df["season"].unique()) <= 2 else "all_seasons"
    filename = f"football_data_{seasons_part}.csv"

    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name=filename,
        mime="text/csv",
    )


# ─────────────────────────────────────────────
# 12. MAIN APP ROUTER
# ─────────────────────────────────────────────
def main():
    df_full = load_data()
    page, seasons, teams, positions, selected_players = build_sidebar(df_full)
    df = filter_data(df_full, seasons, teams, positions, selected_players)

    if df.empty:
        st.warning(
            "⚠️ No data matches the current filters. "
            "Please adjust the Season, Team, Position, or Player selections in the sidebar."
        )
        st.stop()

    if page == "Overview":
        render_overview(df)
    elif page == "Player Analysis":
        render_player_analysis(df)
    elif page == "Team Analysis":
        render_team_analysis(df)
    elif page == "Position Analysis":
        render_position_analysis(df)

    # Footer
    st.markdown(
        "<div class='footer'>⚽ Football Analytics Dashboard · Synthetic Data · Built with Streamlit & Plotly</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
