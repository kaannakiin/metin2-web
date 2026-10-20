#pragma once
#include <cstddef>
#include <cstdint>
#include "UserInterface/Packet.h"

#ifdef ENABLE_RESP_SYSTEM
namespace m2w {
enum class RespPrefixStatus { NeedMore, Valid, Invalid };

// Check the declared frame length before the handler can consume any part of
// the following packet. At most six plaintext prefix bytes are needed.
inline RespPrefixStatus ValidateRespPrefix(const unsigned char* bytes, std::size_t available)
{
    if (available < 3)
        return RespPrefixStatus::NeedMore;
    if (!bytes)
        return RespPrefixStatus::Invalid;
    const std::uint32_t declared = bytes[1] | (std::uint32_t(bytes[2]) << 8);
    if (declared < sizeof(TPacketGCRespHeader))
        return RespPrefixStatus::Invalid;
    if (available < sizeof(TPacketGCRespHeader))
        return RespPrefixStatus::NeedMore;
    std::uint32_t expected = 0;
    switch (bytes[3]) {
    case RESP_GC_SUBHEADER_DATA_RESP:
    case RESP_GC_SUBHEADER_DATA_DROP: {
        const std::uint32_t base = sizeof(TPacketGCRespHeader) + 2 + 4 +
            (bytes[3] == RESP_GC_SUBHEADER_DATA_DROP ? sizeof(TPacketGCRespGold) : 0);
        if (declared < base)
            return RespPrefixStatus::Invalid;
        if (available < 6)
            return RespPrefixStatus::NeedMore;
        const std::uint32_t count = bytes[4] | (std::uint32_t(bytes[5]) << 8);
        expected = base + count * (bytes[3] == RESP_GC_SUBHEADER_DATA_DROP
                                  ? sizeof(TPacketGCRespItem) : sizeof(TPacketGCRespData));
        break;
    }
    case RESP_GC_SUBHEADER_DATA_MOB:
        if (declared < sizeof(TPacketGCRespHeader) + sizeof(TPacketGCMapData))
            return RespPrefixStatus::Invalid;
        if (available < 5)
            return RespPrefixStatus::NeedMore;
        expected = sizeof(TPacketGCRespHeader) + sizeof(TPacketGCMapData) + std::uint32_t(bytes[4]) * 4;
        break;
    case RESP_GC_SUBHEADER_REFRESH_RESP:
        expected = sizeof(TPacketGCRespHeader) + sizeof(TPacketGCRespRefresh);
        break;
    default:
        return RespPrefixStatus::Invalid;
    }
    return declared == expected ? RespPrefixStatus::Valid : RespPrefixStatus::Invalid;
}
}
#endif
