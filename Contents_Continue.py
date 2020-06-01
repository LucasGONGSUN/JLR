import json


# Settings
#EntryList_example = {
#    'No.1':{'本': {'漢字': '本', '訓読': 'もと', '訓読例': '本（もと）', '音読': 'ホン', '音読例': '日本（にほん）'}}}
FileJsonName = 'JLR_Contents.json'


# === Load old ContentList from Json === #
def LoadJsonFile():
    global ContentList, FileJsonName
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)
    print('\n>>> Mission Start! <<<\n')


# === Load numbers and then check if existed === #
def ContentCheckC(ContentList):
    global EntryNum, ContentCheckPoint

    #Get numbers
    LCNumberList = []
    print("\nThe following <Learning Contents No.> are already in the list: ")
    for nums, values in ContentList.items():
        print(nums, end=' ')
        LCNumberList.append(nums)

    #Input a number and then CHECK
    ContentCheckPoint = 'Y'
    while ContentCheckPoint == 'Y':
        EntryNum = 'No.' + input('\n\nPlease input the number of list you want to CONTINUE: ')
        if EntryNum not in LCNumberList:
            print('Warning: This List Number is not in the list!')
            continue
        else:
            ContinueEntry(ContentList)


# === Continue Unfinished EntryList === #
def ContinueEntry(ContentList):
    global EntryList, ContentCheckPoint

    # Get and print list contents
    EntryList = ContentList[EntryNum]
    print('\nHere are the contents of List %s :\n' %EntryNum)
    for keys, values in EntryList.items():
        print(keys + ': ' + str(values))

    # Continue to input
    StartCheckPoint = input('\nGoing to CONTINUE EntryList %s, enter N to abort: ' % EntryNum)
    if StartCheckPoint == 'N':
        print('\n>>> Mission Quit. See you next time. <<<')
        ContentCheckPoint = 'N'
    else:
        for i in range(len(ContentList[EntryNum])+1, 16):
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
            ContinueCheckPoint = input('Above is word No.%s , enter N to abort: ' %i)
            if ContinueCheckPoint == 'N':
                print('\n>>> Mission Abort. See you next time. <<<')
                break
            else:
                continue

        # Combine EntryNum and EntryList, add to ContentList
        ContentList[EntryNum] = EntryList
        ContentCheckPoint = 'N'


# === Save as Json file === #
def SaveJsonFile():
    with open(FileJsonName, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w, indent=2)
    print('\n>>> List %s is saved. Mission Completed! <<<' %EntryNum)


def Job():
    LoadJsonFile()
    ContentCheckC(ContentList)
    SaveJsonFile()


#Job()
