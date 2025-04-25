import streamlit as st
def chat_prompt():
    st.markdown("""
        <style>
        .chat-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 1000;
            background-color: rgba(255, 255, 255, 0.9);
            padding: 10px 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            backdrop-filter: blur(6px);
        }

        .chat-bar input {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            border: 1px solid #ccc;
            margin-right: 10px;
        }

        .chat-bar button {
            padding: 10px 16px;
            font-weight: bold;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
        }

        .block-container {
            padding-top: 80px !important; /* đẩy nội dung xuống dưới chat bar */
        }
        </style>

        <div class="chat-bar">
            <input type="text" placeholder="Bạn muốn hỏi gì hôm nay?"/>
            <button>Gửi</button>
        </div>
    """, unsafe_allow_html=True)
