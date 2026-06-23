-- Headline numbers
SELECT
  COUNT(*)                     AS transactions,
  COUNT(DISTINCT customer_id)  AS customers,
  ROUND(SUM(revenue), 2)       AS total_revenue
FROM clean_transactions;

-- Monthly revenue trend
SELECT year_month, ROUND(SUM(revenue), 2) AS revenue
FROM clean_transactions
GROUP BY year_month
ORDER BY year_month;

-- Top 10 products by revenue
SELECT description, ROUND(SUM(revenue), 2) AS revenue
FROM clean_transactions
GROUP BY description
ORDER BY revenue DESC
LIMIT 10;

-- Top 10 export markets (excluding the home country)
SELECT country, ROUND(SUM(revenue), 2) AS revenue
FROM clean_transactions
WHERE country <> 'United Kingdom'
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;

-- Best customers by lifetime value
SELECT customer_id,
       COUNT(DISTINCT invoice) AS orders,
       ROUND(SUM(revenue), 2)  AS lifetime_value
FROM clean_transactions
GROUP BY customer_id
ORDER BY lifetime_value DESC
LIMIT 10;