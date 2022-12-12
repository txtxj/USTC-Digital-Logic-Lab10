import math


class CircHandler:
	def wire(self, a, b, c, d):
		return "    <wire from=\"({:d},{:d})\" to=\"({:d},{:d})\"/>\n".format(a, b, c, d)

	def rom(self, x, y, b, s):
		return "    <comp lib=\"4\" loc=\"({:d},{:d})\" name=\"ROM\">\n      <a name=\"addrWidth\" val=\"{:d}\"/>\n      <a name=\"dataWidth\" val=\"32\"/>\n      <a name=\"contents\">addr/data: {:d} 32\n{:s}</a>\n    </comp>\n".format(x, y, b, b, s)

	def clock(self, a, b):
		return "    <comp lib=\"0\" loc=\"({:d},{:d})\" name=\"Clock\">\n      <a name=\"facing\" val=\"north\"/>\n      <a name=\"label\" val=\"Clock\"/>\n      <a name=\"labelloc\" val=\"south\"/>\n    </comp>\n".format(a, b)

	def matrix(self, a, b, c, d):
		return "    <comp lib=\"5\" loc=\"({:d},{:d})\" name=\"DotMatrix\">\n      <a name=\"matrixcols\" val=\"{:d}\"/>\n      <a name=\"matrixrows\" val=\"{:d}\"/>\n      <a name=\"color\" val=\"#ffffff\"/>\n      <a name=\"offcolor\" val=\"#000000\"/>\n    </comp>\n".format(a, b, c, d)

	def counter(self, a, b):
		return "    <comp lib=\"4\" loc=\"(100,480)\" name=\"Counter\">\n      <a name=\"width\" val=\"{:d}\"/>\n      <a name=\"max\" val=\"0x{:x}\"/>\n    </comp>\n".format(a, b)

	def pin(self, a, b, s):
		return "    <comp lib=\"0\" loc=\"({:d},{:d})\" name=\"Pin\">\n      <a name=\"facing\" val=\"north\"/>\n      <a name=\"tristate\" val=\"false\"/>\n      <a name=\"label\" val=\"{:s}\"/>\n      <a name=\"labelloc\" val=\"south\"/>\n    </comp>".format(a, b, s)

	def gate(self, x, y, type, facing, siz, inputs):
		return "    <comp lib=\"1\" loc=\"({:d},{:d})\" name=\"{:s}\">\n      <a name=\"facing\" val=\"{:s}\"/>\n      <a name=\"size\" val=\"{:d}\"/>\n      <a name=\"inputs\" val=\"{:d}\"/>\n    </comp>\n".format(x, y, type, facing, siz, inputs)

	def execute(self):
		sampleFile = open("Sample.circ", mode="r")
		outFile = open("LED.circ", mode="w")
		wordsFile = open("Words.txt", mode="r")

		sampleData = sampleFile.read()
		wordsData = wordsFile.read().split("\n")

		fpNum = int(len(wordsData[0]) / 9)

		# 锚点
		pos = sampleData.find("*")

		# 输出数据
		outList = list(sampleData)

		# Rom 的起始位置，以及每个 Rom 的步长
		romX = 300
		romY = 480
		romS = 80

		# 生成所有 Rom ，一竖列
		for i in range(42):
			outList.insert(pos, self.rom(romX, romY + i * romS, int(math.log(fpNum, 2) + 1), "".join(wordsData[i])))

		# Wire 头的起始位置，以及每个 Wire 的步长
		wireHX = 300
		wireHY = 480
		wireHS = 80

		# Wire 尾的起始位置，以及每个 Wire 的步长
		wireTX = 330
		wireTY = 360
		wireTS = 10

		# 生成所有 Wire ，带拐点
		outList.insert(pos, self.wire(90, 540, 90, 610))
		outList.insert(pos, self.wire(100, 480, 160, 480))
		for i in range(42):
			outList.insert(pos, self.wire(wireHX, wireHY + i * wireHS, wireTX + i * wireTS, wireHY + i * wireHS))
			outList.insert(pos, self.wire(wireTX + i * wireTS, wireHY + i * wireHS, wireTX + i * wireTS, wireTY))
		for i in range(1, 42):
			outList.insert(pos, self.wire(160, wireHY + (i - 1) * wireHS, 160, wireHY + i * wireHS))
		outList.insert(pos, self.wire(110, 570, 110, 510))
		outList.insert(pos, self.wire(110, 510, 90, 510))
		outList.insert(pos, self.wire(90, 510, 90, 500))
		outList.insert(pos, self.wire(80, 510, 80, 500))

		# 生成两个 LED 阵列
		outList.insert(pos, self.matrix(330, 360, 21, 32))
		outList.insert(pos, self.matrix(540, 360, 21, 32))

		# 生成计数器、时钟，及其控制部分
		outList.insert(pos, self.counter(int(math.log(fpNum, 2)) + 1, fpNum - 1))
		outList.insert(pos, self.clock(70, 540))
		outList.insert(pos, self.pin(110, 570, "Reset"))
		outList.insert(pos, self.pin(90, 610, "Pause"))
		outList.insert(pos, self.gate(80, 510, "OR Gate", "north", 30, 2))

		outFile.write("".join(outList))
