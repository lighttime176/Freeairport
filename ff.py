from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
import logging,random,time,requests,os,re
import imaplib
import email
headers ={
"User-Agent":"clash"
}
def email_163():
    cookies = os.environ.get("ydyp")
    logger.info(type(cookies)) 
    EMAIL_ADDRESS = 'luo1764682172@163.com'
    EMAIL_PASSWORD = cookies
    server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
    logger.info('连接网易服务器') 
    #网易邮箱需要发送额外的Command验证后才能登录
    #https://blog.csdn.net/jony_online/article/details/108638571
    imaplib.Commands ['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
    logger.info('发送command命令') 
    args = ("name", "imaplib", "version", "1.0.0")
    typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
    server.login (EMAIL_ADDRESS, EMAIL_PASSWORD)
    logger.info('登录邮箱服务器') 
    #print(server.list())
    server.select("INBOX")
    logger.info('检查收件箱') 
    typ,data = server.search(None,'ALL')#'ALL',or 'SEEN'
    data[0].split()
    fetch_data_lst = []
    for num in data[0].split():
        typ,fetch_data = server.fetch(num,'(RFC822)')
        fetch_data_lst.append(fetch_data)
    # for fetch_data in fetch_data_lst:
    #     msg = email.message_from_bytes(fetch_data[0][1])
    #     for part in msg.walk():
    #         print(part.get_content_type())
    #         if part.get_content_maintype() == 'text':
    #             body = part.get_payload(decode=True)
    #             text = body.decode('utf8')
    #             print(text)
    fetch_data = fetch_data_lst[-1]
    msg = email.message_from_bytes(fetch_data[0][1])
    logger.info('获取邮箱字节数据') 
    #print(msg)
    logger.info((msg['subject']))
    # result = msg['subject'].find('Mickey')
    # print('result:',result)

    for part in msg.walk():
        #print(part.get_content_type())
        if part.get_content_maintype() == 'text':
            body = part.get_payload(decode=True)
            text = body.decode('utf8')
            #print(text)
    match = re.search(r"验证码是：(\d+)", text)
    if match:
        verification_code = match.group(1)
        logger.info("验证码:", verification_code)
    else:
        logger.info("未找到验证码")
    return verification_code
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
for i_sleepcode in range(6):
    logger.info(f"等待邮件中,第{i_sleepcode}0秒")
    time.sleep(10)
    
vcode = email_163()
logger.info(vcode)
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > div.styles_xhBix > input')
ele.input(vcode)
tab.listen.start(targets='www.yhcvpn.xyz',timeout = 30)  # 开始监听，指定获取包含该文本的数据包
ele = tab.ele('css=#root > div.styles_C6Q6h > div.styles_svCqL > div.styles_2koXy > button')
ele.click()

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
