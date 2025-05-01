import streamlit as st
import pandas as pd
import pickle
import os

# Load the model and data
with open("model/recommender.pkl", "rb") as f:
    df, similarity_matrix = pickle.load(f)

st.set_page_config(page_title="African Food Product Recommendation", layout="wide")
st.title("🛒 African Food Product Recommendation")

product_list = df['product_name'].tolist()
selected_product = st.selectbox("Select a product you like:", product_list)

def display_product_card(name, category):
    img_path = f"images/{name.lower()}.jpeg"
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(img_path):
            st.image(img_path, width=100)
        else:
            st.image("https://via.placeholder.com/100", width=100)
    with col2:
        st.markdown(f"**{name}**")
        st.caption(f"Category: {category}")

if st.button("Get Recommendations"):
    idx = df[df['product_name'] == selected_product].index[0]
    similarity_scores = list(enumerate(similarity_matrix[idx]))
    sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:4]

    st.subheader("You might also like:")
    for i, score in sorted_scores:
        name = df.iloc[i]["product_name"]
        category = df.iloc[i]["category"]
        display_product_card(name, category)
