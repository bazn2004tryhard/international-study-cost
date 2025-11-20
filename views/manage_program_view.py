import tkinter as tk
from tkinter import ttk

class ManageProgramWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.geometry("700x420")
        self.title("Manage Program")