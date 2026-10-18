#include "StdAfx.h"

#include "../eterBase/Error.h"
#include "../eterlib/Camera.h"
#include "../eterlib/AttributeInstance.h"
#include "../gamelib/AreaTerrain.h"
#include "../EterGrnLib/Material.h"
#include "../EterGrnLib/ModelInstance.h"
#include "../CWebBrowser/CWebBrowser.h"

#include "resource.h"
#include "PythonApplication.h"
#include "PythonCharacterManager.h"

#include <algorithm>

#ifdef max
#undef max
#endif
#ifdef min
#undef min
#endif

#include "ProcessScanner.h"

#ifdef ENABLE_RENEWAL_SWITCHBOT
	#include "PythonSwitchbot.h"
#endif

#ifdef ENABLE_CLIENT_PERFORMANCE
	#include "PythonPlayerSettingsModule.h"
#endif

extern void GrannyCreateSharedDeformBuffer();
extern void GrannyDestroySharedDeformBuffer();

float MIN_FOG = 2400.0f;

#ifdef FPS_APPLICATON_DEVICE_LIMITATION

#define GAME_TICK_FPS         60	// don't touch here, not fps.
#define RENDER_SKIP_BUFFER_MS 1000	// Background render wait time, recommended 1000

#if defined(RENDER_MAX_FPS) && (RENDER_MAX_FPS > 520)
#error "RENDER MAX FPS value cannot exceed 520!"
#endif

#if defined(RENDER_SKIP_BUFFER_MS) && (RENDER_SKIP_BUFFER_MS < 10)
#error "RENDER_SKIP_BUFFER_MS is too low, make it minimum 60!"
#endif

LARGE_INTEGER g_Frequency;

void InitHighPrecisionTimer()
{
	QueryPerformanceFrequency(&g_Frequency);
}

void SleepUntilNextFrame(double targetFrameTimeMs)
{
	static LARGE_INTEGER lastTime = { 0 };
	LARGE_INTEGER currentTime;
	QueryPerformanceCounter(&currentTime);

	if (lastTime.QuadPart == 0)
		lastTime = currentTime;

	double elapsedMs = (double)(currentTime.QuadPart - lastTime.QuadPart) * 1000.0 / (double)g_Frequency.QuadPart;

	if (elapsedMs < targetFrameTimeMs)
	{
		double remainingMs = targetFrameTimeMs - elapsedMs;

		if (remainingMs > 2.0)
			Sleep((DWORD)(remainingMs - 1));

		do {
			QueryPerformanceCounter(&currentTime);
			elapsedMs = (double)(currentTime.QuadPart - lastTime.QuadPart) * 1000.0 / (double)g_Frequency.QuadPart;
		} while (elapsedMs < targetFrameTimeMs);
	}

	lastTime = currentTime;
}

inline double CalculateSpecularSpeed(double fps, double boostFactor = 1.0)
{
	double baseSpeed;

	if (fps <= 120.0)
	{
		baseSpeed = -0.000008333 * fps + 0.0075;
	}
	else if (fps <= 360.0)
	{
		baseSpeed = -0.000020 * fps + 0.0089;
	}
	else if (fps <= 520.0)
	{
		baseSpeed = -0.000001875 * fps + 0.002375;
	}
	else
	{
		baseSpeed = 0.0014;
	}

	return baseSpeed * boostFactor;
}

double g_specularSpd = CalculateSpecularSpeed(RENDER_MAX_FPS);

#else

double g_specularSpd = 0.007f;

#endif

CPythonApplication * CPythonApplication::ms_pInstance;

float c_fDefaultCameraRotateSpeed = 1.5f;
float c_fDefaultCameraPitchSpeed = 1.5f;
float c_fDefaultCameraZoomSpeed = 0.05f;

CPythonApplication::CPythonApplication()
{
	CTimer::Instance().UseCustomTime();
#ifdef FPS_APPLICATON_DEVICE_LIMITATION
	::InitHighPrecisionTimer();
#endif
	m_dwWidth = 800;
	m_dwHeight = 600;

	ms_pInstance = this;
	m_isWindowFullScreenEnable = FALSE;

	m_v3CenterPosition = D3DXVECTOR3(0.0f, 0.0f, 0.0f);
	m_dwStartLocalTime = ELTimer_GetMSec();
	m_tServerTime = 0;
	m_tLocalStartTime = 0;

	m_iPort = 0;
#ifdef FPS_APPLICATON_DEVICE_LIMITATION
	m_iFPS = RENDER_MAX_FPS;
#else
	m_iFPS = 60;
#endif

	m_isActivateWnd = false;
	m_isMinimizedWnd = true;

	m_fRotationSpeed = 0.0f;
	m_fPitchSpeed = 0.0f;
	m_fZoomSpeed = 0.0f;

	m_fFaceSpd = 0.0f;

	m_dwFaceAccCount = 0;
	m_dwFaceAccTime = 0;

	m_dwFaceSpdSum = 0;
	m_dwFaceSpdCount = 0;

	m_FlyingManager.SetMapManagerPtr(&m_pyBackground);

	m_iCursorNum = CURSOR_SHAPE_NORMAL;
	m_iContinuousCursorNum = CURSOR_SHAPE_NORMAL;

	m_isSpecialCameraMode = FALSE;
	m_fCameraRotateSpeed = c_fDefaultCameraRotateSpeed;
	m_fCameraPitchSpeed = c_fDefaultCameraPitchSpeed;
	m_fCameraZoomSpeed = c_fDefaultCameraZoomSpeed;

	m_iCameraMode = CAMERA_MODE_NORMAL;
	m_fBlendCameraStartTime = 0.0f;
	m_fBlendCameraBlendTime = 0.0f;

	m_iForceSightRange = -1;

	CCameraManager::Instance().AddCamera(EVENT_CAMERA_NUMBER);
}

CPythonApplication::~CPythonApplication()
{
}

void CPythonApplication::GetMousePosition(POINT* ppt)
{
	CMSApplication::GetMousePosition(ppt);
}

void CPythonApplication::SetMinFog(float fMinFog)
{
	MIN_FOG = fMinFog;
}

void CPythonApplication::SetFrameSkip(bool isEnable)
{
	if (isEnable)
		m_isFrameSkipDisable=false;
	else
		m_isFrameSkipDisable=true;
}

void CPythonApplication::NotifyHack(const char *c_szFormat, ...)
{
	char szBuf[1024];

	va_list args;
	va_start(args, c_szFormat);	
	_vsnprintf(szBuf, sizeof(szBuf), c_szFormat, args);
	va_end(args);
	m_pyNetworkStream.NotifyHack(szBuf);
}

void CPythonApplication::GetInfo(UINT eInfo, std::string* pstInfo)
{
	switch (eInfo)
	{
	case INFO_ACTOR:
		m_kChrMgr.GetInfo(pstInfo);
		break;
	case INFO_EFFECT:
		m_kEftMgr.GetInfo(pstInfo);
		break;
	case INFO_ITEM:
		m_pyItem.GetInfo(pstInfo);
		break;
	case INFO_TEXTTAIL:
		m_pyTextTail.GetInfo(pstInfo);
		break;
	}
}

#ifdef ENABLE_ABORT_TRACEBACK_WITH_LINE
void CPythonApplication::Abort()
{
    TraceError("============================================================================================================");
    TraceError("Abort!!!!\n\n");

#ifdef __EMSCRIPTEN__
    PyFrameObject* frame = PyEval_GetFrame();
    Py_XINCREF(frame);
    while (frame)
    {
        {
            const CM2wPythonFrame kFrame(frame);
            TraceError("filename=%s, name=%s, line=%d", kFrame.FileName(), kFrame.FunctionName(), kFrame.LineNumber());
        }
        PyFrameObject* back = PyFrame_GetBack(frame);
        Py_DECREF(frame);
        frame = back;
#else
    PyThreadState* tstate = PyThreadState_GET();
    if (tstate)
    {
        for (PyFrameObject* frame = tstate->frame; frame; frame = frame->f_back)
        {
            PyCodeObject* f_code = frame->f_code;
            if (!f_code || !f_code->co_filename || !f_code->co_name)
                continue;

            const char* filename = PyString_AsString(f_code->co_filename);
            const char* funcname = PyString_AsString(f_code->co_name);
            int line = PyFrame_GetLineNumber(frame);
            TraceError("filename=%s, name=%s, line=%d", filename, funcname, line);
        }
#endif
    }

    PostQuitMessage(0);
}
#else
void CPythonApplication::Abort()
{
	TraceError("============================================================================================================");
	TraceError("Abort!!!!\n\n");

	PostQuitMessage(0);
}
#endif

void CPythonApplication::Exit()
{
	PostQuitMessage(0);
}

void CPythonApplication::RenderGame()
{
#ifdef ENABLE_RENDER_TARGET
	m_kRenderTargetManager.RenderBackgrounds();
#endif
	float fAspect = m_kWndMgr.GetAspect();
	float fFarClip = m_pyBackground.GetFarClip();

#ifdef ENABLE_FOV_OPTION
	m_pyGraphic.SetPerspective(CPythonSystem::Instance().GetFOV(), fAspect, 100.0, fFarClip);
#else
	m_pyGraphic.SetPerspective(30.0f, fAspect, 100.0, fFarClip);
#endif

	CCullingManager::Instance().Process();

	m_kChrMgr.Deform();
	m_kEftMgr.Update();
#ifdef ENABLE_RENDER_TARGET
	m_kRenderTargetManager.DeformModels();
#endif

	m_pyBackground.RenderCharacterShadowToTexture();

	m_pyGraphic.SetGameRenderState();
	m_pyGraphic.PushState();

	{
		long lx, ly;
		m_kWndMgr.GetMousePosition(lx, ly);
		m_pyGraphic.SetCursorPosition(lx, ly);
	}

	m_pyBackground.RenderSky();

	m_pyBackground.RenderBeforeLensFlare();

	m_pyBackground.RenderCloud();

	m_pyBackground.BeginEnvironment();
	m_pyBackground.Render();

	m_pyBackground.SetCharacterDirLight();
	m_kChrMgr.Render();
#ifdef ENABLE_RENDER_TARGET
	m_kRenderTargetManager.RenderModels();
#endif

	m_pyBackground.SetBackgroundDirLight();
	m_pyBackground.RenderWater();
	m_pyBackground.RenderSnow();
	m_pyBackground.RenderEffect();
	m_pyBackground.EndEnvironment();

	m_kEftMgr.Render();
	m_pyItem.Render();
	m_FlyingManager.Render();

	m_pyBackground.BeginEnvironment();
	m_pyBackground.RenderPCBlocker();
	m_pyBackground.EndEnvironment();

	m_pyBackground.RenderAfterLensFlare();
}

void CPythonApplication::UpdateGame()
{
	uint32_t t1 = ELTimer_GetMSec();
	POINT ptMouse;
	GetMousePosition(&ptMouse);

	CGraphicTextInstance::Hyperlink_UpdateMousePos(ptMouse.x, ptMouse.y);

	uint32_t t2 = ELTimer_GetMSec();

	{
		CScreen s;
		float fAspect = UI::CWindowManager::Instance().GetAspect();
		float fFarClip = CPythonBackground::Instance().GetFarClip();

#ifdef ENABLE_FOV_OPTION
		s.SetPerspective(CPythonSystem::Instance().GetFOV(), fAspect, 100.0f, fFarClip);
#else
		s.SetPerspective(30.0f,fAspect, 100.0f, fFarClip);
#endif

		s.BuildViewFrustum();
	}

#ifdef ENABLE_RENDER_TARGET
	m_kRenderTargetManager.UpdateModels();
#endif

	uint32_t t3 = ELTimer_GetMSec();
	TPixelPosition kPPosMainActor;
	m_pyPlayer.NEW_GetMainActorPosition(&kPPosMainActor);

	uint32_t t4 = ELTimer_GetMSec();
	m_pyBackground.Update(kPPosMainActor.x, kPPosMainActor.y, kPPosMainActor.z);

	uint32_t t5 = ELTimer_GetMSec();
	m_GameEventManager.SetCenterPosition(kPPosMainActor.x, kPPosMainActor.y, kPPosMainActor.z);
	m_GameEventManager.Update();

	uint32_t t6 = ELTimer_GetMSec();
	m_kChrMgr.Update();
	uint32_t t7 = ELTimer_GetMSec();
	m_kEftMgr.UpdateSound();

	uint32_t t8 = ELTimer_GetMSec();
	m_FlyingManager.Update();
	uint32_t t9 = ELTimer_GetMSec();
	m_pyItem.Update(ptMouse);
	uint32_t t10 = ELTimer_GetMSec();
	m_pyPlayer.Update();
	uint32_t t11 = ELTimer_GetMSec();

	m_pyPlayer.NEW_GetMainActorPosition(&kPPosMainActor);
	SetCenterPosition(kPPosMainActor.x, kPPosMainActor.y, kPPosMainActor.z);
	uint32_t t12 = ELTimer_GetMSec();
}

void CPythonApplication::SkipRenderBuffering(DWORD dwSleepMSec)
{
	m_dwBufSleepSkipTime=ELTimer_GetMSec()+dwSleepMSec;
}

bool CPythonApplication::IsMinimizedWnd()
{
	return m_isMinimizedWnd;
}

bool CPythonApplication::Process()
{
#ifdef FPS_APPLICATON_DEVICE_LIMITATION
	const double fTargetFrameMsec = 1000.0 / static_cast<double>(RENDER_MAX_FPS);

#if defined(CHECK_LATEST_DATA_FILES)
	if (CheckLatestFiles_PollEvent())
		return false;
#endif

	ELTimer_SetFrameMSec();
	DWORD dwStart = ELTimer_GetMSec();

	static DWORD s_dwUpdateFrameCount = 0;
	static DWORD s_dwRenderFrameCount = 0;
	static DWORD s_dwFaceCount = 0;
	static UINT s_uiLoad = 0;
	static DWORD s_dwCheckTime = ELTimer_GetMSec();

	if (ELTimer_GetMSec() - s_dwCheckTime > 1000)
	{
		m_dwUpdateFPS = s_dwUpdateFrameCount;
		m_dwRenderFPS = s_dwRenderFrameCount;
		m_dwLoad = s_uiLoad;
		m_dwFaceCount = s_dwFaceCount / std::max(static_cast<DWORD>(1), s_dwRenderFrameCount);

		s_dwCheckTime = ELTimer_GetMSec();
		s_uiLoad = s_dwFaceCount = s_dwUpdateFrameCount = s_dwRenderFrameCount = 0;

#if defined(EVENT_HANDLER_MASTER)
		EventHandler::Instance().Proccess();
#endif
	}

	static DWORD s_lastLogicTick = ELTimer_GetMSec();
	static double s_logicAccumMs = 0.0;
	const double LOGIC_DT_MS = 1000.0 / static_cast<double>(GAME_TICK_FPS);

	DWORD currentTimeMs = ELTimer_GetMSec();
	DWORD dtMs = currentTimeMs - s_lastLogicTick;
	s_lastLogicTick = currentTimeMs;
	s_logicAccumMs += static_cast<double>(dtMs);

	int maxLogicStepsPerFrame = 1;
	if (m_dwRenderFPS < 80)
		maxLogicStepsPerFrame = 2;
	if (m_dwRenderFPS < 50)
		maxLogicStepsPerFrame = 4;
	if (m_dwRenderFPS < 30)
		maxLogicStepsPerFrame = 8;

	int logicSteps = 0;
	while (s_logicAccumMs >= LOGIC_DT_MS && logicSteps < maxLogicStepsPerFrame)
	{
		CTimer& rkTimer = CTimer::Instance();
		rkTimer.Advance();

		m_fGlobalTime = rkTimer.GetCurrentSecond();
		m_fGlobalElapsedTime = rkTimer.GetElapsedSecond();

		m_pyNetworkStream.Process();
		m_kGuildMarkUploader.Process();
		m_kGuildMarkDownloader.Process();
		m_kAccountConnector.Process();

		UpdateKeyboard();

		POINT Point;
		if (GetCursorPos(&Point))
		{
			ScreenToClient(m_hWnd, &Point);
			OnMouseMove(Point.x, Point.y);
		}

		__UpdateCamera();
		CRenderTargetManager::Instance().UpdateModels();
		CResourceManager::Instance().Update();
		OnCameraUpdate();
		OnMouseUpdate();
		OnUIUpdate();

		++s_dwUpdateFrameCount;

		s_logicAccumMs -= LOGIC_DT_MS;
		++logicSteps;
	}

	int maxBacklogTicks = 2;
	if (m_dwRenderFPS < 50)
		maxBacklogTicks = 4;
	if (m_dwRenderFPS < 30)
		maxBacklogTicks = 8;

	if (s_logicAccumMs > LOGIC_DT_MS * maxBacklogTicks)
		s_logicAccumMs = LOGIC_DT_MS * maxBacklogTicks;

	m_dwCurUpdateTime = ELTimer_GetMSec() - dwStart;

	bool canRender = true;
	if (m_isMinimizedWnd)
	{
		canRender = false;
		CEffectManager::Instance().Update();
	}
	else
	{
#ifdef ENABLE_FIX_MOBS_LAG
		if (DEVICE_STATE_OK != CheckDeviceState())
		{
			canRender = false;

			CPythonBackground& rkBG = CPythonBackground::Instance();
			CRenderTargetManager::Instance().ReleaseRenderTargetTextures();

			if (m_pyGraphic.RestoreDevice())
			{
				CRenderTargetManager::Instance().CreateRenderTargetTextures();
				rkBG.CreateCharacterShadowTexture();
			}
			else
			{
				canRender = false;
			}
		}
#else
		if (m_pyGraphic.IsLostDevice())
		{
			CPythonBackground& rkBG = CPythonBackground::Instance();
			rkBG.ReleaseCharacterShadowTexture();
			CRenderTargetManager::Instance().ReleaseRenderTargetTextures();

			if (m_pyGraphic.RestoreDevice())
			{
				CRenderTargetManager::Instance().CreateRenderTargetTextures();
				rkBG.CreateCharacterShadowTexture();
			}
			else
			{
				canRender = false;
			}
		}
#endif
	}

	if (!IsActive())
		SkipRenderBuffering(RENDER_SKIP_BUFFER_MS);

	if (!canRender)
	{
		SkipRenderBuffering(RENDER_SKIP_BUFFER_MS);
	}
	else
	{
		DWORD dwRenderStartTime = ELTimer_GetMSec();
		CCullingManager::Instance().Update();
		if (m_pyGraphic.Begin())
		{
			m_pyGraphic.ClearDepthBuffer();

#ifdef _DEBUG
			m_pyGraphic.SetClearColor(0.3f, 0.3f, 0.3f);
			m_pyGraphic.Clear();
#endif
			CGrannyMaterial::TranslateSpecularMatrix(g_specularSpd, g_specularSpd, 0.0f);

			m_pyGraphic.SetInterfaceRenderState();
			OnUIRender();
			OnMouseRender();

			m_pyGraphic.End();
			m_pyGraphic.Show();

			DWORD dwRenderEndTime = ELTimer_GetMSec();

			static DWORD s_dwRenderCheckTime = dwRenderEndTime;
			static DWORD s_dwRenderRangeTime = 0;
			static DWORD s_dwRenderRangeFrame = 0;

			m_dwCurRenderTime = dwRenderEndTime - dwRenderStartTime;
			s_dwRenderRangeTime += m_dwCurRenderTime;
			++s_dwRenderRangeFrame;

			if (dwRenderEndTime - s_dwRenderCheckTime > 1000)
			{
				m_fAveRenderTime = float(double(s_dwRenderRangeTime) / double(s_dwRenderRangeFrame));

				s_dwRenderCheckTime = ELTimer_GetMSec();
				s_dwRenderRangeTime = 0;
				s_dwRenderRangeFrame = 0;
			}

			DWORD dwCurFaceCount = m_pyGraphic.GetFaceCount();
			m_pyGraphic.ResetFaceCount();
			s_dwFaceCount += dwCurFaceCount;

			if (dwCurFaceCount > 5000)
			{
				if (dwRenderEndTime > m_dwBufSleepSkipTime)
				{
					static float s_fBufRenderTime = 0.0f;

					float fCurRenderTime = m_dwCurRenderTime;

					if (fCurRenderTime > s_fBufRenderTime)
					{
						float fRatio = fMAX(0.5f, (fCurRenderTime - s_fBufRenderTime) / 30.0f);
						s_fBufRenderTime = (s_fBufRenderTime * (100.0f - fRatio) + (fCurRenderTime + 5) * fRatio) / 100.0f;
					}
					else
					{
						float fRatio = 0.5f;
						s_fBufRenderTime = (s_fBufRenderTime * (100.0f - fRatio) + fCurRenderTime * fRatio) / 100.0f;
					}

					if (s_fBufRenderTime > 100.0f)
						s_fBufRenderTime = 100.0f;

					DWORD dwBufRenderTime = s_fBufRenderTime;

					if (m_isWindowed)
					{
						if (dwBufRenderTime > 58)
							dwBufRenderTime = 64;
						else if (dwBufRenderTime > 42)
							dwBufRenderTime = 48;
						else if (dwBufRenderTime > 26)
							dwBufRenderTime = 32;
						else if (dwBufRenderTime > 10)
							dwBufRenderTime = 16;
						else
							dwBufRenderTime = 8;
					}

					m_fAveRenderTime = s_fBufRenderTime;
				}

				m_dwFaceAccCount += dwCurFaceCount;
				m_dwFaceAccTime += m_dwCurRenderTime;

				m_fFaceSpd = m_dwFaceAccTime ? (m_dwFaceAccCount / m_dwFaceAccTime) : 0;

				if (-1 == m_iForceSightRange)
				{
					static float s_fAveRenderTime = 16.0f;
					float fRatio = 0.3f;
					s_fAveRenderTime = (s_fAveRenderTime * (100.0f - fRatio) + std::max<float>(16.0f, m_dwCurRenderTime) * fRatio) / 100.0f;

					float fFar = 25600.0f;
					float fNear = MIN_FOG;
					double dbAvePow = double(1000.0f / s_fAveRenderTime);
					double dbMaxPow = 60.0;
					float fDistance = std::max<float>(fNear + (fFar - fNear) * (dbAvePow) / dbMaxPow, fNear);
					m_pyBackground.SetViewDistanceSet(0, fDistance);
				}
				else
				{
					m_pyBackground.SetViewDistanceSet(0, float(m_iForceSightRange));
				}
			}
			else
			{
				m_pyBackground.SetViewDistanceSet(0, 25600.0f);
			}

			++s_dwRenderFrameCount;
		}
	}

	s_uiLoad += ELTimer_GetMSec() - dwStart;

	::SleepUntilNextFrame(fTargetFrameMsec);

	return true;
#else
	ELTimer_SetFrameMSec();

	DWORD dwStart = ELTimer_GetMSec();

	///////////////////////////////////////////////////////////////////////////////////////////////////
	static DWORD	s_dwUpdateFrameCount = 0;
	static DWORD	s_dwRenderFrameCount = 0;
	static DWORD	s_dwFaceCount = 0;
	static UINT		s_uiLoad = 0;
	static DWORD	s_dwCheckTime = ELTimer_GetMSec();

	if (ELTimer_GetMSec() - s_dwCheckTime > 1000)
	{
		m_dwUpdateFPS = s_dwUpdateFrameCount;
		m_dwRenderFPS = s_dwRenderFrameCount;
		m_dwLoad = s_uiLoad;

		m_dwFaceCount = s_dwFaceCount / std::max(static_cast<DWORD>(1), s_dwRenderFrameCount);

		s_dwCheckTime = ELTimer_GetMSec();

		s_uiLoad = s_dwFaceCount = s_dwUpdateFrameCount = s_dwRenderFrameCount = 0;
	}

	// Update Time
	static BOOL s_bFrameSkip = false;
	static UINT s_uiNextFrameTime = ELTimer_GetMSec();

	CTimer & rkTimer = CTimer::Instance();
	rkTimer.Advance();

	m_fGlobalTime = rkTimer.GetCurrentSecond();
	m_fGlobalElapsedTime = rkTimer.GetElapsedSecond();

	UINT uiFrameTime = rkTimer.GetElapsedMilliecond();
	s_uiNextFrameTime += uiFrameTime;

	DWORD updatestart = ELTimer_GetMSec();
	// Network I/O
	m_pyNetworkStream.Process();

	m_kGuildMarkUploader.Process();

	m_kGuildMarkDownloader.Process();
	m_kAccountConnector.Process();
#if defined(__EMSCRIPTEN__) && defined(ENABLE_CLIENT_PERFORMANCE)
	CPythonPlayerSettingsModule::Instance().ProcessDeferredCache();
#endif

	//////////////////////
	// Input Process
	// Keyboard
	UpdateKeyboard();
	// Mouse
	POINT Point;
	if (GetCursorPos(&Point))
	{
		ScreenToClient(m_hWnd, &Point);
		OnMouseMove(Point.x, Point.y);
	}
	//////////////////////
	__UpdateCamera();
	// Update Game Playing
	CResourceManager::Instance().Update();
	OnCameraUpdate();
	OnMouseUpdate();
	OnUIUpdate();

	//Update
	m_dwCurUpdateTime = ELTimer_GetMSec() - updatestart;

	DWORD dwCurrentTime = ELTimer_GetMSec();
	BOOL  bCurrentLateUpdate = FALSE;

	s_bFrameSkip = false;

	if (dwCurrentTime > s_uiNextFrameTime)
	{
		int dt = dwCurrentTime - s_uiNextFrameTime;
		int nAdjustTime = (static_cast<float>(dt) / static_cast<float>(uiFrameTime)) * uiFrameTime;

		if (dt >= 500)
		{
			s_uiNextFrameTime += nAdjustTime;
			printf("FrameSkip Adjusting... %d\n", nAdjustTime);
			CTimer::Instance().Adjust(nAdjustTime);
		}

		if (!m_isFrameSkipDisable)
			s_bFrameSkip = true;

		bCurrentLateUpdate = TRUE;
	}

	if (m_isMinimizedWnd)
		CEffectManager::Instance().Update();

	if (m_isFrameSkipDisable && !m_isMinimizedWnd)
		s_bFrameSkip = false;

	if (!s_bFrameSkip)
	{
		CGrannyMaterial::TranslateSpecularMatrix(g_specularSpd, g_specularSpd, 0.0f);

		DWORD dwRenderStartTime = ELTimer_GetMSec();

		bool canRender = true;

		if (m_isMinimizedWnd)
		{
			canRender = false;
		}
		else
		{
#ifdef ENABLE_FIX_MOBS_LAG
			if (DEVICE_STATE_OK != CheckDeviceState())
			{
				canRender = false;

				CPythonBackground& rkBG = CPythonBackground::Instance();
#ifdef ENABLE_RENDER_TARGET
				CRenderTargetManager::Instance().ReleaseRenderTargetTextures();
#endif

				if (m_pyGraphic.RestoreDevice())
				{
#ifdef ENABLE_RENDER_TARGET
					CRenderTargetManager::Instance().CreateRenderTargetTextures();
#endif
					rkBG.CreateCharacterShadowTexture();
				}
				else
				{
					canRender = false;
				}
			}
#else
			if (m_pyGraphic.IsLostDevice())
			{
				CPythonBackground &rkBG = CPythonBackground::Instance();
				rkBG.ReleaseCharacterShadowTexture();
#ifdef ENABLE_RENDER_TARGET
				CRenderTargetManager::Instance().ReleaseRenderTargetTextures();
#endif

				if (m_pyGraphic.RestoreDevice())
				{
#ifdef ENABLE_RENDER_TARGET
					CRenderTargetManager::Instance().CreateRenderTargetTextures();
#endif
					rkBG.CreateCharacterShadowTexture();
				}
				else
				{
					canRender = false;
				}
			}
#endif
		}

		if (!IsActive())
		{
			SkipRenderBuffering(3000);
		}

		if (!canRender)
		{
			SkipRenderBuffering(3000);
		}
		else
		{
			// RestoreLostDevice
			CCullingManager::Instance().Update();
			if (m_pyGraphic.Begin())
			{
				m_pyGraphic.ClearDepthBuffer();

#ifdef _DEBUG
				m_pyGraphic.SetClearColor(0.3f, 0.3f, 0.3f);
				m_pyGraphic.Clear();
#endif

				/////////////////////
				// Interface
				m_pyGraphic.SetInterfaceRenderState();

				OnUIRender();
				OnMouseRender();
				/////////////////////

				m_pyGraphic.End();

				m_pyGraphic.Show();

				DWORD dwRenderEndTime = ELTimer_GetMSec();

				static DWORD s_dwRenderCheckTime = dwRenderEndTime;
				static DWORD s_dwRenderRangeTime = 0;
				static DWORD s_dwRenderRangeFrame = 0;

				m_dwCurRenderTime = dwRenderEndTime - dwRenderStartTime;
				s_dwRenderRangeTime += m_dwCurRenderTime;
				++s_dwRenderRangeFrame;

				if (dwRenderEndTime - s_dwRenderCheckTime > 1000)
				{
					m_fAveRenderTime = float(double(s_dwRenderRangeTime) / double(s_dwRenderRangeFrame));

					s_dwRenderCheckTime = ELTimer_GetMSec();
					s_dwRenderRangeTime = 0;
					s_dwRenderRangeFrame = 0;
				}

				DWORD dwCurFaceCount=m_pyGraphic.GetFaceCount();
				m_pyGraphic.ResetFaceCount();
				s_dwFaceCount += dwCurFaceCount;

				if (dwCurFaceCount > 5000)
				{
					if (dwRenderEndTime > m_dwBufSleepSkipTime)
					{
						static float s_fBufRenderTime = 0.0f;

						float fCurRenderTime = m_dwCurRenderTime;

						if (fCurRenderTime > s_fBufRenderTime)
						{
							float fRatio = fMAX(0.5f, (fCurRenderTime - s_fBufRenderTime) / 30.0f);
							s_fBufRenderTime = (s_fBufRenderTime * (100.0f - fRatio) + (fCurRenderTime + 5) * fRatio) / 100.0f;
						}
						else
						{
							float fRatio = 0.5f;
							s_fBufRenderTime = (s_fBufRenderTime * (100.0f - fRatio) + fCurRenderTime * fRatio) / 100.0f;
						}

						if (s_fBufRenderTime > 100.0f)
							s_fBufRenderTime = 100.0f;

						DWORD dwBufRenderTime = s_fBufRenderTime;

						if (m_isWindowed)
						{
							if (dwBufRenderTime > 58)
								dwBufRenderTime = 64;
							else if (dwBufRenderTime > 42)
								dwBufRenderTime = 48;
							else if (dwBufRenderTime > 26)
								dwBufRenderTime = 32;
							else if (dwBufRenderTime > 10)
								dwBufRenderTime = 16;
							else
								dwBufRenderTime = 8;
						}

						m_fAveRenderTime = s_fBufRenderTime;
					}

					m_dwFaceAccCount += dwCurFaceCount;
					m_dwFaceAccTime += m_dwCurRenderTime;

					m_fFaceSpd = m_dwFaceAccTime ? (m_dwFaceAccCount / m_dwFaceAccTime) : 0;

					if (-1 == m_iForceSightRange)
					{
						static float s_fAveRenderTime = 16.0f;
						float fRatio = 0.3f;
						s_fAveRenderTime =
							(s_fAveRenderTime * (100.0f - fRatio) + std::max<float>(16.0f, m_dwCurRenderTime) * fRatio) / 100.0f;


						float fFar = 25600.0f;
						float fNear = MIN_FOG;
						double dbAvePow = double(1000.0f / s_fAveRenderTime);
						double dbMaxPow = 60.0;
						float fDistance = std::max<float>(fNear + (fFar - fNear) * (dbAvePow) / dbMaxPow, fNear);
						m_pyBackground.SetViewDistanceSet(0, fDistance);
					}
					// °Å¸® °­Á¦ ¼³Á¤½Ã
					else
					{
						m_pyBackground.SetViewDistanceSet(0, float(m_iForceSightRange));
					}
				}
				else
				{
					// 10000 Æú¸®°ï º¸´Ù ÀûÀ»¶§´Â °¡Àå ¸Ö¸® º¸ÀÌ°Ô ÇÑ´Ù
					m_pyBackground.SetViewDistanceSet(0, 25600.0f);
				}

				++s_dwRenderFrameCount;
			}
		}
	}

	int rest = s_uiNextFrameTime - ELTimer_GetMSec();

	if (rest > 0 && !bCurrentLateUpdate )
	{
		s_uiLoad -= rest;	// ½® ½Ã°£Àº ·Îµå¿¡¼­ »«´Ù..
		Sleep(rest);
	}

	++s_dwUpdateFrameCount;

	s_uiLoad += ELTimer_GetMSec() - dwStart;
	return true;
#endif
}

void CPythonApplication::UpdateClientRect()
{
	RECT rcApp;
	GetClientRect(&rcApp);
	OnSizeChange(rcApp.right - rcApp.left, rcApp.bottom - rcApp.top);
}

void CPythonApplication::SetMouseHandler(PyObject* poMouseHandler)
{
	m_poMouseHandler = poMouseHandler;
}

int CPythonApplication::CheckDeviceState()
{
	CGraphicDevice::EDeviceState e_deviceState = m_grpDevice.GetDeviceState();

	switch (e_deviceState)
	{
	case CGraphicDevice::DEVICESTATE_NULL:
		return DEVICE_STATE_FALSE;

	case CGraphicDevice::DEVICESTATE_BROKEN:
		return DEVICE_STATE_SKIP;

#ifdef ENABLE_FIX_MOBS_LAG
	case CGraphicDevice::DEVICESTATE_NEEDS_RESET:
		m_pyBackground.ReleaseCharacterShadowTexture();

#ifdef ENABLE_RENDER_TARGET
		CRenderTargetManager::Instance().ReleaseRenderTargetTextures();
#endif

		Trace("DEVICESTATE_NEEDS_RESET - attempting");
		if (!m_grpDevice.Reset())
		{
			return DEVICE_STATE_SKIP;
		}

		m_pyBackground.CreateCharacterShadowTexture();

#ifdef ENABLE_RENDER_TARGET
		CRenderTargetManager::Instance().CreateRenderTargetTextures();
#endif

		break;

	case CGraphicDevice::DEVICESTATE_OK: break;
	default:;
#else
	case CGraphicDevice::DEVICESTATE_NEEDS_RESET:
		if (!m_grpDevice.Reset())
			return DEVICE_STATE_SKIP;

		break;
#endif
	}

	return DEVICE_STATE_OK;
}

#ifdef ENABLE_MORE_FPS
std::tuple<int, int> GetTimer(int frequency)
{
	if (frequency < 60)
		return { 32, 1 };
	else if (frequency < 90)
		return { 16, 1 };
	else if (frequency < 120)
		return { 11, 0 };
	else if (frequency < 150)
		return { 8, 1 };
	else if (frequency < 180)
		return { 6, 1 };
	else if (frequency < 220)
		return { 5, 1 };
	else if (frequency < 240)
		return { 4, 1 };
	else if (frequency < 300)
		return { 3, 1 };
	else if (frequency < 360)
		return { 2, 1 };
	else if (frequency >= 360)
		return { 1, 1 };

	return  { 16, 1 };
}
#endif

bool CPythonApplication::CreateDevice(int width, int height, int Windowed, int bit /* = 32*/, int frequency /* = 0*/)
{
	int iRet;

	m_grpDevice.InitBackBufferCount(2);

#ifdef ENABLE_MORE_FPS
	g_fGameFPS = static_cast<float>(frequency);

	const auto diff = 0.42f;
	g_specularSpd = (diff / frequency);

	auto [first, sec] = GetTimer(frequency);
	CTimer::Instance().SetUpdateTime(frequency, first, sec);
	//TraceError("Device - Frequency %d g_fGameFPS %.3f (first %d sec %d) val %d specular %.3f", frequency, g_fGameFPS, first, sec, value, g_specularSpd);
#endif

	iRet = m_grpDevice.Create(GetWindowHandle(), width, height, Windowed ? true : false, bit,frequency);

	switch (iRet)
	{
	case CGraphicDevice::CREATE_OK:
		return true;

	case CGraphicDevice::CREATE_REFRESHRATE:
		return true;

	case CGraphicDevice::CREATE_ENUM:
	case CGraphicDevice::CREATE_DETECT:
		SET_EXCEPTION(CREATE_NO_APPROPRIATE_DEVICE);
		TraceError("CreateDevice: Enum & Detect failed");
		return false;

	case CGraphicDevice::CREATE_NO_DIRECTX:
		//PyErr_SetString(PyExc_RuntimeError, "DirectX 8.1 or greater required to run game");
		SET_EXCEPTION(CREATE_NO_DIRECTX);
		TraceError("CreateDevice: DirectX 8.1 or greater required to run game");
		return false;

	case CGraphicDevice::CREATE_DEVICE:
		//PyErr_SetString(PyExc_RuntimeError, "GraphicDevice create failed");
		SET_EXCEPTION(CREATE_DEVICE);
		TraceError("CreateDevice: GraphicDevice create failed");
		return false;

	case CGraphicDevice::CREATE_FORMAT:
		SET_EXCEPTION(CREATE_FORMAT);
		TraceError("CreateDevice: Change the screen format");
		return false;

	case CGraphicDevice::CREATE_GET_DEVICE_CAPS:
		PyErr_SetString(PyExc_RuntimeError, "GetDevCaps failed");
		TraceError("CreateDevice: GetDevCaps failed");
		return false;

	case CGraphicDevice::CREATE_GET_DEVICE_CAPS2:
		PyErr_SetString(PyExc_RuntimeError, "GetDevCaps2 failed");
		TraceError("CreateDevice: GetDevCaps2 failed");
		return false;

	default:
		// CREATE_OK bayraðý varsa TNL kontrolü yap
		if (iRet & CGraphicDevice::CREATE_OK)
		{
			if (iRet & CGraphicDevice::CREATE_NO_TNL)
			{
				CGrannyLODController::SetMinLODMode(true);
			}
			return true;
		}

		SET_EXCEPTION(UNKNOWN_ERROR);
		TraceError("CreateDevice: Unknown Error!");
		return false;
	}
}

void CPythonApplication::Loop()
{
	while (1)
	{
		if (IsMessage())
		{
			if (!MessageProcess())
				break;
		}
		else
		{
			if (!Process())
				break;

			m_dwLastIdleTime=ELTimer_GetMSec();
		}
	}
}

bool LoadLocaleData(const char *localePath)
{
	NANOBEGIN

	CPythonNonPlayer& rkNPCMgr = CPythonNonPlayer::Instance();
	CItemManager& rkItemMgr = CItemManager::Instance();
	CPythonSkill& rkSkillMgr = CPythonSkill::Instance();
	CPythonNetworkStream& rkNetStream = CPythonNetworkStream::Instance();

	char szItemList[256];
	char szItemProto[256];
	char szItemDesc[256];
	char szMobProto[256];
	char szSkillDescFileName[256];
	char szSkillTableFileName[256];
	char szInsultList[256];
#ifdef ENABLE_MOB_SCALE
	char szMobScale[256];
#endif
#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	char szItemScale[256]{};
#endif
#ifdef ENABLE_AURA_COSTUME_SYSTEM
	char szAuraScale[256];
#endif
#ifdef ENABLE_CLIENT_LOCALE_STRING
	char szLocaleStringList[256];
	char szLocaleMonsterChat[256];
	char szLocaleQuizList[256];
#endif
#ifdef ENABLE_CLIENT_PERFORMANCE
	char szGuildBuilding[256];
#endif
#ifdef ENABLE_GROWTH_PET_SYSTEM
	char szPetSkillFileName[256];
#endif
#ifdef ENABLE_NPC_WEAR_ITEM
	char szNPCWearItem[256];
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	const char *localePathCommon = "locale/common";
#endif

#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	snprintf(szItemList, sizeof(szItemList), "%s/item_list.txt", localePathCommon);
	snprintf(szSkillTableFileName, sizeof(szSkillTableFileName), "%s/SkillTable.txt", localePathCommon);
#else
	snprintf(szItemList, sizeof(szItemList), "%s/item_list.txt", localePath);
	snprintf(szSkillTableFileName, sizeof(szSkillTableFileName), "%s/SkillTable.txt", localePath);
#endif

#ifdef ENABLE_MOB_SCALE
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	snprintf(szMobScale, sizeof(szMobScale), "%s/mob_scale.txt", localePathCommon);
#else
	snprintf(szMobScale, sizeof(szMobScale), "%s/mob_scale.txt", localePath);
#endif
#endif

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	snprintf(szItemScale, sizeof(szItemScale), "%s/item_scale.txt", localePathCommon);
#else
	snprintf(szItemScale, sizeof(szItemScale), "%s/item_scale.txt", localePath);
#endif
#endif

#ifdef ENABLE_AURA_COSTUME_SYSTEM
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	snprintf(szAuraScale, sizeof(szAuraScale), "%s/aura_scale.txt", localePathCommon);
#else
	snprintf(szAuraScale, sizeof(szAuraScale), "%s/aura_scale.txt", localePath);
#endif
#endif

#ifdef ENABLE_CLIENT_LOCALE_STRING
	snprintf(szLocaleStringList, sizeof(szLocaleStringList), "%s/locale_string.txt", localePath);
	snprintf(szLocaleMonsterChat, sizeof(szLocaleMonsterChat), "%s/monster_chat.txt", localePath);
	snprintf(szLocaleQuizList, sizeof(szLocaleQuizList), "%s/locale_quiz.txt", localePath);
#endif

#ifdef ENABLE_CLIENT_PERFORMANCE
	snprintf(szGuildBuilding, sizeof(szGuildBuilding), "%s/guildbuildinglist.txt", localePath);
#endif

#ifdef ENABLE_GROWTH_PET_SYSTEM
	snprintf(szPetSkillFileName, sizeof(szPetSkillFileName), "%s/pet_skill.txt", localePath);
#endif

#ifdef ENABLE_NPC_WEAR_ITEM
#ifdef ENABLE_MULTI_LANGUAGE_SYSTEM
	snprintf(szNPCWearItem, sizeof(szNPCWearItem), "%s/npc_wear.txt", localePathCommon);
#else
	snprintf(szNPCWearItem, sizeof(szNPCWearItem), "%s/npc_wear.txt", localePath);
#endif
#endif

	snprintf(szItemProto, sizeof(szItemProto), "%s/item_proto", localePath);
	snprintf(szItemDesc, sizeof(szItemDesc), "%s/itemdesc.txt", localePath);
	snprintf(szMobProto, sizeof(szMobProto), "%s/mob_proto", localePath);
	snprintf(szSkillDescFileName, sizeof(szSkillDescFileName), "%s/SkillDesc.txt", localePath);
	snprintf(szInsultList, sizeof(szInsultList), "%s/insult.txt", localePath);

	rkNPCMgr.Destroy();
	rkItemMgr.Destroy();
	rkSkillMgr.Destroy();

	if (!rkItemMgr.LoadItemList(szItemList))
	{
		TraceError("LoadLocaleData - LoadItemList(%s) Error", szItemList);
	}

	if (!rkItemMgr.LoadItemTable(szItemProto))
	{
		TraceError("LoadLocaleData - LoadItemProto(%s) Error", szItemProto);
		return false;
	}

	if (!rkItemMgr.LoadItemDesc(szItemDesc))
	{
		Tracenf("LoadLocaleData - LoadItemDesc(%s) Error", szItemDesc);
	}

	if (!rkNPCMgr.LoadNonPlayerData(szMobProto))
	{
		TraceError("LoadLocaleData - LoadMobProto(%s) Error", szMobProto);
		return false;
	}

	if (!rkSkillMgr.RegisterSkillDesc(szSkillDescFileName))
	{
		TraceError("LoadLocaleData - RegisterSkillDesc(%s) Error", szMobProto);
		return false;
	}

	if (!rkSkillMgr.RegisterSkillTable(szSkillTableFileName))
	{
		TraceError("LoadLocaleData - RegisterSkillTable(%s) Error", szMobProto);
		return false;
	}

	if (!rkNetStream.LoadInsultList(szInsultList))
	{
		Tracenf("CPythonApplication - CPythonNetworkStream::LoadInsultList(%s)", szInsultList);
	}

#ifdef ENABLE_MOB_SCALE
	if (!rkNPCMgr.LoadMobScale(szMobScale))
	{
		TraceError("LoadMobScale - LoadMobScale(%s) Error", szMobScale);
	}
#endif

#ifdef ENABLE_ACCE_COSTUME_SYSTEM
	if (!rkItemMgr.LoadItemScale(szItemScale))
	{
		Tracenf("LoadLocaleData: error while loading %s.", szItemScale);
		return false;
	}
#endif

#ifdef ENABLE_AURA_COSTUME_SYSTEM
	if (!rkItemMgr.LoadAuraScale(szAuraScale))
	{
		TraceError("LoadLocaleData - LoadAuraScale(%s) Error", szAuraScale);
	}
#endif

#ifdef ENABLE_CLIENT_LOCALE_STRING
	if (!rkNetStream.LoadLocaleStringVnum(szLocaleStringList))
	{
		TraceError("LoadLocaleData - LoadLocaleStringVnum(%s) Error", szLocaleStringList);
		return false;
	}

	if (!rkNetStream.LoadLocaleChatVnum(szLocaleMonsterChat))
	{
		TraceError("LoadLocaleData - LoadLocaleChatVnum(%s) Error", szLocaleStringList);
		return false;
	}

	if (!rkNetStream.LoadLocaleQuizVnum(szLocaleQuizList))
	{
		TraceError("LoadLocaleData - LoadLocaleQuizVnum(%s) Error", szLocaleQuizList);
		return false;
	}
#endif

#ifdef ENABLE_CLIENT_PERFORMANCE
	if (!CPythonPlayerSettingsModule::Instance().RegisterGuildBuildingList(szGuildBuilding))
	{
		TraceError("LoadLocaleData - RegisterGuildBuildingList(%s) Error", szSkillDescFileName);
		return false;
	}
#endif

#ifdef ENABLE_GROWTH_PET_SYSTEM
	if (!rkSkillMgr.RegisterPetSkillTable(szPetSkillFileName))
	{
		TraceError("LoadLocaleData - RegisterPetSkillTable(%s) Error", szPetSkillFileName);
		return false;
	}
#endif

#ifdef ENABLE_NPC_WEAR_ITEM
	if (!rkNPCMgr.LoadNPCWear(szNPCWearItem))
	{
		TraceError("LoadLocaleData - LoadNPCWearItem(%s) Error", szNPCWearItem);
		return false;
	}
#endif

#ifdef ENABLE_WIKI_SYSTEM
	CPythonWiki::Instance().ReadData(localePath);
#endif

	return true;
}

unsigned __GetWindowMode(bool windowed)
{
	if (windowed)
		return WS_OVERLAPPED | WS_CAPTION |   WS_SYSMENU | WS_MINIMIZEBOX;

	return WS_POPUP;
}

bool CPythonApplication::Create(PyObject *poSelf, const char *c_szName, int width, int height, int Windowed)
{
	NANOBEGIN
		Windowed = CPythonSystem::Instance().IsWindowed() ? 1 : 0;

	bool bAnotherWindow = false;

	if (FindWindow(nullptr, c_szName))
		bAnotherWindow = true;

	m_dwWidth = width;
	m_dwHeight = height;

	// Window
	UINT WindowMode = __GetWindowMode(Windowed ? true : false);

	if (!CMSWindow::Create(c_szName, 4, 0, WindowMode, ::LoadIcon( GetInstance(), MAKEINTRESOURCE( IDI_METIN2 ) ), IDC_CURSOR_NORMAL))
	{
		TraceError("CMSWindow::Create failed");
		SET_EXCEPTION(CREATE_WINDOW);
		return false;
	}

	if (m_pySystem.IsUseDefaultIME())
	{
		CPythonIME::Instance().UseDefaultIME();
	}

#ifdef ENABLE_DISCORD_RPC
	m_pyNetworkStream.Discord_Start();
#endif

	AdjustSize(m_pySystem.GetWidth(), m_pySystem.GetHeight());

	if (Windowed)
	{
		m_isWindowed = true;

		if (bAnotherWindow)
		{
			RECT rc;

			GetClientRect(&rc);

			int windowWidth = rc.right - rc.left;
			int windowHeight = (rc.bottom - rc.top);

			CMSApplication::SetPosition(GetScreenWidth() - windowWidth, GetScreenHeight() - 60 - windowHeight);
		}
		SetPosition(-8, 0); //Fix
	}
	else
	{
		m_isWindowed = false;
		SetPosition(0, 0);
	}

	if (!CreateCursors())
	{
		TraceError("CMSWindow::Cursors Create Error");
		SET_EXCEPTION("CREATE_CURSOR");
		return false;
	}

	if (!m_pySystem.IsNoSoundCard())
	{
		// Sound
		if (!m_SoundManager.Create())
		{
		}
	}

	// Device
	if (!CreateDevice(m_pySystem.GetWidth(), m_pySystem.GetHeight(), Windowed, m_pySystem.GetBPP(), m_pySystem.GetFrequency()))
		return false;

	GrannyCreateSharedDeformBuffer();

	SetVisibleMode(true);

	if (m_isWindowFullScreenEnable)
	{
		SetWindowPos(GetWindowHandle(), HWND_TOP, 0, 0, width, height, SWP_SHOWWINDOW);
	}

	if (!InitializeKeyboard(GetWindowHandle()))
		return false;

	m_pySystem.GetDisplaySettings();

	// Mouse
	if (m_pySystem.IsSoftwareCursor())
		SetCursorMode(CURSOR_MODE_SOFTWARE);
	else
		SetCursorMode(CURSOR_MODE_HARDWARE);

	// Network
	if (!m_netDevice.Create())
	{
		TraceError("NetDevice::Create failed");
		SET_EXCEPTION("CREATE_NETWORK");
		return false;
	}

	if (!m_grpDevice.IsFastTNL())
		CGrannyLODController::SetMinLODMode(true);

	m_pyItem.Create();

	// Other Modules
	DefaultFont_Startup();

	CPythonIME::Instance().Create(GetWindowHandle());
	CPythonIME::Instance().SetText("", 0);
	CPythonTextTail::Instance().Initialize();

	// Light Manager
	m_LightManager.Initialize();

	CGraphicImageInstance::CreateSystem(32);

	STICKYKEYS sStickKeys;
	memset(&sStickKeys, 0, sizeof(sStickKeys));
	sStickKeys.cbSize = sizeof(sStickKeys);
	SystemParametersInfo( SPI_GETSTICKYKEYS, sizeof(sStickKeys), &sStickKeys, 0 );
	m_dwStickyKeysFlag = sStickKeys.dwFlags;

	sStickKeys.dwFlags &= ~(SKF_AVAILABLE|SKF_HOTKEYACTIVE);
	SystemParametersInfo( SPI_SETSTICKYKEYS, sizeof(sStickKeys), &sStickKeys, 0 );

	// SphereMap
	CGrannyMaterial::CreateSphereMap(0, "d:/ymir work/special/spheremap.jpg");
	CGrannyMaterial::CreateSphereMap(1, "d:/ymir work/special/spheremap01.jpg");
	return true;
}

void CPythonApplication::SetGlobalCenterPosition(LONG x, LONG y)
{
	CPythonBackground& rkBG=CPythonBackground::Instance();
	rkBG.GlobalPositionToLocalPosition(x, y);

	float z = CPythonBackground::Instance().GetHeight(x, y);

	CPythonApplication::Instance().SetCenterPosition(x, y, z);
}

void CPythonApplication::SetCenterPosition(float fx, float fy, float fz)
{
	m_v3CenterPosition.x = +fx;
	m_v3CenterPosition.y = -fy;
	m_v3CenterPosition.z = +fz;
}

void CPythonApplication::GetCenterPosition(TPixelPosition * pPixelPosition)
{
	pPixelPosition->x = +m_v3CenterPosition.x;
	pPixelPosition->y = -m_v3CenterPosition.y;
	pPixelPosition->z = +m_v3CenterPosition.z;
}

void CPythonApplication::SetServerTime(time_t tTime)
{
	m_dwStartLocalTime	= ELTimer_GetMSec();
	m_tServerTime		= tTime;
	m_tLocalStartTime	= time(0);
}

time_t CPythonApplication::GetServerTime()
{
	return (ELTimer_GetMSec() - m_dwStartLocalTime) + m_tServerTime;
}

time_t CPythonApplication::GetServerTimeStamp()
{
	return (time(0) - m_tLocalStartTime) + m_tServerTime;
}

float CPythonApplication::GetGlobalTime()
{
	return m_fGlobalTime;
}

float CPythonApplication::GetGlobalElapsedTime()
{
	return m_fGlobalElapsedTime;
}

void CPythonApplication::SetFPS(int iFPS)
{
	m_iFPS = iFPS;
}

int CPythonApplication::GetWidth()
{
	return m_dwWidth;
}

int CPythonApplication::GetHeight()
{
	return m_dwHeight;
}

void CPythonApplication::SetConnectData(const char * c_szIP, int iPort)
{
	m_strIP = c_szIP;
	m_iPort = iPort;
}

void CPythonApplication::GetConnectData(std::string & rstIP, int & riPort)
{
	rstIP	= m_strIP;
	riPort	= m_iPort;
}

void CPythonApplication::EnableSpecialCameraMode()
{
	m_isSpecialCameraMode = TRUE;
}

void CPythonApplication::SetCameraSpeed(int iPercentage)
{
	m_fCameraRotateSpeed = c_fDefaultCameraRotateSpeed * float(iPercentage) / 100.0f;
	m_fCameraPitchSpeed = c_fDefaultCameraPitchSpeed * float(iPercentage) / 100.0f;
	m_fCameraZoomSpeed = c_fDefaultCameraZoomSpeed * float(iPercentage) / 100.0f;
}

void CPythonApplication::SetForceSightRange(int iRange)
{
	m_iForceSightRange = iRange;
}

void CPythonApplication::Clear()
{
	m_pySystem.Clear();
}

#ifdef ENABLE_BLINK_ALERT
#include <Windows.h>
void CPythonApplication::FlashApplication()	//@fixme403
{
#ifndef __EMSCRIPTEN__
	HWND hWnd = GetWindowHandle();
	FLASHWINFO fi;
	fi.cbSize = sizeof(FLASHWINFO);
	fi.hwnd = hWnd;
	fi.dwFlags = FLASHW_ALL | FLASHW_TIMERNOFG;
	fi.uCount = 0;
	fi.dwTimeout = 0;
	FlashWindowEx(&fi);
#endif
}
#endif

#ifdef ENABLE_MULTI_FARM_BLOCK
void CPythonApplication::MultiFarmBlockIcon(BYTE bStatus)
{
#ifndef __EMSCRIPTEN__
	HICON exeIcon = bStatus ? LoadIcon(ms_hInstance, MAKEINTRESOURCE(IDI_METIN2)) : LoadIcon(ms_hInstance, MAKEINTRESOURCE(BLOCK_METIN2));
	SendMessage(GetWindowHandle(), WM_SETICON, ICON_BIG, (LPARAM)exeIcon);
#endif
}
#endif

void CPythonApplication::Destroy()
{
	WebBrowser_Destroy();

	// SphereMap
	CGrannyMaterial::DestroySphereMap();

	m_kWndMgr.Destroy();

	CPythonSystem::Instance().SaveConfig();

#ifdef ENABLE_RENDER_TARGET
	m_kRenderTargetManager.Destroy();
#endif

	DestroyCollisionInstanceSystem();

	m_pySystem.SaveInterfaceStatus();

	m_pyEventManager.Destroy();
	m_FlyingManager.Destroy();

	m_pyMiniMap.Destroy();

	m_pyTextTail.Destroy();
	m_pyChat.Destroy();
	m_kChrMgr.Destroy();
	m_RaceManager.Destroy();

	m_pyItem.Destroy();
	m_kItemMgr.Destroy();

	m_pyBackground.Destroy();

	m_kEftMgr.Destroy();
	m_LightManager.Destroy();

	DefaultFont_Cleanup();

	GrannyDestroySharedDeformBuffer();

	m_pyGraphic.Destroy();

#ifdef ENABLE_DISCORD_RPC
	m_pyNetworkStream.Discord_Close();
#endif

	m_pyRes.Destroy();

	m_kGuildMarkDownloader.Disconnect();

	CGrannyModelInstance::DestroySystem();
	CGraphicImageInstance::DestroySystem();

	m_SoundManager.Destroy();
	m_grpDevice.Destroy();

	CAttributeInstance::DestroySystem();
	CTextFileLoader::DestroySystem();
	DestroyCursors();

	CMSApplication::Destroy();

	STICKYKEYS sStickKeys;
	memset(&sStickKeys, 0, sizeof(sStickKeys));
	sStickKeys.cbSize = sizeof(sStickKeys);
	sStickKeys.dwFlags = m_dwStickyKeysFlag;
	SystemParametersInfo( SPI_SETSTICKYKEYS, sizeof(sStickKeys), &sStickKeys, 0 );
}