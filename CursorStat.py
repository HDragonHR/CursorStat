#from https://stackoverflow.com/questions/3698635/getting-cursor-position-in-python

import time
import threading
import tkinter as tk
from collections import deque
from ctypes import windll, Structure, c_long, byref

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]
    
pt = POINT()
x_arr = deque(maxlen = 1)
y_arr = deque(maxlen = 1)
speed_x_1 = deque(maxlen = 1)
speed_y_1 = deque(maxlen = 1)

def capture():
    while True:
        windll.user32.GetCursorPos(byref(pt))
        x_arr.append(pt.x)
        y_arr.append(pt.y)
        time.sleep(1.0/100000.0)

def calculate_speed():
    x1 = x_arr[0]
    y1 = y_arr[0]
        
    time.sleep(100.0/1000.0)
        
    x2 = x_arr[0]
    y2 = y_arr[0]
        
    x_diff = x2 - x1
    y_diff = y2 - y1
                
    return {'speed_x': x_diff/(100.0/1000.0),
            'speed_y': y_diff/(100.0/1000.0)}

def transfer():
    while True:
       time.sleep(1.0/1000.0)
       result = calculate_speed()
       speed_x_1.append(result['speed_x'])
       speed_y_1.append(result['speed_y'])
       
       #print("speed_x_1",result['speed1_x'], "speed_y_1",result['speed1_y'])

class captureThread (threading.Thread):
    def __init__ (self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.tthreadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        capture()

class transferThread (threading.Thread):
    def __init__ (self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.tthreadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        transfer()

class Application(tk.Frame):              
    def __init__(self, master):
        
        self.label1=tk.Label(master)
        self.label1.grid(row=0, column=100)
        self.label1.configure(text='')
        self.label1.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))
        self.count1 = 0

        self.label2=tk.Label(master)
        self.label2.grid(row=100, column=100)
        self.label2.configure(text='')
        self.label2.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))
        self.count2 = 100

        self.label5=tk.Label(master)
        self.label5.grid(row=0, column=0)
        self.label5.configure(text='Speed X : ')
        self.label5.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))

        self.label6=tk.Label(master)
        self.label6.grid(row=100, column=0)
        self.label6.configure(text='Speed Y : ')
        self.label6.config(fg="#ffffff",bg="#00ff00",font=("Courier",40))

        self.update_labels()

    def update_labels(self):
        self.label1.configure(text = self.count1)
        self.label2.configure(text = self.count2)
        self.label1.after(1, self.update_labels) # call this method again in 1,000 milliseconds      
        self.count1 = speed_x_1[0]
        self.count2 = speed_y_1[0]
        

thread1 = captureThread(1,"capture_Thread",1)
thread2 = transferThread(1,"transfer_Thread",1)

thread1.start()
thread2.start()

time.sleep(5.0/100.0)

app = tk.Tk()
app.geometry("620x130")
app.config(bg="#00ff00")
Application(app)                       
app.title('CursorStat')    
app.mainloop() 
