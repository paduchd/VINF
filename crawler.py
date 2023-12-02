import requests
import re

# Base url for the MobyGames website
baseUrl = 'https://www.mobygames.com'

# Downloads html file from url
def downloadHtml(url):
    return requests.get(url)


# Checks if game url exists
def checkIfExists(html):
    title = re.search('<title>\n?\s*(.+)\s*\n?</title>', html.text, flags = re.I | re.M)
    if(title.groups(0)[0] == 'Game not found - MobyGames'):
        return False
    else:
        return True


# Checks if game has a trivia page
def checkForTrivia(html):
    if(re.search('<a class=\"nav-link disabled\" href=\"/game/\d+/.+/trivia/\">\n?Trivia\n?</a>', html.text, flags= re.I | re.M)):
        return False
    else:
        return True


# Gets trivia link from gamePage html
def getTriviaLink(html):
    triviaLink = re.search('<a class=\"nav-link\" href=\"(/game/\d+/.+/trivia/)\">Trivia</a>', html.text, flags = re.I | re.M)
    return triviaLink.groups(0)[0]


# Saves html into specified directory
def saveHtml(html, id):
    name = re.search('<title>\n?\s*(.+)\s*\n?</title>', html.text, flags= re.I | re.M)
    name = re.sub(r'[\\/<>?,*"|:\']', '', name.groups(0)[0])
    f = open(f'RawData/({id}) {name}.html', "w", encoding = "utf-8")
    f.write(html.text)
    f.close()
    print(f'Downloaded: ({id}) {name}')


# Runs the crawler process
def runCrawler():
    counter = 0
    id = 0
    while(counter < 7645):
        gamePage = downloadHtml(f'{baseUrl}/game/{id}')
        print(f"Checking id: {id}")
        # Checking if game with current id exists
        if(checkIfExists(gamePage) == False):
            id += 1
            continue
        # Checking if the game has trivia
        elif(checkForTrivia(gamePage) == False):
            id += 1
            continue
        else:
            triviaLink = getTriviaLink(gamePage)
            triviaPage = downloadHtml(f'{baseUrl}{triviaLink}')
            saveHtml(gamePage, id)
            saveHtml(triviaPage, id)
            id += 1
            counter += 1

runCrawler()