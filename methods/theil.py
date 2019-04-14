import numpy as np
from scipy import stats

x = np.linspace(0,500,num=1000)
y = np.linspace(0,500,num=1000)

def fit(x,y,confidence):
    return stats.theilslopes(y, x, confidence)

m = fit(x,y,0.9)
print(m)