import importlib.util
from pathlib import Path
from types import SimpleNamespace as NS
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('pvp_support_ui', ROOT/'content/client/packs/root/pvp_support_ui.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)

class PolicyTest(unittest.TestCase):
    def test_slots_legacy_recovery_icons_and_repeat_install(self):
        item = NS(EQUIPMENT_BELT=7, COSTUME_SLOT_BODY=10, COSTUME_SLOT_WEAPON=13,
                  EQUIPMENT_MOUNT=20, EQUIPMENT_PET=21)
        equipped = {}
        player = NS(GetItemIndex=lambda cell: equipped.get(cell, 0), ATT_SPEED=7, MOVING_SPEED=8)
        class InventoryWindow:
            equip_info = [[0,0,0,32,32,'Body'],[7,0,0,32,32,'Belt']]
            costume_info = [[10,0,0,32,32,'Body'],[11,0,0,32,32,'Hair'],[13,0,0,32,32,'Weapon']]
            rings_info = [[19,0,0,32,32,'Pendant'],[20,0,0,32,32,'Mount'],[21,0,0,32,32,'Pet']]
            def __LoadWindow(self): pass
            def RefreshEquipSlotWindow(self): self.refreshed=True
        class AffectShower:
            DRAGON_GOD_DESC_IDX_START=1500
            RENEWAL_AFFECT_ICON='icon/affect/'
            AFFECT_DATA_DICT={}
        inv=NS(InventoryWindow=InventoryWindow,item=item,player=player)
        aff=NS(AffectShower=AffectShower,localeInfo=NS(TOOLTIP_ATT_SPEED='Attack +%d',TOOLTIP_MOV_SPEED='Move +%d'))
        policy.install(inv,aff)
        self.assertEqual([r[0] for r in InventoryWindow.costume_info],[10,13])
        self.assertEqual([r[0] for r in InventoryWindow.rings_info],[20,21])
        instance=InventoryWindow()
        appended=[]
        instance.wndCostume=NS(AppendSlot=lambda *args: appended.append(args))
        equipped[11]=45005
        instance.RefreshEquipSlotWindow()
        instance.RefreshEquipSlotWindow()
        self.assertEqual(len(appended),1)
        policy.install(inv,aff)
        self.assertEqual(len(AffectShower.AFFECT_DATA_DICT),2)

    def test_shared_proto_policy(self):
        self.assertEqual((ROOT/'apps/server/common/pvp_support_proto.h').read_bytes(),
                         (ROOT/'apps/client/source/GameLib/pvp_support_proto.h').read_bytes())

if __name__=='__main__': unittest.main()
