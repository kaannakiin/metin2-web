CREATE DATABASE IF NOT EXISTS log;
USE log;

-- src: Source/Server/game/src/log.cpp:73, 98
CREATE TABLE IF NOT EXISTS log (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  type VARCHAR(16) NOT NULL DEFAULT '',
  time DATETIME NULL DEFAULT NULL,
  who INT UNSIGNED NOT NULL DEFAULT 0,
  x INT UNSIGNED NOT NULL DEFAULT 0,
  y INT UNSIGNED NOT NULL DEFAULT 0,
  what INT UNSIGNED NOT NULL DEFAULT 0,
  how VARCHAR(64) NOT NULL DEFAULT '',
  hint VARCHAR(512) NOT NULL DEFAULT '',
  ip VARCHAR(45) NOT NULL DEFAULT '',
  vnum INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_who (who)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:116
CREATE TABLE IF NOT EXISTS loginlog (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  type VARCHAR(8) NOT NULL DEFAULT '',
  time DATETIME NULL DEFAULT NULL,
  channel TINYINT UNSIGNED NOT NULL DEFAULT 0,
  account_id INT UNSIGNED NOT NULL DEFAULT 0,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  level INT NOT NULL DEFAULT 0,
  job TINYINT UNSIGNED NOT NULL DEFAULT 0,
  playtime INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:302, 307, 308
CREATE TABLE IF NOT EXISTS loginlog2 (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  type VARCHAR(8) NOT NULL DEFAULT 'INVALID',
  is_gm CHAR(1) NOT NULL DEFAULT 'N',
  login_time DATETIME NULL DEFAULT NULL,
  logout_time DATETIME NULL DEFAULT NULL,
  channel TINYINT UNSIGNED NOT NULL DEFAULT 0,
  account_id INT UNSIGNED NOT NULL DEFAULT 0,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  ip INT UNSIGNED NOT NULL DEFAULT 0,
  playtime TIME NULL DEFAULT NULL,
  PRIMARY KEY (id),
  KEY idx_account_pid (account_id, pid),
  KEY idx_login_time (login_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:137, 139 (INSERT without column list: time, type, vnum, gold)
CREATE TABLE IF NOT EXISTS money_log (
  time DATETIME NULL DEFAULT NULL,
  type TINYINT UNSIGNED NOT NULL DEFAULT 0,
  vnum INT UNSIGNED NOT NULL DEFAULT 0,
  gold BIGINT NOT NULL DEFAULT 0,
  KEY idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:147
CREATE TABLE IF NOT EXISTS hack_log (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  time DATETIME NULL DEFAULT NULL,
  login VARCHAR(30) NOT NULL DEFAULT '',
  name VARCHAR(48) NOT NULL DEFAULT '',
  ip VARCHAR(45) NOT NULL DEFAULT '',
  server VARCHAR(64) NOT NULL DEFAULT '',
  why VARCHAR(255) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  KEY idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:160
CREATE TABLE IF NOT EXISTS hack_crc_log (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  time DATETIME NULL DEFAULT NULL,
  login VARCHAR(30) NOT NULL DEFAULT '',
  name VARCHAR(48) NOT NULL DEFAULT '',
  ip VARCHAR(45) NOT NULL DEFAULT '',
  server VARCHAR(64) NOT NULL DEFAULT '',
  why VARCHAR(255) NOT NULL DEFAULT '',
  crc INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:202
CREATE TABLE IF NOT EXISTS goldlog (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  date DATE NULL DEFAULT NULL,
  time TIME NULL DEFAULT NULL,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  what INT UNSIGNED NOT NULL DEFAULT 0,
  how VARCHAR(32) NOT NULL DEFAULT '',
  hint VARCHAR(255) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  KEY idx_date (date),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:208
CREATE TABLE IF NOT EXISTS cube (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  x INT UNSIGNED NOT NULL DEFAULT 0,
  y INT UNSIGNED NOT NULL DEFAULT 0,
  item_vnum INT UNSIGNED NOT NULL DEFAULT 0,
  item_uid INT UNSIGNED NOT NULL DEFAULT 0,
  item_count INT NOT NULL DEFAULT 0,
  success TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:320
CREATE TABLE IF NOT EXISTS acce (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  x INT UNSIGNED NOT NULL DEFAULT 0,
  y INT UNSIGNED NOT NULL DEFAULT 0,
  item_vnum INT UNSIGNED NOT NULL DEFAULT 0,
  item_uid INT UNSIGNED NOT NULL DEFAULT 0,
  item_count INT NOT NULL DEFAULT 0,
  item_abs_chance INT NOT NULL DEFAULT 0,
  success TINYINT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:214
CREATE TABLE IF NOT EXISTS speed_hack (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  x INT UNSIGNED NOT NULL DEFAULT 0,
  y INT UNSIGNED NOT NULL DEFAULT 0,
  hack_count INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:220
CREATE TABLE IF NOT EXISTS change_name (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  old_name VARCHAR(48) NOT NULL DEFAULT '',
  new_name VARCHAR(48) NOT NULL DEFAULT '',
  time DATETIME NULL DEFAULT NULL,
  ip VARCHAR(45) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:248
-- UNSURE: server is always inserted as literal 999; port receives the channel number.
CREATE TABLE IF NOT EXISTS command_log (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  userid INT UNSIGNED NOT NULL DEFAULT 0,
  server INT NOT NULL DEFAULT 0,
  ip VARCHAR(45) NOT NULL DEFAULT '',
  port INT UNSIGNED NOT NULL DEFAULT 0,
  username VARCHAR(48) NOT NULL DEFAULT '',
  command VARCHAR(512) NOT NULL DEFAULT '',
  date DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (id),
  KEY idx_date (date),
  KEY idx_userid (userid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:256
CREATE TABLE IF NOT EXISTS refinelog (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  item_name VARCHAR(64) NOT NULL DEFAULT '',
  item_id INT UNSIGNED NOT NULL DEFAULT 0,
  step INT NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  is_success TINYINT NOT NULL DEFAULT 0,
  setType VARCHAR(32) NOT NULL DEFAULT '',
  PRIMARY KEY (id),
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:265 (INSERT without column list: time, channel, empire, text)
CREATE TABLE IF NOT EXISTS shout_log (
  time DATETIME NULL DEFAULT NULL,
  channel TINYINT UNSIGNED NOT NULL DEFAULT 0,
  empire TINYINT UNSIGNED NOT NULL DEFAULT 0,
  text VARCHAR(512) NOT NULL DEFAULT '',
  KEY idx_time (time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:277
-- UNSURE: the code uses REPLACE INTO; with this PK/KEY layout it behaves as a plain INSERT (history per level-up). Add UNIQUE (pid, level) if one row per level is wanted.
CREATE TABLE IF NOT EXISTS levellog (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(48) NOT NULL DEFAULT '',
  level INT UNSIGNED NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  account_id INT UNSIGNED NOT NULL DEFAULT 0,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  playtime INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:282
CREATE TABLE IF NOT EXISTS bootlog (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  time DATETIME NULL DEFAULT NULL,
  hostname VARCHAR(64) NOT NULL DEFAULT '',
  channel TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:287 (INSERT without column list: time, pid, prob_idx, fish_id, fish_level, milliseconds, vnum, value)
CREATE TABLE IF NOT EXISTS fish_log (
  time DATETIME NULL DEFAULT NULL,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  prob_idx INT NOT NULL DEFAULT 0,
  fish_id INT UNSIGNED NOT NULL DEFAULT 0,
  fish_level INT NOT NULL DEFAULT 0,
  milliseconds INT UNSIGNED NOT NULL DEFAULT 0,
  vnum INT UNSIGNED NOT NULL DEFAULT 0,
  value INT UNSIGNED NOT NULL DEFAULT 0,
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:292 (INSERT without column list: quest_name, pid, level, type, value1, value2, time; type is the literal 2)
CREATE TABLE IF NOT EXISTS quest_reward_log (
  quest_name VARCHAR(64) NOT NULL DEFAULT '',
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  level INT UNSIGNED NOT NULL DEFAULT 0,
  type INT NOT NULL DEFAULT 0,
  value1 INT NOT NULL DEFAULT 0,
  value2 INT NOT NULL DEFAULT 0,
  time DATETIME NULL DEFAULT NULL,
  KEY idx_time (time),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:314 (INSERT without column list: guild_id, vnum, start_time, end_time)
CREATE TABLE IF NOT EXISTS dragon_slay_log (
  guild_id INT UNSIGNED NOT NULL DEFAULT 0,
  vnum INT UNSIGNED NOT NULL DEFAULT 0,
  start_time DATETIME NULL DEFAULT NULL,
  end_time DATETIME NULL DEFAULT NULL,
  KEY idx_end_time (end_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:327
-- UNSURE: id is caller-supplied (DWORD), so it is indexed but neither unique nor auto-increment.
CREATE TABLE IF NOT EXISTS wheel_of_fortune (
  id INT UNSIGNED NOT NULL DEFAULT 0,
  pid INT UNSIGNED NOT NULL DEFAULT 0,
  mapindex INT NOT NULL DEFAULT 0,
  x INT NOT NULL DEFAULT 0,
  y INT NOT NULL DEFAULT 0,
  price BIGINT NOT NULL DEFAULT 0,
  `when` DATETIME NULL DEFAULT NULL,
  KEY idx_id (id),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:334, Source/Server/game/src/soulroulette.cpp:17, 245, 256
CREATE TABLE IF NOT EXISTS soul_roulette_log (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(48) NOT NULL DEFAULT '',
  vnum INT NOT NULL DEFAULT 0,
  `count` INT NOT NULL DEFAULT 0,
  state VARCHAR(8) NOT NULL DEFAULT '',
  date DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (id),
  KEY idx_state (state)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: Source/Server/game/src/log.cpp:341
CREATE TABLE IF NOT EXISTS okay_event (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  pid INT NOT NULL DEFAULT 0,
  name VARCHAR(255) NOT NULL DEFAULT '',
  points INT NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  KEY idx_pid (pid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
