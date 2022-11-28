CREATE TABLE `airline` (
  `airline_name` varchar(255) NOT NULL,
   PRIMARY KEY(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airlinestaff` (
  `username` varchar(36) NOT NULL,
  `password` varchar(255) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(255) NOT NULL,
   PRIMARY KEY(`username`),
   FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airplane` (
  `airline_name` varchar(255) NOT NULL,
  `airplane_id` varchar(36) NOT NULL,
  `num_seats` int UNSIGNED NOT NULL,
  `manufacturing_comp` varchar(50) NOT NULL,
  `age` int UNSIGNED NOT NULL,
   PRIMARY KEY(`airline_name`, `airplane_id`),
   FOREIGN KEY(`airline_name`) REFERENCES `airline`(`airline_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `airport` (
  `airport_name` varchar(255) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `type` varchar(13) check (type in ('Domestic', 'International', 'Both')),
   PRIMARY KEY(`airport_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `customer` (
  `customer_email` varchar(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `building_num` int NOT NULL,
  `street` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `phone_num` varchar(20) NOT NULL,
  `passport_num` varchar(50) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
   PRIMARY KEY(`customer_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `flight` (
  `airline_name` varchar(255) NOT NULL,
  `flight_num` varchar(36) NOT NULL,
  `flight_dept_date` date NOT NULL,
  `flight_dept_time` time NOT NULL,
  `flight_arrival_date` date NOT NULL,
  `flight_arrival_time` time NOT NULL,
  `base_price` decimal(8,2) NOT NULL,
  `status` enum('On Time', 'Delayed', 'Cancelled') NOT NULL,
  `dept_airport_name` varchar(255) NOT NULL,
  `arrival_airport_name` varchar(255) NOT NULL,
  `airplane_id` varchar(36) NOT NULL,
  `return_flight_num` varchar(36),
  `return_flight_date` date,
  `return_flight_time` time,
   PRIMARY KEY(`airline_name`, `flight_num`, `flight_dept_date`, `flight_dept_time`),
   FOREIGN KEY(`airline_name`, `airplane_id`) REFERENCES `airplane`(`airline_name`, `airplane_id`),
   FOREIGN KEY(`dept_airport_name`) REFERENCES `airport`(`airport_name`),
   FOREIGN KEY(`arrival_airport_name`) REFERENCES `airport`(`airport_name`),
   FOREIGN KEY(`airline_name`,`return_flight_num`, `return_flight_date`, `return_flight_time`) REFERENCES `flight`(`airline_name`,`flight_num`,`flight_dept_date`,`flight_dept_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `review` (
  `customer_email` varchar(255) NOT NULL,
  `airline_name` varchar(255) NOT NULL,
  `flight_num` varchar(36) NOT NULL,
  `flight_dept_date` date NOT NULL,
  `flight_dept_time` time NOT NULL,
  `rating` decimal(1,0) NOT NULL CHECK (`rating` >= 0 and `rating` <= 5),
  `comments` varchar(500),
   PRIMARY KEY(`customer_email`, `airline_name`, `flight_num`, `flight_dept_date`, `flight_dept_time`),
   FOREIGN KEY(`customer_email`) REFERENCES `customer`(`customer_email`),
   FOREIGN KEY(`airline_name`,`flight_num`, `flight_dept_date`, `flight_dept_time`) REFERENCES `flight`(`airline_name`,`flight_num`,`flight_dept_date`,`flight_dept_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `staffemail` (
  `username` varchar(36) NOT NULL,
  `email` varchar(255) NOT NULL,
   PRIMARY KEY(`username`, `email`),
   FOREIGN KEY(`username`) REFERENCES `airlinestaff`(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `staffphone` (
  `username` varchar(36) NOT NULL,
  `phone` varchar(20) NOT NULL,
   PRIMARY KEY(`username`, `phone`),
   FOREIGN KEY(`username`) REFERENCES `airlinestaff`(`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `ticket` (
  `ticket_id` varchar(36) NOT NULL,
  `flight_num` varchar(36) NOT NULL,
  `flight_dept_date` date NOT NULL,
  `flight_dept_time` time NOT NULL,
  `airline_name` varchar(20) NOT NULL,
  `customer_email` varchar(255),
  `sold_price` decimal(8,2),
  `card_type` enum('Credit', 'Debit'),
  `card_num` varchar(16),
  `card_name` varchar(36),
  `card_expiration_date` date,
  `purchase_date` date,
  `purchase_time` time,
   PRIMARY KEY(`ticket_id`),
   FOREIGN KEY(`airline_name`, `flight_num`, `flight_dept_date`, `flight_dept_time`) REFERENCES `flight`(`airline_name`, `flight_num`, `flight_dept_date`, `flight_dept_time`),
   FOREIGN KEY(`customer_email`) REFERENCES `customer`(`customer_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;