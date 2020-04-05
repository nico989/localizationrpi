from tkinter import *
from tkinter.ttk import *

class Win(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('DEVICE VIEWS')
        self.master.geometry('1200x600')
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        self.grid(sticky=N+S+W+E)

        self._tv = Treeview(self)
        self._tv['columns'] = ('starttime', 'endtime', 'status')
        self._tv.heading("#0", text='Sources', anchor='center')
        self._tv.column("#0", anchor="center")
        self._tv.heading('starttime', text='Start Time')
        self._tv.column('starttime', anchor='center', width=100)
        self._tv.heading('endtime', text='End Time')
        self._tv.column('endtime', anchor='center', width=100)
        self._tv.heading('status', text='Status')
        self._tv.column('status', anchor='center', width=100)
        self._tv.insert('', 'end', text="First", values=('10:00',
                             '10:10', 'Ok'))
        self._tv.grid(row=0, column=0, sticky = (N,S,W,E))

        self._buttonPane = Frame(self)
        self._buttonPane.grid(row=1, column=0, sticky=W+E)

        self._button1 = Button(self._buttonPane, text='IP SCAN')
        self._button1.grid(row=0, column=0)
        self._entry1 = Entry(self._buttonPane)
        self._entry1.grid(row=0, column=1)
        self._button2 = Button(self._buttonPane, text='MAC SEARCH')
        self._button2.grid(row=0, column=2)
        self._entry2 = Entry(self._buttonPane)
        self._entry2.grid(row=0, column=3)
        self._button3 = Button(self._buttonPane, text='CLEAN ALL')
        self._button3.grid(row=0, column=4)
        self._button4 = Button(self._buttonPane, text='OUTDOOR/INDOOR')
        self._button4.grid(row=0, column=5)
        self._label = Label(self._buttonPane, text='PRODUCT BY')
        self._label.grid(row=0, column=6)


        
        self.rowconfigure(0, weight=20)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        for x in range(7):
            self._buttonPane.columnconfigure(x, weight=1)
       

def main():
    Win().mainloop()

if __name__ == "__main__":
    main()
