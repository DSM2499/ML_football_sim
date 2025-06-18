# ⚽ AI-Powered EPL Season Simulator & Monitoring Dashboard

This project is a real-time **football analytics system** that simulates entire **English Premier League (EPL)** seasons using historical data, predictive modeling, and probabilistic simulation. It generates **match outcome forecasts**, team standing probabilities, and scenario-based analysis — all visualized via an interactive **Streamlit dashboard**.

---

## 🚀 What This Project Does

- 🔮 **Predict match scores** using machine learning models trained on team stats, ELO ratings, and recent form
- 🧮 **Simulate 10,000 seasons** using Poisson-distributed goal predictions
- 📊 **Calculate probabilities** of each team finishing at every position
- 🏆 Highlight **title odds**, **top-4 finish chances**, and **relegation risks**
- 📉 Quantify **volatility** of each team’s potential finish
- 📈 Generate professional **PDF reports** with insights and charts
- 🌐 Deliver insights via a full **Streamlit dashboard** for real-time monitoring

---

## 🎯 Use Cases

| Use Case                                | Description |
|----------------------------------------|-------------|
| 🔍 **Fan Engagement Tools**             | Let fans explore how their team might finish |
| 📈 **Sports Betting Research**          | Compare model odds vs. bookmakers to find value bets |
| 📊 **Analyst Previews**                 | Auto-generate weekly league forecasts |
| 📡 **Live Scenario Planning**           | Model “what-if” situations (e.g. if Liverpool beats Arsenal) |
| 🤖 **AI Portfolio Project**             | Showcase ML, simulation, and real-time UI engineering |

---

## 🧠 Skills Demonstrated

### 🧪 Machine Learning
- Regression modeling with **LightGBM**
- Feature engineering (ELO, rolling stats, match history)
- Evaluation (RMSE, F1-score, classification report)

### 📈 Simulation Modeling
- Poisson distribution for goals
- Monte Carlo methods (10,000 season simulations)
- Ranking logic for EPL standings

### 📊 Data Visualization & Reporting
- 📄 **Matplotlib**/Seaborn for charts
- 🧾 **PDF reports** using FPDF2
- 🧭 **Streamlit** for interactive UI

### 🧰 Software Engineering
- Modular Python pipeline (`data_ingest`, `feature_engineering`, `train_model`, `simulate_league`)
- Clean configuration via `config.yaml`
- Reusable utility functions for simulations and scoring

---

## ⚙️ How to Run

### 1. Set up environment
```bash
pip install -r requirements.txt
```

### 2. Collect the data
```bash
python data_ingest.py
```

### 3. Run Simulation
```bash
python train_model.py
python simulate_league.py
```

### 4. Launch the dashboard and generate report
```bash
python pdf_report_gen.py
streamlit run dashboard.py
```
---

## 🧩 Future Enhancements
- 🔁 “What-if scenario” engine (simulate upcoming matches)
- 📅 Live data sync from football-data API
- 🧠 Transfer-aware prediction models (adjust for squad value changes)
- 📊 Betting odds comparison layer

---

