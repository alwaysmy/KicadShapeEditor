import sys
import wx
import shape_para_set

import pcbnew
# import pcbnew
#这个tester.py是个启动器，用来调界面的，使用kicad的环境就行。
# 免得每次都要在kicad里面刷新插件（我也不知道怎么用kicad启动调试）
# 如果要在kicad里面调试，使用kicad的插件显示python控制台里面exec(open('tester.py').read())
# 这样就可以看到报错信息了
class MyDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="My Dialog")
        self.SetSize((300, 200))

        # 创建一个静态文本控件用于显示提示信息
        self.text = wx.StaticText(self, label="这是一个对话框！")
        self.text.SetPosition((20, 20))

        # 创建一个按钮用于关闭对话框
        self.button = wx.Button(self, label="确定")
        self.button.SetPosition((110, 100))
        self.Bind(wx.EVT_BUTTON, self.on_button_clicked, self.button)

    def on_button_clicked(self, event):
        self.Close()

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="My App")
        self.SetSize((600, 400))

        # 创建一个按钮用于打开对话框
        self.button = wx.Button(self, label="打开对话框")
        self.button.SetPosition((220, 150))
        self.Bind(wx.EVT_BUTTON, self.on_button_clicked, self.button)
        shape_para_set.Add_Shapes.Run(self)

    def on_button_clicked(self, event):
        # 创建并显示对话框
        # dialog = MyDialog(self)
        # dialog.ShowModal()
        # shape_para_set.Add_Shapes.Run(self)
        # dialog = Dialog(None)
        # dialog.Center()
        # dialog.ShowModal()
        pass
if __name__ == "__main__":
    app = wx.App()
    # frame = MyFrame()
    # testdlg = shape_para_set.MyDialog(None)
    # testdlg.ShowModal()
    # testdlg.Destroy()
    # app.MainLoop()
    isDebug = True if sys.gettrace() else False
    if isDebug:
        # global boardobj
        # pcbfile = r'C:\Users\Always\Desktop\dd\dd.kicad_pcb'#没有特殊需求可以随便找一个pcb，直接放工程目录下也行
        # boardobj=pcbnew.LoadBoard(pcbfile)
        dialog=shape_para_set.Dialog(None)
        dialog.Show()
    else:
        dialog = shape_para_set.Add_Shapes()
        dialog.Run()
    app.MainLoop()


# frame.Show()
# app.MainLoop()
