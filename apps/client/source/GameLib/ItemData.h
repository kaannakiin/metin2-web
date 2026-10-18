#pragma once

#include "StdAfx.h"

#include "../EterLib/GrpSubImage.h"
#include "../EterGrnLib/Thing.h"
#include "../UserInterface/Locale_inc.h"

class CItemData
{
	public:
		enum
		{
			ITEM_NAME_MAX_LEN = 48,
			ITEM_LIMIT_MAX_NUM = 2,
			ITEM_VALUES_MAX_NUM = 6,
			ITEM_SMALL_DESCR_MAX_LEN = 256,
			ITEM_APPLY_MAX_NUM = 3,
			ITEM_SOCKET_MAX_NUM = 3,
#ifdef ENABLE_BONUS_COSTUME_SYSTEM
			COSTUME_ATTRIBUTE_MAX_NUM = 3,
#endif
		};

		enum EItemType
		{
			ITEM_TYPE_NONE,					// 0
			ITEM_TYPE_WEAPON,				// 1
			ITEM_TYPE_ARMOR,				// 2
			ITEM_TYPE_USE,					// 3
			ITEM_TYPE_AUTOUSE,				// 4
			ITEM_TYPE_MATERIAL,				// 5
			ITEM_TYPE_SPECIAL,				// 6
			ITEM_TYPE_TOOL,					// 7
			ITEM_TYPE_LOTTERY,				// 8
			ITEM_TYPE_ELK,					// 9
			ITEM_TYPE_METIN,				// 10
			ITEM_TYPE_CONTAINER,			// 11
			ITEM_TYPE_FISH,					// 12
			ITEM_TYPE_ROD,					// 13
			ITEM_TYPE_RESOURCE,				// 14
			ITEM_TYPE_CAMPFIRE,				// 15
			ITEM_TYPE_UNIQUE,				// 16
			ITEM_TYPE_SKILLBOOK,			// 17
			ITEM_TYPE_QUEST,				// 18
			ITEM_TYPE_POLYMORPH,			// 19
			ITEM_TYPE_TREASURE_BOX,			// 20
			ITEM_TYPE_TREASURE_KEY,			// 21
			ITEM_TYPE_SKILLFORGET,			// 22
			ITEM_TYPE_GIFTBOX,				// 23
			ITEM_TYPE_PICK,					// 24
			ITEM_TYPE_HAIR,					// 25
			ITEM_TYPE_TOTEM,				// 26
			ITEM_TYPE_BLEND,				// 27
			ITEM_TYPE_COSTUME,				// 28
			ITEM_TYPE_DS,					// 29
			ITEM_TYPE_SPECIAL_DS,			// 30
			ITEM_TYPE_EXTRACT,				// 31
			ITEM_TYPE_SECONDARY_COIN,		// 32
			ITEM_TYPE_RING,					// 33
#ifdef ENABLE_MOUNT_SYSTEM
			ITEM_TYPE_MOUNT,				// 34
#endif
#ifdef ENABLE_PET_SYSTEM
			ITEM_TYPE_PET,					// 35
#endif
#ifdef ENABLE_GROWTH_PET_SYSTEM
			ITEM_TYPE_GROWTH_PET,			// 36
#endif
#ifdef ENABLE_NEW_ITEM_TYPE_GACHA
			ITEM_TYPE_GACHA,				// 37 gacha
#endif
#ifdef ENABLE_PASSIVE_SYSTEM
			ITEM_TYPE_PASSIVE,				// 38 passive
#endif

			ITEM_TYPE_MAX_NUM,
		};

		enum EWeaponSubTypes
		{
			WEAPON_SWORD, //0
			WEAPON_DAGGER,
			WEAPON_BOW, //2
			WEAPON_TWO_HANDED, //3
			WEAPON_BELL, //4
			WEAPON_FAN, //5
			WEAPON_ARROW, //6
			WEAPON_QUIVER, //7
			WEAPON_NUM_TYPES, //11 2015/11/12

			WEAPON_NONE = WEAPON_NUM_TYPES+1,
		};

		enum EMaterialSubTypes
		{
			MATERIAL_LEATHER,
			MATERIAL_BLOOD,
			MATERIAL_ROOT,
			MATERIAL_NEEDLE,
			MATERIAL_JEWEL,
			MATERIAL_DS_REFINE_NORMAL,
			MATERIAL_DS_REFINE_BLESSED,
			MATERIAL_DS_REFINE_HOLLY,
#ifdef ENABLE_PASSIVE_SYSTEM
			MATERIAL_PASSIVE_WEAPON,
			MATERIAL_PASSIVE_ARMOR,
			MATERIAL_PASSIVE_ACCE,
			MATERIAL_PASSIVE_ELEMENT,
#endif
		};

		enum EArmorSubTypes
		{
			ARMOR_BODY,
			ARMOR_HEAD,
			ARMOR_SHIELD,
			ARMOR_WRIST,
			ARMOR_FOOTS,
			ARMOR_NECK,
			ARMOR_EAR,
			ARMOR_BELT,
#ifdef ENABLE_PENDANT_SYSTEM
			ARMOR_PENDANT,
#endif
			ARMOR_NUM_TYPES
		};

		enum ECostumeSubTypes
		{
			COSTUME_BODY,				//0
			COSTUME_HAIR,				//1
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
			COSTUME_ACCE,				//2
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
			COSTUME_WEAPON,				//3
#endif
#ifdef ENABLE_MOUNT_PET_SKIN
			COSTUME_MOUNT,				//4
			COSTUME_PET,				//5
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
			COSTUME_AURA,				//5
#endif
			COSTUME_NUM_TYPES,
		};

		enum EUseSubTypes
		{
			USE_POTION,
			USE_TALISMAN,
			USE_TUNING,
			USE_MOVE,
			USE_TREASURE_BOX,
			USE_MONEYBAG,
			USE_BAIT,
			USE_ABILITY_UP,
			USE_AFFECT,
			USE_CREATE_STONE,
			USE_SPECIAL,
			USE_POTION_NODELAY,
			USE_CLEAR,
			USE_INVISIBILITY,
			USE_DETACHMENT,
			USE_BUCKET,
			USE_POTION_CONTINUE,
			USE_CLEAN_SOCKET,
			USE_CHANGE_ATTRIBUTE,
			USE_ADD_ATTRIBUTE,
			USE_ADD_ACCESSORY_SOCKET,
			USE_PUT_INTO_ACCESSORY_SOCKET,
			USE_ADD_ATTRIBUTE2,
			USE_RECIPE,
			USE_CHANGE_ATTRIBUTE2,
			USE_BIND,
			USE_UNBIND,
			USE_TIME_CHARGE_PER,
			USE_TIME_CHARGE_FIX,
			USE_PUT_INTO_BELT_SOCKET,
			USE_PUT_INTO_RING_SOCKET,
#ifdef ENABLE_TITLE_SYSTEM
			USE_TITLE,
#endif
#ifdef ENABLE_RENEWAL_AFFECT
			USE_AFFECT_PLUS,
#endif
#ifdef ENABLE_BONUS_COSTUME_SYSTEM
			USE_CHANGE_COSTUME_ATTR,
			USE_RESET_COSTUME_ATTR,
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
			USE_PUT_INTO_AURA_SOCKET,
#endif
#ifdef ENABLE_COLLECTIONS_SYSTEM
			USE_COLLECTION_SCROLL,
#endif
		};

#ifdef ENABLE_PASSIVE_SYSTEM
		enum EPassiveSubTypes
		{
			PASSIVE_JOB,
		};
#endif

		enum EResourceSubTypes
		{
			RESOURCE_FISHBONE,
			RESOURCE_WATERSTONEPIECE,
			RESOURCE_WATERSTONE,
			RESOURCE_BLOOD_PEARL,
			RESOURCE_BLUE_PEARL,
			RESOURCE_WHITE_PEARL,
			RESOURCE_BUCKET,
			RESOURCE_CRYSTAL,
			RESOURCE_GEM,
			RESOURCE_STONE,
			RESOURCE_METIN,
			RESOURCE_ORE,
#ifdef ENABLE_AURA_COSTUME_SYSTEM
			RESOURCE_AURA,
#endif
		};

#ifdef ENABLE_GROWTH_PET_SYSTEM
		enum EPetSubTypes
		{
			PET_EGG,
			PET_UPBRINGING,
			PET_BAG,
			PET_FEEDSTUFF,
			PET_SKILL,
			PET_SKILL_DEL_BOOK,
			PET_NAME_CHANGE,
			PET_EXPFOOD,
			PET_SKILL_ALL_DEL_BOOK,
			PET_EXPFOOD_PER,
			PET_ATTR_DETERMINE,
			PET_ATTR_CHANGE,
			PET_PAY,
			PET_PRIMIUM_FEEDSTUFF,
		};

		enum EEggUse
		{
			EGG_USE_SUCCESS,
			EGG_USE_FAILED_BECAUSE_NAME,
			EGG_USE_FAILED_TIMEOVER,
		};

		enum EPetEggUse
		{
			PET_EGG_USE_TRUE,
			PET_EGG_USE_FAILED_BECAUSE_TRADING,
			PET_EGG_USE_FAILED_BECAUSE_SHOP_OPEN,
			PET_EGG_USE_FAILED_BECAUSE_MALL_OPEN,
			PET_EGG_USE_FAILED_BECAUSE_SAFEBOX_OPEN,
		};

		enum EPetNameChange
		{
			NAME_CHANGE_USE_SUCCESS,
			NAME_CHANGE_USE_FAILED_BECAUSE_NAME,
		};

		enum EPet
		{
			PET_ATTR_CHANGE_ITEMVNUM = 55033,
			PET_HATCHING_MONEY = 100000,
			PET_NAME_MAX_SIZE = 20,
			PET_NAME_MIN_SIZE = 4,
			E_SEAL_DATE_DEFAULT_TIMESTAMP = -1,
		};
#endif

		enum EWeddingItem
		{
			WEDDING_TUXEDO1 = 11901,
			WEDDING_TUXEDO2 = 11902,
			WEDDING_BRIDE_DRESS1 = 11903,
			WEDDING_BRIDE_DRESS2 = 11904,
			WEDDING_TUXEDO3 = 11911,
			WEDDING_TUXEDO4 = 11912,
			WEDDING_BRIDE_DRESS3 = 11913,
			WEDDING_BRIDE_DRESS4 = 11914,
			WEDDING_BOUQUET1 = 50201,
			WEDDING_BOUQUET2 = 50202,
		};

		enum EDragonSoulSubType
		{
			DS_SLOT1,
			DS_SLOT2,
			DS_SLOT3,
			DS_SLOT4,
			DS_SLOT5,
			DS_SLOT6,
			DS_SLOT_NUM_TYPES = 6,
		};

		enum EMetinSubTypes
		{
			METIN_NORMAL,
			METIN_GOLD,
		};

		enum ELimitTypes
		{
			LIMIT_NONE,
			LIMIT_LEVEL,
			LIMIT_STR,
			LIMIT_DEX,
			LIMIT_INT,
			LIMIT_CON,
			LIMIT_REAL_TIME,
			LIMIT_REAL_TIME_START_FIRST_USE,
			LIMIT_TIMER_BASED_ON_WEAR,
#ifdef ENABLE_PITTY_REFINE
			LIMIT_PITTY_REFINE,
#endif
			LIMIT_MAX_NUM
		};

		enum EItemAntiFlag
		{
			ITEM_ANTIFLAG_FEMALE		= (1 << 0),
			ITEM_ANTIFLAG_MALE			= (1 << 1),
			ITEM_ANTIFLAG_WARRIOR		= (1 << 2),
			ITEM_ANTIFLAG_ASSASSIN		= (1 << 3),
			ITEM_ANTIFLAG_SURA			= (1 << 4),
			ITEM_ANTIFLAG_SHAMAN		= (1 << 5),
			ITEM_ANTIFLAG_GET			= (1 << 6),
			ITEM_ANTIFLAG_DROP			= (1 << 7),
			ITEM_ANTIFLAG_SELL			= (1 << 8),
			ITEM_ANTIFLAG_EMPIRE_A		= (1 << 9),
			ITEM_ANTIFLAG_EMPIRE_B		= (1 << 10),
			ITEM_ANTIFLAG_EMPIRE_R		= (1 << 11),
			ITEM_ANTIFLAG_SAVE			= (1 << 12),
			ITEM_ANTIFLAG_GIVE			= (1 << 13),
			ITEM_ANTIFLAG_PKDROP		= (1 << 14),
			ITEM_ANTIFLAG_STACK			= (1 << 15),
			ITEM_ANTIFLAG_MYSHOP		= (1 << 16),
			ITEM_ANTIFLAG_SAFEBOX		= (1 << 17),
#ifdef ENABLE_DESTROY_DIALOG
			ITEM_ANTIFLAG_DESTROY		= (1 << 18),
#endif
#ifdef ENABLE_GROWTH_PET_SYSTEM
			ITEM_ANTIFLAG_PETFEED		= (1 << 19),
#endif
			ITEM_ANTIFLAG_RT_REMOVE		= (1 << 20),
		};

		enum EItemFlag
		{
			ITEM_FLAG_REFINEABLE		= (1 << 0),
			ITEM_FLAG_SAVE				= (1 << 1),
			ITEM_FLAG_STACKABLE			= (1 << 2),
			ITEM_FLAG_COUNT_PER_1GOLD	= (1 << 3),
			ITEM_FLAG_SLOW_QUERY		= (1 << 4),
			ITEM_FLAG_RARE				= (1 << 5),
			ITEM_FLAG_UNIQUE			= (1 << 6),
			ITEM_FLAG_MAKECOUNT			= (1 << 7),
			ITEM_FLAG_IRREMOVABLE		= (1 << 8),
			ITEM_FLAG_CONFIRM_WHEN_USE	= (1 << 9),
			ITEM_FLAG_QUEST_USE			= (1 << 10),
			ITEM_FLAG_QUEST_USE_MULTIPLE= (1 << 11),
			ITEM_FLAG_UNUSED03			= (1 << 12),
			ITEM_FLAG_LOG				= (1 << 13),
			ITEM_FLAG_APPLICABLE		= (1 << 14),
		};

		enum EWearPositions
		{
			WEAR_BODY,
			WEAR_HEAD,
			WEAR_FOOTS,
			WEAR_WRIST,
			WEAR_WEAPON,
			WEAR_NECK,
			WEAR_EAR,
			WEAR_UNIQUE1,
			WEAR_UNIQUE2,
			WEAR_ARROW,
			WEAR_SHIELD,

			WEAR_ABILITY1,
			WEAR_ABILITY2,
			WEAR_ABILITY3,
			WEAR_ABILITY4,
			WEAR_ABILITY5,
			WEAR_ABILITY6,
			WEAR_ABILITY7,
			WEAR_ABILITY8,
			WEAR_COSTUME_BODY,
			WEAR_COSTUME_HAIR,
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
			WEAR_COSTUME_ACCE,		// 21
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
			WEAR_COSTUME_WEAPON,		// 22
#endif
#ifdef ENABLE_MOUNT_PET_SKIN
			WEAR_COSTUME_MOUNT,		// 23
			WEAR_COSTUME_PET,		// 24
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
			WEAR_COSTUME_AURA,		// 25
#endif
			WEAR_RING1,		// 26
			WEAR_RING2,		// 27
			WEAR_BELT,		// 28
#ifdef ENABLE_MOUNT_SYSTEM
			WEAR_MOUNT,		// 29
#endif
#ifdef ENABLE_PET_SYSTEM
			WEAR_PET,		// 30
#endif
#ifdef ENABLE_PENDANT_SYSTEM
			WEAR_PENDANT,		// 31
#endif
#ifdef ENABLE_PASSIVE_SYSTEM
			WEAR_PASSIVE,			// 32
#endif

			WEAR_MAX_NUM = 64,
		};

		enum EItemWearableFlag
		{
			WEARABLE_BODY					= (1 << 0),
			WEARABLE_HEAD					= (1 << 1),
			WEARABLE_FOOTS					= (1 << 2),
			WEARABLE_WRIST					= (1 << 3),
			WEARABLE_WEAPON					= (1 << 4),
			WEARABLE_NECK					= (1 << 5),
			WEARABLE_EAR					= (1 << 6),
			WEARABLE_UNIQUE					= (1 << 7),
			WEARABLE_SHIELD					= (1 << 8),
			WEARABLE_ARROW					= (1 << 9),
			WEARABLE_HAIR					= (1 << 10),
			WEARABLE_ABILITY 				= (1 << 11),
			WEARABLE_COSTUME_BODY			= (1 << 12),
			WEARABLE_COSTUME_HAIR			= (1 << 13),
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
			WEARABLE_COSTUME_ACCE			= (1 << 14),
#endif
#ifdef ENABLE_WEAPON_COSTUME_SYSTEM
			WEARABLE_COSTUME_WEAPON			= (1 << 15),
#endif
#ifdef ENABLE_MOUNT_PET_SKIN
			WEARABLE_COSTUME_MOUNT			= (1 << 16),
			WEARABLE_COSTUME_PET			= (1 << 17),
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
			WEARABLE_COSTUME_AURA			= (1 << 18),
#endif
			WEARABLE_BELT					= (1 << 19),
#ifdef ENABLE_MOUNT_SYSTEM
			WEARABLE_MOUNT					= (1 << 20),
#endif
#ifdef ENABLE_PET_SYSTEM
			WEARABLE_PET					= (1 << 21),
#endif
#ifdef ENABLE_PENDANT_SYSTEM
			WEARABLE_PENDANT				= (1 << 22),
#endif
		};

		enum EApplyTypes
		{
			APPLY_NONE,						// 0
			APPLY_MAX_HP,					// 1
			APPLY_MAX_SP,					// 2
			APPLY_CON,						// 3
			APPLY_INT,						// 4
			APPLY_STR,						// 5
			APPLY_DEX,						// 6
			APPLY_ATT_SPEED,				// 7
			APPLY_MOV_SPEED,				// 8
			APPLY_CAST_SPEED,				// 9
			APPLY_HP_REGEN,					// 10
			APPLY_SP_REGEN,					// 11
			APPLY_POISON_PCT,				// 12
			APPLY_STUN_PCT,					// 13
			APPLY_SLOW_PCT,					// 14
			APPLY_CRITICAL_PCT,				// 15
			APPLY_PENETRATE_PCT,			// 16
			APPLY_ATTBONUS_HUMAN,			// 17
			APPLY_ATTBONUS_ANIMAL,			// 18
			APPLY_ATTBONUS_ORC,				// 19
			APPLY_ATTBONUS_MILGYO,			// 20
			APPLY_ATTBONUS_UNDEAD,			// 21
			APPLY_ATTBONUS_DEVIL,			// 22
			APPLY_STEAL_HP,					// 23
			APPLY_STEAL_SP,					// 24
			APPLY_MANA_BURN_PCT,			// 25
			APPLY_DAMAGE_SP_RECOVER,		// 26
			APPLY_BLOCK,					// 27
			APPLY_DODGE,					// 28
			APPLY_RESIST_SWORD,				// 29
			APPLY_RESIST_TWOHAND,			// 30
			APPLY_RESIST_DAGGER,			// 31
			APPLY_RESIST_BELL,				// 32
			APPLY_RESIST_FAN,				// 33
			APPLY_RESIST_BOW,				// 34
			APPLY_RESIST_FIRE,				// 35
			APPLY_RESIST_ELEC,				// 36
			APPLY_RESIST_MAGIC,				// 37
			APPLY_RESIST_WIND,				// 38
			APPLY_REFLECT_MELEE,			// 39
			APPLY_REFLECT_CURSE,			// 40
			APPLY_POISON_REDUCE,			// 41
			APPLY_KILL_SP_RECOVER,			// 42
			APPLY_EXP_DOUBLE_BONUS,			// 43
			APPLY_GOLD_DOUBLE_BONUS,		// 44
			APPLY_ITEM_DROP_BONUS,			// 45
			APPLY_POTION_BONUS,				// 46
			APPLY_KILL_HP_RECOVER,			// 47
			APPLY_IMMUNE_STUN,				// 48
			APPLY_IMMUNE_SLOW,				// 49
			APPLY_IMMUNE_FALL,				// 50
			APPLY_SKILL,					// 51
			APPLY_BOW_DISTANCE,				// 52
			APPLY_ATT_GRADE_BONUS,			// 53
			APPLY_DEF_GRADE_BONUS,			// 54
			APPLY_MAGIC_ATT_GRADE,			// 55
			APPLY_MAGIC_DEF_GRADE,			// 56
			APPLY_CURSE_PCT,				// 57
			APPLY_MAX_STAMINA,				// 58
			APPLY_ATT_BONUS_TO_WARRIOR, // 59
			APPLY_ATT_BONUS_TO_ASSASSIN,// 60
			APPLY_ATT_BONUS_TO_SURA,    // 61
			APPLY_ATT_BONUS_TO_SHAMAN,  // 62
			APPLY_ATT_BONUS_TO_MONSTER, // 63
			APPLY_MALL_ATTBONUS,			// 64
			APPLY_MALL_DEFBONUS,			// 65
			APPLY_MALL_EXPBONUS,			// 66
			APPLY_MALL_ITEMBONUS,			// 67
			APPLY_MALL_GOLDBONUS,			// 68
			APPLY_MAX_HP_PCT,				// 69
			APPLY_MAX_SP_PCT,				// 70
			APPLY_SKILL_DAMAGE_BONUS,		// 71
			APPLY_NORMAL_HIT_DAMAGE_BONUS,	// 72
			APPLY_SKILL_DEFEND_BONUS,		// 73
			APPLY_NORMAL_HIT_DEFEND_BONUS,	// 74
			APPLY_PC_BANG_EXP_BONUS,		// 75
			APPLY_PC_BANG_DROP_BONUS,		// 76
			APPLY_EXTRACT_HP_PCT,			// 77
			APPLY_RESIST_WARRIOR,			// 78
			APPLY_RESIST_ASSASSIN,			// 79
			APPLY_RESIST_SURA,				// 80
			APPLY_RESIST_SHAMAN,			// 81
			APPLY_ENERGY,					// 82
			APPLY_DEF_GRADE,				// 83
			APPLY_COSTUME_ATTR_BONUS,		// 84
			APPLY_MAGIC_ATTBONUS_PER,		// 85
			APPLY_MELEE_MAGIC_ATTBONUS_PER,	// 86

			APPLY_RESIST_ICE,				// 87
			APPLY_RESIST_EARTH,				// 88
			APPLY_RESIST_DARK,				// 89

			APPLY_ANTI_CRITICAL_PCT,		// 90
			APPLY_ANTI_PENETRATE_PCT,		// 91

#ifdef ENABLE_WOLFMAN_CHARACTER
			APPLY_BLEEDING_REDUCE			= 92,
			APPLY_BLEEDING_PCT				= 93,
			APPLY_ATT_BONUS_TO_WOLFMAN		= 94,
			APPLY_RESIST_WOLFMAN			= 95,
			APPLY_RESIST_CLAW				= 96,
#endif

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
			APPLY_ACCEDRAIN_RATE			= 97,
#endif

#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
			APPLY_RESIST_MAGIC_REDUCTION	= 98,
#endif

			APPLY_ENCHANT_ELECT				= 99,
			APPLY_ENCHANT_FIRE				= 100,
			APPLY_ENCHANT_ICE				= 101,
			APPLY_ENCHANT_WIND				= 102,
			APPLY_ENCHANT_EARTH				= 103,
			APPLY_ENCHANT_DARK				= 104,

			APPLY_ATTBONUS_CZ				= 105,
			APPLY_ATTBONUS_INSECT			= 106,
			APPLY_ATTBONUS_DESERT			= 107,
			APPLY_ATTBONUS_SWORD			= 108,
			APPLY_ATTBONUS_TWOHAND			= 109,
			APPLY_ATTBONUS_DAGGER			= 110,
			APPLY_ATTBONUS_BELL				= 111,
			APPLY_ATTBONUS_FAN				= 112,
			APPLY_ATTBONUS_BOW				= 113,
#ifdef ENABLE_WOLFMAN_CHARACTER
			APPLY_ATTBONUS_CLAW				= 114,
#endif

			APPLY_RESIST_HUMAN				= 115,
			APPLY_RESIST_MOUNT_FALL			= 116,
			APPLY_MOUNT						= 118,

#ifdef ENABLE_NEW_BONUS_SYSTEM
			APPLY_ATTBONUS_STONE			= 119,
			APPLY_ATTBONUS_BOSS				= 120,
			APPLY_ATTBONUS_ELEMENTS			= 121,
			APPLY_ENCHANT_ELEMENTS			= 122,
			APPLY_ATTBONUS_CHARACTERS		= 123,
			APPLY_ENCHANT_CHARACTERS		= 124,
			APPLY_RESIST_MONSTER			= 125,
#endif

#ifdef ENABLE_AVG_PVM
			APPLY_ATTBONUS_MEDI_PVM			= 126,
#endif

			APPLY_ATTBONUS_PVM_STR			= 127,
			APPLY_ATTBONUS_PVM_BERSERKER	= 128,

#ifdef ENABLE_CONQUEROR_LEVEL
			APPLY_SUNGMA_STR				= 129,
			APPLY_SUNGMA_HP					= 130,
			APPLY_SUNGMA_MOVE				= 131,
			APPLY_SUNGMA_IMMUNE				= 132,
#endif

			MAX_APPLY_NUM,
		};

		enum EImmuneFlags
		{
			IMMUNE_PARA         = (1 << 0),
			IMMUNE_CURSE        = (1 << 1),
			IMMUNE_STUN         = (1 << 2),
			IMMUNE_SLEEP        = (1 << 3),
			IMMUNE_SLOW         = (1 << 4),
			IMMUNE_POISON       = (1 << 5),
			IMMUNE_TERROR       = (1 << 6),
		};

#pragma pack(push)
#pragma pack(1)
		typedef struct SItemLimit
		{
			BYTE bType;
			long lValue;
		} TItemLimit;

		typedef struct SItemApply
		{
			BYTE bType;
			long lValue;
		} TItemApply;

		typedef struct SItemTable
		{
			DWORD dwVnum;
			DWORD dwVnumRange;
			char szName[ITEM_NAME_MAX_LEN + 1];
			char szLocaleName[ITEM_NAME_MAX_LEN + 1];
			BYTE bType;
			BYTE bSubType;

			BYTE bWeight;
			BYTE bSize;

			DWORD dwAntiFlags;
			DWORD dwFlags;
			DWORD dwWearFlags;
			DWORD dwImmuneFlag;

			DWORD dwIBuyItemPrice;
			DWORD dwISellItemPrice;

			TItemLimit aLimits[ITEM_LIMIT_MAX_NUM];
			TItemApply aApplies[ITEM_APPLY_MAX_NUM];
			long alValues[ITEM_VALUES_MAX_NUM];
			long alSockets[ITEM_SOCKET_MAX_NUM];
			DWORD dwRefinedVnum;
			WORD wRefineSet;
			BYTE bAlterToMagicItemPct;
			BYTE bSpecular;
			BYTE bGainSocketPct;
		} TItemTable;

#pragma pack(pop)

	public:
		CItemData();
		virtual ~CItemData();

		void Clear();
		void SetSummary(const std::string& c_rstSumm);
		void SetDescription(const std::string& c_rstDesc);

		CGraphicThing *GetModelThing();
		CGraphicThing *GetSubModelThing();
		CGraphicThing *GetDropModelThing();
		CGraphicSubImage *GetIconImage();

		DWORD GetLODModelThingCount();
		BOOL GetLODModelThingPointer(DWORD dwIndex, CGraphicThing ** ppModelThing);

		DWORD GetAttachingDataCount();
		BOOL GetCollisionDataPointer(DWORD dwIndex, const NRaceData::TAttachingData ** c_ppAttachingData);
		BOOL GetAttachingDataPointer(DWORD dwIndex, const NRaceData::TAttachingData ** c_ppAttachingData);

		const TItemTable* GetTable() const;
		DWORD GetIndex() const;
		const char *GetName() const;
		const char *GetDescription() const;
		const char *GetSummary() const;
		BYTE GetType() const;
		BYTE GetSubType() const;
#ifdef ENABLE_CHANGE_LOOK_SYSTEM
		DWORD GetAntiFlags() const;
#endif
		UINT GetRefine() const;
		const char *GetUseTypeString() const;
		DWORD GetWeaponType() const;
		BYTE GetSize() const;
		BOOL IsAntiFlag(DWORD dwFlag) const;
		BOOL IsFlag(DWORD dwFlag) const;
		BOOL IsWearableFlag(DWORD dwFlag) const;
		BOOL HasNextGrade() const;
#if defined(ENABLE_WIKI_SYSTEM) || defined(INSIDE_RENDER)
		WORD GetRefinedSet() const;
		WORD GetRefinedVnum() const;
#endif

		DWORD GetWearFlags() const;
		DWORD GetIBuyItemPrice() const;
		DWORD GetISellItemPrice() const;
		BOOL GetLimit(BYTE byIndex, TItemLimit * pItemLimit) const;
		BOOL GetApply(BYTE byIndex, TItemApply * pItemApply) const;
		long GetValue(BYTE byIndex) const;
		long GetSocket(BYTE byIndex) const;
		long SetSocket(BYTE byIndex,DWORD value);
		int GetSocketCount() const;
		DWORD GetIconNumber() const;

		UINT GetSpecularPoweru() const;
		float GetSpecularPowerf() const;

		BOOL IsEquipment() const;

		void SetDefaultItemData(const char *c_szIconFileName, const char *c_szModelFileName  = nullptr);
		void SetItemTableData(TItemTable * pItemTable);

	protected:
		void __LoadFiles();
		void __SetIconImage(const char *c_szFileName);

	protected:
		std::string m_strModelFileName;
		std::string m_strSubModelFileName;
		std::string m_strDropModelFileName;
		std::string m_strIconFileName;
		std::string m_strDescription;
		std::string m_strSummary;
		std::vector<std::string> m_strLODModelFileNameVector;

		CGraphicThing * m_pModelThing;
		CGraphicThing * m_pSubModelThing;
		CGraphicThing * m_pDropModelThing;
		CGraphicSubImage * m_pIconImage;
		std::vector<CGraphicThing *> m_pLODModelThingVector;

		NRaceData::TAttachingDataVector m_AttachingDataVector;
		DWORD m_dwVnum;
		TItemTable m_ItemTable;

	public:
		static void DestroySystem();

		static CItemData* New();
		static void Delete(CItemData* pkItemData);

		static CDynamicPool<CItemData> ms_kPool;

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	protected:
		typedef struct SItemScaleTable
		{
			D3DXVECTOR3 v3Scale[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
			float fScaleParticle[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
		} TItemScaleTable;
		TItemScaleTable m_ItemScaleTable;

	public:
		float GetItemParticleScale(BYTE bJob, BYTE bSex);
		void SetItemTableScaleData(BYTE bJob, BYTE bSex, float fScaleX, float fScaleY, float fScaleZ, float fScaleParticle);
		D3DXVECTOR3 & GetItemScaleVector(BYTE bJob, BYTE bSex);
#endif

#ifdef ENABLE_AURA_COSTUME_SYSTEM
	public:
		enum EAuraGradeType
		{
			AURA_GRADE_NONE,
			AURA_GRADE_ORDINARY,
			AURA_GRADE_SIMPLE,
			AURA_GRADE_NOBLE,
			AURA_GRADE_SPARKLING,
			AURA_GRADE_MAGNIFICENT,
			AURA_GRADE_RADIANT,
			AURA_GRADE_MAX_NUM,
		};

		enum EAuraItem
		{
			AURA_BOOST_ITEM_VNUM_BASE = 49980
		};

		enum EAuraBoostIndex
		{
			ITEM_AURA_BOOST_ERASER,
			ITEM_AURA_BOOST_WEAK,
			ITEM_AURA_BOOST_NORMAL,
			ITEM_AURA_BOOST_STRONG,
			ITEM_AURA_BOOST_ULTIMATE,
			ITEM_AURA_BOOST_MAX,
		};

	protected:
		typedef struct SAuraScaleTable
		{
			D3DXVECTOR3 v3MeshScale[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
			float fParticleScale[NRaceData::SEX_MAX_NUM][NRaceData::JOB_MAX_NUM];
		} TAuraScaleTable;

		TAuraScaleTable m_AuraScaleTable;
		DWORD m_dwAuraEffectID;

	public:
		void SetAuraScaleTableData(BYTE byJob, BYTE bySex, float fMeshScaleX, float fMeshScaleY, float fMeshScaleZ, float fParticleScale);
		D3DXVECTOR3& GetAuraMeshScaleVector(BYTE byJob, BYTE bySex);
		float GetAuraParticleScale(BYTE byJob, BYTE bySex);

		void SetAuraEffectID(const char* szAuraEffectPath);
		DWORD GetAuraEffectID() const { return m_dwAuraEffectID; }
#endif
};
