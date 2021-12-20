import os

if os.path.exists("cache/") == False:
	os.mkdir("cache/")

f = open("cache/temp.txt", mode = "w")

print("请输入想要显示的文本：")
s = input()
f.write(s)
f.close()
os.system("python Translate.py cache/temp.txt")
print("文本已转码成功，转码结果位于 Word.txt 中")
n = ""
while n.isdigit() == False:
	print("请输入 LED 阵列的个数，若输入数据为 0 ，则默认 LED 阵列个数为字符串长度")
	n = input()
os.system("python Circ.py " + str(len(s)) + " {:s}".format(n))
print("电路已生成成功，电路文件名为 LED.circ")
print("是否要打开电路文件？打开请按回车键，不打开请关闭")
input()
print("正在打开电路文件")
os.system("Logisim.exe LED.circ")
input("按下回车键结束...")