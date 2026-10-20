#pragma once

// Socket 0 is the six-use counter for ordinary Metin detectors. Keep the
// reusable starter detector at zero; the alternate item 76006 remains limited.
inline constexpr long MidPvpDetectorSocketValue(unsigned int vnum, int socket, long value)
{
    return vnum == 27989 && socket == 0 ? 0 : value;
}
