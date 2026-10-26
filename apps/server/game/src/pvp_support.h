#ifndef METIN2_PVP_SUPPORT_H
#define METIN2_PVP_SUPPORT_H
#include "../../common/pvp_support_proto.h"
#include "constants.h"
#include "pvp_equipment.h"

namespace pvp_support
{
inline bool PermanentAffect(unsigned type)
{
    return type == AFFECT_BLEND_PLUS || type == AFFECT_MALL_PLUS;
}
inline unsigned Family(LPITEM item)
{
    return item->GetVnum() <= 50832 ? AFFECT_BLEND_PLUS : AFFECT_MALL_PLUS;
}
inline void RemoveTemporary(CHARACTER* ch, LPITEM item, unsigned point)
{
    unsigned family = Family(item) == AFFECT_BLEND_PLUS ? AFFECT_BLEND : AFFECT_MALL;
    if (CAffect* affect = ch->FindAffect(family, point))
        ch->RemoveAffect(affect);
    if (item->GetVnum() == 72737 || item->GetVnum() == 72738)
    {
        unsigned speed = item->GetVnum() == 72737 ? AFFECT_ATT_SPEED : AFFECT_MOV_SPEED;
        if (CAffect* affect = ch->FindAffect(speed, point))
            ch->RemoveAffect(affect);
        if (CAffect* affect = ch->FindAffect(AFFECT_UNIQUE_ABILITY, point))
            ch->RemoveAffect(affect);
    }
}
inline bool Toggle(CHARACTER* ch, LPITEM item)
{
    const int apply = item->GetValue(0);
    if (apply <= 0 || apply >= MAX_APPLY_NUM || ch->IsDead() || !ch->IsLoadedAffect())
        return false;
    const unsigned point = aApplyInfo[apply].bPointType;
    const unsigned family = Family(item);
    if (item->GetSocket(1) == 1)
    {
        if (CAffect* affect = ch->FindAffect(family, point))
            ch->RemoveAffect(affect);
        item->SetSocket(1, 0);
        item->Lock(false);
        return true;
    }
    if (ch->FindAffect(family, point))
        return false;
    RemoveTemporary(ch, item, point);
    if (!ch->AddAffect(family, point, item->GetValue(1), 0, INFINITE_AFFECT_DURATION, 0, false))
        return false;
    item->SetSocket(1, 1);
    item->Lock(true);
    return true;
}
// An owned item's socket is authoritative; orphan saved bonuses are discarded.
inline void Restore(CHARACTER* ch)
{
    ch->RemoveAffect(AFFECT_BLEND_PLUS);
    ch->RemoveAffect(AFFECT_MALL_PLUS);
    for (unsigned cell = 0; cell < INVENTORY_MAX_NUM; ++cell)
    {
        LPITEM item = ch->GetInventoryItem(cell);
        if (!item || !IsPermanent(item->GetVnum()))
            continue;
        item->Lock(false);
        if (item->GetSocket(1) != 1)
            continue;
        const int apply = item->GetValue(0);
        if (apply <= 0 || apply >= MAX_APPLY_NUM)
            continue;
        const unsigned point = aApplyInfo[apply].bPointType;
        const unsigned family = Family(item);
        if (ch->FindAffect(family, point))
        {
            item->SetSocket(1, 0);
            continue;
        }
        RemoveTemporary(ch, item, point);
        if (ch->AddAffect(family, point, item->GetValue(1), 0, INFINITE_AFFECT_DURATION, 0, false))
            item->Lock(true);
    }
}
}
#endif
