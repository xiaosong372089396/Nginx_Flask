
DROP TABLE IF EXISTS `asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sn` varchar(25) DEFAULT NULL,
  `ip` varchar(128) DEFAULT NULL,
  `hostname` varchar(30) DEFAULT NULL,
  `machine_room_id` varchar(25) DEFAULT NULL,
  `bussiness` varchar(25) DEFAULT NULL,
  `admin` varchar(25) DEFAULT NULL,
  `cpu` varchar(25) DEFAULT NULL,
  `ram` varchar(25) DEFAULT NULL,
  `disk` varchar(25) DEFAULT NULL,
  `os` varchar(25) DEFAULT NULL,
  `model` varchar(25) DEFAULT NULL,
  `purchase_date` varchar(30) DEFAULT NULL,
  `vendor` varchar(25) DEFAULT NULL,
  `status` varchar(25) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asset`
--

LOCK TABLES `asset` WRITE;
/*!40000 ALTER TABLE `asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moniter`
--

DROP TABLE IF EXISTS `moniter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `moniter` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `ip` varchar(128) NOT NULL DEFAULT '',
  `cpu` float DEFAULT NULL,
  `mem` float DEFAULT NULL,
  `disk` float DEFAULT NULL,
  `mtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moniter`
--

LOCK TABLES `moniter` WRITE;
/*!40000 ALTER TABLE `moniter` DISABLE KEYS */;
/*!40000 ALTER TABLE `moniter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(32) DEFAULT NULL,
  `password` varchar(32) DEFAULT NULL,
  `age` int(12) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `IPhone` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `webaccess2`
--

DROP TABLE IF EXISTS `webaccess2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `webaccess2` (
  `logdate` datetime DEFAULT NULL,
  `ip` varchar(32) DEFAULT NULL,
  `url` text,
  `code` int(11) DEFAULT NULL,
  `address` varchar(20) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `webaccess2`
--

LOCK TABLES `webaccess2` WRITE;
/*!40000 ALTER TABLE `webaccess2` DISABLE KEYS */;
/*!40000 ALTER TABLE `webaccess2` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-30 16:17:08
