import os
import random
import pygame

# --- Constantes (Aprox. 20 linhas) ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
PLAYER_SPEED, ENEMY_SPEED, MISSILE_SPEED, BG_SCROLL_SPEED = 5, 3, 10, 0.8
PLAYER_SIZE, ENEMY_SIZE, MISSILE_SIZE, EXPLOSION_SIZE = (50, 50), (50, 50), (25, 25), (60, 60)
EXPLOSION_DUR_FRAMES, GAME_OVER_DUR_MS = 20, 3000 # Reduzido para 3s para teste
POINTS_PER_ENEMY = 10
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)

# --- Inicialização (Aprox. 5 linhas) ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Combate Espacial")
clock = pygame.time.Clock()
font_menu = pygame.font.SysFont("Arial", 48, True)
font_score = pygame.font.SysFont("Arial", 30, True)
font_game_over = pygame.font.SysFont("Arial", 90, True)

# --- Carregamento de Assets (Aprox. 15 linhas) ---
def load_img(name, size=None, rotate=None):
    path = os.path.join(os.path.dirname(__file__), 'images', name)
    try:
        img = pygame.image.load(path).convert_alpha()
        if size: img = pygame.transform.scale(img, size)
        if rotate: img = pygame.transform.rotate(img, rotate)
        return img
    except FileNotFoundError: print(f"Erro: Imagem não encontrada: {path}"); pygame.quit(); exit()
    except pygame.error as e: print(f"Erro Pygame: {e}"); pygame.quit(); exit()

bg_img = pygame.transform.scale(load_img('Background1.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
enemy_img = load_img('NavaRedonda1.png', size=ENEMY_SIZE)
player_img = load_img('NavaCombate1.png', size=PLAYER_SIZE, rotate=-45)
missile_img = load_img('Missil1.png', size=MISSILE_SIZE, rotate=-90)
explosion_img = load_img('explosao1.png', size=EXPLOSION_SIZE)

# --- Estado Global (Aprox. 5 linhas) ---
game_state = 'MENU' # 'MENU', 'PLAYING', 'GAME_OVER'
running = True
game_over_start_time = 0
score = 0

# --- Variáveis de Jogo (serão resetadas implicitamente ou no início de 'PLAYING') (Aprox. 10 linhas) ---
player_rect = player_img.get_rect(topleft=(100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2))
enemy_rect = enemy_img.get_rect(topleft=(SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])))
missile_rect = missile_img.get_rect(center=player_rect.center) # Pos inicial, será ajustada
enemy_active = True
missile_fired = False
exploding = False
explosion_timer = 0
bg_scroll_x = 0
# Botão rects são locais para o estado do menu

# --- Loop Principal (Restante das linhas, aprox. 145) ---
while running:
    dt = clock.tick(FPS) / 1000.0
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False # Esc sempre sai

    # --- Estado: MENU ---
    if game_state == 'MENU':
        start_surf = font_menu.render("Start Game", True, GREEN if 'start_rect' in locals() and start_rect.collidepoint(mouse_pos) else WHITE)
        start_rect = start_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        quit_surf = font_menu.render("Quit", True, RED if 'quit_rect' in locals() and quit_rect.collidepoint(mouse_pos) else WHITE)
        quit_rect = quit_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = 'PLAYING'
                # Resetar estado do jogo ao iniciar
                player_rect.topleft = (100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2)
                enemy_rect.topleft = (SCREEN_WIDTH + random.randint(50,200), random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1]))
                enemy_active = True
                missile_fired = False
                score = 0
                exploding = False
                bg_scroll_x = 0
                print("Iniciando jogo...")
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    game_state = 'PLAYING'
                    # Resetar estado do jogo ao iniciar (igual ao Keydown)
                    player_rect.topleft = (100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2)
                    enemy_rect.topleft = (SCREEN_WIDTH + random.randint(50,200), random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1]))
                    enemy_active = True
                    missile_fired = False
                    score = 0
                    exploding = False
                    bg_scroll_x = 0
                    print("Iniciando jogo...")
                elif quit_rect.collidepoint(event.pos): running = False

        screen.blit(bg_img, (0, 0))
        screen.blit(start_surf, start_rect)
        screen.blit(quit_surf, quit_rect)

    # --- Estado: PLAYING ---
    elif game_state == 'PLAYING':
        # Eventos específicos do jogo (nenhum extra por enquanto)
        # Input do Jogador
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT: player_rect.y += PLAYER_SPEED
        if keys[pygame.K_SPACE] and not missile_fired:
            missile_fired = True
            missile_rect.center = player_rect.center
            missile_rect.x += PLAYER_SIZE[0] // 2 - 10 # Ajuste inicial

        # Movimento e Lógica
        bg_scroll_x = (bg_scroll_x - BG_SCROLL_SPEED) % -SCREEN_WIDTH # Scroll contínuo
        if enemy_active: enemy_rect.x -= ENEMY_SPEED
        if missile_fired: missile_rect.x += MISSILE_SPEED
        else: missile_rect.center = player_rect.center # Segue o jogador se não disparado

        # Colisões
        collision_occurred = False
        if enemy_active and player_rect.colliderect(enemy_rect):
            print("Game Over - Colisão Jogador!")
            game_state = 'GAME_OVER'
            game_over_start_time = pygame.time.get_ticks()
            collision_occurred = True
            # Som de game over aqui?
        elif missile_fired and enemy_active and missile_rect.colliderect(enemy_rect):
            print("Inimigo Atingido!")
            score += POINTS_PER_ENEMY
            enemy_active = False
            missile_fired = False
            exploding = True
            explosion_rect = explosion_img.get_rect(center=enemy_rect.center)
            explosion_timer = 0
            collision_occurred = True
            # Som de explosão aqui?

        # Respawn / Reset
        if enemy_active and enemy_rect.right < 0: # Inimigo saiu
            enemy_rect.left = SCREEN_WIDTH + random.randint(50, 150)
            enemy_rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])
        if missile_fired and missile_rect.left > SCREEN_WIDTH: # Míssil saiu
            missile_fired = False

        # Lógica da Explosão
        if exploding:
            explosion_timer += 1
            if explosion_timer >= EXPLOSION_DUR_FRAMES:
                exploding = False
                # Respawn do inimigo após explosão
                enemy_rect.left = SCREEN_WIDTH + random.randint(50, 150)
                enemy_rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])
                enemy_active = True

        # Desenho (só desenha se o estado não mudou para GAME_OVER neste frame)
        if game_state == 'PLAYING':
            screen.blit(bg_img, (bg_scroll_x, 0))
            screen.blit(bg_img, (bg_scroll_x + SCREEN_WIDTH, 0))
            screen.blit(player_img, player_rect)
            if enemy_active: screen.blit(enemy_img, enemy_rect)
            if missile_fired: screen.blit(missile_img, missile_rect)
            if exploding: screen.blit(explosion_img, explosion_rect)
            score_surf = font_score.render(f"Pontos: {score}", True, WHITE)
            screen.blit(score_surf, (10, 10))

    # --- Estado: GAME_OVER ---
    elif game_state == 'GAME_OVER':
        if pygame.time.get_ticks() - game_over_start_time >= GAME_OVER_DUR_MS:
            game_state = 'MENU' # Volta para o menu

        # Desenho
        screen.blit(bg_img, (0,0)) # Pode usar um fundo preto ou o do jogo
        go_surf = font_game_over.render("GAME OVER", True, RED)
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(go_surf, go_rect)

    pygame.display.flip()

# --- Fim ---
pygame.quit()
print("Jogo finalizado.")