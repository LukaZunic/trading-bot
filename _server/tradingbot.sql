CREATE DATABASE IF NOT EXISTS `tradingbot` 
USE `tradingbot`;

CREATE TABLE IF NOT EXISTS `order` (
  `timestamp` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `wallet` (
  `name` varchar(50) DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
