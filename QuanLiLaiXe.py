import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ====================== KẾT NỐI MYSQL ======================
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",   # Thay mật khẩu MySQL nếu có
            database="QLXe"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Lỗi kết nối MySQL", str(e))
        return None


# ====================== CANH GIỮA CỬA SỔ ======================
def center(win, w=750, h=520):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws - w) // 2
    y = (hs - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")


# ====================== CỬA SỔ CHÍNH ======================
root = tk.Tk()
root.title("Quản lý LÁI XE")
center(root)
root.resizable(False, False)

tk.Label(root, text="HỆ THỐNG QUẢN LÝ LÁI XE", font=("Arial", 18, "bold")).pack(pady=10)


# ====================== FORM NHẬP THÔNG TIN ======================
frm = tk.Frame(root)
frm.pack(pady=5, padx=10, fill="x")

# Mã lái xe
tk.Label(frm, text="Mã lái xe").grid(row=0, column=0, padx=5, pady=5)
entry_maso = tk.Entry(frm, width=15)
entry_maso.grid(row=0, column=1, padx=5)

# Hạng bằng lái
tk.Label(frm, text="Hạng bằng").grid(row=0, column=2, padx=5, pady=5)
cbb_hang = ttk.Combobox(frm, width=15, values=["A1", "A2", "B1", "B2", "C", "D", "E", "FC"])
cbb_hang.grid(row=0, column=3, padx=5)

# Họ lót
tk.Label(frm, text="Họ lót").grid(row=1, column=0, padx=5, pady=5)
entry_holot = tk.Entry(frm, width=25)
entry_holot.grid(row=1, column=1, padx=5)

# Tên
tk.Label(frm, text="Tên").grid(row=1, column=2, padx=5, pady=5)
entry_ten = tk.Entry(frm, width=15)
entry_ten.grid(row=1, column=3, padx=5)

# Phái
tk.Label(frm, text="Phái").grid(row=2, column=0, padx=5, pady=5)
gender_var = tk.StringVar(value="Nam")
tk.Radiobutton(frm, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, sticky="w")
tk.Radiobutton(frm, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=2, sticky="w")

# Ngày sinh
tk.Label(frm, text="Ngày sinh").grid(row=2, column=2, padx=5)
date_ngaysinh = DateEntry(frm, width=12, date_pattern="yyyy-mm-dd")
date_ngaysinh.grid(row=2, column=3, padx=5)


# ====================== BẢNG LÁI XE ======================
tk.Label(root, text="Danh sách Lái xe", font=("Arial", 11, "bold")).pack(anchor="w", padx=15)

columns = ("maso", "holot", "ten", "phai", "ngaysinh", "hangbang")

tree = ttk.Treeview(root, columns=columns, show="headings", height=12)

for col in columns:
    tree.heading(col, text=col.upper())

tree.column("maso", width=80)
tree.column("holot", width=150)
tree.column("ten", width=80)
tree.column("phai", width=60)
tree.column("ngaysinh", width=90)
tree.column("hangbang", width=80)

tree.pack(padx=10, pady=5)
# ====================== CÁC HÀM XỬ LÝ ======================
def clear_input():
    entry_maso.delete(0, tk.END)
    entry_holot.delete(0, tk.END)
    entry_ten.delete(0, tk.END)
    gender_var.set("Nam")
    date_ngaysinh.set_date("2000-01-01")
    cbb_hang.set("")


def load_data():
    conn = connect_db()
    if not conn: return
    cur = conn.cursor()

    tree.delete(*tree.get_children())
    cur.execute("SELECT * FROM laixe")

    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)

    conn.close()


def them_laixe():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_ngaysinh.get()
    hang = cbb_hang.get()

    if maso == "" or ten == "" or holot == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin!")
        return

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO laixe VALUES (%s,%s,%s,%s,%s,%s)",
                    (maso, holot, ten, phai, ngaysinh, hang))
        conn.commit()
        messagebox.showinfo("OK", "Đã thêm lái xe!")

        clear_input()
        load_data()

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

    conn.close()


def xoa_laixe():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chọn dòng", "Chọn lái xe để xóa!")
        return

    maso = tree.item(sel)["values"][0]

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM laixe WHERE maso=%s", (maso,))
    conn.commit()
    conn.close()

    load_data()


def sua_laixe():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chọn dòng", "Chọn lái xe để sửa!")
        return

    maso, holot, ten, phai, ns, hang = tree.item(sel)["values"]

    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, maso)

    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, holot)

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, ten)

    gender_var.set(phai)
    date_ngaysinh.set_date(ns)
    cbb_hang.set(hang)


def luu_laixe():
    maso = entry_maso.get()
    holot = entry_holot.get()
    ten = entry_ten.get()
    phai = gender_var.get()
    ngaysinh = date_ngaysinh.get()
    hang = cbb_hang.get()

    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE laixe
        SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, hangbang=%s
        WHERE maso=%s
    """, (holot, ten, phai, ngaysinh, hang, maso))

    conn.commit()
    conn.close()

    load_data()
    clear_input()


# ====================== NÚT CHỨC NĂNG ======================
btn_frame = tk.Frame(root)
btn_frame.pack(pady=7)

tk.Button(btn_frame, text="Thêm", width=10, command=them_laixe).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Sửa", width=10, command=sua_laixe).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Lưu", width=10, command=luu_laixe).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Xóa", width=10, command=xoa_laixe).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Tải lại", width=10, command=load_data).grid(row=0, column=4, padx=5)


load_data()
root.mainloop()