import streamlit as st 
import pandas as pd
import io
import matplotlib.pyplot as plt 
from dotenv import load_dotenv
from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent 
# agent cung cấp phương pháp giải dể ChatGPT mở rộng khả năng của mình cho LLM 
from langchain_openai import ChatOpenAI
from src.logger.base import BaseLogger
from src.models.llms import load_llm
#load enviroment
load_dotenv()
logger = BaseLogger()
MODEL_NAME = "gpt-3.5-turbo"

def process_query(da_agent,query):
    pass 
def main():
    #set up streamlit interface 
    st.set_page_config(
        page_title = "📊 Smart Data Analysis Tool",
        page_icon = "📊",
        layout="centered"
    )
    st.header("Smart data analysis tool")
    st.write("## Welcome to our data analysis tool . This tools can assist your daily data analysis task. Please enjoy!!")
    #load llm model 
    llm = load_llm(model_name= MODEL_NAME)
    #upload csv file 
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your csv file here",type = "csv")
   

    #initial chat history
    if "history" not in st.session_state:
        st.session_state.history = []

    #read csv file 
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("### Your uploaded file",st.session_state.df.head())
    # create data analysis agent to query with our data
    da_agent = create_pandas_dataframe_agent(
        llm = llm,
        df = st.session_state.df,
        agent_type = "tool-calling",
        allow_dangerous_code = True,
        verbose = True,
        return_intermediate_steps =True,
    )
    logger.info("### Successfully loaded data analysis agent ! ###")
    # input qwuery and process query 
    query = st.text_input("Enter your questions : ")

    if st.button("Run Query"):
        with st.spinner("Processing ..."):
            process_query(da_agent,query)
    #Display chat history


if __name__ =="__main__":
    main()
st.header("TEST")
