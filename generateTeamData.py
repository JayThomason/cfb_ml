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


# Constants
offensiveStats = {'scoring offense': 35}
defensiveStats = {'scoring defense': 35}

file = open('11-data/team-game-statistics.csv', 'r')

teamDictionary = dict()
gameDictionary = dict()
gameOrder = list()

def extractGameData(firstTeamData, secondTeamData):
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


def processGame(gameCode):
  '''
  Processes the next game of data by appending to the team's list of
  game data an updated dictionary with the latest cumulative stats.
  '''
  global teamDictionary, gameDictionary
  for i in range(len(gameDictionary[gameCode])):
    firstTeamData = gameDictionary[gameCode][i]
    secondTeamData = gameDictionary[gameCode][(i + 1) % 2]
    teamCode = firstTeamData[0]
    if teamCode not in teamDictionary:
      teamDictionary[teamCode] = list()
    oldTeamData = teamDictionary[teamCode]
    cumulativeSeasonData = extractGameData(firstTeamData, secondTeamData)
    numPrevGames = len(oldTeamData)
    if numPrevGames > 0:
      for key,value in oldTeamData[numPrevGames - 1].items():
        cumulativeSeasonData[key] += oldTeamData[numPrevGames - 1][key]
    oldTeamData.append(cumulativeSeasonData)



# Main Script
for line in file:
  gameData = line.split(',')
  teamCode, gameCode = gameData[0], gameData[1]
  if teamCode[0] == '"':
    continue
  if gameCode in gameDictionary:
    gameDictionary[gameCode].append(gameData)
  else:
    gameDictionary[gameCode] = list()
    gameDictionary[gameCode].append(gameData)
    gameOrder.append(gameCode)

for gameCode in gameOrder:
  processGame(gameCode)


# for testing sorting by passing yards
from collections import OrderedDict

def extractSortingStats(cumulativeList):
  cumulativeList = cumulativeList[1]
  return cumulativeList[len(cumulativeList) - 1]['scoring defense']

orderedDict = OrderedDict(sorted(teamDictionary.items(), key=extractSortingStats))

#print teamDictionary['669']
print orderedDict.keys()

file.close()

