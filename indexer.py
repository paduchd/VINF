import lucene
from java.nio.file import Paths
from java.lang import Integer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, IndexOptions
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.document import Document, Field, TextField, StringField, FieldType, FloatField
from org.apache.lucene.search import IndexSearcher, BooleanQuery, BooleanClause, Sort, SortField
from org.apache.lucene.queryparser.classic import QueryParser
import csv
import os

lucene.initVM()

indexDirectory = r'index'
if not os.path.exists(indexDirectory):
            os.mkdir('index')
indexPath = Paths.get(indexDirectory)
dir = FSDirectory.open(Paths.get(indexDirectory))

analyzer = StandardAnalyzer()
config = IndexWriterConfig(analyzer)
config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
writer = IndexWriter(FSDirectory.open(indexPath), config)


# Create an indexer document with all the important fields
with open('parsedData.csv','r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)
    for lineNum, data in enumerate(reader):
        document = Document()

        # Define field type
        fieldDefinition = FieldType()
        fieldDefinition.setStored(True)
        fieldDefinition.setIndexOptions(IndexOptions.DOCS)
        document.add(Field("Name",  data[0], fieldDefinition))
        document.add(Field("ReleaseYear",  data[1], fieldDefinition))
        document.add(Field("ReleasePlatform",  data[2], fieldDefinition))
        document.add(Field("Credits",  data[3], fieldDefinition))
        document.add(Field("Developer",  data[4], fieldDefinition))
        document.add(Field("MobyScore", data[5], fieldDefinition))
        document.add(Field("CriticsScore",  data[6], fieldDefinition))
        document.add(Field("Genre",  data[7], fieldDefinition))
        document.add(Field("Perspective",  data[8], fieldDefinition))
        document.add(Field("Setting",  data[9], fieldDefinition))
        document.add(Field("Narrative",  data[10], fieldDefinition))
        document.add(Field("Description",  data[11], fieldDefinition))
        document.add(Field("Trivia",  data[12], fieldDefinition))
        document.add(Field("GameMode", data[13], fieldDefinition))
        writer.addDocument(document)

writer.commit()
writer.close()


# Query 1: Get game description and trivia based on the name of the game
def getDescTrivia(inputName):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("Name", analyzer).parse(f"{inputName}")
    s = searcher.search(query, 1)

    if s.scoreDocs:
        results = searcher.doc(s.scoreDocs[0].doc)
        print("Game description: \n", results.get("Description"))
        print("Game Trivia: \n", results.get("Trivia"))
    else:
        print("No game with such name")


# Query 2: Get game names with matching genre and perspective
def getGameNamesByGenrePerspective(genre, perspective):
    searcher = IndexSearcher(DirectoryReader.open(dir))
    query1 = QueryParser("Genre", analyzer).parse(f"{genre}")
    query2 = QueryParser("Perspective", analyzer).parse(f"{perspective}")

    boolQuery = BooleanQuery.Builder()
    boolQuery.add(query1, BooleanClause.Occur.MUST)
    boolQuery.add(query2, BooleanClause.Occur.MUST)

    results = searcher.search(boolQuery.build(), Integer.MAX_VALUE)

    if results.scoreDocs:
        print(f"Games with {genre} genre and {perspective} perspective:")
        for game in results.scoreDocs:
            doc = searcher.doc(game.doc)
            print("\t", doc.get("Name"))
    else:
        return print("No games with matching genre and perspective")


# Query 3: Get all games made by a developer
def getGameByDeveloper(developer):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("Developer", analyzer).parse(f"{developer}")

    results = searcher.search(query, Integer.MAX_VALUE)

    if results.scoreDocs:
        print(f"Games released by {developer}:")
        for game in results.scoreDocs:
            doc = searcher.doc(game.doc)
            print(f"\t{doc.get('Name')}")
            print(f"\t{doc.get('Developer')}")
            print(f"\t\tMobyScore - {doc.get('MobyScore')}")
            print(f"\t\tCriticScore - {doc.get('CriticsScore')}")
    else:
        return print("No games released by this developer.")

# Query 4: Get all games with matching game mode
def getGameByMode(mode):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("GameMode", analyzer).parse(f"{mode}")

    results = searcher.search(query, Integer.MAX_VALUE)

    if results.scoreDocs:
        print(f"Games with matching game mode:")
        for game in results.scoreDocs:
            doc = searcher.doc(game.doc)
            print(f"\t{doc.get('Name')}")
    else:
        return print("No games matching this mode")


# Query 5: Custom query
def searchCustomQuery(customQuery):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("Name", analyzer).parse(f"{customQuery}")

    results = searcher.search(query, Integer.MAX_VALUE)

    if results.scoreDocs:
        print(f"Games matching query - {customQuery}:")
        for game in results.scoreDocs:
            doc = searcher.doc(game.doc)
            print(f"\t{doc.get('Name')}")
    else:
        return print("No matches")

def main():
    print('Please enter the number of the query you would like to perform:\n'
          '\t1. Get game description and trivia by the name of the game\n'
          '\t2. Get game titles matching a genre and perspective\n'
          '\t3. Get game titles and their score by a developer\n'
          '\t4. Get game titles by game mode\n'
          '\t5. Custom query\n'
          '\t6. Exit')
    choice1 = input('Enter your choice: ')

    match choice1:
        case '1':
            print('=========================Game a description and trivia========================')
            game = input('Enter game name: ')
            getDescTrivia(game)
        case '2':
            print('====================Games matching a genre and perspective====================')
            genre = input('Enter a game genre: ')
            perspective = input('Enter a game perspective: ')
            getGameNamesByGenrePerspective(genre, perspective)
        case '3':
            print('=========================Games created by a developer=========================')
            dev = input('Enter a developer name: ')
            getGameByDeveloper(dev)
        case '4':
            print('==========================Games matching a game mode==========================')
            mode = input('Enter a game mode: ')
            getGameByMode(mode)
        case '5':
            print('=================================Custom query=================================')
            print('The custom query should be in this format - ColumnName:Value AND/OR AnotherColumnName:Value...')
            query = input('Enter a custom query: ')
            searchCustomQuery(query)
        case '6':
            print('Exiting application...')
            exit()

    print('==================================Next query==================================')
    print('Do you wih to perform another search?\n0 - No\n1 - Yes\n')
    choice2 = input('Enter your choice: ')

    match choice2:
        case '0':
            exit()
        case '1':
            main()

main()