# 在Kicad控制台中打开这个文件用来测试，执行下面命令即可
# exec(open(r'C:\Users\alwaysLap\Documents\KiCad\7.0\scripting\plugins\KicadShapeEditor\testerInKicad.py').read())
import sys
import pcbnew


kicadVersion = pcbnew.GetMajorMinorVersion()    # 获取住主要版本号 例如7.0
if kicadVersion == '7.0':
    sys.path.append(r'C:\Users\alwaysLap\Documents\KiCad\7.0\scripting\plugins\KicadShapeEditor')
elif kicadVersion == '6.0':
    sys.path.append(r'C:\Users\alwaysLap\Documents\KiCad\6.0\scripting\plugins\KicadShapeEditor')
else:
    pass #更低版本不打算支持，更高版本现在还没出呢
# sys.path.append(r"C:\Users\Always\Documents\KiCad\6.0\3rdparty\plugins\KicadShapeEditor")

import shape_para_set #包含插件入口的那个python脚本
# shape_para_set.Add_Shapes.Run(pcbnew.ActionPlugin)
dialog=shape_para_set.Dialog(None)
dialog.Show()
