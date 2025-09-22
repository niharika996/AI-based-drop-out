# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Make the page use full width
st.set_page_config(layout="wide", page_title="Student Risk Dashboard")

st.title("📊 Student Risk Dashboard")

# ------- Load data -------
DATA_PATH = "new_students_with_predictions.csv"  # adjust if your file name is different
try:
    df = pd.read_csv(DATA_PATH)
except Exception as e:
    st.error(f"Could not load '{DATA_PATH}': {e}")
    st.stop()

# Risk columns we color
risk_cols = ['attendance_risk', 'marks_risk', 'attempts_risk', 'fees_risk', 'dropout_risk']

# Ensure risk columns exist
missing = [c for c in risk_cols if c not in df.columns]
if missing:
    st.error(f"Missing expected columns in CSV: {missing}")
    st.stop()

# ------- Helper: map risk to color -------
def risk_color_hex(label):
    return {"G": "#38A169", "O": "#DD6B20", "R": "#E53E3E"}.get(label, "#B0BEC5")

# ------- Visualizations: side-by-side -------
st.subheader("Visualizations")

col1, col2 = st.columns(2)

# Pie chart (dropout_risk distribution)
with col1:
    st.markdown("**Dropout Risk Distribution (Pie)**")
    counts = df['dropout_risk'].value_counts().reindex(['G','O','R']).fillna(0)
    labels = []
    sizes = []
    colors = []
    for lbl in ['G','O','R']:
        labels.append(f"{lbl} ({int(counts[lbl])})")
        sizes.append(int(counts[lbl]))
        colors.append(risk_color_hex(lbl))
    # Avoid matplotlib error when all sizes are zero
    fig1, ax1 = plt.subplots(figsize=(5,4))
    if sum(sizes) == 0:
        ax1.text(0.5, 0.5, "No data", ha="center", va="center")
    else:
        ax1.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%' if p>0 else '', startangle=90, colors=colors)
        ax1.axis("equal")
    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)

# Bar chart (attendance risk counts)
with col2:
    st.markdown("**Attendance Risk Counts (Bar)**")
    att_counts = df['attendance_risk'].value_counts().reindex(['G','O','R']).fillna(0)
    fig2, ax2 = plt.subplots(figsize=(5,4))
    bars = ax2.bar(['G','O','R'], att_counts.values, color=[risk_color_hex(l) for l in ['G','O','R']])
    ax2.set_xlabel("Risk")
    ax2.set_ylabel("Count")
    ax2.set_title("Attendance Risk")
    for rect, val in zip(bars, att_counts.values):
        ax2.text(rect.get_x() + rect.get_width()/2, val + 0.5, int(val), ha="center", va="bottom", weight="bold")
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)

# ------- Full table (colored cells) -------
st.subheader("Predicted Student Risks (Full Table)")

# Styling function for pandas Styler (returns CSS string)
def style_risk(cell_value):
    if pd.isna(cell_value):
        return ""
    if cell_value == "G":
        return "background-color: #38A169; color: black; font-weight: bold;"
    if cell_value == "O":
        return "background-color: #DD6B20; color: black; font-weight: bold;"
    if cell_value == "R":
        return "background-color: #E53E3E; color: black; font-weight: bold;"
    return ""

# Create styled DataFrame and show full width + large height so it's immediately readable
styled = df.style.map(style_risk, subset=risk_cols)
# Display the styled DataFrame with container width and a generous height so user doesn't need fullscreen
st.dataframe(styled, use_container_width=True, height=700)
