import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from feature_engineering import load_match_data, engineer_feature_goals
from sklearn.metrics import mean_squared_error
import numpy as np
import os

def train_model(X, y, model_name):
    print(f"Training {model_name} model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 24)

    model = lgb.LGBMRegressor(
        objective = "poisson",
        learning_rate = 0.05,
        num_leaves = 64,
        max_depth = 6,
        n_estimators = 500,
        verbosity = -1
    )

    model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        eval_metric="rmse",
        #early_stopping_rounds = 10,
        #verbose = False
    )

    

    return model

if __name__ == "__main__":
    print("Loading match data...")
    df = load_match_data()
    X, y_home, y_away = engineer_feature_goals(df)

    print("Training home goals model...")
    model_home = train_model(X, y_home, "home_goals")

    print("Training away goals model...")
    model_away = train_model(X, y_away, "away_goals")

    os.makedirs("models", exist_ok = True)
    joblib.dump((model_home, model_away), "model/poisson_gbm.pkl")
    print("Models saved to model/poisson_gbm.pkl")

    print("Evaluating models...")
    y_pred_home = model_home.predict(X)
    y_pred_away = model_away.predict(X)
    rmse_home = np.sqrt(mean_squared_error(y_home, y_pred_home))
    rmse_away = np.sqrt(mean_squared_error(y_away, y_pred_away))
    print(f"Home goals RMSE: {rmse_home:.4f}")
    print(f"Away goals RMSE: {rmse_away:.4f}")

