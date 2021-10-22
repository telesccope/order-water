DROP TABLE IF EXISTS `linkman`;
CREATE TABLE `linkman`(
`dormitory_id` int(8) NOT NULL,
`linkman_id` int(8) NOT NULL AUTO_INCREMENT,
`linkman_name` varchar(16) DEFAULT NULL,
`linkman_email` varchar(20) DEFAULT NULL,
PRIMARY KEY(`linkman_id`),
FOREIGN KEY(`dormitory_id`) REFERENCES dormitory(dormitory_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
