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
            
            1. Load and Inquire Learning Contents
            2. Edit Entries
            3. Send Daily Schedule
            4. Save, Export or Import
            5. Quit
            
    ''')

        # Choose a function
        FunctionChoice = input('Please Enter the NUMBER of a function: ')

        # Inquire Contents
        if FunctionChoice == '1':
            LoadJsonFile()
            from Contents_Inquiry import ShowLCNList
            ShowLCNList(ContentList)

        # Edit Entries
        elif FunctionChoice == '2':
            print('''
    ====== Please Choose A Method ======
    
        1. Input A New Entry
        2. Continue Unfinished Entry
        3. Correct Values    
        
        ''')
            MethodChoice_Edit = input('Please Enter the NUMBER of a method: ')

            # Input a New Entry
            if MethodChoice_Edit == '1':
                from Contents_NewEntry import ContentCheckN
                ContentCheckN(ContentList)

            # Continue to input unfinished entry
            elif MethodChoice_Edit == '2':
                from Contents_Continue import ContentCheckC
                ContentCheckC(ContentList)

            # Correct Values
            elif MethodChoice_Edit == '3':
                from Contents_Correct import SearchValue
                SearchValue(ContentList)

        # Send Reminders
        elif FunctionChoice == '3':
            from SendReminder import DrawAndSend
            DrawAndSend()

        # Save updated ContentList to Json file
        elif FunctionChoice == '4':
            print('''
    ====== Please Choose A Method ======
            
        1. Save to Json File
        
        2. Export to Excel File
        3. Import From Excel File
        
        4. Upload to MangoDB
        5. Download From MangoDB
                     
        ''')
            MethodChoice_Convert = input('Please Enter the NUMBER of a method: ')

            # Save to Json
            if MethodChoice_Convert == '1':
                SaveJsonFile()

            # Export to Excel
            elif MethodChoice_Convert == '2':
                from Contents_ExJ import JsonToExcel
                JsonToExcel()

            # Import from Excel
            elif MethodChoice_Convert == '3':
                from Contents_ExJ import ExcelToJson
                ExcelToJson()

            # Upload to MangoDB
            elif MethodChoice_Convert == '4':
                print('To be continued ... ')

            # Download From MangoDB
            elif MethodChoice_Convert == '5':
                print('To be continued ... ')

        # Quit Main Menu
        elif FunctionChoice == '5':
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
