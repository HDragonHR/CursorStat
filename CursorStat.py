#from https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

import math
import threading
import tkinter as tk
from time import sleep
from collections import deque
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

pt = POINT()
Lock = threading.Lock()

x = deque([0], maxlen = 250)
y = deque([0], maxlen = 250)
dist_arr = deque()

sum_dist = 0.0
sum_delta_dist = 0.0

dist = deque([0], maxlen = 1)
accel = deque([0], maxlen = 1)

update_rate = 100

def capture():
    windll.user32.GetCursorPos(byref(pt))
    x.append(pt.x)
    y.append(pt.y)

class CapThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        while True:
            Lock.acquire()
            capture()
            Lock.release()
            time.sleep(1.0/10000.0)

def calc():
    global sum_dist, sum_delta_dist  
    for i in range(len(x)-1):
        x_dist = abs(x[i+1] - x[i])
        y_dist = abs(y[i+1] - y[i])
        temp = math.sqrt((x_dist**2)+(y_dist**2))*2
        dist_arr.append(temp)
        sum_dist += temp

    for i in range(len(dist_arr)-1):
        sum_delta_dist += (dist_arr[i+1] - dist_arr[i])

    dist.append(sum_dist)
    accel.append(sum_delta_dist)  

class CopyThread (threading.Thread):    
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global sum_dist, sum_delta_dist
        while True:
            time.sleep(update_rate/1000.0)
            Lock.acquire()
            calc()
            x.clear()
            y.clear()
            dist_arr.clear()
            sum_dist = 0.0
            sum_delta_dist = 0.0
            Lock.release()

thread1 = CapThread(1, "Capture Thread")
thread2 = CopyThread(2, "Copy Thread")
thread1.start()
thread2.start()

class Application(tk.Frame):              
    def __init__(self, master):
        
        self.label1=tk.Label(master)
        self.label1.grid(row=0, column=40)
        self.label1.configure(text='')
        self.label1.config(fg="#ffffff",bg="#00ff00",font=("Courier",40),anchor="w")
        self.count = 0

        self.label3=tk.Label(master)
        self.label3.grid(row=0, column=0)
        self.label3.configure(text='Speed : ')
        self.label3.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))

        self.label2=tk.Label(master)
        self.label2.grid(row=40, column=40)
        self.label2.configure(text='')
        self.label2.config(fg="#ffffff",bg="#00ff00",font=("Courier",40),anchor="w")
        self.count2 = 0

        self.label4=tk.Label(master)
        self.label4.grid(row=40, column=0)
        self.label4.configure(text='Accel : ')
        self.label4.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))

        self.update()

    def update_label(self):
        self.label1.configure(text = round(dist[0]/(update_rate/1000), 0))
        self.label2.configure(text = round(abs(accel[0])/(update_rate/1000), 0))

    def update(self):
        self.update_label()
        self.label1.after(update_rate, self.update)

app = tk.Tk()
app.geometry("620x140")
app.config(bg="#00ff00")
Application(app)                       
app.title('CursorStat')
app.mainloop()

