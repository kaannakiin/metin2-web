#ifndef __INC_METIN_II_GAME_PVP_SAFE_MAPS_H__
#define __INC_METIN_II_GAME_PVP_SAFE_MAPS_H__

// Mid-easy 1-99 PvP (PVP_HEDEF.md): PC–PC attack denied on these map indexes.
// Villages, guild lands, OX, duel lobby, wedding, trade/event hubs.
// Farm maps intentionally absent → free PvP via existing PK mode rules.

inline bool IsMidPvpSafeMap(long lMapIndex)
{
	static const long kMidPvpSafeMapIndex[] =
	{
		1, 21, 41,			// empire villages
		6, 26, 46,			// guild villages
		4, 24, 44,			// guild lands
		81,					// wedding
		112,				// duel lobby
		113,				// ox event
		200,				// gm guild build
		230,				// event map
		231,				// trade map
	};

	for (size_t i = 0; i < sizeof(kMidPvpSafeMapIndex) / sizeof(kMidPvpSafeMapIndex[0]); ++i)
	{
		if (kMidPvpSafeMapIndex[i] == lMapIndex)
			return true;
	}
	return false;
}

#endif
