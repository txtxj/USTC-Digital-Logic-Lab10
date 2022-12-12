import cv2


class Translator:
	def video2imgs(self, video_name, size, gap):
		img_list = []

		cap = cv2.VideoCapture(video_name)

		while cap.isOpened():
			for i in range(gap):
				cap.read()
			ret, frame = cap.read()
			if ret:
				gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

				img = cv2.resize(gray, size, interpolation=cv2.INTER_AREA)

				img_list.append(img)
			else:
				break

		cap.release()

		return img_list

	def img2bits(self, img, mag):
		res = []

		height, width = img.shape
		for col in range(width):
			line = ""
			for row in range(height):
				if img[row][col] > mag:
					line += "1"
				else:
					line += "0"
			res.append(line)

		return res

	def imgs2bits(self, imgs, mag):
		bits = []
		for img in imgs:
			bits.append(self.img2bits(img, mag))

		return bits

	def execute(self, file_name, mag, gap):
		xpx = 42
		ypx = 32

		imgs = self.video2imgs(file_name, (xpx, ypx), gap)
		bits = self.imgs2bits(imgs, mag)

		f = open("Words.txt", mode="w")

		ans = ""

		for cnt in range(xpx):
			hex_str = ""
			for fp in bits:
				hex_str += "{:08x} ".format(int(fp[cnt], 2))
			ans += hex_str + "\n"

		f.write(ans)
