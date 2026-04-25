# app.py
# Streamlit frontend for GreenScore – Carbon Footprint Calculator
# Run with: streamlit run app.py

import streamlit as st
import pandas as pd
from calculator import calculate_emissions
from scorer import calculate_green_score, get_score_label
from recommender import generate_recommendations
from ml_model import predict_emissions, explain_prediction
from validator import validate_inputs
from storage import save_result, load_history

# --- Page Config ---
st.set_page_config(page_title="GreenScore", page_icon="🌿", layout="wide")

st.title("🌿 GreenScore – Carbon Footprint Calculator")
st.write("Enter your monthly usage details below to calculate your carbon footprint and Green Score.")

st.divider()

# ------------------------------------------------------------------ #
# MODE SELECTION
# ------------------------------------------------------------------ #
st.subheader("⚙️ Calculation Mode")
mode = st.radio(
    "Choose how emissions are calculated:",
    options=["Rule-Based", "ML-Based"],
    horizontal=True,
    help="Rule-Based uses fixed emission factors. ML-Based uses a trained Linear Regression model."
)

st.divider()

# ------------------------------------------------------------------ #
# INPUT SECTION
# ------------------------------------------------------------------ #
st.subheader("📋 Your Monthly Usage")

left, right = st.columns(2)

with left:
    electricity_units = st.number_input(
        "⚡ Electricity Usage (kWh per month)",
        min_value=0.0, max_value=2000.0, value=120.0, step=1.0,
        help="Check your electricity bill for monthly units consumed. Max: 2000 kWh."
    )
    petrol_litres = st.number_input(
        "⛽ Fuel Usage (litres per month)",
        min_value=0.0, max_value=500.0, value=30.0, step=1.0,
        help="Estimate how many litres of petrol you use per month. Max: 500 litres."
    )
    lpg_cylinders = st.number_input(
        "🔥 LPG Usage (cylinders per month)",
        min_value=0.0, max_value=20.0, value=2.0, step=0.5,
        help="Enter the number of LPG cylinders you use per month. Max: 20."
    )

with right:
    transport_type = st.selectbox(
        "🚗 Primary Transport Type",
        options=["bike", "car", "public_transport"],
        format_func=lambda x: x.replace("_", " ").title(),
        help="Select the mode of transport you use most."
    )
    shopping_habit = st.selectbox(
        "🛍️ Shopping Habits",
        options=["low", "medium", "high"],
        format_func=lambda x: x.title(),
        help="Low = minimal purchases, High = frequent/large purchases."
    )

st.divider()

# ------------------------------------------------------------------ #
# CALCULATE BUTTON
# ------------------------------------------------------------------ #
if st.button("🌍 Calculate My Green Score", type="primary", use_container_width=True):

    inputs = {
        "electricity_units": electricity_units,
        "petrol_litres":     petrol_litres,
        "lpg_cylinders":     lpg_cylinders,
        "transport_type":    transport_type,
        "shopping_habit":    shopping_habit,
    }

    # --- Input Validation ---
    errors = validate_inputs(inputs)
    if errors:
        for err in errors:
            st.warning(f"⚠️ {err}")
        st.stop()  # halt execution — do not proceed with invalid inputs

    # --- Calculation based on selected mode ---
    if mode == "Rule-Based":
        breakdown    = calculate_emissions(inputs)
        total        = breakdown["total"]
        score        = calculate_green_score(total)
        label        = get_score_label(score)
        # breakdown dict available for detailed display
    else:
        # ML-Based: predict total, build a synthetic breakdown for display
        total     = predict_emissions(inputs)
        score     = calculate_green_score(total)
        label     = get_score_label(score)
        # Still compute rule-based breakdown for the category chart
        breakdown = calculate_emissions(inputs)

    recommendations = generate_recommendations(inputs, breakdown)

    # --- SHAP explanation (always run for insight) ---
    with st.spinner("Running SHAP explainability analysis..."):
        explanation = explain_prediction(inputs)

    # --- Save to history ---
    save_result(inputs, total, score, label, mode)

    st.divider()

    # ------------------------------------------------------------------ #
    # GREEN SCORE DISPLAY
    # ------------------------------------------------------------------ #
    st.subheader("🏆 Your Green Score")
    st.caption(f"Calculated using: {mode} mode")

    if score >= 700:
        score_color, score_emoji = "green",  "🟢"
    elif score >= 500:
        score_color, score_emoji = "orange", "🟡"
    else:
        score_color, score_emoji = "red",    "🔴"

    st.markdown(
        f"<h1 style='text-align:center; color:{score_color}; font-size:80px;'>"
        f"{score_emoji} {score}</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h3 style='text-align:center; color:{score_color};'>{label}</h3>",
        unsafe_allow_html=True
    )

    progress_value = (score - 300) / (850 - 300)
    st.progress(progress_value, text=f"Score: {score} / 850")

    st.divider()

    # ------------------------------------------------------------------ #
    # EMISSION BREAKDOWN
    # ------------------------------------------------------------------ #
    st.subheader("📊 Emission Breakdown")

    metrics_col, chart_col = st.columns([1, 2])

    with metrics_col:
        st.metric("🌡️ Total CO₂ Emissions", f"{total} kg")
        st.metric("⚡ Electricity",   f"{breakdown['electricity']} kg")
        st.metric("⛽ Petrol / Fuel", f"{breakdown['petrol']} kg")
        st.metric("🔥 LPG",          f"{breakdown['lpg']} kg")
        st.metric("🚗 Transport",     f"{breakdown['transport']} kg")
        st.metric("🛍️ Shopping",     f"{breakdown['shopping']} kg")

    with chart_col:
        st.bar_chart({
            "Electricity": breakdown["electricity"],
            "Petrol":      breakdown["petrol"],
            "LPG":         breakdown["lpg"],
            "Transport":   breakdown["transport"],
            "Shopping":    breakdown["shopping"],
        }, use_container_width=True)

    st.divider()

    # ------------------------------------------------------------------ #
    # XAI: SHAP FEATURE CONTRIBUTIONS
    # ------------------------------------------------------------------ #
    st.subheader("🔍 Why This Score? (Explainable AI)")
    st.caption("SHAP values show how much each input pushed the predicted emissions up or down.")

    top      = explanation["top_contributor"]
    contribs = explanation["contributions"]

    st.info(
        f"🏷️ Top contributing factor: **{top.replace('_', ' ').title()}** "
        f"(SHAP value: {contribs[top]} kg CO₂)"
    )

    st.bar_chart(
        {k.replace("_", " ").title(): v for k, v in contribs.items()},
        use_container_width=True
    )

    st.divider()

    # ------------------------------------------------------------------ #
    # RECOMMENDATIONS
    # ------------------------------------------------------------------ #
    st.subheader("💡 Recommendations")

    for tip in recommendations:
        if "great job" in tip.lower():
            st.success(tip)
        else:
            st.warning(tip)

    st.divider()

    # ------------------------------------------------------------------ #
    # HISTORY
    # ------------------------------------------------------------------ #
    st.subheader("🗂️ Past Calculations")
    st.caption("All your previous results are saved in history.csv")

    history = load_history()
    if history:
        # Show most recent 10 entries, newest first, as a proper DataFrame
        df = pd.DataFrame(history)
        st.dataframe(df.iloc[::-1].head(10).reset_index(drop=True), use_container_width=True)
    else:
        st.info("No history yet. This was your first calculation.")
