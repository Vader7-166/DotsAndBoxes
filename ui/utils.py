import pygame
import math
from constants import *

def lerp(a, b, t):
    return a + (b - a) * t

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)

def draw_glow_line(surface, color, start_pos, end_pos, width, glow_radius=10):
    """Vẽ một đường kẻ với hiệu ứng phát sáng neon và lõi trắng cực sắc nét."""
    # Vẽ các lớp phát sáng bên dưới
    for r in range(glow_radius, 0, -2):
        alpha = int(80 * (1 - r / glow_radius))
        glow_color = (*color[:3], alpha)
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.line(s, glow_color, start_pos, end_pos, width + r * 2)
        surface.blit(s, (0, 0))
    
    # Vẽ đường chính ở trên
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    # Thêm LÕI TRẮNG để tạo hiệu ứng ánh sáng mạnh (hiện đại hơn)
    core_w = max(2, width // 3)
    pygame.draw.line(surface, WHITE, start_pos, end_pos, core_w)
    
    # Làm tròn 2 đầu
    pygame.draw.circle(surface, color, (int(start_pos[0]), int(start_pos[1])), width // 2)
    pygame.draw.circle(surface, color, (int(end_pos[0]), int(end_pos[1])), width // 2)
    pygame.draw.circle(surface, WHITE, (int(start_pos[0]), int(start_pos[1])), core_w // 2)
    pygame.draw.circle(surface, WHITE, (int(end_pos[0]), int(end_pos[1])), core_w // 2)

def draw_modern_background(surface):
    """Vẽ nền hiện đại với các chấm chìm mờ ảo."""
    surface.fill(BG_COLOR)
    # Vẽ lưới chấm chìm (grid dots)
    spacing = 40
    for x in range(0, WIDTH, spacing):
        for y in range(0, HEIGHT, spacing):
            # Biến đổi vị trí một chút để trông tự nhiên hơn hoặc giữ nguyên cho gọn gàng
            pygame.draw.circle(surface, (200, 230, 230), (x, y), 2)


def draw_text(surface, text, x, y, font, color=BLACK, align="center"):
    img = font.render(text, True, color)
    if align == "center":
        rect = img.get_rect(center=(x, y))
    elif align == "left":
        rect = img.get_rect(midleft=(x, y))
    else:
        rect = img.get_rect(midright=(x, y))
    surface.blit(img, rect)

def draw_pill_button(surface, text, x, y, w, h, font, is_active=False, is_disabled=False, icon=None, is_hovered=False):
    rect = pygame.Rect(x, y, w, h)
    
    # Determine colors based on state
    if is_disabled:
        bg_color = UI_DISABLED_GRAY
        text_color = WHITE
    elif is_active:
        bg_color = RED
        text_color = WHITE
    else:
        bg_color = CYAN
        text_color = WHITE
        
    # Apply hover brightness
    if is_hovered and not is_disabled:
        bg_color = tuple(min(255, c + 30) for c in bg_color)
        
    pygame.draw.rect(surface, bg_color, rect, border_radius=15)
    
    # Draw icon if any (for Players icons)
    if icon == '1p':
        draw_text(surface, "👤", x + w//2, y + h//2, font, text_color)
    elif icon == '2p':
        draw_text(surface, "👥", x + w//2, y + h//2, font, text_color)
    else:
        draw_text(surface, text, x + w//2, y + h//2, font, text_color)

def draw_logo(surface, x, y, title_font):
    # DOTS & BOXES
    dots_surf = title_font.render("DOTS", True, RED)
    amp_surf = title_font.render("&", True, DARK_TEAL)
    boxes_surf = title_font.render("BOXES", True, RED)
    
    total_w = dots_surf.get_width() + amp_surf.get_width() + boxes_surf.get_width() + 20
    start_x = x - total_w // 2
    
    surface.blit(dots_surf, (start_x, y))
    surface.blit(amp_surf, (start_x + dots_surf.get_width() + 10, y))
    surface.blit(boxes_surf, (start_x + dots_surf.get_width() + amp_surf.get_width() + 20, y))
    
    # Draw the fancy line underneath
    line_y = y + 90
    for i in range(2):
        lx = start_x + i * (total_w // 2 + 10)
        lw = total_w // 2 - 10
        # Line with dots
        pygame.draw.line(surface, DARK_TEAL, (lx, line_y), (lx + lw, line_y), 8)
        for d in range(5):
            dot_x = lx + d * (lw // 4)
            pygame.draw.circle(surface, WHITE, (dot_x, line_y), 6)
            
def draw_speaker(surface, x, y, sound_on, is_hovered=False):
    radius = 33 if is_hovered else 30
    color = tuple(min(255, c + 30) for c in CYAN) if is_hovered else CYAN
    
    pygame.draw.circle(surface, color, (x, y), radius)
    
    # Draw Speaker Body
    s_col = WHITE
    pygame.draw.rect(surface, s_col, (x - 12, y - 6, 8, 12))
    points = [(x - 4, y - 6), (x + 6, y - 14), (x + 6, y + 14), (x - 4, y + 6)]
    pygame.draw.polygon(surface, s_col, points)
    
    if sound_on:
        # Draw sound waves
        for r in range(12, 18, 4):
            pygame.draw.arc(surface, s_col, (x - r, y - r, r*2, r*2), -0.8, 0.8, 2)
    else:
        # Draw Mute X
        pygame.draw.line(surface, s_col, (x + 10, y - 5), (x + 18, y + 5), 2)
        pygame.draw.line(surface, s_col, (x + 18, y - 5), (x + 10, y + 5), 2)

def draw_icon(surface, icon, x, y, center=True):
    rect = icon.get_rect(center=(x, y)) if center else (x, y)
    surface.blit(icon, rect)

def ease_out_quad(t):
    return 1 - (1 - t) * (1 - t)