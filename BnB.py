import math
import sys

import numpy as np

bestSolution = sys.maxsize / 2

def main(coordinates, timer, tracer):
    distances = calculate_distances(coordinates)
    return BnB(distances, timer, tracer)

def calculate_distances(coordinates):
    distance_map = np.zeros((len(coordinates), len(coordinates)), dtype=int)
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            # taking distance between each node
            distance_map[i, j] = int(round(
                math.sqrt((coordinates[i][0] - coordinates[j][0]) ** 2 + (coordinates[i][1] - coordinates[j][1]) ** 2)))
            distance_map[j, i] = distance_map[i, j]
    return distance_map

def BnB(distances, timer, tracer):
    # modifying the maxtime global variable

    for i in range(distances.shape[0]):
        distances[i, i] = sys.maxsize / 2
    # calling for the lower bound
    lowerBound = findLowerBound(distances)
    # defining the travelling path of the salesperson as an array

    destinationNodeX = [i for i in range(distances.shape[0])]
    destinationNodeY = [i for i in range(distances.shape[0])]
    tour = {}
    # calling the BnB main algorithm
    recursiveSearch(distances, lowerBound, tour, destinationNodeX, destinationNodeY, timer, tracer)
    return tour

def recursiveSearch(distances, lowerBound, tour, nodeListX, nodeListY, timer, tracer):
    global bestSolution

    if not timer(bestSolution):
        return

    tracer.next_result(bestSolution)

    if lowerBound >= bestSolution:
        return
    # print(lowerBound)
    # find new best quality
    if distances.shape[0] <= 1:
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

    if cycleFlag == False:  # no MST cycle is False:
        updatedDistances = distances.copy()
        updatedDistances = np.delete(updatedDistances, int(xIndex), axis=0)
        updatedDistances = np.delete(updatedDistances, int(yIndex), axis=1)
        minDistance = findLowerBound(updatedDistances)
        updatedLowerBound = lowerBound + minValue + minDistance
        newNodeListX = nodeListX[:]
        del newNodeListX[int(xIndex)]
        newNodeListY = nodeListY[:]
        del newNodeListY[yIndex]
        recursiveSearch(updatedDistances, updatedLowerBound, updatedTour, newNodeListX, newNodeListY, timer, tracer)

    distances[int(xIndex), int(yIndex)] = sys.maxsize / 2

    minDistance = min(distances[int(xIndex), :])

    if minDistance != 0:
        lowerBound += minDistance
        distances[int(xIndex), :] -= np.ones(distances.shape[0], dtype=int) * minDistance

    temp = min(distances[:, int(yIndex)])

    if temp != 0:
        lowerBound += minDistance
        distances[:, int(yIndex)] -= np.ones(distances.shape[0], dtype=int) * minDistance
    recursiveSearch(distances, lowerBound, tour, nodeListX, nodeListY, timer, tracer)


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
