import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import pywt
import json

csv = pd.read_csv('C:\\Users\\Jessica\\Documents\\Master\\PDSDMY2\\datasets\\data_csv.txt',sep='\t',decimal=',')
print(csv.head())
print(csv.shape)
csv = csv.values
signal = csv[:,6]
wavelet='db8'
len_times_series = signal.shape[0]
max_level = pywt.dwt_max_level(len_times_series, wavelet)
for _ in range(max_level):
    signal, _ = pywt.dwt(signal, wavelet)
ret = signal
for _ in range(max_level):
    ret = pywt.idwt(ret,None,wavelet)
plt.plot(range(0,len(csv[:,6])),csv[:,6])
plt.plot(range(0,len(ret)),ret)
plt.show()

# save_dict = {}
# save_dict['orig'] = csv[:,6].tolist()
# save_dict['data'] = ret.tolist()
# save_dict['type'] = 'polyish-increasing'

# with open('C:\\Users\\Jessica\\Documents\\Master\\PDSDMY2\\datasets\\out\\data_index.json', 'w') as outfile:  
#     json.dump(save_dict, outfile)

