# app.py
import tkinter as tk
from views.main_view import MainView
from controllers.main_controller import MainController

def main():
    root = tk.Tk()
    root.title("International Study Cost Comparison")
    root.geometry("1000x600")

    # tạo view trước, rồi inject controller
    main_view = MainView(root, controller=None)
    controller = MainController(main_view)
    main_view.controller = controller

    root.mainloop()

if __name__ == "__main__":
    main()
