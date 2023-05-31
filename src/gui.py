import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from pmfunc import PwdLocker

pm = PwdLocker()


class App(ctk.CTk):
	def __init__(self, title):

		super().__init__()
		self.title(title)
		self.width = 800
		self.height = 600
		self.geometry(f"{self.width}x{self.height}")
		self.minsize(800, 600)
		self.maxsize(800, 600)

		ctk.set_default_color_theme("dark-blue")
		ctk.set_appearance_mode("Dark")

		self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
		self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

		self.change_window(0)

		# Error Handling
		self.ERROR_OVER = True

		# Logic
		self.pm = PwdLocker()

	def change_window(self, new_page):

		#frames
		self.framelist = [
		self.Menu(master=self),		#0 Menu Frame
		self.Interface(master=self) #1 Main Interface
		]

		for frame in self.framelist:
			frame.grid_remove()

		self.framelist[new_page].grid()

	def error_handling(self, err_text):
		if self.ERROR_OVER:
			self.Popup(master=self, err_text=err_text)

	class Popup(ctk.CTkToplevel):
		def __init__(self, master, err_text):
			super().__init__(master)
			self.err_text = err_text
			self.geometry("200x75")
			self.rowconfigure(0, weight=1)
			self.columnconfigure((0, 1, 2), weight=1)

			self.buttontext = "Ok!"
			self.master = master

			self.title("Error!")
			self.create_widgets()
			self.create_layout()
			self.minsize(200, 80)
			self.maxsize(200, 80)

			#reset Gui Error message
			self.master.ERROR_OVER = False

		def create_widgets(self):
			self.pop = ctk.CTkLabel(
				self, 
				text=self.err_text,
				font=("Arial", 15, "bold"))
			self.pop_but = ctk.CTkButton(
				self, 
				text=self.buttontext, 
				command=self.reset)

		def create_layout(self):
			self.pop.grid(pady=10, column=0, columnspan=3, sticky="ew")
			self.pop_but.grid(column=1, sticky="n", pady=10)

		def reset(self):
			self.master.ERROR_OVER = True
			self.destroy()

	class Menu(ctk.CTkFrame):
		def __init__(self, master):
			super().__init__(master)
			self.master = master

			self.rowconfigure((0, 1, 2, 3), weight=1)
			self.columnconfigure((0, 1, 2, 3), weight=1)

			# initialize login frame
			self.switch_frames(0, 0)

			self.widgets()
			self.layout()

		def widgets(self):
			self.pwd_locker_label = ctk.CTkLabel(
				self,
				text="PWD-Locker",
				font=("Bondoni", 70, "bold"))

		def layout(self):
			self.grid(
				row=0, column=0, rowspan=8, columnspan=6,
				padx=30, pady=30, sticky="nsew")
			self.pwd_locker_label.grid(
				row=0, column=0, columnspan=6,
				padx=20, pady=30, sticky="nsew")

		def switch_frames(self, old, new):
			#frames
			self.framelist = [
			self.Login(master=self),		#0 Login Frame
			self.New(master=self)]			#1 New File Frame

			self.framelist[old].forget()
			self.framelist[new].tkraise()

		class Login(ctk.CTkFrame):
			def __init__(self, master):
				super().__init__(master)
				self.master = master
				self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
				self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
				self.widgets()
				self.layout()

			def widgets(self):
				fg = "#394867"
				fsize = 20
				self.label = ctk.CTkLabel(
					self,
					text="Login",
					font=("Arial", 30))
				self.load_key_label = ctk.CTkLabel(
					self,
					text="Enter path of key file:",
					font=("Arial", fsize))
				self.load_key_entry = ctk.CTkEntry(
					self,
					font=("Arial", fsize),
					placeholder_text="Keyfile")
				self.load_pwd_label = ctk.CTkLabel(
					self, 
					text="Enter path of password file:",
					font=("Arial", fsize))
				self.load_pwd_entry = ctk.CTkEntry(
					self,
					font=("Arial", fsize),
					placeholder_text="Passwordfile")
				self.login_load_but = ctk.CTkButton(
					self, 
					text="Load",
					font=("Arial", 30, "bold"),
					command=self.load_pwd)
				self.login_new_but = ctk.CTkButton(
					self,
					text="New",
					font=("Arial", 30, "bold"), 
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					command=lambda: self.master.switch_frames(0, 1))


			def layout(self):
				self.grid(
					row=1, column=0, rowspan=3, columnspan=5,
					padx=50, pady=50, sticky="nsew")
				self.label.grid(
					row=2, column=1, columnspan=4)
				self.load_key_entry.grid(
					row=3, column=1, columnspan=4,
					padx=15, pady=10, sticky="ew")
				self.load_pwd_entry.grid(
					row=4, column=1, columnspan=4,
					padx=10, sticky="ew")
				self.login_load_but.grid(
					row=5, column=4,
					pady=20, sticky="ew")
				self.login_new_but.grid(
					row=5, column=2, 
					pady=20, sticky="ew")

			def load_pwd(self):
				key = self.load_key_entry.get()
				pwd = self.load_pwd_entry.get()
				if key and pwd:
					pm.load_key(key)
					pm.load_password_file(pwd)
					if not self.master.master.pm.FNF:
						self.master.master.change_window(1)
					else:
						if self.master.master.ERROR_OVER:
							self.master.master.error_handling("File not found!")
				else:
					if self.master.master.ERROR_OVER:
						self.master.master.error_handling("Enter more information")

		class New(ctk.CTkFrame):
			def __init__(self, master):
				super().__init__(master)
				self.master = master
				self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
				self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
				self.widgets()
				self.layout()

			def widgets(self):
				fg = "#394867"
				fsize = 20
				self.label = ctk.CTkLabel(
					self,
					text="Create Login",
					font=("Arial", 30))
				self.new_key_label = ctk.CTkLabel(
					self,
					text="Enter path for new key-file:",
					font=("Arial", fsize))
				self.new_key_entry = ctk.CTkEntry(
					self,
					font=("Arial", fsize),
					placeholder_text="Keyfile")
				self.new_pwd_label = ctk.CTkLabel(
					self, 
					text="Enter path for new pwd-file:",
					font=("Arial", fsize),)
				self.new_pwd_entry = ctk.CTkEntry(
					self,
					font=("Arial", fsize),
					placeholder_text="Passwordfile")
				self.new_load_but = ctk.CTkButton(
					self, 
					text="Load",
					font=("Arial", 30, "bold"),
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					command=lambda: self.master.switch_frames(1, 0))
				self.new_new_but = ctk.CTkButton(
					self,
					text="Create",
					font=("Arial", 30, "bold"),
					command=self.create_pwd)

			def layout(self):	
				self.grid(
					row=1, column=0, rowspan=3, columnspan=5,
					padx=50, pady=50, sticky="nsew")
				self.label.grid(
					row=2, column=1, columnspan=4)
				self.new_key_entry.grid(
					row=3, column=1, columnspan=4,
					padx=15, pady=10, sticky="ew")
				self.new_pwd_entry.grid(
					row=4, column=1, columnspan=4,
					padx=10, sticky="ew")
				self.new_load_but.grid(
					row=5, column=4,
					pady=20, sticky="ew")
				self.new_new_but.grid(
					row=5, column=2, 
					pady=20, sticky="ew")

			def create_pwd(self, key, pwd):
				key = self.new_key_entry.get()
				pwd = self.new_pwd_entry.get()
				if key and pwd:
					pm.create_key(key)
					pm.generate_password_file(pwd)
					pm.load_key(key)
					pm.load_password_file(pwd)
					self.master.master.change_window(1)
				else:
					self.master.master.error_handling("Enter all information!")


	class Interface(ctk.CTkFrame):
		def __init__(self, master):
			super().__init__(master)

			self.master = master
			self.columnconfigure(0, weight=2)
			self.rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)
			self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

			self.widgets()
			self.layout()

		def widgets(self):
			self.sidebar = self.Sidebar(master=self)
			self.info_window = self.InfoWindow(master=self)

		def layout(self):
			self.grid(
				row=0, column=0, rowspan=8, columnspan=7,
				sticky="nsew")

		def frame_by_name(self, name):
			self.sidebar.show_but.configure(fg_color=("gray75", "gray25") if name == "show" else "transparent")
			self.sidebar.add_but.configure(fg_color=("gray75", "gray25") if name == "add" else "transparent")
			self.sidebar.gen_but.configure(fg_color=("gray75", "gray25") if name == "gen" else "transparent")

			if name == "show":
				self.show_frame = self.info_window.Show(master=self.info_window)
			if name == "add":
				self.add_frame = self.info_window.Add(master=self.info_window)
			if name == "gen":
				self.gen_frame = self.info_window.Gen(master=self.info_window)

		class Sidebar(ctk.CTkFrame):
			def __init__(self, master):
				super().__init__(master)

				self.columnconfigure((0, 1, 2), weight=1)
				self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
				
				self.inactive = "#394867" # unselected button color
				self.active = "#1f538d"
				self.master = master
				self.widgets()
				self.layout()

			def widgets(self):
				self.pwd_locker_label = ctk.CTkLabel(
					self,
					text="PWD-Locker",
					font=("Bondoni", 25, "bold"))
				self.show_but = ctk.CTkButton(
					self,
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					text="Show", font=("Arial", 25, "bold"),
					command=self.show_but_action)
				self.add_but = ctk.CTkButton(
					self,
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					text="Add",
					font=("Arial", 25, "bold"),
					command=self.add_but_action)
				self.gen_but = ctk.CTkButton(
					self,
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					text="Gen", font=("Arial", 25, "bold"),
					command=self.gen_but_func)
				self.quit_but = ctk.CTkButton(
					self,
					corner_radius=0, height=40, border_spacing=10, 
					fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
					text="QUIT", font=("Arial", 25, "bold"),
					command=self.master.master.destroy)

			def layout(self):
				self.grid(
					row=0, column=0, rowspan=8,
					sticky="nsew")
				self.pwd_locker_label.grid(
					row=0 , column=1, 
					pady=20, sticky="nsew")
				self.show_but.grid(
					row=2, column=1,
					pady=5, sticky="nsew")
				self.add_but.grid(
					row=3, column=1,
					pady=5, sticky="nsew")
				self.gen_but.grid(
					row=4, column=1,
					pady=5, sticky="nsew")
				self.quit_but.grid(
					row=8, column=1,
					pady=5, sticky="nsew")

			def show_but_action(self):
				self.master.frame_by_name(name="show")

			def add_but_action(self):
				self.master.frame_by_name(name="add")

			def gen_but_func(self):
				self.master.frame_by_name(name="gen")
					
		class InfoWindow(ctk.CTkFrame):
			def __init__(self, master):
				super().__init__(master)

				self.master = master

				self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
				self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

				self.widgets()
				self.layout()

			def widgets(self):
				pass

			def layout(self):
				self.grid(
					row=0, column=1, rowspan=8, columnspan=6,
					padx=25, pady=25, sticky="nsew")

			class Show(ctk.CTkFrame):
				def __init__(self, master):
					super().__init__(master)
					self.master = master

					self.widgets()
					self.layout()

				def widgets(self):
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
							self.table.insert("", "end", index, values=i)
							index += 1

				def layout(self):
					self.grid(
						row=0, column=0, rowspan=8, columnspan=6,
						padx=25, pady=25, sticky="nsew")
					self.table_scroll.grid(row=0, column=8, rowspan=8, 
						sticky="e")
					self.table.grid(row=0, column=1, rowspan=8, columnspan=6,
						sticky="nsew")

			class Add(ctk.CTkFrame):
				def __init__(self, master):
					super().__init__(master)
					self.widgets()
					self.layout()

				def widgets(self):
					pass 

				def layout(self):
					self.grid(
						row=0, column=0, rowspan=8, columnspan=6,
						padx=25, pady=25, sticky="nsew")

			class Gen(ctk.CTkFrame):
				def __init__(self, master):
					super().__init__(master)
					self.widgets()
					self.layout()

					self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
					self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

				def widgets(self):
					self.slidervalue = 32
					self.gen_label = ctk.CTkLabel(
						self,
						text="Customize password options:", 
						font=("Arial", 25))
					self.output = ctk.CTkEntry(self)
					self.special = ctk.CTkCheckBox(
						self,
						text="Special Characters",
						font=("Arial", 25))
					self.slider = ctk.CTkSlider(
						self,
						from_=0, to=64, number_of_steps=64)
					self.slidertext = ctk.CTkLabel(
						self,
						font=("Arial", 20))
					self.generate_button = ctk.CTkButton(
						self,
						text="Generate",
						font=("Arial", 25),
						command=self.generate)
					self.slider.bind("<ButtonRelease-1>", command=lambda a: [self.slidertext.configure(text=int(self.slider.get()))])

				def layout(self):
					self.grid(
						row=0, column=0, rowspan=8, columnspan=6,
						padx=25, pady=25, sticky="nsew")
					self.gen_label.grid(
						row=0, column=1, columnspan=3, sticky="ew")
					self.output.grid(
						row=1, column=1, columnspan=3, sticky="ew")
					self.special.grid(
						row=2, column=1, columnspan=1)
					self.slider.grid(
						row=3, column=2, columnspan=2, sticky="ew")
					self.slidertext.grid(
						row=3, column=1, sticky="e")
					self.generate_button.grid(
						row=4, column=1)

				def generate(self):
					pwd = pm.generate_password(lenght=int(self.slider.get()), special=self.special.get())
					self.output.configure(textvariable=pwd)
					# as writing in textfield is not doable just copy to clipboard

				# TODO:
				# Enter as faster way to navigate
				# Add
				# Make table dark
				# Extejd show
				# modify pmfunc with secrets module
