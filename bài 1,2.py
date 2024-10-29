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
        center_x, center_y = width // 2, height // 2
        radius = min(center_x, center_y) // 2
        cv2.circle(mask, (center_x, center_y), radius, (255, 255, 255), -1)

        blurred = cv2.GaussianBlur(img_processed, (21, 21), 0)
        img_processed = np.where(mask[..., None] == 255, img_processed, blurred)

    elif filter_type == 'remove_object':
        # Xóa đối tượng xung quanh (dùng thuật toán GrabCut để tách đối tượng)
        mask = np.zeros(img_processed.shape[:2], np.uint8)
        rect = (50, 50, img_processed.shape[1] - 100, img_processed.shape[0] - 100)  # Giữ lại vùng trung tâm
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        cv2.grabCut(img_processed, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img_processed = img_processed * mask2[:, :, np.newaxis]

    elif filter_type == 'beautify':
        # Chức năng làm đẹp: làm mịn da và tăng độ sáng, tương phản
        img_processed = beautify_image(img_processed)

    show_images(img_original, img_processed)

def sharpen_image(image, alpha=1):
    kernel = np.array([[0, -1, 0], [-1, 4 + alpha, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)
def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened

# Chức năng làm đẹp (làm mịn da, tăng độ sáng và tương phản)
def beautify_image(img):
    # Làm mịn da với Bilateral Filter để giữ lại chi tiết khuôn mặt
    smooth = cv2.bilateralFilter(img, 15, 40, 60)

    # Tăng độ sáng và tương phản
    alpha = 1  # Hệ số tăng độ sáng (có thể điều chỉnh)
    beta = 3  # Giảm tăng sáng
    beautified = cv2.convertScaleAbs(smooth, alpha=alpha, beta=beta)

    return beautified


# Lưu ảnh sau xử lý
def save_image():
    global img_processed
    if img_processed is None:
        return
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
    if save_path:
        cv2.imwrite(save_path, img_processed)


# Tạo GUI chính
root = Tk()
root.title("Image Filter Application")

# Khung chứa ảnh gốc và ảnh đã xử lý
frame = Frame(root)
frame.pack()

# Khung hiển thị ảnh gốc
Label(frame, text="Original Image").grid(row=0, column=0)
img_display_original = Label(frame)
img_display_original.grid(row=1, column=0)

# Khung hiển thị ảnh đã xử lý
Label(frame, text="Processed Image").grid(row=0, column=1)
img_display_processed = Label(frame)
img_display_processed.grid(row=1, column=1)

# Thêm khung để chứa các nút chức năng theo hàng ngang
button_frame = Frame(root)
button_frame.pack()

# Thêm các nút chức năng và sắp xếp theo hàng ngang
btn_open = Button(button_frame, text="Open Image", command=open_image)
btn_open.pack(side="left")

btn_filter_3x3 = Button(button_frame, text="3x3 Blur", command=lambda: apply_filter('blur_3x3'))
btn_filter_3x3.pack(side="left")

btn_filter_5x5 = Button(button_frame, text="5x5 Blur", command=lambda: apply_filter('blur_5x5'))
btn_filter_5x5.pack(side="left")

btn_sharpen = Button(button_frame, text="Sharpen", command=lambda: apply_filter('sharpen'))
btn_sharpen.pack(side="left")

btn_gray = Button(button_frame, text="Grayscale", command=lambda: apply_filter('gray'))
btn_gray.pack(side="left")

btn_invert = Button(button_frame, text="Invert Colors", command=lambda: apply_filter('invert'))
btn_invert.pack(side="left")

btn_pixelate = Button(button_frame, text="Pixelate", command=lambda: apply_filter('pixelate'))
btn_pixelate.pack(side="left")

btn_blur_background = Button(button_frame, text="Blur Background", command=lambda: apply_filter('blur_background'))
btn_blur_background.pack(side="left")

btn_beautify = Button(button_frame, text="Beautify", command=lambda: apply_filter('beautify'))
btn_beautify.pack(side="left")

btn_save = Button(button_frame, text="Save Image", command=save_image)
btn_save.pack(side="left")

# Biến toàn cục để lưu ảnh
img_original = None
img_processed = None

# Chạy vòng lặp chính của GUI
root.mainloop()
