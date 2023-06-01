import tkinter as tk
import customtkinter as ctk

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
        self.Login(master=self),        #0 Login Frame
        self.New(master=self)]          #1 New File Frame

        self.framelist[old].forget()
        self.framelist[new].tkraise()
        self.master.bind('<Return>', self.framelist[new].enter_func)
        self.framelist[new].focus_set()

    class Login(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
            self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
            self.widgets()
            self.layout()

        def widgets(self):
            fg = "#394867"
            fsize = 20
            self.label = ctk.CTkLabel(
                self,
                text="Login",
                font=("Arial", 30))
            self.load_key_entry = ctk.CTkEntry(
                self,
                font=("Arial", fsize),
                placeholder_text="Keyfile")
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
                row=2, column=2, columnspan=4)
            self.load_key_entry.grid(
                row=3, column=2, columnspan=5,
                padx=15, pady=10, sticky="ew")
            self.load_pwd_entry.grid(
                row=4, column=2, columnspan=5,
                padx=10, sticky="ew")
            self.login_load_but.grid(
                row=5, column=5,
                pady=20, sticky="ew")
            self.login_new_but.grid(
                row=5, column=3, 
                pady=20, sticky="ew")

        def load_pwd(self):
            self.key = self.load_key_entry.get()
            self.pwd = self.load_pwd_entry.get()
            if self.key and self.pwd:
                self.master.master.pm.load_key(self.key)
                self.master.master.pm.load_password_file(self.pwd)
                if not self.master.master.pm.FileNotFoundError:
                    self.master.master.change_window(1)
                else:
                    if self.master.master.ERROR_OVER:
                        self.master.master.error_handling("File not found!")
            else:
                if self.master.master.ERROR_OVER:
                    self.master.master.error_handling("Enter more information")

        def enter_func(self, event):
            self.load_pwd()

    class New(ctk.CTkFrame):
        def __init__(self, master):
            super().__init__(master)
            self.master = master
            self.rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
            self.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
            self.widgets()
            self.layout()

        def widgets(self):
            fg = "#394867"
            fsize = 20
            self.label = ctk.CTkLabel(
                self,
                text="Create Login",
                font=("Arial", 30))
            self.new_key_entry = ctk.CTkEntry(
                self,
                font=("Arial", fsize),
                placeholder_text="Keyfile")
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
                row=2, column=2, columnspan=4)
            self.new_key_entry.grid(
                row=3, column=2, columnspan=5,
                padx=15, pady=10, sticky="ew")
            self.new_pwd_entry.grid(
                row=4, column=2, columnspan=5,
                padx=10, sticky="ew")
            self.new_load_but.grid(
                row=5, column=5,
                pady=20, sticky="ew")
            self.new_new_but.grid(
                row=5, column=3, 
                pady=20, sticky="ew")

        def create_pwd(self):
            self.key = self.new_key_entry.get()
            self.pwd = self.new_pwd_entry.get()
            if self.key and self.pwd:
                self.master.master.pm.create_key(self.key)
                self.master.master.pm.generate_password_file(self.pwd)
                self.master.master.pm.load_key(self.key)
                self.master.master.pm.load_password_file(self.pwd)
                self.master.master.change_window(1)
            else:
                self.master.master.error_handling("Enter all information!")

        def enter_func(self, event):
            self.create_pwd()