-- Orta-kolay: early NPC +9 (trimmed 1-99 ladder). Apply on player DB.
USE player;

DELETE FROM shop_item WHERE shop_vnum = 1;
INSERT INTO shop_item (shop_vnum, item_vnum, `count`) VALUES
(1,49,1),(1,1019,1),(1,2039,1),(1,3039,1),(1,4009,1),(1,5019,1),(1,7039,1),
(1,8000,50),(1,8001,50),(1,8002,50);

DELETE FROM shop_item WHERE shop_vnum = 2;
INSERT INTO shop_item (shop_vnum, item_vnum, `count`) VALUES
(2,11229,1),(2,11429,1),(2,11629,1),(2,11829,1),
(2,12209,1),(2,12349,1),(2,12489,1),(2,12629,1),
(2,13009,1),
(2,14009,1),(2,14029,1),(2,14049,1),
(2,15009,1),(2,15029,1),(2,15049,1),
(2,16009,1),(2,16029,1),
(2,17009,1),(2,17029,1);

DELETE FROM shop_item WHERE shop_vnum = 6;
INSERT INTO shop_item (shop_vnum, item_vnum, `count`) VALUES
(6,59,1),(6,1029,1),(6,2049,1),(6,3049,1),(6,5029,1),(6,7049,1),
(6,8003,50),(6,8004,50),(6,8005,50);

DELETE FROM shop_item WHERE shop_vnum = 7;
INSERT INTO shop_item (shop_vnum, item_vnum, `count`) VALUES
(7,12229,1),(7,12369,1),(7,12509,1),(7,12649,1),
(7,13029,1),(7,13189,1),
(7,14069,1),
(7,16049,1),(7,16069,1),
(7,17049,1),(7,17069,1);

DELETE FROM shop_item WHERE shop_vnum = 11;
