import pygame
import math
import time
import os

# básico pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.display.set_caption("É Osso")
icon = pygame.image.load("images/shadedicon.png").convert_alpha()
pygame.display.set_icon(icon)

# coisas úteis
font_path = os.path.join(os.path.dirname(__file__), "fonts", "minecraftia.ttf")
font = pygame.font.Font(font_path, 24)
print(font_path)
width, height = screen.get_size()

# níveis
level = 1
maxlevel = 3 # placeholder
newlevel = True

# jogador/coração
heart = pygame.image.load("images/heart32x.png").convert_alpha()
x, y = (width / 2) - 32, (height / 2) - 32
squareSize = 32
velocity = 5


def limitposition(x, y):
    x = max(16, min(width - 48, x))
    y = max(16, min(height - 48, y))
    return x, y

# Função para calcular movimento diagonal
def diagonalmovement(keys):
    global velocity
    return velocity * (math.sqrt(2) / 2) if keys else 0

offset = 16

# Variáveis de controle do tempo
start_time = pygame.time.get_ticks()
display_stage = 0
start_time = pygame.time.get_ticks()
show_overlay = True
overlay_displayed = False
wait_time = 1000

def initscreen():
    borda = pygame.Surface((width - 16, height - 16), pygame.SRCALPHA)
    borda.fill((0, 0, 0, 0))
    startscreen = pygame.image.load("images/start.png")
    startscreenhover = pygame.image.load("images/starthover.png")
    pygame.mixer.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load("sounds/menu.ogg")
    pygame.mixer.music.play()
    while True:
        screen.fill((30, 30, 30))  # Fundo escuro para contraste
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if 255 <= pos[1] <= 350 and 255 <= pos[0] <= 410:
                    maingame()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if 255 <= pos[1] <= 350 and 255 <= pos[0] <= 410:
            screen.blit(startscreenhover, (0, 0))
        else:
            screen.blit(startscreen, (0, 0))
        # pygame.draw.rect(screen, "cyan", (225, 255, 190, 95), 1)
        pygame.display.flip()
        clock.tick(60)

def deathscreen():
    global start_time, display_stage, maxlevel, font, x, y
    
    # sons
    deathsound1 = pygame.mixer.Sound('sounds/death1.wav')
    deathsound2 = pygame.mixer.Sound('sounds/death2.wav')
    deathsound3 = pygame.mixer.Sound('sounds/death3.wav')
    heart = pygame.image.load("images/heart64x.png")
    heart_dead = pygame.image.load("images/heartdead64x.png")

    screen.fill((0, 0, 0))
    pygame.mixer.music.unload()
    pygame.mixer.stop()

    screen.blit(heart, (x - 16, y - 16))
    screen.blit(heart, (x - 16, y - 16))
    deathsound1.play()
    pygame.display.flip()
    pygame.time.delay(1000)


    screen.fill((0, 0, 0))
    screen.blit(heart_dead, (x - 16, y - 16))
    screen.blit(heart_dead, (x - 16, y - 16))
    deathsound2.play()
    pygame.display.flip()
    pygame.time.delay(1000)


    screen.fill((0, 0, 0))
    deathsound3.play()
    pygame.display.flip()
    pygame.time.delay(1000)

    pygame.mixer.music.load("sounds/determination.ogg")
    pygame.mixer.music.play()
    
    surface_youdied = font.render(f"Você morreu.", True, 'white')
    surface_levelreached = font.render(f"Você chegou no Nível {level: .0f}.", True, 'white')
    if level > maxlevel:
        surface_maxlevelreached = font.render(f"Você bateu seu recorde de {maxlevel: .0f}!", True, 'white')
        maxlevel = level
    else:
        surface_maxlevelreached = font.render(f"Seu recorde é o Nível {maxlevel: .0f}.", True, 'white')
    screen.blit(surface_youdied, (width / 5, (width / 4) - 50))
    screen.blit(surface_levelreached, (width / 5, (width / 4) - 25))
    screen.blit(surface_maxlevelreached, (width / 5, (width / 4)))
    pygame.display.flip()
    breakwhile = True
    while breakwhile:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if 255 <= pos[1] <= 350 and 255 <= pos[0] <= 410:
                        breakwhile = False
                        break   
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit() 
        pygame.display.flip()
        clock.tick(60)
    initscreen()

def newlevelscreen():
    soundnewlevel1 = pygame.mixer.Sound('sounds/newlevel1.wav')
    soundnewlevel2 = pygame.mixer.Sound('sounds/newlevel2.wav')
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

def maingame():
    global newlevel, level, maxlevel, x, y

    
    level = 1
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

    # músicas de fundo
    pygame.mixer.music.load("sounds/sans.ogg")

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
            newlevelscreen()
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
        elif level == 5:
            if len(bones) < 5:  # Criar no máximo 5 ossos normais e 5 flipped
                if bone_spawn_timer % bone_delay == 0:  # Verifica o tempo para spawn
                    bones.append({"x": width, "y": 256})  # Osso normal
                    flipped_bones.append({"x": width, "y": -128})  # Osso invertido
                bone_spawn_timer += 1  # Incrementa o temporizador
            
            # Atualiza a posição de cada osso normal e desenha na tela
            for bone_obj in bones:
                bone_obj["x"] -= 4  # Movendo para a esquerda
                screen.blit(bone, (bone_obj["x"], bone_obj["y"]))

            # Atualiza a posição de cada osso invertido e desenha na tela
            for flipped_bone_obj in flipped_bones:
                flipped_bone_obj["x"] -= 4  # Movendo para a esquerda
                screen.blit(flippedbone, (flipped_bone_obj["x"], flipped_bone_obj["y"]))

            # Remover ossos que saíram da tela
            bones = [b for b in bones if b["x"] > -24]
            flipped_bones = [b for b in flipped_bones if b["x"] > -24]

            # Colisão com ossos normais
            for bone_obj in bones:
                bone_rect = pygame.Rect(bone_obj["x"] + 4, bone_obj["y"], 24, 320)
                if heart_rect.colliderect(bone_rect):
                    deathscreen()

            # Colisão com ossos invertidos
            for flipped_bone_obj in flipped_bones:
                flipped_bone_rect = pygame.Rect(flipped_bone_obj["x"] + 4, flipped_bone_obj["y"], 24, 320)
                if heart_rect.colliderect(flipped_bone_rect):
                    deathscreen()

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
        screen.blit(heart, (x, y))
        screen.blit(bone, (bonex, boney))
        screen.blit(flippedbone, (flippedbonex, flippedboney))
        
        pygame.draw.rect(screen, "black", (0, 0, width, height), 8)
        pygame.draw.rect(screen, "white", (8, 8, width - 16, height - 16), 8)
        
        if heart_rect.colliderect(bones_rect) or heart_rect.colliderect(flippedbone_rect): 
            deathscreen()

        pygame.display.flip()
        clock.tick(60)

initscreen()