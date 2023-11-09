#import csv
import os
import re

directoryPath = 'C:/Users/dedo4/Desktop/School/Ing/1. Semester/VINF/Python scripts/RawData'

files = []

for path in os.listdir(directoryPath):
    if os.path.isfile(os.path.join(directoryPath, path)):
        files.append(path)

def removeHtmlTags(text):
    tags = re.compile(r'<.*?>')
    return tags.sub('', text)

def extractInformation(g, t, w):
    name = re.search('<title>(.+?) - MobyGames.+?</title>', g, flags= re.I | re.M | re.S)
    release = re.search('<dt>Released</dt>.+?<a href=.+?>\n?(.+?)</a>.+?<a href=.+?>\n?(.+?)</a>', g, flags= re.I | re.M | re.S)
    credits = re.search('<dt>Credits</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    developer = re.search('<dt>Developers</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    mobyScore = re.search('<div class=\"mobyscore\".+?>\n?(.+?)</div>', g, flags= re.I | re.M | re.S)
    criticsScore = re.search('<dt>Critics</dt>.+?(\d+?%)', g, flags= re.I | re.M | re.S)
    genre = re.search('<dt>Genre</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    perspective = re.search('<dt>Perspective</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    setting = re.search('<dt>Setting</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    narative = re.search('<dt>Narative</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
    description = re.search('<div id=\"description-text\".+?>(.+?)</div>', g, flags= re.I | re.M | re.S)
    description = removeHtmlTags(description.groups()[0])

    trivia = re.search('<h2>Trivia</h2>.+?(<h3>.+?)<p>Information also contributed by.+?</p>', t, flags=re.I | re.M | re.S)
    if(trivia == None):
        trivia = re.search('<h2>Trivia</h2>.+?(<h3>.+?)<a href=\"/contribute/.+?>edit trivia</a>', t, flags=re.I | re.M | re.S)
    if (trivia == None):
        trivia = re.search('<h2>Trivia</h2>.+?<div.+?>(.+?)</div>', t, flags=re.I | re.M | re.S)
    trivia = removeHtmlTags(trivia.groups()[0].strip())

    if(developer == None):
        developer = 'Not listed'
    else:
        developer = developer.groups()[0].strip()


    if(mobyScore == None):
        mobyScore = 'Not listed'
    else:
        mobyScore = mobyScore.groups()[0].strip()


    if(criticsScore == None):
        criticsScore = 'Not listed'
    else:
        criticsScore = criticsScore.groups()[0].strip()


    if(genre == None):
        genre = 'Not listed'
    else:
        genre = genre.groups()[0].strip()


    if(perspective == None):
        perspective = 'Not listed'
    else:
        perspective = perspective.groups()[0].strip()


    if(setting == None):
        setting = 'Not listed'
    else:
        setting = setting.groups()[0].strip()


    if(narative == None):
        narative = 'Not listed'
    else:
        narative = narative.groups()[0].strip()

    # print(f'{name.groups()[0].strip()}\n')
    # print(f"Release date: {release.groups()[0].strip()}\n")
    # print(f"Release platform: {release.groups()[1].strip()}\n")
    # print(f"Credited people: {credits.groups()[0].strip()}\n")
    # print(f'Developer: {developer}')
    # print(f'Moby score: {mobyScore}')
    # print(f'Critics score: {criticsScore}')
    # print(f'Genre: {genre}')
    # print(f'Perspective: {perspective}')
    # print(f'Setting: {setting}')
    # print(f'Narative: {narative}')
    # print(f"Description: {description}")
    # print(f"Trivia: {trivia}\n")

    w.writerow([name.groups()[0].strip(), release.groups()[0].strip(), release.groups()[1].strip(), credits.groups()[0].strip(), developer, mobyScore, criticsScore, genre, perspective, setting, narative, description, trivia])

def main(files):
    with open('parsedData.csv','w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Release date', 'Release platform', 'Credited people', 'Developer', 'Moby score', 'Critics score', 'Genre', 'Perspective', 'Setting', 'Narative', 'Description', 'Trivia'])
        for i in range(0, len(files), 2):
            game = open(f'RawData/{files[i]}', 'r', encoding = "utf-8").read()
            trivia = open(f'RawData/{files[i+1]}', 'r', encoding = "utf-8").read()
            extractInformation(game, trivia, writer)
            i += 2


main(files)