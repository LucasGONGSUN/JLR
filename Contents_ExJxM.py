import json, openpyxl, pymongo
from math import ceil
from datetime import datetime


# Settings
FileExcelName = 'JLR_Contents.xlsx'
FileJsonName = 'JLR_Contents.json'

KanzisNum = 15

#HostAddr = 'mongodb://localhost:27017'
DatabaseName = 'JLR_Alpha_June'
#CollectionName = 'JLR_Local'


# ##### Load Json file and save to Excel file ##### #
# === Load Json file from FileJsonName === #
def LoadJsonFile():
    global ContentList
    with open(FileJsonName, 'r') as jr:
        ContentList = json.load(jr)


# === Create list of items === #
def CreateListItems(ContentList):
    global XlsListEntries

    # Create list for all kanzis and details
    XlsListEntries = []                                 ### Create new list for all items
    for nums, dicts in ContentList.items():             ### Get list number
        for kanzis, details in dicts.items():           ### Get kanzis and details
            XlsKanziEntries = []                        ### Create new list for a new kanzi
            XlsKanziEntries.append(nums)                ### Append List No. to KanziEntry
            for keys, values in details.items():        ### Get values
                XlsKanziEntries.append(values)          ### Append values to KanziEntry
            XlsListEntries.append(XlsKanziEntries)      ### Append KanziEntry to XlsEntry


# === Save to Excel file === #
def SaveExcelFile():
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'JLContents'
    headers = ['List No.', '漢字', '訓読', '訓読例', '音読み', '音読み例']
    ws.append(headers)
    for i in XlsListEntries:
        ws.append(i)
    try:
        wb.save(FileExcelName)
        print('\n>>> Contents in Json are all saved to Excel %s. <<<' %FileExcelName)
        wb.close()
    except PermissionError:
        print('\nThe Excel file %s is running, please close it and try again.' %FileExcelName)


# ##### Load Excel file and save to Json file ##### #
# === Load Excel file from FileJsonN
def LoadExcelFile():
    global ws, rows, cols
    wb = openpyxl.load_workbook(FileExcelName)
    ws = wb['JLContents']
    rows = ws.max_row
    cols = ws.max_column


# === Create Json contents === #
def CreateJsonContent():
    global ContentList
    Headers = []
    EntryList = {}
    ContentList = {}

    # Load Headers
    for row in ws.iter_rows(max_row=1, max_col=cols):
        for cell in row:
            Headers.append(cell.value)

    # Load details of Kanzi
    for row in ws.iter_rows(min_row=1, max_row=rows, max_col=cols):
        kanzi = row[1].value
        kundoku = row[2].value
        kundokurei = row[3].value
        onyomi = row[4].value
        onyomirei = row[5].value

        # Save as entries
        NewEntry = {}
        NewEntry[Headers[1]] = kanzi
        NewEntry[Headers[2]] = kundoku
        NewEntry[Headers[3]] = kundokurei
        NewEntry[Headers[4]] = onyomi
        NewEntry[Headers[5]] = onyomirei
        EntryList[kanzi] = NewEntry

    # Convert dict contents to a list of key-value pairs
    KanziItems = list(EntryList.items())

    # Group entries by number of KanziNum
    for i in range(ceil(len(KanziItems)/KanzisNum)):
        EntryListNum = 'No.' + str(i+1)
        GroupEntryList = {}
        for x in range(i*KanzisNum+1, (i+1)*KanzisNum+1):
            try:
                GroupEntryList[KanziItems[x][0]] = KanziItems[x][1]
            except IndexError:
                break
        ContentList[EntryListNum] = GroupEntryList


# === Save Json file to FileJsonName === #
def SaveJsonFile():
    global ContentList
    with open(FileJsonName, 'w') as jw:
        json.dump(ContentList, jw, indent=2)
    print('\n>>> Excel contents are saved to Json file %s. <<<' %FileJsonName)


# ##### Load Json file and upload to MongoDB ##### #
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
    for nums, values in ContentList.items():
        for kanzi, contents in values.items():
            PostEntry = {}
            try:
                id = 'Kanzi' + str(ord(kanzi))
                PostEntry['_id'] = id
            except TypeError:
                print('Kanzi is null!')
                continue
            PostEntry['Kanzi'] = kanzi
            PostEntry['Contents'] = contents
            PostEntry['tags'] = nums
            PostEntry['date'] = datetime.today()

            # Post to MangoDB
            collection.insert_one(PostEntry)
            print('Posted: %s - %s' %(PostEntry['Kanzi'], PostEntry['Contents']))


# ##### Download contents from MongoDB and save to Json ##### #
def FindFromMongoDB(HostAddr, CollectionName):
    # Connect to MongoDB
    client = pymongo.MongoClient(HostAddr)
    print('\nMaking a connection with MongoClient ...')
    db = client[DatabaseName]
    print('Getting Database - %s ...' % DatabaseName)
    collection = db[CollectionName]
    print('Getting a Collection - %s\n' % CollectionName)

    # Download all contents
    AllContents = collection.find()

    # Save to Json contents
    ContentList = {}
    for content in AllContents:
        EntryNum = content['tags']
        EntryKanzi = content['Kanzi']
        EntryContent = content['Contents']
        if EntryNum not in ContentList.keys():
            ContentList[EntryNum] = {}
        ContentList[EntryNum][EntryKanzi] = EntryContent

    # Save to Json file
    with open(FileJsonName, 'w') as jw:
        json.dump(ContentList, jw, indent=2)
    print('\n>>> All Data from MongoDB are saved to Json file. %s <<<' %FileJsonName)


# ##### Functions ##### #
def JsonToExcel():
    LoadJsonFile()
    CreateListItems(ContentList)
    SaveExcelFile()


def ExcelToJson():
    LoadExcelFile()
    CreateJsonContent()
    SaveJsonFile()


def PostToMongoDB(host, colname):
    LoadJsonFile()
    ConnectToDatabase(host, colname)
    CreateAndPost()
    print('\n>>> All Json contents are uploaded to MangoDB')


#JsonToExcel()
#ExcelToJson()
#PostToMongoDB()
#FindFromMongoDB()