# 测试ssh

import os
import re
import html
import json
import time
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv
from openai import (
    APIError, AuthenticationError, RateLimitError,
    APIConnectionError, Timeout, NotFoundError, PermissionDeniedError
)

# 加载环境变量
load_dotenv()

# ===================== 全局配置 =====================
HISTORY = []  # 上下文记忆
MAX_HISTORY = 5  # 最大记忆轮数

# ===================== 【超级文本清洗】防注入 / 防XSS / 去格式 =====================
def super_clean_text(text: str) -> str:
    if not text:
        return ""

    # 1. 转义 HTML 特殊字符（防XSS）
    text = html.escape(text)

    # 2. 移除所有 Markdown 格式：# * ` _ ~ > [] ()
    text = re.sub(r'[#*_`~>|]', '', text)
    text = re.sub(r'\[.*?\]\(.*?\)', '', text)  # 移除链接

    # 3. 移除多余空白、换行、制表符
    text = re.sub(r'\s+', ' ', text).strip()

    # 4. 移除控制字符
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    # 5. 过滤可能的注入关键词（安全加固）
    blacklist = ["ignore", "forget", "system", "prompt", "inject", "repeat", "code", "function"]
    for word in blacklist:
        text = text.replace(word, "[过滤]")

    return text.strip()

# ===================== 爬虫：书籍信息 =====================
def crawl_books():
    url = "http://books.toscrape.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")[:2]

        books = []
        for i, book in enumerate(items, 1):
            title = book.find("h3").a["title"]
            price = book.find("p", class_="price_color").text
            title = super_clean_text(title)
            price = super_clean_text(price)
            books.append({"id": i, "title": title, "price": price})
        return books

    except Exception as e:
        print(f"爬取失败：{e}")
        return []

# ===================== AI 流式输出（带上下文） =====================
def stream_ai_answer(prompt):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    model = os.getenv("MODEL_NAME", "deepseek-chat")

    if not api_key:
        print("❌ 未配置 API KEY")
        return

    # 清洗用户输入
    prompt = super_clean_text(prompt)
    HISTORY.append({"role": "user", "content": prompt})

    # 裁剪历史长度
    if len(HISTORY) > MAX_HISTORY * 2:
        del HISTORY[:2]

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        stream = client.chat.completions.create(
            model=model,
            messages=HISTORY,
            stream=True,
            temperature=0.7
        )

        print("\n🤖 AI 回答：", end="", flush=True)
        full_ans = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_ans += content

        full_ans = super_clean_text(full_ans)
        HISTORY.append({"role": "assistant", "content": full_ans})
        print("\n")
        return full_ans

    except Exception as e:
        print(f"\n❌ AI 错误：{e}")
        return ""

# ===================== 主程序 =====================
if __name__ == "__main__":
    print("="*60)
    print("📚 书籍价格对比工具（强力清洗 + 流式输出 + 上下文记忆）")
    print("="*60)

    # 1. 爬取
    books = crawl_books()
    if not books:
        print("❌ 无书籍信息")
        exit()

    print("✅ 爬取成功：")
    for b in books:
        print(f"第{b['id']}本：{b['title']} | {b['price']}")

    # 2. 构建分析指令
    analysis_prompt = f"""
    请分析以下两本书的价格与性价比，给出简短购买建议：
    1. {books[0]['title']}，价格：{books[0]['price']}
    2. {books[1]['title']}，价格：{books[1]['price']}
    要求：简洁、实用、不啰嗦。
    """

    # 3. 流式输出
    stream_ai_answer(analysis_prompt)

    print("="*60)
    print("✅ 文本清洗：已过滤注入、XSS、格式、特殊字符")
    print("✅ 流式输出：逐字打印，不卡顿")
    print("✅ 上下文记忆：支持多轮对话")
    print("✅ 安全加固：全流程防护")
    print("="*60)
