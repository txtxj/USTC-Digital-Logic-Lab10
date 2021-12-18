import os
import sys
import pygame #version 2.1.0
import numpy

# 单字符转全角
def b2q(uchar):
	inside_code = ord(uchar)
	if inside_code < 0x0020 or inside_code > 0x7e:
		return uchar 
	if inside_code == 0x0020:
		inside_code = 0x3000
	else:
		inside_code += 0xfee0
	return chr(inside_code)

# 字符串转全角
def B2Q(s):
	txt = ""
	for c in s:
		txt += b2q(c)
	return txt

pygame.init()

# 字符串转化后的长宽 
cols = 16
rows = 16

text = B2Q(sys.argv[1])

cols = len(text) * 16

font = pygame.font.Font(os.path.join("fonts", "simsun.ttc"), 16)
rtext = font.render(text, True, (0, 0, 0), (255, 255, 255))

# 用于储存二进制、十六进制结果
bitstr = ""
hexstr = ""

# RGB 数组
array = pygame.surfarray.array2d(rtext)

for i in range(cols):
	for j in range(rows):
		if (array[i][j] > 0):
			bitstr += "1"
		else:
			bitstr += "0"

cnt = int(cols * rows / 16)

for i in range(cnt):
	hexstr += "{:04x} ".format(int(bitstr[16 * i : 16 * i + 16], 2))

f = open("Words.txt", "w")
f.write(hexstr)