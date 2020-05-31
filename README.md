# JLR
Japanese Learning Reminder


# Version Update Info.

2020.6.1  - alpha.June.1
    1. Combined all functions in a text menu
    2. optimized file structure and key params
    
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
1. Optimize inputting trouble shoot
2. Export to Excel and Import from Excel


# List of Files
--- Calendar ---
Calendar_E2J.py - convert learning schedule from Excel to Json file

Calendar.xlsx - origin learning schedule
Calendar.json

--- Contents ---
Contents_Inquiry.py - Inquire learning contents
Contents_NewEntry.py - Input a new list of entries
Contents_Continue.py - Continue to finish an entry
Contents_Correct.py - Correct wrong values

Contents_fromInput.json - Json file convert from Inputting in python
Contents_fromInput - x.json - backup file with max list number of x

--- Mail ---
SendReminder.py - create daily list and contents, then send to receivers
  
--- documents ---
README.md
JLR_WorkFlowAndFileStructure.xmind


# Longview
  1. input daily learning content, and then save in online database automatically
  2. all process can be operate online
  3. can save and send content individually
  