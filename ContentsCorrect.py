import json

#Settings
FileJsonName = 'Contents_fromInput.json'

# === Load old ContentList from Json === #
def LoadJsonFile():
    global ContentList, FileJsonName
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)
    print('\n>>> Mission Start! <<<\n')

# === Input Keys and Find Value === #
def SearchValue():
    global ModifyTo
    #Find Value
    OriginValue = ContentList['No.6']['丙']['訓読例'] ### Input Manually
    print("The ENTRY you want to correct is %s:" %ContentList['No.6']['丙']) ### Input Manually
    print("The VALUE you want to correct is %s:" %OriginValue)
    ModifyCheckPoint = input('Do you want to correct the value? Enter Y to correct: ')
    if ModifyCheckPoint == 'Y':
        ModifyTo = input('Please input the right value: ')
        ModifyToCheck = input("Do you want to change '%s' to '%s' ? Enter Y to DO THAT: " %(OriginValue, ModifyTo))
        if ModifyToCheck == 'Y':
            CorrectValue()
        else:
            print('Mission Abort!')
    else:
        print('Mission Quit!')

# === Correct values === #
def CorrectValue():
    ContentList['No.6']['丙']['訓読例'] = ModifyTo ### Input Manually
    print('The VALUE is corrected to %s.' %ModifyTo)
    print("The ENTRY now is: %s" %ContentList['No.6']['丙']) ### Input Manually
    SaveCheckPoint = input("Enter Y to save the Correction: ")
    if SaveCheckPoint == 'Y':
        CombineJsonSave()
    else:
        print('\n>>> Mission Canceled <<<')

# === Save as Json file === #
def CombineJsonSave():
    with open(FileJsonName, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w)
    print('\n\n>>> Correction is Saved. Mission Completed! <<<')

def Job():
    LoadJsonFile()
    SearchValue()

Job()
