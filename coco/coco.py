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
    
    # 确保不重复添加 handler
    if not logger.handlers:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 确保 coco 目录存在
        os.makedirs('coco', exist_ok=True)
        file_handler = logging.FileHandler('coco/coco.log', encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger

logger = logging_init()

# ==========================================
# 3. 主执行流程（带异常捕获通知）
# ==========================================
def main():
    # ---- 读取 email.txt ----
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    emails = ast.literal_eval(content)

    # ---- 读取/初始化 计数器 ----
    num_file_path = "coco/coconum.txt"
    if not os.path.exists(num_file_path):
        with open(num_file_path, "w", encoding="utf-8") as file:
            file.write("0")

    with open(num_file_path, "r", encoding="utf-8") as file:
        try:
            number = int(file.read().strip())
        except ValueError:
            number = 0  
            
    sign_email = emails[number] + '@outlook.com'
    logger.info(f"准备注册邮箱: {sign_email}")

    # ---- 浏览器配置 ----
    co = ChromiumOptions().auto_port()
    co.headless(True)   # 无头模式
    co.set_argument('--no-sandbox')
    co.set_argument('--headless=new')
    co.set_paths(browser_path="/opt/google/chrome/google-chrome")
    
    browser = ChromiumPage(co)
    tab = browser.latest_tab

    try:
        # ---- 网页自动化操作 ----
        tab.get('https://dash.cocoduck.co/auth/register')
        logger.info('打开coco url')
        time.sleep(2)
        tab.get_screenshot(path=r"coco/打开网页.png", full_page=True)
        
        try:
            ele = tab.ele('text=点击注册')
            ele.click()
        except:
            pass
            
        ele = tab.ele('css=#email')
        ele.input(sign_email)
        logger.info('输入邮箱成功')
        tab.get_screenshot(path=r"coco/输入邮箱.png", full_page=True)
        
        ele = tab.ele('css=#email-verify')
        ele.click()
        logger.info('发送邮件按钮已点击')
        time.sleep(5)
        tab.get_screenshot(path=r"coco/发完邮件.png", full_page=True)

        ele = tab.ele('css=#success-confirm')
        ele.click()
        logger.info('点击好')

        ele = tab.ele('css=#passwd')
        ele.input('11111111')
        ele = tab.ele('css=#repasswd')
        ele.input('11111111')
        logger.info('输入密码完成')

        ele = tab.ele('css=#tos')
        ele.click(by_js=True)
        logger.info('点击我同意')
        tab.get_screenshot(path=r"coco/点击我同意.png", full_page=True)
        
        # 等待邮件接收
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

        match = re.search(r'邮箱验证代码为: ([a-zA-Z0-9]+)', text)
        if not match:
            match = re.search(r'\b\d{6}\b', text)

        if match:
            code = match.group(1)
            logger.info(f'提取验证码成功: {code}')
        else:
            logger.error('未找到验证码')
            raise ValueError("邮件中未匹配到验证码")

        # ---- 输入验证码并注册 ----
        codeele = tab.ele('css=#emailcode')
        codeele.input(code)
        logger.info('输入验证码完成')
        time.sleep(1)
        tab.get_screenshot(path=r"coco/输完验证码.png", full_page=True)
        
        ele = tab.ele('text=注册新账户')
        tab.listen.start(targets='https://www.cocoduck.live/user')

        # 计数器自增并写回
        number += 1
        with open(num_file_path, "w", encoding="utf-8") as file:
            file.write(str(number))
        logger.info(f"coconum 递增，新数字已写入: {number}")

        ele.click()
        time.sleep(0.2)
        try:
            ele.click()
            time.sleep(1)
        except:
            pass

        logger.info('点击注册按钮')
        tab.get_screenshot(path=r"coco/点击注册后.png", full_page=True)
        
        try:
            ele = tab.ele('css=#announcement-modal > div > div > div.modal-footer > button')
            ele.click()
            logger.info('关闭广告弹窗')
        except:
            pass

        # ---- 提取订阅链接 ----
        link = None
        try:
            res = tab.listen.wait(timeout=10).response
            res_body = res.body
            pattern = r'https://sub\.cocoduck\.cc/sub/[a-f0-9]+/clash'
            matches = re.findall(pattern, res_body)
            if matches:
                link = list(set(matches))[0]
        except Exception as e:
            logger.warning(f"网络监听未抓取到订阅，尝试解析本地HTML... 原因: {e}")
            with open(r"coco/test_browser.html", "w", encoding="utf-8") as f:
                f.write(tab.html)
            
            with open('coco/test_browser.html', 'r', encoding='utf-8') as f:
                html_content = f.read()

            pattern = r'https://sub\.cocoduck\.cc/sub/[a-f0-9]+/clash'
            matches = re.findall(pattern, html_content)
            if matches:
                link = list(set(matches))[0]

        if link:
            logger.info(f"成功找到订阅链接: {link}")
            
            # 保存链接与下载 yaml
            with open("coco/cocourls.txt", "w", encoding="utf-8") as file:
                file.write(link + "\n")
                
            headers_clash = {"User-Agent": "clash"}
            res = requests.get(link, headers=headers_clash, timeout=15)
            res_text = res.content.decode('utf-8')
            modified_str = res_text.replace('enable: true', 'enable: false')
            
            with open("coco/coco.yaml", "w", encoding="utf-8") as file:
                file.write(modified_str)
                
            # 【核心推送1】：成功获取订阅通知
            send_notification(
                title="🎉 COCO账号注册成功通知", 
                content=f"邮箱: {sign_email}\n成功提取订阅:\n{link}"
            )
        else:
            logger.error("未能通过任何途径找到订阅链接")
            raise ValueError("订阅链接抓取失败")

    except Exception as error:
        # ---- 捕获异常并微信报警 ----
        import traceback
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error_stack = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        
        logger.error(f"脚本执行报错:\n{error_stack}")
        
        # 【核心推送2】：错误实时报警
        send_notification(
            title="❌ 自动化脚本报错告警", 
            content=f"当前测试邮箱: {sign_email}\n错误信息: {str(error)}\n\n详细堆栈:\n{error_stack}"
        )
    finally:
        # 确保浏览器关闭
        browser.quit()
        logger.info('浏览器已关闭，主流程结束')

if __name__ == '__main__':
    main()
