-- Question 1
SELECT u.user_id, u.loyalty_status, u.loyalty_status_txt, SUM(price_nominal), to_char("quote_date",'DD/MM/YYYY') AS "day"
FROM cp_datawarehouse.rides AS r
JOIN cp_datawarehouse.users AS u ON u.user_id = r.user_id
GROUP BY u.user_id, day;

-- Question 2

SELECT AVG(price_nominal) AS basket, to_char("quote_date",'DD/MM/YYYY') AS "day"
FROM cp_datawarehouse.rides
WHERE state LIKE 'completed%'
GROUP BY day;

-- Question 3
SELECT * FROM (
    SELECT COUNT(ride_id) AS nb_rides, to_char("quote_date",'DD/MM/YYYY') AS "day"
    FROM cp_datawarehouse.rides
    WHERE state LIKE 'completed%'
    GROUP BY day
    ORDER BY nb_rides ASC limit 5
) as T1
ORDER BY day asc;