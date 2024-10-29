import pygame
import random

# Kích thước màn hình và bảng xếp gạch
chieu_dai = 300
chieu_rong = 600
khoang_gach = 30
hang = chieu_rong // khoang_gach
cot = chieu_dai // khoang_gach

# Khởi tạo Pygame
pygame.init()
mau_nen = (0, 0, 0)
mau_gach = [(0, 255, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255)]
mau_duong_ke = (128, 128, 128)
man_hinh = pygame.display.set_mode((chieu_dai, chieu_rong))
pygame.display.set_caption('Game Xep Gach')

# Các hình dạng gạch (Tetris)
cac_khoi = [
    [[1, 1, 1, 1]],  # Dài
    [[1, 1], [1, 1]],  # Vuông
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[0, 1, 1], [1, 1, 0]]  # S
]


# Tạo bảng xếp gạch
def tao_bang():
    return [[(0, 0, 0) for _ in range(cot)] for _ in range(hang)]


# Vẽ bảng xếp gạch
def ve_bang(bang):
    for i in range(hang):
        for j in range(cot):
            pygame.draw.rect(man_hinh, bang[i][j], (j * khoang_gach, i * khoang_gach, khoang_gach, khoang_gach), 0)
            pygame.draw.rect(man_hinh, mau_duong_ke, (j * khoang_gach, i * khoang_gach, khoang_gach, khoang_gach), 1)


# Vẽ khối gạch
def ve_khoi(khoi, vi_tri, mau):
    for i, hang_khoi in enumerate(khoi):
        for j, o in enumerate(hang_khoi):
            if o:
                pygame.draw.rect(man_hinh, mau,
                                 (vi_tri[0] + j * khoang_gach, vi_tri[1] + i * khoang_gach, khoang_gach, khoang_gach),
                                 0)
                pygame.draw.rect(man_hinh, mau_duong_ke,
                                 (vi_tri[0] + j * khoang_gach, vi_tri[1] + i * khoang_gach, khoang_gach, khoang_gach),
                                 1)


# Kiểm tra va chạm
def kiem_tra_va_cham(bang, khoi, vi_tri):
    for i, hang_khoi in enumerate(khoi):
        for j, o in enumerate(hang_khoi):
            if o:
                x = vi_tri[0] // khoang_gach + j
                y = vi_tri[1] // khoang_gach + i
                if x < 0 or x >= cot or y >= hang or bang[y][x] != (0, 0, 0):
                    return True
    return False


# Xóa hàng đầy
def xoa_hang(bang):
    diem = 0
    for i in range(hang):
        if (0, 0, 0) not in bang[i]:
            del bang[i]
            bang.insert(0, [(0, 0, 0) for _ in range(cot)])
            diem += 100  # Cộng 100 điểm khi xóa hàng
    return diem


# Hiển thị điểm số trên màn hình
def hien_thi_diem(diem):
    font = pygame.font.SysFont('Arial', 24)
    text = font.render(f'Score: {diem}', True, (255, 255, 255))
    man_hinh.blit(text, (10, 10))


# Màn hình chính với nút bắt đầu
def man_hinh_chinh():
    man_hinh.fill(mau_nen)
    font = pygame.font.SysFont('Arial', 40)
    text = font.render("Game Xep Gach", True, (255, 255, 255))
    man_hinh.blit(text, (chieu_dai // 2 - text.get_width() // 2, chieu_rong // 3))

    start_button = pygame.Rect(chieu_dai // 2 - 50, chieu_rong // 2, 100, 50)
    pygame.draw.rect(man_hinh, (0, 255, 0), start_button)
    font = pygame.font.SysFont('Arial', 24)
    start_text = font.render("Start", True, (0, 0, 0))
    man_hinh.blit(start_text, (chieu_dai // 2 - start_text.get_width() // 2, chieu_rong // 2 + 10))

    pygame.display.update()
    return start_button


# Hàm chính của trò chơi
def game():
    bang = tao_bang()
    diem = 0
    fps = 30
    clock = pygame.time.Clock()

    khoi_hien_tai = random.choice(cac_khoi)
    mau_khoi = random.choice(mau_gach)
    vi_tri_khoi = [cot // 2 * khoang_gach, 0]

    dem_thoi_gian = 0
    toc_do_rơi = 10

    running = True
    while running:
        man_hinh.fill(mau_nen)
        ve_bang(bang)
        ve_khoi(khoi_hien_tai, vi_tri_khoi, mau_khoi)
        hien_thi_diem(diem)
        pygame.display.update()

        dem_thoi_gian += 1
        if dem_thoi_gian >= toc_do_rơi:
            vi_tri_khoi[1] += khoang_gach
            dem_thoi_gian = 0
            if kiem_tra_va_cham(bang, khoi_hien_tai, vi_tri_khoi):
                vi_tri_khoi[1] -= khoang_gach
                for i, hang_khoi in enumerate(khoi_hien_tai):
                    for j, o in enumerate(hang_khoi):
                        if o:
                            x = vi_tri_khoi[0] // khoang_gach + j
                            y = vi_tri_khoi[1] // khoang_gach + i
                            bang[y][x] = mau_khoi
                diem += xoa_hang(bang)
                khoi_hien_tai = random.choice(cac_khoi)
                mau_khoi = random.choice(mau_gach)
                vi_tri_khoi = [cot // 2 * khoang_gach, 0]
                if kiem_tra_va_cham(bang, khoi_hien_tai, vi_tri_khoi):
                    running = False  # Kết thúc game nếu không còn chỗ

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    vi_tri_khoi[0] -= khoang_gach
                    if kiem_tra_va_cham(bang, khoi_hien_tai, vi_tri_khoi):
                        vi_tri_khoi[0] += khoang_gach
                elif event.key == pygame.K_RIGHT:
                    vi_tri_khoi[0] += khoang_gach
                    if kiem_tra_va_cham(bang, khoi_hien_tai, vi_tri_khoi):
                        vi_tri_khoi[0] -= khoang_gach
                elif event.key == pygame.K_DOWN:
                    vi_tri_khoi[1] += khoang_gach
                    if kiem_tra_va_cham(bang, khoi_hien_tai, vi_tri_khoi):
                        vi_tri_khoi[1] -= khoang_gach
                elif event.key == pygame.K_SPACE:
                    khoi_quay = list(zip(*khoi_hien_tai[::-1]))  # Xoay khối
                    if not kiem_tra_va_cham(bang, khoi_quay, vi_tri_khoi):
                        khoi_hien_tai = khoi_quay

        clock.tick(fps)

    return diem  # Trả về điểm khi game kết thúc


# Chạy trò chơi với màn hình chính
def main():
    game_over = False
    while True:
        if not game_over:
            start_button = man_hinh_chinh()
            start_game = False
            while not start_game:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if start_button.collidepoint(event.pos):
                            start_game = True

            diem = game()  # Chạy trò chơi và lấy điểm
            game_over = True

        # Hiển thị màn hình game over
        man_hinh.fill(mau_nen)
        font = pygame.font.SysFont('Arial', 40)
        text = font.render(f'Game Over! Point: {diem}', True, (255, 255, 255))
        man_hinh.blit(text, (chieu_dai // 2 - text.get_width() // 2, chieu_rong // 3))

        # Nút để quay lại màn hình chính
        play_again_button = pygame.Rect(chieu_dai // 2 - 50, chieu_rong // 2, 100, 50)
        pygame.draw.rect(man_hinh, (0, 255, 0), play_again_button)
        font = pygame.font.SysFont('Arial', 24)
        play_again_text = font.render("Restart", True, (0, 0, 0))
        man_hinh.blit(play_again_text, (chieu_dai // 2 - play_again_text.get_width() // 2, chieu_rong // 2 + 10))

        pygame.display.update()

        wait_for_click = True
        while wait_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        game_over = False
                        wait_for_click = False


# Chạy chương trình
main()
pygame.quit()
