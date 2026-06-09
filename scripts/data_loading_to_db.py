import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sql" / "bluestock_mf.db"
engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")

processed = BASE_DIR / "data" / "processed"

df = pd.read_csv(processed / "clean_fund_master.csv")

df.to_sql(
    "dim_fund",
    con=engine,
    if_exists="replace",
    index=False
)

df1 = pd.read_csv(processed / "clean_nav.csv")

df1.to_sql(
    "fact_nav",
    con=engine,
    if_exists="replace",
    index=False
)

df2 = pd.read_csv(processed / "clean_transactions.csv")

df2.to_sql(
    "fact_transactions",
    con=engine,
    if_exists="replace",
    index=False
)

df3 = pd.read_csv(processed / "clean_performance.csv")

df3.to_sql(
    "fact_performance",
    con=engine,
    if_exists="replace",
    index=False
)

df4 = pd.read_csv(processed / "clean_aum.csv")

df4.to_sql(
    "fact_aum",
    con=engine,
    if_exists="replace",
    index=False
)

df5 = pd.read_csv(processed / "clean_monthly_sip_inflows.csv")

df5.to_sql(
    "fact_sip_inflows",
    con=engine,
    if_exists="replace",
    index=False
)


df6 = pd.read_csv(processed / "clean_category_inflows.csv")
df6.to_sql(
    "fact_category_inflows",
    con=engine,
    if_exists="replace",
    index=False
)

df7 = pd.read_csv(processed / "clean_folio_count.csv")
df7.to_sql(
    "fact_folio_count",
    con=engine,
    if_exists="replace",
    index=False
)

df8 = pd.read_csv(processed / "clean_holdings.csv")
df8.to_sql(
    "fact_holdings",
    con=engine,
    if_exists="replace",
    index=False
)

df9 = pd.read_csv(processed / "clean_indices.csv")
df9.to_sql(
    "fact_index_values",
    con=engine,
    if_exists="replace",
    index=False
)