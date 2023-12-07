from indexer import searchCustomQuery, getGameNamesByGenrePerspective, getGameByMode
from unittest.mock import patch
from io import StringIO
import unittest
import sys

class Tester(unittest.TestCase):
    def test_customQuery(self):
        with patch("sys.stdout", newCallable=StringIO) as mockStdout:
            result = searchCustomQuery("ReleasePlatform:Intellivision", -1)
            output = mockStdout.getvalue()

        expectedOutput = "Games matching query - ReleasePlatform:Intellivision:\n\tAstrosmash\n\tTropical Trouble\n\tAuto Racing\n\tBuzz Bombers\n\tShark! Shark!\n\tSea Battle\n\tLas Vegas Poker &amp; Blackjack\n\tMasters of the Universe: The Power of He-Man\n\tAdvanced Dungeons &amp; Dragons Cartridge\n\tUtopia\n\tMajor League Baseball\n\tThin Ice\n\tTriple Action\n\tNASL Soccer\n\tSewer Sam\n\tLas Vegas Roulette\n\tSpace Spartans\n\tABPA Backgammon\n\tHorse Racing\n\tArmor Battle\n\tBeamrider\n\tReversi\n\tB-17 Bomber\n\tSnafu\n\tWorm Whomper\n\tThe Dreadnaught Factor\n\tSpace Armada\n\tThe Electric Company Word Fun\n"
        self.assertEqual(result, expectedOutput)

    def test_gameByGenre(self):
        with patch("sys.stdout", newCallable=StringIO) as mockStdout:
            result = getGameNamesByGenrePerspective("Role-playing (RPG)", "Side view")
            output = mockStdout.getvalue()

        expectedOutput = "Games with Role-playing (RPG) genre and Side view perspective:\n\tX-Men II: The Fall of the Mutants\n\tHabitat\n\tPaper Mario\n\tYs III: Wanderers from Ys\n\tSpellForce: The Order of Dawn\n\tShadow Hearts: Covenant\n\tFable\n\tShin Megami Tensei: Digital Devil Saga\n\tPaper Mario: The Thousand-Year Door\n\tToontown Online\n\tThe Matrix Online\n\tGuardian War\n\tDungeon Lords\n\tJade Empire\n\tGuild Wars\n\tFable: The Lost Chapters\n\tFinal Fantasy XII\n\tKingdom Hearts II\n\tGuild Wars: Factions\n\tDark and Light\n\tAge of Pirates: Caribbean Tales\n\tDungeons &amp; Dragons Online: Stormreach\n\tMonster Hunter: Freedom\n\tJade Empire: Special Edition\n\tFinal Fantasy X\n\tSacrifice\n\tArchLord\n\tThe Witcher\n\tMass Effect\n\tRichard Garriott&#39;s Tabula Rasa\n\tFinal Fantasy X\n\tO.D.T.: Escape... or Die Trying\n\tWarriors of Might and Magic\n\tPhantasy Star IV\n\tKingdom Hearts\n\tPanzer Dragoon Saga\n\tPhantasy Star II\n\tGothic II\n\tSuikoden III\n\tDark Cloud 2\n\tStar Wars: Galaxies - An Empire Divided\n\tPirates of the Caribbean\n"
        self.assertEqual(result, expectedOutput)

    def test_gameByMode(self):
        with patch("sys.stdout", newCallable=StringIO) as mockStdout:
            result = getGameByMode("Multiplayer")
            output = mockStdout.getvalue()

        expectedOutput = "Games with matching game mode:\n\tSavage: The Battle for Newerth\n\tUltima Online\n\tAuto Assault\n\tSteel Battalion: Line of Contact\n\tTime of Defiance\n\tStarsiege: Tribes\n\tAshen Empires\n\tArchLord\n\tThandor: The Invasion\n\tBuster Bros.\n\tMotor City Online\n\tThe Sims Online\n\tShadowbane\n\tRuneScape\n\tCadillacs and Dinosaurs: The Second Cataclysm\n\tSea Battle\n\tRobot Rascals\n\tPac-Man Vs.\n\tTriple Action\n\tNASL Soccer\n\tCity of Heroes\n\tEntropia Universe\n\tTribes: Aerial Assault\n\tCounter-Strike: Source\n\tEverQuest II\n\tJoint Operations: Typhoon Rising\n\tThe Matrix Online\n\tTeam Fortress Classic\n\tLegend of the Red Dragon\n\tMyst Online: Uru Live\n\tEverQuest\n\tVanguard: Saga of Heroes\n\tRF Online\n\tHalf-Life 2: Deathmatch\n\tGuild Wars: Eye of the North\n\tMeridian 59\n\tAnarchy Online\n\tDark Age of Camelot\n\tJumpgate: The Reconstruction Initiative\n\tGlobal Conquest\n\tArmor Battle\n\tWolfenstein: Enemy Territory\n\tStarPeace\n\tLords of Conquest\n"
        self.assertEqual(result, expectedOutput)


if __name__ == '__main__':
    unittest.main()