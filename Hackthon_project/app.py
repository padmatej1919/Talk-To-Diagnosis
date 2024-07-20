import pandas as pd
import json

csv_file = './DatasetForTreatment.csv'
df = pd.read_csv(csv_file)

df.to_json('data.json', orient='records')
with open('data.json', 'r') as f:
    data = json.load(f)

print(data)
