import numpy as np
from sklearn.linear_model import LinearRegression

x = np.linspace(0,500,num=1000)
y = np.linspace(0,500,num=1000)

def fit(X,y,order):
    data_complete = []
    for i in range((order+1)):
        data_complete.append(X**i)
    data_complete = np.array(data_complete).T
    model = LinearRegression().fit(data_complete,y)
    return model

m = fit(x,y,1)
print(m.coef_)

