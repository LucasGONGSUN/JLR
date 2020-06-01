import json


# Settings
FileJsonName = 'JLR_Contents.json'


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
            6. Save, Export or Import
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
            print('''
    ====== Please Choose A Method ======
            
        1. Save to Json File
        2. Export to Excel File
        3. Upload to MangoDB
        
        4. Import From Excel File
             
        ''')
            MethodChoice = input('Please Enter the NUMBER of a method: ')

            # Save to Json
            if MethodChoice == '1':
                SaveJsonFile()

            # Export to Excel
            elif MethodChoice == '2':
                from Contents_ExJ import JsonToExcel
                JsonToExcel()

            # Upload to MangoDB
            elif MethodChoice == '3':
                print('To be continued ... ')

            # Import from Excel
            elif MethodChoice == '4':
                from Contents_ExJ import ExcelToJson
                ExcelToJson()

        # Quit Main Menu
        elif FunctionChoice == '7':
            MenuRefresh = False


# === Save as Json file === #
def SaveJsonFile():
    with open(FileJsonName, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w, indent=2)
    print('\n>>> All updates are saved. Mission Completed! <<<')


# === Run main program === #
def Main():
    LoadJsonFile()
    MainMenu()


Main()
