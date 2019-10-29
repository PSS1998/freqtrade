from freqtrade.data.btanalysis import load_backtest_data
import pandas as pd
import numpy as np
from decimal import *

getcontext().prec = 10

pd.set_option('display.max_rows', 250, 'display.max_columns', 100, 'display.expand_frame_repr', False)
df = load_backtest_data("user_data/backtest_data/backtest-result.json")

# Show value-counts per pair
df.groupby("pair")["sell_reason"].value_counts()
print(df)
