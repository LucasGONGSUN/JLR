import json


# Settings
FileJsonName = 'Contents_fromInput.json'


# === Load Json file from "FileJsonName" === #
def LoadJsonFile():
    global ContentList
    with open(FileJsonName, 'r') as file_obj_r:
        ContentList = json.load(file_obj_r)


# === Main Menu === #
def MainMenu():
    # Show Main Menu
    MenuRefresh = True
    while MenuRefresh:
        print('''
    ====== Welcome to Japanese Learning Reminder ======
            
            1. Inquire Learning Contents
            2. Input A New Entry
            3. Continue Unfinished Entry
            4. Correct Values
            5. Send Daily Schedule
            6. Save The Last Updates
            7. Quit
            
    ''')

        # Choose a function
        FunctionChoice = input('Please Enter the NUMBER of a function: ')

        # Inquire Contents
        if FunctionChoice == '1':
            from Contents_Inquiry import ShowLCNList
            ShowLCNList(ContentList)

        # Enter a New Entry
        elif FunctionChoice == '2':
            from Contents_NewEntry import ContentCheckN
            ContentCheckN(ContentList)

        # Continue to input unfinished entry
        elif FunctionChoice == '3':
            from Contents_Continue import ContentCheckC
            ContentCheckC(ContentList)

        # Correct Values
        elif FunctionChoice == '4':
            from Contents_Correct import SearchValue
            SearchValue(ContentList)

        # Send Reminders
        elif FunctionChoice == '5':
            from SendReminder import DrawAndSend
            DrawAndSend()

        # Save updated ContentList to Json file
        elif FunctionChoice == '6':
            SaveJsonFile()

        # Quit Main Menu
        elif FunctionChoice == '7':
            MenuRefresh = False


# === Save as Json file === #
def SaveJsonFile():
    with open(FileJsonName, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w)
    print('\n>>> All updates are saved. Mission Completed! <<<')


# === Run main program === #
def Main():
    LoadJsonFile()
    MainMenu()


Main()
