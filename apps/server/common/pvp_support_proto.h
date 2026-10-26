#ifndef METIN2_PVP_SUPPORT_PROTO_H
#define METIN2_PVP_SUPPORT_PROTO_H

// Kept byte-identical with the client GameLib header. No packet layout changes.
namespace pvp_support
{
inline bool IsPermanent(unsigned vnum)
{
    return (vnum >= 50827 && vnum <= 50832) || (vnum >= 72731 && vnum <= 72738);
}

template <typename Table>
void Configure(Table& table, unsigned affectPlusSubtype, unsigned levelLimit)
{
    if (!IsPermanent(table.dwVnum))
        return;
    for (unsigned i = 0; i < 2; ++i)
    {
        table.aLimits[i].bType = i == 0 ? levelLimit : 0;
        table.aLimits[i].lValue = i == 0 ? 1 : 0;
    }
    // A permanent toggle must never merge with another item's active socket.
    table.dwFlags &= ~(1u << 2); // ITEM_FLAG_STACKABLE
    if (table.dwVnum == 72737 || table.dwVnum == 72738)
    {
        table.bSubType = affectPlusSubtype;
        table.dwVnumRange = 0;
        for (unsigned i = 0; i < 6; ++i)
            table.alValues[i] = 0;
        table.alValues[0] = table.dwVnum == 72737 ? 7 : 8; // APPLY_ATT/MOV_SPEED
        table.alValues[1] = table.dwVnum == 72737 ? 30 : 40;
        table.alValues[2] = 1; // Existing MALL_PLUS family; yellow dew stays separate.
    }
}
}
#endif
