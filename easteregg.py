import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
running = True
width, height = screen.get_size()

easterEggX = width / 2 - 16
easterEggY = height / 2 - 16
easterEggXMovement = 5
easterEggYMovement = 5
heart = pygame.image.load("images/heart32x.png").convert_alpha()
font.render(f"Nível: {level:.0f}", True, 'white')

levelTexts = [
        font.render(f"Nível: {level:.0f}", True, 'white'),
        font.render(f"Recorde: {maxLevel:.0f}", True, 'white')
    ]
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        quit()

    screen.fill((0, 0, 0))

    if easterEggX > width - 48 or easterEggX < 16:
        easterEggXMovement = easterEggXMovement * -1
    if easterEggY > height - 48 or easterEggY < 16:
        easterEggYMovement = easterEggYMovement * -1

    easterEggX += easterEggXMovement
    easterEggY += easterEggYMovement

    screen.blit(heart, (easterEggX, easterEggY))

    for i, text in enumerate(levelTexts):
        textRect = text.get_rect(center=(width // 2, height // 2))
        textShadow = text.copy()
        textShadow.fill((128, 128, 128, 128), special_flags=pygame.BLEND_RGBA_MULT)
        screen.blit(textShadow, (textRect[0] + 3, textRect[1] - 12 + (i * 30)))
        screen.blit(text, (textRect[0], textRect[1] - 15 + (i * 30)))

    pygame.draw.rect(screen, "white", (8, 8, width - 16, height - 16), 8)

    pygame.display.flip()
    clock.tick(60)

