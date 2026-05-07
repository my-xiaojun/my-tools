import requests

def test_chat_api():
    # 这里的IP地址是绝对正确的
    url = "http://127.0.0.1:5000/chat"
    payload = {"message": "你好"}
    
    try:
        # 设置超时，防止卡住
        response = requests.post(url, json=payload, timeout=10)
        # 打印状态码，看请求有没有发出去
        print("状态码：", response.status_code)
        # 打印完整响应
        print("响应内容：", response.json())
    except Exception as e:
        print("出错了：", str(e))

# 运行测试
test_chat_api()
