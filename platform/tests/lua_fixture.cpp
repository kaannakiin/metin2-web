#include <cstdio>
extern "C" {
#include "lua.h"
#include "lauxlib.h"
#include "lualib.h"
}

int main(int argc, char** argv)
{
    if (argc != 3) return 2;
    lua_State* state = lua_open();
    if (!state) return 2;
    luaopen_base(state);
    luaopen_table(state);
    luaopen_string(state);
    luaopen_math(state);
    lua_pushstring(state, argv[2]);
    lua_setglobal(state, "WELCOME_FILE");
    int result = luaL_loadfile(state, argv[1]);
    if (!result) result = lua_pcall(state, 0, 0, 0);
    if (result) std::fprintf(stderr, "%s\n", lua_tostring(state, -1));
    lua_close(state);
    return result ? 1 : 0;
}
