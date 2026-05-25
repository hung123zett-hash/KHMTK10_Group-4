import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

widgets = {}

def create_menu(root, callbacks):
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    chuc_nang_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Chức Năng", menu=chuc_nang_menu)
    chuc_nang_menu.add_command(label="Import CSV", command=callbacks.get('mo_cua_so_import'))
    chuc_nang_menu.add_command(label="Export CSV", command=callbacks.get('export_csv_action'))
    chuc_nang_menu.add_command(label="Thêm 10 NV mẫu", command=callbacks.get('them_10_nv_mau'))
    chuc_nang_menu.add_command(label="Tìm kiếm dữ liệu", command=callbacks.get('mo_cua_so_tim_kiem'))
    chuc_nang_menu.add_command(label="Hiển thị tất cả", command=callbacks.get('load_data'))
    chuc_nang_menu.add_separator()
    chuc_nang_menu.add_command(label="Thoát", command=root.quit)
    
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Trợ giúp", menu=help_menu)
    help_menu.add_command(label="Giới thiệu phần mềm", command=callbacks.get('mo_cua_so_gioi_thieu'))

def create_widgets(root, callbacks):
    global widgets
    
    style = ttk.Style()
    style.configure("TButton", padding=6, font=("Arial", 10))
    style.configure("TLabel", font=("Arial", 10))
    
    frame_nhap = ttk.LabelFrame(root, text="Nhập / Sửa Dữ Liệu Nhân Viên", padding=15)
    frame_nhap.pack(fill=tk.X, padx=15, pady=10)
    
    # Hàng 1
    ttk.Label(frame_nhap, text="Mã NV:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    entry_ma = ttk.Entry(frame_nhap, width=15)
    entry_ma.grid(row=0, column=1, padx=5, pady=5)
    widgets['entry_ma'] = entry_ma
    
    ttk.Label(frame_nhap, text="Tên NV:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    entry_ten = ttk.Entry(frame_nhap, width=25)
    entry_ten.grid(row=0, column=3, padx=5, pady=5)
    widgets['entry_ten'] = entry_ten
    
    ttk.Label(frame_nhap, text="Tháng/Năm (MM/YYYY):").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
    entry_thang = ttk.Entry(frame_nhap, width=15)
    entry_thang.grid(row=0, column=5, padx=5, pady=5)
    widgets['entry_thang'] = entry_thang
    
    # Hàng 2
    ttk.Label(frame_nhap, text="Bộ phận:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    combo_bo_phan = ttk.Combobox(frame_nhap, width=13)
    combo_bo_phan['values'] = ("Nhân sự", "Kế toán", "IT", "Sản xuất", "Marketing", "Kinh doanh")
    combo_bo_phan.set("IT")
    combo_bo_phan.grid(row=1, column=1, padx=5, pady=5)
    widgets['combo_bo_phan'] = combo_bo_phan

    ttk.Label(frame_nhap, text="Ca làm:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    combo_ca_lam = ttk.Combobox(frame_nhap, width=23, state="readonly")
    combo_ca_lam['values'] = ("Hành chính (7h30-16h30)", "Ca 1 (6h-14h)", "Ca 2 (14h-22h)", "Ca 3 (22h-6h)")
    combo_ca_lam.set("Hành chính (7h30-16h30)")
    combo_ca_lam.grid(row=1, column=3, padx=5, pady=5)
    widgets['combo_ca_lam'] = combo_ca_lam

    ttk.Label(frame_nhap, text="Lương cơ sở (VNĐ):").grid(row=1, column=4, padx=5, pady=5, sticky=tk.W)
    entry_lcb = ttk.Entry(frame_nhap, width=15)
    entry_lcb.grid(row=1, column=5, padx=5, pady=5)
    widgets['entry_lcb'] = entry_lcb

    # Hàng 3
    ttk.Label(frame_nhap, text="Số giờ làm (Tiêu chuẩn):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    entry_so_gio_lam = ttk.Entry(frame_nhap, width=15)
    entry_so_gio_lam.grid(row=2, column=1, padx=5, pady=5)
    widgets['entry_so_gio_lam'] = entry_so_gio_lam
    
    ttk.Label(frame_nhap, text="Thưởng (VNĐ):").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    entry_thuong = ttk.Entry(frame_nhap, width=25)
    entry_thuong.grid(row=2, column=3, padx=5, pady=5)
    widgets['entry_thuong'] = entry_thuong
    
    ttk.Label(frame_nhap, text="Phạt (VNĐ):").grid(row=2, column=4, padx=5, pady=5, sticky=tk.W)
    entry_phat = ttk.Entry(frame_nhap, width=15)
    entry_phat.grid(row=2, column=5, padx=5, pady=5)
    widgets['entry_phat'] = entry_phat
    
    # Hàng 4
    ttk.Label(frame_nhap, text="Ghi chú phạt:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    entry_ghi_chu = ttk.Entry(frame_nhap, width=15)
    entry_ghi_chu.grid(row=3, column=1, padx=5, pady=5)
    widgets['entry_ghi_chu'] = entry_ghi_chu
    
    ttk.Label(frame_nhap, text="Giờ làm thêm:").grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    entry_gio_lam_them = ttk.Entry(frame_nhap, width=25)
    entry_gio_lam_them.grid(row=3, column=3, padx=5, pady=5)
    widgets['entry_gio_lam_them'] = entry_gio_lam_them
    
    # Hàng 5: Nút bấm
    frame_buttons = ttk.Frame(frame_nhap)
    frame_buttons.grid(row=4, column=3, columnspan=3, pady=10, sticky=tk.E)
    
    btn_lam_moi = ttk.Button(frame_buttons, text="Trở lại ban đầu", command=callbacks.get('xoa_trang_form'))
    btn_lam_moi.pack(side=tk.LEFT, padx=5)
    
    btn_them = ttk.Button(frame_buttons, text="Thêm Mới", command=callbacks.get('on_add_click'))
    btn_them.pack(side=tk.LEFT, padx=5)
    
    btn_sua = ttk.Button(frame_buttons, text="Cập nhật (Sửa)", command=callbacks.get('on_update_click'))
    btn_sua.pack(side=tk.LEFT, padx=5)
    
    btn_xoa = ttk.Button(frame_buttons, text="Xóa", command=callbacks.get('on_delete_click'))
    btn_xoa.pack(side=tk.LEFT, padx=5)
    
    # --- Frame Bảng Dữ Liệu ---
    frame_bang = ttk.LabelFrame(root, text="Bảng Lương Chi Tiết", padding=15)
    frame_bang.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
    
    columns = ('ID', 'Mã NV', 'Tên NV', 'Bộ phận', 'Ca', 'Lương cơ sở', 'Số giờ', 'Tháng', 'Thưởng', 'Phạt', 'Ghi chú', 'Giờ TC', 'Tiền làm thêm', 'Thực nhận')
    tree = ttk.Treeview(frame_bang, columns=columns, show='headings', height=10)
    widgets['tree'] = tree
    
    tree.heading('ID', text='ID')
    tree.column('ID', width=0, stretch=tk.NO)
    
    widths = [0, 60, 140, 80, 140, 90, 60, 70, 90, 90, 120, 60, 90, 100]
    for i, col in enumerate(columns):
        if col != 'ID':
            tree.heading(col, text=col)
            # Make columns fixed size and nicely aligned
            tree.column(col, width=widths[i], minwidth=widths[i], stretch=tk.NO, anchor=tk.CENTER)
            
    h_scrollbar = ttk.Scrollbar(frame_bang, orient=tk.HORIZONTAL, command=tree.xview)
    h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    v_scrollbar = ttk.Scrollbar(frame_bang, orient=tk.VERTICAL, command=tree.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Bắt sự kiện lăn chuột để cuộn bảng
    tree.bind('<MouseWheel>', lambda e: tree.yview_scroll(int(-1*(e.delta/120)), "units"))
    tree.bind('<Shift-MouseWheel>', lambda e: tree.xview_scroll(int(-1*(e.delta/120)), "units"))
    
    # Chặn người dùng dùng chuột kéo dãn/thu hẹp các cột
    def prevent_resize(event):
        if tree.identify_region(event.x, event.y) == "separator":
            return "break"
    tree.bind('<Button-1>', prevent_resize)
    
    tree.bind('<<TreeviewSelect>>', callbacks.get('on_tree_select'))
    
    # --- Frame Thống Kê ---
    frame_thong_ke = ttk.LabelFrame(root, text="Báo Cáo Tổng Quan", padding=15)
    frame_thong_ke.pack(fill=tk.X, padx=15, pady=10)
    
    lbl_tong_luong = ttk.Label(frame_thong_ke, text="Tổng quỹ lương: 0 VNĐ", font=("Arial", 11, "bold"), foreground="blue")
    lbl_tong_luong.grid(row=0, column=0, padx=20, pady=5, sticky=tk.W)
    widgets['lbl_tong_luong'] = lbl_tong_luong
    
    lbl_luong_tb = ttk.Label(frame_thong_ke, text="Lương trung bình: 0 VNĐ", font=("Arial", 11, "bold"), foreground="blue")
    lbl_luong_tb.grid(row=0, column=1, padx=20, pady=5, sticky=tk.W)
    widgets['lbl_luong_tb'] = lbl_luong_tb
    
    lbl_gio_lam_them = ttk.Label(frame_thong_ke, text="Tổng giờ làm thêm: 0", font=("Arial", 11, "bold"), foreground="#d9534f")
    lbl_gio_lam_them.grid(row=1, column=0, padx=20, pady=5, sticky=tk.W)
    widgets['lbl_gio_lam_them'] = lbl_gio_lam_them

def xoa_trang_form():
    for item in widgets['tree'].selection():
        widgets['tree'].selection_remove(item)
    widgets['entry_ma'].delete(0, tk.END)
    widgets['entry_ten'].delete(0, tk.END)
    widgets['entry_thang'].delete(0, tk.END)
    widgets['combo_bo_phan'].set("IT")
    widgets['combo_ca_lam'].set("Hành chính (7h30-16h30)")
    widgets['entry_lcb'].delete(0, tk.END)
    widgets['entry_so_gio_lam'].delete(0, tk.END)
    widgets['entry_thuong'].delete(0, tk.END)
    widgets['entry_phat'].delete(0, tk.END)
    widgets['entry_ghi_chu'].delete(0, tk.END)
    widgets['entry_gio_lam_them'].delete(0, tk.END)

def fill_form(values):
    xoa_trang_form()
    widgets['entry_ma'].insert(0, values[1])
    widgets['entry_ten'].insert(0, values[2])
    widgets['combo_bo_phan'].set(values[3])
    widgets['combo_ca_lam'].set(values[4])
    
    lcb = str(values[5]).replace(',', '')
    widgets['entry_lcb'].insert(0, lcb)
    
    widgets['entry_so_gio_lam'].insert(0, values[6])
    widgets['entry_thang'].insert(0, values[7])
    
    thuong = str(values[8]).replace(',', '')
    widgets['entry_thuong'].insert(0, thuong)
    
    phat = str(values[9]).replace(',', '')
    widgets['entry_phat'].insert(0, phat)
    
    ghi_chu = "" if values[10] == "None" else values[10]
    widgets['entry_ghi_chu'].insert(0, ghi_chu)
    
    widgets['entry_gio_lam_them'].insert(0, values[11])

def collect_form_data(root):
    try:
        ma = widgets['entry_ma'].get().strip()
        ten = widgets['entry_ten'].get().strip()
        thang = widgets['entry_thang'].get().strip()
        bo_phan = widgets['combo_bo_phan'].get().strip()
        ca_lam = widgets['combo_ca_lam'].get().strip()
        ghi_chu = widgets['entry_ghi_chu'].get().strip()
        
        if not ma or not ten or not thang or not bo_phan or not ca_lam:
            messagebox.showerror("Lỗi Nhập Liệu", "Vui lòng nhập đầy đủ các trường bắt buộc (Mã, Tên, Tháng/Năm, Bộ phận, Ca làm)!", parent=root)
            return None
            
        lcb = float(widgets['entry_lcb'].get().strip())
        so_gio = float(widgets['entry_so_gio_lam'].get().strip())
        thuong = float(widgets['entry_thuong'].get() or 0)
        phat = float(widgets['entry_phat'].get() or 0)
        gio_them = float(widgets['entry_gio_lam_them'].get() or 0)
            
        return {
            "Mã NV": ma, "Tên NV": ten, "Bộ phận": bo_phan, "Ca làm": ca_lam,
            "Tháng/Năm": thang, "Lương cơ sở": lcb, "Số giờ làm": so_gio, "Thưởng": thuong,
            "Phạt": phat, "Ghi chú phạt": ghi_chu, "Giờ làm thêm": gio_them
        }
    except ValueError:
        messagebox.showerror("Lỗi Định Dạng", "Lương, Giờ làm, Thưởng, Phạt phải là SỐ hợp lệ!", parent=root)
        return None

def update_treeview(df):
    for row in widgets['tree'].get_children():
        widgets['tree'].delete(row)
        
    if df is None or df.empty:
        return
        
    for _, row in df.iterrows():
        ghi_chu_val = str(row.get('Ghi chú phạt', ''))
        
        widgets['tree'].insert("", "end", values=(
            row['id'],
            row['Mã NV'], 
            row['Tên NV'], 
            row.get('Bộ phận', ''),
            row.get('Ca làm', ''),
            f"{row['Lương cơ sở']:,.0f}",
            row.get('Số giờ làm', 0),
            row['Tháng/Năm'], 
            f"{row['Thưởng']:,.0f}", 
            f"{row['Phạt']:,.0f}", 
            ghi_chu_val,
            row['Giờ làm thêm'], 
            f"{row.get('Tiền làm thêm', 0):,.0f}",
            f"{row.get('Lương thực nhận', 0):,.0f}"
        ))

def update_statistics(stats):
    widgets['lbl_tong_luong'].config(text=f"Tổng quỹ lương: {stats['tong_luong']:,.0f} VNĐ")
    widgets['lbl_luong_tb'].config(text=f"Lương trung bình: {stats['luong_tb']:,.0f} VNĐ")
    widgets['lbl_gio_lam_them'].config(text=f"Tổng giờ làm thêm: {stats['tong_gio_lam_them']} giờ")
