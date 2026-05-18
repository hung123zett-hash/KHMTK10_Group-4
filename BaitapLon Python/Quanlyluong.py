import tkinter as tk
from controller import EmployeeController

def main():
    root = tk.Tk()
    
    # Áp dụng theme nếu có
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except Exception:
        pass 
        
    # Khởi tạo Controller (Controller sẽ tự động khởi tạo Model và View)
    app = EmployeeController(root)
    
    # Chạy vòng lặp sự kiện chính của Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
