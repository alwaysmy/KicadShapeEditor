***There is no readme actually.***

KiCad 没有一个一键生成边框，有时候做模块还是比较需要的，对板子外型没有严格限制只是需要画一个指定大小的板子，于是模仿JLC的板边设置写了一个插件。

因为插件本身还是中文的，所以就写中文好了。

## 1.用法：

打包下载或者git clone到自己的kicad插件目录下（解压),刷新插件列表就行。比如：``C:\Program Files\KiCad\6.0\share\kicad\scripting\plugins``
或者 ``C:\Users\[your user Name]\Documents\KiCad\6.0\3rdparty\plugins``

剩下目测，有事儿提issue。

## 2.bug

~~用插件添加的外形，无论是边框还是其他层，都会删除后重新显示出来，但是在PCB文件中他实际上确实被删除了。同时，其他插件也有这个bug，于是我觉得这是KiCad的Bug。这个bug基本不影响使用，因为你删除后第二次用插件添加的时候，他就会消除，原因是只需要刷新PCB文件就不会显示错误的轨迹了，但是如果确实需要删除，或者看他不爽什么的，我添加了一个刷新按钮，点一下一键消除。~~    （已修复见日志解释）

输入框对奇奇怪怪的东西没有阻拦也没有异常处理，所以现阶段不要尝试输入数字以外的东西。以后会支持算式输入的。

2、添加了可以在添加边框的时候一同添加尺寸标注，但是存在bug：
添加之后尺寸不会自动显示，需要关闭pcbnew窗口后打开就会自动加载出来了；我不知道具体原因，我感觉我写的没问题，不过找到一个稍微方便一点的凑合用的方法：
在尺寸标注上显示了一个test的文本，这个可以被显示出来，点一下它之后稍微拖动一下这个文本，尺寸标注就会自动加载出来了，拖动错位了也没关系，按一下ctrl+z就归位到正确的位置了。或者使用全选选中随便移动一下就能显示出来了（迷惑。。。。）

## 3、后续功能添加

太多了，先放着，比如正多边形，大小自适应等等，我觉得做复杂了的话还不如就导入DXF. 。还有右键菜单，更多菜单什么的，方便调整设置，还有保存之前的设置等等。

添加多边形的，圆角的边框类型到group里面方便挪动或者整体选择删除。

## 版本修改记录

V0.1

主要功能

V0.10001

添加圆角圆心标注，在铜皮层上和用户注释层上面添加了一个圆角对应的圆心用来方便吸附安装孔的封装。

V0.10002

暂时去掉了铜皮层上的标注，防止影响正常电路绘制，因为我感觉用不上。。。后面再看看有没有好办法来方便吸附，或者等添加更多选项功能再做吧。用户注释层上的圆心仍然保留，可以作为参考，但是好像没办法自动吸附上去。

修复输入不能输入浮点数的bug：太蠢了，输入项没有做测试，目前能保证浮点数输入正常

v0.101

修复了在kicad内删除被添加的边框后，该边框会在随缘时间后回显且删不掉的bug（Dialog改为show方法，即无模式显示，这个bug就不存在了，原来是showModal，？？？摸不着头脑，能用就行）。而且无模式显示能不关插件的情况下操作后面窗口的元素。

v0.101002

增加了层可选，可以选择添加生成的形状到不同的层；

增加了一个全是TODO的右键菜单；增加刷新pcb功能到右键菜单里面

更新调试方法。
v0.101009
添加了自动设置参数，一键获取pcb信息，生成合适的边框大小
增加了获取板子参数并使用标注标注在用户注释层上（存在bug，凑合用）

