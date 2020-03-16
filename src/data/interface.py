from tkinter import *

class Interface(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('DEVICE VIEWS')
        self.master.geometry('1600x800')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+W+E)
        self._ipVar = StringVar()       
        self._upLabel()
        self._upListBox()
        self._upEntryArea()
        self._upButton()
        self._resizable()

    def _upLabel(self):
        _labelName = ['Name', 'Mac address', 'Channel', 'Type', 'Power']
        _listLabel = []
        for label in range(5):
            _listLabel.append(Label(self, text=_labelName[label], font=('Helvetica', 10), pady=5))
            _listLabel[label].grid(row=0, column=label, sticky=N+S+W+E)
        _product = Label(self, text=u'\u00A9 Product by Vinci Nicolò', font=('Comic Sans MS', 8))
        _product.grid(row=2, column=4, padx=10, pady=5, sticky=SE)
        
    def _upListBox(self):
        _listbox = []
        for lis in range(5):
            _listbox.append(Listbox(self, bg='lightgray'))
            _listbox[lis].grid(row=1, column=lis, padx=10, sticky=N+S+W+E)
            _listbox[lis].insert(END, str(lis))
    
    def _upEntryArea(self):
        _ipArea = Entry(self, textvariable=self._ipVar, bg='#C0C0C0')
        _ipArea.grid(row=2, column=1, padx=10, pady=5, sticky=W)

    def _upButton(self):
        _scan = Button(self, text='Insert IP and scan', bg='#808080')  # , command=)
        _scan.grid(row=2, column=0, padx=10, pady=5, sticky=E)

    def _resizable(self):
        self.rowconfigure(1, weight=50)
        self.rowconfigure(2, weight=1)
        for column in range(5):
            self.columnconfigure(column, weight=1)
