import os
import random
import pygame

# --- Constantes (Aprox. 20 linhas) ---
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
FPS = 60
PLAYER_SPEED, ENEMY_SPEED, MISSILE_SPEED, BG_SCROLL_SPEED = 5, 3, 10, 0.8
PLAYER_SIZE, ENEMY_SIZE, MISSILE_SIZE, EXPLOSION_SIZE = (50, 50), (50, 50), (25, 25), (60, 60)
EXPLOSION_DUR_FRAMES, GAME_OVER_DUR_MS = 20, 3000
POINTS_PER_ENEMY = 10
WHITE, BLACK, RED, GREEN = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0)

# --- Inicialização (Aprox. 7 linhas) ---
pygame.init()
try: # Inicializa o mixer para sons
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Mixer de áudio inicializado.")
except pygame.error as e: print(f"Erro ao inicializar mixer: {e}. Sons desativados."); pygame.mixer = None # Desativa sons se falhar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo Condensado com Som")
clock = pygame.time.Clock()
font_menu = pygame.font.SysFont("Arial", 48, True)
font_score = pygame.font.SysFont("Arial", 30, True)
font_game_over = pygame.font.SysFont("Arial", 90, True)

# --- Carregamento de Assets (Imagens + Sons) (Aprox. 25 linhas) ---
def load_asset(asset_type, name, size=None, rotate=None):
    folder = 'images' if asset_type == 'img' else 'sounds'
    path = os.path.join(os.path.dirname(__file__), folder, name)
    try:
        if asset_type == 'img':
            asset = pygame.image.load(path).convert_alpha()
            if size: asset = pygame.transform.scale(asset, size)
            if rotate: asset = pygame.transform.rotate(asset, rotate)
        elif asset_type == 'sound' and pygame.mixer: # Só carrega som se o mixer iniciou
             asset = pygame.mixer.Sound(path)
        elif asset_type == 'music' and pygame.mixer:
            pygame.mixer.music.load(path) # Música é carregada separadamente
            asset = True # Indica sucesso
        else: asset = None # Som desativado ou tipo inválido
        print(f"Carregado [{asset_type}]: {name}")
        return asset
    except (FileNotFoundError, pygame.error) as e:
        print(f"Erro ao carregar [{asset_type}] {name}: {e}. Saindo.")
        pygame.quit(); exit()

bg_img = pygame.transform.scale(load_asset('img', 'Background1.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
enemy_img = load_asset('img', 'NavaRedonda1.png', size=ENEMY_SIZE)
player_img = load_asset('img', 'NavaCombate1.png', size=PLAYER_SIZE, rotate=-45)
missile_img = load_asset('img', 'Missil1.png', size=MISSILE_SIZE, rotate=-90)
explosion_img = load_asset('img', 'explosao1.png', size=EXPLOSION_SIZE)

# Carregar sons (se o mixer estiver ativo)
shoot_sound = load_asset('sound', 'laser_shoot.mp3')
explosion_sound = load_asset('sound', 'explosion.mp3')
game_over_sound = load_asset('sound', 'game_over.mp3')
music_loaded = load_asset('music', 'background_music.mp3') # Carrega música de fundo

if music_loaded and pygame.mixer: pygame.mixer.music.set_volume(0.4) # Ajusta volume da música

# --- Estado Global (Aprox. 5 linhas) ---
game_state = 'MENU' # 'MENU', 'PLAYING', 'GAME_OVER'
running = True
game_over_start_time = 0
score = 0

# --- Variáveis de Jogo (Aprox. 10 linhas) ---
player_rect = player_img.get_rect(topleft=(100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2))
enemy_rect = enemy_img.get_rect(topleft=(SCREEN_WIDTH + 50, random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])))
missile_rect = missile_img.get_rect(center=player_rect.center)
enemy_active = True
missile_fired = False
exploding = False
explosion_timer = 0
bg_scroll_x = 0

# --- Função para tocar som com segurança ---
def play_sound(sound_obj):
    if sound_obj and pygame.mixer: # Verifica se o som foi carregado e o mixer está ativo
        sound_obj.play()

# --- Loop Principal (Restante das linhas, aprox. 150) ---
while running:
    dt = clock.tick(FPS) / 1000.0
    events = pygame.event.get()
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    for event in events:
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False

    # --- Estado: MENU ---
    if game_state == 'MENU':
        start_surf = font_menu.render("Start Game", True, GREEN if 'start_rect' in locals() and start_rect.collidepoint(mouse_pos) else WHITE)
        start_rect = start_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        quit_surf = font_menu.render("Quit", True, RED if 'quit_rect' in locals() and quit_rect.collidepoint(mouse_pos) else WHITE)
        quit_rect = quit_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))

        for event in events:
            is_starting = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: is_starting = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos): is_starting = True
                elif quit_rect.collidepoint(event.pos): running = False
            
            if is_starting:
                game_state = 'PLAYING'
                # Resetar estado do jogo
                player_rect.topleft = (100, SCREEN_HEIGHT // 2 - PLAYER_SIZE[1] // 2)
                enemy_rect.topleft = (SCREEN_WIDTH + random.randint(50,200), random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1]))
                enemy_active = True; missile_fired = False; score = 0; exploding = False; bg_scroll_x = 0
                if music_loaded and pygame.mixer: pygame.mixer.music.play(-1) # Toca música em loop
                print("Iniciando jogo...")

        screen.blit(bg_img, (0, 0))
        screen.blit(start_surf, start_rect)
        screen.blit(quit_surf, quit_rect)

    # --- Estado: PLAYING ---
    elif game_state == 'PLAYING':
        # Input Jogador
        if keys[pygame.K_UP] and player_rect.top > 0: player_rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player_rect.bottom < SCREEN_HEIGHT: player_rect.y += PLAYER_SPEED
        if keys[pygame.K_SPACE] and not missile_fired:
            missile_fired = True
            missile_rect.center = player_rect.center
            missile_rect.x += PLAYER_SIZE[0] // 2 - 10
            play_sound(shoot_sound) # <<< TOCAR SOM TIRO >>>

        # Movimento e Lógica
        bg_scroll_x = (bg_scroll_x - BG_SCROLL_SPEED) % -SCREEN_WIDTH
        if enemy_active: enemy_rect.x -= ENEMY_SPEED
        if missile_fired: missile_rect.x += MISSILE_SPEED
        else: missile_rect.center = player_rect.center

        # Colisões
        if enemy_active and player_rect.colliderect(enemy_rect):
            print("Game Over - Colisão Jogador!")
            play_sound(game_over_sound) # <<< TOCAR SOM GAME OVER >>>
            if pygame.mixer: pygame.mixer.music.stop() # Para música
            game_state = 'GAME_OVER'
            game_over_start_time = pygame.time.get_ticks()
        elif missile_fired and enemy_active and missile_rect.colliderect(enemy_rect):
            print("Inimigo Atingido!")
            play_sound(explosion_sound) # <<< TOCAR SOM EXPLOSÃO >>>
            score += POINTS_PER_ENEMY
            enemy_active = False
            missile_fired = False
            exploding = True
            explosion_rect = explosion_img.get_rect(center=enemy_rect.center)
            explosion_timer = 0

        # Respawn / Reset
        if enemy_active and enemy_rect.right < 0:
            enemy_rect.left = SCREEN_WIDTH + random.randint(50, 150); enemy_rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])
        if missile_fired and missile_rect.left > SCREEN_WIDTH: missile_fired = False

        # Lógica da Explosão
        if exploding:
            explosion_timer += 1
            if explosion_timer >= EXPLOSION_DUR_FRAMES:
                exploding = False
                enemy_rect.left = SCREEN_WIDTH + random.randint(50, 150); enemy_rect.y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE[1])
                enemy_active = True

        # Desenho
        if game_state == 'PLAYING': # Só desenha se ainda estiver jogando
            screen.blit(bg_img, (bg_scroll_x, 0)); screen.blit(bg_img, (bg_scroll_x + SCREEN_WIDTH, 0))
            screen.blit(player_img, player_rect)
            if enemy_active: screen.blit(enemy_img, enemy_rect)
            if missile_fired: screen.blit(missile_img, missile_rect)
            if exploding: screen.blit(explosion_img, explosion_rect)
            score_surf = font_score.render(f"Pontos: {score}", True, WHITE); screen.blit(score_surf, (10, 10))

    # --- Estado: GAME_OVER ---
    elif game_state == 'GAME_OVER':
        if pygame.time.get_ticks() - game_over_start_time >= GAME_OVER_DUR_MS:
            game_state = 'MENU'

        # Desenho
        screen.blit(bg_img, (0,0))
        go_surf = font_game_over.render("GAME OVER", True, RED)
        go_rect = go_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(go_surf, go_rect)

    pygame.display.flip()

# --- Fim ---
if pygame.mixer: pygame.mixer.music.stop() # Garante que a música pare ao fechar
pygame.quit()
print("Jogo finalizado.")