# === 1. Python 内置标准库 ===
import ast
import base64
import binascii
import email
from email.header import decode_header
import imaplib
import logging
import os
import re
import subprocess
import sys
import time
import random

# === 2. 第三方依赖库 ===
from bs4 import BeautifulSoup
import cv2
from DrissionPage import ChromiumOptions, ChromiumPage
import pyperclip
import requests

def scan_qr_native(image_path):
    # 1. 加载图片
    img = cv2.imread(image_path)
    if img is None:
        logger.info(f"Error: Could not read image {image_path}")
        return

    # 2. 初始化 OpenCV 自带的二维码检测器
    detector = cv2.QRCodeDetector()
    
    # 3. 解码
    # data 是识别出的内容, bbox 是坐标, straight_qrcode 是修正后的二维码图
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if data:
        logger.info(f"识别成功！内容: {data}")
        return data
    else:
        logger.info("未检测到二维码。")
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
#ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#co.set_user_agent(ua) 
co.remove_extensions()

browser = ChromiumPage(co)

tab = browser.latest_tab
tab.set.window.full()
# tab.set.cookies(cookies)

logger.info('打开千速 url')
tab.get('https://www.lajiaoyun.xyz/#/register')

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
emails = ast.literal_eval(content)

# ---- 读取/初始化 计数器 ----
num_file_path = "lj/ljnum.txt"
if not os.path.exists(num_file_path):
    with open(num_file_path, "w", encoding="utf-8") as file:
        file.write("0")

with open(num_file_path, "r", encoding="utf-8") as file:
    try:
        number = int(file.read().strip())
    except ValueError:
        number = 0  
        
sign_email = emails[number]
logger.info(f"准备注册邮箱: {sign_email}@outlook.com")
time.sleep(5)
tab.get_screenshot(path=r"./lj/打开网页.png", full_page=True)
