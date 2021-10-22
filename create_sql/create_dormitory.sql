DROP TABLE IF EXISTS `dormitory`;
CREATE TABLE `dormitory`(
`dormitory_id` int(8) NOT NULL AUTO_INCREMENT,
`school_name` varchar(50) DEFAULT NULL,
`dormitory_number` varchar(8) DEFAULT NULL,
`room_number` varchar(8) DEFAULT NULL,
`email` varchar(20) DEFAULT NULL,
`password` varchar(20) DEFAULT NULL,
`banlance` int(8) DEFAULT 0,
`statistic` int(8) DEFAULT 0,
PRIMARY KEY(`dormitory_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
