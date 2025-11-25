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
    # Load initial data after controller is set
    if main_view.country_combo["values"]:
        controller.on_country_changed(main_view.country_combo["values"][0])

    root.mainloop()

if __name__ == "__main__":
    main()
