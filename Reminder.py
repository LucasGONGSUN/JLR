import json, datetime, smtplib, schedule
from email.mime.text import MIMEText
from email.header import Header

#Setting
TodayContent = {}
LearningContent = []

# === Get Checklist dict from Json as a dict === #
def Json2Dict():
    global Checklist, Contentlist
    FileJsonName_date = 'calendar.json'
    with open(FileJsonName_date, 'r') as d:
        Checklist = json.load(d)
    FileJsonName_content = 'contents.json'
    with open(FileJsonName_content, 'r') as c:
        Contentlist = json.load(c)

# === Get TodayQuest from dict === #
def GetQuest():
    global TodayList, TodayQuest
    TodayDate = datetime.datetime.today()
    Today = str(datetime.datetime(TodayDate.year, TodayDate.month, TodayDate.day, 0,0,0))
    TodayList = Checklist[Today]
    TodayQuest = '今天的学习任务是：' + str(TodayList) + '\n\n'

# === Get TodayContents from Excel === #
def GetContent():
    global TodayContent
    for i in TodayList:
        try:
            TodayContent[i] = Contentlist[i]
        except KeyError:
            continue

# === Create MailContent for pushing === #
def CreateMailContent():
    global MailContent
    for keys, values in TodayContent.items():
        entry_key = '\n' + keys + '\n'
        LearningContent.append(entry_key)
        for value in values:
            entry_value = value + '\n'
            LearningContent.append(entry_value)
    LearningContent_str = " ".join(LearningContent)
    MailContent = TodayQuest + LearningContent_str

# === Creat mail === #
def SendMail():
    #Set mail box
    from_addr = '37870979@qq.com'
    password = 'fcapyvxmjdbzbgji'
    to_addr = 'lucasgongsun@163.com'
    smtp_server = 'smtp.qq.com'
    #Set content
    msg = MIMEText(MailContent, 'plain', 'utf-8')
    #Set mail header
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('今日学习任务')
    #Send
    server = smtplib.SMTP_SSL(host=smtp_server)
    server.connect(smtp_server,465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

# === Schedule === #
def job():
    Json2Dict()
    GetQuest()
    GetContent()
    CreateMailContent()
    SendMail()
    print('Mail Sent!')

#schedule.every().day.at("8:00").do(job)
job()

