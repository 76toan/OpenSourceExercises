import cv2
import numpy as np
from tkinter import filedialog, Tk, Button, Label, Frame
from PIL import Image, ImageTk


# Hàm chọn ảnh từ máy tính
def open_image():
    global img_original, img_processed
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        img_original = cv2.imread(file_path)
        img_processed = img_original.copy()  # Tạo bản sao để xử lý
        show_images(img_original, img_processed)


# Hiển thị ảnh gốc và ảnh đã xử lý trên GUI
def show_images(original, processed):
    img_rgb_original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    if len(processed.shape) == 2:  # Xử lý ảnh đen trắng
        img_rgb_processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    else:
        img_rgb_processed = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

    img_pil_original = Image.fromarray(img_rgb_original)
    img_pil_processed = Image.fromarray(img_rgb_processed)

    img_tk_original = ImageTk.PhotoImage(img_pil_original)
    img_tk_processed = ImageTk.PhotoImage(img_pil_processed)

    img_display_original.config(image=img_tk_original)
    img_display_original.image = img_tk_original

    img_display_processed.config(image=img_tk_processed)
    img_display_processed.image = img_tk_processed


# Áp dụng bộ lọc lên ảnh đã xử lý
def apply_filter(filter_type):
    global img_original, img_processed
    if img_original is None:
        return
    img_processed = img_original.copy()  # Reset lại ảnh gốc để xử lý từ đầu

    if filter_type == 'blur_3x3':
        kernel = np.ones((3, 3), np.float32) / 9.0
        img_processed = cv2.filter2D(img_processed, -1, kernel)

    elif filter_type == 'blur_5x5':
        kernel = np.ones((5, 5), np.float32) / 25.0
        img_processed = cv2.filter2D(img_processed, -1, kernel)

    elif filter_type == 'sharpen':
        kernel = np.array([[0, -1, 0], [-1, 5.1, -1], [0, -1, 0]])
        img_processed = cv2.filter2D(img_processed, -1, kernel)

    elif filter_type == 'sharpen':
        img_processed = sharpen_image(img_processed, alpha=10)  # alpha có thể điều chỉnh
    elif filter_type == 'sharpen':
        img_processed = unsharp_mask(img_processed)


    elif filter_type == 'gray':
        img_processed = cv2.cvtColor(img_processed, cv2.COLOR_BGR2GRAY)

    elif filter_type == 'invert':
        img_processed = cv2.bitwise_not(img_processed)

    elif filter_type == 'pixelate':
        pixel_size = 10
        height, width = img_processed.shape[:2]
        temp = cv2.resize(img_processed, (width // pixel_size, height // pixel_size), interpolation=cv2.INTER_LINEAR)
        img_processed = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

    elif filter_type == 'blur_background':
        height, width = img_processed.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
