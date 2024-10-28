import pygame
import random
import sys
from pygame.locals import *

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình
RONG, CAO = 800, 400
man_hinh = pygame.display.set_mode((RONG, CAO))
pygame.display.set_caption("Game Xe Đi Trên Đồi Núi")

# Màu sắc
TRANG = (255, 255, 255)
DEN = (0, 0, 0)

# Font chữ và đồng hồ
font = pygame.font.SysFont(None, 36)
dong_ho = pygame.time.Clock()

# Tải hình ảnh
xe_img = pygame.image.load('xe.png')  # Ảnh xe
xe_img = pygame.transform.scale(xe_img, (80, 40))  # Điều chỉnh kích thước xe
da_img = pygame.image.load('da.png')  # Ảnh chướng ngại vật (cục đá)
da_img = pygame.transform.scale(da_img, (40, 40))  # Điều chỉnh kích thước đá

# Biến trò chơi
xe_rect = xe_img.get_rect()
xe_rect.center = (100, CAO // 2)  # Vị trí ban đầu của xe
van_toc_xe = 5
diem_so = 0
cham_da = False



# Hàm tạo chướng ngại vật
def tao_da():
    x = random.randint(RONG, RONG + 200)
    y = random.randint(250, CAO - 50)
    return pygame.Rect(x, y, 40, 40)


# Danh sách chướng ngại vật (cục đá)
cac_da = [tao_da()]

# Thời gian bắt đầu
bat_dau = pygame.time.get_ticks()

# Vòng lặp chính của trò chơi
while True:
    man_hinh.fill(TRANG)

    # Vẽ địa hình đồi núi


    # Vẽ xe
    man_hinh.blit(xe_img, xe_rect.topleft)

    # Vẽ chướng ngại vật (cục đá)
    for da in cac_da:
        man_hinh.blit(da_img, da.topleft)

    # Cập nhật chướng ngại vật
    for da in cac_da:
        da.x -= van_toc_xe  # Đá di chuyển từ phải qua trái
        if da.right < 0:  # Khi đá ra khỏi màn hình thì tạo đá mới
            cac_da.remove(da)
            cac_da.append(tao_da())

    # Kiểm tra va chạm
    for da in cac_da:
        if xe_rect.colliderect(da):
            cham_da = True
            break

    if cham_da:
        chu_game_over = font.render("Game Over!", True, (255, 0, 0))
        man_hinh.blit(chu_game_over, (RONG // 2 - 100, CAO // 2))
        pygame.display.update()
        pygame.time.wait(2000)  # Tạm dừng 2 giây
        pygame.quit()
        sys.exit()

    # Điều khiển xe
    keys = pygame.key.get_pressed()
    if keys[K_UP] and xe_rect.top > 0:
        xe_rect.y -= 5  # Di chuyển lên
    if keys[K_DOWN] and xe_rect.bottom < CAO:
        xe_rect.y += 5  # Di chuyển xuống

    # Hiển thị thời gian di chuyển
    thoi_gian_da_troi = (pygame.time.get_ticks() - bat_dau) / 1000  # Tính bằng giây
    chu_thoi_gian = font.render(f"Thời gian: {int(thoi_gian_da_troi)}", True, DEN)
    man_hinh.blit(chu_thoi_gian, (20, 20))

    # Cập nhật màn hình
    pygame.display.update()
    dong_ho.tick(60)  # 60 FPS

    # Xử lý sự kiện
    for su_kien in pygame.event.get():
        if su_kien.type == QUIT:
            pygame.quit()
            sys.exit()
