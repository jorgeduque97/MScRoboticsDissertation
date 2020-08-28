import networkx as nx
import numpy as np
import pandas as pd
import random
import copy
import matplotlib.pyplot as plt
import seaborn as sns
import random
import operator
import csv
from Algorithm import Algorithm
from Nodes import Nodes
from mpl_toolkits.mplot3d import Axes3D
from numpy import vectorize


def read_target_points():
    # Variables
    target_points = []

    # Representation of the points' coordinates in a 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    with open('Points.txt', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            target_points.append((row[0], float(row[1]), float(row[2]), float(row[3])))
            ax.scatter(float(row[1]), float(row[2]), float(row[3]), c='r', marker='o')
            ax.text(float(row[1]), float(row[2]), float(row[3]), '%s' % row[0], size=10, zorder=1, color='k')

    ax.set_xlabel('X Coordinates')
    ax.set_ylabel('Y Coordinates')
    ax.set_zlabel('Z Coordinates')
    plt.title("Target points positions | TSP")

    return target_points


def piled_objects_detection(target_points):
    # Variables
    distances = []
    piled_objects = []

    # Selection of the desired points to calculate the distances between them
    points = [s for s in target_points if "AttachPoint_" in s[0]]

    for i in range(0, len(points)):
        for j in range(i, len(points)):
            if i != j:
                distances.append((points[i][0], points[j][0], np.sqrt(
                    (points[i][1] - points[j][1]) ** 2 + (points[i][2] - points[j][2]) ** 2 + (
                            points[i][3] - points[j][3]) ** 2), np.sqrt(
                    (points[i][1] - points[j][1]) ** 2 + (points[i][2] - points[j][2]) ** 2 + (
                            points[i][3] - points[j][3]) ** 2) - abs(points[i][3] - points[j][3]),
                                  (points[i][3] - points[j][3])))

    distances = sorted(distances, key=lambda tup: tup[3])

    for i in range(3):
        if distances[i][4] > 0:
            piled_objects.append((distances[i][0], distances[i][1]))
        else:
            piled_objects.append((distances[i][1], distances[i][0]))

    df = pd.DataFrame(piled_objects)
    df = df.replace('AttachPoint_', '', regex=True)

    piled_objects = [tuple(r) for r in df.to_numpy()]

    return piled_objects


def components_paths_distances(target_points):
    # Variables
    movements = []
    components = ['ConnectingRod1', 'ConnectingRod2', 'ConnectingRod3', 'ConnectingRod4',
                  'ConnectingRod5', 'ConnectingRod6', 'Piston1', 'Piston2', 'Piston3', 'Piston4', 'Piston5',
                  'Piston6']
    i = 1
    j = 0

    while i < 25:
        movements.append((components[j], 2 * np.sqrt((target_points[i][1] - target_points[i + 1][1]) ** 2 + (
                target_points[i][2] - target_points[i + 1][2]) ** 2 + (
                                                             target_points[i][3] - target_points[i + 1][3]) ** 2)))
        i += 2
        j += 1

    return movements


def approximation_points_distances(target_points):
    # Variables
    movements = []
    nodes = []

    # Selection of the approx points to calculate the distances between them
    points = [s for s in target_points if "ApproxPoint_" in s[0]]

    for i in range(0, len(points)):
        for j in range(0, len(points)):
            if i != j:
                movements.append((points[i][0], points[j][0], np.sqrt(
                    (points[i][1] - points[j][1]) ** 2 + (points[i][2] - points[j][2]) ** 2 + (
                            points[i][3] - points[j][3]) ** 2)))
                nodes.append((i, j))
    return movements


def home_approximation_points_distances(target_points):
    # Variables
    movements = []

    # Selection of the desired points to calculate the distances between them
    points = [s for s in target_points if "ApproxPoint_" in s[0]]

    for i in range(0, len(points)):
        movements.append((target_points[0][0], points[i][0], np.sqrt(
            (target_points[0][1] - points[i][1]) ** 2 + (target_points[0][2] - points[i][2]) ** 2 + (
                    target_points[0][3] - points[i][3]) ** 2)))
        movements.append((points[i][0], target_points[0][0], np.sqrt(
            (target_points[0][1] - points[i][1]) ** 2 + (target_points[0][2] - points[i][2]) ** 2 + (
                    target_points[0][3] - points[i][3]) ** 2)))

    return movements


class PathPlanning:
    def __init__(self):
        self.points = read_target_points()
        self.piled_objects = piled_objects_detection(self.points)
        self.components_movements = components_paths_distances(self.points)
        self.approximation_movements = approximation_points_distances(self.points)
        self.home_approximation_movements = home_approximation_points_distances(self.points)
        N = Nodes(self.components_movements, self.approximation_movements, self.home_approximation_movements)
        self.movements = N.data_preparation()

    def path(self):
        A = Algorithm(self.movements, self.piled_objects, 'Home')
        path1 = A.shortest_path()
        collision_avoidance_path = A.collision_avoidance_shortest_path()
        return collision_avoidance_path
