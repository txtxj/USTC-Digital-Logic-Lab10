import os
from Translate import Translator
from Circ import CircHandler


print("请输入想要显示的文本：")
s = input()

try:
	t = Translator()
	t.execute(s)
except Exception as e:
	print("执行翻译操作时出现异常，错误信息：", e)
	exit(-1)

print("文本已转码成功，转码结果位于 Word.txt 中")
n = ""
while not n.isdigit():
	print("请输入 LED 阵列的个数，若输入数据为 0 ，则默认 LED 阵列个数为字符串长度")
	n = input()

try:
	circ = CircHandler()
	circ.execute(len(s), int(n))
except Exception as e:
	print("执行生成电路操作时出现异常，错误信息：", e)
	exit(-1)
print("电路已生成成功，电路文件名为 LED.circ")
print("是否要打开电路文件？打开请按回车键，不打开请关闭")
input()
print("正在打开电路文件")
os.system("Logisim.exe LED.circ")
input("按下回车键结束...")
