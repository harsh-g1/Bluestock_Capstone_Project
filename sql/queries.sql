SELECT
    d.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;



SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date)
ORDER BY month;



WITH yearly_sip AS (
    SELECT
        strftime('%Y', transaction_date) AS year,
        SUM(amount_inr) AS sip_inflow
    FROM fact_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY year
)
SELECT
    year,
    sip_inflow,
    ROUND(
        100.0 * (
            sip_inflow -
            LAG(sip_inflow) OVER (ORDER BY year)
        ) /
        LAG(sip_inflow) OVER (ORDER BY year),
        2
    ) AS yoy_growth_pct
FROM yearly_sip;




SELECT
    state,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_amount DESC;




SELECT
    d.scheme_name,
    p.expense_ratio_pct
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
WHERE p.expense_ratio_pct < 1
ORDER BY p.expense_ratio_pct;




SELECT
    d.scheme_name,
    p.return_3yr_pct,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
ORDER BY p.return_3yr_pct DESC
LIMIT 10;




SELECT
    fund_house,
    COUNT(*) AS total_schemes
FROM dim_fund
GROUP BY fund_house
ORDER BY total_schemes DESC;



SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;



SELECT
    age_group,
    ROUND(AVG(amount_inr), 2) AS avg_investment,
    COUNT(*) AS transaction_count
FROM fact_transactions
GROUP BY age_group
ORDER BY avg_investment DESC;



SELECT
    d.category,
    ROUND(AVG(p.return_3yr_pct), 2) AS avg_3yr_return,
    ROUND(AVG(p.sharpe_ratio), 2) AS avg_sharpe
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
GROUP BY d.category
ORDER BY avg_3yr_return DESC;
