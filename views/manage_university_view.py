import tkinter as tk
from tkinter import ttk

class ManageUniversityWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.geometry("800x430")
        self.title("Manage University")