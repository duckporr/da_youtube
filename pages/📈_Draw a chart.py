import streamlit as st
import base64
from pygwalker.api.streamlit import StreamlitRenderer


def main():

    # Set up Streamlit interface
    st.set_page_config(
        page_title="📈 Trực quan hóa dữ liệu", page_icon="📈", layout="wide"
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
    st.header("📈 Trực quan hóa dữ liệu bằng biểu đồ ")
    st.write("### Trang này hỗ trợ bạn có cái nhìn tổng quan về từng cột dữ liệu bằng cách vẽ biểu đồ giữa các cột mà bạn mong muốn")

    # Render pygwalker
    if st.session_state.get("df") is not None:
        pyg_app = StreamlitRenderer(st.session_state.df)
        pyg_app.explorer()

    else:
        st.info("Dữ liệu để vẽ chưa có , hãy tải dữ liệu lên từ các trang kế toán , kho , marketing , dữ liệu bán hàng để bắt đầu trải nghiệm ")


if __name__ == "__main__": 
    main()