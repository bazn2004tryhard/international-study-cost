# app.py
import tkinter as tk
from views.main_view import MainView
from controllers.main_controller import MainController

# ---------------------------
# 🔧 THÊM HÀM resource_path Ở ĐÂY
# ---------------------------
import os, sys

def resource_path(relative_path):
    """Dùng được khi chạy .py và khi đã đóng gói .exe"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ---------------------------

def main():
    root = tk.Tk()
    root.title("International Study Cost Comparison")
    
    root.state("zoomed")  # mở window full màn hình

    # tạo view trước, rồi inject controller
    main_view = MainView(root, controller=None)
    controller = MainController(main_view)
    main_view.controller = controller

    # Load initial data after controller is set
    if main_view.country_combo["values"]:
        controller.on_country_changed(main_view.country_combo["values"][0])

    root.mainloop()

if __name__ == "__main__":
    main()
