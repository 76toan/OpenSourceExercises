import numpy as np
import tkinter as tk
from tkinter import messagebox, IntVar, Radiobutton, Button
import csv

from scipy.constants import value

students = np.empty((0, 5), dtype=object)
result = np.empty((0, 5), dtype=object)

def load_data():
    global students
    try:
        with open('data.csv', mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            students = np.array(list(reader), dtype=object)
    except FileNotFoundError:
        students = np.empty((0, 5), dtype=object)

def save_data():
    global students
    with open('data.csv', mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(students)

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
    if id in students[:,0]:
        messagebox.showerror("Error", "Thông tin Id bạn vừa nhập đã tồn tại")
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

    new_student = np.array([[id, name, math, physics, chemistry]])
    students = np.append(students, new_student, axis=0)
    print(students)
    save_data()
    messagebox.showinfo("Success", "Thêm sinh viên thành công")
    clear_entries()

def delete_info():
    global students
    id = id_entry.get()
    if not id:
        messagebox.showerror("Error", "Vui lòng nhập id sinh viên mà bạn muốn xóa")
        return
    else:
        if id in students[:, 0]:
            students = students[students[:, 0] != id]
            print(students)
            save_data()
            messagebox.showinfo("Success", f"Xóa sinh viên có id {id} thành công")
            clear_entries()
        else:
            messagebox.showwarning("Warning", "Id bạn vừa nhập không tồn tại")

def sort_info():
    sort_window = tk.Tk()
    sort_window.title("Sort students")
    sort_window.geometry("500x250")

    global sort_by
    sort_by = IntVar()

    radio_math = Radiobutton(sort_window, text="Sort by Math", variable=sort_by, value=1)
    radio_physics = Radiobutton(sort_window, text="Sort by Physics", variable=sort_by, value=2)
    radio_chemistry = Radiobutton(sort_window, text="Sort by Chemistry", variable=sort_by, value=3)
    radio_math.pack()
    radio_physics.pack()
    radio_chemistry.pack()

    btn_sort = Button(sort_window, text="Xác nhận", command=sort_students_by)
    btn_sort.pack()

    sort_window.mainloop()

def sort_students_by():
    global students, sort_by
    if sort_by.get() == 1:
        students = students[students[:, 2].argsort()]
    elif sort_by.get() == 2:
        students = students[students[:, 3].argsort()]
    elif sort_by.get() == 3:
        students = students[students[:, 4].argsort()]

    print(students)
    save_data()

    messagebox.showinfo("Thành công", "Sắp xếp thành công!")





def search_info():
    global result
    id = id_entry.get()
    if not id:
        messagebox.showerror("Error", "Vui lòng nhập id sinh viên mà bạn muốn tìm kiếm")
        return
    else:
        result = students[students[:, 0] == id]
        if result.size > 0:
            messagebox.showinfo("StudentInformation", f"Thông tin sinh viên bạn tìm kiếm là id:{id}, name:{result[0][1]}, "
                                                      f"math:{result[0][2]}, physics: {result[0][3]}, chemistry: {result[0][4]}")
        else:
            messagebox.showwarning("Warning", "Không tìm thấy thông tin sinh viên với id bạn vừa nhập")

def show_info():
    print(students)


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

add_button = Button(root, text="Thêm thông tin", command=add_info)
delete_button = Button(root, text="Xóa thông tin", command=delete_info)
sort_button = Button(root, text="Sắp xếp", command=sort_info)
search_button = Button(root, text="Tìm kiếm", command=search_info)
showinfo_button = Button(root, text="Hiển thị thông tin", command=show_info)

add_button.grid(row=5, column=0)
delete_button.grid(row=6, column=0)
sort_button.grid(row=7, column=0)
search_button.grid(row=8, column=0)
showinfo_button.grid(row=9, column=0)

load_data()

root.mainloop()

