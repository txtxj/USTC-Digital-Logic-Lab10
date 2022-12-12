import os
import pygame


class Translator:
    # 单字符转全角
    def b2q(self, uchar):
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:
            return uchar
        if inside_code == 0x0020:
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        return chr(inside_code)

    # 字符串转全角
    def B2Q(self, s):
        txt = ""
        for c in s:
            txt += self.b2q(c)
        return txt

    def execute(self, text):
        pygame.init()
        text = self.B2Q(text)

        # 字符串转化后的长宽
        rows = 16
        cols = len(text) * 16

        font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 16)
        rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))

        # 用于储存二进制、十六进制结果
        bit_str = ""
        hex_str = ""

        # RGB 数组
        array = pygame.surfarray.array2d(rtext)

        for i in range(cols):
            for j in range(rows):
                if array[i][j] > 0:
                    bit_str += "1"
                else:
                    bit_str += "0"
        cnt = int(cols * rows / 16)
        for i in range(cnt):
            hex_str += "{:04x} ".format(int(bit_str[16 * i: 16 * i + 16], 2))
        f = open("Words.txt", "w")
        f.write(hex_str)
        f.close()
