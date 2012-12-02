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
statNamesAndIndexes = {'pass yard': 7}

file = open('11-data/team-game-statistics.csv', 'r')

teamDictionary = dict()

def extractGameData(gameData):
  '''
  Extracts the relevant data from a single game. The data is
  returned as a list, where the key is the stat name,
  e.g. processedGameData['rush att'] will return the number of 
  rushing attempts by the team in that game.
  '''
  global statNamesAndIndexes
  gameDataDict = dict()
  for key,value in statNamesAndIndexes.items():
    gameDataDict[key] = int(gameData[value])
  return gameDataDict


def processNextGame(teamDictionary, teamCode, gameData):
  '''Processes the next game of data by appending to the team's list of
    game data an updated dictionary with the latest cumulative stats.'''
  teamData = teamDictionary[teamCode]
  cumulativeSeasonData = extractGameData(gameData) 
  numPrevGames = len(teamData)
  if numPrevGames > 0:
    for key,value in teamData[numPrevGames - 1].items():
      cumulativeSeasonData[key] += teamData[numPrevGames - 1][key]
  teamData.append(cumulativeSeasonData)



# Main Script
for line in file:
  gameData = line.split(',')
  teamCode = gameData[0]
  if teamCode[0] == '"':
    continue
  if teamCode in teamDictionary:
    processNextGame(teamDictionary, teamCode, gameData)
#    cumulData = teamDictionary[teamCode][len(teamDictionary[teamCode]) - 1]
#    print type(cumulData)
  else:
    teamDictionary[teamCode] = []
    processNextGame(teamDictionary, teamCode, gameData)
#    print type(teamDictionary[teamCode][0])

#####
#### for testing sorting by passing yards
#####
from collections import OrderedDict

def extractPassYardsFromDict(cumulativeList):
  cumulativeList = cumulativeList[1]
#  print cumulativeList[1]
#  print type(cumulativeList[len(cumulativeList) - 1])
#  print type(cumulativeList[len(cumulativeList) - 1])
  return cumulativeList[len(cumulativeList) - 1]['pass yard']

#print teamDictionary['288']
orderedDict = OrderedDict(sorted(teamDictionary.items(), key=extractPassYardsFromDict, reverse=True))

print orderedDict.keys()

file.close()

