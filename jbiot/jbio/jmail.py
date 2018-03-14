#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from email.mime.text import MIMEText
import smtplib
from email.header import Header
from email.utils import parseaddr,formataddr

def jmail(reciever,subject="",msg="",msgtype="plain"):

    msg = MIMEText(msg,msgtype,'utf-8')
    msg["From"] = Header(u"晶宝")
    msg["Subject"] = Header(subject)

    sender = 'kong_deju@gene.ac'
    password = '123aaaa'
    smtp_server = 'smtp.ym.163.com'

    s = smtplib.SMTP(smtp_server,25)
    #s.set_debuglevel(1)
    s.login(sender,password)
    s.sendmail(sender,reciever,msg.as_string())
    s.quit()

if __name__ == "__main__":
    jmail("kongdeju@gene.ac",u"测试以下","msg")
