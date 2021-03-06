# JLR
Japanese Learning Reminder


# Version Update Info.

2020.6.6 - alpha.Juen.6
    1. Update: Be able to upload to MongoDB Atlas Online
    
2020.6.5 - alpha.June.5
    1. New function: Import % Export of users info with Excel file
    2. New function: Get date of FirstDay and mail addresses from user info, send contents individually
    3. New function: Upload user and contents list to MongoDB local server
    3. Update: Optimized the structure of main menu in text
    4. Update: Automatically organize contents of learning list according to Number of Kanzi (KanziNum)
     
2020.6.1 - alpha.June.1
    1. New function: Import & Export of contents with Excel file
    2. New function: Convert format between Json and Excel
    3. Combined all functions in a text menu
    4. Optimized file structure and key params
    
2020.5.30 - alpha.530
    1. Update workflow:
        1) Write down learning schedule in Excel, then convert to Json file
        2) Input learning contents in Python program, then convert to Json file
        3) Load daily schedule and contents from Json files
        4) Draw a mail with schedule and contents, then send to receivers

2020.5.29 - alpha.529
    1. Set workflow of alpha version:
        1. Write down learning schedule in Excel
        2. Update learning contents everyday in Excel
        3. Convert both learning schedule and contents into Json files for further processing
        4. Load daily schedule and contents from Json files
        5. Draw a mail and then send to receivers automatically.


# Next Plan
1. Upload data to MangoDB Server


# List of Files
--- Main Body ---
MainMenu.py
SendReminder.py - Create daily learning schedule and contents, then send to receivers
  
--- Calendar ---
Calendar_E2J.py - Convert learning schedule from Excel to Json file

Calendar.xlsx - Origin learning schedule
Calendar.json

--- Contents ---
Contents_Inquiry.py - Inquire learning contents
Contents_NewEntry.py - Input a new list of entries
Contents_Continue.py - Continue to finish an entry
Contents_Correct.py - Correct wrong values
Contents_ExJxM.py - Convert format among Excel, Json and MongoDB 

JLR_Contents.xlsx - Excel file of learning contents
JLR_Contents.json - Json file of learning contents
JLR_Contents - x.json - Backup file with max list number of x

--- Users ---
Users_ExJxM.py - Management of user info, including inquiry, add new one, import and export

UserInfo.json
Users.xlsx

--- documents ---
README.md
JLR_WorkFlowAndFileStructure.xmind


# Longview
  1. input daily learning content, and then save in online database automatically
  2. all process can be operate online
  3. can save and send content individually
  