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

    results = searcher.doc(s.scoreDocs[0].doc)
    print("Game description: \n", results.get("Description"))
    print("Game Trivia: \n", results.get("Trivia"))


# Query 2: Get game names with matching genre and perspective
def getGameNamesByGenrePerspective(genre, perspective):
    searcher = IndexSearcher(DirectoryReader.open(dir))
    query1 = QueryParser("Genre", analyzer).parse(f"{genre}")
    query2 = QueryParser("Perspective", analyzer).parse(f"{perspective}")

    boolQuery = BooleanQuery.Builder()
    boolQuery.add(query1, BooleanClause.Occur.MUST)
    boolQuery.add(query2, BooleanClause.Occur.MUST)

    results = searcher.search(boolQuery.build(), Integer.MAX_VALUE)

    print(f"Games with {genre} genre and {perspective} perspective:")
    for game in results.scoreDocs:
        doc = searcher.doc(game.doc)
        print("\t", doc.get("Name"))


# Query 3: Get all games made by a developer
def getGameByDeveloper(developer):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("Developer", analyzer).parse(f"{developer}")

    results = searcher.search(query, Integer.MAX_VALUE)

    print(f"Games released by {developer}:")
    for game in results.scoreDocs:
        doc = searcher.doc(game.doc)
        print(f"\t{doc.get('Name')}")
        print(f"\t\tMobyScore - {doc.get('MobyScore')}")
        print(f"\t\tCriticScore - {doc.get('CriticsScore')}")

# Query 4: Get all games with matching game mode
def getGameByMode(mode):
    searcher = IndexSearcher(DirectoryReader.open(dir))

    query = QueryParser("GameMode", analyzer).parse(f"{mode}")

    results = searcher.search(query, Integer.MAX_VALUE)

    print(f"Games with matching game mode:")
    for game in results.scoreDocs:
        doc = searcher.doc(game.doc)
        print(f"\t{doc.get('Name')}")

# getDescTrivia("The X-Files Game (1998)")
# getGameNamesByGenrePerspective("Action", "1st-person")
# getGameByDeveloper("Psygnosis Limited")
getGameByMode("Multiplayer")
