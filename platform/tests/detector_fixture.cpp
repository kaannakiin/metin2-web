#include "mid_pvp_detector.h"
#include <cassert>
#include <cstdio>

int main()
{
    long socket = 0;
    for (int use = 0; use < 10000; ++use) {
        socket = MidPvpDetectorSocketValue(27989, 0, socket + 1);
        assert(socket == 0);
        assert(socket < 6);
    }
    assert(MidPvpDetectorSocketValue(27989, 0, 5) == 0);
    assert(MidPvpDetectorSocketValue(27989, 1, 12345) == 12345);
    assert(MidPvpDetectorSocketValue(27989, 2, -1) == -1);
    for (long use = 1; use <= 6; ++use)
        assert(MidPvpDetectorSocketValue(76006, 0, use) == use);
    assert(MidPvpDetectorSocketValue(50300, 0, 42) == 42);
    std::puts("DETECTOR: 10000 uses, old counters, alternate item and other sockets PASS");
}
