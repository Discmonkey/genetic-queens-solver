import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')
df = pd.DataFrame.from_csv('log.txt')
df.plot()
plt.show()