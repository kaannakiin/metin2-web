#include "StdAfx.h"
#include "Packet.h"
#include "GameType.h"

std::string g_strResourcePath = "d:/ymir work/";
std::string g_strImagePath = "d:/ymir work/ui/";

std::string g_strGuildSymbolPathName = "mark/10/";

// DEFAULT_FONT
static std::string gs_strDefaultFontName = "±¼¸²Ã¼:12.fnt";
static std::string gs_strDefaultItalicFontName = "±¼¸²Ã¼:12i.fnt";

#ifdef ENABLE_UI_DEBUG_WINDOW
CResource* gs_pkDefaultFont = nullptr;
#else
static CResource* gs_pkDefaultFont = nullptr;
#endif
static CResource* gs_pkDefaultItalicFont = nullptr;

static bool gs_isReloadDefaultFont = false;

void DefaultFont_Startup()
{
	gs_pkDefaultFont = nullptr;
}

void DefaultFont_Cleanup()
{
	if (gs_pkDefaultFont)
	{
		gs_pkDefaultFont->Release();
	}
}

void DefaultFont_SetName(const char* c_szFontName)
{
	gs_strDefaultFontName = c_szFontName;
	gs_strDefaultFontName += ".fnt";

	gs_strDefaultItalicFontName = c_szFontName;
	if (strchr (c_szFontName, ':'))
	{
		gs_strDefaultItalicFontName += "i";
	}
	gs_strDefaultItalicFontName += ".fnt";

	gs_isReloadDefaultFont = true;
}

bool ReloadDefaultFonts()
{
	CResourceManager& rkResMgr = CResourceManager::Instance();

	gs_isReloadDefaultFont = false;

	CResource* pkNewFont = rkResMgr.GetResourcePointer(gs_strDefaultFontName.c_str());
	pkNewFont->AddReference();
	if (gs_pkDefaultFont)
	{
		gs_pkDefaultFont->Release();
	}
	gs_pkDefaultFont = pkNewFont;

	CResource* pkNewItalicFont = rkResMgr.GetResourcePointer(gs_strDefaultItalicFontName.c_str());
	pkNewItalicFont->AddReference();
	if (gs_pkDefaultItalicFont)
	{
		gs_pkDefaultItalicFont->Release();
	}
	gs_pkDefaultItalicFont = pkNewItalicFont;

	return true;
}

CResource* DefaultFont_GetResource()
{
	if (!gs_pkDefaultFont || gs_isReloadDefaultFont)
	{
		ReloadDefaultFonts();
	}
	return gs_pkDefaultFont;
}

CResource* DefaultItalicFont_GetResource()
{
	if (!gs_pkDefaultItalicFont || gs_isReloadDefaultFont)
	{
		ReloadDefaultFonts();
	}
	return gs_pkDefaultItalicFont;
}

// END_OF_DEFAULT_FONT

void SetGuildSymbolPath(const char* c_szPathName)
{
	g_strGuildSymbolPathName = "mark/";
	g_strGuildSymbolPathName += c_szPathName;
	g_strGuildSymbolPathName += "/";
}

const char* GetGuildSymbolFileName(DWORD dwGuildID)
{
	return _getf("%s%03d.jpg", g_strGuildSymbolPathName.c_str(), dwGuildID);
}

BYTE c_aSlotTypeToInvenType[SLOT_TYPE_MAX] =
{
	RESERVED_WINDOW,		// SLOT_TYPE_NONE
	INVENTORY,				// SLOT_TYPE_INVENTORY
	RESERVED_WINDOW,		// SLOT_TYPE_SKILL
	RESERVED_WINDOW,		// SLOT_TYPE_EMOTION
	RESERVED_WINDOW,		// SLOT_TYPE_SHOP
	RESERVED_WINDOW,		// SLOT_TYPE_EXCHANGE_OWNER
	RESERVED_WINDOW,		// SLOT_TYPE_EXCHANGE_TARGET
	RESERVED_WINDOW,		// SLOT_TYPE_QUICK_SLOT
	RESERVED_WINDOW,		// SLOT_TYPE_SAFEBOX
	RESERVED_WINDOW,		// SLOT_TYPE_PRIVATE_SHOP
	RESERVED_WINDOW,		// SLOT_TYPE_MALL
	DRAGON_SOUL_INVENTORY,	// SLOT_TYPE_DRAGON_SOUL_INVENTORY
	BELT_INVENTORY,			// SLOT_TYPE_BELT_INVENTORY
#ifdef ENABLE_RENEWAL_SWITCHBOT
	SWITCHBOT,				// SLOT_TYPE_SWITCHBOT
#endif
#ifdef ENABLE_SPECIAL_INVENTORY
	INVENTORY,				// SLOT_TYPE_SKILL_BOOK_INVENTORY
	INVENTORY,				// SLOT_TYPE_MATERIAL_INVENTORY
	INVENTORY,				// SLOT_TYPE_STONE_INVENTORY
	INVENTORY,				// SLOT_TYPE_GIFT_BOX_INVENTORY
	INVENTORY,				// SLOT_TYPE_CHANGERS_INVENTORY
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
	AURA_REFINE,			// SLOT_TYPE_AURA
#endif
#ifdef ENABLE_CHANGE_LOOK_SYSTEM
	RESERVED_WINDOW,		// SLOT_TYPE_CHANGE_LOOK
#endif
};

BYTE SlotTypeToInvenType(BYTE bSlotType)
{
	if (bSlotType >= SLOT_TYPE_MAX)
	{
		return RESERVED_WINDOW;
	}
	else
	{
		return c_aSlotTypeToInvenType[bSlotType];
	}
}

#ifdef ENABLE_AURA_COSTUME_SYSTEM
static int s_aiAuraRefineInfo[CItemData::AURA_GRADE_MAX_NUM][AURA_REFINE_INFO_MAX] = {
	{1,   1,  49,  1000, 30617, 10,  5000000, 100},
	{2,  50,  99,  2000, 31136, 10,  5000000, 100},
	{3, 100, 149,  4000, 31137, 10,  5000000, 100},
	{4, 150, 199,  8000, 31138, 10,  8000000, 100},
	{5, 200, 249, 16000, 31138, 20, 10000000, 100},
	{6, 250, 250,     0,     0,  0,        0,   0},
	{0,   0,   0,     0,     0,  0,        0,   0}
};

int* GetAuraRefineInfo(BYTE bLevel)
{
	if (bLevel > 250)
		return NULL;

	for (int i = 0; i < CItemData::AURA_GRADE_MAX_NUM + 1; ++i)
	{
		if (bLevel >= s_aiAuraRefineInfo[i][AURA_REFINE_INFO_LEVEL_MIN] && bLevel <= s_aiAuraRefineInfo[i][AURA_REFINE_INFO_LEVEL_MAX])
			return s_aiAuraRefineInfo[i];
	}

	return NULL;
}
#endif

#ifndef ENABLE_CONQUEROR_LEVEL
typedef struct SApplyInfo
{
	BYTE	bPointType;
} TApplyInfo;

const TApplyInfo aApplyInfo[CItemData::MAX_APPLY_NUM] =
{
	{ POINT_NONE,						},
	{ POINT_MAX_HP,		        		},
	{ POINT_MAX_SP,		        		},
	{ POINT_HT,			        		},
	{ POINT_IQ,			        		},
	{ POINT_ST,			        		},
	{ POINT_DX,			        		},
	{ POINT_ATT_SPEED,		    		},
	{ POINT_MOV_SPEED,		    		},
	{ POINT_CASTING_SPEED,	    		},
	{ POINT_HP_REGEN,					},
	{ POINT_SP_REGEN,					},
	{ POINT_POISON_PCT,		    		},
	{ POINT_STUN_PCT,		    		},
	{ POINT_SLOW_PCT,		    		},
	{ POINT_CRITICAL_PCT,				},
	{ POINT_PENETRATE_PCT,				},
	{ POINT_ATTBONUS_HUMAN,				},
	{ POINT_ATTBONUS_ANIMAL,			},
	{ POINT_ATTBONUS_ORC,				},
	{ POINT_ATTBONUS_MILGYO,			},
	{ POINT_ATTBONUS_UNDEAD,			},
	{ POINT_ATTBONUS_DEVIL,				},
	{ POINT_STEAL_HP,					},
	{ POINT_STEAL_SP,					},
	{ POINT_MANA_BURN_PCT,				},
	{ POINT_DAMAGE_SP_RECOVER,			},
	{ POINT_BLOCK,		        		},
	{ POINT_DODGE,		        		},
	{ POINT_RESIST_SWORD,				},
	{ POINT_RESIST_TWOHAND,				},
	{ POINT_RESIST_DAGGER,				},
	{ POINT_RESIST_BELL,				},
	{ POINT_RESIST_FAN,					},
	{ POINT_RESIST_BOW,					},
	{ POINT_RESIST_FIRE,				},
	{ POINT_RESIST_ELEC,				},
	{ POINT_RESIST_MAGIC,				},
	{ POINT_RESIST_WIND,				},
	{ POINT_REFLECT_MELEE,				},
	{ POINT_REFLECT_CURSE,				},
	{ POINT_POISON_REDUCE,				},
	{ POINT_KILL_SP_RECOVER,			},
	{ POINT_EXP_DOUBLE_BONUS,			},
	{ POINT_GOLD_DOUBLE_BONUS,			},
	{ POINT_ITEM_DROP_BONUS,			},
	{ POINT_POTION_BONUS,				},
	{ POINT_KILL_HP_RECOVER,			},
	{ POINT_IMMUNE_STUN,				},
	{ POINT_IMMUNE_SLOW,				},
	{ POINT_IMMUNE_FALL,				},
	{ POINT_NONE,						},
	{ POINT_BOW_DISTANCE,				},
	{ POINT_ATT_GRADE_BONUS,			},
	{ POINT_DEF_GRADE_BONUS,			},
	{ POINT_MAGIC_ATT_GRADE_BONUS,		},
	{ POINT_MAGIC_DEF_GRADE_BONUS,		},
	{ POINT_CURSE_PCT,					},
	{ POINT_MAX_STAMINA					},
	{ POINT_ATTBONUS_WARRIOR,			},
	{ POINT_ATTBONUS_ASSASSIN,			},
	{ POINT_ATTBONUS_SURA,				},
	{ POINT_ATTBONUS_SHAMAN,			},
	{ POINT_ATTBONUS_MONSTER,			},
	{ POINT_ATT_BONUS					},
	{ POINT_MALL_DEFBONUS				},
	{ POINT_MALL_EXPBONUS				},
	{ POINT_MALL_ITEMBONUS				},
	{ POINT_MALL_GOLDBONUS				},
	{ POINT_MAX_HP_PCT					},
	{ POINT_MAX_SP_PCT					},
	{ POINT_SKILL_DAMAGE_BONUS			},
	{ POINT_NORMAL_HIT_DAMAGE_BONUS		},
	{ POINT_SKILL_DEFEND_BONUS			},
	{ POINT_NORMAL_HIT_DEFEND_BONUS		},
	{ POINT_PC_BANG_EXP_BONUS			},
	{ POINT_PC_BANG_DROP_BONUS			},
	{ POINT_NONE,						},
	{ POINT_RESIST_WARRIOR,				},
	{ POINT_RESIST_ASSASSIN,			},
	{ POINT_RESIST_SURA,				},
	{ POINT_RESIST_SHAMAN,				},
	{ POINT_ENERGY						},
	{ POINT_DEF_GRADE					},
	{ POINT_COSTUME_ATTR_BONUS			},
	{ POINT_MAGIC_ATT_BONUS_PER 		},
	{ POINT_MELEE_MAGIC_ATT_BONUS_PER	},
	{ POINT_RESIST_ICE,					},
	{ POINT_RESIST_EARTH,				},
	{ POINT_RESIST_DARK,				},
	{ POINT_RESIST_CRITICAL,			},
	{ POINT_RESIST_PENETRATE,			},
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	{ POINT_ACCEDRAIN_RATE,				},
#endif
#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
	{ POINT_RESIST_MAGIC_REDUCTION,		},
#endif
	{ POINT_ENCHANT_ELECT,				},
	{ POINT_ENCHANT_FIRE,				},
	{ POINT_ENCHANT_ICE,				},
	{ POINT_ENCHANT_WIND,				},
	{ POINT_ENCHANT_EARTH,				},
	{ POINT_ENCHANT_DARK,				},
	{ POINT_ATTBONUS_CZ,				},
	{ POINT_ATTBONUS_INSECT,			},
	{ POINT_ATTBONUS_DESERT,			},
	{ POINT_ATTBONUS_SWORD,				},
	{ POINT_ATTBONUS_TWOHAND,			},
	{ POINT_ATTBONUS_DAGGER,			},
	{ POINT_ATTBONUS_BELL,				},
	{ POINT_ATTBONUS_FAN,				},
	{ POINT_ATTBONUS_BOW,				},
	{ POINT_RESIST_HUMAN,				},
	{ POINT_RESIST_MOUNT_FALL,			},
	{ POINT_NONE,						},
#ifdef ENABLE_MOUNT_COSTUME_EX_SYSTEM
	{ POINT_MOUNT,						},
#endif
#ifdef ENABLE_NEW_BONUS_SYSTEM
	{ POINT_ATTBONUS_STONE,				},
	{ POINT_ATTBONUS_BOSS,				},
	{ POINT_ATTBONUS_ELEMENTS,			},
	{ POINT_ENCHANT_ELEMENTS,			},
	{ POINT_ATTBONUS_CHARACTERS,		},
	{ POINT_ENCHANT_CHARACTERS,			},
	{ POINT_RESIST_MONSTER,				},
#endif
#ifdef ENABLE_AVG_PVM
	{ POINT_ATTBONUS_MEDI_PVM,			},
#endif
	{ POINT_ATTBONUS_PVM_STR, 			},
	{ POINT_ATTBONUS_PVM_BERSERKER, 	},
#ifdef ENABLE_CONQUEROR_LEVEL
	{ POINT_SUNGMA_STR, 				},
	{ POINT_SUNGMA_HP, 					},
	{ POINT_SUNGMA_MOVE, 				},
	{ POINT_SUNGMA_IMMUNE, 				},
	//{ POINT_CONQUEROR_POINT, 			},
#endif
};

BYTE ApplyTypeToPointType(BYTE bApplyType)
{
	if (bApplyType >= CItemData::MAX_APPLY_NUM)
		return POINT_NONE;
	else
		return aApplyInfo[bApplyType].bPointType;
}
#endif