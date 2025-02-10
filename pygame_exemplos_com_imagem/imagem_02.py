import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# carrega e redimensiona imagens
cereja_img  = pygame.image.load('cereja.png').convert_alpha()
cereja_img = pygame.transform.scale(cereja_img, (100, 100)) # redimensionamento
pacman_img = pygame.image.load('pacman.png').convert_alpha()
pacman_img = pygame.transform.scale(pacman_img, (100, 100)) # redimensionamento

# posiciona imagens
cereja_rect = cereja_img.get_rect()
cereja_rect.topleft = (10, 10)
pacman_rect = pacman_img.get_rect()
pacman_rect.topleft = (250, 250)

# variáveis para controlar a movimentação do pacman
velocidade = 10
sentido = 1 # 1 = para a direita, -1 = para a esquerda

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  keys = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if keys[pygame.K_LEFT]:
    if sentido == 1:
      sentido = -1
      pacman_img = pygame.transform.flip(pacman_img, True, False) # inverte a imagem horizontalmente
    pacman_rect.x -= velocidade
  if keys[pygame.K_RIGHT]:
    if sentido == -1:
      sentido = 1
      pacman_img = pygame.transform.flip(pacman_img, True, False) # inverte a imagem horizontalmente
    pacman_rect.x += velocidade
  if keys[pygame.K_UP]:
    pacman_rect.y -= velocidade
  if keys[pygame.K_DOWN]:
    pacman_rect.y += velocidade

  # verifica colisão e move a cereja em caso positivo
  if pacman_rect.colliderect(cereja_rect):
    if cereja_rect.x == 10:
      cereja_rect.topleft = (500, 500)
    else:
      cereja_rect.topleft = (10, 10)

  screen.fill((255, 255, 255)) # limpa a tela

  # desenha imagens na janela nas posições definidas pelos retângulos das imagens
  screen.blit(cereja_img, cereja_rect.topleft)
  screen.blit(pacman_img, pacman_rect.topleft)

  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)

pygame.quit()
