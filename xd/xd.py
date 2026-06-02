from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging, random, time, requests, os, re
import imaplib, sys
import email
import ast
from bs4 import BeautifulSoup

# 读取 email.txt 文件
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 转换成 Python 列表
emails = ast.literal_eval(content)

file_path = "xd/xdnum.txt"

# 如果文件不存在，则初始化为 0
if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("0")

# 读取文件中的数字
with open(file_path, "r", encoding="utf-8") as file:
    try:
        number = int(file.read().strip())  # 读取并转换为整数
    except ValueError:
        number = 0  
sign_email = emails[number]


def logging_init():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = logging.FileHandler('xd/xd.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger

logger = logging_init()

# 创建页面对象
co = ChromiumOptions().auto_port()
co.headless(True)   # 无头模式
co.set_argument('--no-sandbox')
co.set_argument('--headless=new')
co.set_paths(browser_path="/opt/google/chrome/google-chrome")

browser = ChromiumPage(co)
tab = browser.latest_tab

# 开始执行自动化流
try:
    tab.get('https://sulianproxy.com/register')
    logger.info('打开网页：https://sulianproxy.com/register')
    time.sleep(2)
    tab.get_screenshot(path=r"xd/打开网页.png", full_page=True)

    # 1. 输入邮箱用户名 (根据 placeholder 定位最稳妥)
    ele = tab.ele('css=#input-11')
    ele.input(sign_email)
    logger.info(f'已输入邮箱用户名: {sign_email}')

    # 2. 核心修改：点击邮箱后缀下拉栏
    # 在 Vuetify 3 结构中，默认选中的是 @qq.com。点击它的父级或自身即可展开选项框。
    suffix_dropdown = tab.ele("text:@qq.com")
    if suffix_dropdown:
        suffix_dropdown.click()
        logger.info('已成功点击展开邮箱后缀下拉框')
        time.sleep(0.5)  # 等待下拉列表动画渲染渲染出来
        
        # 3. 选择 outlook 后缀
        # 弹出的列表会渲染在 body 的全局浮层里，直接点击文本包含 'outlook' 的行即可
        outlook_option = tab.ele("text:outlook")
        if outlook_option:
            outlook_option.click()
            logger.info('已成功选择 outlook.com 后缀')
        else:
            logger.error('未找到 outlook 选项，请检查页面是否支持该后缀')
    else:
        logger.error('未找到默认的 @qq.com 下拉触发器')

    time.sleep(0.5)
    tab.get_screenshot(path=r"xd/输入邮箱.png", full_page=True)

    # ================== 以下为你续写的注册后续流程 ==================

    # 4. 输入密码和确认密码 (使用页面属性定位)
    # password_input = tab.ele("xpath://input[@placeholder='输入密码']")
    # password_input.input("YourSecurePass123!") # 换成你要填写的统一密码
    
    # confirm_password_input = tab.ele("xpath://input[@placeholder='确认密码']")
    # confirm_password_input.input("YourSecurePass123!")
    # logger.info('已填写密码与确认密码')

    # # 5. 点击“发送验证码”按钮
    # # 源码中按钮包含文本“发送验证码”
    # send_code_btn = tab.ele("text:发送验证码")
    # if send_code_btn:
    #     send_code_btn.click()
    #     logger.info('已点击发送验证码按钮，请在后续逻辑中加入读取邮箱验证码')
    #     time.sleep(2)
    #     tab.get_screenshot(path=r"xd/已发验证码.png", full_page=True)
    # else:
    #     logger.error('未找到发送验证码按钮')
# try:
#     ele = tab.ele('text=点击注册')
#     ele.click()
# except:
#     pass
# ele = tab.ele('css=#email')
# ele.input(sign_email)
# logger.info(sign_email)
# logger.info('输入邮箱')
# tab.get_screenshot(path=r"xd/输入邮箱.png", full_page=True)
# ele = tab.ele('css=#email-verify')
# ele.click()
# logger.info('发送邮件')
# time.sleep(5)
# tab.get_screenshot(path=r"xd/发完邮件.png", full_page=True)


# ele = tab.ele('css=#success-confirm')

# ele.click()
# logger.info('点击好')

# ele = tab.ele('css=#passwd')
# ele.input('11111111')
# ele = tab.ele('css=#repasswd')
# ele.input('11111111')
# logger.info('输入账号密码')

# ele = tab.ele('css=#tos')
# ele.click(by_js=True)

# logger.info('点击我同意')
# tab.get_screenshot(path=r"./点击我同意.png", full_page=True)
# time.sleep(5)



# for _ in range(30):
#   time.sleep(1)
#   logger.info(f"等待邮箱中，第{_}S")


# EMAIL_ADDRESS = 'luo1764682172@163.com'
# cookies = os.environ.get("ydyp")
# EMAIL_PASSWORD = cookies # 请确保是网易邮箱的 IMAP 授权码

# # 连接网易 IMAP 服务器
# server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
# logger.info('连接网易服务器')

# # 添加 ID 命令支持
# imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
# logger.info('发送command命令')

# args = ("name", "imaplib", "version", "1.0.0")
# typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
# server._untagged_response(typ, dat, 'ID')

# # 登录邮箱
# server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
# logger.info('登录邮箱服务器')

# # 选中收件箱
# server.select("INBOX")
# logger.info('检查收件箱')

# # 搜索所有邮件 ID
# typ, data = server.search(None, 'ALL')
# all_ids = data[0].split()
# logger.info(f'共找到 {len(all_ids)} 封邮件')

# # 只取最新5封（若总数不足5封，就全部取）
# latest_ids = all_ids[-5:]

# # 拉取邮件
# fetch_data_lst = []
# for num in latest_ids:
#     typ, fetch_data = server.fetch(num, '(RFC822)')
#     fetch_data_lst.append(fetch_data)

# # 解析最新一封邮件（最后一封）
# fetch_data = fetch_data_lst[-1]
# msg = email.message_from_bytes(fetch_data[0][1])
# logger.info('获取邮箱字节数据')
# logger.info(f'原始主题: {msg["subject"]}')

# # 解码主题（更可靠的方式）
# from email.header import decode_header
# subject_parts = decode_header(msg['subject'])
# decoded_subject = ''.join([
#     (part.decode(charset or "utf-8") if isinstance(part, bytes) else part)
#     for part, charset in subject_parts
# ])
# logger.info(f'解码后主题: {decoded_subject}')
# body = ""
# if msg.is_multipart():
#     for part in msg.walk():
#         content_type = part.get_content_type()
#         content_dispo = str(part.get("Content-Disposition"))
#         if content_type in ["text/plain", "text/html"] and "attachment" not in content_dispo:
#             charset = part.get_content_charset() or 'utf-8'
#             body = part.get_payload(decode=True).decode(charset, errors="replace")
#             break
# else:
#     charset = msg.get_content_charset() or 'utf-8'
#     body = msg.get_payload(decode=True).decode(charset, errors="replace")

# # 如果是 HTML，提取纯文本
# if "<html" in body.lower():
#     soup = BeautifulSoup(body, "html.parser")
#     text = soup.get_text(separator=' ', strip=True)  # 加 separator 保证内容连贯
#     text = re.sub(r'\s+', ' ', text)  # 把多余空白变成单个空格
# else:
#     text = body

# logger.info(f'纯文本正文:\n{text}')

# # 匹配验证码（6位数字，通常居中或在提示后）
# match = re.search(r'邮箱验证代码为: ([a-zA-Z0-9]+)', text)
# if not match:
#     match = re.search(r'\b\d{6}\b', text)  # 备选策略：直接找6位数字

# if match:
#     code = match.group(1)
#     logger.info(f'提取验证码: {code}')
# else:
#     logger.info('未找到验证码')

# codeele = tab.ele('css=#emailcode')
# codeele.input(match.group(1))
# logger.info('输入验证码')
# time.sleep(1)
# tab.get_screenshot(path=r"./输完验证码.png", full_page=True)
# ele = tab.ele('text=注册新账户')
# ele1 = tab.ele('css=#confirm-register')
# ele2 = tab.ele('css=body > div.page.page-center > div > div.card.card-md > div > div.form-footer')
# ele2 = ele2.child()
# tab.listen.start(targets='https://www.xdduck.live/user')  # 开始监听，指定获取包含该文本的数据包

# # # 数字加 1
# number += 1
# # 将更新后的数字写回文件
# with open('xd/xdnum.txt', "w", encoding="utf-8") as file:
#     file.write(str(number))
# logger.info(f"新的数字已写入: {number}")

# ele.click()
# time.sleep(0.2)
# try:
#     ele.click()
#     time.sleep(1)
# except:
#     pass



# logger.info('注册')

# tab.get_screenshot(path=r"./点击注册后.png", full_page=True)
# try:
#     ele = tab.ele('css=#announcement-modal > div > div > div.modal-footer > button')
#     ele.click()
#     logger.info('关闭广告弹窗')
# except:
#     pass
# try:
#     res = tab.listen.wait(timeout=10).response
#     res = res.body
#     pattern = r'https://sub\.xdduck\.cc/sub/[a-f0-9]+/clash'
#     matches = re.findall(pattern, res)
#     # 去重并打印
#     for link in set(matches):
#         logger.info(f"找到订阅链接: {link}")
# except:
#     with open(r"./test_browser.html", "w", encoding="utf-8") as f:
#         f.write(tab.html)
#     with open('test_browser.html', 'r', encoding='utf-8') as f:
#         html_content = f.read()

#     # 匹配以 https 开头，包含该域名的 clash 订阅链接
#     pattern = r'https://sub\.xdduck\.cc/sub/[a-f0-9]+/clash'
#     # 查找所有匹配项
#     matches = re.findall(pattern, html_content)
#     # 去重并打印
#     for link in set(matches):
#         logger.info(f"找到订阅链接: {link}")



# # tab.get_screenshot(path=r"./1.png", full_page=True)



# headers_clash ={
# "User-Agent":"clash"
# }
# with open("xd/xdurls.txt", "w") as file:
#     file.write(link + "\n")
# res = requests.get(link,headers=headers_clash)
# res_text = res.content.decode('utf-8')
# modified_str = res_text.replace('enable: true', 'enable: false')
# with open("xd/xd.yaml", "w") as file:
#     file.write(modified_str)



except Exception as main_e:
    logger.error(f'自动化执行流程中发生异常: {main_e}')
    tab.get_screenshot(path=r"xd/异常错误截图.png", full_page=True)

finally:
    # 无论成功失败，关闭浏览器释放内存
    browser.quit()
    logger.info('浏览器已关闭，主程序退出。')

# browser.quit()
