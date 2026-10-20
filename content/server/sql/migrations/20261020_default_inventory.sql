-- Four standard inventory pages for existing and future characters.
-- Apply while Metin2 game/db services are stopped so cached players cannot
-- overwrite this change. Existing inventory slot positions stay unchanged.
ALTER TABLE player.player ALTER COLUMN inventory_0 SET DEFAULT 18;
UPDATE player.player SET inventory_0 = 18 WHERE inventory_0 <> 18;
