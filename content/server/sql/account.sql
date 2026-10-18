CREATE DATABASE IF NOT EXISTS account;
USE account;

-- src: game/src/input_auth.cpp:129-155, game/src/db.cpp:272-460, game/src/messenger_manager.cpp:762, game/src/char.cpp:2500,2513,12424-12437,12483,12868, db/src/ClientManager.cpp:3434,3436,3455,3717,3752
-- UNSURE: language default 1 (LOCALE_EN); the value read here is ignored on login, the client-sent language is written back instead.
CREATE TABLE IF NOT EXISTS `account` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(30) NOT NULL,
  `password` VARCHAR(45) NOT NULL DEFAULT '',
  `social_id` VARCHAR(18) NOT NULL DEFAULT '',
  `status` VARCHAR(8) NOT NULL DEFAULT 'OK',
  `language` TINYINT UNSIGNED NOT NULL DEFAULT 1,
  `availDt` DATETIME NULL DEFAULT NULL,
  `create_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_play` DATETIME NULL DEFAULT NULL,
  `silver_expire` DATETIME NULL DEFAULT NULL,
  `gold_expire` DATETIME NULL DEFAULT NULL,
  `safebox_expire` DATETIME NULL DEFAULT NULL,
  `autoloot_expire` DATETIME NULL DEFAULT NULL,
  `fish_mind_expire` DATETIME NULL DEFAULT NULL,
  `marriage_fast_expire` DATETIME NULL DEFAULT NULL,
  `money_drop_rate_expire` DATETIME NULL DEFAULT NULL,
  `cash` INT NOT NULL DEFAULT 0,
  `mileage` INT NOT NULL DEFAULT 0,
  `coins` BIGINT NOT NULL DEFAULT 0,
  `jcoins` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create an account; login compares `password` with PASSWORD('<client password>') (41-char '*HEX' hash):
-- INSERT INTO `account` (`login`, `password`, `social_id`) VALUES ('myuser', PASSWORD('changeme'), '1234567');
