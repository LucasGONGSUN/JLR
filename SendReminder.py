import json, datetime, smtplib, schedule
from email.mime.text import MIMEText
from email.header import Header

# Settings
#MailToList = ['lucasgongsun@163.com', '443936352@qq.com']   ### Only for testing
MailToList = ['lucasgongsun@163.com', '443936352@qq.com', 'jo.wang.220@hotmail.com']
TodayContent = {}
LearningContent = []


# === Get Checklist and Contentlist from Json as dicts === #
def Json2Dict():
    global Checklist, Contentlist
    FileJsonName_date = 'Calendar.json'
    with open(FileJsonName_date, 'r') as d:
        Checklist = json.load(d)
    FileJsonName_content = 'contents_fromInput.json'
    with open(FileJsonName_content, 'r') as c:
        Contentlist = json.load(c)


# === Get TodayQuest from Checklist === #
def GetQuest():
    global TodayList, TodayQuest
    TodayDate = datetime.datetime.today()
    Today = str(datetime.datetime(TodayDate.year, TodayDate.month, TodayDate.day, 0,0,0))
    TodayList = Checklist[Today]
    TodayQuest = '今天的学习任务是：' + str(TodayList)


# === Get TodayContents from Contentlist === #
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

    #Get Number and CONTENTS_DICT from TodayContent
    for nums, contents in TodayContent.items():
        entry_num = '\n\n\n === Learning Contents %s === \n' %nums
        LearningContent.append(entry_num)

        #Get Kanzi and DETAILS_DICT from CONTENTS_DICT
        for kanzis, details in contents.items():
            entry_kanzi = '\n --- %s --- \n' %kanzis
            LearningContent.append(entry_kanzi)

            #Get details from DETAILS_DICT
            for keys, values in details.items():
                entry_keys_values = '%s : %s \n' %(keys, values)
                LearningContent.append(entry_keys_values)

    #Combine together
    LearningContent_str = " ".join(LearningContent)
    MailContent = TodayQuest + LearningContent_str


# === Create mail === #
def SendMail():
    #Set mail box
    from_addr = '37870979@qq.com'
    password = 'fcapyvxmjdbzbgji'
    to_addrs = MailToList
    smtp_server = 'smtp.qq.com'

    #Set content
    msg = MIMEText(MailContent, 'plain', 'utf-8')

    #Set mail header
    msg['From'] = Header(from_addr)
    msg['To'] = ','.join(to_addrs)
    msg['Subject'] = Header('今日学习任务')

    #Send
    server = smtplib.SMTP_SSL(host=smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addrs, msg.as_string())
    server.quit()


# === Schedule === #
def DrawAndSend():
    Json2Dict()
    GetQuest()
    GetContent()
    CreateMailContent()
    SendMail()
    print('All mails are sent!')

#schedule.every().day.at("8:00").do(job)
#DrawAndSend()
