import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Machine Learning Application")

# Biến toàn cục
df = None
models = {}
errors = {}
algorithms = ['KNN', 'Hồi quy tuyến tính', 'Cây quyết định', 'Vector hỗ trợ']


# Hàm chọn file
def load_file():
    global df
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Thông báo", "Dữ liệu đã được load thành công!")
    else:
        messagebox.showerror("Lỗi", "Không có file nào được chọn!")


# Hàm train mô hình và tính sai số
def train_and_evaluate_models():
    global df, models, errors
    if df is None:
        messagebox.showerror("Lỗi", "Hãy chọn file dữ liệu trước!")
        return

    # Lấy dữ liệu
    x = np.array(df.iloc[:, :-1]).astype(np.float64)
    y = np.array(df.iloc[:, -1]).astype(np.float64)

    # Chia dữ liệu train/test
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

    # Khởi tạo mô hình
    models = {
        'KNN': KNeighborsRegressor(n_neighbors=3),
        'Hồi quy tuyến tính': LinearRegression(),
        'Cây quyết định': DecisionTreeRegressor(),
        'Vector hỗ trợ': SVR()
    }

    # Khởi tạo dictionary để lưu lỗi cho từng thuật toán
    errors = {
        'MSE': {},
        'RMSE': {},
        'MAE': {}
    }

    # Huấn luyện từng mô hình và tính sai số
    for algo_name, model in models.items():
        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)

        mse = mean_squared_error(y_test, y_predict)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_predict)

        errors['MSE'][algo_name] = mse
        errors['RMSE'][algo_name] = rmse
        errors['MAE'][algo_name] = mae

    messagebox.showinfo("Thông báo", "Huấn luyện và tính toán sai số hoàn tất!")


# Hàm vẽ biểu đồ so sánh sai số
def plot_error_comparison():
    if not errors:
        messagebox.showerror("Lỗi", "Hãy train mô hình trước!")
        return

    # Vẽ biểu đồ cột so sánh các chỉ số sai số MSE, RMSE, MAE
    metrics = ['MSE', 'RMSE', 'MAE']
    x = np.arange(len(algorithms))  # Vị trí các thuật toán
    width = 0.2  # Độ rộng của mỗi cột

    plt.figure(figsize=(10, 6))

    for i, metric in enumerate(metrics):
        plt.bar(x + i * width, [errors[metric][algo] for algo in algorithms], width=width, label=metric)

    plt.xticks(x + width, algorithms)
    plt.xlabel('Thuật toán')
    plt.ylabel('Giá trị lỗi')
    plt.title('So sánh sai số giữa các thuật toán')
    plt.legend()
    plt.show()


# Tạo layout giao diện
load_button = tk.Button(root, text="Chọn file", command=load_file)
load_button.pack()

train_button = tk.Button(root, text="Train và tính sai số", command=train_and_evaluate_models)
train_button.pack()

# Nút vẽ biểu đồ so sánh sai số
compare_errors_button = tk.Button(root, text="Vẽ biểu đồ so sánh sai số", command=plot_error_comparison)
compare_errors_button.pack()

# Chạy ứng dụng
root.mainloop()
