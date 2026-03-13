-- ============================================================
-- Car Rental Order Processing System - SQL Analytics Solutions
-- Developer 6 - Advanced SQL Queries
-- ============================================================


-- ============================================================
-- Q1: Most Rented Vehicles (Top 5)
-- ============================================================
SELECT
    v.Vehicle_ID,
    v.Make,
    v.Model,
    COUNT(r.Reservation_ID) AS Total_Rentals
FROM VEHICLES v
JOIN RESERVATIONS r ON v.Vehicle_ID = r.Vehicle_ID
GROUP BY v.Vehicle_ID, v.Make, v.Model
ORDER BY Total_Rentals DESC
LIMIT 5;


-- ============================================================
-- Q2: Customers with Highest Total Spending
-- ============================================================
SELECT
    c.Customer_ID,
    c.Name,
    c.Loyalty_Tier,
    SUM(p.Amount) AS Total_Spent,
    COUNT(r.Reservation_ID) AS Total_Bookings
FROM CUSTOMERS c
JOIN RESERVATIONS r ON c.Customer_ID = r.Customer_ID
JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
WHERE p.Status = 'Completed'
GROUP BY c.Customer_ID, c.Name, c.Loyalty_Tier
ORDER BY Total_Spent DESC;


-- ============================================================
-- Q3: Vehicles with Highest Utilization (Total Distance)
-- ============================================================
SELECT
    v.Vehicle_ID,
    v.Make,
    v.Model,
    SUM(r.Odo_End - r.Odo_Start) AS Total_Distance_km,
    COUNT(r.Reservation_ID) AS Total_Trips
FROM VEHICLES v
JOIN RESERVATIONS r ON v.Vehicle_ID = r.Vehicle_ID
WHERE r.Odo_End IS NOT NULL AND r.Odo_Start IS NOT NULL
GROUP BY v.Vehicle_ID, v.Make, v.Model
ORDER BY Total_Distance_km DESC;


-- ============================================================
-- Q4: Cities with Most Rentals
-- ============================================================
SELECT
    l.City,
    COUNT(r.Reservation_ID) AS Total_Rentals,
    SUM(p.Amount) AS Total_Revenue
FROM LOCATIONS l
JOIN RESERVATIONS r ON l.Location_ID = r.Location_ID
JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
GROUP BY l.City
ORDER BY Total_Rentals DESC;


-- ============================================================
-- Q5: Vehicles Currently Available (not rented or in maintenance)
-- ============================================================
SELECT
    v.Vehicle_ID,
    v.Make,
    v.Model,
    v.Category,
    v.Daily_Rate,
    l.City,
    l.Address
FROM VEHICLES v
JOIN LOCATIONS l ON v.Location_ID = l.Location_ID
WHERE v.Status = 'Available'
ORDER BY v.Daily_Rate;


-- ============================================================
-- Q6: Average Revenue per Vehicle
-- ============================================================
SELECT
    v.Vehicle_ID,
    v.Make,
    v.Model,
    v.Daily_Rate,
    COUNT(r.Reservation_ID) AS Num_Rentals,
    COALESCE(AVG(p.Amount), 0) AS Avg_Revenue_Per_Rental,
    COALESCE(SUM(p.Amount), 0) AS Total_Revenue
FROM VEHICLES v
LEFT JOIN RESERVATIONS r ON v.Vehicle_ID = r.Vehicle_ID
LEFT JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
GROUP BY v.Vehicle_ID, v.Make, v.Model, v.Daily_Rate
ORDER BY Total_Revenue DESC;


-- ============================================================
-- Q7: Window Function - Running Total Revenue by Customer
-- ============================================================
SELECT
    c.Name,
    r.Reservation_ID,
    p.Amount,
    p.Payment_Date,
    SUM(p.Amount) OVER (
        PARTITION BY c.Customer_ID
        ORDER BY p.Payment_Date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS Running_Total_Spent
FROM CUSTOMERS c
JOIN RESERVATIONS r ON c.Customer_ID = r.Customer_ID
JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
WHERE p.Status = 'Completed'
ORDER BY c.Name, p.Payment_Date;


-- ============================================================
-- Q8: Window Function - Rank Vehicles by Revenue within Each City
-- ============================================================
SELECT
    l.City,
    v.Vehicle_ID,
    v.Make,
    v.Model,
    SUM(p.Amount) AS Total_Revenue,
    RANK() OVER (
        PARTITION BY l.City
        ORDER BY SUM(p.Amount) DESC
    ) AS Revenue_Rank
FROM LOCATIONS l
JOIN VEHICLES v ON l.Location_ID = v.Location_ID
JOIN RESERVATIONS r ON v.Vehicle_ID = r.Vehicle_ID
JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
WHERE p.Status = 'Completed'
GROUP BY l.City, v.Vehicle_ID, v.Make, v.Model
ORDER BY l.City, Revenue_Rank;


-- ============================================================
-- Q9: CTE - Monthly Revenue Trend
-- ============================================================
WITH MonthlyRevenue AS (
    SELECT
        EXTRACT(YEAR FROM p.Payment_Date) AS Rev_Year,
        EXTRACT(MONTH FROM p.Payment_Date) AS Rev_Month,
        SUM(p.Amount) AS Monthly_Revenue,
        COUNT(DISTINCT r.Reservation_ID) AS Num_Bookings
    FROM PAYMENTS p
    JOIN RESERVATIONS r ON p.Reservation_ID = r.Reservation_ID
    WHERE p.Status = 'Completed'
    GROUP BY EXTRACT(YEAR FROM p.Payment_Date), EXTRACT(MONTH FROM p.Payment_Date)
)
SELECT
    Rev_Year,
    Rev_Month,
    Monthly_Revenue,
    Num_Bookings,
    LAG(Monthly_Revenue) OVER (ORDER BY Rev_Year, Rev_Month) AS Prev_Month_Revenue,
    Monthly_Revenue - COALESCE(LAG(Monthly_Revenue) OVER (ORDER BY Rev_Year, Rev_Month), 0) AS Revenue_Change
FROM MonthlyRevenue
ORDER BY Rev_Year, Rev_Month;


-- ============================================================
-- Q10: CTE - Vehicle Maintenance Cost vs Revenue
-- ============================================================
WITH VehicleRevenue AS (
    SELECT
        v.Vehicle_ID,
        v.Make,
        v.Model,
        COALESCE(SUM(p.Amount), 0) AS Total_Revenue
    FROM VEHICLES v
    LEFT JOIN RESERVATIONS r ON v.Vehicle_ID = r.Vehicle_ID
    LEFT JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID AND p.Status = 'Completed'
    GROUP BY v.Vehicle_ID, v.Make, v.Model
),
VehicleMaintenance AS (
    SELECT
        Vehicle_ID,
        COALESCE(SUM(Cost), 0) AS Total_Maintenance_Cost,
        COUNT(*) AS Maintenance_Count
    FROM MAINTENANCE
    GROUP BY Vehicle_ID
)
SELECT
    vr.Vehicle_ID,
    vr.Make,
    vr.Model,
    vr.Total_Revenue,
    COALESCE(vm.Total_Maintenance_Cost, 0) AS Total_Maintenance_Cost,
    COALESCE(vm.Maintenance_Count, 0) AS Maintenance_Count,
    vr.Total_Revenue - COALESCE(vm.Total_Maintenance_Cost, 0) AS Net_Profit
FROM VehicleRevenue vr
LEFT JOIN VehicleMaintenance vm ON vr.Vehicle_ID = vm.Vehicle_ID
ORDER BY Net_Profit DESC;


-- ============================================================
-- Q11: CTE - Customer Loyalty Analysis
-- ============================================================
WITH CustomerActivity AS (
    SELECT
        c.Customer_ID,
        c.Name,
        c.Loyalty_Tier,
        COUNT(r.Reservation_ID) AS Num_Bookings,
        SUM(p.Amount) AS Total_Spent,
        AVG(p.Amount) AS Avg_Spent_Per_Booking,
        MIN(r.Pickup_TS) AS First_Booking,
        MAX(r.Pickup_TS) AS Last_Booking
    FROM CUSTOMERS c
    LEFT JOIN RESERVATIONS r ON c.Customer_ID = r.Customer_ID
    LEFT JOIN PAYMENTS p ON r.Reservation_ID = p.Reservation_ID
    GROUP BY c.Customer_ID, c.Name, c.Loyalty_Tier
)
SELECT
    Customer_ID,
    Name,
    Loyalty_Tier,
    Num_Bookings,
    Total_Spent,
    Avg_Spent_Per_Booking,
    First_Booking,
    Last_Booking,
    CASE
        WHEN Num_Bookings >= 3 AND Total_Spent > 5000 THEN 'High Value'
        WHEN Num_Bookings >= 2 THEN 'Regular'
        ELSE 'New'
    END AS Customer_Segment
FROM CustomerActivity
ORDER BY Total_Spent DESC;


-- ============================================================
-- Q12: Window Function - Gap Between Consecutive Bookings per Vehicle
-- ============================================================
SELECT
    Vehicle_ID,
    Reservation_ID,
    Pickup_TS,
    Return_TS,
    LAG(Return_TS) OVER (PARTITION BY Vehicle_ID ORDER BY Pickup_TS) AS Prev_Return,
    TIMESTAMPDIFF(HOUR,
        LAG(Return_TS) OVER (PARTITION BY Vehicle_ID ORDER BY Pickup_TS),
        Pickup_TS
    ) AS Gap_Hours
FROM RESERVATIONS
WHERE Return_TS IS NOT NULL
ORDER BY Vehicle_ID, Pickup_TS;
