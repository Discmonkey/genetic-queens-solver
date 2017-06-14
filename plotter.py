import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

style.use('ggplot')
df = pd.DataFrame.from_csv('log.txt')
df.plot()
plt.title('Mutation Percentage versus Iterations to Solve')
plt.show()