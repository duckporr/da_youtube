from langchain_openai import ChatOpenAI
import os

def load_llm(model_name): 
    if model_name=="gpt-3.5-turbo":
        return ChatOpenAI(
            model = model_name,
            temperature = 0.0,
            max_tokens = 1000,
            openai_api_key=os.environ.get("OPEN_API_KEY")
        )
    elif model_name=="gpt-4":
        return ChatOpenAI(
            model = model_name,
            temperature = 0.0,
            max_tokens= 1000,
            openai_api_key=os.environ.get("OPEN_API_KEY")
        )
#có thể dùng grmini khi import gemini hay bất cứ con AI nào khác
    else:
        raise ValueError(
            "Unknown mode.\
                Please choose from['gpt-3.5-turbo','gpt-4]"
        )