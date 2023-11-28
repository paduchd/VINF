import csv
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
    narrative = re.search('<dt>Narrative</dt>.+?<a href=.+?>(.+?)</a>', g, flags= re.I | re.M | re.S)
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


    if(narrative == None):
        narative = 'Not listed'
    else:
        narative = narrative.groups()[0].strip()


    if(credits.groups()[0].strip() == "Contribute"):
        credits = 'Not listed'
    else:
        credits = credits.groups()[0].strip()


    w.writerow([name.groups()[0].strip(), release.groups()[0].strip()[-4:], release.groups()[1].strip(), credits, developer, mobyScore, criticsScore, genre, perspective, setting, narative, description, trivia.rstrip()])

def main(files):
    with open('parsedData.csv','w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'ReleaseYear', 'ReleasePlatform', 'Credits', 'Developer', 'MobyScore', 'CriticsScore', 'Genre', 'Perspective', 'Setting', 'Narrative', 'Description', 'Trivia'])
        for i in range(0, len(files), 2):
            game = open(f'RawData/{files[i]}', 'r', encoding = "utf-8").read()
            trivia = open(f'RawData/{files[i+1]}', 'r', encoding = "utf-8").read()
            extractInformation(game, trivia, writer)
            i += 2


main(files)