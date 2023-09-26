import sys
sys.path.append("/Users/MedDoc/AppData/Local/Programs/Python/Python310/Scripts")

import pandas as pd
import sqlite3

db = sqlite3.connect('data.db')
dfs = pd.read_excel('US_Regional_Sales_Data.xls', sheet_name=None)
for table, df in dfs.items():
    df.to_sql(table, db)
    print(f'{df} inserted successfully')