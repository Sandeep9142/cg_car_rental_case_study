-- ============================================================
-- Car Rental Order Processing System - Sample Data Inserts
-- Developer 6 - SQL Analytics
-- At least 10 records per table
-- ============================================================

-- LOCATIONS (12 records)
INSERT INTO LOCATIONS VALUES (1, 'Bengaluru', 'MG Road Hub', 'Central', FALSE, '080-1111-0001');
INSERT INTO LOCATIONS VALUES (2, 'Bengaluru', 'Kempegowda Airport', 'Airport', TRUE, '080-1111-0002');
INSERT INTO LOCATIONS VALUES (3, 'Mumbai', 'Andheri West Station', 'Suburban', FALSE, '022-2222-0001');
INSERT INTO LOCATIONS VALUES (4, 'Mumbai', 'Chhatrapati Shivaji Airport', 'Airport', TRUE, '022-2222-0002');
INSERT INTO LOCATIONS VALUES (5, 'Delhi', 'Connaught Place', 'Central', FALSE, '011-3333-0001');
INSERT INTO LOCATIONS VALUES (6, 'Delhi', 'IGI Airport T3', 'Airport', TRUE, '011-3333-0002');
INSERT INTO LOCATIONS VALUES (7, 'Hyderabad', 'Banjara Hills', 'Central', FALSE, '040-4444-0001');
INSERT INTO LOCATIONS VALUES (8, 'Hyderabad', 'Rajiv Gandhi Airport', 'Airport', TRUE, '040-4444-0002');
INSERT INTO LOCATIONS VALUES (9, 'Chennai', 'T. Nagar', 'Central', FALSE, '044-5555-0001');
INSERT INTO LOCATIONS VALUES (10, 'Chennai', 'Chennai Airport', 'Airport', TRUE, '044-5555-0002');
INSERT INTO LOCATIONS VALUES (11, 'Kolkata', 'Park Street', 'Central', FALSE, '033-6666-0001');
INSERT INTO LOCATIONS VALUES (12, 'Kolkata', 'Netaji Subhas Airport', 'Airport', TRUE, '033-6666-0002');

-- CUSTOMERS (15 records)
INSERT INTO CUSTOMERS VALUES (1, 'Aarav Sharma', 'aarav.sharma@email.com', '9876543210', 'Bengaluru', '2024-01-15', 'Gold');
INSERT INTO CUSTOMERS VALUES (2, 'Priya Patel', 'priya.patel@email.com', '9876543211', 'Mumbai', '2024-02-20', 'Silver');
INSERT INTO CUSTOMERS VALUES (3, 'Rohan Gupta', 'rohan.gupta@email.com', '9876543212', 'Delhi', '2024-03-10', 'Bronze');
INSERT INTO CUSTOMERS VALUES (4, 'Sneha Reddy', 'sneha.reddy@email.com', '9876543213', 'Hyderabad', '2024-04-05', 'Gold');
INSERT INTO CUSTOMERS VALUES (5, 'Vikram Singh', 'vikram.singh@email.com', '9876543214', 'Chennai', '2024-05-12', 'Platinum');
INSERT INTO CUSTOMERS VALUES (6, 'Anjali Nair', 'anjali.nair@email.com', '9876543215', 'Bengaluru', '2024-06-01', 'Silver');
INSERT INTO CUSTOMERS VALUES (7, 'Karthik Iyer', 'karthik.iyer@email.com', '9876543216', 'Kolkata', '2024-07-18', 'Bronze');
INSERT INTO CUSTOMERS VALUES (8, 'Meera Joshi', 'meera.joshi@email.com', '9876543217', 'Mumbai', '2024-08-22', 'Gold');
INSERT INTO CUSTOMERS VALUES (9, 'Arjun Das', 'arjun.das@email.com', '9876543218', 'Delhi', '2024-09-30', 'Silver');
INSERT INTO CUSTOMERS VALUES (10, 'Divya Menon', 'divya.menon@email.com', '9876543219', 'Bengaluru', '2024-10-14', 'Bronze');
INSERT INTO CUSTOMERS VALUES (11, 'Rahul Verma', 'rahul.verma@email.com', '9876543220', 'Hyderabad', '2024-11-05', 'Silver');
INSERT INTO CUSTOMERS VALUES (12, 'Pooja Kumar', 'pooja.kumar@email.com', '9876543221', 'Chennai', '2024-12-01', 'Gold');
INSERT INTO CUSTOMERS VALUES (13, 'Amit Saxena', 'amit.saxena@email.com', '9876543222', 'Delhi', '2025-01-10', 'Bronze');
INSERT INTO CUSTOMERS VALUES (14, 'Neha Agarwal', 'neha.agarwal@email.com', '9876543223', 'Kolkata', '2025-02-18', 'Silver');
INSERT INTO CUSTOMERS VALUES (15, 'Siddharth Rao', 'siddharth.rao@email.com', '9876543224', 'Mumbai', '2025-03-01', 'Platinum');

-- VEHICLES (15 records)
INSERT INTO VEHICLES VALUES ('CAR-01', 'Maruti', 'Swift', 2024, 'Hatchback', 800.00, 1, 'Available', 15000);
INSERT INTO VEHICLES VALUES ('CAR-02', 'Hyundai', 'Creta', 2024, 'SUV', 1500.00, 1, 'Rented', 22000);
INSERT INTO VEHICLES VALUES ('CAR-03', 'Toyota', 'Innova', 2023, 'MPV', 2000.00, 3, 'Available', 45000);
INSERT INTO VEHICLES VALUES ('CAR-04', 'Honda', 'City', 2024, 'Sedan', 1200.00, 5, 'Rented', 18000);
INSERT INTO VEHICLES VALUES ('CAR-05', 'Tata', 'Nexon', 2024, 'SUV', 1300.00, 7, 'Available', 12000);
INSERT INTO VEHICLES VALUES ('CAR-06', 'Kia', 'Seltos', 2023, 'SUV', 1400.00, 9, 'Maintenance', 35000);
INSERT INTO VEHICLES VALUES ('CAR-07', 'Mahindra', 'XUV700', 2024, 'SUV', 2500.00, 2, 'Available', 8000);
INSERT INTO VEHICLES VALUES ('CAR-08', 'Maruti', 'Baleno', 2024, 'Hatchback', 900.00, 4, 'Rented', 20000);
INSERT INTO VEHICLES VALUES ('CAR-09', 'Hyundai', 'Verna', 2023, 'Sedan', 1100.00, 6, 'Available', 30000);
INSERT INTO VEHICLES VALUES ('CAR-10', 'Toyota', 'Fortuner', 2024, 'SUV', 3500.00, 8, 'Available', 10000);
INSERT INTO VEHICLES VALUES ('CAR-11', 'Tata', 'Harrier', 2024, 'SUV', 1800.00, 11, 'Available', 5000);
INSERT INTO VEHICLES VALUES ('CAR-12', 'Honda', 'Amaze', 2023, 'Sedan', 1000.00, 3, 'Rented', 28000);
INSERT INTO VEHICLES VALUES ('CAR-13', 'Kia', 'Sonet', 2024, 'SUV', 1200.00, 5, 'Available', 9000);
INSERT INTO VEHICLES VALUES ('CAR-14', 'Maruti', 'Ertiga', 2024, 'MPV', 1600.00, 10, 'Available', 16000);
INSERT INTO VEHICLES VALUES ('CAR-15', 'Hyundai', 'i20', 2024, 'Hatchback', 850.00, 12, 'Available', 11000);

-- RESERVATIONS (15 records)
INSERT INTO RESERVATIONS VALUES ('RES-00001', 1, 'CAR-02', 1, '2026-01-05 09:00', '2026-01-07 18:00', 22000, 22450, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00002', 2, 'CAR-04', 5, '2026-01-10 10:00', '2026-01-12 10:00', 18000, 18320, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00003', 3, 'CAR-07', 2, '2026-01-15 14:00', '2026-01-18 14:00', 8000, 8600, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00004', 4, 'CAR-10', 8, '2026-01-20 08:00', '2026-01-25 20:00', 10000, 10900, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00005', 5, 'CAR-01', 9, '2026-02-01 07:00', '2026-02-03 19:00', 15000, 15280, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00006', 6, 'CAR-03', 3, '2026-02-05 11:00', '2026-02-08 11:00', 45000, 45750, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00007', 7, 'CAR-08', 4, '2026-02-10 09:30', '2026-02-12 18:30', 20000, 20180, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00008', 8, 'CAR-12', 3, '2026-02-14 10:00', '2026-02-16 10:00', 28000, 28400, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00009', 9, 'CAR-05', 7, '2026-02-20 12:00', '2026-02-22 12:00', 12000, 12350, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00010', 10, 'CAR-11', 11, '2026-02-25 06:00', '2026-02-28 18:00', 5000, 5520, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00011', 1, 'CAR-09', 6, '2026-03-01 08:00', '2026-03-04 08:00', 30000, 30500, 'Active');
INSERT INTO RESERVATIONS VALUES ('RES-00012', 11, 'CAR-13', 5, '2026-03-02 09:00', '2026-03-05 09:00', 9000, 9320, 'Active');
INSERT INTO RESERVATIONS VALUES ('RES-00013', 12, 'CAR-06', 9, '2026-03-03 10:00', NULL, 35000, NULL, 'Active');
INSERT INTO RESERVATIONS VALUES ('RES-00014', 15, 'CAR-14', 10, '2026-03-05 07:00', '2026-03-08 19:00', 16000, 16480, 'Completed');
INSERT INTO RESERVATIONS VALUES ('RES-00015', 13, 'CAR-15', 12, '2026-03-06 11:00', '2026-03-09 11:00', 11000, 11290, 'Completed');

-- PAYMENTS (15 records)
INSERT INTO PAYMENTS VALUES (1, 'RES-00001', 3000.00, 'UPI', '2026-01-07 18:30', 'Completed');
INSERT INTO PAYMENTS VALUES (2, 'RES-00002', 2400.00, 'CARD', '2026-01-12 10:30', 'Completed');
INSERT INTO PAYMENTS VALUES (3, 'RES-00003', 7500.00, 'UPI', '2026-01-18 14:30', 'Completed');
INSERT INTO PAYMENTS VALUES (4, 'RES-00004', 17500.00, 'CARD', '2026-01-25 20:30', 'Completed');
INSERT INTO PAYMENTS VALUES (5, 'RES-00005', 1600.00, 'CASH', '2026-02-03 19:30', 'Completed');
INSERT INTO PAYMENTS VALUES (6, 'RES-00006', 6000.00, 'WALLET', '2026-02-08 11:30', 'Completed');
INSERT INTO PAYMENTS VALUES (7, 'RES-00007', 1800.00, 'UPI', '2026-02-12 18:45', 'Completed');
INSERT INTO PAYMENTS VALUES (8, 'RES-00008', 2000.00, 'CARD', '2026-02-16 10:30', 'Completed');
INSERT INTO PAYMENTS VALUES (9, 'RES-00009', 2600.00, 'UPI', '2026-02-22 12:30', 'Completed');
INSERT INTO PAYMENTS VALUES (10, 'RES-00010', 5400.00, 'CASH', '2026-02-28 18:30', 'Completed');
INSERT INTO PAYMENTS VALUES (11, 'RES-00011', 3300.00, 'WALLET', '2026-03-01 08:15', 'Pending');
INSERT INTO PAYMENTS VALUES (12, 'RES-00012', 3600.00, 'UPI', '2026-03-02 09:15', 'Pending');
INSERT INTO PAYMENTS VALUES (13, 'RES-00013', 0.00, 'CARD', '2026-03-03 10:15', 'Pending');
INSERT INTO PAYMENTS VALUES (14, 'RES-00014', 4800.00, 'CARD', '2026-03-08 19:30', 'Completed');
INSERT INTO PAYMENTS VALUES (15, 'RES-00015', 2550.00, 'CASH', '2026-03-09 11:30', 'Completed');

-- MAINTENANCE (12 records)
INSERT INTO MAINTENANCE VALUES (1, 'CAR-06', 'Oil Change', 'Regular 10K service oil change', 2500.00, '2026-03-01', '2026-03-02', 'Completed');
INSERT INTO MAINTENANCE VALUES (2, 'CAR-03', 'Tire Replacement', 'All four tires replaced', 12000.00, '2026-01-10', '2026-01-11', 'Completed');
INSERT INTO MAINTENANCE VALUES (3, 'CAR-09', 'Brake Pads', 'Front brake pad replacement', 3500.00, '2026-02-05', '2026-02-06', 'Completed');
INSERT INTO MAINTENANCE VALUES (4, 'CAR-01', 'AC Service', 'AC gas refill and compressor check', 4000.00, '2026-01-20', '2026-01-21', 'Completed');
INSERT INTO MAINTENANCE VALUES (5, 'CAR-12', 'Battery Replacement', 'New Exide battery installed', 6500.00, '2026-02-01', '2026-02-01', 'Completed');
INSERT INTO MAINTENANCE VALUES (6, 'CAR-05', 'General Service', '20K km periodic service', 5500.00, '2026-03-10', '2026-03-12', 'In Progress');
INSERT INTO MAINTENANCE VALUES (7, 'CAR-08', 'Clutch Repair', 'Clutch plate and bearing replacement', 8000.00, '2026-02-20', '2026-02-22', 'Completed');
INSERT INTO MAINTENANCE VALUES (8, 'CAR-10', 'Wheel Alignment', 'Four-wheel alignment and balancing', 1500.00, '2026-01-28', '2026-01-28', 'Completed');
INSERT INTO MAINTENANCE VALUES (9, 'CAR-02', 'Insurance Renewal', 'Comprehensive insurance renewal', 15000.00, '2026-03-05', '2026-03-05', 'Completed');
INSERT INTO MAINTENANCE VALUES (10, 'CAR-07', 'Dent Repair', 'Left rear door dent repair and paint', 7000.00, '2026-02-15', '2026-02-17', 'Completed');
INSERT INTO MAINTENANCE VALUES (11, 'CAR-11', 'Oil Change', '10K km service', 2500.00, '2026-03-15', NULL, 'Scheduled');
INSERT INTO MAINTENANCE VALUES (12, 'CAR-14', 'Tire Rotation', 'Rotate and balance all tires', 800.00, '2026-03-20', NULL, 'Scheduled');
