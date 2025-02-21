import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Retângulo Transparente")
width, height = screen.get_size()

# Cores
BRANCO = (255, 255, 255)
TRANSPARENTE = (0, 0, 0, 0)  # Cor de fundo totalmente transparente

# Criando uma superfície transparente

borda = pygame.Surface((width - 16, height - 16), pygame.SRCALPHA)
borda.fill((0, 0, 0, 0))
startscreen = pygame.image.load("images/start.png")
# Loop principal
rodando = True
while rodando:
    screen.fill((30, 30, 30))  # Fundo escuro para contraste
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                if 255 <= pos[1] <= 350 and 255 <= pos[0] <= 410:
                    pygame.quit()
                    exit() # enquanto eu não faço tudo direitinho eu coloco pra fechar a janela pra ver se funciona o básico
        elif event.type == pygame.QUIT:
            rodando = False
    # Desenhando o retângulo transparente
    screen.blit(borda, (300, 250))
    screen.blit(startscreen, (0, 0))
    pygame.draw.rect(screen, "cyan", (225, 255, 190, 95), 1)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
