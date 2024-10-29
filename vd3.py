import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE  # Thêm thư viện SMOTE để cân bằng dữ liệu
import matplotlib.pyplot as plt

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Machine Learning Application")

# Biến toàn cục
df = None
model = None
accuracy = None
y_test = y_predict = None
all_accuracies = {}  # Dictionary lưu độ chính xác cho các thuật toán


# Hàm chọn file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được load thành công!")
        columns_label.config(text=f"Columns: {', '.join(df.columns)}")
    else:
        messagebox.showerror("Lỗi", "Không có file nào được chọn!")


# Hàm kiểm tra phân phối dữ liệu (Potability)
def check_data_distribution():
    global df
    if df is None:
        messagebox.showerror("Lỗi", "Hãy chọn file dữ liệu trước!")
        return

    # Kiểm tra phân phối dữ liệu theo lớp Potability
    potability_counts = df['Potability'].value_counts()
    potability_label.config(text=f"Phân phối dữ liệu: {potability_counts.to_dict()}")


# Hàm làm sạch dữ liệu
def clean_data():
    global df
    if df is None:
        messagebox.showerror("Lỗi", "Hãy chọn file dữ liệu trước!")
        return

    # Loại bỏ các hàng có giá trị null
    df = df.dropna()
    messagebox.showinfo("Thông báo", "Dữ liệu đã được làm sạch (loại bỏ các hàng null)!")


# Hàm chuẩn hóa dữ liệu
def normalize_data():
    global df
    if df is None:
        messagebox.showerror("Lỗi", "Hãy chọn file dữ liệu trước!")
        return

    # Chọn loại chuẩn hóa
    norm_type = norm_var.get()

    if norm_type == "Standardization":
        scaler = StandardScaler()
    elif norm_type == "Min-Max Scaling":
        scaler = MinMaxScaler()

    try:
        df.iloc[:, :-1] = scaler.fit_transform(df.iloc[:, :-1])
        messagebox.showinfo("Thông báo", "Dữ liệu đã được chuẩn hóa thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Xảy ra lỗi khi chuẩn hóa: {e}")


# Hàm train mô hình và cân bằng dữ liệu
def train_model():
    global model, df, accuracy, y_test, y_predict, all_accuracies
    if df is None:
        messagebox.showerror("Lỗi", "Hãy chọn file dữ liệu trước!")
        return

    # Chọn thuật toán
    algorithm = algo_var.get()
    x = np.array(df.iloc[:, :-1]).astype(np.float64)
    y = np.array(df.iloc[:, -1]).astype(np.float64)

    # Cân bằng dữ liệu bằng SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(x, y)

    # Chia dữ liệu train/test
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=1)

    if algorithm == "KNN":
        model = KNeighborsClassifier(n_neighbors=3)
    elif algorithm == "Hồi quy logistic":
        model = LogisticRegression()
    elif algorithm == "Cây quyết định":
        model = DecisionTreeClassifier()
    elif algorithm == "Vector hỗ trợ":
        model = SVC()

    # Train model
    model.fit(X_train, y_train)
    y_predict = model.predict(X_test)

    # Tính độ chính xác
    accuracy = accuracy_score(y_test, y_predict)

    # Lưu độ chính xác cho thuật toán hiện tại
    all_accuracies[algorithm] = accuracy

    # Hiển thị kết quả
    accuracy_label.config(text=f"Độ chính xác: {accuracy:.2f}")

    # Vẽ đồ thị kết quả dự đoán
    plt.figure()
    plt.plot(range(0, len(y_test)), y_test, 'ro', label='Dữ liệu gốc (Có thể uống)')
    plt.plot(range(0, len(y_predict)), y_predict, 'bo', label='Dự đoán')
    for i in range(0, len(y_test)):
        plt.plot([i, i], [y_test[i], y_predict[i]], 'g')
    plt.title('Kết quả dự đoán (1: Có thể uống, 0: Không thể uống)')
    plt.legend()
    plt.show()


# Hàm dự đoán dữ liệu mới
def predict_new():
    if model is None:
        messagebox.showerror("Lỗi", "Hãy train mô hình trước!")
        return

    # Lấy dữ liệu mới
    new_data = new_data_entry.get()
    try:
        new_data = np.array([float(i) for i in new_data.split(',')]).reshape(1, -1)
        prediction = model.predict(new_data)
        if prediction[0] == 1:
            result_label.config(text="Kết quả dự đoán: Có thể uống được")
        else:
            result_label.config(text="Kết quả dự đoán: Không thể uống được")
    except ValueError:
        messagebox.showerror("Lỗi", "Dữ liệu nhập không hợp lệ!")


# Hàm vẽ biểu đồ so sánh độ chính xác giữa các thuật toán
def compare_algorithms():
    if not all_accuracies:
        messagebox.showerror("Lỗi", "Hãy train ít nhất một thuật toán trước!")
        return

    # Lấy dữ liệu để vẽ biểu đồ
    algorithms = list(all_accuracies.keys())
    accuracies = [all_accuracies[algo] for algo in algorithms]

    # Vẽ biểu đồ cột so sánh
    plt.figure()
    plt.bar(algorithms, accuracies, color=['blue', 'orange', 'green', 'red'])
    plt.xlabel('Thuật toán')
    plt.ylabel('Độ chính xác')
    plt.title('So sánh độ chính xác giữa các thuật toán')
    plt.tight_layout()
    plt.show()


# Tạo layout giao diện
load_button = tk.Button(root, text="Chọn file", command=load_file)
load_button.pack()

columns_label = tk.Label(root, text="Columns: N/A")
columns_label.pack()

# Hiển thị phân phối lớp Potability
potability_label = tk.Label(root, text="Phân phối dữ liệu: N/A")
potability_label.pack()

check_distribution_button = tk.Button(root, text="Kiểm tra phân phối dữ liệu", command=check_data_distribution)
check_distribution_button.pack()

clean_button = tk.Button(root, text="Làm sạch dữ liệu", command=clean_data)
clean_button.pack()

norm_var = tk.StringVar()
norm_var.set("Standardization")  # Giá trị mặc định
normalize_menu = tk.OptionMenu(root, norm_var, "Standardization", "Min-Max Scaling")
normalize_menu.pack()

normalize_button = tk.Button(root, text="Chuẩn hóa dữ liệu", command=normalize_data)
normalize_button.pack()

algo_var = tk.StringVar()
algo_var.set("KNN")  # Giá trị mặc định
algorithms_menu = tk.OptionMenu(root, algo_var, "KNN", "Hồi quy logistic", "Cây quyết định", "Vector hỗ trợ")
algorithms_menu.pack()

train_button = tk.Button(root, text="Train", command=train_model)
train_button.pack()

accuracy_label = tk.Label(root, text="Độ chính xác: N/A")
accuracy_label.pack()

new_data_label = tk.Label(root, text="Nhập dữ liệu mới (phân tách bởi dấu phẩy):")
new_data_label.pack()

new_data_entry = tk.Entry(root)
new_data_entry.pack()

predict_button = tk.Button(root, text="Dự đoán", command=predict_new)
predict_button.pack()

result_label = tk.Label(root, text="Kết quả dự đoán: N/A")
result_label.pack()

# Nút vẽ biểu đồ so sánh độ chính xác giữa các thuật toán
compare_button = tk.Button(root, text="So sánh thuật toán", command=compare_algorithms)
compare_button.pack()

# Chạy ứng dụng
root.mainloop()

