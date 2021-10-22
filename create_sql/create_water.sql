DROP TABLE IF EXISTS `water`;
CREATE TABLE `water`(
`water_id` int(4) NOT NULL,
`water_brand` varchar(16) DEFAULT NULL,
`water_price` int(4) DEFAULT NULL,
`water_stock` int(4) DEFAULT NULL,
PRIMARY KEY(`water_id`)

) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO water VALUES (1,'娃哈哈',12,100);
INSERT INTO water VALUES (2,'国星',10,100);
INSERT INTO water VALUES (3,'水状元',8,100);
