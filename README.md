# 🌱 GreenScore – Personal Carbon Footprint & Sustainability Scoring System

GreenScore is a data-driven system that calculates an individual's carbon footprint based on daily lifestyle activities and converts it into a simple, easy-to-understand **Green Score (300–850)**.

The goal is to promote **sustainable decision-making** by providing actionable insights and transparent environmental impact analysis.

---

## 🚀 Features

* 🔢 **Carbon Footprint Calculation**

  * Electricity usage
  * Fuel consumption
  * LPG usage
  * Lifestyle factors (transport, shopping)

* 📊 **Green Score (300–850)**

  * Credit-score style sustainability rating
  * Higher score = more eco-friendly

* 🤖 **Machine Learning Integration**

  * Linear Regression model (scikit-learn)
  * Predicts emissions based on user inputs

* 🔍 **Explainable AI (XAI)**

  * SHAP-based feature contribution analysis
  * Shows *why* your score is high/low

* 💡 **Smart Recommendations**

  * Personalized suggestions to reduce emissions

* 🌐 **Interactive UI**

  * Built using Streamlit
  * Real-time inputs and results

* ⚡ **API Support**

  * FastAPI backend (`/calculate` endpoint)

* 🗂️ **Data Persistence**

  * Saves user history to CSV

---

## 🧱 Tech Stack

* **Python 3.x**
* **Streamlit** (Frontend UI)
* **FastAPI** (Backend API)
* **scikit-learn** (Machine Learning)
* **SHAP** (Explainable AI)
* **Pandas / NumPy**
* **Uvicorn**

---

## 📁 Project Structure

```
greenscore/
├── calculator.py        # Emission calculations
├── scorer.py            # Green Score logic
├── recommender.py       # Recommendations engine
├── ml_model.py          # ML model + SHAP explainability
├── main.py              # Core pipeline
├── app.py               # Streamlit UI
├── api.py               # FastAPI backend
├── requirements.txt     # Dependencies
├── progress.md          # Project progress documentation
└── greenscore_model.pkl # Trained ML model
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```
git clone https://github.com/YOUR_USERNAME/GreenScore.git
cd GreenScore
```

---

### 2. Install Dependencies

```
pip install -r requirements.txt
```

---

### 3. Run Streamlit App

```
python -m streamlit run app.py
```

Then open:
👉 http://localhost:8501

---

### 4. Run API (Optional)

```
uvicorn api:app --reload
```

API endpoint:

```
POST /calculate
```

---

## 📊 How It Works

1. User inputs lifestyle data
2. System calculates emissions (rule-based + ML)
3. Generates:

   * Total emissions
   * Green Score
   * Recommendations
4. SHAP explains:

   * Which factors contributed most

---

## 🌍 Impact

GreenScore supports **sustainable living** by:

* Increasing carbon awareness
* Encouraging eco-friendly habits
* Providing data-driven insights

Aligned with:
👉 **SDG 13 – Climate Action**

---

## 🔮 Future Improvements

* Real-world dataset integration
* Advanced ML models (Random Forest, XGBoost)
* User authentication & dashboards
* Cloud deployment
* Mobile app version

---

## 📌 License

This project is for academic and educational purposes.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
