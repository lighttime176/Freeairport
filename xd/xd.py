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

page = ChromiumPage(addr_or_opts=co)
page.get("https://sulianproxy.com/register")
page.get_screenshot(path=r"xd/打开网页.png", full_page=True)
page.wait.doc_loaded()
time.sleep(2)
logger.info("[OK] 页面加载成功:", page.title)

page.run_js("window.focus();")

# === 1. 邮箱前缀 ===
page.ele("#input-1").input(sign_email)
logger.info("[OK] 已输入邮箱前缀")
page.get_screenshot(path=r"xd/输入邮箱.png", full_page=True)
# === 2. 展开下拉框，点击 outlook ===
for d in page.eles("tag:div"):
    cls = d.attr("class") or ""
    if "register-email-suffix" in cls:
        d.click()
        break
time.sleep(1.5)

result = page.run_js("""
    const items = document.querySelectorAll('.v-list-item');
    for (const item of items) {
        const title = item.querySelector('.v-list-item-title');
        if (title && title.textContent.includes('@outlook.com')) {
            item.click();
            return 'OK';
        }
    }
    return 'NOT_FOUND';
""")
logger.info(f"[OK] 选择 @outlook.com ({result})")
time.sleep(0.5)
page.ele("#input-3").input("11111111")
page.ele("#input-6").input("11111111")
logger.info("[OK] 已输入密码")
page.ele('css=#app > div > div > div.v-row.v-row--no-gutters.bg-containerBg.position-relative > div.v-col-lg-12.v-col-12.d-flex.align-center > div > div > div > div > div > div.v-card-text.pa-sm-10.pa-6 > form > div:nth-child(2) > div > button > span.v-btn__content').click()
# === 3. 密码 ===
page.ele("css=body > div.v-overlay-container > div > div.v-overlay__content > div > div.v-card-actions.px-6.pb-6.pt-0 > button > span.v-btn__content").click()
time.sleep(0.5)
page.get_screenshot(path=r"xd/over.png", full_page=True)


for _ in range(30):
  time.sleep(1)
  logger.info(f"等待邮箱中，第{_}S")


EMAIL_ADDRESS = 'luo1764682172@163.com'
cookies = os.environ.get("ydyp")
EMAIL_PASSWORD = cookies # 请确保是网易邮箱的 IMAP 授权码

# 连接网易 IMAP 服务器
server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
logger.info('连接网易服务器')

# 添加 ID 命令支持
imaplib.Commands['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
logger.info('发送command命令')

args = ("name", "imaplib", "version", "1.0.0")
typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
server._untagged_response(typ, dat, 'ID')

# 登录邮箱
server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
logger.info('登录邮箱服务器')

# 选中收件箱
server.select("INBOX")
logger.info('检查收件箱')

# 搜索所有邮件 ID
typ, data = server.search(None, 'ALL')
all_ids = data[0].split()
logger.info(f'共找到 {len(all_ids)} 封邮件')

# 只取最新5封（若总数不足5封，就全部取）
latest_ids = all_ids[-5:]

# 拉取邮件
fetch_data_lst = []
for num in latest_ids:
    typ, fetch_data = server.fetch(num, '(RFC822)')
    fetch_data_lst.append(fetch_data)

# 解析最新一封邮件（最后一封）
fetch_data = fetch_data_lst[-1]
msg = email.message_from_bytes(fetch_data[0][1])
logger.info('获取邮箱字节数据')
logger.info(f'原始主题: {msg["subject"]}')

# 解码主题（更可靠的方式）
from email.header import decode_header
subject_parts = decode_header(msg['subject'])
decoded_subject = ''.join([
    (part.decode(charset or "utf-8") if isinstance(part, bytes) else part)
    for part, charset in subject_parts
])
logger.info(f'解码后主题: {decoded_subject}')
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

# 如果是 HTML，提取纯文本
if "<html" in body.lower():
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text(separator=' ', strip=True)  # 加 separator 保证内容连贯
    text = re.sub(r'\s+', ' ', text)  # 把多余空白变成单个空格
else:
    text = body

logger.info(f'纯文本正文:\n{text}')

# 匹配验证码（6位数字，通常居中或在提示后）
match = re.search(r'请忽略此邮件。 ([a-zA-Z0-9]+)', text)
if not match:
    match = re.search(r'\b\d{6}\b', text)  # 备选策略：直接找6位数字

if match:
    code = match.group(1)
    logger.info(f'提取验证码: {code}')
else:
    logger.info('未找到验证码')


page.ele("#input-15").input(match.group(1))
print("[OK] 已输入验证码")
logger.info('输入验证码')
time.sleep(1)
page.get_screenshot(path=r"xd/输完验证码.png", full_page=True)
# time.sleep(0.5)
# for btn in page.eles("tag:button"):
#     if btn.text.strip() == "创建账号":
#         btn.click()
#         print("[OK] 已点击「创建账号」按钮")
#         break
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





# browser.quit()
