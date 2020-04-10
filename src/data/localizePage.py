import tkinter as tk  

class LocalizePage(tk.Frame):

    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller
        self._controller = controller
        self._controller.rowconfigure(0, weight=1)
        self._controller.columnconfigure(0, weight=1)
        self.grid(sticky='N'+'S'+'W'+'E')
        label = tk.Label(self, text="This is the start page")
        label.grid(row=0, column=0)

        button1 = tk.Button(self, text="Go to Interface",
                            command=lambda: controller.show_frame('DevicePage'))
        button1.grid(row=1, column=0)
 