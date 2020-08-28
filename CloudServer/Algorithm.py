import numpy as np
import pandas as pd
import networkx as nx
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def swapPositions(string_list, pos1, pos2):
    string_list[pos1], string_list[pos2] = string_list[pos2], string_list[pos1]
    return string_list


class Algorithm:

    def __init__(self, movements, piled_objects, Start):
        self.movements = movements
        self.piled_objects = piled_objects
        self.Start = Start
        self.path = [self.Start]

    def closest_node(self, node, visited_nodes):
        # Variables
        distance = 10000000
        closest_node = []

        for i in self.movements:
            if i[2] < distance and node == i[0] and i[1] not in visited_nodes:
                closest_node = i[1]
                distance = i[2]

        return closest_node

    def shortest_path(self):
        # Variables
        visited_nodes = []
        i = 0

        df = pd.DataFrame(self.movements)
        nodes = df[0].unique().tolist()

        while len(self.path) < len(nodes):
            visited_nodes.append(self.path[i])
            self.path.append(self.closest_node(self.path[i], visited_nodes))
            # visited_nodes[i].replace('ApproxPoint_', '')
            i += 1
        # self.path.append('Home')

        for n, i in enumerate(self.path):
            if "ApproxPoint_" in i:
                self.path[n] = self.path[n].replace('ApproxPoint_', '')

        return self.path

    def collision_avoidance_shortest_path(self):

        for i in range(0, len(self.path) - 1):
            for element in self.piled_objects:
                if (self.path[i] in element) and (self.path[i + 1] in element):
                    if self.path[i] != element[0]:
                        swapPositions(self.path, i, i + 1)
        self.path.remove('Home')
        return self.path
