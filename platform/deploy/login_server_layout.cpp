#include "stdafx.h"
#include "packet.h"
#include <cstdio>

int main()
{
    std::printf("server TSimplePlayer=%zu\n", sizeof(TSimplePlayer));
    std::printf("server TPacketGCLoginSuccess=%zu\n", sizeof(TPacketGCLoginSuccess));
    std::printf("server player slots=%d\n", PLAYER_PER_ACCOUNT);
    return 0;
}
