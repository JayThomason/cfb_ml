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
NUM_PREV_GAMES = 0 

class DataExtractor:

  def getFactors(self):
    '''
    Decides which factors and statistics are going to be used based
    on the content of the offensive and defensive factor files.
    The offensiveStats and defensiveStats dictionaries map the
    names of statistics to their location in the game data.
    ''' 
    offensiveFile, defensiveFile = open('offensiveFactors'), open('defensiveFactors')
    index = 2
    offensiveFactors, defensiveFactors = dict(), dict()
    for oline,dline in zip(offensiveFile, defensiveFile):
      ofactor, dfactor = oline.split(','), dline.split(',')
      if int(ofactor[1]) == 1:
        self.offensiveStats[ofactor[0]] = index
      if int(dfactor[1]) == 1:
        self.defensiveStats[dfactor[0]] = index
      index += 1
    offensiveFile.close()
    defensiveFile.close()
    
  def extractGameData(self, firstTeamData, secondTeamData):
    '''
    Extracts the relevant data from a single game. The data is
    returned as a list, where the key is the stat name,
    e.g. processedGameData['rush att'] will return the number of 
    rushing attempts by the team in that game.
    '''
    gameDataDict = dict()
    for key,value in self.offensiveStats.items():
      gameDataDict[key + '-off'] = float(firstTeamData[value])
    for key,value in self.defensiveStats.items():
      gameDataDict[key + '-def'] = float(secondTeamData[value])
    if firstTeamData[35] > secondTeamData[35]:
      gameDataDict['wins-off'] = 1
    else:
      gameDataDict['wins-off'] = 0 
    return gameDataDict

  def averageStats(self, statDict, numGames):
    '''
    Creates a dictionary of average statistics given a dictionary
    of aggregate statistics and the number of games played.
    '''
    averageDict = dict()
    for key,value in statDict.items():
      averageDict[key] = (1.0 * value) / numGames
    return averageDict

  def arrangeData(self, gameCode):
    '''
    Orders data correctly in the featureDictionary. Given a game code,
    it is ensured that if the data is malformed, it is ignored,
    otherwise, it is put in the form of a pair of input, output, where
    the input is a pair of dictionaries of average statistics (for
    the two playing teams) and the output is +1 if the first team won
    and -1 if the first team lost. The dat is considered malformed if
    there are only stats of for one team, in which case it is likely
    that one of the teams has not played any prior games in the season.
    '''
    data = self.featureDictionary[gameCode]
    if len(data) == 3:
      input = (data[1], data[2])
      output = data[0] 
      self.featureDictionary[gameCode] = (input, output)
    else:
      self.featureDictionary.pop(gameCode)

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
      if numPrevGames > NUM_PREV_GAMES:
        self.featureDictionary[gameCode].append(self.averageStats(oldTeamData[numPrevGames - 1], numPrevGames))
        for key,value in oldTeamData[numPrevGames - 1].items():
          cumulativeSeasonData[key] += oldTeamData[numPrevGames - 1][key]
      oldTeamData.append(cumulativeSeasonData)
    self.arrangeData(gameCode)


  def getOrderedGameList(self, directory):
    '''
    Returns a list of games as they happen in chronological
    order. The directory is the name of the directory which
    holds the season data for which the ordered game list
    is desired. 
    '''
    file = open(directory + '/game.csv', 'r')
    orderedGameList = list()
    for line in file:
      gameData = line.split(',')
      gameCode = gameData[0]
      if gameCode[0] == '"':
        continue
      orderedGameList.append(gameCode)
    file.close()
    return orderedGameList

  def __init__(self, year):
    '''
    Initializes the DataExtractor class. Constructs and fills the teamDictionary,
    gameDictionary, and featureDictionary.
    '''
    self.teamDictionary = dict()
    self.gameDictionary = dict()
    self.featureDictionary = dict()
    self.gameOrder = list()
    self.offensiveStats = dict()
    self.defensiveStats = dict()
    self.getFactors()
    directory = str(year) + '-data'
    file = open(directory + '/team-game-statistics.csv', 'r')
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
    for gameCode in self.getOrderedGameList(directory):
      self.processGame(gameCode)
    file.close()



if __name__ == '__main__':
  dataExtractor = DataExtractor(12)
  featureDictionary =  dataExtractor.featureDictionary
  print len(featureDictionary.keys())
