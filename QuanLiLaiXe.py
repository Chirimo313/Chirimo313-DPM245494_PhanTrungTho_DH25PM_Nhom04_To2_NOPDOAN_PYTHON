import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc

# ========================= KẾT NỐI SQL SERVER =========================
def connect_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=THOTHAOTC147\MSSQLSERVER2022;"
            "DATABASE=QLXe;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi SQL Server", str(e))
        return None

# ========================= CĂN GIỮA CỬA SỔ =========================
def center(win, w=800, h=600):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws//2) - (w//2)
    y = (hs//2) - (h//2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ========================= GIAO DIỆN CHÍNH =========================
root = tk.Tk()
root.title("Quản lý Xe & Lái xe - SQL Server")
center(root)
root.resizable(False, False)

title = tk.Label(root, text="QUẢN LÝ XE & LÁI XE", font=("Arial", 20, "bold"))
title.pack(pady=10)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# =====================================================================
# =========================== TAB QUẢN LÝ XE ===========================
# =====================================================================

tab_xe = tk.Frame(notebook)
notebook.add(tab_xe, text="Quản lý Xe")

# ------- Form nhập -------
frame_xe = tk.Frame(tab_xe)
frame_xe.pack(pady=10)

tk.Label(frame_xe, text="Mã Xe").grid(row=0, column=0)
e_ma_xe = tk.Entry(frame_xe, width=20)
e_ma_xe.grid(row=0, column=1)

tk.Label(frame_xe, text="Tên Xe").grid(row=1, column=0)
e_ten_xe = tk.Entry(frame_xe, width=20)
e_ten_xe.grid(row=1, column=1)

tk.Label(frame_xe, text="Loại Xe").grid(row=2, column=0)
e_loai_xe = tk.Entry(frame_xe, width=20)
e_loai_xe.grid(row=2, column=1)

tk.Label(frame_xe, text="Biển số").grid(row=0, column=2)
e_bienso = tk.Entry(frame_xe, width=20)
e_bienso.grid(row=0, column=3)

tk.Label(frame_xe, text="Ngày Đăng Kiểm").grid(row=1, column=2)
date_dk = DateEntry(frame_xe, width=18, date_pattern="yyyy-mm-dd")
date_dk.grid(row=1, column=3)

# ------- Bảng dữ liệu -------
columns_xe = ("MaXe", "TenXe", "LoaiXe", "BienSo", "NgayDangKiem")
tree_xe = ttk.Treeview(tab_xe, columns=columns_xe, show="headings", height=12)

for col in columns_xe:
    tree_xe.heading(col, text=col)
    tree_xe.column(col, width=140)

tree_xe.pack(pady=10)

# ===================== HÀM XỬ LÝ XE =====================
def clear_xe():
    e_ma_xe.delete(0, tk.END)
    e_ten_xe.delete(0, tk.END)
    e_loai_xe.delete(0, tk.END)
    e_bienso.delete(0, tk.END)
    date_dk.set_date("2000-01-01")

def load_xe():
    conn = connect_db()
    cur = conn.cursor()
    tree_xe.delete(*tree_xe.get_children())

    cur.execute("SELECT * FROM Xe")
    for row in cur.fetchall():
        tree_xe.insert("", tk.END, values=row)

    conn.close()

def add_xe(): 
    ma = e_ma_xe.get()
    ten = e_ten_xe.get()
    loai = e_loai_xe.get()
    bs = e_bienso.get()
    dk = date_dk.get()

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO Xe VALUES (?, ?, ?, ?, ?)",
            (ma, ten, loai, bs, dk)
        )
        conn.commit()
        messagebox.showinfo("OK", "Thêm Xe thành công!")
        load_xe()
        clear_xe()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def delete_xe():
    sel = tree_xe.selection()
    if not sel:
        messagebox.showwarning("Chọn xe", "Hãy chọn một xe để xóa")
        return
    ma = tree_xe.item(sel)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Xe WHERE MaXe=?", (ma,))
    conn.commit()
    conn.close()
    load_xe()

def edit_xe():
    sel = tree_xe.selection()
    if not sel:
        messagebox.showwarning("Chọn xe", "Hãy chọn xe để sửa")
        return
    val = tree_xe.item(sel)["values"]

    e_ma_xe.delete(0, tk.END)
    e_ma_xe.insert(0, val[0])

    e_ten_xe.delete(0, tk.END)
    e_ten_xe.insert(0, val[1])

    e_loai_xe.delete(0, tk.END)
    e_loai_xe.insert(0, val[2])

    e_bienso.delete(0, tk.END)
    e_bienso.insert(0, val[3])

    date_dk.set_date(val[4])

def save_xe():
    ma = e_ma_xe.get()
    ten = e_ten_xe.get()
    loai = e_loai_xe.get()
    bs = e_bienso.get()
    dk = date_dk.get()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Xe 
        SET TenXe=?, LoaiXe=?, BienSo=?, NgayDangKiem=?
        WHERE MaXe=?
    """, (ten, loai, bs, dk, ma))

    conn.commit()
    conn.close()
    load_xe()
    clear_xe()

# ------- Buttons -------
frame_btn_xe = tk.Frame(tab_xe)
frame_btn_xe.pack()

tk.Button(frame_btn_xe, text="Thêm", width=12, command=add_xe).grid(row=0, column=0, padx=5)
tk.Button(frame_btn_xe, text="Sửa", width=12, command=edit_xe).grid(row=0, column=1, padx=5)
tk.Button(frame_btn_xe, text="Lưu", width=12, command=save_xe).grid(row=0, column=2, padx=5)
tk.Button(frame_btn_xe, text="Xóa", width=12, command=delete_xe).grid(row=0, column=3, padx=5)
tk.Button(frame_btn_xe, text="Tải lại", width=12, command=load_xe).grid(row=0, column=4, padx=5)

load_xe()

# =====================================================================
# ======================== TAB QUẢN LÝ LÁI XE ==========================
# =====================================================================

tab_laixe = tk.Frame(notebook)
notebook.add(tab_laixe, text="Quản lý Lái Xe")

frame_lx = tk.Frame(tab_laixe)
frame_lx.pack(pady=10)

tk.Label(frame_lx, text="Mã Lái Xe").grid(row=0, column=0)
e_ma_lx = tk.Entry(frame_lx, width=20)
e_ma_lx.grid(row=0, column=1)

tk.Label(frame_lx, text="Họ Tên").grid(row=1, column=0)
e_ten_lx = tk.Entry(frame_lx, width=20)
e_ten_lx.grid(row=1, column=1)

tk.Label(frame_lx, text="Ngày Sinh").grid(row=2, column=0)
date_ns = DateEntry(frame_lx, width=18, date_pattern="yyyy-mm-dd")
date_ns.grid(row=2, column=1)

tk.Label(frame_lx, text="Bằng Lái").grid(row=0, column=2)
e_bang = tk.Entry(frame_lx, width=20)
e_bang.grid(row=0, column=3)

tk.Label(frame_lx, text="SĐT").grid(row=1, column=2)
e_sdt = tk.Entry(frame_lx, width=20)
e_sdt.grid(row=1, column=3)

# -------- Bảng -------
columns_lx = ("MaLX", "HoTen", "NgaySinh", "BangLai", "SDT")
tree_lx = ttk.Treeview(tab_laixe, columns=columns_lx, show="headings", height=12)

for col in columns_lx:
    tree_lx.heading(col, text=col)
    tree_lx.column(col, width=150)

tree_lx.pack(pady=10)

# ===================== HÀM LÁI XE =====================
def clear_lx():
    e_ma_lx.delete(0, tk.END)
    e_ten_lx.delete(0, tk.END)
    date_ns.set_date("2000-01-01")
    e_bang.delete(0, tk.END)
    e_sdt.delete(0, tk.END)

def load_lx():
    conn = connect_db()
    cur = conn.cursor()
    tree_lx.delete(*tree_lx.get_children())

    cur.execute("SELECT * FROM Laixe")
    for row in cur.fetchall():
        tree_lx.insert("", tk.END, values=row)

    conn.close()

def add_lx():
    ma = e_ma_lx.get()
    ten = e_ten_lx.get()
    ns = date_ns.get()
    bang = e_bang.get()
    sdt = e_sdt.get()

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO Laixe VALUES (?, ?, ?, ?, ?)",
            (ma, ten, ns, bang, sdt)
        )
        conn.commit()
        messagebox.showinfo("OK", "Thêm lái xe thành công!")
        load_lx()
        clear_lx()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def delete_lx():
    sel = tree_lx.selection()
    if not sel:
        messagebox.showwarning("Chọn", "Hãy chọn lái xe để xóa")
        return
    ma = tree_lx.item(sel)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Laixe WHERE MaLX=?", (ma,))
    conn.commit()
    conn.close()
    load_lx()

def edit_lx():
    sel = tree_lx.selection()
    if not sel:
        messagebox.showwarning("Chọn", "Hãy chọn lái xe để sửa")
        return
    val = tree_lx.item(sel)["values"]

    e_ma_lx.delete(0, tk.END)
    e_ma_lx.insert(0, val[0])

    e_ten_lx.delete(0, tk.END)
    e_ten_lx.insert(0, val[1])

    date_ns.set_date(val[2])

    e_bang.delete(0, tk.END)
    e_bang.insert(0, val[3])

    e_sdt.delete(0, tk.END)
    e_sdt.insert(0, val[4])

def save_lx():
    ma = e_ma_lx.get()
    ten = e_ten_lx.get()
    ns = date_ns.get()
    bang = e_bang.get()
    sdt = e_sdt.get()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Laixe 
        SET HoTen=?, NgaySinh=?, BangLai=?, SDT=?
        WHERE MaLX=?
    """, (ten, ns, bang, sdt, ma))

    conn.commit()
    conn.close()
    load_lx()
    clear_lx()

frame_btn_lx = tk.Frame(tab_laixe)
frame_btn_lx.pack()

tk.Button(frame_btn_lx, text="Thêm", width=12, command=add_lx).grid(row=0, column=0, padx=5)
tk.Button(frame_btn_lx, text="Sửa", width=12, command=edit_lx).grid(row=0, column=1, padx=5)
tk.Button(frame_btn_lx, text="Lưu", width=12, command=save_lx).grid(row=0, column=2, padx=5)
tk.Button(frame_btn_lx, text="Xóa", width=12, command=delete_lx).grid(row=0, column=3, padx=5)
tk.Button(frame_btn_lx, text="Tải lại", width=12, command=load_lx).grid(row=0, column=4, padx=5)

load_lx()

root.mainloop()