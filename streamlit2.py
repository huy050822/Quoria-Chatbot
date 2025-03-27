import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import re
import time
import joblib
from googletrans import Translator  

translator = Translator()
load_model = joblib.load("linear regression.pkl")
st.set_page_config(
    page_title="QUORIA 0.4.0",
    page_icon="https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/11zon_cropped.png",
    layout="centered",
    initial_sidebar_state="collapsed" 
)
language = st.sidebar.selectbox("Select Language", options=["vi", "en", "fr", "es", "zh-cn", "ja"], index=0)
st.markdown(
    """
    <style>
    body {
        background-color: #0e0e10;
        color: #707C4F;
    }
    .title {
        text-align: center;
        font-size: 5em;
        font-weight: bold;
        background: linear-gradient(135deg, #FFD700, #FF8C00, #FF4500);
        -webkit-background-clip: text;
        color: transparent;
        text-shadow: 4px 4px 10px rgba(0, 0, 0, 0.2);
        border-radius: 15px;
    }
    .chat-box {
        padding: 20px;
        border-radius: 10px;
        background: #1e1e1f;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        transition: opacity 0.5s ease-in-out;
    }
    </style>
    <h1 class='title'>QUORIA</h1>
    """,
    unsafe_allow_html=True
)
st.markdown("<div class='chat-box' id='chat-box'>Hi, How can I help you?</div>", unsafe_allow_html=True)
if os.path.exists("responses.json"):
    with open("responses.json", "r", encoding="utf-8") as f:
        responses = json.load(f)
else:
    responses = {}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_form" not in st.session_state:
    st.session_state.show_form = False
def get_response(user_input):
    text = user_input.strip().lower()
    for pattern, response in responses.items():
        if re.fullmatch(pattern, text, re.IGNORECASE):
            return response
    return "Nói lại đi đừng ngại, tui chả hiểu bạn đang nói gì cả"
def translate_text(text, dest_language):
    if dest_language != "vi":
        try:
            return translator.translate(text, dest=dest_language).text
        except Exception as e:
            st.error(f"Translation error: {e}")
            return text
    return text
for msg in st.session_state.messages:
    role = "User" if msg["role"] == "user" else "Assistant"
    st.markdown(f"**{role}:** {msg['content']}")
prompt = st.chat_input("Please type a message...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/avatar.png"):
        st.markdown(prompt)
    if language == "vi":
        if "giá xe máy cũ" in prompt.lower():
            st.session_state.show_form = True
    else:
        translated_prompt = translator.translate(prompt, dest="vi").text.lower()
        if "giá xe máy cũ" in translated_prompt:
            st.session_state.show_form = True
    if not st.session_state.show_form:
        bot_response = get_response(prompt)
        bot_response = translate_text(bot_response, language)
        with st.chat_message("assistant", avatar="https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/11zon_cropped%20(2).png"):
            holder = st.empty()
            partial_text = ""
            for word in bot_response.split():
                partial_text += word + " "
                time.sleep(0.05)
                holder.markdown(partial_text + "⚪️")
            holder.markdown(partial_text)
        st.session_state.messages.append({"role": "assistant", "content": bot_response})


if st.session_state.show_form:
    form_subtitle = "Vui lòng điền thông tin xe để tôi giúp định giá:" if language == "vi" else "Please fill in the bike details to help me estimate the price:"
    submit_label = "Submit thông tin" if language == "vi" else "Submit"
    
    st.subheader(translate_text(form_subtitle, language))
    with st.form("price_form"):
        model_input = st.text_input("Model")
        brand_input = st.text_input("Brand")
        km_input = st.number_input("Kilometers Driven", min_value=0, max_value=999999, value=0)
        year_input = st.number_input("Year of Manufacture", min_value=1990, max_value=2025, value=2025)
        min_price_input = st.number_input("Minimum Price(million VNĐ)", value=1, min_value=0, max_value=100)
        submitted = st.form_submit_button(submit_label)
    
    if submitted:
        new_data = pd.DataFrame({
            "Model": [model_input],
            "Brand": [brand_input],
            "Kilometer Driven": [km_input],
            "Year of Manufacture": [year_input],
            "Min_Price": [min_price_input]
        })
        try:
            y_new_pred = load_model.predict(new_data)
            rounded_preds = np.round(y_new_pred[0], 2)
            result_msg = f"The result: {rounded_preds:,.2f}"
            st.success(result_msg)
        except Exception as e:
            result_msg = f"Error: {e}"
            st.error(result_msg)
        
        result_msg_translated = translate_text(result_msg, language)
        with st.chat_message("assistant", avatar="https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/11zon_cropped%20(2).png"):
            holder = st.empty()
            partial_text = ""
            for word in result_msg_translated.split():
                partial_text += word + " "
                time.sleep(0.13)
                holder.markdown(partial_text + "⚪️")
            holder.markdown(partial_text)
        st.session_state.messages.append({"role": "assistant", "content": result_msg_translated})
        
        csv_filename = "input_data.csv"
        try:
            if os.path.exists(csv_filename):
                new_data.to_csv(csv_filename, mode='a', header=False, index=False)
            else:
                new_data.to_csv(csv_filename, mode='w', header=True, index=False)
        except Exception as e:
            st.error(f"Errors: {e}")

        st.session_state.show_form = False
