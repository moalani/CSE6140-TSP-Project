import numpy as np
import math
import time
import sys


bestSolution = sys.maxsize / 2
startingTime = time.time()
maxTime = 0


def BnB(distances, timeout):

    # modifying the maxtime global variable
    global maxTime
    maxTime = timeout
    for i in range(distances.shape[0]):
        distances[i, i] = sys.maxsize / 2
    # calling for the lower bound
    lowerBound = findLowerBound(distances)
    # defining the travelling path of the salesperson as an array

    destinationNodeX = [i for i in range(distances.shape[0])]
    destinationNodeY = [i for i in range(distances.shape[0])]
    tour = {}
    # calling the BnB main algorithm
    recursiveSearch(distances, lowerBound, tour, destinationNodeX, destinationNodeY)


def recursiveSearch(distances, lowerBound, tour, nodeListX, nodeListY):


    global bestSolution
    global startingTime
    global maxTime

    if (time.time() - startingTime > maxTime):
        return

    if (lowerBound >= bestSolution):
        return
    # print(lowerBound)
    # find new best quality
    if (distances.shape[0] <= 1):
        bestSolution = lowerBound

        print(bestSolution)
        return

    minDistance = np.argmin(distances)
    xIndex = minDistance / distances.shape[0]
    yIndex = minDistance % distances.shape[0]
    minValue = np.amin(distances)
    updatedTour = tour.copy()
    updatedTour[nodeListX[int(xIndex)]] = nodeListY[int(yIndex)]

    cycleFlag = isCycle(updatedTour, nodeListX[int(xIndex)])

    if cycleFlag == False :  # no MST cycle is False:
        updatedDistances = distances.copy()
        updatedDistances = np.delete(updatedDistances, int(xIndex), axis=0)
        updatedDistances = np.delete(updatedDistances, int(yIndex), axis=1)
        minDistance = findLowerBound(updatedDistances)
        updatedLowerBound = lowerBound + minValue + minDistance
        newNodeListX = nodeListX[:]
        del newNodeListX[int(xIndex)]
        newNodeListY = nodeListY[:]
        del newNodeListY[yIndex]
        recursiveSearch(updatedDistances, updatedLowerBound, updatedTour, newNodeListX, newNodeListY)

    distances[int(xIndex), int(yIndex)] = sys.maxsize / 2

    minDistance = min(distances[int(xIndex), :])

    if minDistance != 0:
        lowerBound += minDistance
        distances[int(xIndex), :] -= np.ones(distances.shape[0], dtype=int) * minDistance

    temp = min(distances[:, int(yIndex)])

    if temp != 0:
        lowerBound += minDistance
        distances[:, int(yIndex)] -= np.ones(distances.shape[0], dtype=int) * minDistance
    recursiveSearch(distances, lowerBound, tour, nodeListX, nodeListY)


def findLowerBound(distances):
    lowestCost = 0

    for i in range(distances.shape[0]):

        nextLowestCost = min(distances[i, :])
        if nextLowestCost != 0:
            lowestCost += nextLowestCost
            distances[i, :] -= np.ones(distances.shape[0], dtype=int) * nextLowestCost

    for i in range(distances.shape[0]):

        nextLowestCost = min(distances[:, i])
        if nextLowestCost != 0:
            lowestCost += nextLowestCost
            distances[:, i] -= np.ones(distances.shape[0], dtype=int) * nextLowestCost

    return lowestCost

# function to determine if there is cycle in graph

def isCycle(tour, location):
    temp = location
    while temp != None:
        temp = tour.get(temp)
        if temp == location:
            return True
    return False
