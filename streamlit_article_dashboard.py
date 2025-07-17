import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    reception = pd.read_csv("reception_cleaned.csv", parse_dates=["Date"])
    consumption = pd.read_csv("consumption_cleaned.csv", parse_dates=["Date"])
    return reception, consumption

def build_flow_df(reception, consumption):
    received_agg = (
        reception.groupby(["Date", "Article"])
        .agg(Total_Received=("Quantity", "sum"))
        .reset_index()
    )
    consumed_agg = (
        consumption.groupby(["Date", "Article"])
        .agg(Total_Consumed=("Quantity", "sum"))
        .reset_index()
    )
    flow = pd.merge(
        received_agg, consumed_agg,
        on=["Date", "Article"],
        how="outer"
    ).sort_values("Date")
    flow["Total_Received"] = flow["Total_Received"].fillna(0)
    flow["Total_Consumed"] = flow["Total_Consumed"].fillna(0)
    flow["Cumulative_Received"] = flow.groupby("Article")["Total_Received"].cumsum()
    flow["Cumulative_Consumed"] = flow.groupby("Article")["Total_Consumed"].cumsum()
    flow["Running_Stock"] = flow["Cumulative_Received"] - flow["Cumulative_Consumed"]
    return flow

def plot_flows(flow_df, article_code):
    data = flow_df[flow_df["Article"] == article_code]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(data["Date"], data["Cumulative_Received"], label="Cumulative Received")
    ax.plot(data["Date"], data["Cumulative_Consumed"], label="Cumulative Consumed")
    ax.plot(data["Date"], data["Running_Stock"], label="Running Stock", linestyle="--")
    ax.set_xlabel("Date")
    ax.set_ylabel("Quantity")
    ax.set_title(f"Flow Chart - {article_code}")
    ax.legend()
    ax.grid(True)
    return fig

# Streamlit UI
st.title("📦 Article Stock Flow Dashboard")

reception_df, consumption_df = load_data()
flow_df = build_flow_df(reception_df, consumption_df)

articles = sorted(flow_df['Article'].unique())
selected_article = st.selectbox("Select an Article Code:", articles)

if selected_article:
    fig = plot_flows(flow_df, selected_article)
    st.pyplot(fig)
