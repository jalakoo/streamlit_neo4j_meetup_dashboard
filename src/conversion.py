import csv

dict_from_csv = {}

# For converting a csv file to a python dictionary to include as constants
with open('src/programming_languages.csv', mode='r') as inp:
    reader = csv.reader(inp)
    dict_from_csv = {rows[0]:rows[1] for rows in reader}

print(dict_from_csv)