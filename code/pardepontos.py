import pygame
import random
import math
import sys
import time

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Par de Pontos Mais Próximos')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

FONT = pygame.font.SysFont(None, 36)

division_lines = []

def generate_random_points(num_points):
    return [(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(num_points)]

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def draw_scene(points, highlight_pairs=None, strip=None):
    SCREEN.fill(WHITE)
    
    for line in division_lines:
        pygame.draw.line(SCREEN, BLUE, (line, 0), (line, SCREEN_HEIGHT), 2)
    
    for point in points:
        pygame.draw.circle(SCREEN, BLACK, point, 5)
    
    if highlight_pairs:
        for p1, p2 in highlight_pairs:
            pygame.draw.line(SCREEN, RED, p1, p2, 2)
            pygame.draw.circle(SCREEN, RED, p1, 7)
            pygame.draw.circle(SCREEN, RED, p2, 7)
    

    if strip:
        for point in strip:
            pygame.draw.circle(SCREEN, YELLOW, point, 7)
    
    pygame.display.flip()
    pygame.time.delay(500)  # Aguarda 500ms entre cada passo

def brute_force_step_by_step(points):
    min_dist = float('inf')
    p1, p2 = None, None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            draw_scene(points, highlight_pairs=[(points[i], points[j])])
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = points[i], points[j]
    draw_scene(points, highlight_pairs=[(p1, p2)])
    return p1, p2, min_dist

def closest_in_strip_step_by_step(strip, d):
    min_dist = d
    p1, p2 = None, None
    strip.sort(key=lambda point: point[1])
    for i in range(len(strip)):
        for j in range(i + 1, len(strip)):
            if (strip[j][1] - strip[i][1]) >= min_dist:
                break
            draw_scene(strip, highlight_pairs=[(strip[i], strip[j])])
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = strip[i], strip[j]
    return p1, p2, min_dist

def closest_pair_dc_step_by_step(points_sorted_x):
    if len(points_sorted_x) <= 3:
        return brute_force_step_by_step(points_sorted_x)
    
    mid = len(points_sorted_x) // 2
    midpoint = points_sorted_x[mid][0]
    division_lines.append(midpoint) 
    
    left_half = points_sorted_x[:mid]
    right_half = points_sorted_x[mid:]
    
    
    draw_scene(points_sorted_x)
    
    p1_left, p2_left, dist_left = closest_pair_dc_step_by_step(left_half)
    p1_right, p2_right, dist_right = closest_pair_dc_step_by_step(right_half)
    
    if dist_left < dist_right:
        d = dist_left
        p1, p2 = p1_left, p2_left
    else:
        d = dist_right
        p1, p2 = p1_right, p2_right
    
    strip = [p for p in points_sorted_x if abs(p[0] - midpoint) < d]
    draw_scene(points_sorted_x, strip=strip) 
    
    p1_strip, p2_strip, dist_strip = closest_in_strip_step_by_step(strip, d)
    
    if dist_strip < d:
        return p1_strip, p2_strip, dist_strip
    return p1, p2, d


def show_message(message):
    text = FONT.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.flip()
    wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def reset_game():
    global division_lines
    division_lines = []

# Função principal
def main():
    NUM_POINTS = 20
    points = generate_random_points(NUM_POINTS)
    points_sorted_x = sorted(points, key=lambda point: point[0])
    
    global division_lines
    division_lines = []  # Reseta as linhas de divisão
    
    draw_scene(points)
    show_message("Pressione 'B' para Força Bruta, 'D' para Divisão e Conquista")
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    p1, p2, min_dist = brute_force_step_by_step(points)
                    draw_scene(points, highlight_pairs=[(p1, p2)])
                    show_message(f"Força Bruta Finalizada! Distância: {min_dist:.2f}")
                if event.key == pygame.K_d:
                    p1, p2, min_dist = closest_pair_dc_step_by_step(points_sorted_x)
                    draw_scene(points, highlight_pairs=[(p1, p2)])
                    show_message(f"Divisão e Conquista Finalizada! Distância: {min_dist:.2f}")
                if event.key == pygame.K_r:
                    reset_game()  # Apenas limpa as linhas de divisão
                    draw_scene(points)  # Mantém os pontos visíveis
                    show_message("Jogo reiniciado! Pressione 'B' ou 'D' para continuar")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Executa o programa
if __name__ == "__main__":
    main()
