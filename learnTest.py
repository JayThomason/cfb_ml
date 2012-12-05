from sklearn.linear_model import SGDClassifier
from sklearn import svm, preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import GradientBoostingClassifier
from DataExtractor import DataExtractor

trainExtractor = DataExtractor(5)
trainData = trainExtractor.featureDictionary
for i in range(6,10):
  trainData.update(DataExtractor(i).featureDictionary)

trainInput = list()
trainOutput = list()

for value in trainData.values():
  inputData = value[0]
  trainInput.append(inputData[0].values() + inputData[1].values())
  trainOutput.append(1 if value[1] == 1 else 0)

#clf = SGDClassifier(loss="log", penalty="elasticnet")
#clf = SGDClassifier(loss="hinge")
clf = svm.SVC()
#clf = GradientBoostingClassifier(n_estimators=30, max_depth=3, subsample=.7)
#clf = KNeighborsClassifier(n_neighbors=3)
scaledTrainInput = preprocessing.scale(trainInput)
clf.fit(trainInput, trainOutput)


testExtractor = DataExtractor(10)
testData = testExtractor.featureDictionary
for i in range(11,13):
  testData.update(DataExtractor(i).featureDictionary)
predictions = list()
outcome = list()

for value in testData.values():
  inputData = value[0]
  predictions.append(clf.predict(inputData[0].values() + inputData[1].values())[0])
  outcome.append(1 if value[1] == 1 else 0)

results = [1 if predictions[i] == outcome[i] else 0 for i in xrange(len(predictions))]

mean = float(sum(results)) / len(results)

print mean
