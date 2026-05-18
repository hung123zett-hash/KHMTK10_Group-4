import sqlite3
import pandas as pd
import os

class EmployeeModel:
    def __init__(self, db_name="nhanvien.db"):
        self.db_name = db_name
        self.create_table()
        self.khoi_tao_du_lieu_mau()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS nhan_vien (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ma_nv TEXT NOT NULL,
                    ten_nv TEXT NOT NULL,
                    bo_phan TEXT,
                    ca_lam TEXT,
                    thang_nam TEXT NOT NULL,
                    trinh_do TEXT,
                    tham_nien REAL,
                    luong_co_so REAL,
                    so_gio_lam REAL,
                    thuong REAL,
                    phat REAL,
                    ghi_chu_phat TEXT,
                    gio_lam_them REAL
                )
            """)
            conn.commit()

    def khoi_tao_du_lieu_mau(self):
        # Kiểm tra xem có dữ liệu chưa
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM nhan_vien")
            count = cursor.fetchone()[0]
            
            if count == 0:
                danh_sach_nhan_vien_mau = [
                    ("NV01", "Nguyễn Văn A", "IT", "Sáng", "03/2026", "Cao đẳng", 1.5, 2340000, 176, 500000, 0, "", 5),
                    ("NV01", "Nguyễn Văn A", "IT", "Sáng", "04/2026", "Cao đẳng", 1.6, 2340000, 176, 1000000, 0, "", 10),
                    ("NV02", "Trần Thị B", "Kế toán", "Chiều", "04/2026", "Đại học", 3.0, 2340000, 160, 500000, 100000, "Đi muộn", 5),
                    ("NV03", "Lê Văn C", "Nhân sự", "Sáng", "04/2026", "Trung cấp", 5.0, 2340000, 180, 200000, 0, "", 0),
                ]
                cursor.executemany("""
                    INSERT INTO nhan_vien (
                        ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, trinh_do, 
                        tham_nien, luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, danh_sach_nhan_vien_mau)
                conn.commit()

    def get_all_employees(self):
        with self._get_connection() as conn:
            # Sắp xếp để tính tăng trưởng chính xác
            df = pd.read_sql_query("SELECT * FROM nhan_vien ORDER BY ma_nv, thang_nam", conn)
        return self._process_dataframe(df)

    def search_employees(self, keyword):
        keyword = f"%{keyword.lower()}%"
        with self._get_connection() as conn:
            df = pd.read_sql_query(
                "SELECT * FROM nhan_vien WHERE LOWER(ma_nv) LIKE ? OR LOWER(ten_nv) LIKE ? ORDER BY ma_nv, thang_nam", 
                conn, params=(keyword, keyword)
            )
        return self._process_dataframe(df)

    def add_employee(self, data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO nhan_vien (
                    ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, trinh_do, 
                    tham_nien, luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['Mã NV'], data['Tên NV'], data['Bộ phận'], data['Ca làm'], 
                data['Tháng/Năm'], data['Trình độ'], data['Thâm niên'], 
                data['Lương cơ sở'], data['Số giờ làm'], data['Thưởng'], 
                data['Phạt'], data['Ghi chú phạt'], data['Giờ làm thêm']
            ))
            conn.commit()

    def update_employee(self, emp_id, data):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE nhan_vien SET 
                    ma_nv=?, ten_nv=?, bo_phan=?, ca_lam=?, thang_nam=?, trinh_do=?, 
                    tham_nien=?, luong_co_so=?, so_gio_lam=?, thuong=?, phat=?, 
                    ghi_chu_phat=?, gio_lam_them=?
                WHERE id=?
            """, (
                data['Mã NV'], data['Tên NV'], data['Bộ phận'], data['Ca làm'], 
                data['Tháng/Năm'], data['Trình độ'], data['Thâm niên'], 
                data['Lương cơ sở'], data['Số giờ làm'], data['Thưởng'], 
                data['Phạt'], data['Ghi chú phạt'], data['Giờ làm thêm'], emp_id
            ))
            conn.commit()

    def delete_employee(self, emp_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM nhan_vien WHERE id=?", (emp_id,))
            conn.commit()

    def add_many_employees(self, records):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for data in records:
                cursor.execute("""
                    INSERT INTO nhan_vien (
                        ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, trinh_do, 
                        tham_nien, luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    data.get('Mã NV', ''), data.get('Tên NV', ''), data.get('Bộ phận', ''), data.get('Ca làm', ''), 
                    data.get('Tháng/Năm', ''), data.get('Trình độ', ''), data.get('Thâm niên', 0), 
                    data.get('Lương cơ sở', 0), data.get('Số giờ làm', 0), data.get('Thưởng', 0), 
                    data.get('Phạt', 0), data.get('Ghi chú phạt', ''), data.get('Giờ làm thêm', 0)
                ))
            conn.commit()

    # --- Các hàm nghiệp vụ ---
    
    def _xac_dinh_bac_va_hsl(self, trinh_do, tham_nien):
        if tham_nien < 2:
            bac = 1
        elif 2 <= tham_nien < 4:
            bac = 2
        else:
            bac = 4
            
        hsl = 1.0
        if trinh_do in ["Đại học", "Cử nhân", "Kỹ sư"]:
            if bac == 1: hsl = 2.34
            elif bac == 2: hsl = 2.67
            elif bac == 4: hsl = 3.33
            else: hsl = 3.00
        elif trinh_do == "Cao đẳng":
            if bac == 1: hsl = 2.10
            elif bac == 2: hsl = 2.41
            elif bac == 4: hsl = 3.03
        elif trinh_do == "Trung cấp":
            if bac == 1: hsl = 1.86
            elif bac == 2: hsl = 2.06
            elif bac == 4: hsl = 2.46
        else:
            if bac == 1: hsl = 1.50
            elif bac == 2: hsl = 1.65
            elif bac == 4: hsl = 1.95
            
        return bac, round(hsl, 2)

    def _tinh_thue_tncn(self, thu_nhap):
        # Mức giảm trừ gia cảnh cơ bản (11 triệu VND)
        giam_tru = 11000000
        thu_nhap_tinh_thue = thu_nhap - giam_tru
        
        if thu_nhap_tinh_thue <= 0:
            return 0
            
        # Tính thuế lũy tiến từng phần
        thue = 0
        if thu_nhap_tinh_thue <= 5000000:
            thue = thu_nhap_tinh_thue * 0.05
        elif thu_nhap_tinh_thue <= 10000000:
            thue = (thu_nhap_tinh_thue * 0.1) - 250000
        elif thu_nhap_tinh_thue <= 18000000:
            thue = (thu_nhap_tinh_thue * 0.15) - 750000
        elif thu_nhap_tinh_thue <= 32000000:
            thue = (thu_nhap_tinh_thue * 0.20) - 1650000
        elif thu_nhap_tinh_thue <= 52000000:
            thue = (thu_nhap_tinh_thue * 0.25) - 3250000
        elif thu_nhap_tinh_thue <= 80000000:
            thue = (thu_nhap_tinh_thue * 0.30) - 5850000
        else:
            thue = (thu_nhap_tinh_thue * 0.35) - 9850000
            
        return max(0, thue)

    def _process_dataframe(self, df):
        if df.empty:
            return df

        # Đổi tên cột từ database sang tên hiển thị
        df.rename(columns={
            'ma_nv': 'Mã NV', 'ten_nv': 'Tên NV', 'bo_phan': 'Bộ phận',
            'ca_lam': 'Ca làm', 'thang_nam': 'Tháng/Năm', 'trinh_do': 'Trình độ',
            'tham_nien': 'Thâm niên', 'luong_co_so': 'Lương cơ sở', 'so_gio_lam': 'Số giờ làm',
            'thuong': 'Thưởng', 'phat': 'Phạt', 'ghi_chu_phat': 'Ghi chú phạt', 'gio_lam_them': 'Giờ làm thêm'
        }, inplace=True)

        # Tính Bậc và HSL
        bac_hsl_list = df.apply(lambda row: self._xac_dinh_bac_va_hsl(row['Trình độ'], row['Thâm niên']), axis=1)
        df['Bậc'] = [x[0] for x in bac_hsl_list]
        df['HSL'] = [x[1] for x in bac_hsl_list]
        
        # Tính Lương
        df['Lương cơ bản'] = df['Lương cơ sở'] * df['HSL']
        df['Thu nhập trước thuế'] = df['Lương cơ bản'] + df['Thưởng'] - df['Phạt']
        
        # Tính Thuế TNCN
        df['Thuế TNCN'] = df['Thu nhập trước thuế'].apply(self._tinh_thue_tncn)
        
        # Tính Lương thực nhận (Sau thuế)
        df['Lương thực nhận'] = df['Thu nhập trước thuế'] - df['Thuế TNCN']
        
        # Tính Tỷ lệ tăng trưởng bằng Pandas
        try:
            # Thêm cột tạm thời để sắp xếp datetime (nếu cần thiết)
            df['Thời gian_tmp'] = pd.to_datetime(df['Tháng/Năm'], format='%m/%Y')
            df_sorted = df.sort_values(by=['Mã NV', 'Thời gian_tmp'])
            df['Tăng trưởng (%)'] = df_sorted.groupby('Mã NV')['Lương thực nhận'].pct_change() * 100
            df['Tăng trưởng (%)'] = df['Tăng trưởng (%)'].fillna(0).round(2)
            df.drop('Thời gian_tmp', axis=1, inplace=True)
        except Exception:
            df['Tăng trưởng (%)'] = 0.0

        return df

    def get_statistics(self, df):
        if df is None or df.empty:
            return {
                'tong_luong': 0,
                'luong_tb': 0,
                'tong_gio_lam_them': 0,
                'ty_le_tang_truong_tb': 0
            }
            
        tong_luong = df['Lương thực nhận'].sum()
        luong_tb = df['Lương thực nhận'].mean()
        tong_gio = df['Giờ làm thêm'].sum()
        
        ty_le_hop_le = df[df['Tăng trưởng (%)'] != 0]['Tăng trưởng (%)']
        ty_le_tb = ty_le_hop_le.mean() if not ty_le_hop_le.empty else 0
        
        return {
            'tong_luong': tong_luong,
            'luong_tb': luong_tb,
            'tong_gio_lam_them': tong_gio,
            'ty_le_tang_truong_tb': ty_le_tb
        }
