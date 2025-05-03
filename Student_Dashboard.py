import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("student_data.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Students")
classes = st.sidebar.multiselect("Select Class", df["class"].unique(), default=df["class"].unique())
subjects = st.sidebar.multiselect("Select Subject", df["subject"].unique(), default=df["subject"].unique())
genders = st.sidebar.multiselect("Select Gender", df["gender"].unique(), default=df["gender"].unique())

# Filtered Data
filtered_df = df[
    (df["class"].isin(classes)) &
    (df["subject"].isin(subjects)) &
    (df["gender"].isin(genders))
]

# Title
st.title("🎓 Student Performance Dashboard")

# KPIs
st.subheader("📊 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Score", round(filtered_df["score"].mean(), 2))
col2.metric("Pass Rate (%)", round((filtered_df["score"] >= 50).mean() * 100, 2))
if not filtered_df.empty:
    top_subject = filtered_df.groupby("subject")["score"].mean().idxmax()
else:
    top_subject = "N/A"
col3.metric("Top Subject", top_subject)

# Bar chart - average score by subject
st.subheader("📚 Average Score by Subject")
avg_scores = filtered_df.groupby("subject")["score"].mean()
st.bar_chart(avg_scores)

# Line chart - score trend
st.subheader("📈 Score Trend Over Time")
filtered_df["exam_date"] = pd.to_datetime(filtered_df["exam_date"])
score_trend = filtered_df.groupby("exam_date")["score"].mean()
st.line_chart(score_trend)

# Pie chart - gender distribution
st.subheader("👩‍🎓 Gender Distribution")
gender_counts = filtered_df["gender"].value_counts()
fig, ax = plt.subplots()
ax.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Raw data table
st.subheader("🧾 Detailed Student Data")
st.dataframe(filtered_df)
