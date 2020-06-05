import json, smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.header import Header

# Settings
# --- File --- #
FileJsonName_date = 'Calendar.json'
FileJsonName_content = 'JLR_Contents.json'
FileJsonName_user = 'UserInfo.json'

# --- Date --- #
TodayDate = datetime.today()
Today = datetime(TodayDate.year, TodayDate.month, TodayDate.day, 0,0,0)


# ##### Get CheckList, ContentList and UserList from Json as dicts ##### #
def Json2Dict():
    global CheckList, ContentList, UserList
    
    # Load Calendar from 'Calendar.json'
    with open(FileJsonName_date, 'r') as dr:
        CheckList = json.load(dr)

    # Load ContentList from 'JLR_Contents.json'
    with open(FileJsonName_content, 'r') as cr:
        ContentList = json.load(cr)

    # Load User Info from 'UserInfo.json'
    with open(FileJsonName_user, 'r') as ur:
        UserList = json.load(ur)


# ##### Define class Learner() ##### #
class Learner:
    
    def GetStartDay(self, UserList, LearnerNumber):
        """
            Get StartDay from UserList
        """
        StartDay = UserList[LearnerNumber]['FirstDay']
        return StartDay

    def GetDayNumber(self, StartDay, Today):
        """
            Get DayNumber of learning contents of today
        """
        DayFrom = datetime.strptime(StartDay, '%Y-%m-%d %H:%M:%S')
        DayNumber = int((Today-DayFrom).days) + 1
        return DayNumber

    def GetTodayList(self, CheckList, DayNumber):
        """
            Get today's list numbers of contents
        """
        TodayList = CheckList[DayNumber]
        return TodayList

    def GetTodayContent(self, ContentList, TodayList):
        """
            Get learning contents for today from ContentList
        """
        # Get New contents for today
        TodayNew = {}
        for i in TodayList[:1]:
            try:
                TodayNew[i] = ContentList[i]
            except KeyError:
                TodayNew['无'] = '无新学习内容'
                continue
        
        # Get Review contents for today
        TodayReview ={}
        for i in TodayList[1:]:
            try:
                TodayReview[i] = ContentList[i]
            except KeyError:
                continue
        return TodayNew, TodayReview

    def GetMailInfo(self, UserList, LearnerNumber):
        """
            Get MailAddr from UserList
        """
        MailTo = str(UserList[LearnerNumber]['ID'])
        MailAddr = UserList[LearnerNumber]['MailAddr']
        return MailTo, MailAddr

    def CreateMailContent(self, MailTo, TodayNew, TodayReview):
        """
            Create mail content for pushing
        """
        # Get numbers and contents for today's learning
        NewContent = []
        NewContent.append("\n\n\n>>> Today's Learning Contents <<<\n")
        for nums, contents in TodayNew.items():
            entry_num = "\n\n=== Learning Contents %s ===\n" %nums
            NewContent.append(entry_num)

            # Get Kanzi and DETAILS_DICT from CONTENTS_DICT
            try:
                for kanzis, details in contents.items():
                    entry_kanzi = '\n --- %s --- \n' %kanzis
                    NewContent.append(entry_kanzi)

                    #Get details from DETAILS_DICT
                    for keys, values in details.items():
                        entry_keys_values = '%s : %s \n' %(keys, values)
                        NewContent.append(entry_keys_values)
            except AttributeError:
                NewContent.append('\nNo new learnning contents for today.')
    
        # Get numbers and contents for today's reviewing
        ReviewContent = []
        ReviewContent.append("\n\n\n>>> Today's Reviewing Contents <<<\n")
        for nums, contents in TodayReview.items():
            entry_num = "\n\n=== Reviewing Contents %s ===\n" %nums
            ReviewContent.append(entry_num)

            # Get Kanzi and DETAILS_DICT from CONTENTS_DICT
            for kanzis, details in contents.items():
                entry_kanzi = '\n --- %s --- \n' %kanzis
                ReviewContent.append(entry_kanzi)

                #Get details from DETAILS_DICT
                for keys, values in details.items():
                    entry_keys_values = '%s : %s \n' %(keys, values)
                    ReviewContent.append(entry_keys_values)
    
        #Combine together
        LearningContent_str = " ".join(NewContent) + " ".join(ReviewContent)
        Greeting = '\nHello %s :' %MailTo
        MailContent =  Greeting + LearningContent_str
        return MailContent


# ##### Draw mails for each user #### #
def MailDraw():
    # Show List of User Info
    print('\n=== Drawing mails for users as follows ===\n')
    IndexNo = 1
    for nums, details in UserList.items():
        print('No.%s : %s - %s ' %(str(IndexNo), nums, details['ID']))
        IndexNo += 1
    
    # Show List of Daily Contents
    DrawCheckPoint = input('\nPlease check user list above, Enter Y to continue: ')
    if DrawCheckPoint == 'Y':
        print('\n')
        for i, details in UserList.items():
            Receiver = Learner()
            StartDay = Receiver.GetStartDay(UserList, i)
            DayNumber = str(Receiver.GetDayNumber(StartDay, Today))
            TodayList = Receiver.GetTodayList(CheckList, DayNumber)
            MailTo, MailAddr = Receiver.GetMailInfo(UserList, i)
            print('%s : %s (%s) - %s' %(i, MailTo,MailAddr, TodayList))


# ##### Check and Send mail to each user ##### #
def MailSend():
    SendCheckPoint = input('\nPlease check daily learning list of each user, Enter Y to send: ')
    if SendCheckPoint == 'Y':

        # Set mail box and log in
        from_addr = '37870979@qq.com'
        password = 'fcapyvxmjdbzbgji'
        smtp_server = 'smtp.qq.com'
        server = smtplib.SMTP_SSL(host=smtp_server)
        server.connect(smtp_server, 465)
        server.login(from_addr, password)

        # Set mail content
        for i in UserList.keys():
            print('\n\nCreating learner profile for %s...' %i)
            Receiver = Learner()

            print('Getting list of learning content ...')
            StartDay = Receiver.GetStartDay(UserList, i)
            DayNumber = str(Receiver.GetDayNumber(StartDay, Today))
            TodayList = Receiver.GetTodayList(CheckList, DayNumber)

            print('Getting lerning content of %s...'  %TodayList)
            TodayNew, TodayReview = Receiver.GetTodayContent(ContentList, TodayList)

            print('Drawing E-mail ...')
            #Set mail text
            MailTo, MailAddr = Receiver.GetMailInfo(UserList, i)
            MailContent = Receiver.CreateMailContent(MailTo, TodayNew, TodayReview)
            msg = MIMEText(MailContent, 'plain', 'utf-8')

            #Set mail header
            msg['From'] = Header(from_addr)
            msg['To'] = MailAddr
            msg['Subject'] = Header('今日学习内容')

            #Send
            print('Mail to %s is sending ...' %i)
            server.sendmail(from_addr, MailAddr, msg.as_string())
    
        # Log out
        server.quit()

    else:
        pass


# Main body
def DrawAndSend():
    Json2Dict()
    MailDraw()
    MailSend()
    print('\n>>> All mails are sent! <<<')


#DrawAndSend()
