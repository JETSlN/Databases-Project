-- a
INSERT INTO airline VALUES('Jet Blue');
INSERT INTO airline VALUES('American Airlines');

-- b
INSERT INTO airport VALUES('JFK', 'New York', 'USA', 'International');
INSERT INTO airport VALUES('PVG', 'Shanghai', 'China', 'International');

-- c
INSERT INTO customer VALUES('kenny@airlinecustomer.com', 'Kenny', 'password', '6', 'MetroTech Center', 'Brooklyn', 'NY', '000000', '000000', '2023-12-31', 'USA', '2000-1-1');
INSERT INTO customer VALUES('jeff@airlinecustomer.com', 'Jeff', 'password', '6', 'MetroTech Center', 'Brooklyn', 'NY', '000000', '000000', '2023-12-31', 'USA', '2000-1-1');
INSERT INTO customer VALUES('mahmoud@airlinecustomer.com', 'Mahmoud', 'password', '6', 'MetroTech Center', 'Brooklyn', 'NY', '000000', '000000', '2023-12-31', 'USA', '2000-1-1');
INSERT INTO customer VALUES('dummy@airlinecustomer.com', 'Dummy', 'password', '6', 'MetroTech Center', 'Brooklyn', 'NY', '000000', '000000', '2023-12-31', 'USA', '2000-1-1');

-- d
INSERT INTO airplane VALUES('Jet Blue', 1000, 200, 'Boeing', 5);
INSERT INTO airplane VALUES('Jet Blue', 1001, 250, 'Boeing', 20);
INSERT INTO airplane VALUES('Jet Blue', 1002, 300, 'Boeing', 2);
INSERT INTO airplane VALUES('American Airlines', 1000, 300, 'Bombardier', 2);

-- e
INSERT INTO airlinestaff VALUES('johndoe', 'password', 'John', 'Doe', '1980-1-1', 'Jet Blue');
INSERT INTO staffemail VALUES('johndoe', 'johndoe@jetblue.com');
INSERT INTO staffphone VALUES('johndoe', '000000');

-- f
INSERT INTO flight VALUES('Jet Blue', 'J1', '2022-11-03', '09:30:00', '2022-11-04', '1:30:00', '100', 'On Time', 'JFK', 'PVG', '1002', NULL, NULL, NULL);
INSERT INTO flight VALUES('Jet Blue', 'P2', '2022-12-24', '09:30:00', '2022-12-25', '1:30:00', '100', 'On Time', 'PVG', 'JFK', '1000', NULL, NULL, NULL);
INSERT INTO flight VALUES('Jet Blue', 'J2', '2022-12-23', '09:30:00', '2022-12-24', '1:30:00', '100', 'On Time', 'JFK', 'PVG', '1000', 'P2', '2022-12-24', '09:30:00');
INSERT INTO flight VALUES('Jet Blue', 'J3', '2022-12-25', '09:30:00', '2022-12-26', '1:30:00', '100', 'Delayed', 'JFK', 'PVG', '1001', NULL, NULL, NULL);

-- g
INSERT INTO ticket VALUES('J2-0', 'J2', '2022-12-23', '09:30:00', 'Jet Blue', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO ticket VALUES('J2-1', 'J2', '2022-12-23', '09:30:00', 'Jet Blue', 'mahmoud@airlinecustomer.com', 150, 'Credit', '000000', 'DUMMY', '2023-12-31', '2022-11-4', '09:30:00');
INSERT INTO ticket VALUES('J2-2', 'J2', '2022-12-23', '09:30:00', 'Jet Blue', 'jeff@airlinecustomer.com', 150, 'Credit', '000000', 'DUMMY', '2023-12-31', '2022-11-2', '09:30:00');
INSERT INTO ticket VALUES('J2-3', 'J2', '2022-12-23', '09:30:00', 'Jet Blue', 'kenny@airlinecustomer.com', 150, 'Credit', '000000', 'DUMMY', '2023-12-31', '2022-10-31', '09:30:00');
INSERT INTO ticket VALUES('P2-0', 'P2', '2022-12-24', '09:30:00', 'Jet Blue', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO ticket VALUES('P2-1', 'P2', '2022-12-24', '09:30:00', 'Jet Blue', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
