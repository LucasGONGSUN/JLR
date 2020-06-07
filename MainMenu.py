import json


# Settings
FileJsonName_content = 'JLR_Contents.json'
FileJsonName_user = 'UserInfo.json'
FileJsonName_date = 'Calendar.json'


# === Load Json file from "FileJsonName" === #
def LoadJsonFile():
    global CheckList, ContentList, UserList

    # Load Calendar from 'Calendar.json'
    try:
        with open(FileJsonName_date, 'r') as dr:
            CheckList = json.load(dr)
    except FileNotFoundError:
        pass

    # Load Contents from 'JLR_Contents.json'
    try:
        with open(FileJsonName_content, 'r') as cr:
            ContentList = json.load(cr)
    except FileNotFoundError:
        pass

    # Load User Info from 'UserInfo.json'
    try:
        with open(FileJsonName_user, 'r') as ur:
            UserList = json.load(ur)
    except FileNotFoundError:
        pass

    return CheckList, ContentList, UserList

# === Main Menu === #
def MainMenu():
    # Show Main Menu
    MenuRefresh = True
    while MenuRefresh:
        print('''
    ====== Welcome to Japanese Learning Reminder ======
            
            1. Save Calendar to Json File
            2. Edit Users
            3. Edit Contents
            
            4. Send Daily Learning Contents
            
            5. Quit
            
    ''')

        # Choose a function
        FunctionChoice = input('Please Enter the NUMBER of a function: ')

        # Save Calendar from Excel to Json
        if FunctionChoice == '1':
            from Calendar_E2J import Save2Json
            Save2Json()

        # Edit Users
        if FunctionChoice  == '2':
            print('''
    ====== Please Choose A Method of Users ======
    
        1. Show List of Users
        2. Add A New User
        
        3. Import User List from Excel to Json
        4. Export User List From Json to Excel
        
        5. Upload User List to MongoDB
        6. Download User List from MongoDB
        
        ''')
            MethodChoice_User = input('Please Enter the NUMBER of a function: ')

            # Show users list
            if MethodChoice_User == '1':
                from Users_ExJxM import ShowUserList
                ShowUserList()

            # Add a new user
            if MethodChoice_User == '2':
                from Users_ExJxM import AddNewUser
                AddNewUser()

            # User List from Excel to Json
            if MethodChoice_User == '3':
                from Users_ExJxM import ExcelToJson
                ExcelToJson()

            # User List from Json to Excel
            if MethodChoice_User == '4':
                from Users_ExJxM import  JsonToExcel
                JsonToExcel()

            # Upload
            if MethodChoice_User == '5':
                from Users_ExJxM import UploadToMongoDB
                host = 'mongodb://localhost:27017'
                #host = "mongodb+srv://lucassl3:lucas112358@alphajune-czcux.azure.mongodb.net/<dbname>" \
                #       "?retryWrites=true&w=majority"
                colname = 'JLR_User'
                UploadToMongoDB(host, colname)

            # Download
            if MethodChoice_User == '6':
                from Users_ExJxM import FindFromMongoDB
                host = 'mongodb://localhost:27017'
                #host = "mongodb+srv://lucassl3:lucas112358@alphajune-czcux.azure.mongodb.net/<dbname>" \
                #       "?retryWrites=true&w=majority"
                colname = 'JLR_User'
                FindFromMongoDB(host, colname)

        # Edit Contents
        elif FunctionChoice == '3':
            print('''
    ====== Please Choose A Method of Contents ======
    
        1. Load and Inquire for Entries
        2. Input A New Entry
        3. Continue An Unfinished Entry
        4. Correct Values
        5. Save All Changes to Json File
        
        6. Import Contents From Excel to Json
        7. Export Contents From Json to Excel
        
        8. Upload Contents to MangoDB
        9. Download Contents From MangoDB
        
        ''')
            MethodChoice_Edit = input('Please Enter the NUMBER of a method: ')

            # Load and inquire Entries
            if MethodChoice_Edit == '1':
                import Contents_Inquiry
                Contents_Inquiry.LoadJsonFile()
                Contents_Inquiry.ShowLCNList(ContentList)

            # Input a New Entry
            elif MethodChoice_Edit == '2':
                from Contents_NewEntry import ContentCheckN
                ContentCheckN(ContentList)

            # Continue to input unfinished entry
            elif MethodChoice_Edit == '3':
                from Contents_Continue import ContentCheckC
                ContentCheckC(ContentList)

            # Correct Values
            elif MethodChoice_Edit == '4':
                from Contents_Correct import SearchValue
                SearchValue(ContentList)

            # Save changes to Json
            elif MethodChoice_Edit == '5':
                SaveJsonFile()

            # Import contents from Excel
            elif MethodChoice_Edit == '6':
                from Contents_ExJxM import ExcelToJson
                ExcelToJson()

            # Export to Excel
            elif MethodChoice_Edit == '7':
                from Contents_ExJxM import JsonToExcel
                JsonToExcel()

            # Upload to MangoDB
            elif MethodChoice_Edit == '8':
                from Contents_ExJxM import PostToMongoDB
                host = 'mongodb://localhost:27017'
                #host = "mongodb+srv://lucassl3:lucas112358@alphajune-czcux.azure.mongodb.net/" \
                #       "<dbname>?retryWrites=true&w=majority"
                colname = 'JLR_Local'
                PostToMongoDB(host, colname)

            # Download From MangoDB
            elif MethodChoice_Edit == '9':
                from Contents_ExJxM import FindFromMongoDB
                host = 'mongodb://localhost:27017'
                #host = "mongodb+srv://lucassl3:lucas112358@alphajune-czcux.azure.mongodb.net/" \
                #       "<dbname>?retryWrites=true&w=majority"
                colname = 'JLR_Local'
                FindFromMongoDB(host, colname)

        # Send Reminders
        elif FunctionChoice == '4':
            from SendReminder import DrawAndSend
            DrawAndSend()

        # Quit Main Menu
        elif FunctionChoice == '5':
            MenuRefresh = False


# === Save as Json file === #
def SaveJsonFile():
    with open(FileJsonName_content, 'w') as file_obj_w:
        json.dump(ContentList, file_obj_w, indent=2)
    print('\n>>> All updates are saved. Mission Completed! <<<')


# === Run main program === #
def Main():
    LoadJsonFile()
    MainMenu()


Main()
