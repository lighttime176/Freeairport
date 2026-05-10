import cv2
from pyzbar.pyzbar import decode
import sys

def scan(image_path):
    # 1. 加载图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图片文件 {image_path}")
        return

    # 2. 识别二维码
    barcodes = decode(img)
    
    if not barcodes:
        print("未在图片中检测到二维码")
        return

    # 3. 输出结果
    for barcode in barcodes:
        data = barcode.data.decode('utf-8')
        print(f"识别成功！内容为: {data}")

if __name__ == "__main__":
    # 假设你从命令行传入图片路径或参数
    # 这里可以根据你的实际逻辑修改
    test_image = "4.png" 
    scan(test_image)
