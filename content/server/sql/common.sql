CREATE DATABASE IF NOT EXISTS common;
USE common;

-- src: game/src/config.cpp:493,552,592, db/src/ClientManager.cpp:3149
-- UNSURE: mKey is declared UNIQUE; config.cpp:592 orders by CAST(mValue AS unsigned) as if several rows per key could exist, but only the first row is ever read.
CREATE TABLE IF NOT EXISTS `locale` (
  `mKey` VARCHAR(32) NOT NULL,
  `mValue` VARCHAR(255) NOT NULL DEFAULT '',
  UNIQUE KEY `mKey` (`mKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:3190, game/src/messenger_manager.cpp:53, game/src/char.cpp:10069,12868,12905
-- UNSURE: mLanguage / mSecondLanguage are read as "col+0" (suggests ENUM in the original); TINYINT holding an ELocale value (0..11) works the same. mSecondLanguage 12 (LOCALE_MAX_NUM) means "no second flag".
CREATE TABLE IF NOT EXISTS `gmlist` (
  `mID` INT NOT NULL AUTO_INCREMENT,
  `mAccount` VARCHAR(30) NOT NULL DEFAULT '',
  `mName` VARCHAR(32) NOT NULL DEFAULT '',
  `mContactIP` VARCHAR(15) NOT NULL DEFAULT '',
  `mServerIP` VARCHAR(15) NOT NULL DEFAULT 'ALL',
  `mAuthority` ENUM('IMPLEMENTOR','GOD','HIGH_WIZARD','LOW_WIZARD','WIZARD') NOT NULL DEFAULT 'LOW_WIZARD',
  `mIDAccount` INT UNSIGNED NOT NULL DEFAULT 0,
  `mLanguage` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `mSecondLanguage` TINYINT UNSIGNED NOT NULL DEFAULT 12,
  PRIMARY KEY (`mID`),
  UNIQUE KEY `mName` (`mName`),
  KEY `mAccount` (`mAccount`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:3245
CREATE TABLE IF NOT EXISTS `gmhost` (
  `mIP` VARCHAR(15) NOT NULL,
  PRIMARY KEY (`mIP`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/db.cpp:771,777
-- UNSURE: `type` is only ever filtered with 'SPAM'; other values and word length limit are guesses.
CREATE TABLE IF NOT EXISTS `spam_db` (
  `type` VARCHAR(8) NOT NULL DEFAULT 'SPAM',
  `word` VARCHAR(255) NOT NULL,
  `score` INT NOT NULL DEFAULT 10,
  PRIMARY KEY (`type`, `word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- UNSURE: SKILL_POWER_BY_LEVEL is the standard 41-value table (SKILL_MAX_LEVEL + 1) from memory; per-job SKILL_POWER_BY_LEVEL_TYPE0..7 rows are optional (game falls back to this one).
INSERT IGNORE INTO `locale` (`mKey`, `mValue`) VALUES
  ('LOCALE', 'europe'),
  ('SKILL_POWER_BY_LEVEL', '0 5 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 50 52 54 56 58 60 63 66 69 72 82 85 88 91 94 98 102 106 110 115 125');

-- No GM is seeded: a guessable placeholder row would hand IMPLEMENTOR to whoever registers that login/name.
-- After creating your own account and character, run (mIDAccount = account.id, needed by the language-flag join):
-- INSERT INTO `gmlist` (`mAccount`, `mName`, `mContactIP`, `mServerIP`, `mAuthority`, `mIDAccount`)
-- VALUES ('<your_login>', '<your_char>', '', 'ALL', 'IMPLEMENTOR', <your_account_id>);

INSERT IGNORE INTO `gmhost` (`mIP`) VALUES ('127.0.0.1');
