from tkinter import *
import tkinter as tk

class TkLogList:
  def __init__(self, elem, logs):
    self.elem = elem
    self.logs = logs
    self.frame = tk.Frame(self.elem, width = 256)

  def pack(self, num = 3):
    self.frame.pack()
    for log in reversed(self.logs[-num:]):
      msg = tk.Message(self.frame, text = str(log))
      msg.config(width = 256, anchor = NW, justify = LEFT)
      msg.pack(fill = X)

  def destroy(self):
    self.frame.destroy()
