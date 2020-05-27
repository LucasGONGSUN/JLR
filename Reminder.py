import openpyxl, datetime, smtplib, schedule
from email.mime.text import MIMEText
from email.header import Header

#Setting
wb = openpyxl.load_workbook('calendar.xlsx')
ws = wb['Jap']
datelist = []
notelist = []
checklist = {}

# === Create list === #
def getquest():
    global todayquest
    #Read date
    for row in ws.iter_rows(min_row=1, max_col=1, max_row=185):
        for cell in row:
            datelist.append(cell.value)
    #Read list
    for row in ws.iter_rows(min_row=1, max_row=185, min_col=2, max_col=8):
        new_row = []
        for cell in row:
            new_row.append(cell.value)
        notelist.append(new_row)
    #Combine date and list
    for i in range(185):
        checklist[datelist[i]] = notelist[i]

    # === Get today quest === #
    a = datetime.datetime.today()
    today = datetime.datetime(a.year, a.month, a.day, 0,0,0)
    todaylist = checklist[today]
    todaylist_str = "；".join(todaylist)
    todayquest = '今天的学习任务是：' + todaylist_str

# === Creat mail === #
def sendmail():
    #Set mail box
    from_addr = '37870979@qq.com'
    password = 'fcapyvxmjdbzbgji'
    to_addr = 'lucasgongsun@163.com'
    smtp_server = 'smtp.qq.com'
    #Set content
    msg = MIMEText(todayquest, 'plain', 'utf-8')
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
    getquest()
    sendmail()

schedule.every().day.at("8:00").do(job)

