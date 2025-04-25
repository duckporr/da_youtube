import streamlit as st 
import pandas as pd
import io
import base64
import mysql.connector
from sqlalchemy import create_engine
import matplotlib.pyplot as plt 
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent 
# agent cung cấp phương pháp giải dể ChatGPT mở rộng khả năng của mình cho LLM 
from langchain_openai import ChatOpenAI
from src.logger.base import BaseLogger
from src.models.llms import load_llm
from src.utils import execute_plt_code
from src.components.chat_promt import chat_prompt
from Authentication import is_user_authenticated
#load enviroment
load_dotenv()
logger = BaseLogger()
MODEL_NAME = "gpt-3.5-turbo"
if not is_user_authenticated():
    st.warning("⛔ Bạn cần đăng nhập để truy cập trang này.")
    st.stop()
def load_data_from_mysql():
    connection_string = "mysql+mysqlconnector://root:123456@127.0.0.1/clothing_company"
    engine = create_engine(connection_string)

    query = "SELECT * FROM clothing_company.hieuquachiendich_standalone"
    df = pd.read_sql(query, engine)

    return df

def process_query(da_agent, query):
    response = da_agent(query)

    intermediate_steps = response.get("intermediate_steps", [])

    if intermediate_steps and len(intermediate_steps[-1]) > 0:
        try:
            action = intermediate_steps[-1][0].tool_input["query"]
        except (KeyError, AttributeError):
            action = ""
    else:
        action = ""

    if "plt" in action:
        st.write(response["output"])

        fig = execute_plt_code(action, df=st.session_state.df)
        if fig:
            st.pyplot(fig)

        st.write("**Executed code:**")
        st.code(action)

        to_display_string = response["output"] + "\n" + f"```python\n{action}\n```"
        st.session_state.history.append((query, to_display_string))

    else:
        st.write(response["output"])
        st.session_state.history.append((query, response["output"]))

def display_chat_history():
    st.markdown("## Lịch sử chat: ")
    for i, (q, r) in enumerate(st.session_state.history):
        st.markdown(f"**Query: {i+1}:** {q}")
        st.markdown(f"**Response: {i+1}:** {r}")
        st.markdown("---")


def main():
    #set up streamlit interface 
 
    st.set_page_config(
        page_title = "📘 Marketing",
        page_icon = "📘",
        layout="centered"
       
    )
    def get_base64_image(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    
    image_base64 = get_base64_image("D:/DADuckShop/dagpt/templates/assets/img/Ducklogonotbackground.png")
    st.markdown(f"""
        <style>
        .background-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("data:image/png;base64,{image_base64}");
        background-size: cover;
        background-position: center;
        opacity: 0.1;  
        z-index: 0;   
        }}
        </style>
        <div class="background-container"></div>
    """, unsafe_allow_html=True)
    st.header("Tôi có thể giúp gì cho bạn ?")
    st.write("Đây là phần mềm hỗ trợ bạn quản trị doanh nghiệp. Với trang này, AI sẽ hỗ trợ bạn cái nhìn tổng quan về dữ liệu Marketing . ")
    #load llm model 
    llm = load_llm(model_name= MODEL_NAME)
    if "history" not in st.session_state:
        st.session_state.history = []
    #read csv file 
    if st.button("Tải dữ liệu từ MySQL"):
        st.session_state.df = load_data_from_mysql()
        st.session_state.da_agent = create_pandas_dataframe_agent(
            llm=llm,
            df=st.session_state.df,
            agent_type="tool-calling",
            allow_dangerous_code=True,
            verbose=True,
            return_intermediate_steps=True,
        )
        st.session_state.data_loaded = True  # Đánh dấu là đã tải dữ liệu
        logger.info("### Successfully loaded MySQL data and agent! ###")

# Nếu dữ liệu đã được tải → hiển thị dữ liệu và cho nhập câu hỏi
    if st.session_state.get("data_loaded", False):
        st.write("### Dữ liệu Marketing", st.session_state.df.head())

        query = st.text_input("Nhập câu hỏi của bạn:")

        if st.button("Run Query"):
            with st.spinner("Đang xử lý..."):
                process_query(st.session_state.da_agent, query)  
    #Display chat history
    st.divider()
    display_chat_history()

if __name__ == "__main__": 
    main()