import streamlit as st
import mysql.connector
import bcrypt
import re # Thư viện regex để kiểm tra email (tùy chọn)

# --- Cấu hình kết nối Database MySQL ---
# !!! QUAN TRỌNG: Thay thế bằng thông tin kết nối thực tế của bạn
# !!! Trong môi trường production, KHÔNG BAO GIỜ hardcode credentials.
# !!! Sử dụng biến môi trường hoặc Streamlit secrets management.
DB_CONFIG = {
    'host': '127.0.0.1',  # Hoặc địa chỉ IP/domain của server MySQL
    'user': 'root', # Thay bằng user của bạn
    'password': '123456', # Thay bằng mật khẩu của bạn
    'database': 'clothing_company' # Tên database đã tạo ở bước 2
}

# --- Hàm tiện ích Database ---

def create_db_connection():
    """ Tạo kết nối đến database MySQL """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        st.error(f"Lỗi kết nối Database: {err}")
        return None

def close_db_connection(conn, cursor=None):
    """ Đóng cursor và kết nối database """
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()

def hash_password(password):
    """ Băm mật khẩu sử dụng bcrypt """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8') # Lưu dạng string

def check_password(stored_hashed_password, provided_password):
    """ Kiểm tra mật khẩu người dùng nhập với mật khẩu đã băm trong DB """
    password_bytes = provided_password.encode('utf-8')
    stored_hashed_bytes = stored_hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, stored_hashed_bytes)

def add_user(username, password, name=None, email=None):
    """ Thêm người dùng mới vào database """
    hashed = hash_password(password)
    conn = create_db_connection()
    if not conn:
        return False, "Lỗi kết nối database."

    cursor = conn.cursor()
    sql = """
        INSERT INTO users (username, hashed_password, name, email)
        VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (username, hashed, name, email))
        conn.commit()
        return True, f"Tạo tài khoản '{username}' thành công!"
    except mysql.connector.Error as err:
        # Kiểm tra lỗi trùng lặp username hoặc email
        if err.errno == 1062: # Error code for duplicate entry
            if 'username' in err.msg:
                return False, f"Tên đăng nhập '{username}' đã tồn tại."
            elif 'email' in err.msg:
                 return False, f"Email '{email}' đã được sử dụng."
            else:
                return False, "Lỗi trùng lặp dữ liệu."
        else:
            return False, f"Lỗi khi tạo tài khoản: {err}"
    finally:
        close_db_connection(conn, cursor)

def verify_user(username, password):
    """ Xác thực người dùng từ database """
    conn = create_db_connection()
    if not conn:
        return False, None, "Lỗi kết nối database."

    cursor = conn.cursor(dictionary=True) # Lấy kết quả dạng dictionary
    sql = "SELECT username, hashed_password, name FROM users WHERE username = %s"
    try:
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()

        if user_data:
            stored_hash = user_data['hashed_password']
            display_name = user_data.get('name', username) # Lấy tên hoặc dùng username
            if check_password(stored_hash, password):
                return True, display_name, "Đăng nhập thành công."
            else:
                return False, None, "Mật khẩu không đúng."
        else:
            return False, None, "Tên đăng nhập không tồn tại."
    except mysql.connector.Error as err:
        return False, None, f"Lỗi khi xác thực: {err}"
    finally:
        close_db_connection(conn, cursor)

# --- Hàm kiểm tra định dạng email (Tùy chọn) ---
def is_valid_email(email):
    # Biểu thức chính quy đơn giản để kiểm tra email
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None

# --- Khởi tạo Session State ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'user_display_name' not in st.session_state:
    st.session_state['user_display_name'] = ""

# --- Giao diện Đăng nhập / Đăng ký ---
def show_login_signup_page():
    st.title("Chào mừng!")
    choice = st.radio("Bạn muốn:", ('Đăng nhập', 'Đăng ký'))

    if choice == 'Đăng nhập':
        st.header("Đăng nhập")
        with st.form("login_form"):
            login_username = st.text_input("Tên đăng nhập")
            login_password = st.text_input("Mật khẩu", type="password")
            login_submitted = st.form_submit_button("Đăng nhập")

            if login_submitted:
                if not login_username or not login_password:
                    st.warning("Vui lòng nhập tên đăng nhập và mật khẩu.")
                else:
                    is_valid, display_name, message = verify_user(login_username, login_password)
                    if is_valid:
                        st.session_state['authenticated'] = True
                        st.session_state['username'] = login_username
                        st.session_state['user_display_name'] = display_name
                        st.rerun() # Chạy lại script để hiển thị main_app
                    else:
                        st.error(message)

    elif choice == 'Đăng ký':
        st.header("Đăng ký tài khoản mới")
        with st.form("signup_form"):
            signup_name = st.text_input("Tên hiển thị (tùy chọn)")
            signup_email = st.text_input("Email (tùy chọn)")
            signup_username = st.text_input("Tên đăng nhập *")
            signup_password = st.text_input("Mật khẩu *", type="password")
            signup_confirm_password = st.text_input("Xác nhận mật khẩu *", type="password")
            signup_submitted = st.form_submit_button("Đăng ký")

            if signup_submitted:
                # --- Validate Inputs ---
                if not signup_username or not signup_password or not signup_confirm_password:
                    st.warning("Vui lòng điền đầy đủ Tên đăng nhập, Mật khẩu và Xác nhận mật khẩu.")
                elif signup_password != signup_confirm_password:
                    st.error("Mật khẩu xác nhận không khớp.")
                elif signup_email and not is_valid_email(signup_email): # Kiểm tra email nếu được nhập
                     st.error("Địa chỉ email không hợp lệ.")
                # Thêm các kiểm tra khác nếu cần (độ dài mật khẩu, ký tự đặc biệt...)
                else:
                    # --- Add User to DB ---
                    success, message = add_user(
                        signup_username,
                        signup_password,
                        signup_name if signup_name else None, # Lưu None nếu trống
                        signup_email if signup_email else None # Lưu None nếu trống
                    )
                    if success:
                        st.success(message + " Vui lòng chuyển qua tab 'Đăng nhập'.")
                    else:
                        st.error(message)

# --- Giao diện Chính của Ứng dụng ---
def main_app():
    display_name = st.session_state['user_display_name']
    st.sidebar.success(f"Xin chào, {display_name}!")

    if st.sidebar.button("Đăng xuất"):
        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # st.session_state['authenticated'] = False # Cách khác để reset
        # st.session_state['username'] = ""
        # st.session_state['user_display_name'] = ""
        st.rerun() # Chạy lại để hiển thị trang đăng nhập

    # --- Nội dung chính của ứng dụng ---
    st.title("Trang chính của ứng dụng")
    st.write("Đây là nội dung chỉ hiển thị sau khi đăng nhập thành công.")
    st.write(f"Tên đăng nhập của bạn là: {st.session_state['username']}")
    # ... Thêm các thành phần khác của ứng dụng tại đây ...


# --- Logic Hiển thị Chính ---
if not st.session_state['authenticated']:
    show_login_signup_page()
else:
    main_app()