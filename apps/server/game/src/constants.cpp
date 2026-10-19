#include "stdafx.h"
#include "char.h"

#include "../../common/service.h"
#include "../../common/length.h"


TJobInitialPoints JobInitialPoints[JOB_MAX_NUM] =
/*
{
	int st, ht, dx, iq;
	int max_hp, max_sp;
	int hp_per_ht, sp_per_iq;
	int hp_per_lv_begin, hp_per_lv_end;
	int sp_per_lv_begin, sp_per_lv_end;
	int max_stamina;
	int stamina_per_con;
	int stamina_per_lv_begin, stamina_per_lv_end;
}
*/
#ifdef ENABLE_RANDOM_STATUS_PER_LEVEL
{	// Random HP & SP
	// str con dex int HP SP CON/HP INT/SP HP/lv MP/lv stam stam/con stam/lv
	{ 6, 4, 3, 3, 600, 200, 40, 20, 36, 44, 18, 22, 800, 5, 1, 3 }, // JOB_WARRIOR 16
	{ 4, 3, 6, 3, 650, 200, 40, 20, 36, 44, 18, 22, 800, 5, 1, 3 }, // JOB_ASSASSIN 16
	{ 5, 3, 3, 5, 650, 200, 40, 20, 36, 44, 18, 22, 800, 5, 1, 3 }, // JOB_SURA 16
	{ 3, 4, 3, 6, 700, 200, 40, 20, 36, 44, 18, 22, 800, 5, 1, 3 }, // JOB_SHAMAN 16
};
#else
{
	// str con dex int HP SP CON/HP INT/SP HP/lv MP/lv stam stam/con stam/lv
	{ 6, 4, 3, 3, 600, 200, 40, 20, 0, 0, 0, 0, 800, 5, 1, 3 }, // JOB_WARRIOR 16
	{ 4, 3, 6, 3, 650, 200, 40, 20, 0, 0, 0, 0, 800, 5, 1, 3 }, // JOB_ASSASSIN 16
	{ 5, 3, 3, 5, 650, 200, 40, 20, 0, 0, 0, 0, 800, 5, 1, 3 }, // JOB_SURA 16
	{ 3, 4, 3, 6, 700, 200, 40, 20, 0, 0, 0, 0, 800, 5, 1, 3 }, // JOB_SHAMAN 16
};
#endif

const TMobRankStat MobRankStats[MOB_RANK_MAX_NUM] =
/*
{
	int iGoldPercent;
}
*/
{
	{ 20, }, // MOB_RANK_PAWN,
	{ 20, }, // MOB_RANK_S_PAWN,
	{ 25, }, // MOB_RANK_KNIGHT,
	{ 30, }, // MOB_RANK_S_KNIGHT,
	{ 50, }, // MOB_RANK_BOSS,
	{ 100, } // MOB_RANK_KING,
};

TBattleTypeStat BattleTypeStats[BATTLE_TYPE_MAX_NUM] =
/*
{
	int AttGradeBias;
	int DefGradeBias;
	int MagicAttGradeBias;
	int MagicDefGradeBias;
}
*/
{
	{ 0, 0, 0, -10 }, // BATTLE_TYPE_MELEE,
	{ 10, -20, -10, -15 }, // BATTLE_TYPE_RANGE,
	{ -5, -5, 10, 10 }, // BATTLE_TYPE_MAGIC,
	{ 0, 0, 0, 0 }, // BATTLE_TYPE_SPECIAL,
	{ 10, -10, 0, -15 }, // BATTLE_TYPE_POWER,
	{ -10, 10, -10, 0 }, // BATTLE_TYPE_TANKER,
	{ 20, -20, 0, -10 }, // BATTLE_TYPE_SUPER_POWER,
	{ -20, 20, -10, 0 }, // BATTLE_TYPE_SUPER_TANKER,
};

const DWORD * exp_table = NULL;

#ifdef ENABLE_CONQUEROR_LEVEL
const DWORD exp_coqueror_table[PLAYER_MAX_CONQUEROR_LEVEL_CONST + 1] =
{
	0,	//	0
	433400,
	1300204,
	2600413,
	4334029,
	6501054,
	9101490,
	12135339,
	15602603,
	19503284,
	23837384,	//	10
	28604905,
	33805849,
	39440218,
	45508014,
	52009239,
	58943895,
	66311984,
	74113508,
	82348469,
	91016869,	//	20
	100118710,
	109653994,
	119622723,
	130024899,
	140860524,
	152129600,
	163832129,
	175968113,
	188537554,
	188537554,	//	30	
};
#endif

const DWORD exp_table_common[PLAYER_EXP_TABLE_MAX + 1] =
{
	0, // 0
	300,
	800,
	1500,
	2500,
	4300,
	7200,
	11000,
	17000,
	24000,
	33000, // 10
	43000,
	58000,
	76000,
	100000,
	130000,
	169000,
	219000,
	283000,
	365000,
	472000, // 20
	610000,
	705000,
	813000,
	937000,
	1077000,
	1237000,
	1418000,
	1624000,
	1857000,
	2122000, // 30
	2421000,
	2761000,
	3145000,
	3580000,
	4073000,
	4632000,
	5194000,
	5717000,
	6264000,
	6837000, // 40
	7600000,
	8274000,
	8990000,
	9753000,
	10560000,
	11410000,
	12320000,
	13270000,
	14280000,
	15340000, // 50
	16870000,
	18960000,
	19980000,
	21420000,
	22930000,
	24530000,
	26200000,
	27960000,
	29800000,
	32780000, // 60
	36060000,
	39670000,
	43640000,
	48000000,
	52800000,
	58080000,
	63890000,
	70280000,
	77310000,
	85040000, // 70
	93540000,
	102900000,
	113200000,
	124500000,
	137000000,
	150700000,
	165700000,
	236990000,
	260650000,
	286780000, // 80
	315380000,
	346970000,
	381680000,
	419770000,
	461760000,
	508040000,
	558740000,
	614640000,
	676130000,
	743730000, // 90
	1041222000,
	1145344200,
	1259878620,
	1385866482,
	1524453130,
	1676898443,
	1844588288,
	2029047116,
	2050000000, // 99
	2150000000, // 100
	2210000000,
	2250000000,
	2280000000,
	2310000000,
	2330000000,
	2350000000,
	2370000000,
	2390000000,
	2400000000,
	2410000000,
	2420000000,
	2430000000,
	2440000000,
	2450000000,
	2460000000,
	2470000000, // 110
	2480000000,
	2490000000,
	2490000000,
	2500000000,

#ifdef ENABLE_LEVEL_INT
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 130
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 140
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 150
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 160
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 170
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 180
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 190
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 200
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 210
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 220
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 230
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 240
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 250
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 260
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 270
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 280
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 290
	2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u,2500000000u, // 300
#endif
};

// Mid-effort 1-99 PvP (PVP_HEDEF.md): ~8-12h active to 99 with same-level farm.
// Values are percent (100 = 1x). Tuned via platform/tools/mid_pvp_exp_sim.py
// (mob_proto median EXP + 1500 kills/h + nextExp/10 cap). Re-run after edits.
int GetMidPvpMobExpRate(int level)
{
	if (level < 30)
		return 3500;	// 35x  -> ~1-1.5h with travel pad
	if (level < 70)
		return 3800;	// 38x  -> ~3.5h
	if (level < 90)
		return 14000;	// 140x -> ~2.8h
	if (level < 99)
		return 22000;	// 220x -> ~2.5h
	return 100;			// 99+: no push (MAX_LEVEL 99)
}

// Yang scarce: proto amount * this / 100. Boss bombs also hard-capped per kill.
int GetMidPvpGoldAmountRate()
{
	return 50; // 50% of proto yang
}

int GetMidPvpGoldKillCap()
{
	return 400000; // one kill never floods the 10-player economy
}

// Classic metins have Min/MaxGold=0; give modest yang so upgrade costs are farmable.
int GetMidPvpMetinYang(int stoneLevel)
{
	if (stoneLevel < 1)
		stoneLevel = 1;
	if (stoneLevel > 99)
		stoneLevel = 99;
	// lv10 ~1.5k, lv50 ~7.5k, lv90 ~13.5k (before gold amount rate)
	return 500 + stoneLevel * 150;
}

#ifdef ENABLE_AURA_COSTUME_SYSTEM
int s_aiAuraRefineInfo[AURA_GRADE_MAX_NUM][AURA_REFINE_INFO_MAX] = {
//  [ Grade | LevelMin | LevelMax | NeedEXP | EvolMaterial | EvolMaterialCount | EvolCost | EvolPCT ]
	{1,   1,  49,  1000, 30617, 10,  5000000, 100},
	{2,  50,  99,  2000, 31136, 10,  5000000, 100},
	{3, 100, 149,  4000, 31137, 10,  5000000, 100},
	{4, 150, 199,  8000, 31138, 10,  8000000, 100},
	{5, 200, 249, 16000, 31138, 20, 10000000, 100},
	{6, 250, 250,     0,     0,  0,        0,   0},
	{0,   0,   0,     0,     0,  0,        0,   0}
};

int *GetAuraRefineInfo(BYTE bLevel)
{
	if (bLevel > 250)
		return NULL;

	for (int i = 0; i < AURA_GRADE_MAX_NUM; ++i)
	{
		if (bLevel >= s_aiAuraRefineInfo[i][AURA_REFINE_INFO_LEVEL_MIN] && bLevel <= s_aiAuraRefineInfo[i][AURA_REFINE_INFO_LEVEL_MAX])
			return s_aiAuraRefineInfo[i];
	}

	return NULL;
}

int GetAuraRefineInfo(BYTE bGrade, BYTE bInfo)
{
	if (bGrade >= AURA_GRADE_MAX_NUM || bInfo >= AURA_REFINE_INFO_MAX)
		return 0;

	return s_aiAuraRefineInfo[bGrade - 1][bInfo];
}
#endif

const int *aiPercentByDeltaLev = NULL;
const int *aiPercentByDeltaLevForBoss = NULL;

const int aiPercentByDeltaLevForBoss_euckr[MAX_EXP_DELTA_OF_LEV] =
{
	1,		// -15	0
	3,		// -14	1
	5,		// -13	2
	7,		// -12	3
	15,		// -11	4
	30,		// -10	5
	60,		// -9	6
	90,		// -8	7
	91,		// -7	8
	92,		// -6	9
	93,		// -5	10
	94,		// -4	11
	95,		// -3	12
	97,		// -2	13
	99,		// -1	14
	100,	// 0	15
	105,	// 1	16
	110,	// 2	17
	115,	// 3	18
	120,	// 4	19
	125,	// 5	20
	130,	// 6	21
	135,	// 7	22
	140,	// 8	23
	145,	// 9	24
	150,	// 10	25
	155,	// 11	26
	160,	// 12	27
	165,	// 13	28
	170,	// 14	29
	180,	// 15	30
};

const int aiPercentByDeltaLev_euckr[MAX_EXP_DELTA_OF_LEV] =
{
	1,		// -15	0
	5,		// -14	1
	10,		// -13	2
	20,		// -12	3
	30,		// -11	4
	50,		// -10	5
	70,		// -9	6
	80,		// -8	7
	85,		// -7	8
	90,		// -6	9
	92,		// -5	10
	94,		// -4	11
	96,		// -3	12
	98,		// -2	13
	100,	// -1	14
	100,	// 0	15
	105,	// 1	16
	110,	// 2	17
	115,	// 3	18
	120,	// 4	19
	125,	// 5	20
	130,	// 6	21
	135,	// 7	22
	140,	// 8	23
	145,	// 9	24
	150,	// 10	25
	155,	// 11	26
	160,	// 12	27
	165,	// 13	28
	170,	// 14	29
	180,	// 15	30
};

const DWORD party_exp_distribute_table[PLAYER_MAX_LEVEL_CONST + 1] =
{
	0,
	10,		10,		10,		10,		15,		15,		20,		25,		30,		40,		// 1 - 10
	50,		60,		80,		100,	120,	140,	160,	184,	210,	240,	// 11 - 20
	270,	300,	330,	360,	390,	420,	450,	480,	510,	550,	// 21 - 30
	600,	640,	700,	760,	820,	880,	940,	1000,	1100,	1180,	// 31 - 40
	1260,	1320,	1380,	1440,	1500,	1560,	1620,	1680,	1740,	1800,	// 41 - 50
	1860,	1920,	2000,	2100,	2200,	2300,	2450,	2600,	2750,	2900,	// 51 - 60
	3050,	3200,	3350,	3500,	3650,	3800,	3950,	4100,	4250,	4400,	// 61 - 70
	4600,	4800,	5000,	5200,	5400,	5600,	5800,	6000,	6200,	6400,	// 71 - 80
	6600,	6900,	7100,	7300,	7600,	7800,	8000,	8300,	8500,	8800,	// 81 - 90
	9000,	9000,	9000,	9000,	9000,	9000,	9000,	9000,	9000,	9000,	// 91 - 100
	10000,	10000,	10000,	10000,	10000,	10000,	10000,	10000,	10000,	10000,	// 101 - 110
	12000,	12000,	12000,	12000,	12000,	12000,	12000,	12000,	12000,	12000,	// 111 - 120

#ifdef ENABLE_LEVEL_INT
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 121 - 130
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 131 - 140
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 141 - 150
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 151 - 160
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 161 - 170
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 171 - 180
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 181 - 190
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 191 - 200
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 201 - 210
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 211 - 220
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 221 - 230
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 231 - 240
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 241 - 250
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 251 - 260
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 261 - 270
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 271 - 280
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 281 - 290
	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	14000,	// 291 - 300
#endif
};

Coord aArroundCoords[ARROUND_COORD_MAX_NUM] = 
{
	{	     0,	      0	    },
	{        0,      50     },
	{       35,     35      },
	{       50,     -0      },
	{       35,     -35     },
	{       0,      -50     },
	{       -35,    -35     },
	{       -50,    0       },
	{       -35,    35      },
	{       0,      100     },
	{       71,     71      },
	{       100,    -0      },
	{       71,     -71     },
	{       0,      -100    },
	{       -71,    -71     },
	{       -100,   0       },
	{       -71,    71      },
	{       0,      150     },
	{       106,    106     },
	{       150,    -0      },
	{       106,    -106    },
	{       0,      -150    },
	{       -106,   -106    },
	{       -150,   0       },
	{       -106,   106     },
	{       0,      200     },
	{       141,    141     },
	{       200,    -0      },
	{       141,    -141    },
	{       0,      -200    },
	{       -141,   -141    },
	{       -200,   0       },
	{       -141,   141     },
	{       0,      250     },
	{       177,    177     },
	{       250,    -0      },
	{       177,    -177    },
	{       0,      -250    },
	{       -177,   -177    },
	{       -250,   0       },
	{       -177,   177     },
	{       0,      300     },
	{       212,    212     },
	{       300,    -0      },
	{       212,    -212    },
	{       0,      -300    },
	{       -212,   -212    },
	{       -300,   0       },
	{       -212,   212     },
	{       0,      350     },
	{       247,    247     },
	{       350,    -0      },
	{       247,    -247    },
	{       0,      -350    },
	{       -247,   -247    },
	{       -350,   0       },
	{       -247,   247     },
	{       0,      400     },
	{       283,    283     },
	{       400,    -0      },
	{       283,    -283    },
	{       0,      -400    },
	{       -283,   -283    },
	{       -400,   0       },
	{       -283,   283     },
	{       0,      450     },
	{       318,    318     },
	{       450,    -0      },
	{       318,    -318    },
	{       0,      -450    },
	{       -318,   -318    },
	{       -450,   0       },
	{       -318,   318     },
	{       0,      500     },
	{       354,    354     },
	{       500,    -0      },
	{       354,    -354    },
	{       0,      -500    },
	{       -354,   -354    },
	{       -500,   0       },
	{       -354,   354     },
	{       0,      550     },
	{       389,    389     },
	{       550,    -0      },
	{       389,    -389    },
	{       0,      -550    },
	{       -389,   -389    },
	{       -550,   0       },
	{       -389,   389     },
	{       0,      600     },
	{       424,    424     },
	{       600,    -0      },
	{       424,    -424    },
	{       0,      -600    },
	{       -424,   -424    },
	{       -600,   0       },
	{       -424,   424     },
	{       0,      650     },
	{       460,    460     },
	{       650,    -0      },
	{       460,    -460    },
	{       0,      -650    },
	{       -460,   -460    },
	{       -650,   0       },
	{       -460,   460     },
	{       0,      700     },
	{       495,    495     },
	{       700,    -0      },
	{       495,    -495    },
	{       0,      -700    },
	{       -495,   -495    },
	{       -700,   0       },
	{       -495,   495     },
	{       0,      750     },
	{       530,    530     },
	{       750,    -0      },
	{       530,    -530    },
	{       0,      -750    },
	{       -530,   -530    },
	{       -750,   0       },
	{       -530,   530     },
	{       0,      800     },
	{       566,    566     },
	{       800,    -0      },
	{       566,    -566    },
	{       0,      -800    },
	{       -566,   -566    },
	{       -800,   0       },
	{       -566,   566     },
	{       0,      850     },
	{       601,    601     },
	{       850,    -0      },
	{       601,    -601    },
	{       0,      -850    },
	{       -601,   -601    },
	{       -850,   0       },
	{       -601,   601     },
	{       0,      900     },
	{       636,    636     },
	{       900,    -0      },
	{       636,    -636    },
	{       0,      -900    },
	{       -636,   -636    },
	{       -900,   0       },
	{       -636,   636     },
	{       0,      950     },
	{       672,    672     },
	{       950,    -0      },
	{       672,    -672    },
	{       0,      -950    },
	{       -672,   -672    },
	{       -950,   0       },
	{       -672,   672     },
	{       0,      1000    },
	{       707,    707     },
	{       1000,   -0      },
	{       707,    -707    },
	{       0,      -1000   },
	{       -707,   -707    },
	{       -1000,  0       },
	{       -707,   707     },
};

const DWORD guild_exp_table[GUILD_MAX_LEVEL + 1] =
{
	0,
	15000UL,
	45000UL,
	90000UL,
	160000UL,
	235000UL,
	325000UL,
	430000UL,
	550000UL,
	685000UL,
	835000UL,
	1000000UL,
	1500000UL,
	2100000UL,
	2800000UL,
	3600000UL,
	4500000UL,
	6500000UL,
	8000000UL,
	10000000UL,
	42000000UL
};

const int aiMobEnchantApplyIdx[MOB_ENCHANTS_MAX_NUM] =
{
	APPLY_CURSE_PCT,
	APPLY_SLOW_PCT,
	APPLY_POISON_PCT,
	APPLY_STUN_PCT,
	APPLY_CRITICAL_PCT,
	APPLY_PENETRATE_PCT,
};

const int aiMobResistsApplyIdx[MOB_RESISTS_MAX_NUM] =
{
	APPLY_RESIST_SWORD,
	APPLY_RESIST_TWOHAND,
	APPLY_RESIST_DAGGER,
	APPLY_RESIST_BELL,
	APPLY_RESIST_FAN,
	APPLY_RESIST_BOW,
	APPLY_RESIST_FIRE,
	APPLY_RESIST_ELEC,
	APPLY_RESIST_MAGIC,
	APPLY_RESIST_WIND,
	APPLY_POISON_REDUCE,
};

const int aiSocketPercentByQty[5][4] =
{
	{  0,  0,  0,  0 },
	{  3,  0,  0,  0 },
	{ 10,  1,  0,  0 },
	{ 15, 10,  1,  0 },
	{ 20, 15, 10,  1 }
};

const int aiWeaponSocketQty[WEAPON_NUM_TYPES] =
{
	3, // WEAPON_SWORD,
	3, // WEAPON_DAGGER,
	3, // WEAPON_BOW,
	3, // WEAPON_TWO_HANDED,
	3, // WEAPON_BELL,
	3, // WEAPON_FAN,
	0, // WEAPON_ARROW,
	0, // WEAPON_MOUNT_SPEAR
};

const int aiArmorSocketQty[ARMOR_NUM_TYPES] =
{
	3, // ARMOR_BODY,
	1, // ARMOR_HEAD,
	1, // ARMOR_SHIELD,
	0, // ARMOR_WRIST,
	0, // ARMOR_FOOTS,
	0 // ARMOR_ACCESSORY
};

TItemAttrMap g_map_itemAttr;
TItemAttrMap g_map_itemRare;

const TApplyInfo aApplyInfo[MAX_APPLY_NUM] =
/* { DWORD dwPointType; }  */
{
	// Point Type
	{ POINT_NONE,			},   // APPLY_NONE,		0
	{ POINT_MAX_HP,		        },   // APPLY_MAX_HP,		1
	{ POINT_MAX_SP,		        },   // APPLY_MAX_SP,		2
	{ POINT_HT,			        },   // APPLY_CON,		3
	{ POINT_IQ,			        },   // APPLY_INT,		4
	{ POINT_ST,			        },   // APPLY_STR,		5
	{ POINT_DX,			        },   // APPLY_DEX,		6
	{ POINT_ATT_SPEED,		        },   // APPLY_ATT_SPEED,	7
	{ POINT_MOV_SPEED,		        },   // APPLY_MOV_SPEED,	8
	{ POINT_CASTING_SPEED,	        },   // APPLY_CAST_SPEED,	9
	{ POINT_HP_REGEN,			},   // APPLY_HP_REGEN,		10
	{ POINT_SP_REGEN,			},   // APPLY_SP_REGEN,		11
	{ POINT_POISON_PCT,		        },   // APPLY_POISON_PCT,	12
	{ POINT_STUN_PCT,		        },   // APPLY_STUN_PCT,		13
	{ POINT_SLOW_PCT,		        },   // APPLY_SLOW_PCT,		14
	{ POINT_CRITICAL_PCT,		},   // APPLY_CRITICAL_PCT,	15
	{ POINT_PENETRATE_PCT,	        },   // APPLY_PENETRATE_PCT,	16
	{ POINT_ATTBONUS_HUMAN,	        },   // APPLY_ATTBONUS_HUMAN,	17
	{ POINT_ATTBONUS_ANIMAL,	        },   // APPLY_ATTBONUS_ANIMAL,	18
	{ POINT_ATTBONUS_ORC,		},   // APPLY_ATTBONUS_ORC,	19
	{ POINT_ATTBONUS_MILGYO,	        },   // APPLY_ATTBONUS_MILGYO,	20
	{ POINT_ATTBONUS_UNDEAD,	        },   // APPLY_ATTBONUS_UNDEAD,	21
	{ POINT_ATTBONUS_DEVIL,	        },   // APPLY_ATTBONUS_DEVIL,	22
	{ POINT_STEAL_HP,		        },   // APPLY_STEAL_HP,		23
	{ POINT_STEAL_SP,		        },   // APPLY_STEAL_SP,		24
	{ POINT_MANA_BURN_PCT,	        },   // APPLY_MANA_BURN_PCT,	25
	{ POINT_DAMAGE_SP_RECOVER,	        },   // APPLY_DAMAGE_SP_RECOVER,26
	{ POINT_BLOCK,		        },   // APPLY_BLOCK,		27
	{ POINT_DODGE,		        },   // APPLY_DODGE,		28
	{ POINT_RESIST_SWORD,		},   // APPLY_RESIST_SWORD,	29
	{ POINT_RESIST_TWOHAND,	        },   // APPLY_RESIST_TWOHAND,	30
	{ POINT_RESIST_DAGGER,	        },   // APPLY_RESIST_DAGGER,	31
	{ POINT_RESIST_BELL,		},   // APPLY_RESIST_BELL,	32
	{ POINT_RESIST_FAN,		        },   // APPLY_RESIST_FAN,	33
	{ POINT_RESIST_BOW,		        },   // APPLY_RESIST_BOW,	34
	{ POINT_RESIST_FIRE,		},   // APPLY_RESIST_FIRE,	35
	{ POINT_RESIST_ELEC,		},   // APPLY_RESIST_ELEC,	36
	{ POINT_RESIST_MAGIC,		},   // APPLY_RESIST_MAGIC,	37
	{ POINT_RESIST_WIND,		},   // APPLY_RESIST_WIND,	38
	{ POINT_REFLECT_MELEE,	        },   // APPLY_REFLECT_MELEE,	39
	{ POINT_REFLECT_CURSE,	        },   // APPLY_REFLECT_CURSE,	40
	{ POINT_POISON_REDUCE,	        },   // APPLY_POISON_REDUCE,	41
	{ POINT_KILL_SP_RECOVER,	        },   // APPLY_KILL_SP_RECOVER,	42
	{ POINT_EXP_DOUBLE_BONUS,	        },   // APPLY_EXP_DOUBLE_BONUS,	43
	{ POINT_GOLD_DOUBLE_BONUS,	        },   // APPLY_GOLD_DOUBLE_BONUS,44
	{ POINT_ITEM_DROP_BONUS,	        },   // APPLY_ITEM_DROP_BONUS,	45
	{ POINT_POTION_BONUS,		},   // APPLY_POTION_BONUS,	46
	{ POINT_KILL_HP_RECOVERY,	        },   // APPLY_KILL_HP_RECOVER,	47
	{ POINT_IMMUNE_STUN,		},   // APPLY_IMMUNE_STUN,	48
	{ POINT_IMMUNE_SLOW,		},   // APPLY_IMMUNE_SLOW,	49
	{ POINT_IMMUNE_FALL,		},   // APPLY_IMMUNE_FALL,	50
	{ POINT_NONE,			},   // APPLY_SKILL,		51
	{ POINT_BOW_DISTANCE,		},   // APPLY_BOW_DISTANCE,	52
	{ POINT_ATT_GRADE_BONUS,	        },   // APPLY_ATT_GRADE,	53
	{ POINT_DEF_GRADE_BONUS,	        },   // APPLY_DEF_GRADE,	54
	{ POINT_MAGIC_ATT_GRADE_BONUS,      },   // APPLY_MAGIC_ATT_GRADE,	55
	{ POINT_MAGIC_DEF_GRADE_BONUS,      },   // APPLY_MAGIC_DEF_GRADE,	56
	{ POINT_CURSE_PCT,			},   // APPLY_CURSE_PCT,	57
	{ POINT_MAX_STAMINA			},   // APPLY_MAX_STAMINA	58
	{ POINT_ATTBONUS_WARRIOR		},   // APPLY_ATTBONUS_WARRIOR  59
	{ POINT_ATTBONUS_ASSASSIN		},   // APPLY_ATTBONUS_ASSASSIN 60
	{ POINT_ATTBONUS_SURA		},   // APPLY_ATTBONUS_SURA     61
	{ POINT_ATTBONUS_SHAMAN		},   // APPLY_ATTBONUS_SHAMAN   62
	{ POINT_ATTBONUS_MONSTER		},   //	APPLY_ATTBONUS_MONSTER  63
	{ POINT_ATT_BONUS		},   // 64 // APPLY_MALL_ATTBONUS
	{ POINT_MALL_DEFBONUS		},   // 65
	{ POINT_MALL_EXPBONUS		},   // 66 APPLY_MALL_EXPBONUS
	{ POINT_MALL_ITEMBONUS		},   // 67
	{ POINT_MALL_GOLDBONUS		},   // 68
	{ POINT_MAX_HP_PCT			},		// 69
	{ POINT_MAX_SP_PCT			},		// 70
	{ POINT_SKILL_DAMAGE_BONUS		},	// 71
	{ POINT_NORMAL_HIT_DAMAGE_BONUS	},	// 72

	// DEFEND_BONUS_ATTRIBUTES
	{ POINT_SKILL_DEFEND_BONUS		},	// 73
	{ POINT_NORMAL_HIT_DEFEND_BONUS	},	// 74
	// END_OF_DEFEND_BONUS_ATTRIBUTES

	{ POINT_PC_BANG_EXP_BONUS	},		// 75
	{ POINT_PC_BANG_DROP_BONUS	},		// 76

	{ POINT_NONE,		},

	{ POINT_RESIST_WARRIOR,		},
	{ POINT_RESIST_ASSASSIN,	},
	{ POINT_RESIST_SURA,		},
	{ POINT_RESIST_SHAMAN,		},
	{ POINT_ENERGY				},
	{ POINT_DEF_GRADE			},
	{ POINT_COSTUME_ATTR_BONUS	},
	{ POINT_MAGIC_ATT_BONUS_PER },
	{ POINT_MELEE_MAGIC_ATT_BONUS_PER		},			// 86 APPLY_MELEE_MAGIC_ATTBONUS_PER
	{ POINT_RESIST_ICE,			},   // APPLY_RESIST_ICE,	87
	{ POINT_RESIST_EARTH,		},   // APPLY_RESIST_EARTH,	88
	{ POINT_RESIST_DARK,		},   // APPLY_RESIST_DARK,	89
	{ POINT_RESIST_CRITICAL,		},   // APPLY_ANTI_CRITICAL_PCT,	90
	{ POINT_RESIST_PENETRATE,		},   // APPLY_ANTI_PENETRATE_PCT,	91

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	{ POINT_ACCEDRAIN_RATE,			},	// APPLY_ACCEDRAIN_RATE,		97
#endif

#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
	{ POINT_RESIST_MAGIC_REDUCTION,	},	// APPLY_RESIST_MAGIC_REDUCTION,98
#endif

	{ POINT_ENCHANT_ELECT,			},	// APPLY_ENCHANT_ELECT,99
	{ POINT_ENCHANT_FIRE,			},	// APPLY_ENCHANT_FIRE,100
	{ POINT_ENCHANT_ICE,			},	// APPLY_ENCHANT_ICE,101
	{ POINT_ENCHANT_WIND,			},	// APPLY_ENCHANT_WIND,102
	{ POINT_ENCHANT_EARTH,			},	// APPLY_ENCHANT_EARTH,103
	{ POINT_ENCHANT_DARK,			},	// APPLY_ENCHANT_DARK,104

	{ POINT_ATTBONUS_CZ,			},	// APPLY_ATTBONUS_CZ,105
	{ POINT_ATTBONUS_INSECT,		},	// APPLY_ATTBONUS_INSECT,106
	{ POINT_ATTBONUS_DESERT,		},	// APPLY_ATTBONUS_DESERT,107
	{ POINT_ATTBONUS_SWORD,			},	// APPLY_ATTBONUS_SWORD,108
	{ POINT_ATTBONUS_TWOHAND,		},	// APPLY_ATTBONUS_TWOHAND,109
	{ POINT_ATTBONUS_DAGGER,		},	// APPLY_ATTBONUS_DAGGER,110
	{ POINT_ATTBONUS_BELL,			},	// APPLY_ATTBONUS_BELL,111
	{ POINT_ATTBONUS_FAN,			},	// APPLY_ATTBONUS_FAN,112
	{ POINT_ATTBONUS_BOW,			},	// APPLY_ATTBONUS_BOW,113

	{ POINT_RESIST_HUMAN,			},	// APPLY_RESIST_HUMAN,115
	{ POINT_RESIST_MOUNT_FALL,		},	// APPLY_RESIST_MOUNT_FALL,116
	{ POINT_MOUNT,					},	// APPLY_MOUNT,118

#ifdef ENABLE_NEW_BONUS_SYSTEM
	{ POINT_ATTBONUS_STONE, },
	{ POINT_ATTBONUS_BOSS, },
	{ POINT_ATTBONUS_ELEMENTS, },
	{ POINT_ENCHANT_ELEMENTS, },
	{ POINT_ATTBONUS_CHARACTERS, },
	{ POINT_ENCHANT_CHARACTERS, },
	{ POINT_RESIST_MONSTER, },
#endif

#ifdef ENABLE_AVG_PVM
	{ POINT_ATTBONUS_MEDI_PVM },	// APPLY_ATTBONUS_MEDI_PVM,
#endif

	{ POINT_ATTBONUS_PVM_STR, },
	{ POINT_ATTBONUS_PVM_BERSERKER, },

#ifdef ENABLE_CONQUEROR_LEVEL
	{ POINT_SUNGMA_STR, },
	{ POINT_SUNGMA_HP, },
	{ POINT_SUNGMA_MOVE, },
	{ POINT_SUNGMA_IMMUNE, },
#endif
};

// Mid-effort PvP: slightly better natural/high attr rolls (lv4/lv5 more common).
const int aiItemMagicAttributePercentHigh[ITEM_ATTRIBUTE_MAX_LEVEL] =
{
	25, 35, 22, 12, 6
};

const int aiItemMagicAttributePercentLow[ITEM_ATTRIBUTE_MAX_LEVEL] =
{
	45, 40, 12, 3, 0
};

// ADD_ITEM_ATTRIBUTE
const int aiItemAttributeAddPercent[ITEM_ATTRIBUTE_MAX_NUM] =
{
	100, 80, 60, 50, 30, 0, 0,
};
// END_OF_ADD_ITEM_ATTRIBUTE

const int aiExpLossPercents[PLAYER_EXP_TABLE_MAX + 1] =
{
	0,
	5, 5, 5, 5, 5, 5, 5, 5, 5, 4, // 1 - 10
	4, 4, 4, 4, 4, 4, 4, 4, 4, 4, // 11 - 20
	4, 4, 4, 4, 4, 4, 4, 3, 3, 3, // 21 - 30
	3, 3, 3, 3, 3, 3, 3, 3, 3, 3, // 31 - 40
	3, 3, 3, 3, 2, 2, 2, 2, 2, 2, // 41 - 50
	2, 2, 2, 2, 2, 2, 2, 2, 2, 2, // 51 - 60
	2, 2, 1, 1, 1, 1, 1, 1, 1, 1, // 61 - 70
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 71 - 80
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 81 - 90
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 91 - 100
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 101 - 110
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, // 111 - 120

#ifdef ENABLE_LEVEL_INT
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 121 - 130
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 131 - 140
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 141 - 150
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 151 - 160
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 161 - 170
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 171 - 180
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 181 - 190
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 191 - 200
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 201 - 210
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 211 - 220
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 221 - 230
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 231 - 240
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 241 - 250
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 251 - 260
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 261 - 270
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 271 - 280
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 281 - 290
	1, 1, 1, 1, 1, 1, 1, 1, 1, 1,	// 291 - 300
#endif
};

const int aiSkillBookCountForLevelUp[10] =
{
	3, 3, 3, 3, 3, 4, 4, 5, 5, 6
};

// ADD_GRANDMASTER_SKILL
const int aiGrandMasterSkillBookCountForLevelUp[10] =
{
	3, 3, 5, 5, 7, 7, 10, 10, 10, 20,
};

const int aiGrandMasterSkillBookMinCount[10] =
{
	// 1, 1, 3, 5, 10, 15, 20, 30, 40, 50,
	// 3, 3, 5, 5, 10, 10, 15, 15, 20, 30
	1, 1, 1, 2, 2, 3, 3, 4, 5, 6
};

const int aiGrandMasterSkillBookMaxCount[10] =
{
	// 6, 15, 30, 45, 60, 80, 100, 120, 160, 200,
	// 6, 10, 15, 20, 30, 40, 50, 60, 70, 80
	5, 7, 9, 11, 13, 15, 20, 25, 30, 35
};
// END_OF_ADD_GRANDMASTER_SKILL

const int CHN_aiPartyBonusExpPercentByMemberCount[9] =
{
	0, 0, 12, 18, 26, 40, 53, 70, 100
};

const int* aiChainLightningCountBySkillLevel = NULL;

const int aiChainLightningCountBySkillLevel_euckr[SKILL_MAX_LEVEL + 1] =
{
	0, // 0
	2, // 1
	2, // 2
	2, // 3
	2, // 4
	2, // 5
	2, // 6
	2, // 7
	2, // 8
	3, // 9
	3, // 10
	3, // 11
	3, // 12
	3, // 13
	3, // 14
	3, // 15
	3, // 16
	3, // 17
	3, // 18
	4, // 19
	4, // 20
	4, // 21
	4, // 22
	4, // 23
	5, // 24
	5, // 25
	5, // 26
	5, // 27
	5, // 28
	5, // 29
	5, // 30
	5, // 31
	5, // 32
	5, // 33
	5, // 34
	5, // 35
	5, // 36
	5, // 37
	5, // 38
	5, // 39
	5, // 40
};

const SStoneDropInfo aStoneDrop[STONE_INFO_MAX_NUM] =
{
	// mob pct { +0 +1 +2 +3 +4 }
	{8005,	60,	{30,	30,	30,	9,	1}	},
	{8006,	60,	{28,	29,	31,	11,	1}	},
	{8007,	60,	{24,	29,	32,	13,	2}	},
	{8008,	60,	{22,	28,	33,	15,	2}	},
	{8009,	60,	{21,	27,	33,	17,	2}	},
	{8010,	60,	{18,	26,	34,	20,	2}	},
	{8011,	60,	{14,	26,	35,	22,	3}	},
	{8012,	60,	{10,	26,	37,	24,	3}	},
	{8013,	60,	{2,	26,	40,	29,	3}	},
	{8014,	60,	{0,	26,	41,	30,	3}	},
};

const char * c_apszEmpireNames[EMPIRE_MAX_NUM] =
{
	"Tüm krallýklar",
	"Shinsoo Krallýðý",
	"Chunjo Krallýðý",
	"Jinno Krallýðý"
};

const char * c_apszPrivNames[MAX_PRIV_NUM] =
{
	"",
	"Eþya düþme oraný yüzde olarak",
	"Yang düþme oraný yüzde olarak",
	"Yang yaðmuru düþme oraný",
	"Tecrübe yüzdesi",
};

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
std::string m_closeText[LOCALE_MAX_NUM] =
{
	"Close",
	"Close",
	"Închide",
	"Fechar",
	"Cerca",
	"Fermer",
	"Schließen",
	"Zamknac",
	"Vicina",
	"Zavrít",
	"Bezárás",
	"Kapat",
};

std::string m_horseText[LOCALE_MAX_NUM] =
{
	" Horse ",
	" Horse ",
	" Cal ",
	" Cavalo ",
	" Caballo ",
	" Cheval ",
	" Pferd ",
	" Kon ",
	" Cavallo ",
	" Kun ",
	" Ló ",
	" At ",
};
#endif

const int aiPolymorphPowerByLevel[SKILL_MAX_LEVEL + 1] =
{
	0,    // fix saga2
	10,   // 1
	11,   // 2
	11,   // 3
	12,   // 4
	13,   // 5
	13,   // 6
	14,   // 7
	15,   // 8
	16,   // 9
	17,   // 10
	18,   // 11
	19,   // 12
	20,   // 13
	22,   // 14
	23,   // 15
	24,   // 16
	26,   // 17
	27,   // 18
	29,   // 19
	31,   // 20
	33,   // 21
	35,   // 22
	37,   // 23
	39,   // 24
	41,   // 25
	44,   // 26
	46,   // 27
	49,   // 28
	52,   // 29
	55,   // 30
	59,   // 31
	62,   // 32
	66,   // 33
	70,   // 34
	74,   // 35
	79,   // 36
	84,   // 37
	89,   // 38
	94,   // 39
	100,  // 40
};

TGuildWarInfo KOR_aGuildWarInfo[GUILD_WAR_TYPE_MAX_NUM] =
/*
{
	long lMapIndex;
	int iWarPrice;
	int iWinnerPotionRewardPctToWinner;
	int iLoserPotionRewardPctToWinner;
	int iInitialScore;
	int iEndScore;
};
*/
{
	{ 0,        0,      0,      0,      0,      0       },
	{ 110,      0,      100,    50,     0,      100     },
	{ 111,      0,      100,    50,     0,      10      },
};

const int aiAccessorySocketAddPct[ITEM_ACCESSORY_SOCKET_MAX_NUM] =
{
	50, 50, 50
};

const int aiAccessorySocketEffectivePct[ITEM_ACCESSORY_SOCKET_MAX_NUM + 1] =
{
	0, 10, 20, 40
};

const int aiAccessorySocketDegradeTime[ITEM_ACCESSORY_SOCKET_MAX_NUM + 1] =
{
	0, 3600 * 24, 3600 * 12, 3600 * 6
};

const int aiAccessorySocketPutPct[ITEM_ACCESSORY_SOCKET_MAX_NUM + 1] =
{
	90, 80, 70, 0
};
// END_OF_ACCESSORY_REFINE

#ifdef ENABLE_GROWTH_PET_SYSTEM
const TPetEvolution arPetEvolutionTable[3] =
{
	{
		40,
		"the level Wild",
		{
			{55003,	10}, // Young Pet Book
			{30058, 10}, // Spider Egg Sack
			{30073, 10}, // White Hairband+
			{30041, 10}, // Shiriken
			{30017, 10}, // Ornamental Hairpin
			{30074, 5},	 // Black Uniform+
			{30088, 5},	 // Piece of Ice+
		}
	},

	{
		80,
		"the level Valiant",
		{
			{55004, 10}, // Wild Pet Book
			{27994, 2},  // Blood-Red Pearl
			{30035, 10}, // Face Cream
			{30089, 10}, // Yeti Fur+
			{30031, 10}, // Ornament
			{30011, 10}, // Ball
			{30080, 5},  // Curse Book+
		}
	},

	{
		81,
		"the level Heroic",
		{
			{55005, 10}, // Valiant Pet Book
			{30083, 10}, // Unknown Medicine+
			{27992, 2},  // White Pearl
			{27993, 2},  // Blue Pearl
			{30086, 10}, // Demon’s Keepsake+
			{30077, 10}, // Orc Tooth+
			{30550, 5},  // Blue Belt
		}
	},
};

const TPetHatch arPetHatchTable[PET_MAX_NUM] =
{
	{ PET_MONKEY,			2, 1, 14 },
	{ PET_SPIDER,			2, 1, 14 },
	{ PET_RAZADOR,			3, 1, 14 },
	{ PET_NEMERE,			3, 1, 14 },
	{ PET_BLUE_DRAGON,		3, 1, 14 },
	{ PET_RED_DRAGON,		3, 15, 45 },
	{ PET_AZRAEL,			2, 1, 14 },
	{ PET_MINI_EXECUTOR,	3, 1, 14 },
	{ PET_BASHIIDO,			3, 7, 28 },
	{ PET_NESSIE,			3, 15, 45 },
	{ PET_EXEDYAR,			3, 15, 45 },
};

const TPetBonus arPetHPBonusTable[PET_MAX_BONUS_NUM] =
{
	{1, 5},
	{2, 3},
	{1, 7},
	{3, 4},
	{1, 9},
	{5, 6},
	{1, 10},
	{5, 7},
};

const TPetBonus arPetSPBonusTable[PET_MAX_BONUS_NUM] =
{
	{1, 2},
	{2, 3},
	{1, 3},
	{3, 4},
	{1, 4},
	{4, 5},
	{1, 6},
	{5, 6},
};

const TPetBonus arPetDefBonusTable[PET_MAX_BONUS_NUM] =
{
	{1, 5},
	{2, 3},
	{1, 7},
	{3, 4},
	{1, 9},
	{4, 5},
	{1, 11},
	{5, 6},
};
#endif

#ifdef ENABLE_HUNTING_SYSTEM
const DWORD THuntingMissions[HUNTING_MISSION_COUNT+1][2][2] =
{
	// mob1 count1 , mob2 count2,
	{{0, 0}, {0, 0}}, // None
	{{171, 5}, {172, 3}},		// Lv1
	{{171, 10}, {172, 5}},		// Lv2
	{{171, 20}, {172, 10}},		// Lv3
	{{172, 15}, {173, 5}},		// Lv4
	{{173, 10}, {174, 10}},		// Lv5
	{{174, 20}, {178, 10}},		// Lv6
	{{178, 10}, {175, 5}},		// Lv7
	{{178, 20}, {175, 10}},		// Lv8
	{{175, 15}, {179, 5}},		// Lv9
	{{175, 20}, {179, 10}},		// Lv10
	
	{{179, 10}, {180, 5}},		// Lv11
	{{180, 15}, {176, 10}},		// Lv12
	{{176, 20}, {181, 5}},		// Lv13
	{{181, 15}, {177, 5}},		// Lv14
	{{181, 20}, {177, 10}},		// Lv15
	{{177, 15}, {184, 5}},		// Lv16
	{{177, 20}, {184, 10}},		// Lv17
	{{184, 10}, {182, 10}},		// Lv18
	{{182, 20}, {183, 10}},		// Lv19
	{{183, 20}, {352, 15}},		// Lv20
	
	{{352, 10}, {185, 10}},		// Lv21
	{{185, 25}, {354, 10}},		// Lv22
	{{354, 20}, {451, 40}},		// Lv23
	{{451, 60}, {402, 80}},		// Lv24
	{{551, 80}, {454, 20}},		// Lv25
	{{552, 80}, {456, 20}},		// Lv26
	{{456, 30}, {554, 20}},		// Lv27
	{{651, 35}, {554, 30}},		// Lv28
	{{651, 40}, {652, 30}},		// Lv29
	{{652, 40}, {2102, 30}},	// Lv30
	
	{{652, 50}, {2102, 45}},	// Lv31
	{{653, 25}, {2051, 40}},	// Lv32
	{{751, 35}, {2103, 30}},	// Lv33
	{{751, 40}, {2103, 40}},	// Lv34
	{{752, 40}, {2052, 30}},	// Lv35
	{{754, 20}, {2106, 20}},	// Lv36
	{{773, 30}, {2003, 20}},	// Lv37
	{{774, 40}, {2004, 20}},	// Lv38
	{{756, 40}, {2005, 30}},	// Lv39
	{{757, 40}, {2158, 20}},	// Lv40
	
	{{931, 40}, {5123, 25}},	// Lv41
	{{932, 30}, {5123, 30}},	// Lv42
	{{932, 40}, {2031, 35}},	// Lv43
	{{933, 40}, {2031, 30}},	// Lv44
	{{771, 50}, {2032, 45}},	// Lv45
	{{772, 30}, {5124, 30}},	// Lv46
	{{933, 35}, {5125, 30}},	// Lv47
	{{934, 40}, {5125, 35}},	// Lv48
	{{773, 40}, {2033, 45}},	// Lv49
	{{774, 40}, {5126, 20}},	// Lv50
	
	{{775, 50}, {5126, 30}},	// Lv51
	{{934, 45}, {2034, 45}},	// Lv52
	{{934, 50}, {2034, 50}},	// Lv53
	{{776, 40}, {1001, 30}},	// Lv54
	{{777, 40}, {1301, 35}},	// Lv55
	{{935, 50}, {1002, 30}},	// Lv56
	{{935, 60}, {1002, 40}},	// Lv57
	{{936, 45}, {1303, 40}},	// Lv58
	{{936, 50}, {1303, 45}},	// Lv59
	{{937, 45}, {1003, 40}},	// Lv60
	
	{{1004, 50}, {2061, 60}},	// Lv61
	{{1305, 45}, {2131, 55}},	// Lv62
	{{1305, 50}, {1101, 45}},	// Lv63
	{{2062, 50}, {1102, 45}},	// Lv64
	{{1104, 40}, {2063, 40}},	// Lv65
	{{2301, 50}, {1105, 45}},	// Lv66
	{{2301, 55}, {1105, 50}},	// Lv67
	{{1106, 50}, {1061, 50}},	// Lv68
	{{1107, 45}, {1061, 50}},	// Lv69
	{{2302, 55}, {2201, 55}},	// Lv70
	
	{{2303, 55}, {2202, 55}},	// Lv71
	{{2303, 60}, {2202, 60}},	// Lv72
	{{2304, 55}, {1063, 55}},	// Lv73
	{{2305, 50}, {1063, 55}},	// Lv74
	{{1064, 50}, {2204, 50}},	// Lv75
	{{2205, 45}, {1035, 50}},	// Lv76
	{{2311, 50}, {1068, 50}},	// Lv77
	{{1070, 50}, {1066, 55}},	// Lv78
	{{1069, 50}, {1070, 50}},	// Lv79
	{{1071, 50}, {2312, 55}},	// Lv80
	
	{{1071, 55}, {2312, 50}},	// Lv81
	{{2313, 55}, {2314, 45}},	// Lv82
	{{2313, 55}, {2314, 45}},	// Lv83
	{{1131, 60}, {2315, 50}},	// Lv84
	{{1132, 60}, {2315, 45}},	// Lv85
	{{1132, 60}, {1135, 50}},	// Lv86
	{{1132, 60}, {1135, 50}},	// Lv87
	{{1133, 60}, {1136, 50}},	// Lv88
	{{1133, 60}, {1137, 50}},	// Lv89
	{{1132, 60}, {1137, 50}},	// Lv80
};

const DWORD THuntingRewardItem[HUNTING_MISSION_COUNT+1][2][4][2] =
{
	/*
	{ mission_type 1 = { warrior {vnum, count} | assassine {vnum, count} | sura {vnum, count} | shaman {vnum, count} } }
	{ mission_type 2 = { warrior {vnum, count} | assassine {vnum, count} | sura {vnum, count} | shaman {vnum, count} } }
	*/
	
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Yok
	{{{13, 1}, {13, 1}, {13, 1}, {7003, 1}}, {{3003, 1}, {1003, 1}, {13, 1}, {5003, 1}}},					// Seviye 1 - Silahlar
	{{{11203, 1}, {11403, 1}, {11603, 1}, {11803, 1}}, {{11205, 1}, {11405, 1}, {11605, 1}, {11805, 1}}},	// Seviye 2 - Zýrhlar
	{{{13003, 1}, {13003, 1}, {13003, 1}, {13003, 1}}, {{13005, 1}, {13005, 1}, {13005, 1}, {13005, 1}}},	// Seviye 3 - Kalkan
	{{{12203, 1}, {12343, 1}, {12483, 1}, {12623, 1}}, {{12205, 1}, {12345, 1}, {12485, 1}, {12625, 1}}},	// Seviye 4 - Miðfer
	{{{14005, 1}, {14005, 1}, {14005, 1}, {14005, 1}}, {{14025, 1}, {14025, 1}, {14025, 1}, {14025, 1}}},	// Seviye 5 - Bilezik
	{{{16005, 1}, {16005, 1}, {16005, 1}, {16005, 1}}, {{16025, 1}, {16025, 1}, {16025, 1}, {16025, 1}}},	// Seviye 6 - Kolye
	{{{17005, 1}, {17005, 1}, {17005, 1}, {17005, 1}}, {{17025, 1}, {17025, 1}, {17025, 1}, {17025, 1}}},	// Seviye 7 - Küpe
	{{{15005, 1}, {15005, 1}, {15005, 1}, {15005, 1}}, {{15025, 1}, {15025, 1}, {15025, 1}, {15025, 1}}},	// Seviye 8 - Ayakkabý
	{{{11213, 1}, {11413, 1}, {11613, 1}, {11813, 1}}, {{11215, 1}, {11415, 1}, {11615, 1}, {11815, 1}}},	// Seviye 9 - Zýrhlar (Seviye 9 Serisi)
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 10 - Yok

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 11
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 12
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 13
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 14
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 15
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 16
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 17
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 18
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 19
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 20

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 21
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 22
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 23
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 24
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 25
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 26
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 27
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 28
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 29
	{{{296, 1}, {296, 1}, {296, 1}, {7166, 1}}, {{3216, 1}, {1176, 1}, {296, 1}, {5116, 1}}},				// Seviye 30 - 30 Seviye silahlar

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 31
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 32
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 33
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 34
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 35
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 36
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 37
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 38
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 39
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 40

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 41
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 42
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 43
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 44
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 45
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 46
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 47
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 48
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 49
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 50

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 51
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 52
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 53
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 54
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 55
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 56
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 57
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 58
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 59
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 60

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 61
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 62
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 63
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 64
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 65
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 66
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 67
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 68
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 69
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 70

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 71
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 72
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 73
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 74
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 75
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 76
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 77
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 78
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 79
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 80

	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 81
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 82
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 83
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 84
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 85
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 86
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 87
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 88
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 89
	{{{0, 0}, {0, 0}, {0, 0}, {0, 0}}, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}},									// Seviye 90
};

const SHuntingRewardMoney THuntingRewardMoney[HUNTING_MONEY_TABLE_SIZE] =
{
	/*
	Note: The total of all Chances in Level = 100
	from_level, to_level {amount, chance} | {amount, chance} | {amount, chance} | {amount, chance} | {amount, chance}
	*/

	{ 1, 10,	{10000, 20000, 30000, 40000, 50000}},				// Seviye 1-10
	{11, 20,	{20000, 30000, 50000, 70000, 100000}},				// Seviye 11-20
	{21, 30,	{20000, 40000, 60000, 90000, 120000}},				// Seviye 21-30
	{31, 40,	{50000, 80000, 120000, 150000, 200000}},			// Seviye 31-40
	{41, 50,	{100000, 150000, 200000, 300000, 400000}},			// Seviye 41-50
	{51, 60,	{200000, 300000, 400000, 500000, 750000}},			// Seviye 51-60
	{61, 70,	{500000, 750000, 1000000, 1250000, 1500000}},		// Seviye 61-70
	{71, 80,	{1000000, 1500000, 2000000, 2500000, 3500000}},		// Seviye 71-80
	{81, 90,	{3000000, 4000000, 5000000, 7500000, 10000000}}, 	// Seviye 81-90
};

const SHuntingRewardEXP THuntingRewardEXP[HUNTING_EXP_TABLE_SIZE] =
{
	/*
	Not: Her seviye aralýðý için yüzde EXP oraný
	from_level, to_level {percent_min, percent_max}
	*/

	{ 1, 10, {10, 25}}, // Seviye 1-10
	{11, 20, {10, 20}}, // Seviye 11-20
	{21, 30, {10, 15}}, // Seviye 21-30
	{31, 40, {5, 15}},  // Seviye 31-40
	{41, 50, {5, 12}},  // Seviye 41-50
	{51, 60, {3, 10}},  // Seviye 51-60
	{61, 70, {3, 8}},   // Seviye 61-70
	{71, 80, {3, 5}},   // Seviye 71-80
	{81, 90, {2, 5}},   // Seviye 81-90
};

const DWORD THuntingRandomItem_01_20[6][2] =
{
	{27102, 3},		// Yeþil Ýksir G
	{27105, 3},		// Mor Ýksir G
	{71151, 5},		// Yeþil Büyü
	{71152, 2},		// Yeþil Güç
	{70038, 25},	// Cesaret Pelerini
	{25040, 2},		// Kutsama Kaðýdý
};

const DWORD THuntingRandomItem_21_40[13][2] =
{
	{25040, 3},	// Kutsama Kaðýdý
	{25041, 1},	// Sihirli Metal
	{55401, 1},	// Maymun Yumurtasý
	{55402, 1},	// Örümcek Yumurtasý
	{50300, 3},	// Beceri Kitabý
	{70048, 1},	// Kaçýþ Pelerini
	{70049, 1},	// Lucy'nin Yüzüðü
	{70050, 1},	// Bilge Ýmparatorun Simgesi
	{70051, 1},	// Bilge Ýmparatorun Eldiveni
	{71027, 1},	// Ejderha Tanrýsý – Can
	{71028, 1},	// Ejderha Tanrýsý – Saldýrý
	{71029, 1},	// Ejderha Tanrýsý – Zeka
	{71030, 1},	// Ejderha Tanrýsý – Savunma
};

const DWORD THuntingRandomItem_41_60[13][2] =
{
	{25040, 3},	// Kutsama Kaðýdý
	{25041, 1},	// Sihirli Metal
	{55401, 1},	// Maymun Yumurtasý
	{55402, 1},	// Örümcek Yumurtasý
	{50300, 3},	// Beceri Kitabý
	{70048, 1},	// Kaçýþ Pelerini
	{70049, 1},	// Lucy'nin Yüzüðü
	{70050, 1},	// Bilge Ýmparatorun Simgesi
	{70051, 1},	// Bilge Ýmparatorun Eldiveni
	{71027, 1},	// Ejderha Tanrýsý – Can
	{71028, 1},	// Ejderha Tanrýsý – Saldýrý
	{71029, 1},	// Ejderha Tanrýsý – Zeka
	{71030, 1},	// Ejderha Tanrýsý – Savunma
};

const DWORD THuntingRandomItem_61_80[13][2] =
{
	{25040, 3},	// Kutsama Kaðýdý
	{25041, 1},	// Sihirli Metal
	{55401, 1},	// Maymun Yumurtasý
	{55402, 1},	// Örümcek Yumurtasý
	{50300, 3},	// Beceri Kitabý
	{70048, 1},	// Kaçýþ Pelerini
	{70049, 1},	// Lucy'nin Yüzüðü
	{70050, 1},	// Bilge Ýmparatorun Simgesi
	{70051, 1},	// Bilge Ýmparatorun Eldiveni
	{71027, 1},	// Ejderha Tanrýsý – Can
	{71028, 1},	// Ejderha Tanrýsý – Saldýrý
	{71029, 1},	// Ejderha Tanrýsý – Zeka
	{71030, 1},	// Ejderha Tanrýsý – Savunma
};

const DWORD THuntingRandomItem_81_90[13][2] =
{
	{25040, 3},	// Kutsama Kaðýdý
	{25041, 1},	// Sihirli Metal
	{55401, 1},	// Maymun Yumurtasý
	{55402, 1},	// Örümcek Yumurtasý
	{50300, 3},	// Beceri Kitabý
	{70048, 1},	// Kaçýþ Pelerini
	{70049, 1},	// Lucy'nin Yüzüðü
	{70050, 1},	// Bilge Ýmparatorun Simgesi
	{70051, 1},	// Bilge Ýmparatorun Eldiveni
	{71027, 1},	// Ejderha Tanrýsý – Can
	{71028, 1},	// Ejderha Tanrýsý – Saldýrý
	{71029, 1},	// Ejderha Tanrýsý – Zeka
	{71030, 1},	// Ejderha Tanrýsý – Savunma
};
#endif

#ifdef ENABLE_BIOLOGIST_SYSTEM
const DWORD BiyologSistemi[11][14] =
{
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 30006, 10, 0, 100, 30220, 50109, 8, 10, 0, 0, 0, 0, 0, 0 },
	{ 30047, 15, 0, 100, 30221, 50110, 7, 5, 0, 0, 0, 0, 0, 0 },
	{ 30015, 15, 0, 100, 30222, 50111, 54, 60, 0, 0, 0, 0, 0, 0 },
	{ 30050, 20, 0, 100, 30223, 50112, 53, 50, 0, 0, 0, 0, 0, 0 },
	{ 30165, 25, 0, 100, 30224, 50113, 8, 11, 7, 10, 0, 0, 0, 0 },
	{ 30166, 30, 0, 100, 30225, 50114, 7, 6, 64, 10, 0, 0, 0, 0 },
	{ 30167, 40, 0, 100, 30226, 50115, APPLY_RESIST_WARRIOR, 10, APPLY_RESIST_ASSASSIN, 10, APPLY_RESIST_SURA, 10, APPLY_RESIST_SHAMAN, 10 },
	{ 30168, 50, 30, 50, 30227, 50114, 59, 8, 60, 8, 61, 8, 62, 8 },
	{ 30251, 10, 60, 40, 0, 0, 1, 1000, 54, 120, 53, 50, 0, 0 },
	{ 30252, 20, 60, 60, 30228, 0, 1, 1100, 54, 140, 53, 60, 0, 0 }
};
#endif

typedef struct SValueName
{
	const char *c_pszName;
	long lValue;
} TValueName;

TValueName c_aApplyTypeNames[] =
{
	{ "STR",		APPLY_STR		},
	{ "DEX",		APPLY_DEX		},
	{ "CON",		APPLY_CON		},
	{ "INT",		APPLY_INT		},
	{ "MAX_HP",		APPLY_MAX_HP		},
	{ "MAX_SP",		APPLY_MAX_SP		},
	{ "MAX_STAMINA",	APPLY_MAX_STAMINA	},
	{ "POISON_REDUCE",	APPLY_POISON_REDUCE	},
	{ "EXP_DOUBLE_BONUS", APPLY_EXP_DOUBLE_BONUS },
	{ "GOLD_DOUBLE_BONUS", APPLY_GOLD_DOUBLE_BONUS },
	{ "ITEM_DROP_BONUS", APPLY_ITEM_DROP_BONUS	},
	{ "HP_REGEN",	APPLY_HP_REGEN		},
	{ "SP_REGEN",	APPLY_SP_REGEN		},
	{ "ATT_SPEED",	APPLY_ATT_SPEED		},
	{ "MOV_SPEED",	APPLY_MOV_SPEED		},
	{ "CAST_SPEED",	APPLY_CAST_SPEED	},
	{ "ATT_BONUS",	APPLY_ATT_GRADE_BONUS	},
	{ "DEF_BONUS",	APPLY_DEF_GRADE_BONUS	},
	{ "MAGIC_ATT_GRADE",APPLY_MAGIC_ATT_GRADE	},
	{ "MAGIC_DEF_GRADE",APPLY_MAGIC_DEF_GRADE	},
	{ "SKILL",		APPLY_SKILL		},
	{ "ATTBONUS_ANIMAL",APPLY_ATTBONUS_ANIMAL	},
	{ "ATTBONUS_UNDEAD",APPLY_ATTBONUS_UNDEAD	},
	{ "ATTBONUS_DEVIL", APPLY_ATTBONUS_DEVIL	},
	{ "ATTBONUS_HUMAN", APPLY_ATTBONUS_HUMAN	},
	{ "ADD_BOW_DISTANCE",APPLY_BOW_DISTANCE	},
	{ "DODGE",		APPLY_DODGE		},
	{ "BLOCK",		APPLY_BLOCK		},
	{ "RESIST_SWORD",	APPLY_RESIST_SWORD	},
	{ "RESIST_TWOHAND",	APPLY_RESIST_TWOHAND	},
	{ "RESIST_DAGGER",	APPLY_RESIST_DAGGER    },
	{ "RESIST_BELL",	APPLY_RESIST_BELL	},
	{ "RESIST_FAN",	APPLY_RESIST_FAN	},
	{ "RESIST_BOW",	APPLY_RESIST_BOW	},
	{ "RESIST_FIRE",	APPLY_RESIST_FIRE	},
	{ "RESIST_ELEC",	APPLY_RESIST_ELEC	},
	{ "RESIST_MAGIC",	APPLY_RESIST_MAGIC	},
	{ "RESIST_WIND",	APPLY_RESIST_WIND	},
	{ "REFLECT_MELEE",	APPLY_REFLECT_MELEE },
	{ "REFLECT_CURSE",	APPLY_REFLECT_CURSE },
	{ "RESIST_ICE",		APPLY_RESIST_ICE	},
	{ "RESIST_EARTH",	APPLY_RESIST_EARTH	},
	{ "RESIST_DARK",	APPLY_RESIST_DARK	},
	{ "RESIST_CRITICAL",	APPLY_ANTI_CRITICAL_PCT	},
	{ "RESIST_PENETRATE",	APPLY_ANTI_PENETRATE_PCT	},
	{ "POISON",		APPLY_POISON_PCT	},
	{ "SLOW",		APPLY_SLOW_PCT		},
	{ "STUN",		APPLY_STUN_PCT		},
	{ "STEAL_HP",	APPLY_STEAL_HP		},
	{ "STEAL_SP",	APPLY_STEAL_SP		},
	{ "MANA_BURN_PCT",	APPLY_MANA_BURN_PCT	},
	{ "CRITICAL",	APPLY_CRITICAL_PCT	},
	{ "PENETRATE",	APPLY_PENETRATE_PCT	},
	{ "KILL_SP_RECOVER",APPLY_KILL_SP_RECOVER	},
	{ "KILL_HP_RECOVER",APPLY_KILL_HP_RECOVER	},
	{ "PENETRATE_PCT",	APPLY_PENETRATE_PCT	},
	{ "CRITICAL_PCT",	APPLY_CRITICAL_PCT	},
	{ "POISON_PCT",	APPLY_POISON_PCT	},
	{ "STUN_PCT",	APPLY_STUN_PCT		},
	{ "ATT_BONUS_TO_WARRIOR",	APPLY_ATTBONUS_WARRIOR  },
	{ "ATT_BONUS_TO_ASSASSIN",	APPLY_ATTBONUS_ASSASSIN },
	{ "ATT_BONUS_TO_SURA",	APPLY_ATTBONUS_SURA	    },
	{ "ATT_BONUS_TO_SHAMAN",	APPLY_ATTBONUS_SHAMAN   },
	{ "ATT_BONUS_TO_MONSTER",	APPLY_ATTBONUS_MONSTER  },
	{ "ATT_BONUS_TO_MOB",	APPLY_ATTBONUS_MONSTER  },
	{ "MALL_ATTBONUS",	APPLY_MALL_ATTBONUS	},
	{ "MALL_EXPBONUS",	APPLY_MALL_EXPBONUS	},
	{ "MALL_DEFBONUS",	APPLY_MALL_DEFBONUS	},
	{ "MALL_ITEMBONUS",	APPLY_MALL_ITEMBONUS	},
	{ "MALL_GOLDBONUS", APPLY_MALL_GOLDBONUS	},
	{ "MAX_HP_PCT",	APPLY_MAX_HP_PCT	},
	{ "MAX_SP_PCT",	APPLY_MAX_SP_PCT	},
	{ "SKILL_DAMAGE_BONUS",	APPLY_SKILL_DAMAGE_BONUS	},
	{ "NORMAL_HIT_DAMAGE_BONUS",APPLY_NORMAL_HIT_DAMAGE_BONUS	},
	{ "SKILL_DEFEND_BONUS",	APPLY_SKILL_DEFEND_BONUS	},
	{ "NORMAL_HIT_DEFEND_BONUS",APPLY_NORMAL_HIT_DEFEND_BONUS	},

	{ "PCBANG_EXP_BONUS", APPLY_PC_BANG_EXP_BONUS	},
	{ "PCBANG_DROP_BONUS", APPLY_PC_BANG_DROP_BONUS	},

	{ "RESIST_WARRIOR",	APPLY_RESIST_WARRIOR},
	{ "RESIST_ASSASSIN",	APPLY_RESIST_ASSASSIN},
	{ "RESIST_SURA",		APPLY_RESIST_SURA},
	{ "RESIST_SHAMAN",	APPLY_RESIST_SHAMAN},
	{ "INFINITE_AFFECT_DURATION", 0x1FFFFFFF	},
	{ "ENERGY", APPLY_ENERGY },
	{ "COSTUME_ATTR_BONUS", APPLY_COSTUME_ATTR_BONUS },
	{ "MAGIC_ATTBONUS_PER",	APPLY_MAGIC_ATTBONUS_PER	},
	{ "MELEE_MAGIC_ATTBONUS_PER",	APPLY_MELEE_MAGIC_ATTBONUS_PER	},

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	{ "ACCEDRAIN_RATE",APPLY_ACCEDRAIN_RATE },
#endif
#ifdef ENABLE_MAGIC_REDUCTION_SYSTEM
	{ "RESIST_MAGIC_REDUCTION",APPLY_RESIST_MAGIC_REDUCTION },
#endif

	{ "ENCHANT_ELECT", APPLY_ENCHANT_ELECT },
	{ "ENCHANT_FIRE", APPLY_ENCHANT_FIRE },
	{ "ENCHANT_ICE", APPLY_ENCHANT_ICE },
	{ "ENCHANT_WIND", APPLY_ENCHANT_WIND },
	{ "ENCHANT_EARTH", APPLY_ENCHANT_EARTH },
	{ "ENCHANT_DARK", APPLY_ENCHANT_DARK },

#ifdef ENABLE_NEW_BONUS_SYSTEM
	{ "ATTBONUS_STONE", APPLY_ATTBONUS_STONE },
	{ "ATTBONUS_BOSS", APPLY_ATTBONUS_BOSS },
	{ "ATTBONUS_ELEMENTS", APPLY_ATTBONUS_ELEMENTS },
	{ "ENCHANT_ELEMENTS", APPLY_ENCHANT_ELEMENTS },
	{ "ATTBONUS_CHARACTERS",APPLY_ATTBONUS_CHARACTERS },
	{ "ENCHANT_CHARACTERS", APPLY_ENCHANT_CHARACTERS },
	{ "RESIST_MONSTER", APPLY_RESIST_MONSTER },
#endif

#ifdef ENABLE_AVG_PVM
	{ "ATTBONUS_MEDI_PVM", APPLY_ATTBONUS_MEDI_PVM },
#endif

#ifdef ENABLE_CONQUEROR_LEVEL
	{ "SUNGMA_STR", APPLY_SUNGMA_STR },
	{ "SUNGMA_HP", APPLY_SUNGMA_HP },
	{ "SUNGMA_MOVE", APPLY_SUNGMA_MOVE },
	{ "SUNGMA_IMMUNE", APPLY_SUNGMA_IMMUNE },
#endif
	{ "ATTBONUS_PVM_STR",	APPLY_ATTBONUS_PVM_STR },
	{ "ATTBONUS_PVM_BERSERKER",	APPLY_ATTBONUS_PVM_BERSERKER },
	{ NULL,		0			}
};

// from import_item_proto.c
long FN_get_apply_type(const char* apply_type_string)
{
	TValueName* value_name;
	for (value_name = c_aApplyTypeNames; value_name->c_pszName; ++value_name)
	{
		if (0 == strcasecmp(value_name->c_pszName, apply_type_string))
			return value_name->lValue;
	}
	return 0;
}

#ifdef __DUNGEON_INFO__
const std::map<DWORD, std::pair<std::pair<BYTE, BYTE>, std::string>> m_mapDungeonList = {
	//bossIdx, {{minLvl, maxLvl}, questName},
	{1093, {{40, 95}, "deviltower_zone"}},
	{5127, {{50, 90}, "monkeydungeon_zone"}},
	{2092, {{70, 90}, "spiderdungeon3_zone"}},
	{2493, {{70, 105}, "dragonlair_zone"}},
	{2598, {{80, 105}, "devilcatacomb_zone"}},
	{6091, {{90, 120}, "flamedungeon_zone"}},
	{6191, {{90, 120}, "snowdungeon_zone"}},
	{6192, {{105, 120}, "erebus_zone"}},
	{9018, {{105, 120}, "ShipDefense"}},
	{20442, {{110, 120}, "MeleyDungeon"}},
	{4042, {{55, 80}, "nightMare_zone"}},
	{4031, {{115, 120}, "duratusDungeon_zone"}},
	{9838, {{105, 120}, "zodiactemple_zone"}},
	{6500, {{110, 120}, "akzadurlair_zone"}},
	{6756, {{120, 120}, "serpent_zone"}},
	{6790, {{120, 120}, "rxdragonlair_zone"}},
};
#endif

#ifdef ENABLE_RESP_SYSTEM
std::set<uint32_t> g_setRespAllowedMap = {
	1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 20, 22, 23
};
#endif
