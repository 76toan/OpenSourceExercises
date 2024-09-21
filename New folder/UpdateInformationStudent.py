import numpy as np
import tkinter as tk
from tkinter import messagebox

students = np.empty((0, 5), dtype=object)

def clear_entries():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    math_entry.delete(0, tk.END)
    physics_entry.delete(0, tk.END)
    chemistry_entry.delete(0, tk.END)

def add_info():
    global students
    id = id_entry.get()
    name = name_entry.get()
    try:
        math = float(math_entry.get())
        physics = float(physics_entry.get())
        chemistry = float(chemistry_entry.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Điểm Toán, Lý, Hóa phải là số")
        return
    if not id:
        messagebox.showerror("Error", "Vui lòng nhập thông tin id sinh viên")
        return
    if not name:
        messagebox.showerror("Error", "Vui lòng nhập thông tin họ tên sinh viên")
        return
    if math < 0 or math > 10:
        messagebox.showerror("Error", "Vui lòng nhập điểm Toán hợp lệ (từ 0 đến 10)")
        return
    if physics < 0 or physics > 10:
        messagebox.showerror("Error", "Vui lòng nhập điểm Toán hợp lệ (từ 0 đến 10)")
        return
    if chemistry < 0 or chemistry > 10:
        messagebox.showerror("Error", "Vui lòng nhập điểm Toán hợp lệ (từ 0 đến 10)")
        return

    new_student = np.array([id, name, math, physics, chemistry])
    students = np.append(students, new_student, axis=0)
    messagebox.showinfo("Success", "Thêm sinh viên thành công")
    clear_entries()

def delete_info():
    pass

def sort_info():
    pass

def search_info():
    pass

root = tk.Tk()
root.title("Student infomation management")
root.geometry("1000x500")

tk.Label(root, text="ID").grid(row=0, column=0)
tk.Label(root, text="Họ và tên").grid(row=1, column=0)
tk.Label(root, text="Điểm Toán").grid(row=2, column=0)
tk.Label(root, text="Điểm Lý").grid(row=3, column=0)
tk.Label(root, text="Điểm Hóa").grid(row=4, column=0)

id_entry = tk.Entry(root)
name_entry = tk.Entry(root)
math_entry = tk.Entry(root)
physics_entry = tk.Entry(root)
chemistry_entry = tk.Entry(root)

id_entry.grid(row=0, column=1)
name_entry.grid(row=1, column=1)
math_entry.grid(row=2, column=1)
physics_entry.grid(row=3, column=1)
chemistry_entry.grid(row=4, column=1)

add_button = tk.Button(root, text="Thêm thông tin", command=add_info)
delete_button = tk.Button(root, text="Xóa thông tin", command=delete_info)
sort_button = tk.Button(root, text="Sắp xếp", command=sort_info)
search_button = tk.Button(root, text="Tìm kiếm", command=search_info)

add_button.grid(row=5, column=0)
delete_button.grid(row=6, column=0)
sort_button.grid(row=7, column=0)
search_button.grid(row=8, column=1)

root.mainloop()

