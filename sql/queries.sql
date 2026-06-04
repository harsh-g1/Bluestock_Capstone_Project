SELECT
    d.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund d
    ON p.amfi_code = d.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;



SELECT
    strftime('%Y-%m', nav_date) AS month,
    ROUND(AVG(nav), 2) AS avg_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', nav_date)
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