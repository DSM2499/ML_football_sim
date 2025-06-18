import pandas as pd
import numpy as np
from collections import defaultdict

def load_match_data(filename = "data/epl_matches.csv"):
    df = pd.read_csv(filename, parse_dates = ["utc_date"])
    df = df[df["status"] == "FINISHED"].sort_values(by = "utc_date", ascending = True)
    df.reset_index(drop = True, inplace = True)
    df = df[df["matchday"].notnull()]
    return df

def calculate_points(home_goals, away_goals):
    if home_goals > away_goals:
        return 3, 0
    elif home_goals < away_goals:
        return 0, 3
    else:
        return 1, 1

def engineer_feature_goals(df, rolling_window = 5, elo_k = 20):
    """
    Compute rolling average stats: points, goals scored, goals conceded
    """
    team_states = defaultdict(lambda: {
        "points": [],
        "gf": [],
        "ga": [],
        "elo": 1000 #Base Elo
    })
    data_rows = []

    for idx, row in df.iterrows():
        ht, at = row["home_team"], row["away_team"]
        hg, ag = row["home_score"], row["away_score"]

        ht_stats = team_states[ht]
        at_stats = team_states[at]

        def avg(lst):
            return np.mean(lst[-rolling_window:]) if lst else 0
        
        row_features = {
            "matchday": row["matchday"],
            "home_team": ht,
            "away_team": at,
            "home_avg_pts": avg(ht_stats["points"]),
            "away_avg_pts": avg(at_stats["points"]),
            "home_avg_gf": avg(ht_stats["gf"]),
            "away_avg_gf": avg(at_stats["gf"]),
            "home_avg_ga": avg(ht_stats["ga"]),
            "away_avg_ga": avg(at_stats["ga"]),
            "home_elo": ht_stats["elo"],
            "away_elo": at_stats["elo"],
            "home_goals": hg,
            "away_goals": ag,
        }

        data_rows.append(row_features)

        h_pts, a_pts = calculate_points(hg, ag)
        ht_stats['points'].append(h_pts)
        at_stats['points'].append(a_pts)
        ht_stats['gf'].append(hg)
        at_stats['gf'].append(ag)
        ht_stats['ga'].append(ag)
        at_stats['ga'].append(hg)

        #Elo update
        expected_home = 1 / (1 + 10 ** ((at_stats["elo"] - ht_stats["elo"]) / 400))
        actual_home = 1 if hg > ag else 0.5 if hg == ag else 0
        ht_stats["elo"] += elo_k * (actual_home - expected_home)
        at_stats["elo"] += elo_k * ((1 - actual_home) - (1 - expected_home))

    df_features = pd.DataFrame(data_rows)

    X = df_features.drop(columns=["home_goals", "away_goals", "home_team", "away_team"])
    y_home = df_features["home_goals"]
    y_away = df_features["away_goals"]

    return X, y_home, y_away

if __name__ == "__main__":
    df = load_match_data()
    X, y_h, y_a = engineer_feature_goals(df)
    print(X.head())
    print(f"Targets: home_goals → mean {y_h.mean():.2f}, away_goals → mean {y_a.mean():.2f}")

