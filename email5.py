import imaplib
import email
import re
def email_163():
    EMAIL_ADDRESS = 'luo1764682172@163.com'
    EMAIL_PASSWORD = 'ZHQgy35wE28LqzTU'
    server = imaplib.IMAP4_SSL(host='imap.163.com', port=993)
    #网易邮箱需要发送额外的Command验证后才能登录
    #https://blog.csdn.net/jony_online/article/details/108638571
    imaplib.Commands ['ID'] = ('NONAUTH', 'AUTH', 'SELECTED')
    args = ("name", "imaplib", "version", "1.0.0")
    typ, dat = server._simple_command('ID', '("' + '" "'.join(args) + '")')
    server.login (EMAIL_ADDRESS, EMAIL_PASSWORD)
    #print(server.list())
    server.select("INBOX")
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
    #print(msg)
    print((msg['subject']))
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
        print("验证码:", verification_code)
    else:
        print("未找到验证码")
    return verification_code
