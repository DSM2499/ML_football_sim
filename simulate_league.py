import pandas as pd
import numpy as np
import joblib
import yaml
from tqdm import tqdm
from collections import defaultdict, Counter
from feature_engineering import load_match_data, engineer_feature_goals

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

N_SIMULATIONS = config["n_simulations"]
START_MATCHDAY = config["start_matchday"]
MAX_GOALS = config["max_goals"]

def sample_score(lam_h, lam_a, max_goals = 6):
    home_goals = np.random.poisson(lam_h)
    away_goals = np.random.poisson(lam_a)
    return min(home_goals, max_goals), min(away_goals, max_goals)

def simulate_season(fixtures, model_home, model_away, base_points = None, base_gd = None):
    points = defaultdict(int, base_points or {})
    gd = defaultdict(int, base_gd or {})

    for _, row in fixtures.iterrows():
        feature_cols = model_home.feature_name_
        X = row[feature_cols].to_frame().T
        X = X.apply(pd.to_numeric, errors = "coerce").fillna(0)
        lam_h = model_home.predict(X)[0]
        lam_a = model_away.predict(X)[0]
        hg, ag = sample_score(lam_h, lam_a, max_goals = MAX_GOALS)

        ht = row["home_team"]
        at = row["away_team"]

        gd[ht] += hg - ag
        gd[at] += ag - hg

        if hg > ag:
            points[ht] += 3
        elif hg < ag:
            points[at] += 3
        else:
            points[ht] += 1
            points[at] += 1

    return points, gd

def simulate_many_seasons(df, model_home, model_away):
    df = df[df["matchday"].notnull()].copy()
    df = df.sort_values("utc_date", ascending = True).reset_index(drop = True)

    df_past = df[df["matchday"] < START_MATCHDAY]
    df_future = df[df["matchday"] >= START_MATCHDAY]

    base_points = defaultdict(int)
    base_gd = defaultdict(int)

    for _, row in df_past.iterrows():
        ht, at = row["home_team"], row["away_team"]
        hg, ag = row["home_score"], row["away_score"]

        if hg > ag:
            base_points[ht] += 3
        elif hg < ag:
            base_points[at] += 3
        else:
            base_points[ht] += 1
            base_points[at] += 1

        base_gd[ht] += hg - ag
        base_gd[at] += ag - hg
    
    X_future, _, _ = engineer_feature_goals(df_future)
    df_future = df_future.iloc[-len(X_future):].copy()
    df_future[X_future.columns] = X_future
    for col in X_future.columns:
        df_future[col] = pd.to_numeric(df_future[col], errors="coerce")
    
    df_future = df_future.fillna(0)

    team_list = sorted(set(df["home_team"]) | set(df["away_team"]))
    rank_counts = {team: Counter() for team in team_list}

    for _ in tqdm(range(N_SIMULATIONS), desc = "Simulating seasons"):
        pts, gds = simulate_season(df_future, model_home, model_away, base_points, base_gd)

        table = pd.DataFrame({
            "team": list(pts.keys()),
            "pts": [pts[t] for t in pts],
            "gd": [gds[t] for t in gds]
        }).sort_values(["pts", "gd"], ascending = False).reset_index(drop = True)
        
        for pos, team in enumerate(table["team"], start = 1):
            rank_counts[team][pos] += 1
    
    all_positions = list(range(1, 21))
    rows = []
    for team, counts in rank_counts.items():
        row = {"team": team}
        total = sum(counts.values())
        for pos in all_positions:
            row[str(pos)] = round(100 * counts.get(pos, 0) / total, 2)
        rows.append(row)
    
    result_df = pd.DataFrame(rows).fillna(0).sort_values("1", ascending = False)
    return result_df
    
if __name__ == "__main__":
    print("Loading match data...")
    model_home, model_away = joblib.load("model/poisson_gbm.pkl")
    df = load_match_data()

    print("Simulating league...")
    standings_df = simulate_many_seasons(df, model_home, model_away)
    standings_df.to_csv("data/epl_standings.csv", index = False)
    print(f"\nSimulation complete. Results saved to data/epl_standings.csv")
    print(standings_df[["team", "1", "2", "3", "4"]].head(10))  # quick peek