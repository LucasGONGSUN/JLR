import json

#Settings
FileJsonName = 'Contents_fromInput.json'
#EntryList_example = {
#    'No.1':{'本': {'漢字': '本', '訓読': 'もと', '訓読例': '本（もと）', '音読': 'ホン', '音読例': '日本（にほん）'}}}

# === Load old ContentList from Json === #
def LoadJsonFile():
    global ContentList, FileJsonName
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)
    print('\n>>> Mission Start! <<<\n')

# === Load numbers and then check if existed
def ContentCheck():
    global EntryNum, ContentCheckPoint
    #Get numbers
    LCNumberList = []
    print("There're <Learning Contents No.> already in the list as follows: ")
    for nums, values in ContentList.items():
        print(nums, end=' ')
        LCNumberList.append(nums)

    #Input new number and then CHECK
    ContentCheckPoint = 'Y'
    while ContentCheckPoint == 'Y':
        EntryNum = 'No.' + input('\n\nPlease input the number of NEW EntryList: ')
        if EntryNum in LCNumberList:
            print('Warning: This Entry Number is already in the list!')
            continue
        else:
            InputNewEntry()

# === Create new EntryList === #
def InputNewEntry():
    global EntryList, ContentCheckPoint
    EntryList = {}
    StartCheckPoint = input('Going to input EntryList %s, enter Y to continue: ' % EntryNum)
    if StartCheckPoint == 'Y':
        for i in range(1, 16):
            print(' >>> Now is inputting word No.%s <<< ' %i)
            #Input detailed contents
            kanzi = input('漢字：')
            kundoku = input('訓読：')
            kundokurei = input('訓読例：')
            onyomi = input('音読み：')
            onyomirei = input('音読み例：')

            #Save as entries
            NewEntry = {}
            NewEntry['漢字'] = kanzi
            NewEntry['訓読'] = kundoku
            NewEntry['訓読例'] = kundokurei
            NewEntry['音読み'] = onyomi
            NewEntry['音読み例'] = onyomirei
            EntryList[kanzi] = NewEntry

            #Check
            for keys, values in EntryList.items():
                print(keys + ': ' + str(values))
            ContinueCheckPoint = input('Above is word No.%s , enter ｙ to continue: ' %i)
            if ContinueCheckPoint == 'ｙ':
                continue
            else:
                print('>>> Mission Abort. See you next time. <<<')
                break
        ContentCheckPoint = 'N'
    else:
        print('>>> Mission Quit. See you next time. <<<')
        ContentCheckPoint = 'N'

# === Combine EntryNum and EntryList and Save as Json file === #
def CombineJsonSave():
    with open(FileJsonName, 'w') as file_obj_w:
        ContentList[EntryNum] = EntryList
        json.dump(ContentList, file_obj_w)
    print('\n>>> List %s is saved. Mission Completed! <<<' %EntryNum)

def Job():
    LoadJsonFile()
    ContentCheck()
    CombineJsonSave()

Job()
