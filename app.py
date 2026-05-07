from flask import Flask, jsonify
import json

app = Flask(__name__)

# 首页路由
@app.route('/')
def index():
    return "✅ Flask 运行成功！访问 /books 查看爬虫数据"

# 书籍数据接口
@app.route('/books')
def get_books():
    try:
        # 读取爬虫保存的数据
        with open("books.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify({
            "status": "success",
            "count": len(data),
            "books": data
        })
    except:
        return jsonify({"error": "未找到 books.json 文件，请先运行爬虫"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
