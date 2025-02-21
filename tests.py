import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Retângulo Transparente")
width, height = screen.get_size()

def initscreen():
    borda = pygame.Surface((width - 16, height - 16), pygame.SRCALPHA)
    borda.fill((0, 0, 0, 0))
    startscreen = pygame.image.load("images/start.png")
    while True:
        screen.fill((30, 30, 30))  # Fundo escuro para contraste
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    if 255 <= pos[1] <= 350 and 255 <= pos[0] <= 410:
                        pygame.quit()
                        exit() # enquanto eu não faço tudo direitinho eu coloco pra fechar a janela pra ver se funciona o básico
        screen.blit(borda, (300, 250))
        screen.blit(startscreen, (0, 0))
        pygame.draw.rect(screen, "cyan", (225, 255, 190, 95), 1)
        pygame.display.flip()

initscreen()