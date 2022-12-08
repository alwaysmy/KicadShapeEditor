import wx

class MyDialog(wx.Dialog):
    def __init__(self, parent, numbers, target):
        super().__init__(parent, title="My Dialog")
        self.SetSize((300, 200))

        # 保存输入的数字和目标数值
        self.numbers = numbers
        self.target = target

        # 创建一个静态文本控件用于显示提示信息
        self.text = wx.StaticText(self, label="请输入目标数值：")
        self.text.SetPosition((20, 20))

        # 创建一个文本框用于输入目标数值
        self.input = wx.TextCtrl(self)
        self.input.SetPosition((150, 20))

        # 创建一个按钮用于确定目标数值
        self.button = wx.Button(self, label="确定")
        self.button.SetPosition((110, 100))
        self.Bind(wx.EVT_BUTTON, self.on_button_clicked, self.button)

    def on_button_clicked(self, event):
        # 获取输入的目标数值
        value = self.input.GetValue()

        # 调用 get_closest_combination() 函数计算最接近目标数值的数字组合
        combination = get_closest_combination(self.numbers, self.target, value)

        # 显示结果
        wx.MessageBox("最接近目标数值的组合为：%s" % combination)

        # 关闭对话框
        self.Close()

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="My App")
        self.SetSize((600, 400))

        # 保存输入的数字
        self.numbers = []

        # 创建一个文本框用于输入数字
        self.input = wx.TextCtrl(self)
        self.input.SetPosition((20, 20))

        # 创建一个按钮用
