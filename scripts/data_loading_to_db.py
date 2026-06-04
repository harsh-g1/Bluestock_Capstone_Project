import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///D:/bluestock_mf_capstone/sql/bluestock_mf.db")

df = pd.read_csv("D:/bluestock_mf_capstone/data/processed/clean_fund_master.csv")

df.to_sql(
    "dim_fund",
    con=engine,
    if_exists="replace",
    index=False
)

df1 = pd.read_csv("D:/bluestock_mf_capstone/data/processed/clean_nav.csv")

df1.to_sql(
    "fact_nav",
    con=engine,
    if_exists="replace",
    index=False
)

df2 = pd.read_csv("D:/bluestock_mf_capstone/data/processed/clean_transactions.csv")

df2.to_sql(
    "fact_transactions",
    con=engine,
    if_exists="replace",
    index=False
)

df3 = pd.read_csv("D:/bluestock_mf_capstone/data/processed/clean_performance.csv")

df3.to_sql(
    "fact_performance",
    con=engine,
    if_exists="replace",
    index=False
)