import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc

# ====================== KẾT NỐI SQL SERVER ======================
def connect_db():
    try:
        conn = pyodbc.connect(
            r"DRIVER={SQL Server};"
            r"SERVER=THOTHAOTC147\MSSQLSERVER;"
            r"DATABASE=QLLaiXe;"
            r"Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối", str(e))
        return None


# ====================== CANH GIỮA CỬA SỔ ======================
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')


# ====================== CỬA SỔ CHÍNH ======================
root = tk.Tk()
root.title("Quản lý lái xe")
center_window(root)
root.resizable(False, False)

tk.Label(root, text="QUẢN LÝ LÁI XE", font=("Arial", 18, "bold")).pack(pady=10)


# ====================== FORM NHẬP DỮ LIỆU ======================
frame_info = tk.Frame(root)
frame_info.pack(pady=5, padx=10, fill="x")

tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5)
entry_maso = tk.Entry(frame_info, width=15)
entry_maso.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_info, text="Chức vụ").grid(row=0, column=2, padx=5, pady=5)
cbb_chucvu = ttk.Combobox(frame_info, width=20,
                          values=["Trưởng phòng", "Phó phòng", "Nhân viên", "Kế toán", "Lái xe"])
cbb_chucvu.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5)
entry_holot = tk.Entry(frame_info, width=25)
entry_holot.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5)
entry_ten = tk.Entry(frame_info, width=15)
entry_ten.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5)
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, sticky="w")
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=2, sticky="w")

tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5)
date_entry = DateEntry(frame_info, width=12, background="darkblue",
                       foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=2, column=3, padx=5, pady=5)


# ====================== BẢNG DANH SÁCH ======================
tk.Label(root, text="Danh sách nhân viên", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)

columns = ("maso", "holot", "ten", "phai", "ngaysinh", "chucvu")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col.capitalize())

tree.column("maso", width=80)

