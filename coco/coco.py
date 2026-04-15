from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging,random,time,os,re,requests
import imaplib,sys
import email
from bs4 import BeautifulSoup
import os,ast,logging,re,email,imaplib,time
from email.header import decode_header
import pyperclip
import pyperclip
headers ={
"User-Agent":"clash"
}
# with open('email.txt', 'r', encoding='utf-8') as f:
#     content = f.read().strip()

# email_list = ast.literal_eval(content)
# 读取文件中的数字
# with open('num.txt', "r", encoding="utf-8") as file:
#     try:
#         number = int(file.read().strip())  # 读取并转换为整数
#     except ValueError:
#         number = 0  # 如果文件内容不是数字，初始化为 0

# signemail = email_list[number]
# signemail = signemail + '@outlook.com'




def logging_init():
  # 创建一个logger对象
  logger = logging.getLogger('my_logger')
  logger.setLevel(logging.INFO)  # 设置日志级别为INFO

  # 创建一个控制台处理器，输出到控制台
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)  # 设置控制台日志级别为INFO

  # 创建一个文件处理器，输出到文件
  file_handler = logging.FileHandler('ok.log')
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



tab.get('https://www.cocoduck.live/auth/login')
logger.info('打开coco url')
ele = tab.ele('css=#email')
ele.input('b1rtyuii98@outlook.com')
logger.info('输入邮箱')
ele = tab.ele('css=#passwd')
ele.input('11111111')
logger.info('输入邮箱')
ele = tab.ele('css=#login-dashboard')

# tab.listen.start(targets='https://www.cocoduck.live/user')  # 开始监听，指定获取包含该文本的数据包

ele.click()
time.sleep(5)
tab.get_screenshot(path=r"./coco登录.png", full_page=True)
ele = tab.ele('css=#announcement-modal > div > div > div.modal-footer > button')
ele.click()
tab.get_screenshot(path=r"./coco关闭广告.png", full_page=True)
ele = tab.ele('css=body > div.page > div > div.page-body > div > div > div:nth-child(1) > div > div > div:nth-child(4) > div > div > div > button.btn.btn-red.btn-sm.client-btn')

ele.click()
link = pyperclip.paste()
tab.get_screenshot(path=r"./coco点击复制.png", full_page=True)


logger.info(link)
print(ele)
# time.sleep(0.5)
# link = pyperclip.paste()
# print(link)

# res = tab.listen.wait(timeout=10).response
# res = res.body

# logger.info(res)
# 匹配以 https 开头，包含该域名的 clash 订阅链接
# pattern = r'https://sub\.cocoduck\.cc/sub/[a-f0-9]+/clash'


# # 查找所有匹配项
# matches = re.findall(pattern, link)

# # 去重并打印
# for link in set(matches):
#     print(f"找到订阅链接: {link}")
# time.sleep(10)
# ele = tab.ele('css=body > div.page > div > div.page-body > div > div > div:nth-child(1) > div > div > div:nth-child(4) > div > div > div > button.btn.btn-red.btn-sm.client-btn')
# ele.click()
# time.sleep(1)
# tab.get_screenshot(path=r"./1.png", full_page=True)
# with open(r"./coco.html", "w", encoding="utf-8") as f:
#     f.write(tab.html)




