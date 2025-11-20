import tkinter as tk
from tkinter import ttk, messagebox

class ManageCityWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.title("Manage City")
        self.controller = controller
        self.geometry("750x450")