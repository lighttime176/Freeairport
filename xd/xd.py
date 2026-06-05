import ast
import base64
import binascii
import email
from email.header import decode_header
import imaplib
import json
import logging
import os
import re
import subprocess
import sys
import time
from urllib.parse import parse_qs, unquote, urlparse
from bs4 import BeautifulSoup
import cv2
from DrissionPage import ChromiumOptions, ChromiumPage
import requests

# ==========================================
# 1. 微信通知配置与函数
# ==========================================
SC_KEY = "8b2jMqbzZj9YvGvIcvlSY7V00"  # 你的推送密钥
PUSH_URL = f"https://wx.xtuis.cn/{SC_KEY}.send"

def send_notification(title, content):
    """封装微信推送函数"""
    try:
        params = {"text": title, "desp": content}
        response = requests.get(PUSH_URL, params=params, timeout=10)
        return response.text
    except Exception as e:
        print(f"发送通知失败: {e}")

# ==========================================
# 2. 日志初始化
# ==========================================
def logging_init():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        os.makedirs('xd', exist_ok=True)
        file_handler = logging.FileHandler('xd/xd.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger

logger = logging_init()

# ==========================================
# 3. 工具函数
# ==========================================
def scan_qr_native(image_path):
    """使用 OpenCV 检测并解码二维码"""
    img = cv2.imread(image_path)
    if img is None:
        logger.error(f"Error: Could not read image {image_path}")
        return None

    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if data:
        logger.info(f"二维码识别成功！内容: {data}")
        return data
    else:
        logger.warning("未检测到二维码。")
        return None

# ==========================================
# 4. 主执行流程
# ==========================================
def main():
    # 初始化关键变量，防止异常时引发 NameError
    sign_email = "未知"
    sub_url = None
    
    try:
    #     # ---- 读取 email.txt ----
    #     file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
    #     with open(file_path, 'r', encoding='utf-8') as f:
    #         content = f.read()
    #     emails = ast.literal_eval(content)

    #     # ---- 读取/初始化 计数器 ----
    #     num_file_path = "xd/xdnum.txt"
    #     if not os.path.exists(num_file_path):
    #         with open(num_file_path, "w", encoding="utf-8") as file:
    #             file.write("0")

    #     with open(num_file_path, "r", encoding="utf-8") as file:
    #         try:
    #             number = int(file.read().strip())
    #         except ValueError:
    #             number = 0  
                
    #     sign_email = emails[number]
    #     logger.info(f"当前使用的邮箱前缀: {sign_email}")

        # ---- 浏览器配置 ----
        co = ChromiumOptions().auto_port()
        co.headless(True)   # 无头模式
        co.set_argument('--no-sandbox')
        co.set_argument('--headless=new')
        co.set_paths(browser_path="/opt/google/chrome/google-chrome")

        page = ChromiumPage(addr_or_opts=co)
        tab = page.latest_tab  # 保持页面对象调用规范

    #     # ---- 1. 访问注册页面 ----
    #     tab.get("https://sulianproxy.com/register")
    #     tab.wait.doc_loaded()
    #     time.sleep(2)
    #     tab.get_screenshot(path=r"xd/打开网页.png", full_page=True)
    #     logger.info(f"[OK] 页面加载成功: {tab.title}")

    #     tab.run_js("window.focus();")

    #     # 输入邮箱前缀
    #     tab.ele("#input-1").input(sign_email)
    #     logger.info(f"[OK] 已输入邮箱前缀: {sign_email}")
    #     tab.get_screenshot(path=r"xd/输入邮箱.png", full_page=True)
        
    #     # 展开下拉框并选择 outlook
    #     for d in tab.eles("tag:div"):
    #         cls = d.attr("class") or ""
    #         if "register-email-suffix" in cls:
    #             d.click()
    #             break
    #     time.sleep(1.5)

    #     result = tab.run_js("""
    #         const items = document.querySelectorAll('.v-list-item');
    #         for (const item of items) {
    #             const title = item.querySelector('.v-list-item-title');
    #             if (title && title.textContent.includes('@outlook.com')) {
    #                 item.click();
    #                 return 'OK';
    #             }
    #         }
    #         return 'NOT_FOUND';
    #     """)
    #     logger.info(f"[OK] 选择 @outlook.com ({result})")
    #     time.sleep(0.5)
        
    #     # 输入密码并提交
    #     tab.ele("#input-3").input("11111111")
    #     tab.ele("#input-6").input("11111111")
    #     logger.info("[OK] 已输入密码")
        
    #     tab.ele('css=#app > div > div > div.v-row.v-row--no-gutters.bg-containerBg.position-relative > div.v-col-lg-12.v-col-12.d-flex.align-center > div > div > div > div > div > div.v-card-text.pa-sm-10.pa-6 > form > div:nth-child(2) > div > button > span.v-btn__content').click()
        
    #     # 确认弹窗
    #     tab.ele("css=body > div.v-overlay-container > div > div.v-overlay__content > div > div.v-card-actions.px-6.pb-6.pt-0 > button > span.v-btn__content").click()
    #     time.sleep(0.5)
    #     tab.get_screenshot(path=r"xd/over.png", full_page=True)

    #     # ---- 2. 等待接收邮件 ----
    #     for i in range(30):
    #         time.sleep(1)
    #         logger.info(f"等待邮箱中，第 {i+1} S")

    #     # IMAP 读取 163 邮箱
    #     EMAIL_ADDRESS = 'luo1764682172@163.com'
    #     EMAIL_PASSWORD = os.environ.get("ydyp")  # 从环境变量获取授权码

    #     server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
    #     logger.info('连接网易服务器成功')

    #     imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
    #     args = ("name", "imaplib", "version", "1.0.0")
    #     typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
    #     server._untagged_response(typ, dat, 'ID')

    #     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #     logger.info('登录邮箱服务器成功')

    #     server.select("INBOX")
    #     typ, data = server.search(None, 'ALL')
    #     all_ids = data[0].split()
    #     logger.info(f'共找到 {len(all_ids)} 封邮件')

    #     latest_ids = all_ids[-5:]
    #     fetch_data_lst = []
    #     for num in latest_ids:
    #         typ, fetch_data = server.fetch(num, '(RFC822)')
    #         fetch_data_lst.append(fetch_data)

    #     fetch_data = fetch_data_lst[-1]
    #     msg = email.message_from_bytes(fetch_data[0][1])
        
    #     subject_parts = decode_header(msg['subject'])
    #     decoded_subject = ''.join([
    #         (part.decode(charset or "utf-8") if isinstance(part, bytes) else part)
    #         for part, charset in subject_parts
    #     ])
    #     logger.info(f'最新邮件主题: {decoded_subject}')
        
    #     body = ""
    #     if msg.is_multipart():
    #         for part in msg.walk():
    #             content_type = part.get_content_type()
    #             content_dispo = str(part.get("Content-Disposition"))
    #             if content_type in ["text/plain", "text/html"] and "attachment" not in content_dispo:
    #                 charset = part.get_content_charset() or 'utf-8'
    #                 body = part.get_payload(decode=True).decode(charset, errors="replace")
    #                 break
    #     else:
    #         charset = msg.get_content_charset() or 'utf-8'
    #         body = msg.get_payload(decode=True).decode(charset, errors="replace")

    #     if "<html" in body.lower():
    #         soup = BeautifulSoup(body, "html.parser")
    #         text = soup.get_text(separator=' ', strip=True)
    #         text = re.sub(r'\s+', ' ', text)
    #     else:
    #         text = body

    #     logger.info(f'纯文本正文:\n{text}')

    #     # 匹配验证码
    #     match = re.search(r'请忽略此邮件。 ([a-zA-Z0-9]+)', text)
    #     if not match:
    #         match = re.search(r'\b\d{6}\b', text)

    #     if match:
    #         code = match.group(1)
    #         logger.info(f'提取验证码成功: {code}')
    #     else:
    #         logger.error('未找到验证码')
    #         raise ValueError("未从邮件正文中匹配到有效的验证码")

    #     # ---- 3. 输入验证码并创建账号 ----
    #     tab.ele("#input-15").input(code)
    #     logger.info('[OK] 已输入验证码')
    #     tab.get_screenshot(path=r"xd/输完验证码.png", full_page=True)
    #     time.sleep(0.5)
        
    #     for btn in tab.eles("tag:button"):
    #         if btn.text.strip() == "创建账号":
    #             btn.click()
    #             logger.info("[OK] 已点击「创建账号」按钮")
    #             break
        
        # ---- 4. 登录账户 ----
        tab.get("https://sulianproxy.com/login")
        tab.wait.doc_loaded()
        time.sleep(2)
        
        FULL_EMAIL = sign_email + '@outlook.com'
        FULL_EMAIL = 'a1fgbf6666@outlook.com'
        PASSWORD = '11111111'
        
        if "login" in tab.url.lower():
            tab.ele("#input-0").input(FULL_EMAIL)
            tab.ele("#input-2").input(PASSWORD)
            time.sleep(0.3)
            for btn in tab.eles("tag:button"):
                if "登录" in btn.text.strip():
                    btn.click()
                    break
            time.sleep(4)
            logger.info(f"当前跳转 URL: {tab.url}")
        else:
            logger.info("系统检测为：已登录状态")
            
        time.sleep(5)
        tab.get_screenshot(path=r"xd/1.png", full_page=True)
        
        # 关闭用户后台弹窗
        logger.info("正在自动关闭弹窗...")
        tab.run_js("""
            var btns = document.querySelectorAll('button');
            for (var i = 0; i < btns.length; i++) {
                var t = btns[i].textContent.trim();
                if (t.indexOf('Skip') > -1 || t === '关闭' || t.indexOf('稍后提醒') > -1) {
                    btns[i].click();
                }
            }
        """)
        time.sleep(3)
        tab.get_screenshot(path=r"xd/2.png", full_page=True)
        # ---- 5. 触发 Clash 二维码弹窗 ----
        logger.info("正在查找 Clash QR 二维码按钮...")
        click_result = tab.run_js("""
            var cards = document.querySelectorAll('.v-card');
            for (var i = 0; i < cards.length; i++) {
                if (cards[i].textContent.indexOf('订阅与导入') > -1) {
                    var items = cards[i].querySelectorAll('.v-list-item');
                    for (var j = 0; j < items.length; j++) {
                        if (items[j].textContent.indexOf('Clash') > -1 && items[j].textContent.indexOf('ClashMeta') === -1) {
                            var qrBtn = items[j].querySelector('.qr-trigger');
                            if (qrBtn) {
                                qrBtn.click();
                                return 'CLICKED_QR';
                            }
                        }
                    }
                }
            }
            return 'NOT_FOUND';
        """)
        logger.info(f"查找二维码按钮结果: {click_result}")
        time.sleep(2)
        tab.get_screenshot(path=r"xd/3.png", full_page=True)
        # 美化弹窗并截图
        tab.run_js("""
            var dialog = document.querySelector('.v-overlay--active.v-dialog .scan-dialog');
            if (dialog) {
                dialog.style.background = 'white';
                dialog.style.padding = '20px';
                dialog.style.borderRadius = '12px';
            }
        """)
        time.sleep(0.5)
        tab.get_screenshot(path=r"xd/4.png", full_page=True)
        screenshot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xd/dashboard_qr.png")
        tab.get_screenshot(path=screenshot_path, full_page=True)
        logger.info(f"后台二维码弹窗截图已保存: {screenshot_path}")

        # 备份 SVG 二维码内容
        svg_content = tab.run_js("""
            var svg = document.querySelector('.scan-dialog__qr-card svg');
            if (svg) return svg.outerHTML;
            return 'NO_SVG';
        """)
        if svg_content != "NO_SVG":
            svg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "xd/qr_code.svg")
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            logger.info(f"SVG 二维码源码已备份: {svg_path}")

        # ---- 6. 二维码解码与标准链接提取 ----
        qr_data = scan_qr_native(screenshot_path)
        if not qr_data:
            raise ValueError("OpenCV 未能在截图中识别到有效的二维码")

        parsed_url = urlparse(qr_data)
        query_params = parse_qs(parsed_url.query)
        
        if 'url' in query_params:
            sub_url = unquote(query_params['url'][0])
            sub_name = unquote(query_params['name'][0]) if 'name' in query_params else "未命名"
            logger.info(f"【配置名称】: {sub_name}")
            logger.info(f"【标准订阅链接】: {sub_url}")
        else:
            raise KeyError("二维码解析数据中未包含标准的 'url' 关键参数")

        # ---- 7. 数据持久化保存 ----
        with open("xd/urls.txt", "w", encoding="utf-8") as file:
            file.write(sub_url + "\n")
            
        number += 1
        with open('xd/xdnum.txt', "w", encoding="utf-8") as file:
            file.write(str(number))
        logger.info(f"成功更新计数器。新数字已写入: {number}")

        # 【核心推送 1】: 成功提取订阅通知
        send_notification(
            title="🎉 苏联Proxy 账号注册成功", 
            content=f"账号: {FULL_EMAIL}\n配置名称: {sub_name}\n\n标准订阅链接:\n{sub_url}"
        )

    except Exception as error:
        # ---- 8. 异常捕获与微信实时报警 ----
        import traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_stack = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        logger.error(f"自动化脚本执行遇到致命错误:\n{error_stack}")
        
        # 【核心推送 2】: 错误实时报警
        send_notification(
            title="❌ 苏联Proxy 自动化脚本报错", 
            content=f"当前操作邮箱前缀: {sign_email}\n异常摘要: {str(error)}\n\n详细错误堆栈:\n{error_stack}"
        )
    finally:
        # 释放浏览器实例
        page.quit()
        logger.info('浏览器服务已安全退出，主流程结束。')

if __name__ == '__main__':
    main()
