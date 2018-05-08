import smtplib
import os.path as pth
import time
from email.mime.text import MIMEText
from email.header import Header

def sendEmail(content, title, from_name, from_address, to_address, serverport, serverip, username, password):
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = Header(title, 'utf-8')
    # 这里的to_address只用于显示，必须是一个string
    msg['To'] = ','.join(to_address)
    msg['From'] = from_name
    try:
        s = smtplib.SMTP_SSL(serverip, serverport)
        s.login(username, password)
        # 这里的to_address是真正需要发送的到的mail邮箱地址需要的是一个list
        s.sendmail(from_address, to_address, msg.as_string())
        print('%s----发送邮件成功' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    except Exception as err:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print(err)
#HEFEN_D = pth.abspath(pth.dirname(__file__))

def main2():
    TO = ['274717413@qq.com']
    config = {
        "from": "773767639@qq.com",
        "from_name": '骆驼userAPI自动化测试报告:',
        "to": TO,
        "serverip": "smtp.qq.com",
        "serverport": "465",
        "username": "773767639@qq.com",
        "password": "nukzwhfhhifrbdbg"  # QQ邮箱的SMTP授权码
    }

    title = "骆驼userAPI自动化测试报告"
    f = open("/var/lib/jenkins/workspace/birdmanagerAPI/report/result.html", 'rb')
    #f = open("C:\\Users\\liugc\\PycharmProjects\\birdmanagerAPI\\report\\result.html", 'rb')
    mail_body = f.read()
    f.close()
    sendEmail(mail_body, title, config['from_name'], config['from'], config['to'], config['serverport'], config['serverip'],
              config['username'], config['password'])
