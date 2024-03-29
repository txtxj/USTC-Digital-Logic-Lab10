# USTC 数字电路实验 大作业

该项目使用 Python 生成电路文件，

text 实现 LED 阵列滚动显示字符串（大作业选题 1 中的电路）。

animation 实现 LED 阵列显示动画。

---

Python >= 3.7

在 `./text` 或 `./animation` 目录下执行以下命令：

```bash
pip install requirements.txt
python Start.py
```

---

text 目前已实现的功能：
 - 生成所有 `Wire` 、 `Rom` 、 `DotMatrix` 、 `Clock` 、 `Pin`
 - 根据字符串长度自动生成对应数量的元件，并调整位宽
 - 自动向 `Rom` 中写入数据
 - 向左、向右（可选）滚动显示整个字符串
 - 自定义输入 `DotMatrix` 个数，使得字符串可以显示在与之长度不相等的 LED 阵列上
 - 暂停播放

待实现的功能：
 - 字符串闪烁
 - 每个字独立地像俄罗斯方块一样从右侧推出，到左侧停下
 - ......

---

animation 目前已实现的功能：
 - 生成所有 `Wire` 、 `Rom` 、 `DotMatrix` 、 `Clock` 、 `Pin`
 - 通过自定义输入数据调整显示的黑白阈值
 - 播放 42px * 32px 的动画
 - 停止播放与暂停播放
 - 通过自定义输入数据调整视频采样率

待实现的功能：
 - ......