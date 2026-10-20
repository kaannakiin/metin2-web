// Regression fixtures match the running FreeBSD i386 RESP layouts (DWARF).
#include "UserInterface/StdAfx.h"
#include "UserInterface/Packet.h"
#include "resp_wire.h"
#include <cassert>
#include <cstdio>
#include <cstring>

int main()
{
    // A complete refresh packet followed immediately by the next packet.
    const unsigned char fixture[] = {
        49, 24, 0, 3,
        7, 0, 0, 0, 0x44, 0x1f, 0, 0,
        0x78, 0x56, 0x34, 0x12,
        0xa0, 0x86, 0x01, 0, 0x40, 0x0d, 0x03, 0,
        44
    };
    TPacketGCRespHeader header{};
    std::memcpy(&header, fixture, sizeof(header));
    assert(header.header == HEADER_GC_RESP);
    assert(header.subheader == RESP_GC_SUBHEADER_REFRESH_RESP);
    assert(header.size == sizeof(header) + sizeof(TPacketGCRespRefresh));
    TPacketGCRespRefresh refresh{};
    std::memcpy(&refresh, fixture + sizeof(header), sizeof(refresh));
    assert(refresh.id == 7 && refresh.vnum == 8004);
    assert(refresh.nextRespTime == 0x12345678);
    assert(refresh.x == 100000 && refresh.y == 200000);
    assert(fixture[sizeof(header) + sizeof(refresh)] == HEADER_GC_PING);

    // The list entry has a different field order, with time at byte 16.
    const unsigned char entry[] = {
        9, 0, 0, 0, 0xa0, 0x86, 0x01, 0,
        0x40, 0x0d, 0x03, 0, 60, 0, 0, 0,
        0xff, 0xff, 0xff, 0xff
    };
    TPacketGCRespData data{};
    static_assert(sizeof(data) == sizeof(entry), "RESP list entry size");
    std::memcpy(&data, entry, sizeof(data));
    assert(data.id == 9 && data.x == 100000 && data.y == 200000);
    assert(data.time == 60 && data.nextRespTime == -1);
    using Status = m2w::RespPrefixStatus;
    for (unsigned n = 0; n < 4; ++n)
        assert(m2w::ValidateRespPrefix(fixture, n) == Status::NeedMore);
    assert(m2w::ValidateRespPrefix(fixture, 4) == Status::Valid);
    const unsigned char shortHeader[] = {49, 3, 0};
    assert(m2w::ValidateRespPrefix(shortHeader, 3) == Status::Invalid);
    const unsigned char wrongRefresh[] = {49, 23, 0, 3};
    assert(m2w::ValidateRespPrefix(wrongRefresh, 4) == Status::Invalid);
    const unsigned char list[] = {49, 30, 0, 0, 1, 0};
    assert(m2w::ValidateRespPrefix(list, 5) == Status::NeedMore);
    assert(m2w::ValidateRespPrefix(list, 6) == Status::Valid);
    const unsigned char overrun[] = {49, 30, 0, 0, 255, 255};
    assert(m2w::ValidateRespPrefix(overrun, 6) == Status::Invalid);
    const unsigned char drop[] = {49, 24, 0, 1, 1, 0};
    assert(m2w::ValidateRespPrefix(drop, 6) == Status::Valid);
    const unsigned char mob[] = {49, 25, 0, 2, 1};
    assert(m2w::ValidateRespPrefix(mob, 5) == Status::Valid);
    const unsigned char unknown[] = {49, 24, 0, 255};
    assert(m2w::ValidateRespPrefix(unknown, 4) == Status::Invalid);
    std::puts("RESP REGRESSION: layouts, signed fields, next header, fragmentation and malformed lengths PASS");
    return 0;
}
