# Mutual Fund Analytics Database – Data Dictionary

## Overview

This database supports mutual fund analytics, investor behavior analysis, fund performance evaluation, SIP trend monitoring, portfolio analysis, and dashboard reporting. The schema follows a star-schema design with dimension tables and fact tables.

---

# Table: dim_fund

**Purpose:** Master reference table containing details of all mutual fund schemes.

**Source:** 01_fund_master.csv

| Column Name        | Data Type | Key         | Description                                                     |
| ------------------ | --------- | ----------- | --------------------------------------------------------------- |
| amfi_code          | TEXT      | Primary Key | Unique AMFI scheme identifier                                   |
| fund_house         | TEXT      |             | Asset Management Company (AMC) name                             |
| scheme_name        | TEXT      |             | Official mutual fund scheme name                                |
| category           | TEXT      |             | Fund category (Equity, Debt, Hybrid, etc.)                      |
| sub_category       | TEXT      |             | Detailed category (Large Cap, Mid Cap, Small Cap, Liquid, etc.) |
| plan               | TEXT      |             | Direct or Regular plan                                          |
| launch_date        | DATE      |             | Fund launch date                                                |
| benchmark          | TEXT      |             | Benchmark index used for comparison                             |
| expense_ratio_pct  | REAL      |             | Annual expense ratio charged by AMC                             |
| exit_load_pct      | REAL      |             | Exit load percentage applicable on redemption                   |
| min_sip_amount     | REAL      |             | Minimum SIP investment amount                                   |
| min_lumpsum_amount | REAL      |             | Minimum lump sum investment amount                              |
| fund_manager       | TEXT      |             | Name of the primary fund manager                                |
| risk_category      | TEXT      |             | Risk classification (Low, Moderate, High, Very High)            |
| sebi_category_code | TEXT      |             | SEBI classification code                                        |

---

# Table: fact_nav

**Purpose:** Stores historical daily NAV values for each scheme.
**Source:** 02_nav_history.csv

| Column Name  | Data Type | Key         | Description                                       |
| ------------ | --------- | ----------- | ------------------------------------------------- |
| nav_id       | INTEGER   | Primary Key | Unique NAV record identifier                      |
| amfi_code    | TEXT      | Foreign Key | References dim_fund.amfi_code                     |
| nav_date     | DATE      |             | NAV reporting date                                |
| nav          | REAL      |             | Net Asset Value per unit                          |
| daily_return | REAL      |             | Daily percentage return derived from NAV movement |

---

# Table: fact_transactions

**Purpose:** Stores investor transaction history.
**Source:** 08_investor_transactions.csv

| Column Name        | Data Type | Key         | Description                             |
| ------------------ | --------- | ----------- | --------------------------------------- |
| transaction_id     | INTEGER   | Primary Key | Unique transaction identifier           |
| investor_id        | TEXT      |             | Unique investor identifier              |
| amfi_code          | TEXT      | Foreign Key | Fund associated with the transaction    |
| transaction_date   | DATE      |             | Date of transaction                     |
| transaction_type   | TEXT      |             | SIP, Lumpsum, or Redemption             |
| amount_inr         | REAL      |             | Transaction amount in Indian Rupees     |
| state              | TEXT      |             | Investor state                          |
| city               | TEXT      |             | Investor city                           |
| city_tier          | TEXT      |             | T30 or B30 classification               |
| age_group          | TEXT      |             | Investor age bucket                     |
| gender             | TEXT      |             | Investor gender                         |
| annual_income_lakh | REAL      |             | Annual income in lakh rupees            |
| payment_mode       | TEXT      |             | UPI, Net Banking, Mandate, Cheque, etc. |
| kyc_status         | TEXT      |             | KYC verification status                 |

---

# Table: fact_performance

**Purpose:** Stores fund performance and risk metrics.
**Source:** 07_scheme_performance.csv

| Column Name        | Data Type | Key         | Description                          |
| ------------------ | --------- | ----------- | ------------------------------------ |
| performance_id     | INTEGER   | Primary Key | Unique performance record            |
| amfi_code          | TEXT      | Foreign Key | References dim_fund.amfi_code        |
| return_1yr_pct     | REAL      |             | One-year return percentage           |
| return_3yr_pct     | REAL      |             | Three-year CAGR                      |
| return_5yr_pct     | REAL      |             | Five-year CAGR                       |
| benchmark_3yr_pct  | REAL      |             | Benchmark three-year CAGR            |
| alpha              | REAL      |             | Excess return over benchmark         |
| beta               | REAL      |             | Market sensitivity measure           |
| sharpe_ratio       | REAL      |             | Risk-adjusted return metric          |
| sortino_ratio      | REAL      |             | Downside-risk-adjusted return metric |
| std_dev_ann_pct    | REAL      |             | Annualized volatility                |
| max_drawdown_pct   | REAL      |             | Maximum historical loss from peak    |
| aum_crore          | REAL      |             | Assets Under Management in crore INR |
| expense_ratio_pct  | REAL      |             | Annual expense ratio                 |
| morningstar_rating | INTEGER   |             | Morningstar star rating (1–5)        |
| risk_grade         | TEXT      |             | Risk grade assigned to scheme        |

---

# Table: fact_aum

**Purpose:** Historical AUM records by fund house.
**Source:** 03_aum_by_fund_house.csv

| Column Name        | Data Type | Key         | Description                |
| ------------------ | --------- | ----------- | -------------------------- |
| aum_id             | INTEGER   | Primary Key | Unique AUM record          |
| date               | DATE      |             | Reporting date             |
| fund_house         | TEXT      |             | Asset management company   |
| aum_lakh_crore     | REAL      |             | AUM in lakh crore INR      |
| aum_crore          | REAL      |             | AUM in crore INR           |
| num_schemes        | INTEGER   |             | Number of schemes managed  |
| (date, fund_house) | UNIQUE    |             | Prevents duplicate records |

---

# Table: fact_category_inflows

**Purpose:** Tracks category-wise monthly inflows.
**Source:** 05_category_inflows.csv

| Column Name       | Data Type | Key         | Description                       |
| ----------------- | --------- | ----------- | --------------------------------- |
| inflow_id         | INTEGER   | Primary Key | Unique inflow record              |
| month             | DATE      |             | Reporting month                   |
| category          | TEXT      |             | Fund category                     |
| net_inflow_crore  | REAL      |             | Net monthly inflow in crore INR   |
| (month, category) | UNIQUE    |             | One record per category per month |

---

# Table: fact_folio_count

**Purpose:** Monthly folio statistics.
**Source:** 06_industry_folio_count.csv

| Column Name         | Data Type | Key         | Description           |
| ------------------- | --------- | ----------- | --------------------- |
| folio_id            | INTEGER   | Primary Key | Unique folio record   |
| month               | DATE      |             | Reporting month       |
| total_folios_crore  | REAL      |             | Total folios in crore |
| equity_folios_crore | REAL      |             | Equity fund folios    |
| debt_folios_crore   | REAL      |             | Debt fund folios      |
| hybrid_folios_crore | REAL      |             | Hybrid fund folios    |
| others_folios_crore | REAL      |             | Other category folios |
| month               | UNIQUE    |             | One record per month  |

---

# Table: fact_holdings

**Purpose:** Portfolio holdings of schemes.
**Source:** 09_portfolio_holdings.csv

| Column Name                               | Data Type | Key         | Description                     |
| ----------------------------------------- | --------- | ----------- | ------------------------------- |
| holding_id                                | INTEGER   | Primary Key | Unique holding record           |
| amfi_code                                 | TEXT      | Foreign Key | References dim_fund.amfi_code   |
| stock_symbol                              | TEXT      |             | Stock ticker symbol             |
| stock_name                                | TEXT      |             | Company name                    |
| sector                                    | TEXT      |             | Industry sector                 |
| weight_pct                                | REAL      |             | Portfolio allocation percentage |
| market_value_cr                           | REAL      |             | Market value in crore INR       |
| current_price_inr                         | REAL      |             | Current stock price             |
| portfolio_date                            | DATE      |             | Portfolio reporting date        |
| (amfi_code, stock_symbol, portfolio_date) | UNIQUE    |             | Prevents duplicate holdings     |

---

# Table: dim_index

**Purpose:** Master list of benchmark indices.

| Column Name | Data Type | Key         | Description          |
| ----------- | --------- | ----------- | -------------------- |
| index_name  | TEXT      | Primary Key | Benchmark index name |

---

# Table: fact_index_values

**Purpose:** Historical benchmark index values.
**Source:** 10_benchmark_indices.csv

| Column Name        | Data Type | Key         | Description                     |
| ------------------ | --------- | ----------- | ------------------------------- |
| index_value_id     | INTEGER   | Primary Key | Unique index value record       |
| date               | DATE      |             | Observation date                |
| index_name         | TEXT      | Foreign Key | References dim_index.index_name |
| close_value        | REAL      |             | Index closing value             |
| (date, index_name) | UNIQUE    |             | Prevents duplicate index values |

---

# Table: fact_sip_inflows

**Purpose:** Monthly SIP industry statistics.
**Source:** 04_monthly_sip_inflows.csv

| Column Name               | Data Type | Key         | Description                                   |
| ------------------------- | --------- | ----------- | --------------------------------------------- |
| sip_id                    | INTEGER   | Primary Key | Unique SIP record                             |
| month                     | DATE      |             | Reporting month                               |
| sip_inflow_crore          | REAL      |             | Total SIP inflow in crore INR                 |
| active_sip_accounts_crore | REAL      |             | Active SIP accounts in crore                  |
| new_sip_accounts_lakh     | REAL      |             | Newly registered SIP accounts in lakh         |
| sip_aum_lakh_crore        | REAL      |             | SIP assets under management in lakh crore INR |
| yoy_growth_pct            | REAL      |             | Year-over-year growth in SIP inflows          |
| month                     | UNIQUE    |             | One record per month                          |

---

# Relationships

* dim_fund → fact_nav (1:M)
* dim_fund → fact_transactions (1:M)
* dim_fund → fact_performance (1:1 or 1:M)
* dim_fund → fact_holdings (1:M)
* dim_index → fact_index_values (1:M)

