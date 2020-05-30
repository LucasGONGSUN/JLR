import json

FileJsonName = 'Contents_fromInput.json'
with open(FileJsonName, 'r') as file_obj_r:
    ContentList = json.load(file_obj_r)

for nums, dicts in ContentList.items():
    print('\n\n' + nums)
    for kanzi, detail in dicts.items():
        print(kanzi)
        print(detail)
