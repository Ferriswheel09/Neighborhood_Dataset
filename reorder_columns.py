import pandas as pd

df = pd.read_csv('./final_compilation/newer_redfin.csv')

cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
cols = cols[0:1] + cols[-1:] + cols[1:-1]

df = df[cols]

df.to_csv('./final_compilation/newer_redfin.csv', index=False)
