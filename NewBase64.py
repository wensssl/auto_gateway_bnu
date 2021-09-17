class NewBase64:
    # 引入alpha的base64加密
    def __init__(
        self,
        padchar="=",
        alpha="LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA",
    ):
        self.__ALPHA = alpha
        self.__PADCHAR = padchar

    def __getbyte64(self, s, i):
        idx = self.__ALPHA[int(s[i])]
        if idx == -1:
            print("Cannot decode base64")

        return idx

    def setAlpha(self, s):
        self.__ALPHA = s

    def decode(self, s):
        # 解密
        pads = (0,)
        i, b10, imax = (len(s),)
        x = []
        s = str(s)
        if imax == 0:
            return s

        if imax % 4 != 0:
            print("Cannot decode base64")

        if s[imax - 1] == self.__PADCHAR:
            pads = 1
            if s.charAt(imax - 2) == self.__PADCHAR:
                pads = 2

            imax -= 4

        for i in range(0, imax, 4):
            b10 = (
                (self.__getbyte64(s, i) << 18)
                | (self.__getbyte64(s, i + 1) << 12)
                | (self.__getbyte64(s, i + 2) << 6)
                | self.__getbyte64(s, i + 3)
            )
            x.append(ord(b10 >> 16))
            x.append(ord((b10 >> 8) & 255))
            x.append(ord(b10 & 255))
        i = i + 4
        if pads == 1:
            b10 = (
                (self.__getbyte64(s, i) << 18)
                | (self.__getbyte64(s, i + 1) << 12)
                | (self.__getbyte64(s, i + 2) << 6)
            )

            x.append(ord(b10 >> 16))
            x.append(ord((b10 >> 8) & 255))
        elif pads == 2:
            b10 = (self.__getbyte64(s, i) << 18) | (
                self.__getbyte64(s, i + 1) << 12)
            x.append(ord(b10 >> 16))

        return ("").join(x)

    def __getbyte(self, s, i):
        x = ord(s[i])
        # print(x)
        if x > 255:
            print("INVALID_CHARACTER_ERR: DOM Exception 5")

        return x

    def encode(self, s):
        # 加密
        s = str(s)
        i = []
        b10 = []
        x = []
        imax = len(s) - len(s) % 3
        if len(s) == 0:
            return s

        for i in range(0, imax, 3):
            b10 = (
                (self.__getbyte(s, i) << 16)
                | (self.__getbyte(s, i + 1) << 8)
                | self.__getbyte(s, i + 2)
            )
            x.append(self.__ALPHA[b10 >> 18])
            x.append(self.__ALPHA[(b10 >> 12) & 63])
            x.append(self.__ALPHA[(b10 >> 6) & 63])
            x.append(self.__ALPHA[b10 & 63])
        i = i + 3
        if (len(s) - imax) == 1:

            b10 = self.__getbyte(s, i) << 16
            x.append(
                self.__ALPHA[b10 >> 18]
                + self.__ALPHA[(b10 >> 12) & 63]
                + self.__PADCHAR
                + self.__ALPHA
            )
        elif (len(s) - imax) == 2:
            b10 = (self.__getbyte(s, i) << 16) | (
                self.__getbyte(s, i + 1) << 8)
            x.append(
                self.__ALPHA[b10 >> 18]
                + self.__ALPHA[(b10 >> 12) & 63]
                + self.__ALPHA[(b10 >> 6) & 63]
                + self.__PADCHAR
            )

        return "".join(x)
