-- Compatibility entry point: active +9 shops now live in shop_table_ex.txt.
-- Standard and ShopEx registrations cannot coexist for the same NPC.
USE player;
DELETE FROM shop_item WHERE shop_vnum IN (1,2,3,6,7);
DELETE FROM shop WHERE vnum IN (1,2,3,6,7);
