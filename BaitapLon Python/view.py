import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class EmployeeView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Phần mềm Quản lý Lương Nhân Viên - MVC & SQLite")
        self.root.geometry("1500x800")
        
        self.current_selected_id = None
        
        self.create_menu()
        self.create_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Chức năng
        chuc_nang_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Chức Năng", menu=chuc_nang_menu)
        chuc_nang_menu.add_command(label="Import CSV", command=self.mo_cua_so_import)
        chuc_nang_menu.add_command(label="Export CSV", command=self.controller.export_csv)
        chuc_nang_menu.add_command(label="Tìm kiếm dữ liệu", command=self.mo_cua_so_tim_kiem)
        chuc_nang_menu.add_command(label="Hiển thị tất cả", command=self.controller.load_data)
        chuc_nang_menu.add_separator()
        chuc_nang_menu.add_command(label="Thoát", command=self.root.quit)
        
        # Menu Giúp đỡ
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Giới thiệu phần mềm", command=self.mo_cua_so_gioi_thieu)

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 10))
        
        # --- Frame Nhập Liệu ---
        frame_nhap = ttk.LabelFrame(self.root, text="Nhập / Sửa Dữ Liệu Nhân Viên", padding=15)
        frame_nhap.pack(fill=tk.X, padx=15, pady=10)
        
        # Hàng 1
        ttk.Label(frame_nhap, text="Mã NV:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_ma = ttk.Entry(frame_nhap, width=15)
        self.entry_ma.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Tên NV:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_ten = ttk.Entry(frame_nhap, width=25)
        self.entry_ten.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Tháng/Năm (MM/YYYY):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_thang = ttk.Entry(frame_nhap, width=15)
        self.entry_thang.grid(row=0, column=5, padx=5, pady=5)
        
        # Hàng 2
        ttk.Label(frame_nhap, text="Trình độ:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_trinh_do = ttk.Combobox(frame_nhap, width=13, state="readonly")
        self.combo_trinh_do['values'] = ("Sơ cấp", "Trung cấp", "Cao đẳng", "Đại học", "Cử nhân", "Kỹ sư")
        self.combo_trinh_do.set("Đại học")
        self.combo_trinh_do.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Thâm niên (Năm):").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_tham_nien = ttk.Entry(frame_nhap, width=25)
        self.entry_tham_nien.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Lương cơ sở (VNĐ):").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_lcb = ttk.Entry(frame_nhap, width=15)
        self.entry_lcb.grid(row=1, column=5, padx=5, pady=5)

        # Hàng 3
        ttk.Label(frame_nhap, text="Bộ phận:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.combo_bo_phan = ttk.Combobox(frame_nhap, width=13)
        self.combo_bo_phan['values'] = ("Nhân sự", "Kế toán", "IT", "Sản xuất", "Marketing", "Kinh doanh")
        self.combo_bo_phan.set("IT")
        self.combo_bo_phan.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_nhap, text="Ca làm:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.combo_ca_lam = ttk.Combobox(frame_nhap, width=23, state="readonly")
        self.combo_ca_lam['values'] = ("Sáng", "Chiều", "Đêm", "Hành chính")
        self.combo_ca_lam.set("Hành chính")
        self.combo_ca_lam.grid(row=2, column=3, padx=5, pady=5)

        ttk.Label(frame_nhap, text="Số giờ làm (Tiêu chuẩn):").grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_so_gio_lam = ttk.Entry(frame_nhap, width=15)
        self.entry_so_gio_lam.grid(row=2, column=5, padx=5, pady=5)
        
        # Hàng 4
        ttk.Label(frame_nhap, text="Thưởng (VNĐ):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_thuong = ttk.Entry(frame_nhap, width=15)
        self.entry_thuong.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Phạt (VNĐ):").grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
        self.entry_phat = ttk.Entry(frame_nhap, width=25)
        self.entry_phat.grid(row=3, column=3, padx=5, pady=5)
        
        ttk.Label(frame_nhap, text="Ghi chú phạt:").grid(row=3, column=4, padx=5, pady=5, sticky=tk.W)
        self.entry_ghi_chu = ttk.Entry(frame_nhap, width=15)
        self.entry_ghi_chu.grid(row=3, column=5, padx=5, pady=5)
        
        # Hàng 5: Giờ làm thêm và Nút bấm
        ttk.Label(frame_nhap, text="Giờ làm thêm:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.entry_gio_lam_them = ttk.Entry(frame_nhap, width=15)
        self.entry_gio_lam_them.grid(row=4, column=1, padx=5, pady=5)
        
        frame_buttons = ttk.Frame(frame_nhap)
        frame_buttons.grid(row=4, column=3, columnspan=3, pady=10, sticky=tk.E)
        
        btn_lam_moi = ttk.Button(frame_buttons, text="Trở lại ban đầu", command=self.xoa_trang_form)
        btn_lam_moi.pack(side=tk.LEFT, padx=5)
        
        btn_them = ttk.Button(frame_buttons, text="Thêm Mới", command=self.on_add_click)
        btn_them.pack(side=tk.LEFT, padx=5)
        
        btn_sua = ttk.Button(frame_buttons, text="Cập nhật (Sửa)", command=self.on_update_click)
        btn_sua.pack(side=tk.LEFT, padx=5)
        
        btn_xoa = ttk.Button(frame_buttons, text="Xóa", command=self.on_delete_click)
        btn_xoa.pack(side=tk.LEFT, padx=5)
        
        # --- Frame Bảng Dữ Liệu ---
        frame_bang = ttk.LabelFrame(self.root, text="Bảng Lương Chi Tiết", padding=15)
        frame_bang.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        
        # Bổ sung ID (ẩn) và Thuế TNCN
        self.columns = ('ID', 'Mã NV', 'Tên NV', 'Bộ phận', 'Ca', 'Trình độ', 'Thâm niên', 'Bậc', 'HSL', 'Lương cơ sở', 'Số giờ', 'Lương CB', 'Tháng', 'Thưởng', 'Phạt', 'Ghi chú', 'Giờ TC', 'Thuế TNCN', 'Thực nhận', 'Tăng trưởng')
        self.tree = ttk.Treeview(frame_bang, columns=self.columns, show='headings', height=10)
        
        # Cấu hình ID ẩn đi
        self.tree.heading('ID', text='ID')
        self.tree.column('ID', width=0, stretch=tk.NO)
        
        # Cấu hình chiều rộng các cột khác
        widths = [0, 50, 110, 70, 50, 70, 60, 40, 40, 80, 50, 80, 60, 70, 70, 90, 50, 70, 90, 80]
        for i, col in enumerate(self.columns):
            if col != 'ID':
                self.tree.heading(col, text=col)
                self.tree.column(col, width=widths[i], anchor=tk.CENTER)
            
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bắt sự kiện chọn dòng trên Treeview
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        
        scrollbar = ttk.Scrollbar(frame_bang, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # --- Frame Thống Kê ---
        frame_thong_ke = ttk.LabelFrame(self.root, text="Báo Cáo Tổng Quan", padding=15)
        frame_thong_ke.pack(fill=tk.X, padx=15, pady=10)
        
        self.lbl_tong_luong = ttk.Label(frame_thong_ke, text="Tổng quỹ lương: 0 VNĐ", font=("Arial", 11, "bold"), foreground="blue")
        self.lbl_tong_luong.grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
        
        self.lbl_luong_tb = ttk.Label(frame_thong_ke, text="Lương trung bình: 0 VNĐ", font=("Arial", 11, "bold"), foreground="blue")
        self.lbl_luong_tb.grid(row=0, column=1, padx=20, pady=5, sticky=tk.W)
        
        self.lbl_gio_lam_them = ttk.Label(frame_thong_ke, text="Tổng giờ làm thêm: 0", font=("Arial", 11, "bold"), foreground="#d9534f")
        self.lbl_gio_lam_them.grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)
        
        self.lbl_tang_truong = ttk.Label(frame_thong_ke, text="Tỷ lệ tăng trưởng trung bình: 0%", font=("Arial", 11, "bold"), foreground="#5cb85c")
        self.lbl_tang_truong.grid(row=1, column=1, padx=20, pady=5, sticky=tk.W)

    def xoa_trang_form(self):
        self.current_selected_id = None
        for item in self.tree.selection():
            self.tree.selection_remove(item)
        self.entry_ma.delete(0, tk.END)
        self.entry_ten.delete(0, tk.END)
        self.entry_thang.delete(0, tk.END)
        self.combo_bo_phan.set("IT")
        self.combo_ca_lam.set("Hành chính")
        self.combo_trinh_do.set("Đại học")
        self.entry_tham_nien.delete(0, tk.END)
        self.entry_lcb.delete(0, tk.END)
        self.entry_so_gio_lam.delete(0, tk.END)
        self.entry_thuong.delete(0, tk.END)
        self.entry_phat.delete(0, tk.END)
        self.entry_ghi_chu.delete(0, tk.END)
        self.entry_gio_lam_them.delete(0, tk.END)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
            
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Điền dữ liệu ngược lên form
        self.xoa_trang_form()
        self.current_selected_id = values[0]
        
        self.entry_ma.insert(0, values[1])
        self.entry_ten.insert(0, values[2])
        self.combo_bo_phan.set(values[3])
        self.combo_ca_lam.set(values[4])
        self.combo_trinh_do.set(values[5])
        self.entry_tham_nien.insert(0, values[6])
        
        # Bỏ dấu phẩy ở lương để hiển thị số gốc
        lcb = str(values[9]).replace(',', '')
        self.entry_lcb.insert(0, lcb)
        
        self.entry_so_gio_lam.insert(0, values[10])
        self.entry_thang.insert(0, values[12])
        
        thuong = str(values[13]).replace(',', '')
        self.entry_thuong.insert(0, thuong)
        
        phat = str(values[14]).replace(',', '')
        self.entry_phat.insert(0, phat)
        
        ghi_chu = "" if values[15] == "None" else values[15]
        self.entry_ghi_chu.insert(0, ghi_chu)
        
        self.entry_gio_lam_them.insert(0, values[16])

    def collect_form_data(self):
        try:
            ma = self.entry_ma.get().strip()
            ten = self.entry_ten.get().strip()
            thang = self.entry_thang.get().strip()
            bo_phan = self.combo_bo_phan.get().strip()
            ca_lam = self.combo_ca_lam.get().strip()
            trinh_do = self.combo_trinh_do.get()
            ghi_chu = self.entry_ghi_chu.get().strip()
            
            if not ma or not ten or not thang or not bo_phan or not ca_lam:
                messagebox.showerror("Lỗi Nhập Liệu", "Vui lòng nhập đầy đủ các trường bắt buộc (Mã, Tên, Tháng/Năm, Bộ phận, Ca làm)!")
                return None
                
            tham_nien = float(self.entry_tham_nien.get().strip())
            lcb = float(self.entry_lcb.get().strip())
            so_gio = float(self.entry_so_gio_lam.get().strip())
            thuong = float(self.entry_thuong.get() or 0)
            phat = float(self.entry_phat.get() or 0)
            gio_them = float(self.entry_gio_lam_them.get() or 0)
                
            return {
                "Mã NV": ma, "Tên NV": ten, "Bộ phận": bo_phan, "Ca làm": ca_lam,
                "Tháng/Năm": thang, "Trình độ": trinh_do, "Thâm niên": tham_nien,
                "Lương cơ sở": lcb, "Số giờ làm": so_gio, "Thưởng": thuong,
                "Phạt": phat, "Ghi chú phạt": ghi_chu, "Giờ làm thêm": gio_them
            }
        except ValueError:
            messagebox.showerror("Lỗi Định Dạng", "Thâm niên, Lương, Giờ làm, Thưởng, Phạt phải là SỐ hợp lệ!")
            return None

    def on_add_click(self):
        data = self.collect_form_data()
        if data:
            self.controller.add_employee(data)

    def on_update_click(self):
        if not self.current_selected_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên từ bảng để sửa!")
            return
            
        data = self.collect_form_data()
        if data:
            self.controller.update_employee(self.current_selected_id, data)

    def on_delete_click(self):
        if not self.current_selected_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên từ bảng để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa dữ liệu này?"):
            self.controller.delete_employee(self.current_selected_id)

    def update_treeview(self, df):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        if df is None or df.empty:
            return
            
        for _, row in df.iterrows():
            ghi_chu_val = str(row.get('Ghi chú phạt', ''))
            
            self.tree.insert("", "end", values=(
                row['id'],
                row['Mã NV'], 
                row['Tên NV'], 
                row.get('Bộ phận', ''),
                row.get('Ca làm', ''),
                row['Trình độ'], 
                f"{row['Thâm niên']}", 
                f"Bậc {row.get('Bậc', '')}",
                row.get('HSL', ''),
                f"{row['Lương cơ sở']:,.0f}", 
                row.get('Số giờ làm', 0),
                f"{row.get('Lương cơ bản', 0):,.0f}", 
                row['Tháng/Năm'], 
                f"{row['Thưởng']:,.0f}", 
                f"{row['Phạt']:,.0f}", 
                ghi_chu_val,
                row['Giờ làm thêm'], 
                f"{row.get('Thuế TNCN', 0):,.0f}",
                f"{row.get('Lương thực nhận', 0):,.0f}", 
                f"{row.get('Tăng trưởng (%)', 0)}%"
            ))

    def update_statistics(self, stats):
        self.lbl_tong_luong.config(text=f"Tổng quỹ lương: {stats['tong_luong']:,.0f} VNĐ")
        self.lbl_luong_tb.config(text=f"Lương trung bình: {stats['luong_tb']:,.0f} VNĐ")
        self.lbl_gio_lam_them.config(text=f"Tổng giờ làm thêm: {stats['tong_gio_lam_them']} giờ")
        self.lbl_tang_truong.config(text=f"Tỷ lệ tăng trưởng TB: {stats['ty_le_tang_truong_tb']:.2f}%")

    def show_info(self, title, message):
        messagebox.showinfo(title, message, parent=self.root)

    def show_error(self, title, message):
        messagebox.showerror(title, message, parent=self.root)

    # --- Cửa sổ phụ ---
    def mo_cua_so_import(self):
        win_import = tk.Toplevel(self.root)
        win_import.title("Import dữ liệu từ CSV")
        win_import.geometry("400x200")
        
        ttk.Label(win_import, text="Vui lòng chọn file CSV chứa dữ liệu.", font=("Arial", 10)).pack(pady=20)
        lbl_file = ttk.Label(win_import, text="Chưa chọn file nào", foreground="gray")
        lbl_file.pack(pady=5)
        
        filepath = tk.StringVar()
        
        def chon_file():
            path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if path:
                filepath.set(path)
                lbl_file.config(text=os.path.basename(path), foreground="blue")
                
        def thuc_hien_import():
            path = filepath.get()
            if not path:
                messagebox.showerror("Lỗi", "Vui lòng chọn file trước!", parent=win_import)
                return
            self.controller.import_csv(path, win_import)

        btn_chon = ttk.Button(win_import, text="Duyệt File...", command=chon_file)
        btn_chon.pack(pady=5)
        btn_import = ttk.Button(win_import, text="Import Dữ Liệu", command=thuc_hien_import)
        btn_import.pack(pady=10)

    def mo_cua_so_tim_kiem(self):
        win_search = tk.Toplevel(self.root)
        win_search.title("Tìm kiếm nhân viên")
        win_search.geometry("450x150")
        
        frame = ttk.Frame(win_search, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Nhập Tên hoặc Mã NV:").grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        entry_tk = ttk.Entry(frame, width=30)
        entry_tk.grid(row=0, column=1, padx=5, pady=10)
        
        def thuc_hien_tim():
            tu_khoa = entry_tk.get().strip()
            self.controller.search_employees(tu_khoa, win_search)
                
        btn_tim = ttk.Button(frame, text="Tìm kiếm", command=thuc_hien_tim)
        btn_tim.grid(row=1, column=0, columnspan=2, pady=15)

    def mo_cua_so_gioi_thieu(self):
        win_about = tk.Toplevel(self.root)
        win_about.title("Giới thiệu phần mềm")
        win_about.geometry("350x200")
        
        ttk.Label(win_about, text="Phần Mềm Quản Lý Lương Nhân Viên", font=("Arial", 12, "bold"), foreground="blue").pack(pady=15)
        ttk.Label(win_about, text="Phiên bản: 2.0.0 (MVC, SQLite)", font=("Arial", 10)).pack(pady=5)
        ttk.Label(win_about, text="Hỗ trợ: Python 3, Tkinter, Pandas", font=("Arial", 10)).pack(pady=5)
        ttk.Label(win_about, text="Bản quyền © 2026", font=("Arial", 10)).pack(pady=5)
        
        btn_dong = ttk.Button(win_about, text="Đóng", command=win_about.destroy)
        btn_dong.pack(pady=15)
