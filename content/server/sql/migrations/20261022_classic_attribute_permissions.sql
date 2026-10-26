-- Close 14 non-classic random attributes in all normal/costume equipment sets.
-- Preserve natural item addons, prototype bonuses, existing items and rare pool.
-- Requires a backup and all 14 source rows. Run WITHOUT --force.
-- Refresh all game cores through GM /reload p after the database update.
USE player;
CREATE TEMPORARY TABLE classic_attribute_block_20261022 (
  `apply` varchar(64) NOT NULL PRIMARY KEY
);
INSERT INTO classic_attribute_block_20261022 VALUES
('DEF_GRADE_BONUS'),
('SKILL_DAMAGE_BONUS'),
('NORMAL_HIT_DAMAGE_BONUS'),
('SKILL_DEFEND_BONUS'),
('NORMAL_HIT_DEFEND_BONUS'),
('ATTBONUS_WARRIOR'),
('ATTBONUS_ASSASSIN'),
('ATTBONUS_SURA'),
('ATTBONUS_SHAMAN'),
('RESIST_WARRIOR'),
('RESIST_ASSASSIN'),
('RESIST_SURA'),
('RESIST_SHAMAN'),
('ATTBONUS_MONSTER');
CREATE TEMPORARY TABLE classic_attribute_guard_20261022 (
  `valid` tinyint NOT NULL CHECK (`valid` = 1)
);
INSERT INTO classic_attribute_guard_20261022
SELECT COUNT(*) = 14 AND COUNT(DISTINCT a.`apply`) = 14
FROM item_attr AS a
JOIN classic_attribute_block_20261022 AS b ON a.`apply` = b.`apply`;
START TRANSACTION;
UPDATE item_attr AS a
JOIN classic_attribute_block_20261022 AS b ON a.`apply` = b.`apply`
SET a.weapon=0, a.body=0, a.wrist=0, a.foots=0, a.neck=0, a.head=0,
    a.shield=0, a.ear=0, a.pendant=0,
    a.costume_body=0, a.costume_hair=0, a.costume_weapon=0;
COMMIT;
DROP TEMPORARY TABLE classic_attribute_guard_20261022;
DROP TEMPORARY TABLE classic_attribute_block_20261022;
