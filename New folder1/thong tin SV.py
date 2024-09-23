import numpy as np

def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    data = np.genfromtxt(file_path, delimiter=',', dtype=None, encoding='utf-8', skip_header=1)
    return data

def search_student(data, student_id):
    """Search for a student's information by ID."""
    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        print(f"Không tìm thấy thông tin cho sinh viên có ID {student_id}.")
    else:
        print("Thông tin sinh viên:")
        for row in student_data:
            print(row)

def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        print(f"Không tìm thấy điểm cho môn học {subject_name}.")
    else:
        print("Điểm các sinh viên cho môn học:")
        for row in subject_data:
            print(f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}")

def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        print(f"Không tìm thấy thông tin cho sinh viên có ID {student_id}.")
    else:
        grades = student_data[:, 3].astype(float)  # Convert grades to float
        average_grade = np.mean(grades)
        print(f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}.")

def main():
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    while True:
        print("\n1. Tìm kiếm thông tin sinh viên")
        print("2. Tìm kiếm điểm môn học")
        print("3. Tính TBC điểm của sinh viên")
        print("4. Thoát")

        choice = input("Chọn tùy chọn: ")

        if choice == '1':
            student_id = input("Nhập ID sinh viên: ")
            search_student(data, student_id)
        elif choice == '2':
            subject_name = input("Nhập tên môn học: ")
            search_subject(data, subject_name)
        elif choice == '3':
            student_id = input("Nhập ID sinh viên: ")
            calculate_average(data, student_id)
        elif choice == '4':
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

if __name__ == "__main__":
    main()
