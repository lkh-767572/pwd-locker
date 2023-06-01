import tkinter as tk
import customtkinter as ctk

class Popup(ctk.CTkToplevel):
    def __init__(self, master, err_text):
        super().__init__(master)
        self.err_text = err_text
        self.bind("<Return>", self.enter_func)
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

    def enter_func(self, event):
        self.reset()