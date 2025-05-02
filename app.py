import streamlit as st
import pandas as pd
import os

# Load data directly from CSV
df = pd.read_csv("data/products.csv")
df.columns = df.columns.str.strip().str.lower()

# App configuration
st.set_page_config(page_title="African Food Product Recommendation", layout="wide")
st.title("🛒 African Food Product Recommendation")

# Product selection
product_list = df['product_name'].tolist()
selected_product = st.selectbox("Select a product you like:", product_list)

# Function to display product info
def display_product_card(name, category, subcategory, price, description): 
    img_path = f"images/{name.lower()}.jpeg"
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(img_path):
            st.image(img_path, width=100)
        else:
            st.image("https://via.placeholder.com/100", width=100)
    with col2:
        st.markdown(f"**{name}**")
        st.caption(f"Category: {category} | Subcategory: {subcategory}")
        st.markdown(f" **Price:** £{price}")
        st.markdown(f"📝 *{description}*")

# Get recommendations when button is clicked
if st.button("Get Recommendations"):
    selected_row = df[df['product_name'] == selected_product].iloc[0]
    selected_category = selected_row['category']

    # Filter products in same category excluding selected one
    recommendations = df[
        (df['category'] == selected_category) &
        (df['product_name'] != selected_product)
    ]

    if len(recommendations) >= 3:
        recommendations = recommendations.sample(n=3, replace=False)
    elif len(recommendations) > 0:
        recommendations = recommendations.sample(n=len(recommendations), replace=False)
    else:
        st.warning("No other products found in the same category to recommend.")
        recommendations = pd.DataFrame()

    if not recommendations.empty:
        st.subheader("You might also like:")
        for _, row in recommendations.iterrows():
            display_product_card(
                row['product_name'],
                row['category'],
                row['subcategory'],
                row['price'],
                row['description']
            )



