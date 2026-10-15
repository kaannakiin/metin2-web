-- ============================================================================
-- player database schema (reconstructed from the C++ queries; no original dump exists)
--
-- Routing: db process SQL_PLAYER slot (default slot of CDBManager) and the game
-- channels' PLAYER_SQL (DBManager). On the auth server PLAYER_SQL points at the
-- `account` database instead, so account queries done there are NOT player tables.
-- Tables of the `account`, `common` and `log` databases are intentionally absent.
--
-- Feature flags assumed = those enabled in Source/Server/common/service.h
-- (ENABLE_NINETH_SKILL on, ENABLE_WOLFMAN_CHARACTER off, ENABLE_LEVEL_INT,
--  ENABLE_GOLD_LIMIT, ENABLE_STACK_LIMIT, ... all on).
--
-- SQL mode: the server sends INSERTs that omit columns, so every NOT NULL column
-- has a DEFAULT. Zero-dates ('0000-00-00') are used only in ishop_data; run the
-- server connection with a sql_mode that lacks NO_ZERO_DATE (MariaDB 10.6 default
-- is fine).
--
-- TABLE_POSTFIX is empty/blank in every conf, so all table names are unsuffixed.
-- ============================================================================
SET SQL_MODE='NO_ENGINE_SUBSTITUTION';

CREATE DATABASE IF NOT EXISTS `player` DEFAULT CHARACTER SET utf8mb4;
USE `player`;


-- ============================================================================
-- Characters / accounts
-- ============================================================================

-- src: db/src/ClientManagerPlayer.cpp:102 (UPDATE), :639 (SELECT), :1423 (INSERT); db/src/ClientManagerLogin.cpp:189, :453; db/src/ClientManagerOfflineshop.cpp:46, :367; game/src/char.cpp:12536, :12868; game/src/questlua_pc.cpp:2899
-- UNSURE: name is a plain (non-unique) index. player_deleted is created LIKE this table and receives
--         duplicates of a deleted name, and the code already checks uniqueness with COUNT(*).
CREATE TABLE IF NOT EXISTS `player` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `account_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(48) NOT NULL DEFAULT '',
  `ip` VARCHAR(15) NOT NULL DEFAULT '',
  `job` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `voice` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `dir` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `x` INT NOT NULL DEFAULT 0,
  `y` INT NOT NULL DEFAULT 0,
  `z` INT NOT NULL DEFAULT 0,
  `map_index` INT NOT NULL DEFAULT 0,
  `exit_x` INT NOT NULL DEFAULT 0,
  `exit_y` INT NOT NULL DEFAULT 0,
  `exit_map_index` INT NOT NULL DEFAULT 0,
  `hp` INT NOT NULL DEFAULT 0,
  `mp` INT NOT NULL DEFAULT 0,
  `stamina` INT NOT NULL DEFAULT 0,
  `random_hp` INT NOT NULL DEFAULT 0,
  `random_sp` INT NOT NULL DEFAULT 0,
  `playtime` INT NOT NULL DEFAULT 0,
  `gold` BIGINT NOT NULL DEFAULT 0,
  `gem` INT NOT NULL DEFAULT 0,
  `level` INT NOT NULL DEFAULT 1,
  `level_step` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `st` SMALLINT NOT NULL DEFAULT 0,
  `ht` SMALLINT NOT NULL DEFAULT 0,
  `dx` SMALLINT NOT NULL DEFAULT 0,
  `iq` SMALLINT NOT NULL DEFAULT 0,
  `exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `stat_point` SMALLINT NOT NULL DEFAULT 0,
  `skill_point` SMALLINT NOT NULL DEFAULT 0,
  `sub_skill_point` SMALLINT NOT NULL DEFAULT 0,
  `stat_reset_count` SMALLINT NOT NULL DEFAULT 0,
  `part_base` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `part_main` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `part_hair` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `part_acce` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `part_aura` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `skill_level` BLOB NULL,
  `quickslot` BLOB NULL,
  `skill_group` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `alignment` INT NOT NULL DEFAULT 0,
  `conquerorlevel` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `conqueror_level_step` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `sungma_str` SMALLINT NOT NULL DEFAULT 0,
  `sungma_hp` SMALLINT NOT NULL DEFAULT 0,
  `sungma_move` SMALLINT NOT NULL DEFAULT 0,
  `sungma_immune` SMALLINT NOT NULL DEFAULT 0,
  `conqueror_exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `conqueror_point` SMALLINT NOT NULL DEFAULT 0,
  `horse_level` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `horse_riding` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `horse_hp` SMALLINT NOT NULL DEFAULT 0,
  `horse_hp_droptime` INT UNSIGNED NOT NULL DEFAULT 0,
  `horse_stamina` SMALLINT NOT NULL DEFAULT 0,
  `horse_skill_point` SMALLINT NOT NULL DEFAULT 0,
  `last_play` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `change_name` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `anti_exp` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `shop_flag` BIGINT UNSIGNED NOT NULL DEFAULT 0,
  `shop_money` BIGINT NOT NULL DEFAULT 0,
  `pick_up_mode` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_0` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_1` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_2` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_3` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_4` INT UNSIGNED NOT NULL DEFAULT 0,
  `inventory_5` INT UNSIGNED NOT NULL DEFAULT 0,
  `mount_up_grade_exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `mount_up_grade_fail` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `soul` INT NOT NULL DEFAULT 0,
  `soulre` INT NOT NULL DEFAULT 0,
  `halounlv` INT NOT NULL DEFAULT 0,
  `phaloun` BIGINT NOT NULL DEFAULT 0,
  `rhaloun` INT NOT NULL DEFAULT 0,
  `statistics_jinno_kills` INT NOT NULL DEFAULT 0,
  `statistics_shinsoo_kills` INT NOT NULL DEFAULT 0,
  `statistics_chunjo_kills` INT NOT NULL DEFAULT 0,
  `statistics_total_kills` INT NOT NULL DEFAULT 0,
  `statistics_total_deaths` INT NOT NULL DEFAULT 0,
  `statistics_duels_won` INT NOT NULL DEFAULT 0,
  `statistics_duels_lost` INT NOT NULL DEFAULT 0,
  `statistics_bosses_kills` INT NOT NULL DEFAULT 0,
  `statistics_stones_kills` INT NOT NULL DEFAULT 0,
  `statistics_mobs_kills` INT NOT NULL DEFAULT 0,
  `top_damage` INT NOT NULL DEFAULT 0,
  `r0` BIGINT NOT NULL DEFAULT 0,
  `r1` BIGINT NOT NULL DEFAULT 0,
  `r2` BIGINT NOT NULL DEFAULT 0,
  `r3` BIGINT NOT NULL DEFAULT 0,
  `r4` BIGINT NOT NULL DEFAULT 0,
  `r5` BIGINT NOT NULL DEFAULT 0,
  `r6` BIGINT NOT NULL DEFAULT 0,
  `r7` BIGINT NOT NULL DEFAULT 0,
  `r8` BIGINT NOT NULL DEFAULT 0,
  `r9` BIGINT NOT NULL DEFAULT 0,
  `r10` BIGINT NOT NULL DEFAULT 0,
  `r11` BIGINT NOT NULL DEFAULT 0,
  `r12` BIGINT NOT NULL DEFAULT 0,
  `r13` BIGINT NOT NULL DEFAULT 0,
  `r14` BIGINT NOT NULL DEFAULT 0,
  `r15` BIGINT NOT NULL DEFAULT 0,
  `r16` BIGINT NOT NULL DEFAULT 0,
  `r17` BIGINT NOT NULL DEFAULT 0,
  `r18` BIGINT NOT NULL DEFAULT 0,
  `r19` BIGINT NOT NULL DEFAULT 0,
  `r20` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `account_id_idx` (`account_id`),
  KEY `name_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerPlayer.cpp:1699 (INSERT ... SELECT * FROM player, so the layout must match player exactly)
CREATE TABLE IF NOT EXISTS `player_deleted` LIKE `player`;

-- src: db/src/ClientManagerLogin.cpp:143, :165, :173; db/src/ClientManagerPlayer.cpp:1366, :1580, :1649, :1744; db/src/ClientManager.cpp:1101, :1107; game/src/char_change_empire.cpp:25, :93
CREATE TABLE IF NOT EXISTS `player_index` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid1` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid2` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid3` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid4` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid5` INT UNSIGNED NOT NULL DEFAULT 0,
  `empire` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `pid1_idx` (`pid1`),
  KEY `pid2_idx` (`pid2`),
  KEY `pid3_idx` (`pid3`),
  KEY `pid4_idx` (`pid4`),
  KEY `pid5_idx` (`pid5`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/char_change_empire.cpp:127, :165, :170
CREATE TABLE IF NOT EXISTS `change_empire` (
  `account_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `change_count` INT NOT NULL DEFAULT 0,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Items
-- ============================================================================

-- src: db/src/Cache.cpp:45, :123; db/src/ClientManager.cpp:631, :857, :1400, :1727; db/src/ClientManagerPlayer.cpp:597, :1764; db/src/ItemIDRangeManager.cpp:94
-- window ordinal == EWindows value in common/length.h (RESERVED_WINDOW=0 is never stored). The code writes the number
-- (REPLACE ... window=%d) and also the names ('SAFEBOX', 'MALL', ... in IN (...)), hence an ENUM.
-- UNSURE: the loaders only SELECT INVENTORY/EQUIPMENT/DRAGON_SOUL_INVENTORY/BELT_INVENTORY/SWITCHBOT, so items saved in the
--         special-inventory windows (ordinals 8-12) are never read back by db/src (the ENUM only has to accept them).
CREATE TABLE IF NOT EXISTS `item` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `window` ENUM('INVENTORY','EQUIPMENT','SAFEBOX','MALL','DRAGON_SOUL_INVENTORY','BELT_INVENTORY','SWITCHBOT','SKILL_BOOK_INVENTORY','UPGRADE_ITEMS_INVENTORY','STONE_INVENTORY','GIFT_BOX_INVENTORY','CHANGERS_INVENTORY','AURA_REFINE','GROUND') NOT NULL DEFAULT 'INVENTORY',
  `pos` SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  `count` INT UNSIGNED NOT NULL DEFAULT 1,
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `transmutation` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket0` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket1` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket2` INT UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue0` SMALLINT NOT NULL DEFAULT 0,
  `attrtype1` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue1` SMALLINT NOT NULL DEFAULT 0,
  `attrtype2` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue2` SMALLINT NOT NULL DEFAULT 0,
  `attrtype3` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue3` SMALLINT NOT NULL DEFAULT 0,
  `attrtype4` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue4` SMALLINT NOT NULL DEFAULT 0,
  `attrtype5` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue5` SMALLINT NOT NULL DEFAULT 0,
  `attrtype6` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue6` SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `owner_id_idx` (`owner_id`, `window`),
  KEY `vnum_idx` (`vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:554, :950, :981, :1002, :1091; game/src/char.cpp:8212, :8222
-- gold is only written (QUERY_SAFEBOX_SAVE), never selected.
CREATE TABLE IF NOT EXISTS `safebox` (
  `account_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `size` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `password` VARCHAR(6) NOT NULL DEFAULT '',
  `gold` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/Cache.cpp:394, :400; db/src/ClientManager.cpp:2175, :2206; db/src/ClientManagerPlayer.cpp:1781
CREATE TABLE IF NOT EXISTS `myshop_pricelist` (
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `item_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `price` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`owner_id`, `item_vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/Cache.cpp:440, :448; db/src/ClientManager.cpp:909, :4438, :4447; db/src/ClientManagerPlayer.cpp:844
-- owner_id is the player id, or the account id while state = 3 (STATE_SAFEBOX). state is numeric (EPetState starts at 0, so no ENUM).
-- skill_level holds the raw TPetSkill[PET_SKILL_COUNT_MAX] bytes.
CREATE TABLE IF NOT EXISTS `growth_pet` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `state` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(20) NOT NULL DEFAULT '',
  `size` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `level` INT UNSIGNED NOT NULL DEFAULT 1,
  `level_step` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `evolution` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `type` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `hp` INT UNSIGNED NOT NULL DEFAULT 0,
  `sp` INT UNSIGNED NOT NULL DEFAULT 0,
  `def` INT UNSIGNED NOT NULL DEFAULT 0,
  `hp_apply` INT UNSIGNED NOT NULL DEFAULT 0,
  `sp_apply` INT UNSIGNED NOT NULL DEFAULT 0,
  `def_apply` INT UNSIGNED NOT NULL DEFAULT 0,
  `age_apply` INT UNSIGNED NOT NULL DEFAULT 0,
  `skill_level` BLOB NULL,
  `exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `item_exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `birthday` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` INT NOT NULL DEFAULT 0,
  `max_time` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `owner_id_idx` (`owner_id`, `state`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerPlayer.cpp:422-489 (SELECT), db/src/Cache.cpp:154-261 (REPLACE)
-- UNSURE: the SELECT reads 9 skill slots + 5 buff slots (14 groups), but the active REPLACE variant in Cache.cpp
--         (NINETH_SKILL on, WOLFMAN off) names 9 skill + 7 buff slots (16 groups, last two written as 0).
--         All 16 groups exist here so both statements work. Values are written with %d, hence signed INT.
CREATE TABLE IF NOT EXISTS `skill_color` (
  `player_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `skillSlot1_Col1` INT NOT NULL DEFAULT 0, `skillSlot1_Col2` INT NOT NULL DEFAULT 0, `skillSlot1_Col3` INT NOT NULL DEFAULT 0, `skillSlot1_Col4` INT NOT NULL DEFAULT 0, `skillSlot1_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot2_Col1` INT NOT NULL DEFAULT 0, `skillSlot2_Col2` INT NOT NULL DEFAULT 0, `skillSlot2_Col3` INT NOT NULL DEFAULT 0, `skillSlot2_Col4` INT NOT NULL DEFAULT 0, `skillSlot2_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot3_Col1` INT NOT NULL DEFAULT 0, `skillSlot3_Col2` INT NOT NULL DEFAULT 0, `skillSlot3_Col3` INT NOT NULL DEFAULT 0, `skillSlot3_Col4` INT NOT NULL DEFAULT 0, `skillSlot3_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot4_Col1` INT NOT NULL DEFAULT 0, `skillSlot4_Col2` INT NOT NULL DEFAULT 0, `skillSlot4_Col3` INT NOT NULL DEFAULT 0, `skillSlot4_Col4` INT NOT NULL DEFAULT 0, `skillSlot4_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot5_Col1` INT NOT NULL DEFAULT 0, `skillSlot5_Col2` INT NOT NULL DEFAULT 0, `skillSlot5_Col3` INT NOT NULL DEFAULT 0, `skillSlot5_Col4` INT NOT NULL DEFAULT 0, `skillSlot5_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot6_Col1` INT NOT NULL DEFAULT 0, `skillSlot6_Col2` INT NOT NULL DEFAULT 0, `skillSlot6_Col3` INT NOT NULL DEFAULT 0, `skillSlot6_Col4` INT NOT NULL DEFAULT 0, `skillSlot6_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot7_Col1` INT NOT NULL DEFAULT 0, `skillSlot7_Col2` INT NOT NULL DEFAULT 0, `skillSlot7_Col3` INT NOT NULL DEFAULT 0, `skillSlot7_Col4` INT NOT NULL DEFAULT 0, `skillSlot7_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot8_Col1` INT NOT NULL DEFAULT 0, `skillSlot8_Col2` INT NOT NULL DEFAULT 0, `skillSlot8_Col3` INT NOT NULL DEFAULT 0, `skillSlot8_Col4` INT NOT NULL DEFAULT 0, `skillSlot8_Col5` INT NOT NULL DEFAULT 0,
  `skillSlot9_Col1` INT NOT NULL DEFAULT 0, `skillSlot9_Col2` INT NOT NULL DEFAULT 0, `skillSlot9_Col3` INT NOT NULL DEFAULT 0, `skillSlot9_Col4` INT NOT NULL DEFAULT 0, `skillSlot9_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill1_Col1` INT NOT NULL DEFAULT 0, `buffSkill1_Col2` INT NOT NULL DEFAULT 0, `buffSkill1_Col3` INT NOT NULL DEFAULT 0, `buffSkill1_Col4` INT NOT NULL DEFAULT 0, `buffSkill1_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill2_Col1` INT NOT NULL DEFAULT 0, `buffSkill2_Col2` INT NOT NULL DEFAULT 0, `buffSkill2_Col3` INT NOT NULL DEFAULT 0, `buffSkill2_Col4` INT NOT NULL DEFAULT 0, `buffSkill2_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill3_Col1` INT NOT NULL DEFAULT 0, `buffSkill3_Col2` INT NOT NULL DEFAULT 0, `buffSkill3_Col3` INT NOT NULL DEFAULT 0, `buffSkill3_Col4` INT NOT NULL DEFAULT 0, `buffSkill3_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill4_Col1` INT NOT NULL DEFAULT 0, `buffSkill4_Col2` INT NOT NULL DEFAULT 0, `buffSkill4_Col3` INT NOT NULL DEFAULT 0, `buffSkill4_Col4` INT NOT NULL DEFAULT 0, `buffSkill4_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill5_Col1` INT NOT NULL DEFAULT 0, `buffSkill5_Col2` INT NOT NULL DEFAULT 0, `buffSkill5_Col3` INT NOT NULL DEFAULT 0, `buffSkill5_Col4` INT NOT NULL DEFAULT 0, `buffSkill5_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill6_Col1` INT NOT NULL DEFAULT 0, `buffSkill6_Col2` INT NOT NULL DEFAULT 0, `buffSkill6_Col3` INT NOT NULL DEFAULT 0, `buffSkill6_Col4` INT NOT NULL DEFAULT 0, `buffSkill6_Col5` INT NOT NULL DEFAULT 0,
  `buffSkill7_Col1` INT NOT NULL DEFAULT 0, `buffSkill7_Col2` INT NOT NULL DEFAULT 0, `buffSkill7_Col3` INT NOT NULL DEFAULT 0, `buffSkill7_Col4` INT NOT NULL DEFAULT 0, `buffSkill7_Col5` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`player_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerPlayer.cpp:581, :588; db/src/ClientManager.cpp:529, :535; db/src/ClientManagerEventFlag.cpp:11, :52; db/src/ClientManagerGuild.cpp:76, :113; game/src/char_manager.cpp:2152
-- dwPID = 0 rows are the global event flags (szState = '').
CREATE TABLE IF NOT EXISTS `quest` (
  `dwPID` INT UNSIGNED NOT NULL DEFAULT 0,
  `szName` VARCHAR(32) NOT NULL DEFAULT '',
  `szState` VARCHAR(64) NOT NULL DEFAULT '',
  `lValue` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`dwPID`, `szName`, `szState`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerPlayer.cpp:588, :1803, :1822; game/src/cmd_gm.cpp:3119
CREATE TABLE IF NOT EXISTS `affect` (
  `dwPID` INT UNSIGNED NOT NULL DEFAULT 0,
  `bType` INT UNSIGNED NOT NULL DEFAULT 0,
  `bApplyOn` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `lApplyValue` INT NOT NULL DEFAULT 0,
  `dwFlag` INT UNSIGNED NOT NULL DEFAULT 0,
  `lDuration` INT NOT NULL DEFAULT 0,
  `lSPCost` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`dwPID`, `bType`, `bApplyOn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerHorseName.cpp:8, :19
CREATE TABLE IF NOT EXISTS `horse_name` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(48) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerPlayer.cpp:1831, :1858, :1880; game/src/db.cpp:574; game/src/questlua.cpp:228, :245
CREATE TABLE IF NOT EXISTS `highscore` (
  `board` VARCHAR(20) NOT NULL DEFAULT '',
  `pid` INT UNSIGNED NOT NULL DEFAULT 0,
  `value` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`board`, `pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:4539
-- Only ever written; nothing in the source reads it back (ranking boards use player.r0..r20).
CREATE TABLE IF NOT EXISTS `player_ranking` (
  `dwPID` INT UNSIGNED NOT NULL DEFAULT 0,
  `rank` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `lValue` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`dwPID`, `rank`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/Marriage.cpp:40, :43, :102, :141, :188, :231
CREATE TABLE IF NOT EXISTS `marriage` (
  `pid1` INT UNSIGNED NOT NULL DEFAULT 0,
  `pid2` INT UNSIGNED NOT NULL DEFAULT 0,
  `love_point` INT NOT NULL DEFAULT 0,
  `time` INT UNSIGNED NOT NULL DEFAULT 0,
  `is_married` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid1`, `pid2`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ItemAwardManager.cpp:58, :69, :175; db/src/ClientManager.cpp:829-880; db/src/GuildManager.cpp:1095, :1285, :1384; game/src/questlua_pc.cpp:3573, :3604
CREATE TABLE IF NOT EXISTS `item_award` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(30) NOT NULL DEFAULT '',
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `count` INT UNSIGNED NOT NULL DEFAULT 1,
  `given_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `taken_time` DATETIME NULL DEFAULT NULL,
  `item_id` INT UNSIGNED NULL DEFAULT NULL,
  `why` VARCHAR(50) NULL DEFAULT NULL,
  `socket0` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket1` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket2` INT UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue0` SMALLINT NOT NULL DEFAULT 0,
  `attrtype1` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue1` SMALLINT NOT NULL DEFAULT 0,
  `attrtype2` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue2` SMALLINT NOT NULL DEFAULT 0,
  `attrtype3` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue3` SMALLINT NOT NULL DEFAULT 0,
  `attrtype4` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue4` SMALLINT NOT NULL DEFAULT 0,
  `attrtype5` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue5` SMALLINT NOT NULL DEFAULT 0,
  `attrtype6` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue6` SMALLINT NOT NULL DEFAULT 0,
  `mall` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `login_idx` (`login`),
  KEY `taken_time_idx` (`taken_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/messenger_manager.cpp:49, :691, :772, :790, :808; db/src/ClientManagerPlayer.cpp:1785
-- Both columns hold character names.
CREATE TABLE IF NOT EXISTS `messenger_list` (
  `account` VARCHAR(48) NOT NULL DEFAULT '',
  `companion` VARCHAR(48) NOT NULL DEFAULT '',
  PRIMARY KEY (`account`, `companion`),
  KEY `companion_idx` (`companion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/messenger_manager.cpp:58, :376, :418, :435
CREATE TABLE IF NOT EXISTS `messenger_block_list` (
  `account` VARCHAR(48) NOT NULL DEFAULT '',
  `companion` VARCHAR(48) NOT NULL DEFAULT '',
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`account`, `companion`),
  KEY `companion_idx` (`companion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/item_manager.cpp:1208; game/src/char_item.cpp:4262; game/src/questlua_pc.cpp:2256
-- Written positionally as (0, 'server<postfix>', pid, NOW()).
CREATE TABLE IF NOT EXISTS `lotto_list` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `server` VARCHAR(32) NOT NULL DEFAULT 'server',
  `pid` INT UNSIGNED NOT NULL DEFAULT 0,
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/db.cpp:619
CREATE TABLE IF NOT EXISTS `string` (
  `name` VARCHAR(64) NOT NULL DEFAULT '',
  `text` TEXT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Guilds
-- ============================================================================

-- src: game/src/guild.cpp:84, :657, :670, :689; db/src/GuildManager.cpp:131, :162, :727, :1128; db/src/ClientManagerGuild.cpp:106; game/src/questlua_pc.cpp:3120
-- skill is the raw BYTE abySkill[GUILD_SKILL_COUNT] blob.
CREATE TABLE IF NOT EXISTS `guild` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(12) NOT NULL DEFAULT '',
  `master` INT UNSIGNED NOT NULL DEFAULT 0,
  `sp` INT NOT NULL DEFAULT 1000,
  `level` INT NOT NULL DEFAULT 1,
  `exp` INT UNSIGNED NOT NULL DEFAULT 0,
  `skill_point` INT NOT NULL DEFAULT 0,
  `skill` BLOB NULL,
  `ladder_point` INT NOT NULL DEFAULT 0,
  `win` INT NOT NULL DEFAULT 0,
  `draw` INT NOT NULL DEFAULT 0,
  `loss` INT NOT NULL DEFAULT 0,
  `gold` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `name_idx` (`name`),
  KEY `master_idx` (`master`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/guild.cpp:93, :662, :806, :849, :888; db/src/ClientManagerGuild.cpp:109
-- UNSURE: auth is a numeric bitmask (GUILD_AUTH_* bits 0-3); the code only writes numbers and reads auth+0, so no SET.
CREATE TABLE IF NOT EXISTS `guild_grade` (
  `guild_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `grade` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(8) NOT NULL DEFAULT '',
  `auth` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`guild_id`, `grade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerGuild.cpp:32, :38, :72, :116; game/src/guild.cpp:665, :1571
-- Positional INSERT (pid, guild_id, grade, is_general, offer).
CREATE TABLE IF NOT EXISTS `guild_member` (
  `pid` INT UNSIGNED NOT NULL DEFAULT 0,
  `guild_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `grade` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `is_general` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `offer` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`pid`),
  KEY `guild_id_idx` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/guild.cpp:1104, :1115, :1139; db/src/ClientManagerGuild.cpp:119
CREATE TABLE IF NOT EXISTS `guild_comment` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `guild_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(48) NOT NULL DEFAULT '',
  `notice` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `content` VARCHAR(50) NOT NULL DEFAULT '',
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `guild_id_idx` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/guild.cpp:239, :2159; game/src/input_main.cpp:3536
-- Positional REPLACE (guild id, unix time).
CREATE TABLE IF NOT EXISTS `guild_invite_limit` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `value` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/GuildManager.cpp:843, :1003, :1050, :1248, :1270, :1349
-- winner = -1 means "not decided yet" (BootReserveWar).
CREATE TABLE IF NOT EXISTS `guild_war_reservation` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `guild1` INT UNSIGNED NOT NULL DEFAULT 0,
  `guild2` INT UNSIGNED NOT NULL DEFAULT 0,
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `type` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `warprice` INT NOT NULL DEFAULT 0,
  `initscore` INT NOT NULL DEFAULT 0,
  `started` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `winner` INT NOT NULL DEFAULT -1,
  `result1` INT NOT NULL DEFAULT 0,
  `result2` INT NOT NULL DEFAULT 0,
  `bet_from` INT UNSIGNED NOT NULL DEFAULT 0,
  `bet_to` INT UNSIGNED NOT NULL DEFAULT 0,
  `power1` INT NOT NULL DEFAULT 0,
  `power2` INT NOT NULL DEFAULT 0,
  `handicap` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `started_idx` (`started`, `winner`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/GuildManager.cpp:1154, :1230
CREATE TABLE IF NOT EXISTS `guild_war_bet` (
  `war_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `login` VARCHAR(30) NOT NULL DEFAULT '',
  `gold` INT UNSIGNED NOT NULL DEFAULT 0,
  `guild` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`war_id`, `login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Guild land / buildings
-- ============================================================================

-- src: db/src/ClientManagerBoot.cpp:1042, :1059; db/src/ClientManager.cpp:2066; game/src/questlua_building.cpp:97
-- Static map data (which plots exist). Loaded at db boot; empty table is accepted but then no plot can be bought.
CREATE TABLE IF NOT EXISTS `land` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `map_index` INT NOT NULL DEFAULT 0,
  `x` INT NOT NULL DEFAULT 0,
  `y` INT NOT NULL DEFAULT 0,
  `width` INT NOT NULL DEFAULT 0,
  `height` INT NOT NULL DEFAULT 0,
  `guild_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `guild_level_limit` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `price` INT UNSIGNED NOT NULL DEFAULT 0,
  `enable` ENUM('YES','NO') NOT NULL DEFAULT 'YES',
  PRIMARY KEY (`id`),
  KEY `guild_id_idx` (`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:1996, :2031; db/src/ClientManagerBoot.cpp:1052, :1233
CREATE TABLE IF NOT EXISTS `object` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `land_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `map_index` INT NOT NULL DEFAULT 0,
  `x` INT NOT NULL DEFAULT 0,
  `y` INT NOT NULL DEFAULT 0,
  `x_rot` FLOAT NOT NULL DEFAULT 0,
  `y_rot` FLOAT NOT NULL DEFAULT 0,
  `z_rot` FLOAT NOT NULL DEFAULT 0,
  `life` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `land_id_idx` (`land_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:1162
-- materials format: "itemvnum,count/itemvnum,count/..." (parse_pair_number_string).
CREATE TABLE IF NOT EXISTS `object_proto` (
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `price` INT UNSIGNED NOT NULL DEFAULT 0,
  `materials` VARCHAR(255) NOT NULL DEFAULT '',
  `upgrade_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `upgrade_limit_time` INT UNSIGNED NOT NULL DEFAULT 0,
  `life` INT NOT NULL DEFAULT 0,
  `reg_1` INT NOT NULL DEFAULT 0,
  `reg_2` INT NOT NULL DEFAULT 0,
  `reg_3` INT NOT NULL DEFAULT 0,
  `reg_4` INT NOT NULL DEFAULT 0,
  `npc` INT UNSIGNED NOT NULL DEFAULT 0,
  `group_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `dependent_group` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Boot-time prototype tables (read by db/src/ClientManagerBoot.cpp)
--
-- Data sources: NONE of these is shipped in the repo, except refine_proto
-- (see the LOAD DATA hint below). The db process refuses to boot while
-- shop, skill_proto, item_attr, item_attr_rare or growth_pet_skill_proto
-- has zero rows. mob_proto / item_proto are NOT in the database: they are read
-- from home/main/db/mob_proto.txt and item_proto.txt.
-- ============================================================================

-- src: db/src/ClientManagerBoot.cpp:122
-- Data hint: the client's wiki table Tools/binary_unpack/locale/common/refine_table.txt (tab separated, 15 columns:
-- id, vnum0,count0 .. vnum4,count4, cost, <unused>, <unused>, prob) matches this table, e.g.
--   LOAD DATA LOCAL INFILE 'Tools/binary_unpack/locale/common/refine_table.txt' INTO TABLE refine_proto
--     (id, vnum0, count0, vnum1, count1, vnum2, count2, vnum3, count3, vnum4, count4, cost, @unused1, @unused2, prob);
-- UNSURE: that the client file mirrors the original server refine_proto 1:1 is inferred from PythonWiki.cpp, not proven.
CREATE TABLE IF NOT EXISTS `refine_proto` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `cost` INT NOT NULL DEFAULT 0,
  `prob` INT NOT NULL DEFAULT 0,
  `vnum0` INT UNSIGNED NOT NULL DEFAULT 0,
  `count0` INT NOT NULL DEFAULT 0,
  `vnum1` INT UNSIGNED NOT NULL DEFAULT 0,
  `count1` INT NOT NULL DEFAULT 0,
  `vnum2` INT UNSIGNED NOT NULL DEFAULT 0,
  `count2` INT NOT NULL DEFAULT 0,
  `vnum3` INT UNSIGNED NOT NULL DEFAULT 0,
  `count3` INT NOT NULL DEFAULT 0,
  `vnum4` INT UNSIGNED NOT NULL DEFAULT 0,
  `count4` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:345 (needs at least one row in `shop`, otherwise InitializeShopTable fails)
CREATE TABLE IF NOT EXISTS `shop` (
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `npc_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `shop_item` (
  `shop_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `item_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `count` SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  KEY `shop_vnum_idx` (`shop_vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:427 (ENABLE_RENEWAL_SHOPEX). price_type is the STableExTypes value: 1 gold, 2 coins, 3 item, 4 exp.
CREATE TABLE IF NOT EXISTS `shopex` (
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(32) NOT NULL DEFAULT '',
  `npc_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `shopex_item` (
  `shop_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `item_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `count` SMALLINT UNSIGNED NOT NULL DEFAULT 1,
  `price` BIGINT NOT NULL DEFAULT 0,
  `price_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `price_type` ENUM('GOLD','COINS','ITEM','EXP') NOT NULL DEFAULT 'GOLD',
  `socket0` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket1` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket2` INT UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue0` SMALLINT NOT NULL DEFAULT 0,
  `attrtype1` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue1` SMALLINT NOT NULL DEFAULT 0,
  `attrtype2` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue2` SMALLINT NOT NULL DEFAULT 0,
  `attrtype3` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue3` SMALLINT NOT NULL DEFAULT 0,
  `attrtype4` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue4` SMALLINT NOT NULL DEFAULT 0,
  `attrtype5` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue5` SMALLINT NOT NULL DEFAULT 0,
  `attrtype6` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue6` SMALLINT NOT NULL DEFAULT 0,
  KEY `shop_vnum_idx` (`shop_vnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:738 (needs at least one row)
-- setFlag is a SET whose member order equals the ESkillFlags bit order (game/src/skill.h); eSkillType is an ENUM whose
-- ordinal equals SKILL_ATTR_TYPE_* (common/length.h, starts at 1). The db reads both as x+0.
-- setAffectFlag / setAffectFlag2 stay numeric: they hold EAffectBits values (game/src/affect.h) and 0 means none, which an
-- ENUM cannot encode.
-- szPointOn / szPointOn2 must name an entry of kPointOnTypes (game/src/skill.cpp); '' makes the game reject the whole table.
-- Every string column is NOT NULL because strlcpy() is called on the raw row pointer.
CREATE TABLE IF NOT EXISTS `skill_proto` (
  `dwVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `szName` VARCHAR(32) NOT NULL DEFAULT '',
  `bType` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `bMaxLevel` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `dwSplashRange` INT UNSIGNED NOT NULL DEFAULT 0,
  `szPointOn` VARCHAR(63) NOT NULL DEFAULT 'NONE',
  `szPointPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szSPCostPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szDurationPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szDurationSPCostPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szCooldownPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szMasterBonusPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `setFlag` SET('ATTACK','USE_MELEE_DAMAGE','COMPUTE_ATTGRADE','SELFONLY','USE_MAGIC_DAMAGE','USE_HP_AS_COST','COMPUTE_MAGIC_DAMAGE','SPLASH','GIVE_PENALTY','USE_ARROW_DAMAGE','PENETRATE','IGNORE_TARGET_RATING','SLOW','STUN','HP_ABSORB','SP_ABSORB','FIRE_CONT','REMOVE_BAD_AFFECT','REMOVE_GOOD_AFFECT','CRUSH','POISON','TOGGLE','DISABLE_BY_POINT_UP','CRUSH_LONG','WIND','ELEC','FIRE','PARTY','KNOCKBACK') NOT NULL DEFAULT '',
  `setAffectFlag` INT UNSIGNED NOT NULL DEFAULT 0,
  `szPointOn2` VARCHAR(63) NOT NULL DEFAULT 'NONE',
  `szPointPoly2` VARCHAR(100) NOT NULL DEFAULT '',
  `szDurationPoly2` VARCHAR(100) NOT NULL DEFAULT '',
  `setAffectFlag2` INT UNSIGNED NOT NULL DEFAULT 0,
  `szPointOn3` VARCHAR(63) NOT NULL DEFAULT '',
  `szPointPoly3` VARCHAR(100) NOT NULL DEFAULT '',
  `szDurationPoly3` VARCHAR(100) NOT NULL DEFAULT '',
  `szGrandMasterAddSPCostPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `bLevelStep` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `bLevelLimit` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `prerequisiteSkillVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `prerequisiteSkillLevel` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `iMaxHit` INT NOT NULL DEFAULT 0,
  `szSplashAroundDamageAdjustPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `eSkillType` ENUM('NORMAL','MELEE','RANGE','MAGIC') NOT NULL DEFAULT 'NORMAL',
  `dwTargetRange` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`dwVnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:856 (item_attr), :955 (item_attr_rare); both need at least one row.
-- apply is an ENUM whose ordinal equals the EApplyTypes value (common/length.h, APPLY_NONE=0 excluded): the db reads
-- apply+0 and the game indexes g_map_itemAttr by it. Names are the APPLY_* enumerators without the prefix.
CREATE TABLE IF NOT EXISTS `item_attr` (
  `apply` ENUM('MAX_HP','MAX_SP','CON','INT','STR','DEX','ATT_SPEED','MOV_SPEED','CAST_SPEED','HP_REGEN','SP_REGEN','POISON_PCT','STUN_PCT','SLOW_PCT','CRITICAL_PCT','PENETRATE_PCT','ATTBONUS_HUMAN','ATTBONUS_ANIMAL','ATTBONUS_ORC','ATTBONUS_MILGYO','ATTBONUS_UNDEAD','ATTBONUS_DEVIL','STEAL_HP','STEAL_SP','MANA_BURN_PCT','DAMAGE_SP_RECOVER','BLOCK','DODGE','RESIST_SWORD','RESIST_TWOHAND','RESIST_DAGGER','RESIST_BELL','RESIST_FAN','RESIST_BOW','RESIST_FIRE','RESIST_ELEC','RESIST_MAGIC','RESIST_WIND','REFLECT_MELEE','REFLECT_CURSE','POISON_REDUCE','KILL_SP_RECOVER','EXP_DOUBLE_BONUS','GOLD_DOUBLE_BONUS','ITEM_DROP_BONUS','POTION_BONUS','KILL_HP_RECOVER','IMMUNE_STUN','IMMUNE_SLOW','IMMUNE_FALL','SKILL','BOW_DISTANCE','ATT_GRADE_BONUS','DEF_GRADE_BONUS','MAGIC_ATT_GRADE','MAGIC_DEF_GRADE','CURSE_PCT','MAX_STAMINA','ATTBONUS_WARRIOR','ATTBONUS_ASSASSIN','ATTBONUS_SURA','ATTBONUS_SHAMAN','ATTBONUS_MONSTER','MALL_ATTBONUS','MALL_DEFBONUS','MALL_EXPBONUS','MALL_ITEMBONUS','MALL_GOLDBONUS','MAX_HP_PCT','MAX_SP_PCT','SKILL_DAMAGE_BONUS','NORMAL_HIT_DAMAGE_BONUS','SKILL_DEFEND_BONUS','NORMAL_HIT_DEFEND_BONUS','PC_BANG_EXP_BONUS','PC_BANG_DROP_BONUS','EXTRACT_HP_PCT','RESIST_WARRIOR','RESIST_ASSASSIN','RESIST_SURA','RESIST_SHAMAN','ENERGY','DEF_GRADE','COSTUME_ATTR_BONUS','MAGIC_ATTBONUS_PER','MELEE_MAGIC_ATTBONUS_PER','RESIST_ICE','RESIST_EARTH','RESIST_DARK','ANTI_CRITICAL_PCT','ANTI_PENETRATE_PCT','ACCEDRAIN_RATE','RESIST_MAGIC_REDUCTION','ENCHANT_ELECT','ENCHANT_FIRE','ENCHANT_ICE','ENCHANT_WIND','ENCHANT_EARTH','ENCHANT_DARK','ATTBONUS_CZ','ATTBONUS_INSECT','ATTBONUS_DESERT','ATTBONUS_SWORD','ATTBONUS_TWOHAND','ATTBONUS_DAGGER','ATTBONUS_BELL','ATTBONUS_FAN','ATTBONUS_BOW','RESIST_HUMAN','RESIST_MOUNT_FALL','MOUNT','ATTBONUS_STONE','ATTBONUS_BOSS','ATTBONUS_ELEMENTS','ENCHANT_ELEMENTS','ATTBONUS_CHARACTERS','ENCHANT_CHARACTERS','RESIST_MONSTER','ATTBONUS_MEDI_PVM','ATTBONUS_PVM_STR','ATTBONUS_PVM_BERSERKER','SUNGMA_STR','SUNGMA_HP','SUNGMA_MOVE','SUNGMA_IMMUNE') NOT NULL,
  `prob` INT UNSIGNED NOT NULL DEFAULT 0,
  `lv1` INT NOT NULL DEFAULT 0,
  `lv2` INT NOT NULL DEFAULT 0,
  `lv3` INT NOT NULL DEFAULT 0,
  `lv4` INT NOT NULL DEFAULT 0,
  `lv5` INT NOT NULL DEFAULT 0,
  `weapon` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `body` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `wrist` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `foots` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `neck` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `head` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `shield` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `ear` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `pendant` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `costume_body` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `costume_hair` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `costume_weapon` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`apply`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `item_attr_rare` (
  `apply` ENUM('MAX_HP','MAX_SP','CON','INT','STR','DEX','ATT_SPEED','MOV_SPEED','CAST_SPEED','HP_REGEN','SP_REGEN','POISON_PCT','STUN_PCT','SLOW_PCT','CRITICAL_PCT','PENETRATE_PCT','ATTBONUS_HUMAN','ATTBONUS_ANIMAL','ATTBONUS_ORC','ATTBONUS_MILGYO','ATTBONUS_UNDEAD','ATTBONUS_DEVIL','STEAL_HP','STEAL_SP','MANA_BURN_PCT','DAMAGE_SP_RECOVER','BLOCK','DODGE','RESIST_SWORD','RESIST_TWOHAND','RESIST_DAGGER','RESIST_BELL','RESIST_FAN','RESIST_BOW','RESIST_FIRE','RESIST_ELEC','RESIST_MAGIC','RESIST_WIND','REFLECT_MELEE','REFLECT_CURSE','POISON_REDUCE','KILL_SP_RECOVER','EXP_DOUBLE_BONUS','GOLD_DOUBLE_BONUS','ITEM_DROP_BONUS','POTION_BONUS','KILL_HP_RECOVER','IMMUNE_STUN','IMMUNE_SLOW','IMMUNE_FALL','SKILL','BOW_DISTANCE','ATT_GRADE_BONUS','DEF_GRADE_BONUS','MAGIC_ATT_GRADE','MAGIC_DEF_GRADE','CURSE_PCT','MAX_STAMINA','ATTBONUS_WARRIOR','ATTBONUS_ASSASSIN','ATTBONUS_SURA','ATTBONUS_SHAMAN','ATTBONUS_MONSTER','MALL_ATTBONUS','MALL_DEFBONUS','MALL_EXPBONUS','MALL_ITEMBONUS','MALL_GOLDBONUS','MAX_HP_PCT','MAX_SP_PCT','SKILL_DAMAGE_BONUS','NORMAL_HIT_DAMAGE_BONUS','SKILL_DEFEND_BONUS','NORMAL_HIT_DEFEND_BONUS','PC_BANG_EXP_BONUS','PC_BANG_DROP_BONUS','EXTRACT_HP_PCT','RESIST_WARRIOR','RESIST_ASSASSIN','RESIST_SURA','RESIST_SHAMAN','ENERGY','DEF_GRADE','COSTUME_ATTR_BONUS','MAGIC_ATTBONUS_PER','MELEE_MAGIC_ATTBONUS_PER','RESIST_ICE','RESIST_EARTH','RESIST_DARK','ANTI_CRITICAL_PCT','ANTI_PENETRATE_PCT','ACCEDRAIN_RATE','RESIST_MAGIC_REDUCTION','ENCHANT_ELECT','ENCHANT_FIRE','ENCHANT_ICE','ENCHANT_WIND','ENCHANT_EARTH','ENCHANT_DARK','ATTBONUS_CZ','ATTBONUS_INSECT','ATTBONUS_DESERT','ATTBONUS_SWORD','ATTBONUS_TWOHAND','ATTBONUS_DAGGER','ATTBONUS_BELL','ATTBONUS_FAN','ATTBONUS_BOW','RESIST_HUMAN','RESIST_MOUNT_FALL','MOUNT','ATTBONUS_STONE','ATTBONUS_BOSS','ATTBONUS_ELEMENTS','ENCHANT_ELEMENTS','ATTBONUS_CHARACTERS','ENCHANT_CHARACTERS','RESIST_MONSTER','ATTBONUS_MEDI_PVM','ATTBONUS_PVM_STR','ATTBONUS_PVM_BERSERKER','SUNGMA_STR','SUNGMA_HP','SUNGMA_MOVE','SUNGMA_IMMUNE') NOT NULL,
  `prob` INT UNSIGNED NOT NULL DEFAULT 0,
  `lv1` INT NOT NULL DEFAULT 0,
  `lv2` INT NOT NULL DEFAULT 0,
  `lv3` INT NOT NULL DEFAULT 0,
  `lv4` INT NOT NULL DEFAULT 0,
  `lv5` INT NOT NULL DEFAULT 0,
  `weapon` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `body` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `wrist` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `foots` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `neck` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `head` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `shield` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `ear` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `pendant` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`apply`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:828 (empty table is fine)
CREATE TABLE IF NOT EXISTS `banword` (
  `word` VARCHAR(24) NOT NULL DEFAULT '',
  PRIMARY KEY (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerBoot.cpp:1280 (needs at least one row, InitializeGrowthPetSkillTable returns false when empty)
-- bType and setAffectFlag are read as numbers (+0); stored numerically for the same reason as skill_proto.
CREATE TABLE IF NOT EXISTS `growth_pet_skill_proto` (
  `dwPetVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `dwSkillVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `szName` VARCHAR(32) NOT NULL DEFAULT '',
  `bType` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `dwCooldown` INT UNSIGNED NOT NULL DEFAULT 0,
  `setAffectFlag` INT UNSIGNED NOT NULL DEFAULT 0,
  `szPointOn` VARCHAR(63) NOT NULL DEFAULT '',
  `szPointPoly1` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly2` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly3` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly4` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly5` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly6` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly7` VARCHAR(100) NOT NULL DEFAULT '',
  `szPointPoly8` VARCHAR(100) NOT NULL DEFAULT '',
  `szActivatePctPoly` VARCHAR(100) NOT NULL DEFAULT '',
  `szDurationPoly` VARCHAR(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`dwPetVnum`, `dwSkillVnum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Offline shop (ENABLE_RENEWAL_OFFLINESHOP)
-- ============================================================================

-- src: db/src/ClientManagerOfflineshop.cpp:23 (SELECT *, column order matters), :113, :177, :477, :518, :539; db/src/ClientManager.cpp:105
-- UNSURE: slotflag is signed because the code prints an unsigned long long with %lld.
CREATE TABLE IF NOT EXISTS `offline_shop_npc` (
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `owner_name` VARCHAR(48) NOT NULL DEFAULT '',
  `sign` VARCHAR(45) NOT NULL DEFAULT '',
  `x` INT NOT NULL DEFAULT 0,
  `y` INT NOT NULL DEFAULT 0,
  `z` INT NOT NULL DEFAULT 0,
  `mapindex` INT UNSIGNED NOT NULL DEFAULT 0,
  `type` INT NOT NULL DEFAULT 0,
  `channel` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `slotflag` BIGINT NOT NULL DEFAULT 0,
  `time` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerOfflineshop.cpp:56, :208, :251, :290, :336, :433; db/src/ItemIDRangeManager.cpp:110
-- id comes from the item id range generator, not AUTO_INCREMENT. status 0 = on sale, 1 = sold.
CREATE TABLE IF NOT EXISTS `offline_shop_item` (
  `id` INT UNSIGNED NOT NULL DEFAULT 0,
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `pos` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `count` INT NOT NULL DEFAULT 0,
  `vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket0` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket1` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket2` INT UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue0` SMALLINT NOT NULL DEFAULT 0,
  `attrtype1` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue1` SMALLINT NOT NULL DEFAULT 0,
  `attrtype2` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue2` SMALLINT NOT NULL DEFAULT 0,
  `attrtype3` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue3` SMALLINT NOT NULL DEFAULT 0,
  `attrtype4` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue4` SMALLINT NOT NULL DEFAULT 0,
  `attrtype5` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue5` SMALLINT NOT NULL DEFAULT 0,
  `attrtype6` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue6` SMALLINT NOT NULL DEFAULT 0,
  `price` BIGINT NOT NULL DEFAULT 0,
  `status` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `ownername` VARCHAR(48) NOT NULL DEFAULT '',
  `buyername` VARCHAR(48) NOT NULL DEFAULT '',
  `transmutation` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `owner_id_idx` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerOfflineshop.cpp:122, :214, :398, :495
-- time is a preformatted string ("%X-%d.%m.%Y"), copied into a char[25].
CREATE TABLE IF NOT EXISTS `offline_shop_log` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `target` VARCHAR(48) NOT NULL DEFAULT '',
  `time` VARCHAR(25) NOT NULL DEFAULT '',
  `itemvnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemcount` INT NOT NULL DEFAULT 0,
  `price` BIGINT NOT NULL DEFAULT 0,
  `item_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `pos` INT NOT NULL DEFAULT 0,
  `transmutation` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket0` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket1` INT UNSIGNED NOT NULL DEFAULT 0,
  `socket2` INT UNSIGNED NOT NULL DEFAULT 0,
  `attrtype0` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue0` SMALLINT NOT NULL DEFAULT 0,
  `attrtype1` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue1` SMALLINT NOT NULL DEFAULT 0,
  `attrtype2` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue2` SMALLINT NOT NULL DEFAULT 0,
  `attrtype3` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue3` SMALLINT NOT NULL DEFAULT 0,
  `attrtype4` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue4` SMALLINT NOT NULL DEFAULT 0,
  `attrtype5` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue5` SMALLINT NOT NULL DEFAULT 0,
  `attrtype6` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `attrvalue6` SMALLINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `owner_id_idx` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManagerOfflineshop.cpp:9
CREATE TABLE IF NOT EXISTS `offline_shop_log_important` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `reason` VARCHAR(64) NOT NULL DEFAULT '',
  `owner_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `owner` VARCHAR(48) NOT NULL DEFAULT '',
  `target_id` INT UNSIGNED NOT NULL DEFAULT 0,
  `target` VARCHAR(48) NOT NULL DEFAULT '',
  `itemid` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemvnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemcount` INT NOT NULL DEFAULT 0,
  `price` BIGINT NOT NULL DEFAULT 0,
  `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `owner_id_idx` (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Item shop (ENABLE_ITEMSHOP + USE_ITEMSHOP_RENEWED). Coins live in account.account, not here.
-- ============================================================================

-- src: db/src/ClientManager.cpp:3542, :3689, :3700, :4097
-- price_type ordinal == EItemShopPriceType (1 coin, 2 jeton). offerTime / addedTime are read as strings, so they must not be
-- NULL; '0000-00-00 00:00:00' means "no time" (mktime() < 0 is clamped to 0).
-- UNSURE: relies on zero-dates being allowed (no NO_ZERO_DATE in sql_mode).
CREATE TABLE IF NOT EXISTS `ishop_data` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `categoryType` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `categorySubType` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `itemVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `priceType` ENUM('COIN','JETON') NOT NULL DEFAULT 'COIN',
  `itemPrice` BIGINT NOT NULL DEFAULT 0,
  `discount` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `offerTime` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
  `addedTime` DATETIME NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sellCount` BIGINT NOT NULL DEFAULT 0,
  `week_limit` INT NOT NULL DEFAULT 0,
  `month_limit` INT NOT NULL DEFAULT 0,
  `maxSellCount` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `category_idx` (`categoryType`, `categorySubType`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: db/src/ClientManager.cpp:3790 (SELECT *, column order matters), :3982, :4016, :4053
CREATE TABLE IF NOT EXISTS `ishop_log` (
  `accountID` INT UNSIGNED NOT NULL DEFAULT 0,
  `playerName` VARCHAR(48) NOT NULL DEFAULT '',
  `buyDate` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `buyTime` INT NOT NULL DEFAULT 0,
  `ipAdress` VARCHAR(15) NOT NULL DEFAULT '',
  `itemID` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemCount` INT NOT NULL DEFAULT 0,
  `itemPrice` BIGINT NOT NULL DEFAULT 0,
  `itemPriceJD` BIGINT NOT NULL DEFAULT 0,
  KEY `account_idx` (`accountID`, `itemID`, `buyDate`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Game-side feature tables (game channels, DBManager)
-- ============================================================================

-- src: game/src/maintenance.cpp:102, :290, :309 (single-row table, only UPDATEd; the seed row below is required)
CREATE TABLE IF NOT EXISTS `maintenance` (
  `time` INT UNSIGNED NOT NULL DEFAULT 0,
  `duration` INT UNSIGNED NOT NULL DEFAULT 0,
  `reason` VARCHAR(128) NOT NULL DEFAULT 'no_reason'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/CollectionsSystem.cpp:29 (static data; empty table only logs an error)
CREATE TABLE IF NOT EXISTS `collections_categories` (
  `collection_index` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `name` VARCHAR(64) NOT NULL DEFAULT '',
  `reward_type0` INT UNSIGNED NOT NULL DEFAULT 0,
  `reward_value0` INT NOT NULL DEFAULT 0,
  `reward_type1` INT UNSIGNED NOT NULL DEFAULT 0,
  `reward_value1` INT NOT NULL DEFAULT 0,
  `reward_type2` INT UNSIGNED NOT NULL DEFAULT 0,
  `reward_value2` INT NOT NULL DEFAULT 0,
  `reward_type3` INT UNSIGNED NOT NULL DEFAULT 0,
  `reward_value3` INT NOT NULL DEFAULT 0,
  `reward_type4` INT UNSIGNED NOT NULL DEFAULT 0,
  `reward_value4` INT NOT NULL DEFAULT 0,
  `percent` INT UNSIGNED NOT NULL DEFAULT 0,
  `affect_id` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`collection_index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/CollectionsSystem.cpp:69
CREATE TABLE IF NOT EXISTS `collections_items` (
  `collectionIndex` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `itemIndex` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemVnum` INT UNSIGNED NOT NULL DEFAULT 0,
  `itemCount` INT UNSIGNED NOT NULL DEFAULT 1,
  PRIMARY KEY (`collectionIndex`, `itemIndex`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/dungeon_info.cpp:47 (static data, empty table is accepted)
-- name/img/entrance_dungeon/resistance_dungeon/force_dungeon are memcpy'd into char[100].
CREATE TABLE IF NOT EXISTS `date_dungeon` (
  `id` INT NOT NULL DEFAULT 0,
  `name` VARCHAR(99) NOT NULL DEFAULT '',
  `img` VARCHAR(99) NOT NULL DEFAULT '',
  `lv_min` INT NOT NULL DEFAULT 0,
  `lv_max` INT NOT NULL DEFAULT 0,
  `difficulty` INT NOT NULL DEFAULT 0,
  `party_max` INT NOT NULL DEFAULT 0,
  `respawn` INT UNSIGNED NOT NULL DEFAULT 0,
  `time_room` INT UNSIGNED NOT NULL DEFAULT 0,
  `entrance_dungeon` VARCHAR(99) NOT NULL DEFAULT '',
  `resistance_dungeon` VARCHAR(99) NOT NULL DEFAULT '',
  `force_dungeon` VARCHAR(99) NOT NULL DEFAULT '',
  `vnum_item` INT NOT NULL DEFAULT 0,
  `count_item` INT NOT NULL DEFAULT 0,
  `index_map` INT NOT NULL DEFAULT 0,
  `x_dungeon_join` INT NOT NULL DEFAULT 0,
  `y_dungeon_join` INT NOT NULL DEFAULT 0,
  `id_boss` INT NOT NULL DEFAULT 0,
  `x_map_npc` INT NOT NULL DEFAULT 0,
  `y_map_npc` INT NOT NULL DEFAULT 0,
  `vnum_mob_mision` INT NOT NULL DEFAULT 0,
  `count_mob_mision` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/dungeon_info.cpp:460, :477, :489, :506
CREATE TABLE IF NOT EXISTS `ranking_dungeon` (
  `id_player` INT UNSIGNED NOT NULL DEFAULT 0,
  `vnum_mob` INT NOT NULL DEFAULT 0,
  `name` VARCHAR(48) NOT NULL DEFAULT '',
  `kills` INT NOT NULL DEFAULT 0,
  `danger` INT NOT NULL DEFAULT 0,
  `time` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_player`, `vnum_mob`),
  KEY `vnum_mob_idx` (`vnum_mob`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/stone_event.cpp:61
-- UNSURE: write-only in the source (a single INSERT in the stone event); columns taken from that INSERT, no reader exists.
CREATE TABLE IF NOT EXISTS `mail_box` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `reader_name` VARCHAR(48) NOT NULL DEFAULT '',
  `sender_name` VARCHAR(48) NOT NULL DEFAULT '',
  `title` VARCHAR(64) NOT NULL DEFAULT '',
  `type` INT NOT NULL DEFAULT 0,
  `time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `post` TEXT NULL,
  `item_count` INT NOT NULL DEFAULT 0,
  `item_vnum` INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `reader_name_idx` (`reader_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- src: game/src/questmanager.cpp:109 (monthly TRUNCATE only; the commented-out code above it names player_login, tower_level, tower_time)
-- UNSURE: columns are guessed from that commented-out SELECT; nothing in the source inserts into it.
CREATE TABLE IF NOT EXISTS `sung_mahi_ranking` (
  `player_login` VARCHAR(48) NOT NULL DEFAULT '',
  `tower_level` INT NOT NULL DEFAULT 0,
  `tower_time` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`player_login`, `tower_level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- Seed data
-- ============================================================================

-- maintenance.cpp only UPDATEs this table, so one row must exist.
INSERT INTO `maintenance` (`time`, `duration`, `reason`)
SELECT 0, 0, 'no_reason' FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM `maintenance`);
