import pandas as pd
from tkinter import messagebox, filedialog, Toplevel, StringVar
from tkinter import ttk
import os

import model
import view

current_selected_id = None
current_df = None
root_ref = None

def load_data():
    global current_df
    try:
        df = model.get_all_employees()
        current_df = df
        view.update_treeview(df)
        
        stats = model.get_statistics(df)
        view.update_statistics(stats)
    except Exception as e:
        messagebox.showerror("Lỗi Tải Dữ Liệu", f"Không thể tải dữ liệu từ CSDL:\n{e}", parent=root_ref)

def on_add_click():
    data = view.collect_form_data(root_ref)
    if data:
        if model.is_duplicate_ma_nv(data['Mã NV']):
            messagebox.showwarning("Cảnh báo", f"Mã nhân viên {data['Mã NV']} đã tồn tại! Vui lòng nhập mã khác.", parent=root_ref)
            return
            
        try:
            model.add_employee_db(data)
            view.xoa_trang_form()
            load_data()
            messagebox.showinfo("Thành công", f"Đã thêm mới nhân viên {data['Tên NV']} thành công!", parent=root_ref)
        except Exception as e:
            messagebox.showerror("Lỗi Thêm Mới", f"Không thể thêm dữ liệu:\n{e}", parent=root_ref)

def on_update_click():
    global current_selected_id
    if not current_selected_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên từ bảng để sửa!", parent=root_ref)
        return
        
    data = view.collect_form_data(root_ref)
    if data:
        if model.is_duplicate_ma_nv(data['Mã NV'], current_selected_id):
            messagebox.showwarning("Cảnh báo", f"Mã nhân viên {data['Mã NV']} đã tồn tại ở một bản ghi khác!", parent=root_ref)
            return
            
        try:
            model.update_employee_db(current_selected_id, data)
            view.xoa_trang_form()
            load_data()
            messagebox.showinfo("Thành công", "Đã cập nhật dữ liệu thành công!", parent=root_ref)
        except Exception as e:
            messagebox.showerror("Lỗi Cập Nhật", f"Không thể cập nhật dữ liệu:\n{e}", parent=root_ref)

def on_delete_click():
    global current_selected_id
    if not current_selected_id:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên từ bảng để xóa!", parent=root_ref)
        return
        
    if messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa dữ liệu này?", parent=root_ref):
        try:
            model.delete_employee_db(current_selected_id)
            view.xoa_trang_form()
            load_data()
            messagebox.showinfo("Thành công", "Đã xóa dữ liệu thành công!", parent=root_ref)
        except Exception as e:
            messagebox.showerror("Lỗi Xóa", f"Không thể xóa dữ liệu:\n{e}", parent=root_ref)

def on_tree_select(event):
    global current_selected_id
    selected = view.widgets['tree'].selection()
    if not selected:
        return
        
    item = view.widgets['tree'].item(selected[0])
    values = item['values']
    current_selected_id = values[0]
    
    view.fill_form(values)

def search_employees_action(keyword, window):
    global current_df
    if not keyword:
        load_data()
        window.destroy()
        return
        
    try:
        df = model.search_employees_db(keyword)
        if df.empty:
            messagebox.showinfo("Kết quả", "Không tìm thấy nhân viên nào phù hợp!", parent=window)
        else:
            current_df = df
            view.update_treeview(df)
            messagebox.showinfo("Kết quả", f"Tìm thấy {len(df)} kết quả.", parent=window)
            window.destroy()
    except Exception as e:
        messagebox.showerror("Lỗi Tìm Kiếm", f"Có lỗi xảy ra:\n{e}", parent=window)

def mo_cua_so_tim_kiem():
    win_search = Toplevel(root_ref)
    win_search.title("Tìm kiếm nhân viên")
    win_search.geometry("450x150")
    
    frame = ttk.Frame(win_search, padding=20)
    frame.pack(fill='both', expand=True)
    
    ttk.Label(frame, text="Nhập Tên hoặc Mã NV:").grid(row=0, column=0, padx=5, pady=10, sticky='w')
    entry_tk = ttk.Entry(frame, width=30)
    entry_tk.grid(row=0, column=1, padx=5, pady=10)
    
    def thuc_hien_tim():
        tu_khoa = entry_tk.get().strip()
        search_employees_action(tu_khoa, win_search)
            
    btn_tim = ttk.Button(frame, text="Tìm kiếm", command=thuc_hien_tim)
    btn_tim.grid(row=1, column=0, columnspan=2, pady=15)

def import_csv_action(path, window):
    try:
        df = pd.read_csv(path)
        du_lieu_csv = df.to_dict('records')
        
        existing_df = model.get_all_employees()
        existing_ma_nv = set(existing_df['Mã NV']) if not existing_df.empty else set()
        
        unique_records = []
        for item in du_lieu_csv:
            for k in item:
                if pd.isna(item[k]):
                    item[k] = "" if isinstance(item[k], str) else 0
            
            ma_nv = item.get('Mã NV')
            if ma_nv and ma_nv not in existing_ma_nv:
                unique_records.append(item)
                existing_ma_nv.add(ma_nv)
                    
        if not unique_records:
            messagebox.showwarning("Cảnh báo", "Không có dữ liệu mới nào được import (Tất cả mã NV đã tồn tại)!", parent=window)
            return

        model.add_many_employees_db(unique_records)
        load_data()
        messagebox.showinfo("Thành công", f"Đã import thành công {len(unique_records)} dòng dữ liệu mới!", parent=window)
        window.destroy()
    except Exception as e:
        messagebox.showerror("Lỗi Import", f"Có lỗi xảy ra khi đọc file CSV:\n{e}", parent=window)

def mo_cua_so_import():
    win_import = Toplevel(root_ref)
    win_import.title("Import dữ liệu từ CSV")
    win_import.geometry("400x200")
    
    ttk.Label(win_import, text="Vui lòng chọn file CSV chứa dữ liệu.", font=("Arial", 10)).pack(pady=20)
    lbl_file = ttk.Label(win_import, text="Chưa chọn file nào", foreground="gray")
    lbl_file.pack(pady=5)
    
    filepath = StringVar()
    
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
        import_csv_action(path, win_import)

    btn_chon = ttk.Button(win_import, text="Duyệt File...", command=chon_file)
    btn_chon.pack(pady=5)
    btn_import = ttk.Button(win_import, text="Import Dữ Liệu", command=thuc_hien_import)
    btn_import.pack(pady=10)

def export_csv_action():
    global current_df
    if current_df is None or current_df.empty:
        messagebox.showerror("Lỗi Export", "Không có dữ liệu để xuất!", parent=root_ref)
        return
        
    try:
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Lưu file xuất CSV"
        )
        
        if not path:
            return
            
        export_df = current_df.drop(columns=['id'], errors='ignore')
        export_df.to_csv(path, index=False, encoding='utf-8-sig')
        
        messagebox.showinfo("Thành công", f"Đã xuất file dữ liệu tới:\n{path}", parent=root_ref)
    except Exception as e:
        messagebox.showerror("Lỗi Export", f"Có lỗi khi lưu file:\n{e}", parent=root_ref)

def mo_cua_so_gioi_thieu():
    win_about = Toplevel(root_ref)
    win_about.title("Giới thiệu phần mềm")
    win_about.geometry("350x200")
    
    ttk.Label(win_about, text="Phần Mềm Quản Lý Lương Nhân Viên", font=("Arial", 12, "bold"), foreground="blue").pack(pady=15)
    ttk.Label(win_about, text="Phiên bản: 3.0.0 (MVC, Functions)", font=("Arial", 10)).pack(pady=5)
    ttk.Label(win_about, text="Hỗ trợ: Python 3, Tkinter, Pandas", font=("Arial", 10)).pack(pady=5)
    ttk.Label(win_about, text="Bản quyền © 2026", font=("Arial", 10)).pack(pady=5)
    
    btn_dong = ttk.Button(win_about, text="Đóng", command=win_about.destroy)
    btn_dong.pack(pady=15)

def them_10_nv_mau():
    try:
        # Get all existing employees to see which ones are already added
        existing_df = model.get_all_employees()
        existing_ma_nv = set()
        if not existing_df.empty:
            existing_ma_nv = set(existing_df['Mã NV'])
            
        records = [
            {"Mã NV": "NV04", "Tên NV": "Phạm Văn D", "Bộ phận": "Kinh doanh", "Ca làm": "Hành chính (7h30-16h30)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 168, "Thưởng": 800000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 8},
            {"Mã NV": "NV05", "Tên NV": "Hoàng Thị E", "Bộ phận": "Marketing", "Ca làm": "Ca 1 (6h-14h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 172, "Thưởng": 600000, "Phạt": 50000, "Ghi chú phạt": "Đi muộn", "Giờ làm thêm": 4},
            {"Mã NV": "NV06", "Tên NV": "Ngô Văn F", "Bộ phận": "Sản xuất", "Ca làm": "Ca 2 (14h-22h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 180, "Thưởng": 400000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 12},
            {"Mã NV": "NV07", "Tên NV": "Đỗ Thị G", "Bộ phận": "Kế toán", "Ca làm": "Hành chính (7h30-16h30)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 160, "Thưởng": 500000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 0},
            {"Mã NV": "NV08", "Tên NV": "Bùi Văn H", "Bộ phận": "IT", "Ca làm": "Ca 3 (22h-6h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 176, "Thưởng": 1200000, "Phạt": 100000, "Ghi chú phạt": "Lỗi quy trình", "Giờ làm thêm": 15},
            {"Mã NV": "NV09", "Tên NV": "Vũ Thị I", "Bộ phận": "Nhân sự", "Ca làm": "Ca 1 (6h-14h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 168, "Thưởng": 300000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 2},
            {"Mã NV": "NV10", "Tên NV": "Phan Văn J", "Bộ phận": "Kinh doanh", "Ca làm": "Ca 2 (14h-22h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 170, "Thưởng": 700000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 6},
            {"Mã NV": "NV11", "Tên NV": "Lê Thị K", "Bộ phận": "Marketing", "Ca làm": "Hành chính (7h30-16h30)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 160, "Thưởng": 200000, "Phạt": 20000, "Ghi chú phạt": "Quên chấm công", "Giờ làm thêm": 0},
            {"Mã NV": "NV12", "Tên NV": "Trịnh Văn L", "Bộ phận": "Sản xuất", "Ca làm": "Ca 3 (22h-6h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 192, "Thưởng": 1000000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 20},
            {"Mã NV": "NV13", "Tên NV": "Mai Thị M", "Bộ phận": "Kế toán", "Ca làm": "Ca 1 (6h-14h)", "Tháng/Năm": "04/2026", "Lương cơ sở": 2340000, "Số giờ làm": 164, "Thưởng": 900000, "Phạt": 0, "Ghi chú phạt": "", "Giờ làm thêm": 4}
        ]
        
        to_add = [r for r in records if r["Mã NV"] not in existing_ma_nv]
        
        if to_add:
            model.add_many_employees_db(to_add)
            load_data()
            messagebox.showinfo("Thành công", f"Đã thêm thành công {len(to_add)} nhân viên mẫu vào bảng lương!", parent=root_ref)
        else:
            messagebox.showinfo("Thông báo", "Tất cả 10 nhân viên mẫu đã tồn tại trong bảng lương!", parent=root_ref)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể thêm nhân viên mẫu:\n{e}", parent=root_ref)

def main(root):
    global root_ref
    root_ref = root
    
    model.create_table()
    model.khoi_tao_du_lieu_mau()
    
    callbacks = {
        'xoa_trang_form': view.xoa_trang_form,
        'on_add_click': on_add_click,
        'on_update_click': on_update_click,
        'on_delete_click': on_delete_click,
        'on_tree_select': on_tree_select,
        'mo_cua_so_import': mo_cua_so_import,
        'export_csv_action': export_csv_action,
        'mo_cua_so_tim_kiem': mo_cua_so_tim_kiem,
        'load_data': load_data,
        'mo_cua_so_gioi_thieu': mo_cua_so_gioi_thieu,
        'them_10_nv_mau': them_10_nv_mau
    }
    
    view.create_menu(root, callbacks)
    view.create_widgets(root, callbacks)
    
    load_data()
