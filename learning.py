import util, random, math
from math import exp, log
from util import Counter

############################################################
# Feature extractors: a feature extractor should take a raw input x (tuple of
# tokens) and add features to the featureVector (Counter) provided.

def footballFeatureExtractor(x):
  team1, team2 = x
  featureVector = util.Counter()

  for stat, val in team1.items():
    featureVector[stat + '1'] = val
  
  for stat, val in team2.items():
    featureVector[stat + '2'] = val

  return featureVector

"""
The logistic loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 3)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the logistic loss.
"""
def logisticLoss(featureVector, y, weights):
  return math.log(1 + math.exp(-(weights*featureVector)*y))

"""
The gradient of the logistic loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the logistic loss, with respect to w,
        the weights we are learning.
"""
def logisticLossGradient(featureVector, y, weights):
  dot = weights*featureVector
  exp = math.exp(dot*y)
  return featureVector*(-y/(1+exp))

"""
The hinge loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the hinge loss.
"""
def hingeLoss(featureVector, y, weights):
  margin = (weights*featureVector)*y
  return max(1-margin, 0)

"""
The gradient of the hinge loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the hinge loss, with respect to w,
        the weights we are learning.
        You should not worry about the case when the hinge loss is exactly 1
"""
def hingeLossGradient(featureVector, y, weights):
  margin = (weights*featureVector)*y
  if margin > 1: 
    return util.Counter()
  else:
    return featureVector*(-y)

"""
The squared loss, for a given weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The scalar value of the squared loss.
"""
def squaredLoss(featureVector, y, weights):
  return 0.5*((weights*featureVector - y)**2)
"""
The gradient of the squared loss with respect to the weight vector.
@param featureVector: The featurized representation of a training example
@param y: The true value of the example (in our case, +/- 1)
@param weights: The weight vector assigning a weight to every feature
@return The gradient [vector] of the squared loss, with respect to w,
        the weights we are learning.
"""
def squaredLossGradient(featureVector, y, weights):
  scalar = weights*featureVector - y
  return featureVector*scalar

class StochasticGradientLearner():
  def __init__(self, featureExtractor):
    self.featureExtractor = util.memoizeById(featureExtractor)

  """
  This function takes a list of training examples and performs stochastic 
  gradient descent to learn weights.
  @param trainExamples: list of training examples (you should only use this to
                        update weights).
                        Each element of this list is a list whose first element
                        is the input, and the second element, and the second
                        element is the true label of the training example.
  @param validationExamples: list of validation examples (just to see how well
                             you're generalizing)
  @param loss: function that takes (x, y, weights) and returns a number
               representing the loss.
  @param lossGradient: function that takes (x, y, weights) and returns the
                       gradient vector as a counter.
                       Recall that this is a function of the featureVector,
                       the true label, and the current weights.
  @param options: various parameters of the algorithm
     * initStepSize: the initial step size
     * stepSizeReduction: the t-th update should have step size:
                          initStepSize / t^stepSizeReduction
     * numRounds: make this many passes over your training data
     * regularization: the 'lambda' term in L2 regularization
  @return No return value, but you should set self.weights to be a counter with
          the new weights, after learning has finished.
  """
  def learn(self, trainExamples, validationExamples, loss, lossGradient, options):
    self.weights = util.Counter()
    random.seed(42)
    initStepSize = options.initStepSize
    stepSizeReduction = options.stepSizeReduction
    regularization = options.regularization

    # You should go over the training data numRounds times.
    # Each round, go through all the examples in some random order and update
    # the weights with respect to the gradient.
    for round in range(0, options.numRounds):
      random.shuffle(trainExamples)
      numUpdates = 0  # Should be incremented with each example and determines the step size.

      # Loop over the training examples and update the weights based on loss and regularization.
      # If your code runs slowly, try to explicitly write out the dot products
      # in the code here (e.g., "for key,value in counter: counter[key] += ---"
      # rather than "counter * other_vector")
      for x, y in trainExamples:
        numUpdates += 1
        stepSize = initStepSize/(numUpdates**stepSizeReduction)
        lossTerm = lossGradient(self.featureExtractor(x), y, self.weights)*stepSize
        if regularization != 0:
          regTerm = self.weights*(regularization/len(trainExamples))
          self.weights = self.weights - lossTerm - regTerm
        else:
          self.weights = self.weights - lossTerm
      # Compute the objective function.
      # Here, we have split the objective function into two components:
      # the training loss, and the regularization penalty.
      # The objective function is the sum of these two values
      trainLoss = 0  # Training loss
      regularizationPenalty = 0  # L2 Regularization penalty
      for x, y in trainExamples:
        trainLoss += loss(self.featureExtractor(x), y, self.weights)
      regularizationPenalty += 0.5*(self.weights*self.weights)
      self.objective = trainLoss + regularizationPenalty

      # See how well we're doing on our actual goal (error rate).
      trainError = util.getClassificationErrorRate(trainExamples, self.predict, 'train', options.verbose, self.featureExtractor, self.weights)
      validationError = util.getClassificationErrorRate(validationExamples, self.predict, 'validation', options.verbose, self.featureExtractor, self.weights)

      print "Round %s/%s: objective = %.2f = %.2f + %.2f, train error = %.4f, validation error = %.4f" % (round+1, options.numRounds, self.objective, trainLoss, regularizationPenalty, trainError, validationError)

    # Print out feature weights
    out = open('weights', 'w')
    for f, v in sorted(self.weights.items(), key=lambda x: -x[1]):
      print >>out, f + "\t" + str(v)
    out.close()

  """
  Classify a new input into either +1 or -1 based on the current weights
  (self.weights). Note that this function should be agnostic to the loss
  you are using for training.
  You may find the following fields useful:
    self.weights: Your current weights
    self.featureExtractor(): A function which takes a datum as input and
                             returns a featurized version of the datum.
  @param x An input example, not yet featurized.
  @return +1 or -1
  """
  def predict(self, x):
    if self.weights*self.featureExtractor(x) > 0:
      return 1
    else:
      return -1

def setTunedOptions(options):
  options.featureExtractor = 'custom'
  options.loss = 'logistic'
  options.initStepSize = 2
  options.stepSizeReduction = 0.3
  options.regularization = 0
  options.numRounds = 10
