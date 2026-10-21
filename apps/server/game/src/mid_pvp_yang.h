#pragma once

inline constexpr int MID_PVP_MAP_GOLD_CAP = 800000;

// Nominal totals on a successful Yang roll at mob_gold=400. Personal
// modifiers and the existing kill cap are applied by RewardGold afterwards.
struct MidPvpYangBand
{
    long map;
    int mobMin;
    int mobMax;
    int stoneMin;
    int stoneMax;
};

inline const MidPvpYangBand* GetMidPvpYangBand(long mapIndex)
{
    if (mapIndex >= 10000)
        mapIndex /= 10000;
    static const MidPvpYangBand bands[] = {
        {1, 400, 1000, 20000, 50000},
        {21, 400, 1000, 20000, 50000},
        {41, 400, 1000, 20000, 50000},
        {3, 1500, 3000, 80000, 120000},
        {23, 1500, 3000, 80000, 120000},
        {43, 1500, 3000, 80000, 120000},
        {64, 3000, 6000, 160000, 240000},
        {63, 5000, 10000, 240000, 360000},
        {61, 5000, 10000, 240000, 360000},
        {62, 8000, 14000, 360000, 500000},
        {67, 12000, 20000, 500000, 600000},
        {68, 16000, 30000, 600000, 800000},
        {104, 2000, 5000, 0, 0},
        {71, 2000, 5000, 0, 0},
        {217, 2000, 5000, 0, 0},
        {72, 6000, 12000, 0, 0},
        {73, 6000, 12000, 0, 0},
    };
    for (const auto& band : bands)
        if (band.map == mapIndex)
            return &band;
    return nullptr;
}
