
import pandas as pd
import json
#
# df = pd.DataFrame([range(10,20),range(30,40)])
# print(df.transpose().head())
# data = json.loads(df.transpose().to_json())
#
# print(list(data.values()))

data = {1:2,3:4}

data.pop(1,None)
print(data)