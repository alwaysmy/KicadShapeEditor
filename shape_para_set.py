# from cProfile import label
import pcbnew
import os
import wx
from pcbnew import *
import sys
import SettingInterface as mSetting
# Import the gettext module,用于执行不同翻译
# import gettext 
#this plugin is deved for KiCad 6.0.x 只适配了kicad6的api

#---------------------TODO-list：========================
# TODO：AddDimensionToBoard函数内一些写死的值改一下
# TODO: 位置坐标分到一组，大小分为一组，位置坐标增加可选中心还是左上角为坐标点。
# TODO: 增加选项，添加边框的时候删除原来的边框
# TODO：添加高级选项功能--就是设置
# TODO:添加更多选型，用来实现1可以填充为实心图形，2修改线宽 （线宽也放在高级编辑里面# 生成线宽可选
# TODO :添加功能配置记录，用来存放配置和用来每次打开的时候读取上一次保存的记录
# TODO:增加退出的时候自动保存配置，打开的时候自动加载上一次配置（增加在设置里面选择是否记忆）
# TODO: 添加正多边形的添加
# TODO： 添加预览界面
# TODO: 输入数字框换成wxspinctrldouble（不一定做）
# TODO: 添加一键还原默认设置（放右键菜单里面）
# giveupTODO:1 单位可选择 （默认跟随全局还是mm？）放弃原因：做边框用个毛线英制
# 选择边框类型 设置边框大小（圆角大小）（是否添加四角固定孔封装），
# 删除原来的闭合边框（），自动判断坐标（手动设定左上角或者中心坐标）|一键导入外部DXF 一键导入其他pcb文件板框，支持openscad多边形语法
# 对于自动设定参数功能：目前有下述问题
            # 这样做有个缺点就是：
            # 1、板子上所有的元素都被用来计算包围盒了，倒是可以利用这个手动标记边界
            # 2、如上，板子本来就有边框的话就不能识别正确的大小，不过可以加入勾选删除边框的功能，
            # 或者手工按钮删除边框。
            # 3、 注意，之前添加在用户注释层上的东西，也会被包围进去（TODO:想办法排除无关元素）
            # TODO:fix this ,make it better
            # TODO:设置加一条，自动设置参数的时候直接应用而不用确认（提前标记好了可以这样做）
            # TODO:由于自动设置好之后手工调整比较麻烦，
            # 所以添加功能：鼠标滚轮在输入框上滚动的时可以调整值的大小，同时调整之后实时更新生成的边框
            # 不过实时更新的事件来源是鼠标滚动，不能是数值变化，不然前面手动输入的时候就会没输入完四个值就更新了（好像这样也可以？）
            # 这样的话就要获取自己添加的元素的id，每次生成的时候删除上一次生成的，否则就会一直叠加。
            # 设置里面添加关闭这个的功能，避免误触。。感觉也不会（先不做
            # TODO:限制边框尺寸精度，不然会给人造成错觉,默认让这个精度等于线宽，可以改，按照测量来看，准确到小数点后两位就可以了
            # TODO:添加功能，不依赖记录id的情况下删除edge。cuts元素或者最外层edgecuts（暂时不用）
            # TODO:增加偏移量，用于自动设定参数的时候自动扩大或者减小上下左右的距离，放在设置里面还是外面？
#
#3 等后面复选框没有bug了在看看文档层能不能吸附圆心 
# 更新：这里确认了圆心基本不能自动吸附在不对其网格的点上，
# 功能本来就是为了摆放安装孔方便，所以这个功能暂时不做了
# 再更新，发现似乎圆心放在用户注释层，一些元素是可以自动对齐吸附的
# 0 语言忘差不多了，写法得看看了
#2 todo:添加脚本功能类似openscad编辑边框形状
# 分段的边框添加到一个组里面避免移动困难（可选）
# 圆心标记功能添加到高级里面可以取消
# TODO:对于标记的尺寸，后面导入到jlc的小助手读一下看看尺寸要不要做偏移

#1：根据屏幕像素自适应像素大小，目前是根据M这个字母的大小小郑 TODO:或者是调整布局适应方式，看起来没啥大问题其实，先不改了

# -------------------更新表单：----------------------
# 2022 12 之前的就不说了
# 1、更新默认线宽为0.1mm，因为kicad的默认是这么多，以免看着不舒服。
# 2、又该回去了默认线宽，因为jlc开槽精度到不了那么大，太细的线会有错觉（
# 3、分离了部分ui代码，剩下慢慢搞吧。
# 4、准备添加一个右键菜单，已经做了但是没加功能
# 5、添加打开插件就先刷新pcb的代码，避免有文件修改
# 6、更新TODO项目，完成添加层可选的功能
# 7、 添加自适应参数功能，妈妈再也不用担心我要手动写参数了。
# 8、增加添加之后的边框添加尺寸标注，但是有bug，先凑合用
# 9、更新TODO：完成圆角矩形添加到组里，方便选中和移动
# ----------------------Fixed：-------------------------
# 1#原始问题：不知道为什么这样会算不出来宽度，也没报错就运行不了
# 解决：--- 输入线宽需要是整数，已经修复，后续可以添加调整线宽的功能
# 2修复了删除被添加的边框后被回显出来的bug（改dialog的显示方法为show而不是showModal，摸不着头脑
# 但是保留刷新按键，方便一些别的改文件操作 TODO:实际上板子不重新打开pcbnew编辑器是不会从文件重新加载板子的，所以这里没用，起码refresh没用，去掉或者修改。
# 3 
# #-----其他记录---------------
# 增加了一个layerDict用来存储当前板子的层的名称和序号，其实用不用无所谓，放着吧
# 不过这个刷新板子并获取数据的位置不太好，不应该放在ui初始化中间，后面再修改
UNITS = ["mm", "in"]#可以直接从kicad的pcbnew的对象来获取
g_multiplier = 1000000#KiCad中数字的单位是10^-6 mm 所以要乘回去

#
def alert(s, icon=0):
    print(s)
    wx.MessageBox(s, '阿巴阿巴title', wx.OK|icon)
    
# 方便调试的时候加载板子所以写了个函数来区分
def mLoadBoard():
    isDebug = True if sys.gettrace() else False
    if isDebug:
        pcbfile = r'C:\Users\Always\Desktop\dd\dd.kicad_pcb'#没有特殊需求可以随便找一个pcb，直接放工程目录下也行
        boardobj=pcbnew.LoadBoard(pcbfile)
    else:
        boardobj = pcbnew.GetBoard()
    return boardobj


# 这里这些是主要的shape类型
# SHAPE_T_ARC pcbnew
# SHAPE_T_asString pcbnew::EDA_SHAPE
# SHAPE_T_BEZIER pcbnew
# SHAPE_T_CIRCLE pcbnew
# SHAPE_T_LAST pcbnew
# SHAPE_T_POLY pcbnew
# SHAPE_T_RECT pcbnew
# SHAPE_T_SEGMENT pcbnew
# SHAPE_TYPE_asString pcbnew
#添加方形板框，参数长宽 起始点,线段宽度,指定层，
def AddRectShape(shape_length,shape_width,segmentWidth,x0,y0,chosenLayer,boardObj):
    # boardObj = pcbnew.GetBoard()
    # shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments.SetShape(pcbnew.SHAPE_T_RECT)#设置为方形

    shape_segments.SetStart(wxPoint(x0,y0))
    # shape_segments.SetEnd(wxPoint(x0+shape_length,y0+shape_width))
    shape_segments.SetEnd(wxPoint(x0+shape_length,y0+shape_width))

    shape_segments.SetWidth(segmentWidth)#250000
    shape_segments.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 

    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
    boardObj.Add(shape_segments)

#添加圆角矩形 
def AddRoundRectShape(shape_length,shape_width,shape_ra,segmentWidth,x0,y0,chosenLayer,boardObj):
    # boardObj = pcbnew.GetBoard()
    # shape_segments = pcbnew.PCB_SHAPE(boardObj)
    
    # 左上角的圆角 
    # TODO:不知道为啥这里改了PCBshape的变量名就会有问题，以后再说  
    shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments.SetShape(pcbnew.SHAPE_T_ARC)#设置为圆弧
    # 第一个圆角，坐标是（x0-r,y0-r),起始点是（x0-r,y0)
    shape_segments.SetStart(wxPoint(x0,y0+shape_ra))
    shape_segments.SetCenter(wxPoint(x0+shape_ra,y0+shape_ra))
    # shape_segments.SetEnd(wxPoint(x0+shape_ra,y0)) #这样写是顺时针270°不带角度的话      
    # shape_segments.SetArcGeometry(wxPoint(x0,y0+shape_ra),wxPoint(x0+shape_ra,y0+shape_ra),wxPoint(x0+shape_ra,y0))#中点是弧的中点
    shape_segments.SetArcAngleAndEnd(900.0)

    shape_segments.SetWidth(segmentWidth)#250000q
    shape_segments.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
                
    # 右上角的圆角
    arc_ur = pcbnew.PCB_SHAPE(boardObj)
    arc_ur.SetShape(pcbnew.SHAPE_T_ARC)#设置为圆弧
    arc_ur.SetStart(wxPoint(x0+shape_length-shape_ra,y0))
    arc_ur.SetCenter(wxPoint(x0+shape_length-shape_ra,y0+shape_ra))
    arc_ur.SetArcAngleAndEnd(900.0)#顺时针90度，..既然是double为啥还要用0.1做单位度。。
    # arc_ur.SetEnd(wxPoint(x0+shape_ra,y0))
    arc_ur.SetWidth(segmentWidth)#250000q
    arc_ur.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
    
    # 右下角的圆角
    arc_dr = pcbnew.PCB_SHAPE(boardObj)
    arc_dr.SetShape(pcbnew.SHAPE_T_ARC)#设置为圆弧
    arc_dr.SetStart(wxPoint(x0+shape_length,y0+shape_width-shape_ra))
    arc_dr.SetCenter(wxPoint(x0+shape_length-shape_ra,y0+shape_width-shape_ra))
    arc_dr.SetArcAngleAndEnd(900.0)
    # arc_ur.SetEnd(wxPoint(x0+shape_ra,y0))
    arc_dr.SetWidth(segmentWidth)#250000q
    arc_dr.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
    
    arc_dl = pcbnew.PCB_SHAPE(boardObj)
    arc_dl.SetShape(pcbnew.SHAPE_T_ARC)#设置为圆弧
    arc_dl.SetStart(wxPoint(x0+shape_ra,y0+shape_width))
    arc_dl.SetCenter(wxPoint(x0+shape_ra,y0+shape_width-shape_ra))
    arc_dl.SetArcAngleAndEnd(900.0)
    # arc_ur.SetEnd(wxPoint(x0+shape_ra,y0))
    arc_dl.SetWidth(segmentWidth)#250000q
    arc_dl.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
       
    # 左侧线段
    shape_seg_L = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_L.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    # 
    shape_seg_L.SetStart(wxPoint(x0,y0+shape_ra))
    shape_seg_L.SetEnd(wxPoint(x0,y0+shape_width-shape_ra))

    shape_seg_L.SetWidth(segmentWidth)#250000
    shape_seg_L.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    
    # 上方线段
    shape_seg_U = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_U.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_U.SetStart(wxPoint(x0+shape_ra,y0))
    shape_seg_U.SetEnd(wxPoint(x0+shape_length-shape_ra,y0))

    shape_seg_U.SetWidth(segmentWidth)#250000
    shape_seg_U.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    
    # 右侧线段
    shape_seg_R = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_R.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_R.SetStart(wxPoint(x0+shape_length,y0+shape_ra))
    shape_seg_R.SetEnd(wxPoint(x0+shape_length,y0+shape_width-shape_ra))

    shape_seg_R.SetWidth(segmentWidth)#250000
    shape_seg_R.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    
    # 下侧线段
    shape_seg_D = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_D.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_D.SetStart(wxPoint(x0+shape_ra,y0+shape_width))
    shape_seg_D.SetEnd(wxPoint(x0+shape_length-shape_ra,y0+shape_width))

    shape_seg_D.SetWidth(segmentWidth)#250000
    shape_seg_D.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    
    #继承 EDA_SHAPE的属性可以添加圆弧和贝塞尔曲线       
    # 添加用户注释层圆角的圆心：（测试可以自动吸附）
    AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False,boardObj=boardObj)
    AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False,boardObj=boardObj)
    AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_width-shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False,boardObj=boardObj)
    AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_width-shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False,boardObj=boardObj)
    # # 添加在边框层的圆心
    # AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_ra,pcbnew.Edge_Cuts,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_ra,pcbnew.Edge_Cuts,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_width-shape_ra,pcbnew.Edge_Cuts,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_width-shape_ra,pcbnew.Edge_Cuts,isFill=True,isLocked=False)
    # 添加在第一层铜皮层的圆心 #这一层目前可以自动吸附，所以添加了这个，不然不应该影响电路的元素
    # AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_ra,pcbnew.F_Cu,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_ra,pcbnew.F_Cu,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_width-shape_ra,pcbnew.F_Cu,isFill=True,isLocked=False)
    # AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_width-shape_ra,pcbnew.F_Cu,isFill=True,isLocked=False)
    


    shapeGroup = pcbnew.PCB_GROUP(boardObj)
    shapeGroup.AddItem(shape_segments)
    shapeGroup.AddItem(arc_ur)
    shapeGroup.AddItem(arc_dr)
    shapeGroup.AddItem(arc_dl) 
    shapeGroup.AddItem(shape_seg_L)
    shapeGroup.AddItem(shape_seg_U)
    shapeGroup.AddItem(shape_seg_R)
    shapeGroup.AddItem(shape_seg_D)
    shapeGroup.SetName("RRectGroup")
    # 添加所有元素到shapeGroup里面：应该不需要做可选，因为解组很简单，但是添加组很累，，
    boardObj.Add(shape_segments)
    boardObj.Add(arc_ur)
    boardObj.Add(arc_dr)
    boardObj.Add(arc_dl) 
    boardObj.Add(shape_seg_L)
    boardObj.Add(shape_seg_U)
    boardObj.Add(shape_seg_R)
    boardObj.Add(shape_seg_D)
    # for bdITEM in shapeGroup.GetItems():#不支持迭代，，不知道怎么取出来
    #     print(bdITEM)
    #     boardObj.Add(bdITEM)
    boardObj.Add(shapeGroup)#这里如果不加就会导致操作pcbnew的时候其崩溃

    # a=shapeGroup.m_Uuid(id不是一个字符串，需要转换)
    # print(a)
    # print(shapeGroup.m_Uuid)
    # ----调试保存
    # pathpcb = boardObj.GetFileName()
    # boardObj.Save(pathpcb)
    # pcbnew.Refresh()
    # return shapeGroup

#添加圆形shape
# TODO：圆形的参数应该用直径还是半径？
def AddRoundShape(shape_radius,segmentWidth,x0,y0,chosenLayer,isFill=False,isLocked=False,boardObj=None):
    # boardObj = pcbnew.GetBoard()
    # shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments.SetShape(pcbnew.SHAPE_T_CIRCLE)#设置为圈.SetShape(pcbnew.S_ARC)

    # shape_segments.SetCenter(wxPoint(x0,y0))
    shape_segments.SetStart(wxPoint(x0,y0))
    # shape_segments.SetEnd(wxPoint(x0+shape_length,y0+shape_width))
    shape_segments.SetEnd(wxPoint(x0+shape_radius,y0))

    shape_segments.SetWidth(segmentWidth)#
    shape_segments.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    shape_segments.SetFilled(isFill)
    shape_segments.SetLocked(isLocked)
    
    # TODO :然后添加一个圆心，暂时搁置,圆边框本来就有圆心，没必要
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要这段也没事
    #     shape_segments.SetTimeStamp(ts)
    boardObj.Add(shape_segments)
# 这个还没做TODO,添加用openscad描述的自定义形状（不实用）
def AddScadShape(segmentWidth,chosenLayer):
    pass
# 参数分别是 起始点 终点到x的距离和到y的距离（不是终点坐标）
def AddDimensionToBoard(x0,y0,x1,y1,boardObj):
    # pcbnew.dim
    # (dimension (type aligned) (layer "Cmts.User") (tstamp 4fa95958-237b-45e5-ad3a-89f1d72d7b41)
    #     (pts (xy 118.134 47.423) (xy 118.134 89.344001))
    #     (height -6.961)
    #     (gr_text "41.9210 mm" (at 123.945 68.3835 90) (layer "Cmts.User") (tstamp 8b9758f8-d9b7-4a5e-ad84-56ff4f8c66f5)
    #       (effects (font (size 1 1) (thickness 0.15)))
    #     )
    #     (format (units 3) (units_format 1) (precision 4))
    #     (style (thickness 0.15) (arrow_length 1.27) (text_position_mode 0) (extension_height 0.58642) (extension_offset 0.5) keep_text_aligned)
    #   )
    #构建一个标注（dimension）
    x_end = x0+x1
    y_end = y0+y1
    dimensionObj = pcbnew.PCB_DIM_ALIGNED(boardObj)#PCB_DIM_CENTER是个十字，不知道具体会变成咋样，应该使用aligned才能正确显示标注
    dimensionObj.SetLayer(pcbnew.Cmts_User)
    dimensionObj.SetStart(wxPoint(x0,y0))#TODO:如果是圆角矩形需要进动一点（不改也行）
    dimensionObj.SetEnd(wxPoint(x_end,y_end))

    #设置标注文本--- TODO:这里的方法可能存在问题，需要修改,是用于临时解决不重新加载板子的情况下刷新出来注释的方法
    # dimensionObj.SetText('t')
    # dimensionObj.GetMeasuredValue()
    # dimensionObj.SetMeasuredValue(2*g_multiplier)
    # dimensionObj.SetText("test")
    dimText=dimensionObj.Text()
    # dimText.SetLayer
    dimText.SetText("Test")#能设置，但是只能设置一会儿
    
    #设置标注偏离测量点多远以及文本位置
    if x1==0:
        dimensionObj.SetHeight(int(4*g_multiplier))#向左边拓4mm，如果是圆角矩形进动了，要加上半径
        dimText.SetPosition(wxPoint(x0-8,y0))
    elif y1==0:
        dimensionObj.SetHeight(int(-4*g_multiplier))#向上边拓4mm
        dimText.SetPosition(wxPoint(x0,y0+8))
    #设置标注线format
    dimensionObj.SetUnits(pcbnew.EDA_UNITS_MILLIMETRES)#可以设置自动单位，但是拒绝英制
    dimensionObj.SetUnitsFormat(1)
    dimensionObj.SetPrecision(4)
    #设置标注style
    dimensionObj.SetLineThickness(int(0.15*g_multiplier))
    dimensionObj.SetArrowLength(int(1.27*g_multiplier))
    dimensionObj.SetTextPositionMode(pcbnew.DIM_TEXT_POSITION_INLINE)#0 
    dimensionObj.SetExtensionHeight(int(0.58642*g_multiplier))
    dimensionObj.SetExtensionOffset(int(0*g_multiplier))
    dimensionObj.SetKeepTextAligned(True)
    # dimensionObj.SetSelected()
    

    dimensionObj.SetForceVisible(True)
    dimensionObj.SetBrightened()
    # print(dimensionObj.GetUnits(pcbnew.EDA_UNITS_MILLIMETRES))#get为什么要参数。。
    # dimensionObj.SetAutoUnits()
    # dimensionObj.SetKeepTextAligned(True)
    # dimensionObj.SetUnitsFormat()
    # dimensionObj.SetUnitsMode()
    
    # dimensionObj.SetWireImage()
    # dimensionObj.SetText("test")#设置文字好像不起作用
    # print(dimensionObj.GetStatus())
    # dimensionObj.SetOverrideTextEnabled
    dimensionObj.SetTextPositionMode(pcbnew.DIM_TEXT_POSITION_INLINE)
    # dimensionObj.SetBrightened()
    boardObj.Add(dimensionObj)
# 自动找到合适板边框的参数并设置
def findNiceParams(boardobj):
    #加载板子：
    # boardobj = pcbnew.GetBoard()
    # boardobj = mLoadBoard()
    #原本是打算获取所有元素的几何中心和边界的，结果发现有包围盒可以直接用
    # board_X,board_Y = boardobj.GetCenter()
    # xmm = pcbnew.ToMM(board_X)
    # ymm = pcbnew.ToMM()
    # 获取所有元素的包围盒
    bbox = boardobj.ComputeBoundingBox()
    # 计算边框的大小和位置
    bdwidth = bbox.GetWidth()
    bdheight = bbox.GetHeight()
    bdx = bbox.GetX()
    bdy = bbox.GetY()
    centerX,centerY = bbox.GetCenter() #获取中心点
    return bdx,bdy,bdwidth,bdheight,centerX,centerY
# class BoardOperation():

class Dialog(wx.Dialog):
    chsize = (10,20)#这个最好改掉，不能放到init里面，会失效
    # Borderop = BoardOperation()
    # Borderop.onClickConfirmBtn()
    def __init__(self, parent):
        # 用来调整布局的
        #InitEm 函数首先定义了一个全局变量 chsize，
        # 并将其初始化为 (10,20)。
        # 然后它创建一个 wx.ScreenDC 对象，
        # 这个对象可以用来在屏幕上绘图。
        # 接着，它创建一个字体对象，
        # 并将这个字体设置到 wx.ScreenDC 对象上
        def InitEm():
            global chsize
            dc=wx.ScreenDC()
            font=wx.Font(pointSize=10,family=wx.DEFAULT,style=wx.NORMAL,weight=wx.NORMAL)
            dc.SetFont(font)
            # 获取 "M" 这个字符的宽和高
            tx=dc.GetTextExtent("M")
            # 将 chsize 全局变量的值
            #设置为字符宽度和高度的 1.5 倍。
            chsize=(tx[0]*1.1,tx[1]*1.5)
        def Em(x,y,dx=0,dy=0):
            return (chsize[0]*x+dx, chsize[1]*y+dy)

        #-----------------------设定窗口信息------------------
        InitEm()
        funcName =      '外形生成'#illet board edges
        version  =      'v0.15'
        shapeRboxLable = '外形类型'
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') #图标
        # self.manufacturers_dir = os.path.join(os.path.dirname(__file__), 'Manufacturers')
        wx.Dialog.__init__(self, parent, id=-1, 
                            title=funcName+version, 
                            size=Em(44,14),
                            style=wx.DEFAULT_DIALOG_STYLE 
                            | wx.RESIZE_BORDER
                            | wx.DIALOG_NO_PARENT
                            # | wx.FRAME_EX_CONTEXTHELP
                            )

        # self.Bind(wx.EVT_CLOSE, self.OnClose, id=self.GetId())
        icon=wx.Icon(self.icon_file_name)
        self.SetIcon(icon)#显示Logo图标
        # self.BoxSizer = wx.BoxSizer(self)
        # #TODO:设计器里面的流程是先加一个sizer？回头看看文档,似乎加不加没影响
        bSizer_1 = wx.BoxSizer( wx.VERTICAL )
        self.panel = wx.Panel(self) #添加一个panel容纳元素 
        # self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )

        # --------------根据板子信息自动初始化一些数据--TODO:这里后面写----
        #边框中心位置（或者左上角）边框默认大小
        center_posX = 0
        center_posY = 0
        X_length = 100
        Y_length = 100
        R_value = 5
        #-------------下面是UI部分---------------------
        # wx.StaticText(self.panel, wx.ID_ANY, getstr('LABEL'), size=Em(70,1), pos=Em(1,1))
        # wx.StaticText(self.panel, wx.ID_ANY, getstr('MENUFACTURERS'),size=Em(14,1), pos=Em(1,2.5))
        # wx.StaticText(self.panel, wx.ID_ANY, getstr('MENUFACTURERS'),size=Em(14,1), pos=Em(1,2.5))
        #if in chinese,四个选项包含
        shapeList = ['矩形', '圆角矩形', '圆形','多边形导入'] 
        shapeList = ['矩形', '圆角矩形', '圆形','脚本生成']#ScriptEdit
        self.theShapeSelection = 0
        self.lineWidth = 0.254 # mm 
        # self.lineWidth = 0.1 #mm
        self.theLayer = pcbnew.Edge_Cuts
        #TODO 这里是几个默认参数，确认不需要的话可以删掉
        self.shapeRbox = wx.RadioBox(self.panel,  wx.ID_ANY, label = shapeRboxLable ,pos=Em(1,1), choices = shapeList,
            majorDimension = 1, style = wx.RA_SPECIFY_ROWS) 
                # self.panel.o

        # 板框类型选择radioBox， 绑定函数onSelectShape
        self.shapeRbox.SetSelection(self.theShapeSelection)#默认选择矩形
        self.shapeRbox.Bind(wx.EVT_RADIOBOX,self.onSelectShape)#绑定动作到onSeletShape函数
        #(self, parent, id=ID_ANY, value=EmptyString, pos=DefaultPosition, size=DefaultSize, style=0, validator=DefaultValidator, name=TextCtrlNameStr 

        # ---输入数据单位可选，同时读取板设置自动选择mm mil
        #X坐标输入框
        self.PosX_Input = wx.TextCtrl(self.panel,wx.ID_ANY,value=str(center_posX),pos=Em(2+2,5),size=Em(8,1),name='x')
        #Y坐标输入框
        self.PosY_Input = wx.TextCtrl(self.panel,wx.ID_ANY,value=str(center_posY),pos=Em(14+2,5),size=Em(8,1),name='y')

        #X长度输入框
        #圆形的半径直接取上面的X
        self.length_Input = wx.TextCtrl(self.panel,wx.ID_ANY,value=str(X_length),pos=Em(2+2,7),size=Em(8,1),name='xl')
        #宽度输入框Y
        self.width_Input = wx.TextCtrl(self.panel,wx.ID_ANY,value=str(Y_length),pos=Em(14+2,7),size=Em(8,1),name='yl')
        # 圆角半径生成参数
        self.angleRadius_Input = wx.TextCtrl(self.panel,wx.ID_ANY,value=str(R_value),pos=Em(2+2,9),size=Em(8,1),name='rvalue')
        # alert('select:%d'%self.shapeRbox.GetSelection())
        # ----------文本----------
        # X坐标和Y坐标文本
        xytxt = '位置坐标'
        self.Xytext = wx.StaticText(self.panel, wx.ID_ANY, label=xytxt, pos=Em(2,4))#, size, style)
        xtxt = "X:"
        self.Xtext = wx.StaticText(self.panel, wx.ID_ANY, label=xtxt, pos=Em(2,5))#, size, style)
        ytxt = "Y:"
        self.Ytext = wx.StaticText(self.panel, wx.ID_ANY, label=ytxt, pos=Em(14,5))#, size, style)

        # 参数文本
        sizetxt = '尺寸'
        self.Sizetext = wx.StaticText(self.panel, wx.ID_ANY, label=sizetxt, pos=Em(2,6))#, size, style)
        xtxt = "XL"
        self.Xtext = wx.StaticText(self.panel, wx.ID_ANY, label=xtxt, pos=Em(2,7))#, size, style)
        Rtxt = "R:"
        self.Rtext = wx.StaticText(self.panel, wx.ID_ANY, label=Rtxt, pos=Em(2,7))#, size, style)
        ytxt = "YL"
        self.Ytext = wx.StaticText(self.panel, wx.ID_ANY, label=ytxt, pos=Em(14,7))#, size, style)
            # 圆角矩形的圆角大小
        # sizetxt = '半径'
        # self.Sizetext = wx.StaticText(self.panel, wx.ID_ANY, label=sizetxt, pos=Em(2,6))#, size, style)
        r_angle_txt = "R:"
        self.R_angle_text = wx.StaticText(self.panel, wx.ID_ANY, label=r_angle_txt, pos=Em(2,9))#, size, style)
        
        #-------需要默认隐藏的项目
        self.Rtext.Hide()
        self.R_angle_text.Hide()
        self.angleRadius_Input.Hide()

        # ---------按钮----------
        confirmText = '应用'
        self.confirmBtn = wx.Button(self.panel,wx.ID_ANY,label=confirmText,pos=Em(16,10))#,size=DefaultSize)
        self.confirmBtn.Bind(wx.EVT_BUTTON,self.onClickConfirmBtn)

        testText = '刷新PCB'
        self.confirmBtn = wx.Button(self.panel,wx.ID_ANY,label=testText,pos=Em(28,10))#,size=DefaultSize)
        self.confirmBtn.Bind(wx.EVT_BUTTON,self.onClickTestBtn)

        autoSetText = '自动设置参数'
        self.autoSetBtn = wx.Button(self.panel,wx.ID_ANY,label=autoSetText,pos=Em(2,10))#,size=DefaultSize)
        self.autoSetBtn.Bind(wx.EVT_BUTTON,self.autoSetNiceParams)
        # testText = 'ScriptEdit'
        # self.confirmBtn = wx.Button(self.panel,wx.ID_ANY,label=testText,pos=Em(16,11))#,size=DefaultSize)
        # self.confirmBtn.Bind(wx.EVT_BUTTON,self.onClickTestBtn)

        # ---------combobox----------
        self.layerCombBoxChoices = []
        # print(pcbnew.PCB_LAYER_ID_COUNT)
        
        # for i in range(pcbnew.PCB_LAYER_ID_COUNT):
        #     # print(pcbnew.LayerName(i))#获取所有的层的名称
        #     layer_colors = {}

        # for layer_id in range(pcbnew.LAYER_ID_COUNT):
        #     layer = board.GetLayer(layer_id)
        #     color = layer.GetColor()
        #     layer_colors[layer.GetName()] = color

        # for i in range(pcbnew.PCB_LAYER_ID_COUNT):
        #     print(pcbnew.current (i))
        # for layer in pcbnew.GetBoard().getLay
                # self._layer_choices = layer_choices = ["F.Cu", "F.Paste", "F.SilkS", "F.Mask", "F.Cu/F.Mask"]
        # self.m_LayerComboBox.AppendItems(layer_choices)
        # self.m_LayerComboBox.SetSelection(0)
        # ComboBox(parent, id=ID_ANY, value=EmptyString, pos=DefaultPosition, size=DefaultSize, choices=[], style=0, validator=DefaultValidator, name=ComboBoxNameStr)
        self.layerCombBox = wx.ComboBox( self.panel, wx.ID_ANY, 
                                u"",
                                pos=Em(14+14,5), 
                                size=Em(14,1), 
                                # choices=self.layerCombBoxChoices, 
                                style=0 )
        bSizer_1.Add( self.layerCombBox, 0, wx.ALL, 5 )
        #不需要为layercombobox绑定什么，点确定的时候获取就行了。
        # self.layerCombBox.Bind(wx.EVT_COMBOBOX)
        # self.layerCombBox.Dismiss()
        # self.layerCombBox = wx.ComboBox(self, choices=["Option 1", "Option 2", "Option 3"])
        # # Add the combobox to the dialog
        # self.sizer = wx.BoxSizer(wx.VERTICAL)
        # self.sizer.Add(self.layerCombBox, 0, wx.ALL, 5)
        # self.SetSizer(self.sizer)

        
        # Create the menu创建右键菜单
        self.rightMenu = wx.Menu()

        self.rightMenuItem0 = wx.MenuItem( 
                            self.rightMenu, 
                            wx.ID_ANY, 
                            u"打开设置",
                            wx.EmptyString, wx.ITEM_NORMAL )
        self.rightMenu.Append( self.rightMenuItem0 )
        # self.rightMenuItemAutoSet = wx.MenuItem( 
        #             self.rightMenu, 
        #             wx.ID_ANY, 
        #             u"自动设置参数",
        #             wx.EmptyString, wx.ITEM_NORMAL)
        #添加一个分割，和上面的设置分开
        self.rightMenu.AppendSeparator()
        self.rightMenu.Append(wx.ID_REFRESH, "刷新PCB")# 右键刷新pcb
        self.rightMenu.Append(wx.ID_ANY, "TODO2")
        # self.rightMenu.Append(self.rightMenuItemAutoSet)#点击自动设置参数 
        # TODO:自动设置参数应该放到界面上才方便使用，这里就先不做了
        #添加一个分割 后面是checkitem
        self.rightMenu.AppendSeparator()
        self.rightMenu.AppendCheckItem(wx.ID_ANY, "TODO3")
        #添加一个分割 后面是radioitem
        self.rightMenu.AppendSeparator()
        self.rightMenu.AppendRadioItem(wx.ID_ANY, "TODO2")
        self.rightMenu.AppendRadioItem(wx.ID_ANY, "TODO2")
        #添加一个分割 后面是submenu
        self.rightMenu.AppendSeparator()
        self.submenu = wx.Menu()
        self.rightMenu.AppendSubMenu(self.submenu, "TODO2")
        # Append(id, item=EmptyString, helpString=EmptyString, kind=ITEM_NORMAL)
        # AppendCheckItem(self, id, item, help=EmptyString):
        # AppendRadioItem(self, id, item, help=EmptyString):
        # AppendSubMenu(self, submenu, text, help=EmptyString):

        #把绑定右键事件到panel上
        self.panel.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        # Bind the menu items to actions绑定菜单里的选项
        self.Bind(wx.EVT_MENU, self.OpenSetting, id=self.rightMenuItem0.GetId())
        self.Bind(wx.EVT_MENU, self.onClickTestBtn, id=wx.ID_REFRESH)#绑定到刷新PCB上

#--------------------根据板参数刷新ui上的选项--------------------
        #TODO:初始化界面里面不应该加载pcb，先凑合用，后面再改出去界面初始化加载和pcb加载分开
        # boardobj = pcbnew.GetBoard()
        boardobj = mLoadBoard()
        #------调试加载板子用------------TODO:debug here
        # pcbfile = r'C:\Users\Always\Desktop\dd\dd.kicad_pcb'#没有特殊需求可以随便找一个pcb，直接放工程目录下也行
        # boardobj=pcbnew.LoadBoard(pcbfile)
        
        enabledLayerSet = boardobj.GetEnabledLayers()
        enabledLayers = enabledLayerSet.Seq()#使用seq方法获取layerset的对应的id的list
        self.layerIDlist = []#用来同时存放读出来的id
        #除了最后10个，也就是用户定义层，当前pcb有的层全部加入combobox TODO:是否所有工程都有最后10层用户层和resue？不过问题不大，先不管
        for theLayerID in enabledLayers[:-10]:
            # print(pcbnew.LayerName(theLayerID))
            self.layerCombBoxChoices.append(pcbnew.LayerName(theLayerID))#把名称加到choice里面
            self.layerIDlist.append(theLayerID)

        self.layerDict=dict(zip(self.layerIDlist,self.layerCombBoxChoices))#打包成字典方便后面用

        #因为主要是画边框，所以首先定位到边框选项
        self.layerCombBox.AppendItems(self.layerCombBoxChoices)
        self.layerCombBox.SetSelection(self.layerCombBoxChoices.index('Edge.Cuts'))
        # TODO :这里添加选项之后没有和kicad里面一样的颜色指示，
        # 怎么获取添加颜色？chatgpt也不能给出方案，在kicad文档里面也没找到合适的color相关内容
        # TODO :最好是默认去掉一般用不上的层，太长一串看着烦。。比如说最后10层都是用户定义层（反正加了之后自己可以改）
    
    #点确认之后应用板框，添加到板子上
    def onClickConfirmBtn(self,event):
        # (gr_rect (start 215.9 60.96) (end 228.6 71.12) (layer "Edge.Cuts") (width 0.2) (fill none) (tstamp 1799c71f-013d-402a-b710-c5585561a246))
        # (gr_line (start 196.85 53.34) (end 229.87 53.34) (layer "Edge.Cuts") (width 0.2) (tstamp cf625e85-a2c0-4557-8b5f-dc6b2e43c20d))
        # self.boardObj = pcbnew.GetBoard()
        self.boardobj = mLoadBoard()
        # print(self.layerCombBox.GetStringSelection())
        # self.theLayer = 1
        #获取层索引来写道指定层上
        layerindex=self.layerCombBoxChoices.index(self.layerCombBox.GetStringSelection())
        self.theLayer = self.layerIDlist[layerindex]
        
        # pcbShape = pcbnew.PCB_SHAPE(self.boardobj)
        x0=float(self.PosX_Input.GetValue())*g_multiplier
        y0=float(self.PosY_Input.GetValue())*g_multiplier
        linewidth = int(float(g_multiplier)*self.lineWidth)#linewidth只接受整数
        # alert('edge:%d'%self.theShapeSelection)
        if(self.theShapeSelection == 0):
            x1=float(self.length_Input.GetValue())*g_multiplier
            y1=float(self.width_Input.GetValue())*g_multiplier
            # alert('anything')
            # alert('edge:%s'%type(self.lineWidth))
            AddRectShape(x1,y1,linewidth,x0,y0,self.theLayer,self.boardobj)
        elif self.theShapeSelection == 1:
            x1=float(self.length_Input.GetValue())*g_multiplier
            y1=float(self.width_Input.GetValue())*g_multiplier
            ra = float(self.angleRadius_Input.GetValue())*g_multiplier
            AddRoundRectShape(x1,y1,ra,linewidth,x0,y0,self.theLayer,self.boardobj)
            # self.boardobj.Add(SHgroup)#不起作用
        elif self.theShapeSelection == 2:
            r_circle=float(self.length_Input.GetValue())*g_multiplier
            AddRoundShape(r_circle,linewidth,x0,y0,self.theLayer,boardObj=self.boardobj)
            #添加一个圆心标记用来方便自动对齐
            AddRoundShape(1,linewidth,x0,y0,pcbnew.Cmts_User,isFill=True,isLocked=False,boardObj=self.boardobj)
            # pass
        elif self.theShapeSelection == 3:
            pass
        elif self.theShapeSelection == 4:
            pass
        else:
            event.Skip()
        if(True):#预留的条件TODO:后面增加可选，（不一定做）
            if (self.theShapeSelection == 0):
                #在板子上为边框添加测量长宽的注释：
                #纵向注释 
                AddDimensionToBoard(x0,y0,0,y1,self.boardobj)
                #横向注释
                AddDimensionToBoard(x0,y0,x1,0,self.boardobj)
            elif (self.theShapeSelection == 1):
                #在板子上为边框添加测量长宽的注释：
                #纵向注释 
                AddDimensionToBoard(x0,y0,0,y1,self.boardobj)
                #横向注释
                AddDimensionToBoard(x0,y0,x1,0,self.boardobj)
            elif (self.theShapeSelection == 2):
                #在板子上为边框添加测量长宽的注释：
                #纵向注释  圆不需要
                # AddDimensionToBoard(x0,y0,0,y1,self.boardobj)
                #横向注释
                AddDimensionToBoard(x0,y0,r_circle,0,self.boardobj)
                #TODO:现在标注的是半径，是否改成直径？
            else:
                pass
        # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
        #     shape_segments.SetTimeStamp(ts)
        #调试用-----debug TODO-----
        # pcbfile = r'C:\Users\Always\Desktop\dd\dd.kicad_pcb'
        # self.boardobj.Save(pcbfile)

        # ----最后刷新PCB------
        pcbnew.Refresh()
        
        # self.EndModal()
    # onSelectShape：点击不同外形设置的时候切换界面
    def onSelectShape(self,event):
        obj = event.GetEventObject()
        self.theShapeSelection = obj.GetSelection()
        # alert('select:%d'%self.shapeRbox.GetSelection())
        self.showShapeSetInterface(self.theShapeSelection)
        # #分别是0 1 2 3
        # if(self.theShapeSelection==0):
        #     # alert('select:%d'%self.shapeRbox.GetSelection())
        # else:
        #     event.Skip()
    # showShapeSetInterface：根据不同的选择外形类型，显示不同的界面来输入参数
    def showShapeSetInterface(self,shapeKind):
        # alert('select:%d'%self.shapeRbox.GetSelection())
        if(shapeKind==0):
            # alert('select:%d'%self.shapeRbox.GetSelection())
            #set Value
            # self.length_Input.SetValue(str(100))
            #show
            self.Xtext.Show()
            self.Ytext.Show()
            self.width_Input.Show()
            #Hide
            self.R_angle_text.Hide()
            self.Rtext.Hide()
            self.angleRadius_Input.Hide()
            # 显示矩形长宽，左上角位置的填写框
        elif shapeKind==1:
            
            #set Value
            # self.length_Input.SetValue(str(100)) #TODO:需要判断是否使用了自动适配参数，或者直接判断之前是不是100或者圆的50，使用了就不变，否则直接切回去看起来不舒服
            #show
            self.Xtext.Show()
            self.Ytext.Show()
            self.R_angle_text.Show()
            self.angleRadius_Input.Show()
            self.width_Input.Show()
            # Hide
            self.Rtext.Hide()
            # pass
            # 显示圆角矩形长宽，左上角位置，圆角半径
        elif shapeKind==2:
            # 显示圆弧半径，圆心x 圆心 y
            # 直接和矩形框的填写复用吧，改一下显示的条目就行
            # self.R_angle_text.Show()
            # self.length_Input.SetValue(str(50))
            self.Rtext.Show()
            # Hide
            self.R_angle_text.Hide()
            self.Xtext.Hide()
            self.Ytext.Hide()
            self.width_Input.Hide()
            self.angleRadius_Input.Hide()
            # pass
        elif shapeKind==3:
            # 显示脚本编辑框
            # Hide
            self.R_angle_text.Hide()
            self.Xtext.Hide()
            self.Ytext.Hide()
            self.width_Input.Hide()
            self.angleRadius_Input.Hide()
            self.Rtext.Show()
            pass
        else:
            pass
            # event.Skip()
    #   onClickTestBtn：现在叫做刷新显示按键，实现刷新重新装载pcb文件（从文件而不是缓存）
    def onClickTestBtn(self,event):
        # TODO:需要修改
        # alert("刷新")
        
        pcbnew.Refresh()
        #下面方法不确定有没有效果,测试是并不能从文件中重新加载，同时下面这一坨可能会导致pcb添加组的时候
        # 保存的时候崩溃。虽然引用的地方都是按键，但是就是这么奇妙，我好像也就修改了这里修好这个问题的。。。
        # Get the current PCB
        # pcb = pcbnew.GetBoard()
        # # Get the file path of the PCB
        # pcbpath = pcb.GetFileName()
        # # Load the PCB from the file
        # pcb=pcbnew.LoadBoard(pcbpath)#
        # pcb.Save(pcbpath)
        # pcbnew.LoadBoard(pcbpath)#
        # # pcbnew.
        # pcbnew.Refresh()
    # OnRightDown：绑定右键菜单
    def OnRightDown( self, event ):
        self.PopupMenu( self.rightMenu, event.GetPosition())
    #     self.PopupMenu(self.menu)
        # alert(self.rightMenuItem0.GetId())
    def OpenSetting(self, event):
        event.Skip()
        # alert("Testing")
        
        dlg = mSetting.MyDialog(self)
        dlg.ShowModal()
        dlg.Destroy()
    #     event.Skip()
    def autoSetNiceParams(self,event):
        # event.Skip()
        # 加载板子：
        # boardobj = pcbnew.GetBoard()
        boardobj = mLoadBoard()
        bdx,bdy,bdwidth,bdheight,centerX,centerY = findNiceParams(boardobj)
        # 创建边框对象
        # border = pcbnew.EDGE_MODULE(board)
        # border.SetWidth(pcbnew.FromMM(2))  # 设置边框线宽为 2 mm
        # border.SetLayer(pcbnew.F_SilkS)  # 设置边框在 F.SilkS 层

        # 设置边框的大小和位置
        # border.SetStart(pcbnew.wxPoint(x, y))
        # border.SetEnd(pcbnew.wxPoint(x + width, y + height))
        # 将边框添加到 PCB 上
        # board.Add(border)
        # print(pcbnew.ToMM(bdx))
        #获取当前选的边缘类型
        self.theShapeSelection = self.shapeRbox.GetSelection()
        if (self.theShapeSelection == 0 or self.theShapeSelection==1):
            # 圆角矩形和矩形的参数共用一套，不过 TODO:圆角矩形最好加个判断圆角内会不会有器件落入进入
            self.PosX_Input.SetValue(str(pcbnew.ToMM(bdx)))
            self.PosY_Input.SetValue(str(pcbnew.ToMM(bdy)))
            self.length_Input.SetValue(str(pcbnew.ToMM(bdwidth)))
            self.width_Input.SetValue(str(pcbnew.ToMM(bdheight)))
        elif self.theShapeSelection==2:
            #设置半径：
            r_circle = 0.5*sqrt(pcbnew.ToMM(bdwidth)**2+pcbnew.ToMM(bdheight)**2)
            self.length_Input.SetValue(str(r_circle))
            self.width_Input.SetValue(str(r_circle))
            #设置圆心
            # centerX = pcbnew.ToMM(bdx+0.5*bdwidth)
            self.PosX_Input.SetValue(str(pcbnew.ToMM(centerX)))
            self.PosY_Input.SetValue(str(pcbnew.ToMM(centerY)))
            # r_circle=float(self.length_Input.GetValue())*g_multiplier
            # AddRoundShape(r_circle,linewidth,x0,y0,self.theLayer,boardObj=self.boardobj)
            #圆的参数单独获取，因为圆是从圆心出发的，直径应该是刚刚获取的包围框的长宽平方和开根号，
            # 不过圆心坐标可以用center获取吧。
        elif self.theShapeSelection==3:
            pass
        else:
            event.Skip()
    def onLayerChoseChanged(self, event):
        pass
    #TODO:保留给其他的右键菜单按钮或者神
    def todo(self, event):
        pass

# 插件入口
class Add_Shapes(pcbnew.ActionPlugin):
    # global g_multiplier
    def defaults(self):
        self.name = "添加板框"
        self.category = "形状编辑" #？这写啥
        self.description = "参数化添加常用板框形状或者其他层的形状"
        self.show_toolbar_button = True # 可选，默认为 False(在插件bar上显示出来)
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # 可选
    def Run(self):
        # 在用户操作时执行的插件的入口函数
        # wx.TextEntryDialog(None,message="Enter Number of Layers to Skip")
        # 窗体启动入口
        pcbnew.Refresh()                        #Anyway,fresh the pcb first.
        try:
            mydialog = Dialog(None)
            mydialog.Center()
            mydialog.Show()#是否存在内存问题，答曰：不存在这个问题，见下面解释
            # 如果您在编写插件时，将所有的对话框代码都放在脚本文件的全局作用域中，则当您关闭插件时，所有的对话框都会被销毁。这是因为，当插件被关闭时，KiCad会卸载该插件，并释放其占用的内存空间。
        except:
            mydialog.Destroy()
            print("dead")
        # finally:
        #     pass
        # dialog.ShowModal()#使用模式显示会导致kicad回显已经删除的边框的bug
        # dialog.Destroy()
        # with Dialog(None) as myDialog:
        #     if myDialog.ShowModal() == wx.ID_OK:
        #     # do something here
        #         print('good')
        #     else:
        #         print('deaad')