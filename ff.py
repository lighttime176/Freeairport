from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging,random,time,email5,requests

headers ={
"User-Agent":"clash"
}
def logging_init():
  # 创建一个logger对象
  logger = logging.getLogger('my_logger')
  logger.setLevel(logging.INFO)  # 设置日志级别为INFO

  # 创建一个控制台处理器，输出到控制台
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)  # 设置控制台日志级别为INFO

  # 创建一个文件处理器，输出到文件
  file_handler = logging.FileHandler('test.log')
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
co.set_user_agent("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0") 
# co.incognito(True)
co.remove_extensions()
browser = ChromiumPage(co)

tab = browser.latest_tab
# tab.set.cookies(cookies)

logger.info('打开FireFly url')
tab.get('https://www.yhcvpn.xyz/index.php#/register')
account = ''
randomlength = 10
base_str = 'abcdefghijklmnopqrstuvwxyz0123456789'
length = len(base_str) - 1
for i in range(randomlength):
    account += base_str[random.randint(0, length)]
account = f"{account}@176468.xyz"
logger.info(account)
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > input:nth-child(1)')
ele.input(account)
logger.info(f'输入邮箱{account}')
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > div.styles_xhBix > button > span')
ele.click()
logger.info('发送邮件')
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > span:nth-child(3) > input')
ele.input('123456789')
logger.info('输入密码')
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > span:nth-child(4) > input')
ele.input('123456789')
logger.info('再次输入密码')
for i_sleepcode in range(3):
    logger.info(f"等待邮件中,第{i_sleepcode}0秒")
    time.sleep(10)
    
vcode = email5.email_163()
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > div.styles_xhBix > input')
ele.input(vcode)
tab.listen.start(targets='www.yhcvpn.xyz')  # 开始监听，指定获取包含该文本的数据包
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > button')
ele.click()
tab.get_screenshot(path=r"./test_browser_page.png", full_page=True)
with open(r"./test_browser.html", "w", encoding="utf-8") as f:
    f.write(tab.html)
logger.info('注册')
res = tab.listen.wait().response
res = res.body
logger.info(res)
token = res['data']['token']
clash_url = f"https://www.yhc1314dy.link/api/v1/client/subscribe?token={token}"
logger.info(clash_url)
response = ''
response = requests.get(clash_url,headers=headers)
with open('clash.yaml', 'w', encoding='utf-8') as file:
    file.writelines(response.text)
browser.quit()
