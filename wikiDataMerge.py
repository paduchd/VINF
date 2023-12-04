import csv
import os
import re

dir = 'WikiData/'
dataDict = {}
updatedRows = []

# Create a dictionary containing the game name and mode from the extracted wiki data
def extractWikiData():
    for file in os.listdir(dir):
        path = os.path.join(dir, file)

        with open(path, 'r') as f:
            lines = f.readlines()

            if len(lines) >= 2:
                gameName = re.search('Game:\s(.+)', lines[0].strip(), flags = re.I | re.M)
                gameMode = re.search('Mode:\s(.+)', lines[1].strip(), flags = re.I | re.M)

                print(gameName.groups()[0])
                print("\t" + gameMode.groups()[0])

                dataDict[gameName.groups()[0]] = gameMode.groups()[0]

extractWikiData()

# Add a new column to parsedData.csv containing the newly extracted game mode
with open('parsedData.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)

    header.append('GameMode')

    for row in reader:
        nameInRow = row[0]
        mode = dataDict.get(nameInRow)

        if mode == None:
            row.append("Unknown")
        else:
            row.append(mode)

        updatedRows.append(row)

with open('parsedData.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerows(updatedRows)
