import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog


def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    try:
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
        return data
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {e}")
        return np.array([])


def search_student(data, student_id):
    """Search for a student's information by ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])


def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])


def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."


def search_action():
    choice = choice_var.get()
    student_id = id_entry.get().strip()
    subject_name = subject_entry.get().strip()

    if choice == '1':  # Search for student info
        if not student_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sinh viên.")
            return
        result = search_student(data, student_id)
    elif choice == '2':  # Search for subject grades
        if not subject_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên môn học.")
            return
        result = search_subject(data, subject_name)
    elif choice == '3':  # Calculate average grade
        if not student_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ID sinh viên.")
            return
        result = calculate_average(data, student_id)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)


def load_file():
    """Open a file dialog to load the data."""
    global data
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        data = load_data(file_path)


def main():
    global data
    data = np.array([])  # Initialize data

    # Create main window
    root = tk.Tk()
    root.title("Tìm kiếm thông tin sinh viên")

    tk.Button(root, text="Tải dữ liệu", command=load_file).pack(pady=5)

    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')

    tk.Label(root, text="ID sinh viên:").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    tk.Button(root, text="Tìm kiếm", command=search_action).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
