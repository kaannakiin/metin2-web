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
		time_t	tLastFailure;
		int		iLocks;
	};

	const int LOGIN_FAILURE_LIMIT_PER_ACCOUNT_SOURCE = 5;
	const int LOGIN_FAILURE_LIMIT_PER_HOST = 20;
	const int LOGIN_FAILURE_LIMIT_PER_ACCOUNT = 30;
	const time_t LOGIN_FAILURE_WINDOW = 300;
	const time_t LOGIN_FAILURE_BACKOFF_RESET = 3600;
	const int LOGIN_FAILURE_MAX_BACKOFF_STEPS = 4;
	const size_t LOGIN_FAILURE_MAX_ENTRIES = 10000;

	std::unordered_map<std::string, SLoginFailures> s_mapLoginFailures;

	std::string AccountKey(const char* c_szLogin)
	{
		char szLogin[LOGIN_MAX_LEN + 1];
		trim_and_lower(c_szLogin, szLogin, sizeof(szLogin));
		return std::string("a:") + szLogin;
	}

	std::string AccountSourceKey(LPDESC d, const char* c_szLogin)
	{
		return AccountKey(c_szLogin) + "@" + d->GetHostName();
	}

	std::string HostKey(LPDESC d)
	{
		return std::string("h:") + d->GetHostName();
	}

	bool IsLocked(const std::string& stKey)
	{
		auto it = s_mapLoginFailures.find(stKey);
		return it != s_mapLoginFailures.end() && it->second.tLockedUntil > get_global_time();
	}

	bool FailedRecently(const std::string& stKey)
	{
		auto it = s_mapLoginFailures.find(stKey);
		return it != s_mapLoginFailures.end() && it->second.tLastFailure + LOGIN_FAILURE_WINDOW > get_global_time();
	}

	void EvictStale(time_t tNow)
	{
		for (auto it = s_mapLoginFailures.begin(); it != s_mapLoginFailures.end();)
		{
			if (it->second.tWindowEnd <= tNow && it->second.tLockedUntil + LOGIN_FAILURE_BACKOFF_RESET <= tNow
				&& it->second.tLastFailure + LOGIN_FAILURE_WINDOW <= tNow)
				it = s_mapLoginFailures.erase(it);
			else
				++it;
		}
	}

	void AddFailure(const std::string& stKey, int iLimit, bool bBackoff)
	{
		const time_t tNow = get_global_time();

		if (s_mapLoginFailures.size() >= LOGIN_FAILURE_MAX_ENTRIES)
			EvictStale(tNow);

		SLoginFailures& r = s_mapLoginFailures[stKey];
		r.tLastFailure = tNow;

		if (r.tWindowEnd <= tNow)
		{
			r.iCount = 0;
			r.tWindowEnd = tNow + LOGIN_FAILURE_WINDOW;
		}

		if (r.tLockedUntil + LOGIN_FAILURE_BACKOFF_RESET <= tNow)
			r.iLocks = 0;

		if (++r.iCount < iLimit)
			return;

		r.iCount = 0;
		if (bBackoff)
		{
			r.iLocks = MIN(r.iLocks + 1, LOGIN_FAILURE_MAX_BACKOFF_STEPS);
			r.tLockedUntil = tNow + LOGIN_FAILURE_WINDOW * (1 << (r.iLocks - 1));
		}
		else
			r.tLockedUntil = tNow + LOGIN_FAILURE_WINDOW;
	}
}

bool IsLoginThrottled(LPDESC d, const char* c_szLogin)
{
	const std::string stSource = AccountSourceKey(d, c_szLogin);
	const bool bProxied = IsTrustedProxyIP(d->GetHostName());

	if (IsLocked(stSource))
		return true;

	if (!bProxied && IsLocked(HostKey(d)))
		return true;

	// The account-wide lock only stops sources that already failed: the owner,
	// coming from a clean address, can always log in, while a distributed
	// attack gets one try per new address until the lock expires.
	if (IsLocked(AccountKey(c_szLogin)))
		return FailedRecently(stSource) || (!bProxied && FailedRecently(HostKey(d)));

	return false;
}

void OnLoginFailed(LPDESC d, const char* c_szLogin)
{
	AddFailure(AccountSourceKey(d, c_szLogin), LOGIN_FAILURE_LIMIT_PER_ACCOUNT_SOURCE, true);
	AddFailure(AccountKey(c_szLogin), LOGIN_FAILURE_LIMIT_PER_ACCOUNT, false);

	if (!IsTrustedProxyIP(d->GetHostName()))
		AddFailure(HostKey(d), LOGIN_FAILURE_LIMIT_PER_HOST, true);
}

void OnLoginSucceeded(LPDESC d, const char* c_szLogin)
{
	s_mapLoginFailures.erase(AccountSourceKey(d, c_szLogin));
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
