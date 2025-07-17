
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📦 Article Movement Dashboard")

@st.cache_data
def load_data():
    reception = pd.read_csv("reception_cleaned.csv", parse_dates=["Date"])
    consumption = pd.read_csv("consumption_cleaned.csv", parse_dates=["Date"])
    return pd.concat([reception, consumption])

df = load_data()

articles = sorted(df['Article'].unique())
selected_article = st.selectbox("Select an article:", articles)

filtered_df = df[df["Article"] == selected_article]

st.subheader(f"📊 Quantity Over Time for Article: {selected_article}")

fig, ax = plt.subplots()
for label, group in filtered_df.groupby("Type"):
    ax.plot(group["Date"], group["Quantity"], marker="o", linestyle="-", label=label)

ax.set_xlabel("Date")
ax.set_ylabel("Quantity")
ax.legend()
ax.grid(True)
st.pyplot(fig)
