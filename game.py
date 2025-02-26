import pygame
import math
import os

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load('images/shadedicon.png'))
pygame.display.set_caption("É Osso")

# Setup resources
fontPath = os.path.join(os.path.dirname(__file__), "fonts", "minecraftia.ttf")
font = pygame.font.Font(fontPath, 24)
width, height = screen.get_size()

# Game state variables
level = 1
maxLevel = 3
newLevel = True
squareSize = 32
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
    if recordBreak:
        maxLevel = level
    
    # Create text surfaces
    gameOverTexts = [
        font.render("Você morreu.", True, 'white'),
        font.render(f"Você chegou no Nível {level:.0f}.", True, 'white'),
        font.render(f"Você bateu seu recorde de {maxLevel:.0f}!" if recordBreak 
                   else f"Seu recorde é o Nível {maxLevel:.0f}.", True, 'white')
    ]
    
    # Position and render text
    deathScreenImage = pygame.image.load("images/deathScreen.png")
    deathScreenPlayHover = pygame.image.load("images/deathScreenPlayHover.png")
    deathScreenMenuHover = pygame.image.load("images/deathScreenMenuHover.png")
    
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

def mainGame():
    global newLevel, level, maxLevel, x, y

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

        # Level logic
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
            heartRect = pygame.Rect(newX, y, squareSize, squareSize)
            
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
            heartRect = pygame.Rect(newX, y, squareSize, squareSize)
            
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
        else:
            print('tá fazendo o que aqui, bobão?')
            exit()

        # Draw bones for levels 1-4
        if level < 5:
            screen.blit(bone, (boneX, boneY))
            screen.blit(flippedBone, (flippedBoneX, flippedBoneY))
            
            # Collision detection for levels 1-4
            heartRect = pygame.Rect(newX, y, squareSize, squareSize)
            bonesRect = pygame.Rect(boneX + 4, boneY, 24, 320)
            flippedBoneRect = pygame.Rect(flippedBoneX + 4, flippedBoneY, 24, 320)
            
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

# Start the game
initScreen()