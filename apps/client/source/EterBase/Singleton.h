#ifndef __INC_ETERLIB_SINGLETON_H__
#define __INC_ETERLIB_SINGLETON_H__

#include <assert.h>
#include <stdio.h>
#include <typeinfo>
#ifdef _WIN32
#include <windows.h>
#endif

template <typename T> class CSingleton
{
	static T * ms_singleton;

public:
	CSingleton()
	{
		assert(!ms_singleton);
		int offset = (int) (T*) 1 - (int) (CSingleton <T>*) (T*) 1;
		ms_singleton = (T*) ((int) this + offset);
	}

	virtual ~CSingleton()
	{
		assert(ms_singleton);
		ms_singleton = 0;
	}

	__forceinline static T & Instance()
	{
		if (!ms_singleton)
		{
#ifdef _WIN32
			char szMsg[512];
			const char* pTypeName = typeid(T).name();
#ifdef _MSC_VER
			sprintf_s(szMsg, sizeof(szMsg), "CSingleton<%s>::Instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#else
			snprintf(szMsg, sizeof(szMsg), "CSingleton<%s>::Instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#endif
			OutputDebugStringA(szMsg);
			// Log dosyasýna da yaz
			FILE* fp = fopen("singleton_error.log", "a");
			if (fp)
			{
				fprintf(fp, "%s\n", szMsg);
				fprintf(fp, "Please press 'Retry' button and check Call Stack window in Visual Studio debugger.\n\n");
				fclose(fp);
			}
#endif
		}
		assert(ms_singleton && "CSingleton::Instance() called before initialization! Check singleton_error.log or call stack for details.");
		return (*ms_singleton);
	}

	__forceinline static T * InstancePtr()
	{
		return (ms_singleton);
	}

	__forceinline static T & instance()
	{
		if (!ms_singleton)
		{
#ifdef _WIN32
			char szMsg[512];
			const char* pTypeName = typeid(T).name();
#ifdef _MSC_VER
			sprintf_s(szMsg, sizeof(szMsg), "CSingleton<%s>::instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#else
			snprintf(szMsg, sizeof(szMsg), "CSingleton<%s>::instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#endif
			OutputDebugStringA(szMsg);
			// Log dosyasýna da yaz
			FILE* fp = fopen("singleton_error.log", "a");
			if (fp)
			{
				fprintf(fp, "%s\n", szMsg);
				fprintf(fp, "Please press 'Retry' button and check Call Stack window in Visual Studio debugger.\n\n");
				fclose(fp);
			}
#endif
		}
		assert(ms_singleton && "CSingleton::instance() called before initialization! Check singleton_error.log or call stack for details.");
		return (*ms_singleton);
	}
};

template <typename T> T * CSingleton <T>::ms_singleton = 0;

//
// singleton for non-hungarian
//
template <typename T> class singleton
{
	static T * ms_singleton;

public:
	singleton()
	{
		assert(!ms_singleton);
		int offset = (int) (T*) 1 - (int) (singleton <T>*) (T*) 1;
		ms_singleton = (T*) ((int) this + offset);
	}

	virtual ~singleton()
	{
		assert(ms_singleton);
		ms_singleton = 0;
	}

	__forceinline static T & Instance()
	{
		if (!ms_singleton)
		{
#ifdef _WIN32
			char szMsg[512];
			const char* pTypeName = typeid(T).name();
#ifdef _MSC_VER
			sprintf_s(szMsg, sizeof(szMsg), "singleton<%s>::Instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#else
			snprintf(szMsg, sizeof(szMsg), "singleton<%s>::Instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#endif
			OutputDebugStringA(szMsg);
			FILE* fp = fopen("singleton_error.log", "a");
			if (fp)
			{
				fprintf(fp, "%s\n", szMsg);
				fprintf(fp, "Please press 'Retry' button and check Call Stack window in Visual Studio debugger.\n\n");
				fclose(fp);
			}
#endif
		}
		assert(ms_singleton && "singleton::Instance() called before initialization! Check singleton_error.log or call stack for details.");
		return (*ms_singleton);
	}

	__forceinline static T * InstancePtr()
	{
		return (ms_singleton);
	}

	__forceinline static T & instance()
	{
		if (!ms_singleton)
		{
#ifdef _WIN32
			char szMsg[512];
			const char* pTypeName = typeid(T).name();
#ifdef _MSC_VER
			sprintf_s(szMsg, sizeof(szMsg), "singleton<%s>::instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#else
			snprintf(szMsg, sizeof(szMsg), "singleton<%s>::instance() called before initialization!\nFile: %s\nLine: %d\n", pTypeName, __FILE__, __LINE__);
#endif
			OutputDebugStringA(szMsg);
			FILE* fp = fopen("singleton_error.log", "a");
			if (fp)
			{
				fprintf(fp, "%s\n", szMsg);
				fprintf(fp, "Please press 'Retry' button and check Call Stack window in Visual Studio debugger.\n\n");
				fclose(fp);
			}
#endif
		}
		assert(ms_singleton && "singleton::instance() called before initialization! Check singleton_error.log or call stack for details.");
		return (*ms_singleton);
	}
};

template <typename T> T * singleton <T>::ms_singleton = 0;

#endif
