import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import pyodbc

# ========================= KẾT NỐI SQL SERVER =========================
def connect_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=THOTHAOTC147\\MSSQLSERVER2022;"
            "DATABASE=QLXe;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi SQL Server", str(e))
        return None

# ========================= CĂN GIỮA CỬA SỔ =========================
def center(win, w=900, h=650):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

# ========================= MAIN WINDOW =========================
root = tk.Tk()
root.title("Phần mềm quản lý Xe & Lái Xe – SQL Server")
center(root)
root.resizable(False, False)

title = tk.Label(root, text="QUẢN LÝ XE & LÁI XE", font=("Arial", 22, "bold"))
title.pack(pady=15)

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# =====================================================================
# =========================== TAB QUẢN LÝ XE ===========================
# =====================================================================

tab_xe = tk.Frame(notebook)
notebook.add(tab_xe, text="Quản lý Xe")

frame_xe = tk.Frame(tab_xe)
frame_xe.pack(pady=10)

tk.Label(frame_xe, text="Số Xe").grid(row=0, column=0)
e_soxe = tk.Entry(frame_xe, width=20)
e_soxe.grid(row=0, column=1)

tk.Label(frame_xe, text="Loại Xe").grid(row=1, column=0)
e_loaixe = tk.Entry(frame_xe, width=20)
e_loaixe.grid(row=1, column=1)

tk.Label(frame_xe, text="Năm Sản Xuất").grid(row=2, column=0)
e_namsx = tk.Entry(frame_xe, width=20)
e_namsx.grid(row=2, column=1)

tk.Label(frame_xe, text="Màu Sơn").grid(row=0, column=2)
e_mauson = tk.Entry(frame_xe, width=20)
e_mauson.grid(row=0, column=3)

tk.Label(frame_xe, text="Biển Số").grid(row=1, column=2)
e_bienso = tk.Entry(frame_xe, width=20)
e_bienso.grid(row=1, column=3)

tk.Label(frame_xe, text="Tình Trạng").grid(row=2, column=2)
e_tinhtrang = tk.Entry(frame_xe, width=20)
e_tinhtrang.grid(row=2, column=3)

columns_xe = ("Số Xe", "Loại Xe", "Năm SX", "Màu Sơn", "Biển Số", "Tình Trạng")
tree_xe = ttk.Treeview(tab_xe, columns=columns_xe, show="headings", height=10)

for col in columns_xe:
    tree_xe.heading(col, text=col)
    tree_xe.column(col, width=130)

tree_xe.pack(pady=10)

def clear_xe():
    e_soxe.delete(0, tk.END)
    e_loaixe.delete(0, tk.END)
    e_namsx.delete(0, tk.END)
    e_mauson.delete(0, tk.END)
    e_bienso.delete(0, tk.END)
    e_tinhtrang.delete(0, tk.END)

def load_xe():
    conn = connect_db()
    cur = conn.cursor()
    tree_xe.delete(*tree_xe.get_children())

    cur.execute("SELECT soxe, loaixe, namsx, mauson, bienso, tinhtrang FROM Xe")
    for row in cur.fetchall():
        clean_values = []
        for v in row:
            if isinstance(v, str):
                v = v.replace("'", "").replace(",", "").strip()
            clean_values.append(str(v))
        
        tree_xe.insert("", tk.END, values=tuple(clean_values))

    conn.close()

def add_xe():
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO Xe VALUES (?, ?, ?, ?, ?, ?)
        """, (
            e_soxe.get(), e_loaixe.get(), e_namsx.get(),
            e_mauson.get(), e_bienso.get(), e_tinhtrang.get()
        ))
        conn.commit()
        messagebox.showinfo("OK", "Thêm xe thành công!")
        load_xe()
        clear_xe()
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def delete_xe():
    sel = tree_xe.selection()
    if not sel:
        messagebox.showwarning("Chọn", "Hãy chọn xe để xóa")
        return

    soxe = tree_xe.item(sel)["values"][0]
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Xe WHERE soxe=?", (soxe,))
    conn.commit()
    conn.close()
    load_xe()

def edit_xe():
    sel = tree_xe.selection()
    if not sel:
        messagebox.showwarning("Chọn", "Hãy chọn xe để sửa")
        return

    val = tree_xe.item(sel)["values"]

    e_soxe.delete(0, tk.END)
    e_loaixe.delete(0, tk.END)
    e_namsx.delete(0, tk.END)
    e_mauson.delete(0, tk.END)
    e_bienso.delete(0, tk.END)
    e_tinhtrang.delete(0, tk.END)

    e_soxe.insert(0, val[0])
    e_loaixe.insert(0, val[1])
    e_namsx.insert(0, val[2])
    e_mauson.insert(0, val[3])
    e_bienso.insert(0, val[4])
    e_tinhtrang.insert(0, val[5])

def save_xe():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Xe 
        SET loaixe=?, namsx=?, mauson=?, bienso=?, tinhtrang=?
        WHERE soxe=?
    """, (
        e_loaixe.get(), e_namsx.get(), e_mauson.get(),
        e_bienso.get(), e_tinhtrang.get(), e_soxe.get()
    ))
    conn.commit()
    conn.close()
    load_xe()
    clear_xe()

frame_btn_xe = tk.Frame(tab_xe)
frame_btn_xe.pack()

tk.Button(frame_btn_xe, text="Thêm", width=12, command=add_xe).grid(row=0, column=0)
tk.Button(frame_btn_xe, text="Sửa", width=12, command=edit_xe).grid(row=0, column=1)
tk.Button(frame_btn_xe, text="Lưu", width=12, command=save_xe).grid(row=0, column=2)
tk.Button(frame_btn_xe, text="Xóa", width=12, command=delete_xe).grid(row=0, column=3)
tk.Button(frame_btn_xe, text="Tải lại", width=12, command=load_xe).grid(row=0, column=4)

load_xe()

# =====================================================================
# ======================== TAB QUẢN LÝ LÁI XE ==========================
# =====================================================================

tab_lx = tk.Frame(notebook)
notebook.add(tab_lx, text="Quản lý Lái Xe")

frame_lx = tk.Frame(tab_lx)
frame_lx.pack(pady=10)

tk.Label(frame_lx, text="Mã Lái Xe").grid(row=0, column=0)
e_ma = tk.Entry(frame_lx, width=20)
e_ma.grid(row=0, column=1)

tk.Label(frame_lx, text="Họ tên").grid(row=1, column=0)
e_ten = tk.Entry(frame_lx, width=20)
e_ten.grid(row=1, column=1)
tk.Label(frame_lx, text="Phái").grid(row=2, column=0)
e_phai = tk.Entry(frame_lx, width=20)
e_phai.grid(row=2, column=1)

tk.Label(frame_lx, text="Ngày sinh").grid(row=0, column=2)
date_ns2 = DateEntry(frame_lx, width=18, date_pattern="yyyy-mm-dd")
date_ns2.grid(row=0, column=3)

tk.Label(frame_lx, text="Hạng bằng").grid(row=1, column=2)
e_bang = tk.Entry(frame_lx, width=20)
e_bang.grid(row=1, column=3)

columns_lx = ("Mã", "Họ tên", "Phái", "Ngày sinh", "Hạng bằng")
tree_lx = ttk.Treeview(tab_lx, columns=columns_lx, show="headings", height=10)

for col in columns_lx:
    tree_lx.heading(col, text=col)
    tree_lx.column(col, width=150)

tree_lx.pack(pady=10)

def clear_lx():
    e_ma.delete(0, tk.END)
    e_ten.delete(0, tk.END)
    e_phai.delete(0, tk.END)
    date_ns2.set_date("2000-01-01")
    e_bang.delete(0, tk.END)

def load_lx():
    conn = connect_db()
    cur = conn.cursor()
    tree_lx.delete(*tree_lx.get_children())

    cur.execute("SELECT maso, hoten, phai, ngaysinh, hangbang FROM Laixe")
    for row in cur.fetchall():
        values = tuple(row)
        tree_lx.insert("", tk.END, values=values)

    conn.close()

def add_lx():
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Laixe VALUES (?, ?, ?, ?, ?)
        """, (
            e_ma.get(), e_ten.get(), e_phai.get(),
            date_ns2.get(), e_bang.get()
        ))
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
    cur.execute("DELETE FROM Laixe WHERE maso=?", (ma,))
    conn.commit()
    conn.close()
    load_lx()

def edit_lx():
    sel = tree_lx.selection()
    if not sel:
        messagebox.showwarning("Chọn", "Hãy chọn lái xe để sửa")
        return

    val = tree_lx.item(sel)["values"]

    e_ma.delete(0, tk.END)
    e_ten.delete(0, tk.END)
    e_phai.delete(0, tk.END)
    e_bang.delete(0, tk.END)

    e_ma.insert(0, val[0])
    e_ten.insert(0, val[1])
    e_phai.insert(0, val[2])
    date_ns2.set_date(val[3])
    e_bang.insert(0, val[4])

def save_lx():
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE Laixe SET hoten=?, phai=?, ngaysinh=?, hangbang=?
        WHERE maso=?
    """, (
        e_ten.get(), e_phai.get(), date_ns2.get(),
        e_bang.get(), e_ma.get()
    ))

    conn.commit()
    conn.close()
    load_lx()
    clear_lx()

frame_btn_lx = tk.Frame(tab_lx)
frame_btn_lx.pack()

tk.Button(frame_btn_lx, text="Thêm", width=12, command=add_lx).grid(row=0, column=0)
tk.Button(frame_btn_lx, text="Sửa", width=12, command=edit_lx).grid(row=0, column=1)
tk.Button(frame_btn_lx, text="Lưu", width=12, command=save_lx).grid(row=0, column=2)
tk.Button(frame_btn_lx, text="Xóa", width=12, command=delete_lx).grid(row=0, column=3)
tk.Button(frame_btn_lx, text="Tải lại", width=12, command=load_lx).grid(row=0, column=4)

load_lx()

root.mainloop()