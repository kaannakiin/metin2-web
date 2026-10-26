# -*- coding: ascii -*-
"""Shared Windows/web presentation policy; wire constants stay unchanged."""

def install(inventory, affects):
    cls = inventory.InventoryWindow
    if getattr(cls, "_pvp_support_installed", False):
        return
    item = inventory.item
    player = inventory.player
    allowed_costume = (item.COSTUME_SLOT_BODY, item.COSTUME_SLOT_WEAPON)
    allowed_extra = (item.EQUIPMENT_MOUNT, item.EQUIPMENT_PET)
    removed = []
    for name, window, keep in (
        ("equip_info", "wndEquip", lambda row: row[0] != item.EQUIPMENT_BELT),
        ("costume_info", "wndCostume", lambda row: row[0] in allowed_costume),
        ("rings_info", "wndRings", lambda row: row[0] in allowed_extra),
    ):
        rows = getattr(cls, name)
        removed.extend((window, row) for row in rows if not keep(row))
        setattr(cls, name, [row for row in rows if keep(row)])

    refresh = cls.RefreshEquipSlotWindow
    def refresh_slots(self):
        # A legacy equipped item remains reachable for unequip; never hide property.
        for window, row in removed:
            if player.GetItemIndex(row[0]):
                slots = getattr(self, window)
                if not hasattr(self, "_pvp_legacy_slots"):
                    self._pvp_legacy_slots = set()
                key = (window, row[0])
                if key not in self._pvp_legacy_slots:
                    slots.AppendSlot(row[0], row[1], row[2], row[3], row[4])
                    self._pvp_legacy_slots.add(key)
        return refresh(self)
    cls.RefreshEquipSlotWindow = refresh_slots

    load = cls._InventoryWindow__LoadWindow
    def load_window(self):
        result = load(self)
        for name in ("CostumeHairButton", "CostumeAcceButton", "CostumeAuraButton"):
            if self.IsChild(name):
                self.GetChild(name).Hide()
        return result
    cls._InventoryWindow__LoadWindow = load_window

    shower = affects.AffectShower
    start = shower.DRAGON_GOD_DESC_IDX_START
    icons = shower.RENEWAL_AFFECT_ICON
    shower.AFFECT_DATA_DICT[start + player.ATT_SPEED] = (
        affects.localeInfo.TOOLTIP_ATT_SPEED, icons + "affect_13.png")
    shower.AFFECT_DATA_DICT[start + player.MOVING_SPEED] = (
        affects.localeInfo.TOOLTIP_MOV_SPEED, icons + "affect_14.png")
    cls._pvp_support_installed = True
