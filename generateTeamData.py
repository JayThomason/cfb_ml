#
# File: generateTeamData.py
# Author: Jay Thomason
#
# --------------------------------------------------------
#
# This script takes in a season's worth of team game data,
# and builds a dictionary of cumulative statistics out of
# the data. The keys of the dictionary are the team-codes 
# of the teams, and each entry in the dictionary is a list.
# This list consists of one dictionary per game played,
# where this secondary dictionary contains the team's
# cumulative statistics for the season so far.
# The first entry in the list will be the dictionary of
# the team's statistics in the first game, while the second
# entry will be the cumulative statistics for the team's 
# first and second games, and so forth. This dictionary's
# keys are the names of statistics. For example, the key
# "rush yard" returns the team's cumulative rushing yards
# through that game of the season.
# Furthermore, we create a feature stat, which maps game
# codes to average stats, ie. rush yards / game, or 
# scoring defense (points scored by the opposing team / game.


# Constants
offensiveStats = {'scoring offense': 35}
defensiveStats = {'scoring defense': 35}

class DataExtractor:

  teamDictionary = dict()
  gameDictionary = dict()
  featureDictionary = dict()
  gameOrder = list()

  def extractGameData(self, firstTeamData, secondTeamData):
    '''
    Extracts the relevant data from a single game. The data is
    returned as a list, where the key is the stat name,
    e.g. processedGameData['rush att'] will return the number of 
    rushing attempts by the team in that game.
    '''
    global offensiveStats, defensiveStats
    gameDataDict = dict()
    for key,value in offensiveStats.items():
      gameDataDict[key] = int(firstTeamData[value])
    for key,value in defensiveStats.items():
      gameDataDict[key] = int(secondTeamData[value])
    return gameDataDict

  def averageStats(self, statDict, numGames):
    averageDict = dict()
    for key,value in statDict.items():
      averageDict[key] = (1.0 * value) / numGames
    return averageDict

  def arrangeData(self, gameCode):
    data = self.featureDictionary[gameCode]
    if len(data) == 3:
      input = (data[1], data[2])
      output = data[0] 
      self.featureDictionary[gameCode] = (input, output)

  def processGame(self, gameCode):
    '''
    Processes the next game of data by appending to the team's list of
    game data an updated dictionary with the latest cumulative stats.
    '''
    for i in range(len(self.gameDictionary[gameCode])):
      firstTeamData = self.gameDictionary[gameCode][i]
      secondTeamData = self.gameDictionary[gameCode][(i + 1) % 2]
      teamCode = firstTeamData[0]
      if teamCode not in self.teamDictionary:
        self.teamDictionary[teamCode] = list()
      oldTeamData = self.teamDictionary[teamCode]
      cumulativeSeasonData = self.extractGameData(firstTeamData, secondTeamData)
      numPrevGames = len(oldTeamData)
      if i == 0:
        self.featureDictionary[gameCode] = list()
        self.featureDictionary[gameCode].append(1 if firstTeamData[35] > secondTeamData[35] else -1)
      if numPrevGames > 0:
        self.featureDictionary[gameCode].append(self.averageStats(oldTeamData[numPrevGames - 1], numPrevGames))
        for key,value in oldTeamData[numPrevGames - 1].items():
          cumulativeSeasonData[key] += oldTeamData[numPrevGames - 1][key]
      oldTeamData.append(cumulativeSeasonData)
    self.arrangeData(gameCode)


  def getOrderedGameList(self):
    file = open('11-data/game.csv')
    orderedGameList = list()
    for line in file:
      gameData = line.split(',')
      gameCode = gameData[0]
      if gameCode[0] == '"':
        continue
      orderedGameList.append(gameCode)
    file.close()
    return orderedGameList

  def __init__(self):
    file = open('11-data/team-game-statistics.csv', 'r')
    for line in file:
      gameData = line.split(',')
      teamCode, gameCode = gameData[0], gameData[1]
      if teamCode[0] == '"':
        continue
      if gameCode in self.gameDictionary:
        if int(teamCode) == int(gameCode[:4]):
          self.gameDictionary[gameCode].insert(0, gameData)
        else:
          self.gameDictionary[gameCode].append(gameData)
      else:
        self.gameDictionary[gameCode] = list()
        self.gameDictionary[gameCode].append(gameData)
        self.gameOrder.append(gameCode)
    for gameCode in self.getOrderedGameList():
      self.processGame(gameCode)
    file.close()

dataExtractor = DataExtractor()
featureDictionary =  dataExtractor.featureDictionary
for key, value in featureDictionary.items():
  print value
