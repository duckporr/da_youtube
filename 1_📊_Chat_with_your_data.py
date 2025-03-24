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

def main():
    #set up streamlit interface 
    st.set_page_config(
        page_title = "📊 Smart Data Analysis Tool",
        page_icon = "📊",
        layout="centered"
    )
    #load llm model 
    llm = load_llm(model_name= MODEL_NAME)
    logger.info("### Successfully loaded {MODEL_NAME} ! ###")
    #upload csv file 
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your csv file here",type = "csv")
   

    #initial chat history
    #read csv file 
    # create data analysis agent to query with our dât 
    # input qwuery and process query 
    #Display chat history


if __name__ =="__main__":
    main()
st.header("TEST")
