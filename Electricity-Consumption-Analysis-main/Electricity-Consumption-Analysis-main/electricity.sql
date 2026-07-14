CREATE TABLE Electricity (
    States VARCHAR2(50),
    Regions VARCHAR2(10),
    Latitude NUMBER,
    Longitude NUMBER,
    Dates DATE,
    Usage NUMBER
);
SELECT COUNT(*) FROM Electricityy;
SELECT *
FROM Electricityy
FETCH FIRST 10 ROWS ONLY;
SELECT DISTINCT States
FROM Electricityy
ORDER BY States;


SELECT DISTINCT States
FROM Electricityy
ORDER BY States;

SELECT DISTINCT Regions
FROM Electricityy;

SELECT MAX(Usage)
FROM Electricityy;

SELECT MIN(Usage)
FROM Electricityy;

SELECT ROUND(AVG(Usage),2)
FROM Electricityy;

SELECT ROUND(SUM(Usage),2)
FROM Electricityy;

SELECT States,
       ROUND(SUM(Usage),2) Total_Usage
FROM Electricityy
GROUP BY States
ORDER BY Total_Usage DESC;

SELECT Regions,
       ROUND(SUM(Usage),2) Total_Usage
FROM Electricityy
GROUP BY Regions
ORDER BY Total_Usage DESC;

SELECT States,
       ROUND(AVG(Usage),2) Average_Usage
FROM Electricityy
GROUP BY States
ORDER BY Average_Usage DESC;

SELECT States,
       COUNT(*) Records
FROM Electricityy
GROUP BY States;

SELECT EXTRACT(YEAR FROM Dates) Year,
       ROUND(SUM(Usage),2) Total_Usage
FROM Electricityy
GROUP BY EXTRACT(YEAR FROM Dates)
ORDER BY Year;

SELECT TO_CHAR(Dates,'Month') Month,
       ROUND(SUM(Usage),2) Total_Usage
FROM Electricityy
GROUP BY TO_CHAR(Dates,'Month')
ORDER BY MIN(EXTRACT(MONTH FROM Dates));

SELECT Dates,
       ROUND(AVG(Usage),2)
FROM Electricityy
GROUP BY Dates
ORDER BY Dates;

SELECT *
FROM Electricityy
WHERE Usage > 500;
SELECT *
FROM Electricityy
WHERE Regions='SR';

SELECT *
FROM Electricityy
ORDER BY Usage DESC;

SELECT States,
       SUM(Usage)
FROM Electricityy
GROUP BY States
HAVING SUM(Usage)>100000;


SELECT States,
       SUM(Usage) Total_Usage,
       RANK() OVER(ORDER BY SUM(Usage) DESC) Ranking
FROM Electricityy
GROUP BY States;

SELECT *
FROM
(
SELECT States,
       SUM(Usage) Total_Usage
FROM Electricityy
GROUP BY States
ORDER BY Total_Usage DESC
)
FETCH FIRST 5 ROWS ONLY;


SELECT *
FROM
(
SELECT Regions,
       States,
       SUM(Usage) Total_Usage,
       RANK() OVER(PARTITION BY Regions ORDER BY SUM(Usage) DESC) rnk
FROM Electricityy
GROUP BY Regions,States
)
WHERE rnk=1;


SELECT States,
       Usage,
       CASE
           WHEN Usage<200 THEN 'Low'
           WHEN Usage BETWEEN 200 AND 400 THEN 'Medium'
           ELSE 'High'
       END Usage_Level
FROM Electricityy;

SELECT *
FROM
(
SELECT
EXTRACT(YEAR FROM Dates) Year,
States,
SUM(Usage) Total_Usage,
DENSE_RANK() OVER
(
PARTITION BY EXTRACT(YEAR FROM Dates)
ORDER BY SUM(Usage) DESC
) rnk
FROM Electricityy
GROUP BY EXTRACT(YEAR FROM Dates),States
)
WHERE rnk<=3;





















































































































































