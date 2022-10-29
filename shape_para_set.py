# from cProfile import label
import pcbnew
import os
import wx
from pcbnew import *

#this plugin is deved for KiCad 6.0.x 只适配了kicad6的api

#TODO list：


#1：根据屏幕像素自适应像素大小 TODO:调整布局方式
# TODO：添加之后的边框添加尺寸标注
# TODO:1 单位可选择 
# TODO:自动选择一组合适的大小和位置用来初始化板子参数（模仿jlc，但是他那个做的不好）
# TODO :让添加的层可选
# TODO: 增加选项，添加边框的时候删除原来的边框
# TODO:添加更多选型，用来实现1可以填充为实心图形，2修改线宽 （线宽也放在高级编辑里面
# TODO:添加正多边形的添加
# TODO： 添加预览界面
# TODO：添加高级选项功能
# TODO :添加功能配置记录，用来存放配置和用来每次打开的时候读取上一次保存的记录
#3 等后面复选框没有bug了在看看文档层能不能吸附圆心 更新：这里确认了圆心基本不能自动吸附在不对其网格的点上，功能本来就是为了摆放安装孔方便，所以这个功能暂时不做了
# 0 语言忘差不多了，写法得看看了
#2 todo:添加脚本功能类似openscad编辑边框形状
# 分段的边框添加到一个组里面避免移动困难（可选）
# 圆心标记功能添加到高级里面可以取消

## 
UNITS = ["mm", "in"]
multiplier = 1000000#KiCad中数字的单位是10^-6 mm
#
def alert(s, icon=0):
    wx.MessageBox(s, 'xxxtitle', wx.OK|icon)

chsize = (10,20)#这个最好改掉
def InitEm():
    global chsize
    dc=wx.ScreenDC()
    font=wx.Font(pointSize=10,family=wx.DEFAULT,style=wx.NORMAL,weight=wx.NORMAL)
    dc.SetFont(font)
    tx=dc.GetTextExtent("M")
    chsize=(tx[0],tx[1]*1.5)

def Em(x,y,dx=0,dy=0):
    return (chsize[0]*x+dx, chsize[1]*y+dy)

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
def AddRectShape(shape_length,shape_width,segmentWidth,x0,y0,chosenLayer):
    boardObj = pcbnew.GetBoard()
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
# #TODO:需要用丝印或者什么元素标记圆角中心点方便手动添加安装孔TODO:这里多段添加的写法是不是有点问题
def AddRoundRectShape(shape_length,shape_width,shape_ra,segmentWidth,x0,y0,chosenLayer):
    boardObj = pcbnew.GetBoard()
    # shape_segments = pcbnew.PCB_SHAPE(boardObj)

    # 左上角的圆角 TODO:不知道为啥这里改了PCBshape的变量名就会有问题，以后再说  
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
    boardObj.Add(shape_segments)            
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
    boardObj.Add(arc_ur)
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
    boardObj.Add(arc_dr)

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
    boardObj.Add(arc_dl)    

    # 左侧线段
    shape_seg_L = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_L.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    # 
    shape_seg_L.SetStart(wxPoint(x0,y0+shape_ra))
    shape_seg_L.SetEnd(wxPoint(x0,y0+shape_width-shape_ra))

    shape_seg_L.SetWidth(segmentWidth)#250000
    shape_seg_L.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    boardObj.Add(shape_seg_L)
    # 上方线段
    shape_seg_U = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_U.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_U.SetStart(wxPoint(x0+shape_ra,y0))
    shape_seg_U.SetEnd(wxPoint(x0+shape_length-shape_ra,y0))

    shape_seg_U.SetWidth(segmentWidth)#250000
    shape_seg_U.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    boardObj.Add(shape_seg_U)
    # 右侧线段
    shape_seg_R = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_R.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_R.SetStart(wxPoint(x0+shape_length,y0+shape_ra))
    shape_seg_R.SetEnd(wxPoint(x0+shape_length,y0+shape_width-shape_ra))

    shape_seg_R.SetWidth(segmentWidth)#250000
    shape_seg_R.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    boardObj.Add(shape_seg_R)
    # 下侧线段
    shape_seg_D = pcbnew.PCB_SHAPE(boardObj)
    shape_seg_D.SetShape(pcbnew.SHAPE_T_SEGMENT)#设置为线段
    shape_seg_D.SetStart(wxPoint(x0+shape_ra,y0+shape_width))
    shape_seg_D.SetEnd(wxPoint(x0+shape_length-shape_ra,y0+shape_width))

    shape_seg_D.SetWidth(segmentWidth)#250000
    shape_seg_D.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    boardObj.Add(shape_seg_D)
    #继承 EDA_SHAPE的属性可以添加圆弧和贝塞尔曲线       
    # 添加用户注释层圆角的圆心：
    AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False)
    AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False)
    AddRoundShape(1,250000*2,x0+shape_length-shape_ra,y0+shape_width-shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False)
    AddRoundShape(1,250000*2,x0+shape_ra,y0+shape_width-shape_ra,pcbnew.Cmts_User,isFill=True,isLocked=False)
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
#添加圆形
def AddRoundShape(shape_radius,segmentWidth,x0,y0,chosenLayer,isFill=False,isLocked=False):
    boardObj = pcbnew.GetBoard()
    # shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments = pcbnew.PCB_SHAPE(boardObj)
    shape_segments.SetShape(pcbnew.SHAPE_T_CIRCLE)#设置为圈.SetShape(pcbnew.S_ARC)

    # shape_segments.SetCenter(wxPoint(x0,y0))
    shape_segments.SetStart(wxPoint(x0,y0))
    # shape_segments.SetEnd(wxPoint(x0+shape_length,y0+shape_width))
    shape_segments.SetEnd(wxPoint(x0+shape_radius,y0))

    shape_segments.SetWidth(segmentWidth)#250000
    shape_segments.SetLayer(chosenLayer)#PCBNEW_LAYER_ID_START 
    shape_segments.SetFilled(isFill)
    shape_segments.SetLocked(isLocked)
    
    # TODO :然后添加一个圆心
    # if hasattr(shape_segments,'SetTimeStamp'):   #不要也没事
    #     shape_segments.SetTimeStamp(ts)
    boardObj.Add(shape_segments)
def AddScadShape(segmentWidth,chosenLayer):
    pass
class Add_Shapes(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = "添加板框"
        self.category = "形状编辑" #？这写啥
        self.description = "参数化添加常用板框形状或者其他层的形状"
        self.show_toolbar_button = True # 可选，默认为 False
        self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') # 可选

    def Run(self):
        # 在用户操作时执行的插件的入口函数
        # print("Hello World")
        # wx.TextEntryDialog(None,message="Enter Number of Layers to Skip")
        class Dialog(wx.Dialog):
            def __init__(self, parent):
                #-----------------------设定窗口信息------------------
                InitEm()
                funcName = '外型设置'
                version='v0.1'
                shapeRboxLable = '外型类型'
                self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png') #图标
                # self.manufacturers_dir = os.path.join(os.path.dirname(__file__), 'Manufacturers')
                wx.Dialog.__init__(self, parent, id=-1, title=funcName+version, size=Em(44,14),
                                   style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
                # wx.Dialog.__init__(
                #     self, parent, title=f'Fillet board edges',
                #     style=(wx.DEFAULT_DIALOG_STYLE | wx.DIALOG_NO_PARENT))
                # self.Bind(wx.EVT_CLOSE, self.OnClose, id=self.GetId())
                icon=wx.Icon(self.icon_file_name)
                self.SetIcon(icon)#显示Logo图标
                self.panel = wx.Panel(self) #添加一个panel容纳元素 
                # TODO:似乎dialog并不需要添加panel？

                
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
                self.theLayer = pcbnew.Edge_Cuts
                self.shapeRbox = wx.RadioBox(self.panel,  wx.ID_ANY, label = shapeRboxLable ,pos=Em(1,1), choices = shapeList,
                    majorDimension = 1, style = wx.RA_SPECIFY_ROWS) 
                    

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

                testText = '刷新显示'
                self.confirmBtn = wx.Button(self.panel,wx.ID_ANY,label=testText,pos=Em(28,10))#,size=DefaultSize)
                self.confirmBtn.Bind(wx.EVT_BUTTON,self.onClickTestBtn)

                # testText = 'ScriptEdit'
                # self.confirmBtn = wx.Button(self.panel,wx.ID_ANY,label=testText,pos=Em(16,11))#,size=DefaultSize)
                # self.confirmBtn.Bind(wx.EVT_BUTTON,self.onClickTestBtn)

                # 选择边框类型 设置边框大小（圆角大小）（是否添加四角固定孔封装），删除原来的闭合边框（），自动判断坐标（手动设定左上角或者中心坐标）|一键导入外部DXF 一键导入其他pcb文件板框，支持openscad多边形语法
            def showShapeSetInterface(self,shapeKind):
                # alert('select:%d'%self.shapeRbox.GetSelection())
                if(shapeKind==0):
                    # alert('select:%d'%self.shapeRbox.GetSelection())
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
            def onSelectShape(self,event):
                obj = event.GetEventObject()
                self.theShapeSelection = obj.GetSelection()
                # alert('select:%d'%self.shapeRbox.GetSelection())
                self.showShapeSetInterface(self.theShapeSelection)
                #分别是0 1 2 3
                if(self.theShapeSelection==0):
                    # alert('select:%d'%self.shapeRbox.GetSelection())
                    pass
                elif self.theShapeSelection==1:
                    pass
                elif self.theShapeSelection==2:
                    pass
                elif self.theShapeSelection==3:
                    pass
                else:
                    event.Skip()
            def onClickConfirmBtn(self,event):
                #应用板框画到板子上
                # (gr_rect (start 215.9 60.96) (end 228.6 71.12) (layer "Edge.Cuts") (width 0.2) (fill none) (tstamp 1799c71f-013d-402a-b710-c5585561a246))
                # (gr_line (start 196.85 53.34) (end 229.87 53.34) (layer "Edge.Cuts") (width 0.2) (tstamp cf625e85-a2c0-4557-8b5f-dc6b2e43c20d))
                self.boardObj = pcbnew.GetBoard()
                # pcbShape = pcbnew.PCB_SHAPE(self.boardObj)

                x0=float(self.PosX_Input.GetValue())*multiplier
                y0=float(self.PosY_Input.GetValue())*multiplier
                linewidth = 250000
                # alert('edge:%d'%self.theShapeSelection)
                if(self.theShapeSelection == 0):
                    x1=float(self.length_Input.GetValue())*multiplier
                    y1=float(self.width_Input.GetValue())*multiplier
                    # linewidth = float(multiplier)*self.lineWidth#TODO:不知道为什么这样会算不出来宽度，也没报错就运行不了      
                    # alert('anything')
                    # alert('edge:%s'%type(self.lineWidth))
                    AddRectShape(x1,y1,linewidth,x0,y0,self.theLayer)
                elif self.theShapeSelection == 1:
                    x1=float(self.length_Input.GetValue())*multiplier
                    y1=float(self.width_Input.GetValue())*multiplier
                    ra = float(self.angleRadius_Input.GetValue())*multiplier
                    AddRoundRectShape(x1,y1,ra,linewidth,x0,y0,self.theLayer)
                elif self.theShapeSelection == 2:
                    r_circle=float(self.length_Input.GetValue())*multiplier
                    AddRoundShape(r_circle,linewidth,x0,y0,self.theLayer)
                    AddRoundShape(1,linewidth,x0,y0,pcbnew.Cmts_User,isFill=True,isLocked=False)#添加一个圆心标记
                    # pass
                elif self.theShapeSelection == 3:

                    pass
                elif self.theShapeSelection == 4:
                    pass
                else:
                    event.Skip()

                pcbnew.Refresh()
                # self.EndModal()
                # 这样添加有个bug。。。不知道为什么删除之后会仍然显示但是刷新PCB就没有了 #大概是kicad的bug
            def onClickTestBtn(self,event):
                pcbnew.Refresh()

        dialog = Dialog(None)
        dialog.Center()
        dialog.ShowModal()
        dialog.Destroy()