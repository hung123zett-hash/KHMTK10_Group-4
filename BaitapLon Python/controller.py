import pandas as pd

from tkinter import filedialog
from model import EmployeeModel
from view import EmployeeView

class EmployeeController:
    def __init__(self, root):
        self.model = EmployeeModel()
        # Khởi tạo View và truyền chính Controller vào
        self.view = EmployeeView(root, self)
        
        # Biến lưu trữ dataframe hiện tại để export
        self.current_df = None
        
        # Load dữ liệu lên View
        self.load_data()

    def load_data(self):
        try:
            df = self.model.get_all_employees()
            self.current_df = df
            self.view.update_treeview(df)
            
            stats = self.model.get_statistics(df)
            self.view.update_statistics(stats)
        except Exception as e:
            self.view.show_error("Lỗi Tải Dữ Liệu", f"Không thể tải dữ liệu từ CSDL:\n{e}")

    def add_employee(self, data):
        try:
            self.model.add_employee(data)
            self.view.xoa_trang_form()
            self.load_data()
            self.view.show_info("Thành công", f"Đã thêm mới nhân viên {data['Tên NV']} thành công!")
        except Exception as e:
            self.view.show_error("Lỗi Thêm Mới", f"Không thể thêm dữ liệu:\n{e}")

    def update_employee(self, emp_id, data):
        try:
            self.model.update_employee(emp_id, data)
            self.view.xoa_trang_form()
            self.load_data()
            self.view.show_info("Thành công", "Đã cập nhật dữ liệu thành công!")
        except Exception as e:
            self.view.show_error("Lỗi Cập Nhật", f"Không thể cập nhật dữ liệu:\n{e}")

    def delete_employee(self, emp_id):
        try:
            self.model.delete_employee(emp_id)
            self.view.xoa_trang_form()
            self.load_data()
            self.view.show_info("Thành công", "Đã xóa dữ liệu thành công!")
        except Exception as e:
            self.view.show_error("Lỗi Xóa", f"Không thể xóa dữ liệu:\n{e}")

    def search_employees(self, keyword, window):
        if not keyword:
            self.load_data()
            window.destroy()
            return
            
        try:
            df = self.model.search_employees(keyword)
            if df.empty:
                self.view.show_info("Kết quả", "Không tìm thấy nhân viên nào phù hợp!")
            else:
                self.current_df = df
                self.view.update_treeview(df)
                self.view.show_info("Kết quả", f"Tìm thấy {len(df)} kết quả.")
                window.destroy()
        except Exception as e:
            self.view.show_error("Lỗi Tìm Kiếm", f"Có lỗi xảy ra:\n{e}")

    def import_csv(self, path, window):
        try:
            df = pd.read_csv(path)
            du_lieu_csv = df.to_dict('records')
            
            # Đảm bảo các cột có tồn tại và xử lý NaN
            for item in du_lieu_csv:
                for k in item:
                    if pd.isna(item[k]):
                        item[k] = "" if isinstance(item[k], str) else 0
                        
            self.model.add_many_employees(du_lieu_csv)
            self.load_data()
            self.view.show_info("Thành công", f"Đã import thành công {len(du_lieu_csv)} dòng dữ liệu!")
            window.destroy()
        except Exception as e:
            self.view.show_error("Lỗi Import", f"Có lỗi xảy ra khi đọc file CSV:\n{e}")

    def export_csv(self):
        if self.current_df is None or self.current_df.empty:
            self.view.show_error("Lỗi Export", "Không có dữ liệu để xuất!")
            return
            
        try:
            path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
                title="Lưu file xuất CSV"
            )
            
            if not path:
                return
                
            # Không xuất cột ID ẩn ra ngoài nếu không cần, nhưng cứ export hết df
            export_df = self.current_df.drop(columns=['id'], errors='ignore')
            export_df.to_csv(path, index=False, encoding='utf-8-sig')
            
            self.view.show_info("Thành công", f"Đã xuất file dữ liệu tới:\n{path}")
        except Exception as e:
            self.view.show_error("Lỗi Export", f"Có lỗi khi lưu file:\n{e}")
