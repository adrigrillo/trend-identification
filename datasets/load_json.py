import json
import numpy as np
with open('C:\\Users\\Jessica\\Documents\\Master\\PDSDMY2\\datasets\\out\\gold_monthly_json_out.txt') as json_file:  
    data = json.load(json_file)
trend = np.array(data['data'])
print(trend)