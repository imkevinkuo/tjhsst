import numpy as np
import random
import ast
import sys
notin = [0,1]
notout = [1,0]
gatein = [[0,0,1], [0,1,1], [1,0,1], [1,1,1]] #bias on third argument
andout = [0,0,0,1]
orout  = [0,1,1,1]
xorout = [0,1,1,0]
##
def sigmoid(x):
    return 1/(1+np.exp(-x))
def dsigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))
def tanh(x):
    return np.tanh(x)
# forward pass for a single input set
def layerProd(outputs, weights):
    return [sum(outputs[j]*weights[j][i] for j in range(len(outputs))) for i in range(len(weights[0]))]
def forward(inputs, weights):
    depth = len(weights)
    net = [[] for n in range(depth)] # net[0] is for 2nd layer, net[-1] is final output
    sig = [[i for i in inputs]] # "output" of 1st layer is the set's input value
    dsig = [[]] # we dont take sigmoid or dsigmoid of 1st layer
    for l in range(depth): # l for layer
        net[l] = layerProd(sig[l], weights[l])
        if l < depth - 1:
            sig.append([sigmoid(n) for n in net[l]])
            dsig.append([n*(1-n) for n in sig[l+1]])
    return net, sig, dsig
# derivatives man
def backward(weights, net, sig, dsig, target):
    depth = len(weights)
    # calculate differential of w/resp to a neuron
    # multiply by differential of neuron w/resp to parent weight
    # multiply by differential of error w/resp to final output
    #
    # get differential of error w/resp to specific weight
    dNeurons = [[] for n in range(depth)]
    for l in range(depth-1, 0, -1): # L for layer
        for n in range(len(dsig[l])): # N for node
            # calculate dx:final/dx:n
            if l == depth-1:
                dNeurons[l].append(dsig[l][n]*weights[l][n][0])
            else:
                total = 0
                for k in range(len(weights[l][n])):
                    total += dNeurons[l+1][k]*weights[l][n][k]
                dNeurons[l].append(total*dsig[l][n])
    dWeights = [[] for n in range(depth)]
    for l in range(depth):
        for n in range(len(weights[l])):
            dWeights[l].append([])
            for k in range(len(weights[l][n])):
                if l == depth-1:
                    dWeights[l][n].append(sig[l][n]*(net[-1][0]-target))
                else:
                    dWeights[l][n].append(sig[l][n]*dNeurons[l+1][k]*(net[-1][0]-target))
    return dWeights
def trainNN(inSet, outSet, internalLayers):    
    # Set up structure
    layers = [len(inSet[0])] + internalLayers + [1]
    print(layers)
    weights = [[[(random.random()*2 - 1) for w in range(layers[l+1])]
                for n in range(layers[l])]
               for l in range(len(layers)-1)] + [[[1]]]
    printNN(weights, inSet)


    epoch = 0
    lastError = 0
    lastWeightDiffs = []
    momentum = 0.3
    learningRate = 0.5
    while (epoch < 5000):
        epoch += 1
        
        storeWeights = []
        totalError = 0
        
        for i in range(len(inSet)):
            net, sig, dsig = forward(inSet[i], weights)
            totalError += 0.5*(outSet[i] - net[-1][0])**2
            dWeights = backward(weights, net, sig, dsig, outSet[i])
            storeWeights.append(dWeights)
            
        print(epoch, totalError)

        
        weightDiffs = [[[sum([storeWeights[i][layer][node][weight] for i in range(len(inSet))])
                       for weight in range(len(weights[layer][node]))]
                      for node in range(len(weights[layer]))]
                     for layer in range(len(weights))]
        for layer in range(len(weights)):
            for node in range(len(weights[layer])):
                for weight in range(len(weights[layer][node])):
                    mm = 0
                    if (epoch > 1):
                        mm = momentum*lastWeightDiffs[layer][node][weight]
                    delta = learningRate*weightDiffs[layer][node][weight] + mm
                    weights[layer][node][weight] -= delta
                    
        lastError = totalError
        lastWeightDiffs = weightDiffs
def printNN(weights, inSet=None):
    print("----------------------------")
    for n in range(len(weights)):
        print(n, weights[n])
    if inSet is not None:
        print()
        
inSet, outSet = gatein, xorout
internalLayers = [3]
trainNN(inSet, outSet, internalLayers)
