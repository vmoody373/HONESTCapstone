import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


df = pd.read_csv("data/input/pcaps/output/netflow.csv")

df0 = df[(df["sa"] == "44.218.53.147") | (df["da"] == "44.218.53.147")]

print(df0)

print(df.tail(100))
