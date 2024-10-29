DROP TABLE IF EXISTS `timesheet`;
CREATE TABLE `timesheet` (
  `date` datetime NOT NULL,
  `date_of_run` varchar(45) NOT NULL,
  `time_of_run` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


DROP TABLE IF EXISTS `live`;
CREATE TABLE `live` (
  `date` datetime NOT NULL,
  `start_date` varchar(45) NOT NULL,
  `close_price_start` varchar(45) NOT NULL,
  `support` varchar(45) NOT NULL,
  `nearest_support` varchar(45) NOT NULL,
  `date_below_support` varchar(45) NOT NULL,
  `atr` varchar(45) NOT NULL,
  `entry` varchar(45) NOT NULL,
  `entry_date` varchar(45) NOT NULL,
  `Buy/Sell` varchar(45) NOT NULL,
  `sma_value` varchar(45) NOT NULL,
  `exit_date` varchar(45) NOT NULL,
  `Company` varchar(45) NOT NULL,
  `date_of_run` varchar(45) NOT NULL,
  `time_of_run` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;