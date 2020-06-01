import json

# Settings
FileJsonName = 'JLR_Contents.json'


# === Load Json file from "FileJsonName" === #
def LoadJsonFile():
    global ContentList
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)


# === Show list numbers and contents === #
def ShowLCNList(ContentList):
    # Show list of <Learning Contents No.>
    print("\n=== The followings are all the <Learning Contents No.> ===")
    for nums, dicts in ContentList.items():
        print(nums, end='  ')
    print('\n')

    # Input number of start
    InputCheckPoint_start = True
    while InputCheckPoint_start:
        try:
            ListNumberStart = int(input("Please enter the 'BEGINNING No.' (1-150): "))
            InputCheckPoint_start = False
        except ValueError:
            print('Please input an integrate number.')
            continue


    # Input number of end
    InputCheckPoint_end = True
    while InputCheckPoint_end:
        try:
            ListNumberEnd = int(input("Please enter the 'END No.' (1-150): "))
            InputCheckPoint_end = False
        except ValueError:
            print('Please input an integrate number.')
            continue


    # Print inquired contents
    try:
        for i in range(ListNumberStart, ListNumberEnd+1):
            print('\n\n===== Here are the contents of No.%s =====\n' %str(i))
            for keys, values in ContentList['No.'+str(i)].items():
                print(keys + ': ' + str(values))
    except KeyError:
        print('The List No. is out of range. Please try again.\n')

def Job():
    LoadJsonFile()
    ShowLCNList(ContentList)


#Job()
