import tkinter as tk
import controller

def main():
    root = tk.Tk()
    root.title("Phần mềm Quản lý Lương Nhân Viên - MVC & Functions")
    root.geometry("1500x800")
    
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "light")
    except Exception:
        pass 
        
    controller.main(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
