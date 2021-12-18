import os

print("请输入想要显示的文本：")
s = input()
os.system("python Translate.py " + s)
print("文本已转码成功，转码结果位于 Word.txt 中")
os.system("python Circ.py " + str(len(s)))
print("电路已生成成功，电路文件名为 LED.circ")
print("正在打开电路文件")
os.system("Logisim.exe LED.circ")
input("按下回车键结束...")