import tkinter as tk

root = tk.Tk()
txtw = tk.Text(root)
txtw.pack(expand=True, fill=tk.BOTH)

txtw.insert("1.0", "I WILL PROTECT YOU NOW!")


def addindex(str):
    try:
        txtw.tag_add('ru', index1=str)  # , index2='1.4')
    except Exception as e:
        txtw.tag_add('ru', index1=str.replace("0",""))  # , index2='1.4')
        print(e)


addindex('1.2')
txtw.tag_config('ru', underline=True, underlinefg='red')
root.mainloop()
"""from tkinter import *
import time
import os
root = Tk()

frameCnt = 26
frames = [PhotoImage(file='C://Users//Dell//Downloads//poi-samaritan.gif',format = 'gif -index %i' %(i)) for i in range(frameCnt)]

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)
label = Label(root)
label.pack()
root.after(0, update, 0)
root.mainloop()"""
