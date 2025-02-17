import pygame
import math
import time

# básico pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("É Osso")
icon = pygame.image.load("images/shadedicon.png").convert_alpha()
pygame.display.set_icon(icon)

# coisas úteis
font = pygame.font.Font(None, 40)
width, height = screen.get_size()

# jogador/coração
heart = pygame.image.load("images/heart32x.png").convert_alpha()
x, y = (width / 2) - 32, (height / 2) - 32
squareSize = 32
velocity = 5

# níveis
level = 1
maxlevel = 100 # placeholder
newlevel = True

# plataforma
blocksize = squareSize
blockx, blocky = 200, 200
block = pygame.Surface([blocksize, blocksize])
block.fill((128, 128, 128))

# plataforma
platformsize = squareSize
platformx, platformy = 400, 200
platform = pygame.Surface([platformsize, platformsize / 4])
platform.fill((196, 196, 196))

# ossos
bonesize = squareSize
bonex, boney = width, 256
bone = pygame.image.load("images/bone.png")

flippedbonex, flippedboney = width, -128
flippedbone = pygame.transform.flip(bone, False, True) 

# bordas
borders = pygame.Surface((width, height), pygame.SRCALPHA)

borderleft = pygame.Surface([8, height - 16])
borderleft.fill((255, 255, 255))

borderright = pygame.Surface([8, height - 16])
borderright.fill((255, 255, 255))

borderup = pygame.Surface([width - 16, 8])
borderup.fill((255, 255, 255))

borderdown = pygame.Surface([width - 16, 8])
borderdown.fill((255, 255, 255))

blackborderleft = pygame.Surface([8, height])
blackborderleft.fill((0, 0, 0))

blackborderright = pygame.Surface([8, height])
blackborderright.fill((0, 0, 0))

blackborderup = pygame.Surface([width, 8])
blackborderup.fill((0, 0, 0))

blackborderdown = pygame.Surface([width, 8])
blackborderdown.fill((0, 0, 0))

borders.blit(borderleft, (8, 8))
borders.blit(borderright, (width - 16, 8))
borders.blit(borderup, (8, 8))
borders.blit(borderdown, (8, height - 16))

borders.blit(blackborderleft, (0, 0))
borders.blit(blackborderright, (width - 8, 8))
borders.blit(blackborderup, (0, 0))
borders.blit(blackborderdown, (0, height - 8))

# sons
sound1 = pygame.mixer.Sound('sounds/death1.wav')
sound2 = pygame.mixer.Sound('sounds/death2.wav')
sound3 = pygame.mixer.Sound('sounds/death3.wav')
soundnewlevel1 = pygame.mixer.Sound('sounds/newlevel1.wav')
soundnewlevel2 = pygame.mixer.Sound('sounds/newlevel2.wav')
pygame.mixer.music.load("sounds/sans.ogg")

rect_x, rect_y, rect_width, rect_height = 200, 200, 100, 100

def limitposition(x, y):
    x = max(16, min(width - (squareSize + 16), x))
    y = max(16, min(height - (squareSize + 16), y))
    return x, y

# Função para calcular movimento diagonal
def diagonalmovement(keys):
    return velocity * (math.sqrt(2) / 2) if keys else 0

offset = 16


# Variáveis de controle do tempo
start_time = pygame.time.get_ticks()
display_stage = 0
offset = 16
start_time = pygame.time.get_ticks()
show_overlay = True
overlay_displayed = False
wait_time = 1000

def deathscreen():
    global start_time, display_stage
    heart = pygame.image.load("images/heart64x.png")
    heart_dead = pygame.image.load("images/heartdead64x.png")
    font = pygame.font.Font(None, 36)
    offset = 16

    screen.fill((0, 0, 0))
    pygame.mixer.music.stop()
    screen.blit(heart, (x - offset, y - offset))
    sound1.play()
    pygame.display.flip()
    pygame.time.delay(1000)
    screen.fill((0, 0, 0))
    screen.blit(heart_dead, (x - offset, y - offset))
    sound2.play()
    pygame.display.flip()
    pygame.time.delay(1000)
    screen.fill((0, 0, 0))
    sound3.play()
    pygame.display.flip()
    pygame.time.delay(1000)
    surface_youdied = font.render(f"Você morreu.", True, 'white')
    surface_levelreached = font.render(f"Você chegou no nível {level: .0f}.", True, 'white')
    surface_maxlevelreached = font.render(f"Seu recorde é o nível {maxlevel: .0f}.", True, 'white')
    screen.blit(surface_youdied, (width / 4, (width / 2) - 50))
    screen.blit(surface_levelreached, (width / 4, (width / 2) - 25))
    screen.blit(surface_maxlevelreached, (width / 4, (width / 2)))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                exit()
                break
            pygame.display.flip()
            clock.tick(60)

import pygame

def newlevel():
    pygame.mixer.music.pause()
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # RGBA: vermelho com 50% de transparência
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    soundnewlevel1.play()
    pygame.time.delay(1000)

    surface_level = font.render(f"Nível: {level: .0f}", True, 'white')
    surface_maxlevel = font.render(f"Recorde: {maxlevel: .0f}", True, 'white')
    text_render_x = (width // 2) - surface_level.get_width() // 2
    text_render_y = (height // 2) - surface_level.get_height() // 2
    screen.blit(surface_level, ((width // 2) - surface_level.get_width() // 2, text_render_y - 17))
    screen.blit(surface_maxlevel, ((width // 2) - surface_level.get_width() // 2, text_render_y + 17))
    pygame.display.flip()
    soundnewlevel2.play()
    pygame.time.delay(1000)

    soundnewlevel1.play()
    pygame.mixer.music.unpause()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    dx = dy = 0

    

    if newlevel:
        if level == 1:
            pygame.mixer.music.play()
        newlevel()
        newlevel = False
        

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
        dx = diagonalmovement(True) * (1 if dx > 0 else -1)
        dy = diagonalmovement(True) * (1 if dy > 0 else -1)

    # Atualização da posição proposta
    new_x = x + dx
    new_y = y + dy

    # níveis
    if level == 1:
        bonex -= 2
        if bonex <= -16:
            level += 1
            bonex = width
            level += 1
            newlevel = True
    elif level == 2:
        bonex -= 4
        if bonex <= -16:
            bonex = width
            level += 1
            newlevel = True
    elif level == 3:
        bonex -= 4
        flippedbonex -= 4
        if bonex <= -16:
            level += 1
            bonex = width
            flippedbonex = width
            newlevel = True
            bonedirection = -1  # 1 para subir, -1 para descer
    elif level == 4:
        bonex -= 4
        flippedbonex -= 4

        if boney >= 320:
            bonedirection = -1
        elif boney <= 250:
            bonedirection = 1

        boney += bonedirection
        flippedboney += bonedirection

        if bonex <= -16:
            level += 1
            bonex = width
            flippedbonex = width
            newlevel = True
            bonedirection = -1  # 1 para subir, -1 para descer
    else:
        print('algo aconteceu') # vai que eu mecho e acabo bugando algo e pulando
        exit()

    # rects
    heart_rect = pygame.Rect(new_x, y, squareSize, squareSize)
    bones_rect = pygame.Rect(bonex + 4, boney, 24, 320)
    flippedbone_rect = pygame.Rect(flippedbonex + 4, flippedboney, 24, 320)
    # platform_rect = pygame.Rect(blockx, blocky, blocksize, blocksize)

    # colisão com plataforma
    # if heart_rect.colliderect(platform_rect):
    #     if dx > 0:  # Movendo para a direita
    #         new_x = platform_rect.left - squareSize
    #     elif dx < 0:  # Movendo para a esquerda
    #         new_x = platform_rect.right

    # atualizar o retângulo temporário
    heart_rect = pygame.Rect(x, new_y, squareSize, squareSize)
    
    # atualizar a posição final após colisão
    x, y = limitposition(new_x, new_y)

    # renderização (blit)
    screen.fill((0, 0, 0))
    # screen.blit(platform, (platformx, platformy))
    # screen.blit(block, (blockx, blocky))
    screen.blit(heart, (x, y))
    screen.blit(bone, (bonex, boney))
    screen.blit(flippedbone, (flippedbonex, flippedboney))
    
    screen.blit(borders, (0, 0))

    # morte
    if heart_rect.colliderect(bones_rect) or heart_rect.colliderect(flippedbone_rect): 
        
        deathscreen()

    pygame.display.flip()
    clock.tick(60)