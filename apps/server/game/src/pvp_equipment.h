#ifndef METIN2_PVP_EQUIPMENT_H
#define METIN2_PVP_EQUIPMENT_H
namespace pvp_support
{
inline bool DisabledEquipment(unsigned type, unsigned subtype)
{
    if (type == ITEM_ARMOR)
        return subtype >= ARMOR_BELT;
    if (type == ITEM_COSTUME)
        return subtype != COSTUME_BODY && subtype != COSTUME_WEAPON;
    if (type == ITEM_RING || type == ITEM_DS || type == ITEM_SPECIAL_DS)
        return true;
#ifdef ENABLE_GROWTH_PET_SYSTEM
    if (type == ITEM_GROWTH_PET)
        return true;
#endif
#ifdef ENABLE_PASSIVE_SYSTEM
    if (type == ITEM_PASSIVE)
        return true;
#endif
    return false;
}
}
#endif
