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
tree.column("holot", width=150)
tree.column("ten", width=100)
tree.column("phai", width=60)
tree.column("ngaysinh", width=100)
tree.column("chucvu", width=140)

tree.pack(padx=10, pady=5, fill="both")


# ====================== HÀM XỬ LÝ ======================
def clear_input():
    entry_maso.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    date_entry.set_date("2000-01-01")
    cbb_chucvu.set("")


def load_data():
    conn = connect_db()
    if conn is None: return

    cur = conn.cursor()
    tree.delete(*tree.get_children())

    cur.execute("SELECT * FROM nhanvien")
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


def them_nv():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    chucvu = cbb_chucvu.get()

    if maso == "" or holot == "" or ten == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO nhanvien VALUES (?, ?, ?, ?, ?, ?)
        """, (maso, holot, ten, phai, ngaysinh, chucvu))

        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm nhân viên")

        load_data()
        clear_input()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

    conn.close()


def xoa_nv():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa")
        return

    maso = tree.item(selected)["values"][0]

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM nhanvien WHERE maso = ?", (maso,))
    conn.commit()
    conn.close()
    load_data()


def sua_nv():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên cần sửa")
        return

    values = tree.item(selected)["values"]

    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, values[0])

    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, values[1])

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[2])

    gender_var.set(values[3])
    date_entry.set_date(values[4])
    cbb_chucvu.set(values[5])


def luu_nv():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_entry.get()
    chucvu = cbb_chucvu.get()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE nhanvien 
        SET holot=?, ten=?, phai=?, ngaysinh=?, chucvu=?
        WHERE maso=?
    """, (holot, ten, phai, ngaysinh, chucvu, maso))

    conn.commit()
    conn.close()
    load_data()
    clear_input()


# ====================== NÚT CHỨC NĂNG ======================
frame_btn = tk.Frame(root)
frame_btn.pack(pady=8)

tk.Button(frame_btn, text="Thêm", width=10, command=them_nv).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Sửa", width=10, command=sua_nv).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Lưu", width=10, command=luu_nv).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Xóa", width=10, command=xoa_nv).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Tải lại", width=10, command=load_data).grid(row=0, column=4, padx=5)


# ====================== CHẠY APP ======================
load_data()
root.mainloop()
