import pygame
import math
import time

# Inicialização
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Configurações do quadrado
squareSize = 32
velocity = 5
heart = pygame.image.load("images/heart32x.png")
heart = heart.convert()
x, y = 50, 50
width, height = screen.get_size()

font = pygame.font.Font(None, 40)

level = 1
maxlevel = 100 # placeholder

newlevel = False

platformsize = squareSize
platformx, platformy = 200, 200
platform = pygame.Surface([platformsize, platformsize])
platform.fill((128, 128, 128))

bonessize = squareSize
bonesx, bonesy = 300, 300
bones = pygame.image.load("images/bone.png")




sound1 = pygame.mixer.Sound('sounds/death1.wav')
sound2 = pygame.mixer.Sound('sounds/death2.wav')

#
soundnewlevel1 = pygame.mixer.Sound('sounds/newlevel1.wav')
soundnewlevel2 = pygame.mixer.Sound('sounds/newlevel2.wav')



# Função para limitar a posição dentro da tela
def limitar_posicao(quadradox, quadradoy):
    quadradox = max(0, min(width - squareSize, quadradox))
    quadradoy = max(0, min(height - squareSize, quadradoy))
    return quadradox, quadradoy

# Função para calcular movimento diagonal
def movimento_diagonal(teclas):
    return velocity * (math.sqrt(2) / 2) if teclas else 0

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    # if newlevel:
    #     overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    #     overlay.fill((255, 0, 0, 128))  # RGBA: vermelho com 50% de transparência
    #     pygame.display.flip()
    #     soundnewlevel1.play()
    #     time.sleep(1)
    #     surface_level = font.render(f"Nível: {level}", True, 'white')
    #     surface_maxlevel = font.render(f"Recorde: {maxlevel}", True, 'white')
    #     text_render_x = (width // 2) - surface_level.get_width() // 2
    #     text_render_y = (height // 2) - surface_level.get_height() // 2
    #     screen.blit(surface_level, (text_render_x - 30, text_render_y - 17))
    #     screen.blit(surface_maxlevel, (text_render_x - 30, text_render_y + 17))
    #     pygame.display.flip()
    #     soundnewlevel2.play()
    #     time.sleep(1)
    #     soundnewlevel1.play()
    #     newlevel = False



    keys = pygame.key.get_pressed()
    dx = dy = 0

    # Movimentação
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        dy -= velocity
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dy += velocity
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx -= velocity
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx += velocity

    # Ajuste para movimento diagonal
    if dx != 0 and dy != 0:
        dx = movimento_diagonal(True) * (1 if dx > 0 else -1)
        dy = movimento_diagonal(True) * (1 if dy > 0 else -1)

    # Atualização da posição proposta
    new_x = x + dx
    new_y = y + dy

    # Criar retângulos para detecção de colisão
    heart_rect = pygame.Rect(new_x, y, squareSize, squareSize)
    platform_rect = pygame.Rect(platformx, platformy, platformsize, platformsize)
    bones_rect = pygame.Rect(bonesx, bonesy, 6, 1000)

    # Verificar colisão no eixo X
    if heart_rect.colliderect(platform_rect):
        if dx > 0:  # Movendo para a direita
            new_x = platform_rect.left - squareSize
        elif dx < 0:  # Movendo para a esquerda
            new_x = platform_rect.right

    # Atualizar o retângulo temporário após ajuste no X
    heart_rect = pygame.Rect(x, new_y, squareSize, squareSize)

    # Verificar colisão no eixo Y
    if heart_rect.colliderect(platform_rect):
        if dy > 0:  # Movendo para baixo
            new_y = platform_rect.top - squareSize
        elif dy < 0:  # Movendo para cima
            new_y = platform_rect.bottom

    # Atualizar a posição final após colisão
    x, y = limitar_posicao(new_x, new_y)

    # Renderização
    screen.fill((0, 0, 0))
    screen.blit(heart, (x, y))
    screen.blit(bones, (bonesx, bonesy))
    screen.blit(platform, (platformx, platformy))

    if heart_rect.colliderect(bones_rect):
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, 128))  # RGBA: vermelho com 50% de transparência
        pygame.display.flip()
        soundnewlevel1.play()
        time.sleep(1)
        surface_level = font.render(f"Nível: {level}", True, 'white')
        surface_maxlevel = font.render(f"Recorde: {maxlevel}", True, 'white')
        text_render_x = (width // 2) - surface_level.get_width() // 2
        text_render_y = (height // 2) - surface_level.get_height() // 2
        screen.blit(surface_level, (text_render_x - 30, text_render_y - 17))
        screen.blit(surface_maxlevel, (text_render_x - 30, text_render_y + 17))
        pygame.display.flip()
        soundnewlevel2.play()
        time.sleep(1)
        soundnewlevel1.play()
        newlevel = False
        heart = pygame.image.load("images/heart64x.png")
        screen.fill((0, 0, 0))
        offset = 16  # Valor do offset em pixels
        screen.blit(heart, (x - offset, y - offset))
        sound1.play()
        pygame.display.flip()
        time.sleep(1)
        heart = pygame.image.load("images/heartdead64x.png")
        screen.fill((0, 0, 0))
        screen.blit(heart, (x - offset, y - offset))
        sound2.play()
        pygame.display.flip()
        time.sleep(1)
        exit()




    pygame.display.flip()
    clock.tick(60)