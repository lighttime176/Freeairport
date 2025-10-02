from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging,random,time,requests,os,re
import imaplib,sys
import email
import ast



# 读取 email.txt 文件
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../email.txt')
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 转换成 Python 列表
emails = ast.literal_eval(content)


file_path = "yylx/yylxnum.txt"


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
  # 创建一个logger对象
  logger = logging.getLogger('my_logger')
  logger.setLevel(logging.INFO)  # 设置日志级别为INFO

  # 创建一个控制台处理器，输出到控制台
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)  # 设置控制台日志级别为INFO

  # 创建一个文件处理器，输出到文件
  file_handler = logging.FileHandler('yylx/yylx.log')
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
co.set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0") 
# co.incognito(True)
co.remove_extensions()
browser = ChromiumPage(co)

tab = browser.latest_tab
# tab.set.cookies(cookies)

logger.info('打开yylx url')
tab.get('https://yylx7.yylxjichang.link/#/register')

account = sign_email

logger.info(account)

ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div.form-group.v2board-email-whitelist-enable > input')
ele.input(account)

ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div.form-group.v2board-email-whitelist-enable > select')
ele.select.by_value('outlook.com')
ele.click()

ele = tab.ele('text=发送')
ele.click()
# ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div.form-group.form-row > div.col-3 > button')
# ele.click()


ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div:nth-child(3) > input')
ele.input('11111111')
ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div:nth-child(4) > input')
ele.input('11111111')
for _ in range(60):
  time.sleep(1)
  print(f"等待邮箱中，第{_}S")
tab.get_screenshot(path=r"./1.png", full_page=True)
# cookies = os.environ.get("ydyp")
# EMAIL_ADDRESS = 'luo1764682172@163.com'
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
# match = re.search(r'您的验证码是：.*?(\d{6})', text)  # 例如："请填写以下验证码完成邮箱验证...288437"
# if not match:
#     match = re.search(r'\b\d{6}\b', text)  # 备选策略：直接找6位数字

# if match:
#     code = match.group(1)
#     logger.info(f'提取验证码: {code}')
# else:
#     logger.info('未找到验证码')
# codeele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div.form-group.form-row > div.col-9 > input')
# codeele.input(match.group(1))

# ele = tab.ele('css=#main-container > div.no-gutters.v2board-auth-box > div > div > div > div.row.no-gutters > div > div > div:nth-child(2) > div.form-group.mb-0 > button')
# tab.listen.start(targets='/register')  # 开始监听，指定获取包含该文本的数据包
# ele.click()
# tab.get_screenshot(path=r"./1.png", full_page=True)
# res = tab.listen.wait(timeout=10).response
# res = res.body
# logger.info(res)
# tab.get_screenshot(path=r"./1.png", full_page=True)
# # 数字加 1
# try:
#     if(res['data']['is_admin'] == None):
#         number += 1
# except:
#     pass

# # 将更新后的数字写回文件
# with open(file_path, "w", encoding="utf-8") as file:
#     file.write(str(number))
# print(f"新的数字已写入: {number}")
