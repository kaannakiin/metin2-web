// SPDX-License-Identifier: GPL-2.0-or-later
// shellapi.h - ShellExecute for the Anka2 fork's app.ShellExecute (links
// from the game UI). Only http(s) URLs are opened, in a new tab.

#pragma once

#include "win32_compat.h"
#include <emscripten/emscripten.h>

inline HINSTANCE ShellExecuteA(HWND, LPCSTR, LPCSTR c_szFile, LPCSTR, LPCSTR, INT)
{
    if (c_szFile && (strncmp(c_szFile, "http://", 7) == 0 || strncmp(c_szFile, "https://", 8) == 0))
        EM_ASM({ window.open(UTF8ToString($0), '_blank', 'noopener'); }, c_szFile);
    return (HINSTANCE)(intptr_t)33;
}
#define ShellExecute ShellExecuteA
