DROP VIEW IF EXISTS `agg_view`;
CREATE VIEW `agg_view` AS 
WITH
agg AS
(SELECT
	DATE(i.date) AS `date`
    ,c.id AS `campaign_id`
    ,a.id AS `ad_id`
    ,c.name AS `campaign_name`
    ,a.name AS `ad_name`
    ,COUNT(*) AS `impressions`
    ,SUM(i.click) AS `clicks`
    ,SUM(i.swipe) AS `swipes`
    ,SUM(i.pinch) AS `pinches`
    ,SUM(i.touch) AS `touches`
    ,COUNT(DISTINCT i.id_user) AS `uniqueUsers`
FROM campaign AS c
INNER JOIN ad AS a ON a.id_campaign = c.id
INNER JOIN impression AS i ON i.id_ad = a.id
GROUP BY DATE(i.date), c.id, a.id
)
SELECT *, clicks+swipes+touches+pinches AS `interactions` FROM agg