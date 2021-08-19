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
  `method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table tradingbot.order: ~3 rows (approximately)
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` (`timestamp`, `type`, `name`, `quantity`, `price`, `method`) VALUES
	('2021-04-28 19:32:46.172681', 'BUY', 'NKLA', 673.4006561022246, 14.850000381469727, 'MACD'),
	('2021-04-28 19:33:06.797453', 'SELL', 'NKLA', 673.4006561022246, 63.54999923706055, 'MACD'),
	('2021-04-28 19:34:39.596883', 'BUY', 'NKLA', 3470.7714068395208, 12.329999923706055, 'MACD');
/*!40000 ALTER TABLE `order` ENABLE KEYS */;

-- Dumping structure for table tradingbot.wallet
CREATE TABLE IF NOT EXISTS `wallet` (
  `name` varchar(50) DEFAULT NULL,
  `balance` double DEFAULT NULL,
  `quantity` double DEFAULT NULL,
  `method` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dumping data for table tradingbot.wallet: ~3 rows (approximately)
/*!40000 ALTER TABLE `wallet` DISABLE KEYS */;
INSERT INTO `wallet` (`name`, `balance`, `quantity`, `method`) VALUES
	('NKLA', 0, 0, 'MACD'),
	('NKLA', 10000, 0, 'ICHIMOKU CLOUD'),
	('NKLA', 10000, 0, 'BB & MACD');
/*!40000 ALTER TABLE `wallet` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
