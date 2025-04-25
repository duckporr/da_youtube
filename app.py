import subprocess
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")  # giao diện chính

@app.route('/analytics')
def analytics():
    # Mở Streamlit trong một tab mới
    subprocess.Popen(["streamlit", "run", "1_📊_Chat_with_your_data.py"])
    return "Đang mở dashboard phân tích..."

if __name__ == '__main__':
    app.run(debug=True)