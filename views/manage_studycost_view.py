import tkinter as tk
from tkinter import ttk, messagebox


class ManageStudyCostWindow(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.title("Manage Study Cost")
        self.geometry("950x600")