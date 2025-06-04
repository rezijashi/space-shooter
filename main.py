import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space shooter")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

FONT_PATH = pygame.font.match_font('arial')
FONT_SIZE_LARGE = 64
FONT_SIZE_MEDIUM = 48
FONT_SIZE_SMALL = 24

player_rect = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 60, 50, 50)
player_speed = 5
player_shoot_delay = 300
player_last_shot = pygame.time.get_ticks()
player_lives = 3

enemies = []
bullets = []
explosions = []

def create_enemy():
    enemy_rect = pygame.Rect(random.randrange(0, WIDTH - 40), random.randrange(-100, -40), 40, 40)
    enemy_speed_y = random.randrange(2, 5)
    return {"rect": enemy_rect, "speed_y": enemy_speed_y}

def create_bullet(x, y):
    bullet_rect = pygame.Rect(x - 2, y - 15, 5, 15)
    bullet_speed_y = -10
    return {"rect": bullet_rect, "speed_y": bullet_speed_y}

def create_explosion(center_x, center_y):
    explosion_frames = []
    for i in range(5):
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(surf, YELLOW, (25, 25), 25 - i * 5, 2)
        explosion_frames.append(surf)
    return {"frames": explosion_frames, "current_frame": 0, "rect": explosion_frames[0].get_rect(center=(center_x, center_y)), "last_update": pygame.time.get_ticks(), "frame_rate": 50}

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def game():
    global player_rect, player_last_shot, player_lives, enemies, bullets, explosions

    for i in range(5):
        enemies.append(create_enemy())

    score = 0
    running = True

    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    now = pygame.time.get_ticks()
                    if now - player_last_shot > player_shoot_delay:
                        player_last_shot = now
                        bullets.append(create_bullet(player_rect.centerx, player_rect.top))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed

        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.bottom > HEIGHT:
            player_rect.bottom = HEIGHT
        if player_rect.top < 0:
            player_rect.top = 0

        for bullet in bullets[:]:
            bullet["rect"].y += bullet["speed_y"]
            if bullet["rect"].bottom < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy["rect"].y += enemy["speed_y"]
            if enemy["rect"].top > HEIGHT:
                enemies.remove(enemy)
                enemies.append(create_enemy())

        for explosion in explosions[:]:
            now = pygame.time.get_ticks()
            if now - explosion["last_update"] > explosion["frame_rate"]:
                explosion["last_update"] = now
                explosion["current_frame"] += 1
                if explosion["current_frame"] == len(explosion["frames"]):
                    explosions.remove(explosion)
                else:
                    explosion["image"] = explosion["frames"][explosion["current_frame"]]

        bullets_to_remove = []
        enemies_to_remove = []
        for bullet in bullets:
            for enemy in enemies:
                if bullet["rect"].colliderect(enemy["rect"]):
                    score += 10
                    explosions.append(create_explosion(enemy["rect"].centerx, enemy["rect"].centery))
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    break

        for bullet_to_remove in bullets_to_remove:
            if bullet_to_remove in bullets:
                bullets.remove(bullet_to_remove)
        for enemy_to_remove in enemies_to_remove:
            if enemy_to_remove in enemies:
                enemies.remove(enemy_to_remove)
                enemies.append(create_enemy())

        player_hit = False
        for enemy in enemies[:]:
            if player_rect.colliderect(enemy["rect"]):
                player_hit = True
                enemies.remove(enemy)
                enemies.append(create_enemy())
                break

        if player_hit:
            player_lives -= 1
            if player_lives == 0:
                pygame.quit()
                exit()
            else:
                player_rect.centerx = WIDTH // 2
                player_rect.bottom = HEIGHT - 10

        SCREEN.fill(BLACK)

        for bullet in bullets:
            pygame.draw.rect(SCREEN, GREEN, bullet["rect"])

        for enemy in enemies:
            pygame.draw.circle(SCREEN, RED, enemy["rect"].center, enemy["rect"].width // 2)

        pygame.draw.polygon(SCREEN, BLUE, [(player_rect.centerx, player_rect.top), (player_rect.left, player_rect.bottom), (player_rect.right, player_rect.bottom)])

        for explosion in explosions:
            if "image" in explosion:
                SCREEN.blit(explosion["image"], explosion["rect"])
            else:
                SCREEN.blit(explosion["frames"][explosion["current_frame"]], explosion["rect"])

        draw_text(SCREEN, f"Score: {score}", FONT_SIZE_SMALL, WIDTH // 2, 10)
        draw_text(SCREEN, f"Lives: {player_lives}", FONT_SIZE_SMALL, WIDTH - 70, 10)

        pygame.display.flip()

clock = pygame.time.Clock()

game()

pygame.quit()
