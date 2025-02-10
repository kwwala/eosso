import pygame
import math
import time

# básico pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
width, height = screen.get_size()

# coisas úteis
font = pygame.font.Font(None, 40)

# jogador/coração
heart = pygame.image.load("images/heart32x.png")
heart = heart.convert()
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
bonex, boney = width, 300
bone = pygame.image.load("images/bone.png")

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

borders.blit(borderleft, (8, 8))
borders.blit(borderright, (width - 16, 8))
borders.blit(borderup, (8, 8))
borders.blit(borderdown, (8, height - 16))

# sons
sound1 = pygame.mixer.Sound('sounds/death1.wav')
sound2 = pygame.mixer.Sound('sounds/death2.wav')
sound3 = pygame.mixer.Sound('sounds/death3.wav')
soundnewlevel1 = pygame.mixer.Sound('sounds/newlevel1.wav')
soundnewlevel2 = pygame.mixer.Sound('sounds/newlevel2.wav')

def limitposition(x, y):
    x = max(16, min(width - (squareSize + 16), x))
    y = max(16, min(height - (squareSize + 16), y))
    return x, y

# Função para calcular movimento diagonal
def diagonalmovement(keys):
    return velocity * (math.sqrt(2) / 2) if keys else 0

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    dx = dy = 0

    if newlevel:
        # placeholder pra o novo level
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # RGBA: vermelho com 50% de transparência
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        soundnewlevel1.play()
        time.sleep(1)
        surface_level = font.render(f"Nível: {level: .0f}", True, 'white')
        surface_maxlevel = font.render(f"Recorde: {maxlevel: .0f}", True, 'white')
        text_render_x = (width // 2) - surface_level.get_width() // 2
        text_render_y = (height // 2) - surface_level.get_height() // 2
        screen.blit(surface_level, (text_render_x - 30, text_render_y - 17))
        screen.blit(surface_maxlevel, (text_render_x - 30, text_render_y + 17))
        pygame.display.flip()
        soundnewlevel2.play()
        time.sleep(1)
        soundnewlevel1.play()
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

    if level == 1:
        bonex -= 2
        if bonex <= -8:
            level += .5
    elif level == 1.5:
        bonex = width
        level += .5
        newlevel = True
    elif level == 2:
        bonex -= 4
        if bonex <= -8:
            level += .5
    elif level == 2.5:
        bonex = width
        level += .5
        newlevel = True
    elif level == 3:
        exit()
    else:
        print('algo aconteceu') # vai que eu mecho e acabo bugando algo e pulando
        exit()

    
    # Criar retângulos para detecção de colisão
    heart_rect = pygame.Rect(new_x, y, squareSize, squareSize)
    platform_rect = pygame.Rect(blockx, blocky, blocksize, blocksize)
    bones_rect = pygame.Rect(bonex, boney, 6, 1000)

    # Verificar colisão no eixo X
    if heart_rect.colliderect(platform_rect):
        if dx > 0:  # Movendo para a direita
            new_x = platform_rect.left - squareSize
        elif dx < 0:  # Movendo para a esquerda
            new_x = platform_rect.right

    # Atualizar o retângulo temporário após ajuste no X
    heart_rect = pygame.Rect(x, new_y, squareSize, squareSize)

    # Atualizar a posição final após colisão
    x, y = limitposition(new_x, new_y)

    # Renderização
    screen.fill((0, 0, 0))
    screen.blit(platform, (platformx, platformy))
    screen.blit(heart, (x, y))
    
    screen.blit(block, (blockx, blocky))
    screen.blit(bone, (bonex, boney))
    screen.blit(borders, (0, 0))

    if heart_rect.colliderect(bones_rect):
        # animação de morte real
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
        screen.fill((0, 0, 0)) # ir pro menu do jogo
        pygame.display.flip()
        sound3.play()
        time.sleep(1)
        exit()

    pygame.display.flip()
    clock.tick(60)