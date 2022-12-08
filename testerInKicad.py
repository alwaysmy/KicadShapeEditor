import sys
import pcbnew
sys.path.append(r"C:\Users\Always\Documents\KiCad\6.0\3rdparty\plugins\KicadShapeEditor")

import shape_para_set #包含插件入口的那个python脚本

# shape_para_set.Add_Shapes.Run(pcbnew.ActionPlugin)
dialog=shape_para_set.Dialog(None)
dialog.Show()

# exec(open(r'C:\Users\Always\Documents\KiCad\6.0\3rdparty\plugins\KicadShapeEditor\testerInKicad.py').read())