import pygame, sys
from pygame.locals import *
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước màn hình
chieu_dai = 800
chieu_rong = 500
w = pygame.display.set_mode((chieu_dai, chieu_rong))
pygame.display.set_caption('Game Bắn Chim')

# ------------- tạo nền của game là 1 ảnh -----------------
anh_nen_list = [
    pygame.image.load('nui.jpg'),
    pygame.image.load('bien.png'),
    pygame.image.load('thanh_pho.png')
]
anh_nen_list = [pygame.transform.scale(nen, (chieu_dai, chieu_rong)) for nen in anh_nen_list]

# ----------- tạo ảnh các con chim --------------
chim1 = pygame.image.load('chim1.png')
chim2 = pygame.image.load('chim2.png')

# ----------- tạo ảnh thợ săn --------------
tho_san = pygame.image.load('tho_san.png')
tho_san = pygame.transform.scale(tho_san, (50, 80))

# ----------- tạo người nhảy dù --------------
nguoi_nhay_du = pygame.image.load('nguoi_nhay_du.png')
nguoi_nhay_du = pygame.transform.scale(nguoi_nhay_du, (40, 50))

# ----------- tạo gói quà và đạn nổ --------------
goi_qua = pygame.image.load('goi_qua.png')
goi_qua = pygame.transform.scale(goi_qua, (30, 30))
dan_no = pygame.image.load('dan_no.png')
dan_no = pygame.transform.scale(dan_no, (30, 30))

# Biến thợ săn
tho_san_x = chieu_dai // 2 - 25
tho_san_y = chieu_rong - 90

# Biến tốc độ và cấp độ
toc_do_chim = 2
toc_do_nhay_du = 1
toc_do_ban = 5
dan_ba_tia = False
thoi_gian_ba_tia = 0
diem = 0
game_over = False

# Vị trí người nhảy dù
nguoi_nhay_du_x, nguoi_nhay_du_y = random.randint(0, chieu_dai - 50), -50
nguoi_nhay_du_mau = 3

# Danh sách đạn và gói quà
dan_list = []
goi_qua_x, goi_qua_y = random.randint(0, chieu_dai - 30), -50
goi_qua_xuat_hien = False

# Vị trí ban đầu của chim
so_chim = 2
chim_list = [
    {'image': pygame.transform.scale(chim1, (40, 50)), 'x': random.randint(0, chieu_dai - 80), 'y': random.randint(50, 300), 'speed': 2, 'score': 1},
    {'image': pygame.transform.scale(chim2, (60, 80)), 'x': random.randint(0, chieu_dai - 80), 'y': random.randint(50, 300), 'speed': 1, 'score': 3}
]

# Khung thời gian
FPS = 60
fpsClock = pygame.time.Clock()

# Thời gian cho màn chơi
thoi_gian_con_lai = 60
start_time = pygame.time.get_ticks()

# Hàm vẽ đạn
def ve_dan(dan_list):
    for dan in dan_list:
        pygame.draw.rect(w, (255, 0, 0), dan)

# Hàm kiểm tra va chạm
def kiem_tra_va_cham(dan, chim_rect):
    return dan.colliderect(chim_rect)

# Hàm tạo viên đạn mới
def tao_dan(x, y):
    return pygame.Rect(x + 22, y, 5, 10)

# Hàm hiển thị game over
def hien_thi_game_over():
    font = pygame.font.SysFont('Arial', 50)
    text_game_over = font.render('Game Over', True, (255, 0, 0))
    w.blit(text_game_over, (chieu_dai // 2 - 100, chieu_rong // 2 - 50))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Hàm thay đổi nền theo cấp độ
def doi_nen_theo_diem():
    cap_do = min(diem // 10, len(anh_nen_list) - 1)
    return anh_nen_list[cap_do]

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            dan_list.append(tao_dan(tho_san_x, tho_san_y))
        if event.type == KEYDOWN and event.key == K_SPACE:
            dan_list.append(tao_dan(tho_san_x, tho_san_y))

    # Kiểm tra phím di chuyển
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and tho_san_x > 0:
        tho_san_x -= 5
    if keys[K_RIGHT] and tho_san_x < chieu_dai - 50:
        tho_san_x += 5

    # Vẽ nền
    w.blit(doi_nen_theo_diem(), (0, 0))

    # Di chuyển chim
    for chim_obj in chim_list:
        chim_obj['x'] += chim_obj['speed']
        chim_rect = w.blit(chim_obj['image'], (chim_obj['x'], chim_obj['y']))
        if chim_obj['x'] > chieu_dai or chim_obj['x'] < 0:
            chim_obj['x'], chim_obj['y'] = random.randint(0, chieu_dai - 80), random.randint(50, 300)
        # Kiểm tra va chạm đạn và chim
        for dan in dan_list:
            if kiem_tra_va_cham(dan, chim_rect):
                diem += chim_obj['score']
                dan_list.remove(dan)
                chim_obj['x'], chim_obj['y'] = random.randint(0, chieu_dai - 80), random.randint(50, 300)

    # Di chuyển đạn
    for dan in dan_list:
        dan.y -= toc_do_ban

    # Di chuyển người nhảy dù
    nguoi_nhay_du_y += toc_do_nhay_du
    nguoi_nhay_du_rect = w.blit(nguoi_nhay_du, (nguoi_nhay_du_x, nguoi_nhay_du_y))

    # Kiểm tra va chạm đạn và người nhảy dù
    for dan in dan_list:
        if kiem_tra_va_cham(dan, nguoi_nhay_du_rect):
            nguoi_nhay_du_mau -= 1
            dan_list.remove(dan)
            if nguoi_nhay_du_mau <= 0:
                game_over = True

    # Hiển thị thanh máu người nhảy dù
    pygame.draw.rect(w, (255, 0, 0), (nguoi_nhay_du_x, nguoi_nhay_du_y - 10, 40, 5))
    pygame.draw.rect(w, (0, 255, 0), (nguoi_nhay_du_x, nguoi_nhay_du_y - 10, nguoi_nhay_du_mau * 40 / 3, 5))

    # Vẽ gói quà và kiểm tra va chạm
    if goi_qua_xuat_hien:
        goi_qua_y += 3
        goi_qua_rect = w.blit(goi_qua, (goi_qua_x, goi_qua_y))
        if goi_qua_y > chieu_rong:
            goi_qua_xuat_hien = False
        for dan in dan_list:
            if kiem_tra_va_cham(dan, goi_qua_rect):
                dan_ba_tia = True
                thoi_gian_ba_tia = pygame.time.get_ticks()
                goi_qua_xuat_hien = False

    # Reset đạn ba tia sau 5 giây
    if dan_ba_tia and pygame.time.get_ticks() - thoi_gian_ba_tia > 5000:
        dan_ba_tia = False

    # Xuất hiện gói quà ngẫu nhiên
    if not goi_qua_xuat_hien and random.randint(0, 1000) < 5:
        goi_qua_x, goi_qua_y = random.randint(0, chieu_dai - 30), -50
        goi_qua_xuat_hien = True

    # Hiển thị điểm số
    font = pygame.font.SysFont('Arial', 30)
    text_diem = font.render(f'Score: {diem}', True, (0, 255, 0))
    w.blit(text_diem, (10, 10))

    # Hiển thị thời gian
    thoi_gian_da_choi = (pygame.time.get_ticks() - start_time) / 1000
    thoi_gian_con_lai = max(60 - thoi_gian_da_choi, 0)
    text_thoi_gian = font.render(f'Time: {int(thoi_gian_con_lai)}', True, (0, 255, 0))
    w.blit(text_thoi_gian, (chieu_dai - 150, 10))

    # Kiểm tra điều kiện game over
    if game_over or thoi_gian_con_lai <= 0:
        hien_thi_game_over()

    # Vẽ thợ săn và đạn
    w.blit(tho_san, (tho_san_x, tho_san_y))
    ve_dan(dan_list)

    pygame.display.update()
    fpsClock.tick(FPS)
