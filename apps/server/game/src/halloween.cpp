#include "stdafx.h"
#include "char.h"

int iConfigRewardHaloun[4][2] = 
{
	// ITEM_VNUM, COUNTS
	{	8706,	1},
	{	8706,	1},
	{	8706,	1},
	
	// Auto() Final reward
	{	8706,	1},
};

void CHARACTER::OpenHalloween()
{
	for (int i = 0; i<4; ++i){	ChatPacket(CHAT_TYPE_COMMAND, "halloween_rewards %d %d %d", i, iConfigRewardHaloun[i][0], iConfigRewardHaloun[i][1]);}
	ChatPacket(CHAT_TYPE_COMMAND, "eveniment_haloun %d", 1);
	ChatPacket(CHAT_TYPE_COMMAND, "level_halloween %d", GetHalounLv()-1);
	ChatPacket(CHAT_TYPE_COMMAND, "points_halloween %d", GetHalounPoints());
}

void CHARACTER::IncreaseNivel()
{
	if (GetHalounLv() == 4)
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Tebrikler! %d seviyesine ulaþtýn ve bir bonus kazandýn!"), GetHalounLv());
		PointChange(POINT_RHALOUN, 1);
	}
	if (GetHalounLv() == 9)
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Tebrikler! %d seviyesine ulaþtýn ve bir bonus kazandýn!"), GetHalounLv());
		PointChange(POINT_RHALOUN, 1);
	}
	if (GetHalounLv() == 13)
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Tebrikler! %d seviyesine ulaþtýn ve bir bonus kazandýn!"), GetHalounLv());
		PointChange(POINT_RHALOUN, 1);
	}
	if (GetHalounLv() == 17)
	{
		ChatPacket(CHAT_TYPE_INFO, LC_TEXT("Tebrikler! Son seviyeye ulaþtýn ve bir bonus kazandýn!"));
		PointChange(POINT_HALOUNLV, -GetHalounLv());
		PointChange(POINT_HALOUN, -GetHalounPoints());
		AutoGiveItem(iConfigRewardHaloun[0][0], iConfigRewardHaloun[0][1]);
		ChatPacket(CHAT_TYPE_COMMAND, "eveniment_haloun %d", 0);
	}

	ChatPacket(CHAT_TYPE_COMMAND, "level_halloween %d", GetHalounLv()-1);
	ChatPacket(CHAT_TYPE_COMMAND, "points_halloween %d", GetHalounPoints());
}
