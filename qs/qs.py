from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging,random,time,requests,os,re
import imaplib,sys
import email
import ast
import requests
import pyperclip
import subprocess
import cv2

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

def logging_init():
  # 创建一个logger对象
  logger = logging.getLogger('my_logger')
  logger.setLevel(logging.INFO)  # 设置日志级别为INFO

  # 创建一个控制台处理器，输出到控制台
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)  # 设置控制台日志级别为INFO

  # 创建一个文件处理器，输出到文件
  file_handler = logging.FileHandler('qs/qs.log')
  file_handler.setLevel(logging.INFO)  # 设置文件日志级别为INFO

  # 创建一个日志格式化器
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  console_handler.setFormatter(formatter)  # 给控制台处理器设置格式
  file_handler.setFormatter(formatter)  # 给文件处理器设置格式

  # 将控制台和文件处理器添加到logger
  logger.addHandler(console_handler)
  logger.addHandler(file_handler)
  return logger
logger = logging_init()


# 创建页面对象
co = ChromiumOptions().auto_port()  # 指定程序每次使用空闲的端口和临时用户文件夹创建浏览器
co.headless(True)   # 无头模式
co.set_argument('--no-sandbox')  # 无沙盒模式
co.set_argument('--headless=new')  # 无界面系统添加
co.set_paths(browser_path="/opt/google/chrome/google-chrome")  # 设置浏览器路径
co.set_argument('--disable-gpu')    # 禁用gpu，提高加载速度
co.set_argument('--blink-settings=imagesEnabled=false')  # 禁用图片加载
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
co.set_user_agent(ua) 
co.remove_extensions()

browser = ChromiumPage(co)

tab = browser.latest_tab
tab.set.window.full()
# tab.set.cookies(cookies)

logger.info('打开千速 url')
tab.get('https://user2.1000ws.top/#/register')
# 随机生成邮箱
account = ''.join(random.choice('0123456789') for _ in range(10))
#data['email'] = f"{account}@"
logger.info(f"注册邮箱：{account}")

logger.info(account)
ele = tab.ele('css=#emailPrefix')
ele.input(account)
tab.get_screenshot(path=r"./qs/1.png", full_page=True)
logger.info(ele)
ele = tab.ele('css=#password')
ele.input('11111111')
ele = tab.ele('css=#confirmPassword')
ele.input('11111111')
tab.get_screenshot(path=r"./qs/2.png", full_page=True)
ele = tab.ele('css=#app > div > div.auth-container > div.auth-card > form > div:nth-child(6) > button')

ele.click()
time.sleep(5)
ele = tab.ele('text=Import Subscription')
ele.click()
tab.get_screenshot(path=r"./qs/3.png", full_page=True)
ele = tab.ele('text=Scan QR Code to Subscribe')
logger.info(ele)
ele.click()

time.sleep(2)
tab.get_screenshot(path=r"./qs/4.png", full_page=True)
image_to_scan = "qs/4.png" 
scan_qr_native(image_to_scan)
