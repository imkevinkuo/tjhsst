import numpy as np
import random
notin = np.array([[0], [1]])
notout = np.array([1 - num for num in notin])
gatein = np.array([[0,0,1], [0,1,1], [1,0,1], [1,1,1]]) #bias on third argument
andout = np.array([[0], [0], [0], [1]])
orout = np.array([[0], [1], [1], [1]])
xorout= np.array([[0], [1], [1], [0]])
def sigmoid(x):
    return 1/(1+np.exp(-x))
def dsigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))

# example - 6 nodes: 3 input, 2 hidden, 1 output
# nNet: Structure and weights
# ex: [{3:w0, 4:w1}, {3:w2, 4:w3}, {3:w4, 4:w5}, {5:w6}, {5:w7}, {}]
# nNet[i] = dict of nodes that node 'i' feeds into
# nNet[i][j] = weight of link from node 'i' to node 'j'

# nValues : values of function w/previous weighted values
# e.g: [0, 0, 1, ?, ?, final ?]

# Pass input values, get output
def calc(nNet, nValues, inputs):
    nFeeders = [[] for i in range(len(nNet))]
    for i in range(len(nNet)):
        if i < len(inputs):
            nValues[i] = inputs[i]
        else:
            nValues[i] = sigmoid(sum(nFeeders[i]))
        for j in nNet[i]:
            nFeeders[j].append(nValues[i]*nNet[i][j])
    return nValues
def trainNN(inSet, outSet, internalLayers):    
    # Set up structure
    nNet = []
    layers = [len(inSet[0])] + internalLayers + [1,0]
    print(layers)
    cNodes = 0
    for l in range(len(layers)-1):
        cNodes += layers[l] # cumulative nodes
        for i in range(layers[l]):
            nNet.append({(j+cNodes):(random.random()*2 - 1) for j in range(layers[l+1])})
    
    # Print out
    printNN(nNet, inSet)
    error = calcError(nNet, inSet, outSet)
    print(error)
        
    # Start stepping
    step = 0.01
    count = 0
    while error > 0.0001:
        count+=1
        if count%100 == 0:
            printNN(nNet, inSet)
            print(error)
        for n in range(len(nNet)):
            neuron = nNet[n]
            for nextNode in neuron:
                # test stepping direction
                neuron[nextNode] += step
                testError = calcError(nNet, inSet, outSet)
                if testError > error:
                    neuron[nextNode] -= step*2
                # new error should be lower unless we are at a local min
                error = testError
                #print(error)
    # Done training
    printNN(nNet, inSet)
def printNN(nNet, inSet):
    print("----------------------------")
    for n in range(len(nNet)):
        print(n, nNet[n])
    print()
    currentValues = [calc(nNet, [-1 for n in nNet], inSet[i]) for i in range(len(inSet))]
    for i in range(len(currentValues)):
        print(i, ["%.2f" % v for v in currentValues[i]])        
def calcError(nNet, inSet, outSet):
    currentValues = [calc(nNet, [-1 for n in nNet], inSet[i]) for i in range(len(inSet))]
    return sum([abs(outSet[i] - currentValues[i][-1]) for i in range(len(outSet))])

internalLayers = [2,2,2]
trainNN(gatein, xorout, internalLayers)
