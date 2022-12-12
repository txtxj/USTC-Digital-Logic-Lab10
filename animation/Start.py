import os
from Translate import Translator
from Circ import CircHandler

print("请输入要播放的视频文件文件名")
s = input()
if not os.path.exists(s):
	print("文件不存在")
else:
	print("请输入亮部阈值（该值越低，所显示的视频中白色占比越多）")
	print("范围0~255")
	mag = input()
	print("请输入采样间隔（不小于0）")
	gap = input()
	try:
		t = Translator()
		t.execute(s, int(mag), int(gap))
	except Exception as e:
		print("视频转码过程中出现异常，错误信息：", e)
		exit(-1)
	print("视频已转码成功，转码结果位于 Word.txt 中")
	try:
		c = CircHandler()
		c.execute()
	except Exception as e:
		print("执行生成电路操作时出现异常，错误信息：", e)
		exit(-1)
	print("电路已生成成功，电路文件名为 LED.circ")
	print("是否要打开电路文件？打开请按回车键，不打开请关闭")
	input()
	print("正在打开电路文件")
	os.system("Logisim.exe LED.circ")
print("按回车结束...")
