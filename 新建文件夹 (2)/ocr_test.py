from paddleocr import PaddleOCR
import time

# 经典稳定初始化，无参数报错
ocr = PaddleOCR(use_angle_cls=True, lang="ch", device='cpu')

def run_ocr(img_path, desc):
    print(f"\n===== {desc} =====")
    start = time.time()
    result = ocr.ocr(img_path, cls=True)
    cost = round(time.time() - start, 2)
    print(f"耗时：{cost}秒")
    if result and result[0]:
        for item in result[0]:
            text, score = item[1]
            print(f"识别文字：{text}，置信度：{round(score*100)}%")
    else:
        print("未识别到文字")

if __name__ == "__main__":
    # 改成你自己的图片文件名
    print_img = "print.jpg"
    hand_img = "hand.jpg"

    run_ocr(print_img, "打印体文字识别")
    run_ocr(hand_img, "手写体文字识别")
