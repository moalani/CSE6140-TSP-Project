import numpy as np
import math

def main():

    # testing Atlanta
    atlCoordinates, atlDisances = getData("Atlanta.tsp")

    print(atlCoordinates)
    print (atlDisances)



def getData(fileName):

    # reading file
    with open(fileName, 'r') as inputFile:
        coordinates = []
        # Skipping the first five lines by reading them. This is because the data starts from the 6th line
        for i in range(6):
            line = inputFile.readline()
        # Reading the remaining file, and reading the coordinates of each city
        while (line != 'EOF\n'):
            # saving the coordinates in a tuple
            coordinates.append((int(float(line.split(' ')[1])), int(float(line.split(' ')[2]))))
            # reading next line
            line = inputFile.readline()
        # defining a zero array to store the distances from one node to another
        distance_map = calculate_distances(coordinates)
    return coordinates, distance_map


def calculate_distances(coordinates):
    distance_map = np.zeros((len(coordinates), len(coordinates)), dtype=int)
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            # taking distance between each node
            distance_map[i, j] = int(round(
                math.sqrt((coordinates[i][0] - coordinates[j][0]) ** 2 + (coordinates[i][1] - coordinates[j][1]) ** 2)))
            distance_map[j, i] = distance_map[i, j]
    return distance_map


if __name__ == '__main__':
    main()
