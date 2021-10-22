DROP TABLE IF EXISTS `order_form`;
CREATE TABLE `order_form`(
`order_id` int(8) NOT NULL AUTO_INCREMENT,
`dormitory_id` int(8) DEFAULT NULL,
`water_brand` varchar(8) DEFAULT NULL,
`water_number` int(1) DEFAULT NULL,
`create_time` datetime DEFAULT NULL,
`preset_day` date DEFAULT NULL,
`preset_time` varchar(8) DEFAULT NULL,
PRIMARY KEY(`order_id`),
FOREIGN KEY(`dormitory_id`) REFERENCES dormitory(dormitory_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
