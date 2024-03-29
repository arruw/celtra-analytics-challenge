DROP TABLE IF EXISTS `agg_daily`;

CREATE TABLE `agg_daily` (
  `date` date NOT NULL,
  `id_campaign` int(10) unsigned NOT NULL,
  `id_ad` int(10) unsigned NOT NULL,
  `impressions` bigint(20) NOT NULL,
  `interactions` bigint(20) NOT NULL,
  `clicks` bigint(20) NOT NULL,
  `uniqueUsers` bigint(20) NOT NULL,
  `swipes` bigint(20) NOT NULL,
  `pinches` bigint(20) NOT NULL,
  `touches` bigint(20) NOT NULL,
  PRIMARY KEY (`date`,`id_campaign`,`id_ad`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
