import cv2
import sys

def scan_qr_native(image_path):
    # 1. 加载图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return

    # 2. 初始化 OpenCV 自带的二维码检测器
    detector = cv2.QRCodeDetector()
    
    # 3. 解码
    # data 是识别出的内容, bbox 是坐标, straight_qrcode 是修正后的二维码图
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if data:
        print(f"识别成功！内容: {data}")
        return data
    else:
        print("未检测到二维码。")
        return None

if __name__ == "__main__":
    # 这里的参数根据你的 workflow 传入逻辑修改
    image_to_scan = "qs/4.png" 
    scan_qr_native(image_to_scan)
