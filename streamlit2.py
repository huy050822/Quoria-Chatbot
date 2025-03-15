import streamlit as st
from streamlit_chat import message  
import time
import json
import re
#streamlit run streamlit2.py


st.set_page_config(page_title="QUORIA 0.4.0", page_icon=r"C:\Users\DELL\Downloads\11zon_cropped.png", layout="centered", initial_sidebar_state="collapsed")

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
st.markdown("<div class='chat-box' id='chat-box'>Hi, Tui giúp được gì cho bạn ?</div>", unsafe_allow_html=True)

prompt = st.chat_input("Please type a message...")


with open("responses.json", "r", encoding="utf-8") as f:
    responses = json.load(f)




if "messages" not in st.session_state: 
    st.session_state.messages = []

for msg in st.session_state["messages"]:
    role = "User" if msg["role"] == "user" else "Assistant"
    st.markdown(f"**{role}:** {msg["content"]}")



def get_response(user_input):
    for pattern, response in responses.items():
        if re.fullmatch(pattern, user_input, re.IGNORECASE):
            return response
    return "Nói lại đi đừng ngại, tui chả hiểu bạn đang nói gì cả"


if prompt:
    st.session_state.messages.append(
        {
        "role": "user", 
        "content": prompt
        }
    )
    
    with st.chat_message("user", avatar=r"C:\Users\DELL\Downloads\avatar.png"):
        st.markdown(prompt)

    responses = get_response(prompt)
    
    with st.chat_message("assistant", avatar=r"C:\Users\DELL\Downloads\chatbot.png"):

     
        holder = st.empty()
        responses_divide = ""

        for word in responses.split():
            responses_divide += word + " " 
            time.sleep(0.1)
            holder.markdown(responses_divide + "⚪️")
        holder.markdown(responses_divide)
    


    st.session_state.messages.append(
        {
        "role": "assistant",
        "content": responses
        }
    )

    


    # with st.chat_message("assistant", avatar=r"C:\Users\DELL\Downloads\chatbot.png"):
    #     st.markdown("Mimic: {}".format(prompt))

