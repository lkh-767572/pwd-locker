import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from pmfunc import PwdLocker
from .windows import Menu, Interface, Popup

class App(ctk.CTk):
	def __init__(self, title, pm_logic):

		super().__init__()
		self.title(title)
		self.width = 900
		self.height = 600
		self.geometry(f"{self.width}x{self.height}")
		self.minsize(900, 600)
		self.maxsize(900, 600)

		# Logic
		self.pm = pm_logic()

		ctk.set_default_color_theme("dark-blue")
		ctk.set_appearance_mode("Dark")

		self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
		self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

		self.change_window(0)

		# Error Handling
		self.ERROR_OVER = True

	def change_window(self, new_page):

		#frames
		self.framelist = [
		Menu(master=self),			#0 Menu Frame
		Interface(master=self)	 	#1 Main Interface
		]

		for frame in self.framelist:
			frame.grid_remove()

		self.framelist[new_page].grid()

	def error_handling(self, err_text):
		if self.ERROR_OVER:
			Popup(master=self, err_text=err_text)