from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# 加载环境变量（安全存放API Key）
load_dotenv()

app = Flask(__name__)

# 从 .env 文件读取密钥
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_URL = "https://api.deepseek.com/chat/completions"

# 核心：调用AI
def ask_deepseek(message):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI调用失败：{str(e)}"

# Web接口
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    reply = ask_deepseek(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
