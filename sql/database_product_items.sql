-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: database
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `product_items`
--

DROP TABLE IF EXISTS `product_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_items` (
  `product_id` int NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity_sold` int NOT NULL,
  `revenue` decimal(15,2) NOT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_items`
--

LOCK TABLES `product_items` WRITE;
/*!40000 ALTER TABLE `product_items` DISABLE KEYS */;
INSERT INTO `product_items` VALUES (1,'Капучино 300мл',450,81000.00),(2,'Латте 400мл',420,84000.00),(3,'Американо 200мл',350,49000.00),(4,'Фильтр-кофе 250мл',310,46500.00),(5,'Эспрессо 30мл',280,33600.00),(6,'Флэт Уайт 200мл',240,48000.00),(7,'Раф Кофе 300мл',210,52500.00),(8,'Матча Латте 350мл',190,47500.00),(9,'Какао с маршмеллоу 300мл',150,30000.00),(10,'Горячий шоколад 200мл',90,19800.00),(11,'Американо 300мл',310,49600.00),(12,'Капучино 400мл',260,57200.00),(13,'Айс Латте 400мл',180,39600.00),(14,'Бамбл Кофе 350мл',120,32400.00),(15,'Эспрессо-Тоник 250мл',140,35000.00),(16,'Чай Эрл Грей 400мл',95,14250.00),(17,'Чай Ягодный микс 400мл',115,20700.00),(18,'Авторский Раф Лаванда 300мл',85,22100.00),(19,'Сироп в ассортименте (порция)',530,26500.00),(20,'Альтернативное молоко (порция)',380,22800.00);
/*!40000 ALTER TABLE `product_items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-15 22:36:46
