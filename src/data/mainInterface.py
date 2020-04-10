import tkinter as tk             
from devicePage import DevicePage
from localizePage import LocalizePage

class MainInterface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames = {}
        for F in (DevicePage, LocalizePage):
            page_name = F.__name__
            frame = F(controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='N'+'S'+'E'+'W')

        self.show_frame('DevicePage')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
