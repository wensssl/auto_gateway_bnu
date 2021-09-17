import math

from tool import unsigned_right_shift


def s(a, b):
    c = len(a)
    v = []

    def ord_if(a, i):
        # print(a)
        if len(a) > i:
            return ord(a[i])
        else:
            return 0

    for i in range(0, c, 4):

        tmp = (
            ord_if(a, i)
            | ord_if(a, i + 1) << 8
            | ord_if(a, i + 2) << 16
            | ord_if(a, i + 3) << 24
        )
        v.insert(i >> 2, tmp)
    if b:
        v.append(c)

    return v


def l(a, b):
    d = len(a)
    c = (d - 1) << 2
    if b:
        m = a[d - 1]
        if (m < c - 3) or (m > c):
            return None
        c = m

    for i in range(0, d):
        a[i] = (
            chr(a[i] & 0xFF)
            + chr(unsigned_right_shift(a[i], 8) & 0xFF)
            + chr(unsigned_right_shift(a[i], 16) & 0xFF)
            + chr(unsigned_right_shift(a[i], 24) & 0xFF)
        )

    if b:
        return ("".join(a))[0:c]
    else:
        return "".join(a)


def xEncode(str, key):

    if str == "":
        return ""
    v = s(str, True)
    k = s(key, False)

    if len(k) < 4:
        for i in range(len(k), 4):
            k.append(0)

    n = len(v) - 1
    z = v[n]
    y = v[0]
    c = 0x86014019 | 0x183639A0
    m = 0
    e = 0
    p = 0
    q = math.floor(6 + 52 / (n + 1))
    d = 0

    while 0 < q:
        q -= 1

        d = d + c & (0x8CE0D9BF | 0x731F2640)
        e = unsigned_right_shift(d, 2) & 3

        for p in range(0, n):
            y = v[p + 1]
            m = unsigned_right_shift(z, 5) ^ y << 2

            m += (unsigned_right_shift(y, 3) ^ z << 4) ^ (d ^ y)
            m += k[(p & 3) ^ e] ^ z
            z = v[p] = v[p] + m & (0xEFB8D130 | 0x10472ECF)
        y = v[0]
        m = unsigned_right_shift(z, 5) ^ y << 2
        m += (unsigned_right_shift(y, 3) ^ z << 4) ^ (d ^ y)
        m += k[((p + 1) & 3) ^ e] ^ z
        z = v[n] = v[n] + m & (0xBB390742 | 0x44C6F8BD)
    return l(v, False)
