import os

print("请输入要播放的视频文件文件名")
s = input()
if os.path.exists(s) == False:
	print("文件不存在")
else:
	print("请输入亮部阈值（该值越低，所显示的视频中白色占比越多）")
	print("范围0~255")
	mag = input()
	print("请输入采样间隔（不小于0）")
	gap = input()
	os.system("python Translate.py " + s + " " + mag + " " + gap)
	print("视频已转码成功，转码结果位于 Word.txt 中")
	os.system("python Circ.py")
	print("电路已生成成功，电路文件名为 LED.circ")
	print("是否要打开电路文件？打开请按回车键，不打开请关闭")
	input()
	print("正在打开电路文件")
	os.system("Logisim.exe LED.circ")
print("按回车结束...")