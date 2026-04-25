# GreenScore – Project Progress Documentation

## Project Overview

GreenScore is a personal carbon footprint calculator and sustainability scoring system.
It takes monthly usage data from a user (electricity, fuel, LPG, transport, shopping),
calculates CO2 emissions, assigns a Green Score (300–850), and provides actionable
recommendations to reduce environmental impact. The system is designed to be modular,
UI-ready, and extensible with machine learning.

---

## Completed Phases
3
### Phase 1: System Design
- Defined user input parameters: electricity, petrol, LPG, transport type, shopping habit
- Established emission factors: 0.82 kg/kWh, 2.3 kg/litre, 42 kg/cylinder
- Designed Green Score formula: linear mapping of emissions (0–500 kg) to score (850–300)
- Defined score labels: Excellent / Moderate / Needs Improvement / Critical
- Designed rule-based recommendation logic
- Defined JSON output structure for frontend integration

### Phase 2: Backend Development
- `calculator.py` — individual emission functions + full breakdown calculator
- `scorer.py` — `calculate_green_score()` and `get_score_label()`
- `recommender.py` — `generate_recommendations()` with rule-based tips
- `main.py` — orchestrates all modules, returns clean JSON output
- `api.py` — FastAPI endpoint (`POST /calculate`) for frontend/API integration

### Phase 3: Frontend UI
- `app.py` — Streamlit app with full user input form
- Input fields: electricity, fuel, LPG (number inputs), transport and shopping (dropdowns)
- Calculate button triggers backend pipeline
- Displays: Green Score, total emissions, breakdown metrics, recommendations

### Phase 4: UI Enhancements
- Color-coded Green Score display (green / orange / red) with large font
- Progress bar representing score on the 300–850 scale
- Two-column layout for inputs and results
- Bar chart for emission breakdown by category
- Recommendations displayed using `st.warning()` and `st.success()` boxes

### Phase 5: Machine Learning Integration
- `ml_model.py` — Linear Regression model using scikit-learn
- Synthetic dataset of 1000 samples generated using the same emission factors
- 80/20 train/test split; Mean Absolute Error ~8.5 kg CO2
- Model saved to `greenscore_model.pkl` (trains once, reloads on subsequent runs)
- `predict_emissions(inputs)` function compatible with existing input format
- `main.py` updated to return both rule-based and ML-predicted results
- `app.py` updated with ML vs Rule-Based comparison panel

---

## Current Features

- Full carbon emission calculation (electricity, petrol, LPG, transport, shopping)
- Green Score (300–850) with label and color-coded visual
- Emission breakdown with bar chart
- Rule-based recommendation engine
- ML-based emission prediction (Linear Regression)
- Side-by-side ML vs rule-based comparison in UI
- REST API endpoint via FastAPI
- Clean JSON output structure throughout

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.x | Core language |
| Streamlit | Frontend UI |
| scikit-learn | ML model (Linear Regression) |
| FastAPI | REST API backend |
| Uvicorn | ASGI server for FastAPI |
| Pydantic | Request validation in API |
| pickle | Model serialization |

---

## Folder Structure

```
greenscore/
├── calculator.py          # Emission calculation functions
├── scorer.py              # Green Score formula and labels
├── recommender.py         # Rule-based recommendation engine
├── ml_model.py            # Synthetic data, model training, predict_emissions()
├── main.py                # Full pipeline runner (rule-based + ML)
├── app.py                 # Streamlit frontend
├── api.py                 # FastAPI REST endpoint
├── requirements.txt       # Python dependencies
├── greenscore_model.pkl   # Saved trained ML model (auto-generated)
└── progress.md            # This file
```

---

## What Is NOT Implemented Yet

- Explainable AI (SHAP / LIME) — no feature importance or explanation layer
- Database / persistent storage — no user history or session saving
- User authentication — no login or profile system
- Advanced ML models (Random Forest, XGBoost, etc.)
- Real-world dataset — currently using synthetic data only
- Deployment — not hosted on any cloud platform yet

---

## Next Steps

### Phase 6: Explainable AI
- Integrate SHAP to explain which input contributes most to emissions
- Display feature importance in the Streamlit UI

### Phase 7: Database & History
- Store user inputs and scores using SQLite or a simple CSV log
- Show historical score trends over time

### Optional Improvements
- Add user authentication (login/profile)
- Replace synthetic data with real-world emission datasets
- Deploy on Streamlit Cloud or as a Docker container
- Add PDF report export for the user's carbon footprint summary
