import numpy as np
import pandas as pd


class Nodes:

    def __init__(self, components_movements, approximation_movements, home_approximation_movements):
        self.components_movements = components_movements
        self.approximation_movements = approximation_movements
        self.home_approximation_movements = home_approximation_movements

    def data_preparation(self):
        # Variables
        movements = []

        for i in self.home_approximation_movements:
            movements.append(i)

        for i in self.approximation_movements:
            movements.append(i)

        # Creating a data frame to process the points
        df1 = pd.DataFrame(movements)

        for i in self.components_movements:
            for j in movements:
                if (i[0] in j[0]) and (j[0] != "Home"):
                    df1.iat[movements.index(j), 2] += i[1]

        # np.savetxt(r'D:\Jorge Duque\Documents\MSc Robotics\Dissertation project\Path planning\Movements5.txt',
        #           df1.values, fmt='%s %s %f')

        movements = [tuple(r) for r in df1.to_numpy()]
        return movements
