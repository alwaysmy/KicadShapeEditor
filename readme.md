***There is no readme actually.***

KiCad 没有一个一键生成边框，有时候做模块还是比较需要的，对板子外型没有严格限制只是需要画一个指定大小的板子，于是模仿JLC的板边设置写了一个插件。

因为插件本身还是中文的，所以就写中文好了。

## 1.用法：

目测，有事儿提issue。

## 2.bug

用插件添加的外形，无论是边框还是其他层，都会删除后重新显示出来，但是在PCB文件中他实际上确实被删除了。同时，其他插件也有这个bug，于是我觉得这是KiCad的Bug。这个bug基本不影响使用，因为你删除后第二次用插件添加的时候，他就会消除，原因是只需要刷新PCB文件就不会显示错误的轨迹了，但是如果确实需要删除，或者看他不爽什么的，我添加了一个刷新按钮，点一下一键消除。

## 3、后续功能添加

太多了，先放着，比如正多边形，大小自适应等等，我觉得做复杂了的话还不如就导入DXF.

## 版本修改记录

V0.1

主要功能

V0.10001

添加圆角圆心标注，在铜皮层上和用户注释层上面添加了一个圆角对应的圆心用来方便吸附安装孔的封装。

V0.10002

暂时去掉了铜皮层上的标注，防止影响正常电路绘制，因为我感觉用不上。。。后面再看看有没有好办法来方便吸附，或者等添加更多选项功能再做吧。

修复输入不能用浮点数的bug：太蠢了，输入项没有做测试，目前能保证浮点数输入正常


