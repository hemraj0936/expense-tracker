import streamlit as st
from datetime import datetime
import requests
import pandas as pd


API_URL = "http://localhost:8000"


def analytics_tab():
    st.markdown("### 📊 Expense Analytics")
    st.markdown("Use the date range below to generate a summary of your expenses by category.")
    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("📈 Get Analytics"):
        with st.spinner("Fetching analytics..."):
            payload = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d")
            }

            try:
                response = requests.post(f"{API_URL}/analytics/", json=payload)
                response.raise_for_status()
                data = response.json()

                if not data:
                    st.warning("No data found for the selected date range.")
                    return

                df = pd.DataFrame({
                    "Category": list(data.keys()),
                    "Total": [data[cat]["total"] for cat in data],
                    "Percentage": [data[cat]["percentage"] for cat in data]
                })

                df_sorted = df.sort_values(by="Percentage", ascending=False)

                st.markdown("#### 🔍 Expense Breakdown by Category")
                st.bar_chart(df_sorted.set_index("Category")["Percentage"], use_container_width=True)

                # Format numbers nicely
                df_sorted["Total"] = df_sorted["Total"].map("₹{:.2f}".format)
                df_sorted["Percentage"] = df_sorted["Percentage"].map("{:.2f}%".format)

                st.markdown("#### 📋 Detailed Table")
                st.table(df_sorted)

            except Exception as e:
                st.error("❌ Failed to fetch analytics. Please try again.")
                st.exception(e)
