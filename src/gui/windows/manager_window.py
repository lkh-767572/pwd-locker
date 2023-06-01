import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class Interface(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        self.columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        
        self.widgets()
        self.layout()

    def widgets(self):
        self.sidebar = self.Sidebar(master=self)
        self.info_window = self.InfoWindow(master=self)
        self.frame_by_name(name="show") # init show frame

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

            self.columnconfigure((0), weight=1)
            self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
            
            self.inactive = "#394867" # unselected button color
            self.active = "#1f538d"
            self.master = master
            self.widgets()
            self.layout()

        def widgets(self):
            self.pwd_locker_label = ctk.CTkLabel(
                self,
                text="PWD-Locker \n ------------------",
                font=("Bondoni", 15, "bold"))
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
                row=0, column=0, rowspan=8, columnspan=1,
                sticky="nsew")
            self.pwd_locker_label.grid(
                row=0 , column=0, 
                pady=20, sticky="ew")
            self.show_but.grid(
                row=2, column=0,
                pady=5, sticky="nsew")
            self.add_but.grid(
                row=3, column=0,
                pady=5, sticky="nsew")
            self.gen_but.grid(
                row=4, column=0,
                pady=5, sticky="nsew")
            self.quit_but.grid(
                row=8, column=0,
                pady=5, sticky="nsew")

        def show_but_action(self):
            self.master.frame_by_name(name="show")
            self.master.show_frame.fill_table()

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

            self.layout()

        def layout(self):
            self.grid(
                row=0, column=2, rowspan=8, columnspan=5,
                padx=25, pady=25, sticky="nsew")


        class Show(ctk.CTkFrame):
            def __init__(self, master):
                super().__init__(master)
                self.master = master

                self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
                self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

                self.widgets()
                self.layout()
                self.fill_table()

            def widgets(self):
                self.table = ttk.Treeview(self)
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

            def layout(self):
                style = ttk.Style(self.master.master.master)
                style.theme_use("clam")
                style.configure("Treeview", background="black", 
                                fieldbackground="black", foreground="white")
                self.grid(
                    row=0, column=0, rowspan=8, columnspan=6,
                    padx=25, pady=25, sticky="nsew")
                self.table.grid(row=0, column=0, rowspan=6, columnspan=5,
                    sticky="nsew")

            def fill_table(self):
                self.master.master.master.pm.load_password_file(self.master.master.master.pm.pfile)
                if self.table.exists('0'): # check if data in treeview
                    for index in self.table.get_children():
                        self.table.delete(str(index))

                data_list = self.master.master.master.pm.show()
                if data_list:
                    index = 0
                    for data in data_list:
                        self.table.insert("", "end", index, values=data)
                        index += 1

        class Add(ctk.CTkFrame):
            def __init__(self, master):
                super().__init__(master)
                self.widgets()
                self.layout()

                self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
                self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

            def widgets(self):
                self.add_label = ctk.CTkLabel(
                    self,
                     text="Add the your account details:",
                     font=("Arial", 35, "bold"))
                self.site_entry = ctk.CTkEntry(
                    self,
                    font=("Arial", 20),
                    placeholder_text="Site/ Program")
                self.user_entry = ctk.CTkEntry(
                    self,
                    font=("Arial", 20),
                    placeholder_text="Username")
                self.pwd_entry = ctk.CTkEntry(
                    self,
                    font=("Arial", 20),
                    placeholder_text="Password")
                self.add_but = ctk.CTkButton(
                    self,
                    text="Add",
                    font=("Arial", 20, "bold"),
                    command=self.add_data)
                # Enter button adds data too
                self.master.master.master.bind('<Return>', self.enter_func)

            def layout(self):
                self.grid(
                    row=0, column=0, rowspan=8, columnspan=6,
                    padx=25, pady=25, sticky="nsew")
                self.add_label.grid(
                    row=0, column=0, columnspan=6, 
                    pady=30, sticky="ew")
                self.site_entry.grid(
                    row=1, column=1, columnspan=4, sticky="ew")
                self.user_entry.grid(
                    row=2,column=1, columnspan=4, sticky="ew")
                self.pwd_entry.grid(
                    row=3, column=1, columnspan=4, sticky="ew")
                self.add_but.grid(
                    row=4, column=2, columnspan=2)

            def enter_func(self, event):
                self.add_data()

            def add_data(self):
                site, user, pwd = self.site_entry.get(), self.user_entry.get(), self.pwd_entry.get()
                if site and user and pwd:
                    self.master.master.master.pm.add_password(site, user, pwd)
                    self.master.master.master.pm.save(self.master.master.master.pm.key, self.master.master.master.pm.decData)
                    if self.master.master.master.pm.ValueError:
                        if self.master.master.master.ERROR_OVER:
                            self.master.master.master.error_handling("Value Error; Nothing saved!")
                else:
                    self.master.master.master.error_handling("Add all information!")

        class Gen(ctk.CTkFrame):
            def __init__(self, master):
                super().__init__(master)
                self.widgets()
                self.layout()

                self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
                self.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

            def widgets(self):
                self.gen_label = ctk.CTkLabel(
                    self,
                    text="Password Generator", 
                    font=("Arial", 35, "bold"))
                self.output = ctk.CTkEntry(self)
                self.special = ctk.CTkCheckBox(
                    self,
                    text="!@#$%^&*",
                    font=("Arial", 20))
                self.upper = ctk.CTkCheckBox(
                    self,
                    text="A-Z",
                    font=("Arial", 20))
                self.digits = ctk.CTkCheckBox(
                    self,
                    text="0-9",
                    font=("Arial", 20))
                self.options = ctk.CTkLabel(
                    self,
                    text="Options:", font=("Arial", 20))
                self.slider = ctk.CTkSlider(
                    self,
                    from_=0, to=64, number_of_steps=64)
                self.lenghttext = ctk.CTkLabel(
                    self,
                    text="Length:", font=("Arial", 20))
                self.lenghttext.configure(text="Length: (32)")
                self.generate_button = ctk.CTkButton(
                    self,
                    text="Generate",
                    font=("Arial", 25),
                    command=self.generate)
                self.copy_but = ctk.CTkButton(
                    self,
                    text="Copy to Clipboard",
                    font=("Arial", 25),
                    command=self.copy)
                # keybindings
                self.slider.bind("<ButtonRelease-1>", command=self.slider_move)
                # move slider with arrow-keys
                self.master.master.master.bind("<Left>", self.slider_minus)
                self.master.master.master.bind("<Right>", self.slider_plus)
                # generate new password when options changed
                self.special.bind("<Button-1>", self.option_changed)
                self.upper.bind("<Button-1>", self.option_changed)
                self.digits.bind("<Button-1>", self.option_changed)

            def layout(self):
                self.grid(
                    row=0, column=0, rowspan=8, columnspan=6,
                    padx=25, pady=25, sticky="nsew")
                self.gen_label.grid(
                    row=0, column=0, columnspan=6, sticky="ew")
                self.output.grid(
                    row=1, column=0, columnspan=6, sticky="ew", padx=50)
                self.lenghttext.grid(
                    row=2, column=0, columnspan=2, 
                    padx=10, sticky="ew")
                self.slider.grid(
                    row=2, column=2, columnspan=4, 
                    padx=10, sticky="ew")
                self.options.grid(
                    row=3, column=0, columnspan=2, padx=10,
                    sticky="ew")
                self.special.grid(
                    row=3, column=3, sticky="nsew", padx=10)
                self.upper.grid(
                    row=3, column=4, sticky="nsew", padx=10)
                self.digits.grid(
                    row=3, column=5, sticky="nsew", padx=10)
                self.generate_button.grid(
                    row=4, column=3, padx=10)
                self.copy_but.grid(
                    row=4, column=4, padx=10, columnspan=2)
            
            def slider_move(self, event):
                i = int(self.slider.get())
                s = "Lenght: " + "(" + str(i) + ")"
                self.lenghttext.configure(text=s)
                self.generate()

            def option_changed(self, event):
                self.generate()

            def generate(self):
                pwd = self.master.master.master.pm.generate_password(length=int(self.slider.get()), special=self.special.get(),
                    digits=self.digits.get(), uppercase=self.upper.get())
                self.output.delete(0, 64)       # clear entry field
                self.output.insert(0, pwd)      # insert password

            def copy(self):
                pwd = self.output.get()
                self.master.master.master.clipboard_clear()
                self.master.master.master.clipboard_append(pwd)
                self.master.master.master.update()

            def slider_minus(self, event):
                current_val = int(self.slider.get())
                next_val = current_val - 1
                if next_val < 0:
                    next_val = 0
                self.slider.set(next_val)
                s = "Lenght: " + "(" + str(next_val) + ")"
                self.lenghttext.configure(text=s)
                self.generate()

            def slider_plus(self, event):
                current_val = int(self.slider.get())
                next_val = current_val + 1
                if next_val > 64:
                    next_val = 64
                self.slider.set(next_val)
                s = "Lenght: " + "(" + str(next_val) + ")"
                self.lenghttext.configure(text=s)
                self.generate()

            # TODO:
            # Remove duplicates?
            # remove passwords
            # edit passwords
