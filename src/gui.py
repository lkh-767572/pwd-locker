import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from pmfunc import PwdLocker

pm = PwdLocker()
fsize = 20

class Gui(ctk.CTk):
	def __init__(self, title):
		
		# main setup
		super().__init__()
		self.title(title)
		self.width = 400
		self.height = 400
		self.geometry(f"{self.width}x{self.height}")

		# CustomTkinter
		ctk.set_default_color_theme("dark-blue")
		ctk.set_appearance_mode("Dark")

		# Window Manager
		self.no_window = True
		self.manager = WindowMan(master=self)
		# fix if no menu
		if self.no_window:
			Menu(master=self)
			self.manager.change_window(0, 0)
			self.no_window = False

		# Error Handling
		self.ERROR_TEXT = ""
		self.ERROR_OVER = True

		self.mainloop()

class WindowMan():
	def __init__(self, master):

		# frames
		self.framelist = [			#Index
		Menu(master),				#0 Menu Frame
		GenNew(master),				#1 New Pwd & File
		LoadData(master),			#2 Load existing Data
		GeneratePassword(master),	#3 Generate random pwd
		ShowData(master),			#4 Show Passwords
		AddData(master),			#5 Add new Passwords
		ChooseNext(master)]			#6 Choose next option

	def change_window(self, del_page, new_page):
		self.framelist[del_page].forget()
		self.framelist[new_page].tkraise()
		self.framelist[new_page].pack(expand=True, fill="both")

class Menu(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		self.master = master
		self.master.width, self.master.height = 400, 400
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		button_scale = (125, 75)
		bfontsize = 50
		self.menu = ctk.CTkLabel(
			self, 
			text="PWD-Locker", 
			font=("Arial", 75, "bold"))
		self.load_but = ctk.CTkButton(
			self, 
			text="New", 
			font=("Arial", bfontsize, "bold"), 
			corner_radius=7, 
			command=lambda: self.master.manager.change_window(0, 1), 
			width=button_scale[0], height=button_scale[1])
		self.new_but = ctk.CTkButton(
			self, 
			text="Load", 
			font=("Arial", bfontsize, "bold"), 
			corner_radius=7, 
			command=lambda: self.master.manager.change_window(0, 2), 
			width=button_scale[0], height=button_scale[1])

	def create_layout(self):
		self.menu.pack(pady=20)
		self.load_but.pack(pady=25)
		self.new_but.pack(pady=10)

class GenNew(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		self.master = master
		self.master.geometry("200x350")
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		width = 200
		self.gen_key_label = ctk.CTkLabel(
			self,
			text="Enter path for generated key:",
			font=("Arial", fsize),
			width=width)
		self.gen_key_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5),
			width=width)
		self.gen_pwd_label = ctk.CTkLabel(
			self, 
			text="Enter path for generated password file:",
			font=("Arial", fsize),
			width=width)
		self.gen_pwd_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5),
			width=width)
		self.gen_but = ctk.CTkButton(
			self, 
			text="Generate",
			font=("Arial", 30, "bold"),
			width=width,
			# weirldy command only works with lambda; same for load_but_func
			command=lambda: self.gen_but_func(key=self.gen_key_entry.get(), pwd=self.gen_pwd_entry.get()))

	def create_layout(self):
		distx = 50
		self.gen_key_label.pack(pady=25, padx=distx, anchor="w")
		self.gen_key_entry.pack(pady=10, padx=distx, anchor="w")
		self.gen_pwd_label.pack(pady=15, padx=distx, anchor="w")
		self.gen_pwd_entry.pack(pady=10, padx=distx, anchor="w")
		self.gen_but.pack(pady=15, padx=distx, anchor="w")

	def gen_but_func(self, key, pwd):
		if key and pwd:
			pm.create_key(key)
			pm.generate_password_file(pwd)
			pm.load_key(key)
			pm.load_password_file(pwd)
			self.master.manager.change_window(1, 5)

class LoadData(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		self.master = master
		master.geometry("200x350")
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		width = 200
		self.load_key_label = ctk.CTkLabel(
			self,
			text="Enter path of key:",
			font=("Arial", fsize),
			width=width)
		self.load_key_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5),
			width=width)
		self.load_pwd_label = ctk.CTkLabel(
			self, 
			text="Enter path of password file:",
			font=("Arial", fsize),
			width=width)
		self.load_pwd_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5),
			width=width)
		self.load_but = ctk.CTkButton(
			self, 
			text="Load",
			font=("Arial", 30, "bold"),
			width=width,
			command=lambda: self.load_but_func(key=self.load_key_entry.get(), pwd=self.load_pwd_entry.get()))

	def create_layout(self):
		distx = 50
		self.load_key_label.pack(pady=25, padx=distx, anchor="w")
		self.load_key_entry.pack(pady=10, padx=distx, anchor="w")
		self.load_pwd_label.pack(pady=15, padx=distx, anchor="w")
		self.load_pwd_entry.pack(pady=10, padx=distx, anchor="w")
		self.load_but.pack(pady=15, padx=distx, anchor="w")

	def load_but_func(self, key, pwd):
		if key and pwd:
			pm.load_key(key)
			pm.load_password_file(pwd)
			if not pm.FNF:
				print(key)
				data_list = pm.show()
				if data_list:
					lambda: self.master.manager.change_window(2, 4)
				else:
					lambda: self.master.manager.change_window(2, 5)

			else:
				self.master.ERROR_TEXT = "File not found!"
				if self.master.ERROR_OVER:
					Popup(self.master, self.master.ERROR_TEXT)

		else:
			self.master.ERROR_TEXT = "Enter more information"
			if self.master.ERROR_OVER:
				Popup(self.master, self.master.ERROR_TEXT)

class GeneratePassword(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)

class ShowData(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)

		self.master = master
		self.create_widgets()
		self.create_layout()
		
	def create_widgets(self):
		data_list = pm.show()
		
		self.table = ttk.Treeview(self)
		self.table_scroll = ctk.CTkScrollbar(self, command=self.table.yview)

		self.table["columns"] = ("site", "user", "pwd")
		self.table["show"] = "headings"
		self.table.heading(
			"site", 
			text="Site", 
			anchor=tk.CENTER)
		self.table.heading(
			"user", 
			text="Username", 
			anchor=tk.CENTER)
		self.table.heading(
			"pwd", 
			text="Password", 
			anchor=tk.CENTER)

		# fill table
		if data_list:
			index = 0
			for i in data_list:
				table.insert(END, index, values=i)
				index += 1

	def create_layout(self):
		self.table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
		self.table.pack()
		
class AddData(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		self.master = master
		self.master.geometry("200x500")
		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.site_label = ctk.CTkLabel(
			self,
			text="Enter the site:",
			font=("Arial", fsize))
		self.site_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5))
		self.user_label = ctk.CTkLabel(
			self,
			text="Enter the username:",
			font=("Arial", fsize))
		self.user_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5))
		self.pwd_label = ctk.CTkLabel(
			self,
			text="Enter the password:",
			font=("Arial", fsize))
		self.pwd_entry = ctk.CTkEntry(
			self,
			font=("Arial", fsize+5))
		self.add_but = ctk.CTkButton(
			self,
			text="Add",
			font=("Arial", 30, "bold"),
			width=200,
			command=lambda: self.add_but_func(
				site=self.site_entry.get(),
				user=self.user_entry.get(),
				pwd=self.pwd_entry.get()))

	def create_layout(self):
		distx = 50
		self.site_label.pack(pady=25, padx=distx, anchor="w")
		self.site_entry.pack(pady=5, padx=distx, anchor="w")
		self.user_label.pack(pady=25, padx=distx, anchor="w")
		self.user_entry.pack(pady=5, padx=distx, anchor="w")
		self.pwd_label.pack(pady=25, padx=distx, anchor="w")
		self.pwd_entry.pack(pady=5, padx=distx, anchor="w")
		self.add_but.pack(pady=25, padx=distx, anchor="w")

	def add_but_func(self, site, user, pwd):
		# TODO: Func that adds the data and then gives option to go to show/ add more or quit
		# New window for this?
		if site and user and pwd:
			pm.add_password(site, user, pwd)
			self.master.manager.change_window(5, 6)
		else:
			self.master.ERROR_TEXT = "Please enter all information! "
			if self.master.ERROR_OVER:
				Popup(self.master, self.master.ERROR_TEXT)

class ChooseNext(ctk.CTkFrame):
	def __init__(self, master, **kwargs):
		super().__init__(master)
		self.master = master

		self.create_widgets()
		self.create_layout()

	def create_widgets(self):
		self.next_steps = ctk.CTkLabel(
			self,
			text="Select next action:",
			font=("Arial", 20))
		self.add_another = ctk.CTkButton(
			self,
			text="Add another",
			font=("Arial", 30),
			command=lambda: self.master.manager.change_window(6, 5))
		self.show = ctk.CTkButton(
			self,
			text="Show Passwords",
			font=("Arial", 30),
			command=lambda: self.master.manager.change_window(6, 4))
		self.quit = ctk.CTkButton(
			self,
			text="QUIT",
			font=("Arial", 30),
			command=lambda: self.save_and_quit())

	def create_layout(self):
		self.next_steps.pack(pady=10)
		self.add_another.pack(pady=20)
		self.show.pack(pady=5)
		self.quit.pack(pady=5)

	def save_and_quit(self):
		pm.save()
		self.master.destroy()

class Popup(ctk.CTkToplevel):
		def __init__(self, master, err_text):
			super().__init__(master)
			self.err_text = err_text
			self.geometry("200x75")
			self.buttontext = "Ok!"
			self.master = master
			self.title("Error!")
			self.create_widgets()
			self.create_layout()

			#reset Gui Error message
			self.master.ERROR_OVER = False

		def create_widgets(self):
			self.pop = ctk.CTkLabel(
				self, 
				text=self.err_text)
			self.pop_but = ctk.CTkButton(
				self, 
				text=self.buttontext, 
				command=self.reset)

		def create_layout(self):
			self.pop.pack()
			self.pop_but.pack()

		def reset(self):
			self.master.ERROR_OVER = True
			self.destroy()