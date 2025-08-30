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
  file_handler = logging.FileHandler('hx/hx.log')
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
