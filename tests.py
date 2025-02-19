import pygame

# Inicializa o pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Retângulo Transparente")
width, height = screen.get_size()

# Cores
BRANCO = (255, 255, 255)
TRANSPARENTE = (0, 0, 0, 0)  # Cor de fundo totalmente transparente

# Criando uma superfície transparente

borda = pygame.Surface((width - 16, height - 16), pygame.SRCALPHA)
borda.fill((0, 0, 0, 0))

# Loop principal
rodando = True
while rodando:
    screen.fill((30, 30, 30))  # Fundo escuro para contraste
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Desenhando o retângulo transparente
    screen.blit(borda, (300, 250))
    pygame.draw.rect(screen, "black", (0, 0, width, height), 8)
    pygame.draw.rect(screen, "white", (8, 8, width - 16, height - 16), 8)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
