import streamlit as st
import time
import json
import re
#streamlit run streamlit2.py


st.set_page_config(page_title="QUORIA 0.4.0", page_icon= "https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/11zon_cropped.png", layout="centered", initial_sidebar_state="collapsed")

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
st.markdown("<div class='chat-box' id='chat-box'>Hi, How can i help you ?</div>", unsafe_allow_html=True)

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
    
    with st.chat_message("user", avatar=r"https://raw.githubusercontent.com/huy050822/Quoria-Chatbot/refs/heads/main/avatar.png"):
        st.markdown(prompt)

    responses = get_response(prompt)
    
     with st.chat_message("assistant", avatar=r"C:\Users\DELL\Downloads\chatbot.png"):

         
        if prompt.lower() in ["giá xe máy cũ", "giá xe cũ"]:
            with st.form("BIKE DETAIL FORM"):
                st.write("Vui lòng điền thông tin xe để tôi giúp bạn định giá:")
                car_name = st.text_input("Tên xe (VD: Yamaha):")
                year = st.number_input("Năm sản xuất:", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("Số km đã đi:", min_value=0, step=1000)
                brand = st.text_input("Hãng xe (VD: Honda, Yamaha):")
                submitted = st.form_submit_button("Gửi thông tin")

            if submitted:
                if car_name and year and mileage >= 0 and brand:
                    response = f"Tôi đã nhận thông tin xe của bạn: {car_name}, {brand}, năm sản xuất {year}, đã đi {mileage} km. Giá ước tính có thể dao động từ 500 triệu đến 600 triệu VND."
                else:
                    response = "Vui lòng điền đầy đủ thông tin để tôi có thể giúp bạn!"

        elif prompt.lower() in ["price of old bike", "old bike's price","old bike price" ]:
            with st.form("BIKE DETAIL FORM"):
                st.write("Please fill in the bike details to help me estimate the price:")
                bike_name = st.text_input("Bike name (e.g. Yamaha):")
                year = st.number_input("Year of manufacture:", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("Mileage:", min_value=0, step=1000)
                brand = st.text_input("Brand (e.g. Honda, Yamaha):")
                submitted = st.form_submit_button("Submit")

            if submitted:
                if bike_name and year and mileage >= 0 and brand:
                    response = f"I have received the bike details: {bike_name}, {brand}, year {year}, mileage {mileage} km. The estimated price could range from 200,000 to 300,000 VND."
                else:
                    response = "Please fill in all the details so I can help you!"

        elif prompt.lower() == "precio de motocicleta usada":
            with st.form("BIKE DETAIL FORM"):
                st.write("Por favor, complete los detalles de la motocicleta para ayudarme a estimar el precio:")
                bike_name = st.text_input("Nombre de la moto (ej. Yamaha):")
                year = st.number_input("Año de fabricación:", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("Kilometraje:", min_value=0, step=1000)
                brand = st.text_input("Marca (ej. Honda, Yamaha):")
                submitted = st.form_submit_button("Enviar")

            if submitted:
                if bike_name and year and mileage >= 0 and brand:
                    response = f"Recibí los detalles de tu moto: {bike_name}, {brand}, año {year}, kilometraje {mileage} km. El precio estimado podría oscilar entre 200,000 y 300,000 VND."
                else:
                    response = "¡Por favor, completa todos los detalles para que pueda ayudarte!"

        elif prompt.lower() == "prix de la moto d'occasion":
            with st.form("BIKE DETAIL FORM"):
                st.write("Veuillez remplir les détails de la moto pour m'aider à estimer le prix :")
                bike_name = st.text_input("Nom de la moto (ex : Peugeot, Yamaha) :")
                year = st.number_input("Année de fabrication :", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("Kilométrage :", min_value=0, step=1000)
                brand = st.text_input("Marque (ex : Honda, Yamaha) :")
                submitted = st.form_submit_button("Envoyer")

            if submitted:
                if bike_name and year and mileage >= 0 and brand:
                    response = f"J'ai reçu les détails de votre moto : {bike_name}, {brand}, année {year}, kilométrage {mileage} km. Le prix estimé pourrait varier entre 200,000 et 300,000 VND."
                else:
                    response = "Veuillez remplir tous les détails pour que je puisse vous aider !"

        elif prompt.lower() in ["中古バイクの価格", "ちゅうこバイクのかかく", "chūko baiku no kakaku"]:
            with st.form("BIKE DETAIL FORM"):
                st.write("バイクの詳細を入力してください。価格を見積もるお手伝いをします:")
                bike_name = st.text_input("バイク名（例：ヤマハ）:")
                year = st.number_input("製造年:", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("走行距離:", min_value=0, step=1000)
                brand = st.text_input("メーカー（例：ホンダ、ヤマハ）:")
                submitted = st.form_submit_button("送信")

            if submitted:
                if bike_name and year and mileage >= 0 and brand:
                    response = f"バイクの情報を受け取りました: {bike_name}, {brand}, 製造年 {year}, 走行距離 {mileage} km。推定価格は 200,000 VND から 300,000 VND の範囲です。"
                else:
                    response = "すべての詳細を入力してください！"

        elif prompt.lower() in ["二手摩托车价格", "èrshǒu mótuōchē jiàgé", "ershoumotuochejiage"]:
            with st.form("BIKE DETAIL FORM"):
                st.write("请填写摩托车详细信息，以帮助我估算价格：")
                bike_name = st.text_input("摩托车名称（例如：雅马哈）：")
                year = st.number_input("制造年份：", min_value=1900, max_value=2025, step=1)
                mileage = st.number_input("行驶里程：", min_value=0, step=1000)
                brand = st.text_input("品牌（例如：本田，雅马哈）：")
                submitted = st.form_submit_button("提交")

            if submitted:
                if bike_name and year and mileage >= 0 and brand:
                    response = f"我已收到您的摩托车详细信息：{bike_name}, {brand}, 制造年份 {year}, 行驶里程 {mileage} km。估计价格可能在 200,000 VND 到 300,000 VND 之间。"
                else:
                    response = "请填写所有详细信息，以便我能帮助您！"


     
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

