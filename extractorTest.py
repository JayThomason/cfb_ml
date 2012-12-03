from DataExtractor import *

data = DataExtractor(11)
data10 = DataExtractor(10)
data9 = DataExtractor(9)
print len(data.featureDictionary.items())
print len(data10.featureDictionary.items())
data.featureDictionary.update(data10.featureDictionary)
print len(data.featureDictionary.items())

