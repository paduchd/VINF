import csv
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import expr

# Create a spark session and read wiki dump data
spark = SparkSession.builder.appName("wiki").config("spark.jars.packages", "com.databricks:spark-xml_2.12:0.15.0").getOrCreate()
data = spark.read.format('xml').options(rowTag='page', charset='UTF-8').load("Wiki/enwiki-latest-pages-articles10.xml-p4045403p5399366")

# List of all crawled games
gameNames = []

# Function to get all game names from csv
def getGameNames():
    with open('parsedData.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)
        for row in reader:
            gameNames.append(row[0])

getGameNames()

# Search wiki for pages which's title contains the game name
def getGameInformation(dataRow):
    title = str(dataRow["title"])
    title = re.sub(r'[\\/<>?,*"|:\']', '', title)
    page = str(dataRow["_VALUE"])

    # Find the game mode with regex
    gameModes = re.search(r"modes\s*?=\s*?\[\[([^\]]+)\]\]", page, flags=re.I | re.M | re.S)

    # Write the extracted game mode into a file with corresponding name
    fileName = "WikiData/" + title + ".txt"
    if(gameModes != None):
        with open(fileName, "w", encoding='utf-8') as file:
            file.write("Game: " + str(dataRow["title"]) + "\n")
            file.write("Mode: " + gameModes.groups()[0])


# Filter only relevant pages from the wiki dump (Title must contain the name of the game) and call getGameInformation() on each
game_name_literals = [lit(name) for name in gameNames]
condition = col("title").isin(*game_name_literals)

relevantData = data.withColumn("containsGame", condition)
relevantData = relevantData.filter(col("containsGame") == "True")
relevantData = relevantData.select("title", "revision.text._VALUE")
relevantData.foreach(getGameInformation)
