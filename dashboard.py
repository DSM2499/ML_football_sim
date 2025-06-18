import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

CSV_PATH = "data/epl_standings.csv"
POS_COLS = [str(i) for i in range(1, 21)] 

@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Derived metrics
    df["title_odds"] = df["1"]
    df["top4_odds"] = df[["1", "2", "3", "4"]].sum(axis = 1)
    df["relegation_odds"] = df[["18", "19", "20"]].sum(axis = 1)
    df["volatility"] = df[POS_COLS].std(axis = 1)
    return df

df = load_data(CSV_PATH)
teams = ["All teams"] + list(df["team"].unique())

# ---------- SIDEBAR ------------------------------------------------
st.sidebar.header("🔧 Filters")
focus_team = st.sidebar.selectbox("Select a team (optional)", teams)
topn = st.sidebar.slider("How many teams to show in charts:", 5, 20, 10)

st.sidebar.markdown(
    """
    **About**  
    • Data from 10 000 Monte-Carlo season simulations  
    • Probabilities are percentages (0‒100)  
    • File: `epl_position_odds.csv`
    """
)

# ---------- MAIN PAGE ---------------------------------------------
st.title("⚽️ EPL Season Simulation Dashboard")
st.caption("Probabilistic league-table projections (10 000 simulations)")

# Helper: filter top-N rows for a metric
def topn_df(metric, ascending=False):
    return df.sort_values(metric, ascending=ascending).head(topn)

# 1. Title odds
st.subheader("🏆 Title Race – Probability to Finish 1st")
title_chart = px.bar(
    topn_df("title_odds", ascending=False),
    x="title_odds",
    y="team",
    orientation="h",
    labels={"title_odds": "Win Title (%)", "team": ""},
    text_auto=".2f"
)
st.plotly_chart(title_chart, use_container_width=True)

# 2. Top-4 odds
st.subheader("🎯 Top-4 Finish Odds")
top4_chart = px.bar(
    topn_df("top4_odds", ascending=False),
    x="top4_odds",
    y="team",
    orientation="h",
    labels={"top4_odds": "Top-4 (%)", "team": ""},
    text_auto=".2f",
    color="top4_odds",
    color_continuous_scale="Greens"
)
st.plotly_chart(top4_chart, use_container_width=True)

# 3. Relegation odds
st.subheader("⚠️ Relegation Risk (18-20)")
releg_chart = px.bar(
    topn_df("relegation_odds", ascending=False),
    x="relegation_odds",
    y="team",
    orientation="h",
    labels={"relegation_odds": "Relegation (%)", "team": ""},
    text_auto=".2f",
    color="relegation_odds",
    color_continuous_scale="Reds"
)
st.plotly_chart(releg_chart, use_container_width=True)

# 4. Volatility table
with st.expander("📈 Volatility – Standard Deviation of Final Position"):
    vol_df = df[["team", "volatility"]].sort_values("volatility", ascending=False)
    st.dataframe(vol_df.style.format({"volatility": "{:.2f}"}), use_container_width=True)

# 5. Heat-map: probability distribution for chosen team(s)
st.subheader("🔍 Finish-Position Probability Heat-Map")
if focus_team != "All teams":
    heat_df = df[df["team"] == focus_team]
else:
    heat_df = df.copy()

# Melt to long format for plotly heatmap
melt_df = heat_df.melt(id_vars="team", value_vars=POS_COLS,
                       var_name="position", value_name="prob")
# Cast types
melt_df["position"] = melt_df["position"].astype(int)

heatmap = px.imshow(
    melt_df.pivot(index="team", columns="position", values="prob"),
    color_continuous_scale="Blues",
    aspect="auto",
    labels=dict(color="Probability (%)"),
)
heatmap.update_xaxes(side="top")
st.plotly_chart(heatmap, use_container_width=True)

st.caption("© 2025 SportSight Demo – Probabilistic EPL Analytics")