-- MySQL Script generated by MySQL Workbench
-- 2020年03月15日 星期日 13时16分02秒
-- Model: New Model Version: 1.0
-- MySQL Workbench Forward Engineering

-- -----------------------------------------------------
-- Table Country
-- -----------------------------------------------------
CREATE TABLE Country (
  id SERIAL NOT NULL,
  code VARCHAR(2) NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code),
  UNIQUE (name)
);


-- -----------------------------------------------------
-- Table City
-- -----------------------------------------------------
CREATE TABLE City (
  id SERIAL NOT NULL,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  country_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code, country_id),
  FOREIGN KEY (country_id) REFERENCES Country (id)
);


-- -----------------------------------------------------
-- Table Station
-- -----------------------------------------------------
CREATE TABLE Station (
  id SERIAL NOT NULL,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  city_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code, city_id),
  FOREIGN KEY (city_id) REFERENCES City (id)
);


-- -----------------------------------------------------
-- Table Customer
-- -----------------------------------------------------
CREATE TABLE Customer (
  id SERIAL NOT NULL,
  id_card VARCHAR(20) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  nick_name VARCHAR(20) NULL,
  phone_number VARCHAR(20) NOT NULL,
  city_id BIGINT NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (id_card),
  UNIQUE (phone_number),
  FOREIGN KEY (city_id) REFERENCES City (id)
);


-- -----------------------------------------------------
-- Table TrainLine
-- -----------------------------------------------------
CREATE TABLE TrainLine (
  id SERIAL NOT NULL,
  name VARCHAR(50) NOT NULL,
  depart_station BIGINT NOT NULL,
  arrive_station BIGINT NOT NULL,
  depart_time TIMESTAMP NOT NULL,
  arrive_time TIMESTAMP NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (name)
);


-- -----------------------------------------------------
-- Table Train
-- -----------------------------------------------------
CREATE TABLE Train (
  id SERIAL NOT NULL,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code)
);


-- -----------------------------------------------------
-- Table Seat
-- -----------------------------------------------------
CREATE TABLE Seat (
  id SERIAL NOT NULL,
  code VARCHAR(20) NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (code)
);


-- -----------------------------------------------------
-- Table Ticket
-- -----------------------------------------------------
CREATE TABLE Ticket (
  id SERIAL NOT NULL,
  train_id BIGINT NOT NULL,
  customer_id BIGINT NOT NULL,
  train_line_id BIGINT NOT NULL,
  from_station_id BIGINT NOT NULL,
  to_station_id BIGINT NOT NULL,
  seat_id BIGINT NOT NULL,
  seat_position BIGINT NOT NULL,
  price INT NOT NULL,
  date TIMESTAMP NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (from_station_id) REFERENCES Station (id),
  FOREIGN KEY (to_station_id) REFERENCES Station (id),
  FOREIGN KEY (customer_id) REFERENCES Customer (id),
  FOREIGN KEY (train_line_id) REFERENCES TrainLine (id),
  FOREIGN KEY (train_id) REFERENCES Train (id),
  FOREIGN KEY (seat_id) REFERENCES Seat (id)
);


-- -----------------------------------------------------
-- Table OrderForm
-- -----------------------------------------------------
CREATE TABLE OrderForm (
  customer_id BIGINT NOT NULL,
  ticket_id BIGINT NOT NULL,
  status INT NOT NULL,
  create_date TIMESTAMP NOT NULL,
  PRIMARY KEY (customer_id, ticket_id),
  FOREIGN KEY (customer_id) REFERENCES Customer (id),
  FOREIGN KEY (ticket_id) REFERENCES Ticket (id)
);


-- -----------------------------------------------------
-- Table TrainLineStation
-- -----------------------------------------------------
CREATE TABLE TrainLineStation (
  train_line_id BIGINT NOT NULL,
  station_id BIGINT NOT NULL,
  arrive_time TIMESTAMP NOT NULL,
  PRIMARY KEY (train_line_id, station_id),
  FOREIGN KEY (train_line_id) REFERENCES TrainLine (id),
  FOREIGN KEY (station_id) REFERENCES Station (id)
);


-- -----------------------------------------------------
-- Table TrainSeat
-- -----------------------------------------------------
CREATE TABLE TrainSeat (
  train_id BIGINT NOT NULL,
  seat_id BIGINT NOT NULL,
  seat_count INT NOT NULL,
  PRIMARY KEY (train_id, seat_id),
  FOREIGN KEY (train_id) REFERENCES Train (id),
  FOREIGN KEY (seat_id) REFERENCES Seat (id)
);