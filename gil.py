import numpy as np
from random import uniform
import matplotlib.pyplot as plt

def propensity(react, rates):
    prop = [0,0,0,0,0,0,0,0]
    #hardcoded because reasons
    prop[0] = rates[0]*react[0]*react[4]
    prop[1] = rates[1]*react[3]
    prop[2] = rates[2]*react[0]
    prop[3] = rates[3]*react[1]
    prop[4] = rates[4]*react[2]*(react[2]-1)/2
    prop[5] = rates[5]*react[4]
    prop[6] = rates[6]*react[1]
    prop[7] = rates[7]*react[2]

    return prop


def gilStep(matrix, react, prop, t):
    propSum = sum(prop)
    otherSum = 0

    tau = -np.log(uniform(0,1))/propSum
    x2 = uniform(0,1)
    nextReact = 0

    #too lazy to do it properly lmao
    while(True):
        if nextReact == len(prop)-1 or (otherSum + prop[nextReact]) > x2*propSum:
            break
        else:
            nextReact += 1
    newReact = np.add(react, matrix[nextReact])
    newReact = np.array([n if n > 0 else 0 for n in newReact])
    newTime = t+tau

    return([newReact, newTime])


def gillespie(maxTime):
    #reaction rows, reactant columns, [G, R, P, DG, D]
    speciesMat = np.array([[-1, 0, 0, 1, -1],
                            [1, 0, 0, -1, 1],
                            [0, 1, 0, 0, 0],
                            [0, 0, 1, 0, 0],
                            [0, 0, -2, 0, 1],
                            [0, 0, 2, 0, -1],
                            [0, -1, 0, 0, 0],
                            [0, 0, -1, 0, 0]])


    react = np.array([10, 0, 0, 0, 0])
    rates = [1, 10, 0.01, 10, 1, 1, 0.1, 0.01]
    prop = []
    t = 0
    times = [t]
    reactsOverTime = [react]
    while(t < maxTime):
        print(react)
        prop = propensity(react, rates)
        nextStep = gilStep(speciesMat, react, prop, t)

        reactsOverTime.append(nextStep[0])
        times.append(nextStep[1])
        react = nextStep[0]
        t = nextStep[1]
    reactsOverTime = np.array(reactsOverTime).transpose()
    return([times, reactsOverTime])


poopoohead =  gillespie(500)

plt.plot(poopoohead[0], poopoohead[1][2])
plt.show()
