import pygame
import math
import os

# Initialize pygame
pygame.display.set_caption("É Osso")
icon = pygame.image.load('images/shadedicon.png')
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Setup resources
font = pygame.font.Font("fonts/minecraftia.ttf", 24)
width, height = screen.get_size()

# Game state variables
level = 1
maxLevel = 0
newLevel = True
heartSize = 32
velocity = 5

# Player setup
heart = pygame.image.load("images/heart32x.png").convert_alpha()
x, y = (width / 2) - 16, (height / 2) - 16

def limitPosition(x, y):
    return max(16, min(width - 48, x)), max(16, min(height - 48, y))

def diagonalMovement():
    return velocity * (math.sqrt(2) / 2)

def initScreen():
    # Load assets
    startScreen = pygame.image.load("images/startScreen.png")
    startScreenHover = pygame.image.load("images/startHoverScreen.png")
    pygame.mixer.stop()
    pygame.mixer.music.load("sounds/menu.ogg")
    pygame.mixer.music.play(-1)
    
    while True:
        screen.fill((30, 30, 30))
        pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if 260 <= pos[0] <= 380 and 280 <= pos[1] <= 330:
                    mainGame()
                elif pos[0] < 50 and pos[1] > height - 50:
                    easterEgg()
        
        screen.blit(startScreenHover if (260 <= pos[0] <= 380 and 280 <= pos[1] <= 330) else startScreen, (0, 0))
        # pygame.draw.rect(screen, "cyan", (260, 280, 120, 50), 1)

        pygame.display.flip()
        clock.tick(60)

def deathScreen():
    global maxLevel, x, y
    
    # Load death sequence assets
    deathSounds = [
        pygame.mixer.Sound('sounds/death1.wav'),
        pygame.mixer.Sound('sounds/death2.wav'),
        pygame.mixer.Sound('sounds/death3.wav')
    ]
    heartLarge = pygame.image.load("images/heart64x.png")
    heartDead = pygame.image.load("images/heartdead64x.png")

    # Stop all sounds and music
    pygame.mixer.music.unload()
    pygame.mixer.stop()

    # Death animation sequence
    screen.fill((0, 0, 0))
    screen.blit(heartLarge, (x - 16, y - 16))
    deathSounds[0].play()
    pygame.display.flip()
    pygame.time.delay(1000)

    screen.fill((0, 0, 0))
    screen.blit(heartDead, (x - 16, y - 16))
    deathSounds[1].play()
    pygame.display.flip()
    pygame.time.delay(1000)

    screen.fill((0, 0, 0))
    deathSounds[2].play()
    pygame.display.flip()
    pygame.time.delay(1000)

    # Game over screen
    pygame.mixer.music.load("sounds/determination.ogg")
    pygame.mixer.music.play(-1)
    
    # Update max level if needed
    recordBreak = level > maxLevel

    # Create text surfaces
    gameOverTexts = [
        font.render("Você morreu.", True, 'white'),
        font.render(f"Você chegou no Nível {level:.0f}.", True, 'white'),
        font.render(f"Você bateu seu recorde de {maxLevel:.0f}!" if recordBreak 
                   else f"Seu recorde é o Nível {maxLevel:.0f}.", True, 'white')
    ]
    
    # Position and render text
    deathScreenImage = pygame.image.load("images/clickScreen.png")
    deathScreenPlayHover = pygame.image.load("images/playHoverScreen.png")
    deathScreenMenuHover = pygame.image.load("images/menuHoverScreen.png")
    deathScreenOverlay = pygame.image.load("images/deathScreenOverlay.png")

    
    # Wait for mouse click
    waitForClick = True
    while waitForClick:
        pos = pygame.mouse.get_pos()
        if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294:
            screen.blit(deathScreenPlayHover, (0, 0))
        elif 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
            screen.blit(deathScreenMenuHover, (0, 0))
        else:
            screen.blit(deathScreenImage, (0, 0))

        screen.blit(deathScreenOverlay, (0, 0))

        for i, text in enumerate(gameOverTexts):
            textRect = text.get_rect(center=(width // 2, height // 2))
            textShadow = text.copy()
            textShadow.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(textShadow, (textRect[0] + 3, textRect[1] - 95 + (i * 30)))
            screen.blit(text, (textRect[0], textRect[1] - 98 + (i * 30)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294 or 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
                    if recordBreak:
                        maxLevel = level
                    if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294:
                        mainGame()
                    elif 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
                        initScreen()
        pygame.display.flip()
        clock.tick(60)

def newLevelScreen():
    soundNewLevel = [
        pygame.mixer.Sound('sounds/newlevel1.wav'),
        pygame.mixer.Sound('sounds/newlevel2.wav')
    ]
    
    pygame.mixer.music.pause()
    
    # Semi-transparent overlay
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))
    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    # soundNewLevel[0].play()
    # pygame.time.delay(1000)
    
    # Level info
    levelTexts = [
        font.render(f"Nível: {level:.0f}", True, 'white'),
        font.render(f"Recorde: {maxLevel:.0f}", True, 'white')
    ]
    
    for i, text in enumerate(levelTexts):
        textRect = text.get_rect(center=(width // 2, height // 2))
        textShadow = text.copy()
        textShadow.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(textShadow, (textRect[0] + 3, textRect[1] - 12 + (i * 30)))
        screen.blit(text, (textRect[0], textRect[1] - 15 + (i * 30)))
    
    pygame.display.flip()
    soundNewLevel[1].play()
    pygame.time.delay(1000)

    soundNewLevel[0].play()
    pygame.mixer.music.unpause()

def winScreen():
    global level, maxLevel

    pygame.mixer.music.unload()
    pygame.mixer.stop()
    pygame.mixer.music.load("sounds/holiday.ogg")
    pygame.mixer.music.play(-1)


    recordBreak = level > maxLevel

    gameOverTexts = [
        font.render("Parabéns!", True, 'white'),
        font.render(f"Você zerou esse jogo.", True, 'white'),
        font.render(f"Você bateu seu recorde de {maxLevel:.0f}!" if recordBreak 
                   else f"Você já tinha zerado antes.", True, 'white')
    ]
    
    # Position and render text
    deathScreenImage = pygame.image.load("images/clickScreen.png")
    deathScreenPlayHover = pygame.image.load("images/playHoverScreen.png")
    deathScreenMenuHover = pygame.image.load("images/menuHoverScreen.png")

    
    # Wait for mouse click
    waitForClick = True
    while waitForClick:
        pos = pygame.mouse.get_pos()
        if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294:
            screen.blit(deathScreenPlayHover, (0, 0))
        elif 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
            screen.blit(deathScreenMenuHover, (0, 0))
        else:
            screen.blit(deathScreenImage, (0, 0))

        for i, text in enumerate(gameOverTexts):
            textRect = text.get_rect(center=(width // 2, height // 2))
            textShadow = text.copy()
            textShadow.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(textShadow, (textRect[0] + 3, textRect[1] - 95 + (i * 30)))
            screen.blit(text, (textRect[0], textRect[1] - 98 + (i * 30)))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294 or 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
                    if recordBreak:
                        maxLevel = level
                    if 260 <= pos[0] <= 380 and 244 <= pos[1] <= 294:
                        mainGame()
                    elif 260 <= pos[0] <= 380 and 304 <= pos[1] <= 354:
                        initScreen()
        pygame.display.flip()
        clock.tick(60)

def mainGame():
    global newLevel, level, maxLevel, x, y
    global boneX8, boneY8, phase8, flippedBoneX8, flippedBoneY8, phase8_flipped


    # levels
    level = 1
    newLevel = True

    # Game objects
    bone = pygame.image.load("images/bone.png")
    flippedBone = pygame.transform.flip(bone, False, True)
    
    # Initial positions
    boneX, boneY = width, 272
    flippedBoneX, flippedBoneY = width, -112
    x, y = (width / 2) - 16, (height / 2) - 16
    
    # Load game music
    pygame.mixer.music.load("sounds/sans.ogg")

    # Game variables for level 5
    amountBones = []
    amountFlippedBones = []
    boneSpawnTimer = 0
    boneTickDelay = 15
    totalBones = 0
    maxBones = 5

    # variaveis level 8
    boneX8 = width
    boneY8 = 272 - 32
    phase8 = "horizontal_left"
    
    flippedBoneX8 = 8
    flippedBoneY8 = -112
    phase8_flipped = "horizontal_right"

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        
        # Movement controls
        dx = dy = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= velocity
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += velocity
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= velocity
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += velocity

        # Diagonal movement adjustment
        if dx != 0 and dy != 0:
            diagonal = diagonalMovement()
            dx = diagonal * (1 if dx > 0 else -1)
            dy = diagonal * (1 if dy > 0 else -1)

        # Update position
        newX = x + dx
        newY = y + dy
        x, y = limitPosition(newX, newY)

        # Clear screen and draw player
        screen.fill((0, 0, 0))
        screen.blit(heart, (x, y))

        # Collision detection for levels 1-4
        heartRect = pygame.Rect(newX, y, heartSize, heartSize)
        bonesRect = pygame.Rect(boneX + 4, boneY, 24, 320)
        flippedBoneRect = pygame.Rect(flippedBoneX + 4, flippedBoneY, 24, 320)

        
        if level == 1:
            boneX -= 2
            if boneX <= -16:
                level += 1
                boneX = width
                newLevel = True
        elif level == 2:
            boneX -= 4
            if boneX <= -16:
                level += 1
                boneX = width
                newLevel = True
        elif level == 3:
            boneX -= 4
            flippedBoneX -= 4
            if boneX <= -16:
                level += 1
                boneX = width
                flippedBoneX = width
                newLevel = True
                boneDirection = -1
        elif level == 4:
            boneX -= 4
            flippedBoneX -= 4

            # Bone movement up/down
            if boneY >= 320:
                boneDirection = -1
            elif boneY <= 250:
                boneDirection = 1

            boneY += boneDirection
            flippedBoneY += boneDirection

            if boneX <= -16:
                level += 1
                boneX = width
                flippedBoneX = width
                newLevel = True
        elif level == 5:
            # Generate bones up to the limit
            if totalBones < maxBones:
                if boneSpawnTimer % boneTickDelay == 0:
                    amountBones.append({"x": width, "y": 272})
                    amountFlippedBones.append({"x": width, "y": -112})
                    totalBones += 1
                boneSpawnTimer += 1
            
            for boneObj in amountBones:
                if "direction" not in boneObj:
                    boneObj["direction"] = 1

                if boneObj["y"] >= 320:
                    boneObj["direction"] = -1
                elif boneObj["y"] <= 250:
                    boneObj["direction"] = 1

                boneObj["y"] += boneObj["direction"]

            for boneObj in amountFlippedBones:
                if "direction" not in boneObj:
                    boneObj["direction"] = 1

                if boneObj["y"] >= -64:
                    boneObj["direction"] = -1
                elif boneObj["y"] <= -134:
                    boneObj["direction"] = 1

                boneObj["y"] += boneObj["direction"]


            # Update and draw bones
            for boneObj in amountBones:
                boneObj["x"] -= 4
                screen.blit(bone, (boneObj["x"], boneObj["y"]))

            for flippedBoneObj in amountFlippedBones:
                flippedBoneObj["x"] -= 4
                screen.blit(flippedBone, (flippedBoneObj["x"], flippedBoneObj["y"]))

            # Remove off-screen bones
            amountBones = [b for b in amountBones if b["x"] > -24]
            amountFlippedBones = [b for b in amountFlippedBones if b["x"] > -24]

            # Collision detection
            heartRect = pygame.Rect(newX, y, heartSize, heartSize)
            
            allAmountBones = amountBones + amountFlippedBones

            for boneObj in allAmountBones:
                boneRect = pygame.Rect(boneObj["x"] + 4, boneObj["y"], 24, 320)
                if heartRect.colliderect(boneRect):
                    deathScreen()
            
            # Level completion check
            if totalBones >= maxBones and not amountBones and not amountFlippedBones:
                level += 1
                newLevel = True
                amountBones.clear()
                amountFlippedBones.clear()
                boneSpawnTimer = 0
                totalBones = 0
        elif level == 6:
            # Generate bones up to the limit
            if totalBones < maxBones:
                if boneSpawnTimer % boneTickDelay == 0:
                    amountBones.append({"x": 8, "y": 272})
                    amountFlippedBones.append({"x": 8, "y": -112})
                    totalBones += 1
                boneSpawnTimer += 1
            
            for boneObj in amountBones:
                if "direction" not in boneObj:
                    boneObj["direction"] = 1

                if boneObj["y"] >= 320:
                    boneObj["direction"] = -1
                elif boneObj["y"] <= 250:
                    boneObj["direction"] = 1

                boneObj["y"] += boneObj["direction"]

            for boneObj in amountFlippedBones:
                if "direction" not in boneObj:
                    boneObj["direction"] = 1

                if boneObj["y"] >= -64:
                    boneObj["direction"] = -1
                elif boneObj["y"] <= -134:
                    boneObj["direction"] = 1

                boneObj["y"] += boneObj["direction"]


            # Update and draw bones
            for boneObj in amountBones:
                boneObj["x"] += 4
                screen.blit(bone, (boneObj["x"], boneObj["y"]))

            for flippedBoneObj in amountFlippedBones:
                flippedBoneObj["x"] += 4
                screen.blit(flippedBone, (flippedBoneObj["x"], flippedBoneObj["y"]))

            # Remove off-screen bones
            amountBones = [b for b in amountBones if b["x"] < width + 24]
            amountFlippedBones = [b for b in amountFlippedBones if b["x"] < width + 24]

            # Collision detection
            heartRect = pygame.Rect(newX, y, heartSize, heartSize)
            
            allAmountBones = amountBones + amountFlippedBones

            for boneObj in allAmountBones:
                boneRect = pygame.Rect(boneObj["x"] + 4, boneObj["y"], 24, 320)
                if heartRect.colliderect(boneRect):
                    deathScreen()
            
            # Level completion check
            if totalBones >= maxBones and not amountBones and not amountFlippedBones:
                level += 1
                newLevel = True
                amountBones.clear()
                amountFlippedBones.clear()
                boneSpawnTimer = 0
                totalBones = 0
        elif level == 7:
            if totalBones < 1:
                if boneSpawnTimer % boneTickDelay == 0:
                    amountBones.append({"x": 8, "y": 272})
                    amountFlippedBones.append({"x": 8, "y": -112})
                    totalBones += 1
                boneSpawnTimer += 1
                
            # blit os ossos
            for boneObj in amountBones:
                boneObj["x"] += 8
                screen.blit(bone, (boneObj["x"], boneObj["y"]))

            for flippedBoneObj in amountFlippedBones:
                flippedBoneObj["x"] += 8
                screen.blit(flippedBone, (flippedBoneObj["x"], flippedBoneObj["y"]))
            
            allAmountBones = amountBones + amountFlippedBones

            for boneObj in allAmountBones:
                boneRect = pygame.Rect(boneObj["x"] + 4, boneObj["y"], 24, 320)
                if heartRect.colliderect(boneRect):
                    deathScreen()

            # Remove ossos que saíram completamente da tela
            amountBones = [b for b in amountBones if b["x"] < width + 24]
            amountFlippedBones = [b for b in amountFlippedBones if b["x"] < width + 24]

            # Se todos os ossos saíram da tela, avance de nível
            if totalBones >= 1 and not amountBones and not amountFlippedBones:
                level += 1
                newLevel = True
                amountBones.clear()
                amountFlippedBones.clear()
                boneSpawnTimer = 0
                totalBones = 0      
        elif level == 8:
            if newLevel:
                boneX8 = width
                boneY8 = 272 - 32
                phase8 = "horizontal_left"
                
                flippedBoneX8 = 8
                flippedBoneY8 = -112
                phase8_flipped = "horizontal_right"
                
                newLevel = False

            # Flags para indicar quando cada osso concluiu o ciclo horizontal de retorno
            normal_bone_done = False
            flipped_bone_done = False

            # Movimento do osso normal
            if phase8 == "horizontal_left":
                boneX8 -= 8  # Movimento para a esquerda
                if boneX8 <= -16:
                    phase8 = "vertical_down"
            elif phase8 == "vertical_down":
                boneY8 += 2  # Movimento vertical (descendo)
                if boneY8 >= 272 + 32:  # Quando atinge 304 (32 pixels abaixo do normal 272)
                    phase8 = "horizontal_right"
            elif phase8 == "horizontal_right":
                boneX8 += 8  # Movimento para a direita
                if boneX8 >= width:
                    normal_bone_done = True

            # Movimento do flippedBone
            if phase8_flipped == "horizontal_right":
                flippedBoneX8 += 8  # Movimento para a direita
                if flippedBoneX8 >= width:
                    phase8_flipped = "vertical_down"
            elif phase8_flipped == "vertical_down":
                flippedBoneY8 += 2  # Movimento vertical (descendo)
                if flippedBoneY8 >= -112 + 64:  # Quando atinge -112 + 32 = -80 (32 pixels abaixo do normal -112)
                    phase8_flipped = "horizontal_left"
            elif phase8_flipped == "horizontal_left":
                flippedBoneX8 -= 8  # Movimento para a esquerda
                if flippedBoneX8 <= -16:
                    flipped_bone_done = True

            # Desenha os ossos
            screen.blit(bone, (boneX8, boneY8))
            screen.blit(flippedBone, (flippedBoneX8, flippedBoneY8))
            
            # Cria os retângulos para detecção de colisão
            boneRect8 = pygame.Rect(boneX8 + 4, boneY8, 24, 320)
            flippedBoneRect8 = pygame.Rect(flippedBoneX8 + 4, flippedBoneY8, 24, 320)
            if heartRect.colliderect(boneRect8) or heartRect.colliderect(flippedBoneRect8):
                deathScreen()

            # Se ambos os ossos completaram o ciclo de retorno, finaliza o nível
            if normal_bone_done and flipped_bone_done:
                level += 1
                newLevel = True
        elif level == 9:
            winScreen()
        else:
            print('tá fazendo o que aqui, bobão?')
            exit()

        # Draw bones for levels 1-4
        if level < 5:
            screen.blit(bone, (boneX, boneY))
            screen.blit(flippedBone, (flippedBoneX, flippedBoneY))
            if heartRect.colliderect(bonesRect) or heartRect.colliderect(flippedBoneRect): 
                deathScreen()

        # Draw border
        pygame.draw.rect(screen, "black", (0, 0, width, height), 8)
        pygame.draw.rect(screen, "white", (8, 8, width - 16, height - 16), 8)
        
        # New level setup
        if newLevel:
            if level == 1:
                pygame.mixer.music.play(-1)
            newLevelScreen()
            newLevel = False
            # Reset level 5 variables if needed
            if level == 5:
                amountBones = []
                amountFlippedBones = []
                boneSpawnTimer = 0
                totalBones = 0

        pygame.display.flip()
        clock.tick(60)

def easterEgg():
    easterEggX = width / 2 - 16
    easterEggY = height / 2 - 16
    easterEggXMovement = easterEggYMovement = 5
    
    h = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            initScreen()

        screen.fill((0, 0, 0))

        if easterEggX > width - 48 or easterEggX < 16:
            easterEggXMovement = easterEggXMovement * -1
        if easterEggY > height - 48 or easterEggY < 16:
            easterEggYMovement = easterEggYMovement * -1

        easterEggX += easterEggXMovement
        easterEggY += easterEggYMovement
        
        h = (h + 1) % 360
        
        # Função para converter HSV para RGB
        def hsv_to_rgb(h, s, v):
            h = h / 360
            c = v * s
            x = c * (1 - abs((h * 6) % 2 - 1))
            m = v - c
            
            if 0 <= h < 1/6:
                r, g, b = c, x, 0
            elif 1/6 <= h < 2/6:
                r, g, b = x, c, 0
            elif 2/6 <= h < 3/6:
                r, g, b = 0, c, x
            elif 3/6 <= h < 4/6:
                r, g, b = 0, x, c
            elif 4/6 <= h < 5/6:
                r, g, b = x, 0, c
            else:
                r, g, b = c, 0, x
                
            r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
            return (r, g, b)
        
        text = font.render(f"o logo do dvd kk", True, hsv_to_rgb(h, 1, 1))
        
        textRect = text.get_rect(center=(width // 2, height // 2))
        textShadow = text.copy()
        textShadow.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(textShadow, (textRect[0] + 3, textRect[1] + 3))
        screen.blit(text, (textRect[0], textRect[1]))
        
        screen.blit(heart, (easterEggX, easterEggY))

        pygame.draw.rect(screen, "white", (8, 8, width - 16, height - 16), 8)

        pygame.display.flip()
        clock.tick(60)

# Start the game
initScreen()




