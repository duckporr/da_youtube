
import streamlit as st
import mysql.connector
import bcrypt
import re

# --- DB Config ---
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'clothing_company'
}


def create_db_connection():
    """ Tạo kết nối đến database MySQL """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Lỗi kết nối Database: {err}")
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
    return hashed.decode('utf-8')

def check_password(stored_hashed_password, provided_password):
    """ Kiểm tra mật khẩu người dùng nhập với mật khẩu đã băm trong DB """
    password_bytes = provided_password.encode('utf-8')
    stored_hashed_bytes = stored_hashed_password.encode('utf-8')
    try:
        return bcrypt.checkpw(password_bytes, stored_hashed_bytes)
    except ValueError:
        print(f"Lỗi: Định dạng hash không hợp lệ.")
        return False
    except Exception as e:
        print(f"Lỗi khi kiểm tra mật khẩu: {e}")
        return False


def add_user(username, password, name=None, email=None):
    """ Thêm người dùng mới vào database """
    hashed = hash_password(password)
    conn = create_db_connection()
    if not conn:
        return False, "Lỗi kết nối database khi thêm người dùng."

    cursor = conn.cursor()
    sql = "INSERT INTO users (username, hashed_password, name, email) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(sql, (username, hashed, name, email))
        conn.commit()
        return True, f"Tạo tài khoản '{username}' thành công!"
    except mysql.connector.Error as err:
        if err.errno == 1062:
             if 'username' in err.msg: return False, f"Tên đăng nhập '{username}' đã tồn tại."
             elif 'email' in err.msg: return False, f"Email '{email}' đã được sử dụng."
             else: return False, "Lỗi trùng lặp dữ liệu (username hoặc email)."
        else: return False, f"Lỗi SQL khi tạo tài khoản: {err}"
    finally:
        close_db_connection(conn, cursor)


def verify_user(username, password):
    """ Xác thực người dùng từ database """
    conn = create_db_connection()
    if not conn:
        return False, None, "Lỗi kết nối database khi xác thực." 

    cursor = conn.cursor(dictionary=True)
    sql = "SELECT username, hashed_password, name FROM users WHERE username = %s"
    try:
        cursor.execute(sql, (username,))
        user_data = cursor.fetchone()
        if user_data:
            stored_hash = user_data['hashed_password'] 
            display_name = user_data.get('name', username)
            if check_password(stored_hash, password):
                return True, display_name, "Đăng nhập thành công."
            else:
                return False, None, "Mật khẩu không đúng."
        else:
            return False, None, "Tên đăng nhập không tồn tại."
    except mysql.connector.Error as err:
        return False, None, f"Lỗi SQL khi xác thực: {err}"
    finally:
        close_db_connection(conn, cursor)

def is_valid_email(email):
    """Kiểm tra định dạng email đơn giản."""
    if not email: 
        return True
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email) is not None


def is_user_authenticated():
    """Kiểm tra cờ 'authenticated' trong session state."""
    return st.session_state.get('authenticated', False)