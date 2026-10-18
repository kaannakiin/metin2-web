-- DEPRECATED for orta-kolay: early shops now sell +9.
-- Use update_mid_pvp_shop_plus9.sql instead (or re-run seed_shop_refine_pet.sql).
-- Kept so old docs/scripts that reference this file fail loudly rather than re-trim to +0.
USE player;
SELECT 'Use sql/update_mid_pvp_shop_plus9.sql (orta-kolay +9 NPC)' AS msg;
