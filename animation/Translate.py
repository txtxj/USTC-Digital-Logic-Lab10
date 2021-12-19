import numpy as np
import cv2
import sys

def video2imgs(video_name, size):
	"""

	:param video_name: 字符串, 视频文件的路径
	:param size: 二元组，(宽, 高)，用于指定生成的字符画的尺寸
	:return: 一个 img 对象的列表，img对象实际上就是 numpy.ndarray 数组
	"""

	img_list = []

	# 从指定文件创建一个VideoCapture对象
	cap = cv2.VideoCapture(video_name)

	# 如果cap对象已经初始化完成了，就返回true，换句话说这是一个 while true 循环
	while cap.isOpened():
		# cap.read() 返回值介绍：
		#   ret 表示是否读取到图像
		#   frame 为图像矩阵，类型为 numpy.ndarry.
		# 每次读 2 帧 30 帧降到 15 帧
		ret, frame = cap.read()
		ret, frame = cap.read()
		if ret:
			# 转换成灰度图，也可不做这一步，转换成彩色字符视频。
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# resize 图片，保证图片转换成字符画后，能完整地在命令行中显示。
			img = cv2.resize(gray, size, interpolation = cv2.INTER_AREA)

			# 分帧保存转换结果
			img_list.append(img)
		else:
			break

	# 结束时要释放空间
	cap.release()

	return img_list


def img2bits(img, mag):
	"""

	:param img: numpy.ndarray, 图像矩阵
	:return: 二进制数的列表
	"""
	res = []

	# 灰度是用8位表示的，最大值为255。
	# 这里将灰度转换到0-1之间
	# 使用 numpy 的逐元素除法加速，这里 numpy 会直接对 img 中的所有元素都除以 255
	percents = img / 255

	# 将灰度值进一步转换到 0 或 1 
	# 同样使用 numpy 的逐元素算法，然后使用 astype 将元素全部转换成 int 值。
	indexes = (percents * mag).astype(np.int) 
	
	# 要注意这里的顺序和 之前的 size 刚好相反（numpy 的 shape 返回 (行数、列数)）
	height, width = img.shape
	for col in range(width):
		line = ""
		for row in range(height):
			if indexes[row][col] > 0:
				line += "1"
			else:
				line += "0"
		res.append(line)

	return res


def imgs2bits(imgs, mag):
	bits = []
	for img in imgs:
		bits.append(img2bits(img, mag))

	return bits

xpx = 42
ypx = 32

imgs = video2imgs(sys.argv[1], (xpx, ypx))
bits = imgs2bits(imgs, int(sys.argv[2]))

f = open("Words.txt", mode = "w")

ans = ""

for cnt in range(xpx):
	hexstr = ""
	for fp in bits:
		hexstr += "{:08x} ".format(int(fp[cnt], 2))
	ans += hexstr + "\n"

f.write(ans)