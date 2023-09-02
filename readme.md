***There is no readme actually.***

KiCad 没有一个一键生成边框，有时候做模块还是比较需要的，对板子外型没有严格限制只是需要画一个指定大小的板子，于是模仿JLC的板边设置写了一个插件。

因为插件本身还是中文的，所以就写中文好了。

## 0、feature

Kicad7.0已经集成了倒角（圆角功能，画框之后右键-圆角线），所以除了能参数化生成边框之外说点别的。

自动设定边框大小（其实就是全包围）

生成圆角边框的时候自动放到分组里面，方便挪动，因为kicad自带的倒角功能最后都是分段的。

也可生成其他层的图形，不过我也没想到有啥用，顺手加上去的。

其他的设想功能，都还在TODO里面

## 1.用法：

打包下载或者git clone到自己的kicad插件目录下（解压),刷新插件列表就行。

以KiCad6.0为例，比如：``C:\Program Files\KiCad\6.0\share\kicad\scripting\plugins`` （取决于你的安装目录）
或者 ``C:\Users\[your user Name]\Documents\KiCad\6.0\3rdparty\plugins`` 个人推荐放在后者路径下，方便迁移和备份。如果是KiCad7.0那么更换到对应的路径即可
Linux下的路径位于
``~/.local/share/kicad/scripting/plugins``

剩下目测，因为目前就一个小窗口都写在上面了。有事儿提issue。


## 2.bug

~~用插件添加的外形，无论是边框还是其他层，都会删除后重新显示出来，但是在PCB文件中他实际上确实被删除了。同时，其他插件也有这个bug，于是我觉得这是KiCad的Bug。这个bug基本不影响使用，因为你删除后第二次用插件添加的时候，他就会消除，原因是只需要刷新PCB文件就不会显示错误的轨迹了，但是如果确实需要删除，或者看他不爽什么的，我添加了一个刷新按钮，点一下一键消除。~~    （已修复见日志解释）

输入框对奇奇怪怪的东西没有阻拦也没有异常处理，所以现阶段不要尝试输入数字以外的东西。以后会支持算式输入的。

2、这个插件我尝试实现了生成边框的同时标注外框尺寸，但是存在bug：

添加之后尺寸不会自动显示，需要关闭pcbnew窗口后打开就会自动加载出来了；我不知道具体原因，我感觉我写的没问题，不过找到一个稍微方便一点的凑合用的方法：
在尺寸标注上显示了一个test的文本，这个可以被显示出来，点一下它之后稍微拖动一下这个文本，尺寸标注就会自动加载出来了，拖动错位了也没关系，按一下ctrl+z就归位到正确的位置了。或者使用全选选中随便移动一下就能显示出来了（迷惑。。。。）

## 3、后续功能添加

太多了，先放着，比如正多边形，大小自适应等等，我觉得做复杂了的话还不如就导入DXF. 。还有右键菜单，更多菜单什么的，方便调整设置，还有保存之前的设置等等。

添加多边形的，圆角的边框类型到group里面方便挪动或者整体选择删除。

Kicad 7.0出了，似乎内置圆角功能，后续再看看整点实用点的。

## 版本修改记录

