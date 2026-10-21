#pragma once

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
        {1, 200, 500, 10000, 25000},
        {21, 200, 500, 10000, 25000},
        {41, 200, 500, 10000, 25000},
        {3, 750, 1500, 40000, 60000},
        {23, 750, 1500, 40000, 60000},
        {43, 750, 1500, 40000, 60000},
        {64, 1500, 3000, 80000, 120000},
        {63, 2500, 5000, 120000, 180000},
        {61, 2500, 5000, 120000, 180000},
        {62, 4000, 7000, 180000, 250000},
        {67, 6000, 10000, 250000, 300000},
        {68, 8000, 15000, 300000, 400000},
        {104, 1000, 2500, 0, 0},
        {71, 1000, 2500, 0, 0},
        {217, 1000, 2500, 0, 0},
        {72, 3000, 6000, 0, 0},
        {73, 3000, 6000, 0, 0},
    };
    for (const auto& band : bands)
        if (band.map == mapIndex)
            return &band;
    return nullptr;
}
