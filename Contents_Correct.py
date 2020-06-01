import json

# Settings
FileJsonName = 'JLR_Contents.json'

# === Load old ContentList from Json === #
def LoadJsonFile():
    global ContentList, FileJsonName
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)
    print('\n>>> Mission Start! <<<\n')

# === Input Keys and Find Value === #
def SearchValue(ContentList):
    global ModifyTo, ListToModify, KanziToModify, ItemToModify
    # Get List
    ListToModify = 'No.' + input('\nPlease input the list number: ')
    print('\n=== Here are the contents of List %s ===' %ListToModify)
    for keys, values in ContentList[ListToModify].items():
        print(keys + ': ' + str(values))

    # Get Kanzi
    KanziToModify = input('\nPlease input the Kanzi you want to modify: ')
    print('\n=== Here are the items of %s: ===' %KanziToModify)
    for keys, values in ContentList[ListToModify][KanziToModify].items():
        print(keys + ': ' + str(values))

    # Get Value
    ItemToModify = input('\nPlease input the Item you want to modify: ')
    OriginValue = ContentList[ListToModify][KanziToModify][ItemToModify]
    print("\nThe ENTRY you want to correct is %s:" %ContentList[ListToModify][KanziToModify])
    print("The VALUE you want to correct is %s:" %OriginValue)

    # Input Right Value
    ModifyCheckPoint = input('\nDo you want to correct the value? Enter Y to correct: ')
    if ModifyCheckPoint == 'Y':
        ModifyTo = input('Please input the right value: ')
        ModifyToCheck = input("\nDo you want to change '%s' to '%s' ? Enter Y to DO THAT: " %(OriginValue, ModifyTo))
        if ModifyToCheck == 'Y':
            CorrectValue(ContentList)
        else:
            print('\nMission Abort!')
    else:
        print('\nMission Quit!')

# === Correct values === #
def CorrectValue(ContentList):
    ContentList[ListToModify][KanziToModify][ItemToModify] = ModifyTo
    print('\nThe VALUE is corrected to %s.' %ModifyTo)
    print("The ENTRY now is: %s" %ContentList[ListToModify][KanziToModify])
    SaveCheckPoint = input("\nEnter Y to save the Correction: ")
    if SaveCheckPoint == 'Y':
        SaveJsonFile(ContentList)
    else:
        print('\n>>> Mission Canceled <<<')

# === Save as Json file === #
def SaveJsonFile(ContentList):
    with open(FileJsonName, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w, indent=2)
    print('\n\n>>> Correction is Saved. Mission Completed! <<<')

def Job():
    LoadJsonFile()
    SearchValue(ContentList)

#Job()
