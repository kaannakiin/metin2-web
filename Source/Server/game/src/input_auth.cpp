#include "stdafx.h"

#include "../../common/service.h"

#include "constants.h"
#include "config.h"
#include "input.h"
#include "desc_client.h"
#include "desc_manager.h"
#include "protocol.h"
#include "locale_service.h"
#include "db.h"

extern time_t get_global_time();

namespace
{
	struct SLoginFailures
	{
		int		iCount;
		time_t	tWindowEnd;
		time_t	tLockedUntil;
	};

	const int LOGIN_FAILURE_LIMIT_PER_ACCOUNT = 5;
	const int LOGIN_FAILURE_LIMIT_PER_HOST = 20;
	const time_t LOGIN_FAILURE_WINDOW = 300;
	const size_t LOGIN_FAILURE_MAX_ENTRIES = 10000;

	std::unordered_map<std::string, SLoginFailures> s_mapLoginFailures;

	std::string AccountKey(const char* c_szLogin)
	{
		char szLogin[LOGIN_MAX_LEN + 1];
		trim_and_lower(c_szLogin, szLogin, sizeof(szLogin));
		return std::string("a:") + szLogin;
	}

	bool IsLocked(const std::string& stKey)
	{
		auto it = s_mapLoginFailures.find(stKey);
		return it != s_mapLoginFailures.end() && it->second.tLockedUntil > get_global_time();
	}

	void AddFailure(const std::string& stKey, int iLimit)
	{
		const time_t tNow = get_global_time();

		if (s_mapLoginFailures.size() >= LOGIN_FAILURE_MAX_ENTRIES)
		{
			for (auto it = s_mapLoginFailures.begin(); it != s_mapLoginFailures.end();)
			{
				if (it->second.tWindowEnd <= tNow && it->second.tLockedUntil <= tNow)
					it = s_mapLoginFailures.erase(it);
				else
					++it;
			}
		}

		SLoginFailures& r = s_mapLoginFailures[stKey];
		if (r.tWindowEnd <= tNow)
		{
			r.iCount = 0;
			r.tWindowEnd = tNow + LOGIN_FAILURE_WINDOW;
		}

		if (++r.iCount >= iLimit)
			r.tLockedUntil = tNow + LOGIN_FAILURE_WINDOW;
	}
}

bool IsLoginThrottled(LPDESC d, const char* c_szLogin)
{
	if (IsLocked(AccountKey(c_szLogin)))
		return true;

	return !IsTrustedProxyIP(d->GetHostName()) && IsLocked(std::string("h:") + d->GetHostName());
}

void OnLoginFailed(LPDESC d, const char* c_szLogin)
{
	AddFailure(AccountKey(c_szLogin), LOGIN_FAILURE_LIMIT_PER_ACCOUNT);

	if (!IsTrustedProxyIP(d->GetHostName()))
		AddFailure(std::string("h:") + d->GetHostName(), LOGIN_FAILURE_LIMIT_PER_HOST);
}

void OnLoginSucceeded(const char* c_szLogin)
{
	s_mapLoginFailures.erase(AccountKey(c_szLogin));
}

bool FN_IS_VALID_LOGIN_STRING(const char *str)
{
	const char*	tmp;

	if (!str || !*str)
		return false;

	if (strlen(str) < 2)
		return false;

	for (tmp = str; *tmp; ++tmp)
	{
		// Only alphanumeric characters allowed
		if (isdigit(*tmp) || isalpha(*tmp))
			continue;

		return false;
	}

	return true;
}

bool Login_IsInChannelService(const char* c_login)
{
	if (c_login[0] == '[')
		return true;
	return false;
}

CInputAuth::CInputAuth()
{
}

void CInputAuth::Login(LPDESC d, const char * c_pData)
{
	TPacketCGLogin3 * pinfo = (TPacketCGLogin3 *) c_pData;

	if (!g_bAuthServer)
	{
		sys_err ("CInputAuth class is not for game server. IP %s might be a hacker.",
			inet_ntoa(d->GetAddr().sin_addr));
		d->DelayedDisconnect(5);
		return;
	}

	// copy for string integrity
	char login[LOGIN_MAX_LEN + 1];
	trim_and_lower(pinfo->login, login, sizeof(login));

	char passwd[PASSWD_MAX_LEN + 1];
	strlcpy(passwd, pinfo->passwd, sizeof(passwd));

	sys_log(0, "InputAuth::Login : %s(%d) desc %p",
			login, strlen(login), get_pointer(d));

	// check login string
	if (false == FN_IS_VALID_LOGIN_STRING(login))
	{
		sys_log(0, "InputAuth::Login : IS_NOT_VALID_LOGIN_STRING(%s) desc %p",
				login, get_pointer(d));
		LoginFailure(d, "NOID");
		return;
	}

	if (IsLoginThrottled(d, login))
	{
		sys_log(0, "InputAuth::Login : throttled %s from %s", login, d->GetHostName());
		LoginFailure(d, "BLKLOGIN");
		return;
	}

	if (g_bNoMoreClient)
	{
		TPacketGCLoginFailure failurePacket;

		failurePacket.header = HEADER_GC_LOGIN_FAILURE;
		strlcpy(failurePacket.szStatus, "SHUTDOWN", sizeof(failurePacket.szStatus));

		d->Packet(&failurePacket, sizeof(failurePacket));
		return;
	}

	if (DESC_MANAGER::instance().FindByLoginName(login))
	{
		LoginFailure(d, "ALREADY");
		return;
	}

#ifdef ENABLE_RENEWAL_CLIENT_VERSION
	if (strncmp(g_stClientVersion.c_str(), pinfo->ClientVersion, sizeof(pinfo->ClientVersion)))
	{
		TPacketGCLoginFailure failurePacket;

		failurePacket.header = HEADER_GC_LOGIN_FAILURE;
		strlcpy(failurePacket.szStatus, "WRONGVER", sizeof(failurePacket.szStatus));

		d->Packet(&failurePacket, sizeof(failurePacket));
		return;
	}
#endif

	DWORD dwKey = DESC_MANAGER::instance().CreateLoginKey(d);

	sys_log(0, "InputAuth::Login : key %u login %s", dwKey, login);

	TPacketCGLogin3 * p = M2_NEW TPacketCGLogin3;
	thecore_memcpy(p, pinfo, sizeof(TPacketCGLogin3));

	char szPasswd[PASSWD_MAX_LEN * 2 + 1];
	DBManager::instance().EscapeString(szPasswd, sizeof(szPasswd), passwd, strlen(passwd));

	char szLogin[LOGIN_MAX_LEN * 2 + 1];
	DBManager::instance().EscapeString(szLogin, sizeof(szLogin), login, strlen(login));

	// CHANNEL_SERVICE_LOGIN
	if (Login_IsInChannelService(szLogin))
	{
		sys_log(0, "ChannelServiceLogin [%s]", szLogin);

		DBManager::instance().ReturnQuery(QID_AUTH_LOGIN, dwKey, p,
				"SELECT '%s',password,social_id,id,status,"
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
				"language,"
#endif
				"availDt - NOW() > 0,"
				"UNIX_TIMESTAMP(silver_expire),"
				"UNIX_TIMESTAMP(gold_expire),"
				"UNIX_TIMESTAMP(safebox_expire),"
				"UNIX_TIMESTAMP(autoloot_expire),"
				"UNIX_TIMESTAMP(fish_mind_expire),"
				"UNIX_TIMESTAMP(marriage_fast_expire),"
				"UNIX_TIMESTAMP(money_drop_rate_expire),"
				"UNIX_TIMESTAMP(create_time)"
				" FROM account WHERE login='%s'",

				szPasswd, szLogin);
	}
	// END_OF_CHANNEL_SERVICE_LOGIN
	else
	{
		DBManager::instance().ReturnQuery(QID_AUTH_LOGIN, dwKey, p, 
				"SELECT PASSWORD('%s'),password,social_id,id,status,"
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
				"language,"
#endif
				"availDt - NOW() > 0,"
				"UNIX_TIMESTAMP(silver_expire),"
				"UNIX_TIMESTAMP(gold_expire),"
				"UNIX_TIMESTAMP(safebox_expire),"
				"UNIX_TIMESTAMP(autoloot_expire),"
				"UNIX_TIMESTAMP(fish_mind_expire),"
				"UNIX_TIMESTAMP(marriage_fast_expire),"
				"UNIX_TIMESTAMP(money_drop_rate_expire),"
				"UNIX_TIMESTAMP(create_time)"
				" FROM account WHERE login='%s'",
				szPasswd, szLogin);
	}
}

extern void socket_timeout(socket_t s, long sec, long usec);

int CInputAuth::Analyze(LPDESC d, BYTE bHeader, const char * c_pData)
{
	if (!g_bAuthServer)
	{
		sys_err ("CInputAuth class is not for game server. IP %s might be a hacker.",
			inet_ntoa(d->GetAddr().sin_addr));
		d->DelayedDisconnect(5);
		return 0;
	}

	int iExtraLen = 0;

	if (test_server)
		sys_log(0, " InputAuth Analyze Header[%d] ", bHeader);

	switch (bHeader)
	{
		case HEADER_CG_PONG:
			Pong(d);
			break;

		case HEADER_CG_LOGIN3:
			Login(d, c_pData);
			break;

		case HEADER_CG_HANDSHAKE:
			break;

		default:
			sys_err("This phase does not handle this header %d (0x%x)(phase: AUTH)", bHeader, bHeader);
			break;
	}

	return iExtraLen;
}
