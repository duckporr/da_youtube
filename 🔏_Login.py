
import streamlit as st

from Authentication import (
    verify_user, add_user, is_valid_email,
    is_user_authenticated, create_db_connection, close_db_connection 
)


if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_display_name' not in st.session_state:
    st.session_state.user_display_name = ""


def show_login_signup_forms():
    st.title("Chào mừng!")
    st.write("Vui lòng đăng nhập hoặc đăng ký để tiếp tục.")
    st.markdown("---")

    choice = st.radio(
        "Lựa chọn:",
        ('Đăng nhập', 'Đăng ký'),
        key="auth_choice_main",
        horizontal=True
    )
    st.markdown("---")

    conn_check = create_db_connection()
    if conn_check is None:
        st.error("Không thể kết nối đến cơ sở dữ liệu. Vui lòng thử lại sau.")
        st.stop() 
    else:
        close_db_connection(conn_check) 

    if choice == 'Đăng nhập':
        st.subheader("Đăng nhập")
        with st.form("login_form_main_page"):
            login_username = st.text_input("Tên đăng nhập", key="login_user_main_page")
            login_password = st.text_input("Mật khẩu", type="password", key="login_pass_main_page")
            login_submitted = st.form_submit_button("Đăng nhập")

            if login_submitted:
                if not login_username or not login_password:
                    st.warning("Vui lòng nhập tên đăng nhập và mật khẩu.")
                else:
                    is_valid, display_name, message = verify_user(login_username, login_password)
                    if is_valid:
                        # Cập nhật session state
                        st.session_state.authenticated = True
                        st.session_state.username = login_username
                        st.session_state.user_display_name = display_name
                        st.success(message + " Đang tải ứng dụng...") 
                        st.rerun() 
                    else:
                        st.error(message) 

    elif choice == 'Đăng ký':
        st.subheader("Đăng ký tài khoản mới")
        with st.form("signup_form_main_page"):
            signup_name = st.text_input("Tên hiển thị (tùy chọn)", key="signup_name_main_page")
            signup_email = st.text_input("Email (tùy chọn)", key="signup_email_main_page")
            signup_username = st.text_input("Tên đăng nhập *", key="signup_user_main_page")
            signup_password = st.text_input("Mật khẩu *", type="password", key="signup_pass_main_page")
            signup_confirm_password = st.text_input("Xác nhận mật khẩu *", type="password", key="signup_confirm_main_page")
            signup_submitted = st.form_submit_button("Đăng ký")

            if signup_submitted:
                valid = True
                if not signup_username or not signup_password or not signup_confirm_password:
                    st.warning("Vui lòng điền đầy đủ Tên đăng nhập, Mật khẩu và Xác nhận mật khẩu.")
                    valid = False
                if signup_password != signup_confirm_password:
                    st.error("Mật khẩu xác nhận không khớp.")
                    valid = False
                if signup_email and not is_valid_email(signup_email):
                     st.error("Địa chỉ email không hợp lệ.")
                     valid = False

                if valid:
                    success, message = add_user(
                        signup_username, signup_password,
                        signup_name if signup_name else None,
                        signup_email if signup_email else None
                    )
                    if success:
                        st.success(message + " Vui lòng chuyển qua tab 'Đăng nhập'.")
                    else:
                        st.error(message) 


def show_main_app_content():
    st.set_page_config(page_title="Trang Chủ", layout="wide")

    display_name = st.session_state.get('user_display_name', 'Người dùng')
    st.sidebar.success(f"Xin chào, {display_name}!")

    if st.sidebar.button("Đăng xuất", key="main_app_logout"):
        st.session_state.authenticated = False
        if 'username' in st.session_state: del st.session_state.username
        if 'user_display_name' in st.session_state: del st.session_state.user_display_name
        st.rerun()

    st.title("Trang chính của ứng dụng")
    st.write("Chào mừng bạn đến với ứng dụng quản lý doanh nghiệp toàn diện")
    st.write(f"Tên đăng nhập của bạn là: {st.session_state.get('username', 'N/A')}")


if not is_user_authenticated():
    show_login_signup_forms() 
else:
    show_main_app_content() 