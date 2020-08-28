import numpy as np
import pandas as pd

df = []

for i in range(1, 30):
    df.append(pd.DataFrame(np.ones((20000 * i, 1)), columns=['column_1_name']))  # np.random.rand(5000 * i, 1)

for i in range(1, 30):
    df[i-1].to_csv('file' + str(i) + '.csv', index=False, header=False)
