-- Scoped transition to ShopEx. Other NPC shops remain intact.
USE player;
START TRANSACTION;
DELETE FROM shop_item WHERE shop_vnum IN (1,2,3,6,7);
DELETE FROM shop WHERE vnum IN (1,2,3,6,7);
REPLACE INTO quest (dwPID,szName,szState,lValue) VALUES
(0,'mob_gold','',400),(0,'mob_gold_buyer','',400);
COMMIT;
