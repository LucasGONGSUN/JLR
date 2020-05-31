import openpyxl
import json

# Settings
WB = openpyxl.load_workbook('Calendar.xlsx')
WS = WB['Jap']
DateList = []
NoteList = []
Checklist = {}


# === Create a learning list, save as a dict === #
def Createlist():
    # Read date from calendar
    for row in WS.iter_rows(min_row=1, max_row=185, max_col=1):
        for cell in row:
            DateList.append(cell.value)

    # Read notelist from calendar
    for row in WS.iter_rows(min_row=1, max_row=185, min_col=2, max_col=8):
        new_row = []
        for cell in row:
            new_row.append(cell.value)
        NoteList.append(new_row)

    # Combine date and notelist
    for i in range(185):
        Checklist[str(DateList[i])] = NoteList[i]


# === Save dict as json files === #
def Dict2Json():
    FileJsonName = 'Calendar.json'
    with open(FileJsonName, 'w') as file_obj:
        json.dump(Checklist, file_obj)

Createlist()
Dict2Json()
print('Mission Completed!')
