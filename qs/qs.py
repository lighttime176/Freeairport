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
import base64
import binascii
import ast
import email
from email.header import decode_header
import imaplib
import logging
import os
import re
import sys
import time
from bs4 import BeautifulSoup
from DrissionPage import ChromiumOptions, ChromiumPage
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
tab.get('https://user2.1000ws.top/#/register')

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
emails = ast.literal_eval(content)

# ---- 读取/初始化 计数器 ----
num_file_path = "qs/qsnum.txt"
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
tab.get_screenshot(path=r"./qs/1.png", full_page=True)
ele = tab.ele('css=#emailPrefix')
ele.input(sign_email)

def choose_email_suffix(tab, suffix='outlook.com'):
    suffix_box = tab.ele('css=.email-suffix', timeout=10)
    suffix_box.click()
    time.sleep(0.5)

    option = tab.ele(
        f'xpath://div[contains(@class, "suffix-option") and normalize-space()="{suffix}"]',
        timeout=5,
    )
    option.click()
    time.sleep(0.3)

    current = tab.ele('css=.suffix-text', timeout=5).text.strip()
    if current != suffix:
        raise RuntimeError(f'邮箱后缀选择失败，当前为: {current}')


choose_email_suffix(tab, 'outlook.com')
ele = tab.ele('css=#password')
ele.input('11111111')
ele = tab.ele('css=#confirmPassword')
ele.input('11111111')
ele = tab.ele('css=body > div:nth-child(1) > div > div.auth-container:nth-child(1) > div.auth-card:nth-child(3) > form.auth-form > div.form-group:nth-child(2) > div.input-with-button > button.send-code-btn')
ele.click()
for i in range(60):
    time.sleep(1)
    logger.info(f"等待邮箱中，第 {i+1} S")

# ---- IMAP 读取邮件 ----
EMAIL_ADDRESS = 'luo1764682172@163.com'
EMAIL_PASSWORD = os.environ.get("ydyp") # 环境变量中获取授权码

server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
logger.info('连接网易 IMAP 服务器成功')

imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
args = ("name", "imaplib", "version", "1.0.0")
typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
server._untagged_response(typ, dat, 'ID')

server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
logger.info('登录网易邮箱成功')

server.select("INBOX")
typ, data = server.search(None, 'ALL')
all_ids = data[0].split()
logger.info(f'共找到 {len(all_ids)} 封邮件')

latest_ids = all_ids[-5:]
fetch_data_lst = []
for num in latest_ids:
    typ, fetch_data = server.fetch(num, '(RFC822)')
    fetch_data_lst.append(fetch_data)

fetch_data = fetch_data_lst[-1]
msg = email.message_from_bytes(fetch_data[0][1])

subject_parts = decode_header(msg['subject'])
decoded_subject = ''.join([
    (part.decode(charset or "utf-8") if isinstance(part, bytes) else part)
    for part, charset in subject_parts
])
logger.info(f'最新邮件主题: {decoded_subject}')

body = ""
if msg.is_multipart():
    for part in msg.walk():
        content_type = part.get_content_type()
        content_dispo = str(part.get("Content-Disposition"))
        if content_type in ["text/plain", "text/html"] and "attachment" not in content_dispo:
            charset = part.get_content_charset() or 'utf-8'
            body = part.get_payload(decode=True).decode(charset, errors="replace")
            break
else:
    charset = msg.get_content_charset() or 'utf-8'
    body = msg.get_payload(decode=True).decode(charset, errors="replace")

if "<html" in body.lower():
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)
else:
    text = body

match = re.search(r'5分钟内有效\s*\)\s*(\d{6})\s*\(', text)
if not match:
    match = re.search(r'\b\d{6}\b', text)

if match:
    code = match.group(1)
    logger.info(f'提取验证码成功: {code}')
else:
    logger.info('未找到验证码')
    raise ValueError("邮件中未匹配到验证码")
ele = tab.ele('css=#verificationCode')
ele.input(code)
time.sleep(1)
ele = tab.ele('css=body > div:nth-child(1) > div > div.auth-container:nth-child(1) > div.auth-card:nth-child(3) > form.auth-form > div.form-group:nth-child(7) > button.btn.btn-primary.btn-block')
ele.click()
tab.get_screenshot(path=r"./qs/2.png", full_page=True)
# ele = tab.ele('css=#app > div > div.auth-container > div.auth-card > form > div:nth-child(6) > button')

# ele.click()
time.sleep(5)
ele = tab.ele('text=Import Subscription')
ele.click()
tab.get_screenshot(path=r"./qs/3.png", full_page=True)
ele = tab.ele('text=Scan QR Code to Subscribe')

ele.click()

time.sleep(2)
tab.get_screenshot(path=r"./qs/4.png", full_page=True)
image_to_scan = "qs/4.png" 
data = scan_qr_native(image_to_scan)
# with open("urls.txt", "w") as file:
#     file.write(data + "\n")


# headers_clash = {
#     "User-Agent": "clash-verge/v1.3.8", # 模拟更具体的客户端
#     "Accept": "*/*",
# }

# try:
#     res = requests.get(data, headers=headers_clash, timeout=15)
#     res.raise_for_status() # 检查是否请求成功
    
#     raw_content = res.content
    
#     # --- 尝试处理 Base64 编码 ---
#     try:
#         # 有些订阅是 Base64 后的 YAML，尝试解码
#         decoded_bytes = base64.b64decode(raw_content, validate=True)
#         content_str = decoded_bytes.decode('utf-8')
#     except (binascii.Error, UnicodeDecodeError):
#         # 如果不是 Base64 或者解码失败，则视为普通文本
#         content_str = raw_content.decode('utf-8')

#     # --- 执行修改 ---
#     # 建议使用正则表达式或更安全的匹配，防止误伤其他配置项
#     modified_str = content_str.replace('enable: true', 'enable: false')

#     # --- 保存文件 ---
#     with open("qs/qs.yaml", "w", encoding='utf-8') as file:
#         file.write(modified_str)
    
#     logger.info("订阅转换成功！")

# except Exception as e:
#     logger.info(f"获取订阅失败: {e}")
