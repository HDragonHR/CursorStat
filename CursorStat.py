#from https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

import time
import math
import tkinter as tk
from collections import deque
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
    
pt = POINT()
x_arr = deque([0,0],maxlen = 2)
y_arr = deque([0,0],maxlen = 2)


def capture():
    windll.user32.GetCursorPos(byref(pt))
    x_arr.append(pt.x)
    y_arr.append(pt.y)
    

class Application(tk.Frame):              
    def __init__(self, master):
        
        self.label1=tk.Label(master)
        self.label1.grid(row=0, column=40)
        self.label1.configure(text='')
        self.label1.config(fg="#ffffff",bg="#00ff00",font=("Courier",40),anchor="w")
        self.count = 0

        self.label5=tk.Label(master)
        self.label5.grid(row=0, column=0)
        self.label5.configure(text='Speed : ')
        self.label5.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))

        self.update()

    def update_label(self):
        x_diff = x_arr[-1] - x_arr[0]
        y_diff = y_arr[-1] - y_arr[0]
        self.count = (math.sqrt((x_diff**2)+(y_diff**2)))*2
        self.label1.configure(text = round(self.count, 0))

    def update(self):
        i = 0
        while True and i < 2:
            capture()
            time.sleep(250.0/1000.0)
            i += 1
        self.update_label()
        self.label1.after(1, self.update)
        
app = tk.Tk()
app.geometry("620x70")
app.config(bg="#00ff00")
Application(app)                       
app.title('CursorStat')    
app.mainloop() 
