import math


class CircHandler:
    def wire(self, a, b, c, d):
        return "    <wire from=\"({:d},{:d})\" to=\"({:d},{:d})\"/>\n".format(a, b, c, d)

    def rom(self, x, y, b, s):
        return "    <comp lib=\"4\" loc=\"({:d},{:d})\" name=\"ROM\">\n      <a name=\"addrWidth\" val=\"{:d}\"/>\n      <a name=\"dataWidth\" val=\"16\"/>\n      <a name=\"contents\">addr/data: {:d} 16\n{:s}</a>\n    </comp>\n".format(
            x, y, b, b, s)

    def matrix(self, a, b):
        return "    <comp lib=\"5\" loc=\"({:d},{:d})\" name=\"DotMatrix\">\n      <a name=\"matrixcols\" val=\"16\"/>\n      <a name=\"matrixrows\" val=\"16\"/>\n      <a name=\"color\" val=\"#f5ff00\"/>\n      <a name=\"offcolor\" val=\"#ff001e\"/>\n    </comp>\n".format(
            a, b)

    def counter(self, a, b):
        return "    <comp lib=\"4\" loc=\"(100,240)\" name=\"Counter\">\n      <a name=\"width\" val=\"{:d}\"/>\n      <a name=\"max\" val=\"0x{:x}\"/>\n    </comp>\n".format(
            a, b)

    def clock(self, a, b):
        return "    <comp lib=\"0\" loc=\"({:d},{:d})\" name=\"Clock\">\n      <a name=\"facing\" val=\"north\"/>\n      <a name=\"label\" val=\"Clock\"/>\n      <a name=\"labelloc\" val=\"south\"/>\n    </comp>\n".format(
            a, b)

    def pin(self, a, b, c):
        return "    <comp lib=\"0\" loc=\"({:d},{:d})\" name=\"Pin\">\n      <a name=\"tristate\" val=\"false\"/>\n      <a name=\"label\" val=\"{:s}\"/>\n    </comp>\n".format(
            a, b, c)

    def gate(self, x, y, type, facing, siz, inputs):
        return "    <comp lib=\"1\" loc=\"({:d},{:d})\" name=\"{:s}\">\n      <a name=\"facing\" val=\"{:s}\"/>\n      <a name=\"size\" val=\"{:d}\"/>\n      <a name=\"inputs\" val=\"{:d}\"/>\n    </comp>\n".format(
            x, y, type, facing, siz, inputs)

    # 将 Rom 内容左移四位，求得下一个 Rom 的内容
    def next_list(self, lst):
        return lst[5:] + lst[:5]

    def execute(self, wordNum, pwordNum):
        sampleFile = open("Sample.circ", mode="r")
        outFile = open("LED.circ", mode="w")
        wordsFile = open("Words.txt", mode="r")

        sampleData = sampleFile.read()
        wordsData = wordsFile.read()
        romData = list(wordsData)

        # 锚点
        pos = sampleData.find("*")

        # 输出数据
        outList = list(sampleData)

        # 总字数、显示的字数、总行数、显示的行数
        if pwordNum == 0:
            pwordNum = wordNum
        lineNum = wordNum * 16
        plineNum = pwordNum * 16

        # Rom 的起始位置，以及每个 Rom 的步长
        romX = 300
        romY = 240
        romS = 80

        # 生成所有 Rom ，一竖列
        for i in range(plineNum):
            outList.insert(pos, self.rom(romX, romY + i * romS, int(math.log(lineNum, 2) + 1), "".join(wordsData)))
            wordsData = self.next_list(wordsData)

        # DotMatrix 的起始位置，以及每个 DotMatrix 的步长
        matrixX = 310
        matrixY = 190
        matrixS = 160

        # 生成所有 DotMatrix ， 一横行
        for i in range(pwordNum):
            outList.insert(pos, self.matrix(matrixX + i * matrixS, matrixY))

        # Wire 头的起始位置，以及每个 Wire 的步长
        wireHX = 300
        wireHY = 240
        wireHS = 80

        # Wire 尾的起始位置，以及每个 Wire 的步长
        wireTX = 310
        wireTY = 190
        wireTS = 10

        # 生成所有 Wire ，带拐点
        outList.insert(pos, self.wire(80, 260, 80, 270))
        outList.insert(pos, self.wire(70, 300, 70, 380))
        outList.insert(pos, self.wire(90, 300, 90, 340))
        outList.insert(pos, self.wire(100, 240, 160, 240))
        for i in range(plineNum):
            outList.insert(pos, self.wire(wireHX, wireHY + i * wireHS, wireTX + i * wireTS, wireHY + i * wireHS))
            outList.insert(pos, self.wire(wireTX + i * wireTS, wireHY + i * wireHS, wireTX + i * wireTS, wireTY))
        for i in range(1, plineNum):
            outList.insert(pos, self.wire(160, wireHY + (i - 1) * wireHS, 160, wireHY + i * wireHS))

        # 生成计数器、时钟，及其控制部分
        outList.insert(pos, self.counter(int(math.log(lineNum, 2)) + 1, lineNum - 1))
        outList.insert(pos, self.clock(90, 340))
        outList.insert(pos, self.pin(70, 230, "Left/Right"))
        outList.insert(pos, self.pin(70, 380, "Pause"))
        outList.insert(pos, self.gate(80, 270, "OR Gate", "north", 30, 2))

        outFile.write("".join(outList))
