import learning, util, sys, DataExtractor
from learning import StochasticGradientLearner, footballFeatureExtractor, logisticLoss, logisticLossGradient
from DataExtractor import DataExtractor
learner = StochasticGradientLearner(footballFeatureExtractor)

dataExtractor = DataExtractor(11)
data11 = dataExtractor.featureDictionary.values()


from optparse import OptionParser
parser = OptionParser()
def default(str):
  return str + ' [Default: %default]'
parser.add_option('-f', '--featureExtractor', dest='featureExtractor', type='string',
                  help=default('Which feature extractor to use (basic or custom)'), default="basic")
parser.add_option('-l', '--loss', dest='loss', type='string',
                  help=default('Which loss function to use (logistic, hinge, or squared)'), default="logistic")
parser.add_option('-i', '--initStepSize', dest='initStepSize', type='float',
                    help=default('the initial step size'), default=0.05)
parser.add_option('-s', '--stepSizeReduction', dest='stepSizeReduction', type='float',
                    help=default('How much to reduce the step size [0, 1]'), default=1)
parser.add_option('-R', '--numRounds', dest='numRounds', type='int',
                    help=default('Number of passes over the training data'), default=1000)
parser.add_option('-r', '--regularization', dest='regularization', type='float',
                    help=default('The lambda in L2 regularization'), default=0)
#parser.add_option('-d', '--dataset', dest='dataset', type='string',
#help=default('Prefix of dataset to load (files are <prefix>.{train,validation}.csv)'), default='toy')
parser.add_option('-v', '--verbose', dest='verbose', type='int',
                    help=default('Verbosity level'), default=0)

options, extra_args = parser.parse_args(sys.argv[1:])
if len(extra_args) != 0:
  print "Ignoring extra arguments:", extra_args

learner.learn(data11, data11, logisticLoss, logisticLossGradient, options)
