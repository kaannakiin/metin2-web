-- Standard 1-5 attributes: classic equipment permissions, fixed values, HP 3000.
-- After applying, refresh every game core via the existing GM /reload p path
-- (which also reloads other prototype tables), or a coordinated maintenance
-- restart of game/db. A DB update alone does not refresh in-memory attributes.
-- Back up player.item_attr first. Do not use seed_item_attr.sql on a live DB:
-- that bootstrap seed deletes/recreates both normal and rare pools.
-- Existing player.item rows, rare attributes, deferred rows, selection weights,
-- pendant and costume permissions are not updated. Fixed values are shared by
-- all enabled sets, including pendant and costumes (explicit user decision).
-- Run with mysql/mariadb WITHOUT --force so a failed preflight aborts execution.

USE player;

CREATE TEMPORARY TABLE normal_attribute_patch_20261022 (
  `apply` varchar(64) NOT NULL PRIMARY KEY,
  `fixed_value` smallint NOT NULL,
  `weapon` tinyint unsigned NOT NULL,
  `body` tinyint unsigned NOT NULL,
  `wrist` tinyint unsigned NOT NULL,
  `foots` tinyint unsigned NOT NULL,
  `neck` tinyint unsigned NOT NULL,
  `head` tinyint unsigned NOT NULL,
  `shield` tinyint unsigned NOT NULL,
  `ear` tinyint unsigned NOT NULL
);

INSERT INTO normal_attribute_patch_20261022 VALUES
  ('MAX_HP', 3000, 0, 5, 5, 5, 5, 0, 0, 0),
  ('MAX_SP', 80, 0, 5, 5, 5, 5, 0, 0, 0),
  ('CON', 12, 5, 0, 0, 0, 0, 0, 5, 0),
  ('INT', 12, 5, 0, 0, 0, 0, 0, 5, 0),
  ('STR', 12, 5, 0, 0, 0, 0, 0, 5, 0),
  ('DEX', 12, 5, 0, 0, 0, 0, 0, 5, 0),
  ('ATT_SPEED', 8, 0, 0, 0, 5, 0, 5, 0, 0),
  ('MOV_SPEED', 20, 0, 0, 0, 0, 0, 0, 0, 5),
  ('CAST_SPEED', 20, 5, 5, 0, 0, 0, 0, 0, 0),
  ('HP_REGEN', 30, 0, 0, 0, 0, 5, 5, 0, 0),
  ('SP_REGEN', 30, 0, 0, 0, 0, 5, 5, 0, 0),
  ('POISON_PCT', 8, 5, 0, 0, 0, 0, 5, 0, 0),
  ('STUN_PCT', 8, 5, 0, 0, 5, 5, 0, 0, 0),
  ('SLOW_PCT', 8, 5, 0, 0, 5, 0, 0, 0, 0),
  ('CRITICAL_PCT', 10, 5, 0, 0, 5, 5, 0, 0, 0),
  ('PENETRATE_PCT', 10, 5, 0, 5, 0, 5, 0, 0, 0),
  ('ATTBONUS_HUMAN', 10, 5, 0, 5, 0, 0, 5, 5, 5),
  ('ATTBONUS_ANIMAL', 20, 5, 0, 5, 0, 0, 5, 5, 5),
  ('ATTBONUS_ORC', 20, 5, 0, 5, 0, 0, 5, 5, 5),
  ('ATTBONUS_MILGYO', 20, 5, 0, 5, 0, 0, 5, 5, 5),
  ('ATTBONUS_UNDEAD', 20, 5, 0, 5, 0, 0, 5, 5, 5),
  ('ATTBONUS_DEVIL', 20, 5, 0, 5, 0, 0, 5, 5, 5),
  ('STEAL_HP', 10, 0, 5, 5, 0, 0, 0, 0, 0),
  ('STEAL_SP', 10, 0, 5, 0, 0, 5, 5, 0, 0),
  ('MANA_BURN_PCT', 10, 0, 0, 5, 0, 5, 0, 0, 5),
  ('BLOCK', 15, 0, 0, 0, 0, 0, 0, 5, 0),
  ('DODGE', 15, 0, 0, 0, 5, 0, 5, 0, 0),
  ('RESIST_SWORD', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_TWOHAND', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_DAGGER', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_BELL', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_FAN', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_BOW', 15, 0, 5, 0, 5, 5, 0, 0, 5),
  ('RESIST_FIRE', 15, 0, 5, 5, 0, 0, 5, 0, 0),
  ('RESIST_ELEC', 15, 0, 5, 5, 0, 0, 5, 0, 0),
  ('RESIST_MAGIC', 15, 0, 5, 5, 0, 0, 5, 0, 0),
  ('RESIST_WIND', 15, 0, 5, 5, 0, 0, 5, 0, 0),
  ('REFLECT_MELEE', 10, 0, 5, 0, 0, 0, 0, 5, 0),
  ('POISON_REDUCE', 5, 0, 0, 0, 0, 0, 0, 0, 5),
  ('EXP_DOUBLE_BONUS', 20, 0, 0, 0, 5, 5, 0, 5, 0),
  ('GOLD_DOUBLE_BONUS', 20, 0, 0, 0, 5, 5, 0, 5, 0),
  ('ITEM_DROP_BONUS', 20, 0, 0, 5, 0, 0, 0, 0, 5),
  ('IMMUNE_STUN', 1, 0, 0, 0, 0, 0, 0, 1, 0),
  ('IMMUNE_SLOW', 1, 0, 0, 0, 0, 0, 0, 1, 0),
  ('ATT_GRADE_BONUS', 50, 0, 5, 0, 0, 0, 0, 0, 0);

-- Fail before UPDATE if a target row is missing or duplicated. The CHECK is
-- enforced on the project's MariaDB; this is not a MySQL 5.x migration.
CREATE TEMPORARY TABLE normal_attribute_guard_20261022 (
  `valid` tinyint NOT NULL CHECK (`valid` = 1)
);
INSERT INTO normal_attribute_guard_20261022
SELECT IF(COUNT(*) = 45 AND COUNT(DISTINCT a.`apply`) = 45, 1, 0)
FROM item_attr AS a
JOIN normal_attribute_patch_20261022 AS p ON a.`apply` = p.`apply`;

START TRANSACTION;
UPDATE item_attr AS a
JOIN normal_attribute_patch_20261022 AS p ON a.`apply` = p.`apply`
SET a.lv1 = p.fixed_value, a.lv2 = p.fixed_value,
    a.lv3 = p.fixed_value, a.lv4 = p.fixed_value, a.lv5 = p.fixed_value,
    a.weapon = p.weapon, a.body = p.body, a.wrist = p.wrist,
    a.foots = p.foots, a.neck = p.neck, a.head = p.head,
    a.shield = p.shield, a.ear = p.ear;
COMMIT;

DROP TEMPORARY TABLE normal_attribute_guard_20261022;
DROP TEMPORARY TABLE normal_attribute_patch_20261022;
