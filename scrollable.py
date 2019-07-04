import tkinter as tk
from tkinter import ttk


class Scrollable(tk.Frame):
	def __init__(self, frame, width=16):
		scrollbar = tk.Scrollbar(frame, width=width)
		scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

		self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		scrollbar.config(command=self.canvas.yview)

		self.canvas.bind('<Configure>', self.__fill_canvas)

		# base class initialization
		tk.Frame.__init__(self, frame)

		# assign this obj (the inner frame) to the windows item of the canvas
		self.windows_item = self.canvas.create_window(0, 0, window=self, anchor=tk.NW)

	def __fill_canvas(self, event):
		"Enlarge the windows item to the canvas width"

		canvas_width = event.width
		self.canvas.itemconfig(self.windows_item, width=canvas_width)

	def update(self):
		"Update the canvas and the scrollregion"

		self.update_idletasks()
		self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


class ScrollFrame(tk.Frame):
	def __init__(self, parent):
		super().__init__(parent)  # create a frame (self)

		self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")  # place canvas on self
		self.viewPort = tk.Frame(self.canvas,
								 background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
		self.vsb = tk.Scrollbar(self, orient="vertical",
								command=self.canvas.yview)  # place a scrollbar on self
		self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

		self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
		self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
		self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",  # add view port frame to canvas
								  tags="self.viewPort")

		self.viewPort.bind("<Configure>",
						   self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.

	def onFrameConfigure(self, event):
		'''Reset the scroll region to encompass the inner frame'''
		self.canvas.configure(scrollregion=self.canvas.bbox(
			"all"))  # whenever the size of the frame changes, alter the scroll region respectively.
