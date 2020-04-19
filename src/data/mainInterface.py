import tkinter as tk             
from devicePage import DevicePage
from localizePage import LocalizePage

class MainInterface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.frames = {}
        for F in (DevicePage, LocalizePage):
            pageName = F.__name__
            frame = F(controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky='N'+'S'+'E'+'W')
        self.showFrame('DevicePage')

    def showFrame(self, pageName):
        frame = self.frames[pageName]
        frame.tkraise()

    def setIPToLocalizePage(self, value):
        self.frames['LocalizePage'].setIPAddr(value)
