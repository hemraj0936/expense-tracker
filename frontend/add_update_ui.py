import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
    st.markdown("### 📝 Add or Update Expenses")
    st.markdown("<hr>", unsafe_allow_html=True)

    selected_date = st.date_input("Select Date", datetime(2024, 8, 1))

    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("❌ Failed to retrieve expenses.")
        existing_expenses = []

    # Define categories with emojis
    categories = ["🏠 Rent", "🍽️ Food", "🛍️ Shopping", "🎬 Entertainment", "📦 Other"]
    raw_categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    st.markdown("#### 💸 Enter Your Expenses")
    with st.form(key="expense_form"):
        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                amount, category, notes = 0.0, "Shopping", ""

            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                amount_input = st.number_input("Amount", min_value=0.0, value=amount, step=1.0, key=f"amount_{i}")
            with col2:
                category_index = raw_categories.index(category) if category in raw_categories else 2
                category_input = st.selectbox("Category", categories, index=category_index, key=f"category_{i}")
            with col3:
                notes_input = st.text_input("Notes", value=notes, key=f"notes_{i}")

            # Remove emojis before saving
            cleaned_category = raw_categories[categories.index(category_input)]
            expenses.append({
                'amount': amount_input,
                'category': cleaned_category,
                'notes': notes_input
            })

        st.markdown(" ")
        submit_button = st.form_submit_button("💾 Submit")

        if submit_button:
            filtered_expenses = [e for e in expenses if e["amount"] > 0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)

            if response.status_code == 200:
                st.success("✅ Expenses updated successfully!")
                st.balloons()
            else:
                st.error("❌ Failed to update expenses.")
