import sqlite3
import pandas as pd

DB_NAME = "nhanvien.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    with get_connection() as conn:
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

def khoi_tao_du_lieu_mau():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM nhan_vien")
        count = cursor.fetchone()[0]
        
        if count == 0:
            danh_sach = [
                ("NV01", "Nguyễn Văn A", "IT", "Sáng", "03/2026", "Cao đẳng", 1.5, 2340000, 176, 500000, 0, "", 5),
                ("NV02", "Trần Thị B", "Kế toán", "Chiều", "04/2026", "Đại học", 3.0, 2340000, 160, 500000, 100000, "Đi muộn", 5),
                ("NV03", "Lê Văn C", "Nhân sự", "Sáng", "04/2026", "Trung cấp", 5.0, 2340000, 180, 200000, 0, "", 0),
            ]
            cursor.executemany("""
                INSERT INTO nhan_vien (
                    ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, trinh_do, 
                    tham_nien, luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, danh_sach)
            conn.commit()

def _xac_dinh_bac_va_hsl(trinh_do, tham_nien):
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

def _process_dataframe(df):
    if df.empty:
        return df

    df.rename(columns={
        'ma_nv': 'Mã NV', 'ten_nv': 'Tên NV', 'bo_phan': 'Bộ phận',
        'ca_lam': 'Ca làm', 'thang_nam': 'Tháng/Năm',
        'luong_co_so': 'Lương cơ sở', 'so_gio_lam': 'Số giờ làm',
        'thuong': 'Thưởng', 'phat': 'Phạt', 'ghi_chu_phat': 'Ghi chú phạt', 'gio_lam_them': 'Giờ làm thêm'
    }, inplace=True)

    df['Tiền làm thêm'] = df['Giờ làm thêm'] * 50000
    df['Lương thực nhận'] = df['Lương cơ sở'] + df['Thưởng'] - df['Phạt']
    
    return df

def is_duplicate_ma_nv(ma_nv, emp_id=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        if emp_id:
            cursor.execute("SELECT id FROM nhan_vien WHERE ma_nv=? AND id!=?", (ma_nv, emp_id))
        else:
            cursor.execute("SELECT id FROM nhan_vien WHERE ma_nv=?", (ma_nv,))
        return cursor.fetchone() is not None

def get_all_employees():
    with get_connection() as conn:
        df = pd.read_sql_query("SELECT * FROM nhan_vien ORDER BY ma_nv, thang_nam", conn)
    return _process_dataframe(df)

def search_employees_db(keyword):
    keyword = f"%{keyword.lower()}%"
    with get_connection() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM nhan_vien WHERE LOWER(ma_nv) LIKE ? OR LOWER(ten_nv) LIKE ? ORDER BY ma_nv, thang_nam", 
            conn, params=(keyword, keyword)
        )
    return _process_dataframe(df)

def add_employee_db(data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO nhan_vien (
                ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, 
                luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['Mã NV'], data['Tên NV'], data['Bộ phận'], data['Ca làm'], 
            data['Tháng/Năm'], 
            data['Lương cơ sở'], data['Số giờ làm'], data['Thưởng'], 
            data['Phạt'], data['Ghi chú phạt'], data['Giờ làm thêm']
        ))
        conn.commit()

def update_employee_db(emp_id, data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE nhan_vien SET 
                ma_nv=?, ten_nv=?, bo_phan=?, ca_lam=?, thang_nam=?, 
                luong_co_so=?, so_gio_lam=?, thuong=?, phat=?, 
                ghi_chu_phat=?, gio_lam_them=?
            WHERE id=?
        """, (
            data['Mã NV'], data['Tên NV'], data['Bộ phận'], data['Ca làm'], 
            data['Tháng/Năm'], 
            data['Lương cơ sở'], data['Số giờ làm'], data['Thưởng'], 
            data['Phạt'], data['Ghi chú phạt'], data['Giờ làm thêm'], emp_id
        ))
        conn.commit()

def delete_employee_db(emp_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM nhan_vien WHERE id=?", (emp_id,))
        conn.commit()

def add_many_employees_db(records):
    with get_connection() as conn:
        cursor = conn.cursor()
        for data in records:
            cursor.execute("""
                INSERT INTO nhan_vien (
                    ma_nv, ten_nv, bo_phan, ca_lam, thang_nam, 
                    luong_co_so, so_gio_lam, thuong, phat, ghi_chu_phat, gio_lam_them
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('Mã NV', ''), data.get('Tên NV', ''), data.get('Bộ phận', ''), data.get('Ca làm', ''), 
                data.get('Tháng/Năm', ''), 
                data.get('Lương cơ sở', 0), data.get('Số giờ làm', 0), data.get('Thưởng', 0), 
                data.get('Phạt', 0), data.get('Ghi chú phạt', ''), data.get('Giờ làm thêm', 0)
            ))
        conn.commit()

def get_statistics(df):
    if df is None or df.empty:
        return {
            'tong_luong': 0,
            'luong_tb': 0,
            'tong_gio_lam_them': 0
        }
        
    tong_luong = df['Lương thực nhận'].sum()
    luong_tb = df['Lương thực nhận'].mean()
    tong_gio = df['Giờ làm thêm'].sum()
    
    return {
        'tong_luong': tong_luong,
        'luong_tb': luong_tb,
        'tong_gio_lam_them': tong_gio
    }
