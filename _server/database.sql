-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               10.4.17-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for tradingbot
CREATE DATABASE IF NOT EXISTS `tradingbot` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `tradingbot`;

-- Dumping structure for table tradingbot.order
CREATE TABLE IF NOT EXISTS `order` (
  `timestamp` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `price` double DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL,
  `wallet_id` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table tradingbot.order: ~14 rows (approximately)
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` (`timestamp`, `type`, `name`, `quantity`, `price`, `method`, `wallet_id`) VALUES
	('2021-05-08 00:53:54.636339', 'BUY', 'NKLA', 869.5652173913044, 11.5, 'MACD', 'wv63ci'),
	('2021-05-08 00:54:28.356998', 'BUY', 'NKLA', 869.5652173913044, 11.5, 'MACD', '2dxrkq'),
	('2021-08-15 19:43:54.046407', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 20:03:13.522605', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 20:36:08.424357', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 20:37:06.919048', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:04:54.217572', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:05:45.837990', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:17:34.378424', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:20:44.594469', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:22:42.900960', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:23:59.612628', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:24:53.910401', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:31:35.401854', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:35:09.548605', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2'),
	('2021-08-15 21:36:26.613975', 'BUY', 'DOGE-USD', 34116.53604792562, 0.29311299324035645, 'MACD', 'hdo1i2');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;

-- Dumping structure for table tradingbot.wallet
CREATE TABLE IF NOT EXISTS `wallet` (
  `id` varchar(50) DEFAULT NULL,
  `name` varchar(50) DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table tradingbot.wallet: ~9 rows (approximately)
/*!40000 ALTER TABLE `wallet` DISABLE KEYS */;
INSERT INTO `wallet` (`id`, `name`, `balance`, `quantity`, `method`) VALUES
	('g56f8a', 'NKLA', 10000, 0, 'ICHIMOKU CLOUD'),
	('18fpj', 'NKLA', 10000, 0, 'BB & MACD'),
	('wv63ci', 'NKLA', 0, 869.5652173913044, 'MACD'),
	('2dxrkq', 'NKLA', 0, 869.5652173913044, 'MACD'),
	('g2t18g', 'BTC-USD', 10000, 0, 'MACD'),
	('uenygb', 'BTC-USD', 10000, 0, 'MACD'),
	('60ixxs', 'BTC-USD', 10000, 0, 'MACD'),
	('r4tme8', 'BTC-USD', 10000, 0, 'MACD'),
	('yy54yf', 'BTC-USD', 10000, 0, 'MACD'),
	('dvyy0u', 'BTC-USD', 10000, 0, 'MACD'),
	('hdo1i2', 'DOGE-USD', 0, 34116.53604792562, 'MACD');
/*!40000 ALTER TABLE `wallet` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
