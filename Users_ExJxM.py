import json, openpyxl, pymongo
from datetime import datetime


# Settings
FileExcelName_User = 'Users.xlsx'
FileJsonName_User = 'UserInfo.json'

DatabaseName = 'JLR_Alpha_June'
CollectionName = 'JLR_User'

# ##### Convert Excel contents to Json file ##### #
def ExcelToJson():
    LoadUserInfo()
    CreateUserList()
    SaveJsonFile()


# === Load User Infos from Excel === #
def LoadUserInfo():
    global ws, rows, cols
    wb = openpyxl.load_workbook(FileExcelName_User)
    ws = wb['JLR']
    rows = ws.max_row
    cols = ws.max_column


# === Create list of users for Json === #
def CreateUserList():
    global UserList
    Headers = []
    UserList = {}

    # Load Headers
    for row in ws.iter_rows(max_row=1, max_col=cols):
        for cell in row:
            Headers.append(cell.value)

    # Load details of Users
    for row in ws.iter_rows(min_row=2, max_row=rows, max_col=cols):
        LearnerNumber = row[1].value
        ID = row[2].value
        FirstDay = row[3].value
        MailAddr = row[4].value

        # Save as entries
        NewEntry = {}
        NewEntry[Headers[1]] = LearnerNumber
        NewEntry[Headers[2]] = ID
        NewEntry[Headers[3]] = str(FirstDay) 
        NewEntry[Headers[4]] = MailAddr
        UserList[LearnerNumber] = NewEntry


# === Save to Json file === #
def SaveJsonFile():
    with open(FileJsonName_User, 'w') as uw:
        json.dump(UserList, uw, indent=2)
    print('\nAll User Informations are saved to Json file %s.' %FileJsonName_User)


# ##### Inquiry User List ##### #
def ShowUserList():
    global UserList
    # Load User Infos from Json file
    with open(FileJsonName_User, 'r') as ur:
        UserList = json.load(ur)
    
    # Show List of User Info
    print('\n===== User Info =====')
    for nums, infos in UserList.items():
        print('\n --- %s ---' %str(nums))
        for keys, values in infos.items():
            print('%s : %s' %(keys, values))


# ##### Load and Add a new user ##### #
def AddNewUser():
    # Load user info from Json file
    with open(FileJsonName_User, 'r') as ur:
        UserList = json.load(ur)
    
    # Show List of User Info
    print('\n=== The followings are users already in the list. ===\n')
    for nums, infos in UserList.items():
        print('%s : %s' %(nums, infos['ID']))
    TotalNumber = int(len(UserList))
    NextNumber = str(TotalNumber + 1)
    print('\nTotal numbers: %s' %str(TotalNumber))

    # Input new user
    AddCheckPoint = input('\nGoing to input User No.%s , enter Y to continue: ' %NextNumber)
    while AddCheckPoint == 'Y':
        # Input info
        LearnerNumber = 'JLR-' + NextNumber
        ID = input('ID: ')
        FirstDay_M = int(input('Month of FirstDay: '))
        FirstDay_D = int(input('Day of FirstDay: '))
        MailAddr = input('MailAddr: ')

        # Save as entries
        NewEntry = {}
        NewEntry['LearnerNumber'] = LearnerNumber
        NewEntry['ID'] = ID
        NewEntry['FirstDay'] = str(datetime(2020, FirstDay_M, FirstDay_D, 0,0,0))
        NewEntry['MailAddr'] = MailAddr
        
        # Save check
        print('\nNew User Info:\n  LearnerNumber: %s\n  ID: %s\n  FirstDay: %s\n  MailAddr: %s' 
                %(NewEntry['LearnerNumber'], NewEntry['ID'], NewEntry['FirstDay'], NewEntry['MailAddr']))
                
        SaveCheckPoint = input("\nPlease check user's information, enter Y to save or R to re-input: ")
        
        # Save to Json
        if SaveCheckPoint == 'Y':
            UserList[LearnerNumber] = NewEntry
            with open(FileJsonName_User, 'w') as uw:
                json.dump(UserList, uw, indent=2)
            print('\n>>> Learner %s: %s is saved to user list. <<<' %(LearnerNumber, ID))
            AddCheckPoint = 'N'
        
        # Input again
        elif SaveCheckPoint == 'R':
            print('\nGoing to input User No.%s again: ' %NextNumber)
            continue

        # Break
        else:
            print('\nMission About!')
            break


# ##### Save to Excel file ##### #
def JsonToExcel():
    CreateUserItems()
    SaveExcelFile()


# Create user items to save
def CreateUserItems():
    global UserList, XlsWriterEntries
    # Load user info from Json file    
    with open(FileJsonName_User, 'r') as ur:
        UserList = json.load(ur)

    # Create list for all user info
    XlsWriterEntries = []                              ### Create new list for all items
    IndexNumber = 1
    for users, details in UserList.items():            ### Get LearnerNumber and details
        XlsUserEntries = []                            ### Create new list for a new user
        XlsUserEntries.append(IndexNumber)
        IndexNumber += 1
        for keys, values in details.items():           ### Get details
            XlsUserEntries.append(values)              ### Append values to UserEntry
        XlsWriterEntries.append(XlsUserEntries)            ### Append User to XlsWriterEntry


# === Save to Excel file === #
def SaveExcelFile():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'JLR'
    headers = ['Index No.', 'LearnerNumber', 'ID', 'FirstDay', 'MailAddr']
    ws.append(headers)
    for i in XlsWriterEntries:
        ws.append(i)
    try:
        wb.save(FileExcelName_User)
        print('\n>>> User informations in Json are all saved to Excel %s. <<<' %FileExcelName_User)
        wb.close()
    except PermissionError:
        print('\nThe Excel file %s is running, please close it and try again.' %FileExcelName_User)


# ##### Load Json file and upload to MongoDB ##### #
# === Upload to MongoDB === #
def UploadToMongoDB(host, colname):
    ConnectToDatabase(host, colname)
    CreateAndPost()


# === Getting conection on database === #
def ConnectToDatabase(HostAddr, CollectionName):
    global client, db, collection, posts
    client = pymongo.MongoClient(HostAddr)

    print('\nMaking a connection with MongoClient ...')
    db = client[DatabaseName]
    print('Getting Database - %s ...' %DatabaseName)
    collection = db[CollectionName]
    print('Getting a Collection - %s ...\n' %CollectionName)


# === Create post contents and then post to database=== #
def CreateAndPost():
    # Create entry for posting
    with open(FileJsonName_User, 'r') as ur:
        UserList = json.load(ur)
    for ln, contents in UserList.items():
        PostEntry = {}
        PostEntry['LearnerNumber'] = ln
        PostEntry['Contents'] = contents
        PostEntry['tags'] = 'JLR'
        PostEntry['date'] = datetime.today()

        # Post to MangoDB
        post_id = collection.insert_one(PostEntry).inserted_id
        print('Posted: %s - %s' %(PostEntry['LearnerNumber'], PostEntry['Contents']))


# ##### Download Users from MongoDB and save to Json ##### #
def FindFromMongoDB(HostAddr, CollectionName):
    # Connect to MongoDB
    client = pymongo.MongoClient(HostAddr)
    print('\nMaking a connection with MongoClient ...')
    db = client[DatabaseName]
    print('Getting Database - %s ...' % DatabaseName)
    collection = db[CollectionName]
    print('Getting a Collection - %s\n' % CollectionName)

    # Download all contents
    AllUsers = collection.find()

    # Save Json contents
    UserList = {}
    for content in AllUsers:
        EntryNum = content['LearnerNumber']
        EntryContent = content['Contents']
        UserList[EntryNum] = EntryContent

    # Save to Json file
    with open(FileJsonName_User, 'w') as jw:
        json.dump(UserList, jw, indent=2)
    print('\n>>> All Users from MongoDB are saved to Json file. %s <<<' %FileJsonName_User)


# ##### Functions ##### #
#ExcelToJson()
#ShowUserList()
#AddNewUser()
#JsonToExcel()
#UploadToMongoDB()
