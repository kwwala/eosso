import pygame

class CerejaSprite(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    cereja_img  = pygame.image.load('cereja.png').convert_alpha()
    cereja_img = pygame.transform.scale(cereja_img, (100, 100))
    self.image = cereja_img
    self.rect = cereja_img.get_rect()
    self.rect.topleft = (x, y)
  
  def mover(self):
    if self.rect.x == 10:
      self.rect.topleft = (500, 500)
    else:
      self.rect.topleft = (10, 10)

class PacmanSprite(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)  # prepara o comportamento do Sprite
    img = pygame.image.load('pacman.png').convert_alpha()
    self.img_1 = pygame.transform.scale(img, (100, 100))
    img = pygame.image.load('pacman2.png').convert_alpha()
    self.img_2 = pygame.transform.scale(img, (100, 100))
    self.image = self.img_1
    self.rect = self.image.get_rect()
    self.rect.topleft = (250, 250)
    # variáveis para controlar a movimentação do pacman
    self.velocidade = 10
    self.sentido = 1 # 1 = para a direita, -1 = para a esquerda
    # variável para controlar a velocidade de animação do pacman
    self.tick = 1

  def update(self):
    if self.tick == 15:
      self.tick = 0
      if self.image == self.img_1:
        self.image = self.img_2
      else:
        self.image = self.img_1
    self.tick += 1

  def para_a_esquerda(self):
    if self.sentido == 1:
      self.sentido = -1
      self.img_1 = pygame.transform.flip(self.img_1, True, False)
      self.img_2 = pygame.transform.flip(self.img_2, True, False)
      self.image = pygame.transform.flip(self.image, True, False)
    self.rect.x -= self.velocidade

  def para_a_direita(self):
    if self.sentido == -1:
      self.sentido = 1
      self.img_1 = pygame.transform.flip(self.img_1, True, False)
      self.img_2 = pygame.transform.flip(self.img_2, True, False)
      self.image = pygame.transform.flip(self.image, True, False)
    self.rect.x += self.velocidade

  def para_cima(self):
    self.rect.y -= self.velocidade

  def para_baixo(self):
    self.rect.y += self.velocidade

### GAME LOOP ###
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# cria sprites
pacman = PacmanSprite()
todos_sprites = pygame.sprite.Group([pacman])
lista_cerejas = [CerejaSprite(10, 10), CerejaSprite(500, 10), CerejaSprite(250, 500)]
todos_sprites.add(lista_cerejas)
sprites_cerejas = pygame.sprite.Group([lista_cerejas])

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()

  keys = pygame.key.get_pressed() # Para capturar o pressionamento das teclas de forma contínua
  if keys[pygame.K_LEFT]:
    pacman.para_a_esquerda()
  if keys[pygame.K_RIGHT]:
    pacman.para_a_direita()
  if keys[pygame.K_UP]:
    pacman.para_cima()
  if keys[pygame.K_DOWN]:
    pacman.para_baixo()

  # verifica colisão do pacman com alguma cereja
  hit_list = pygame.sprite.spritecollide(pacman, sprites_cerejas, True)
  todos_sprites.remove(hit_list)
  sprites_cerejas.remove(hit_list)

  todos_sprites.update() # chama a função update de todos os sprites

  screen.fill((255, 255, 255)) # limpa a tela

  # desenha os sprites
  todos_sprites.draw(screen)

  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)

pygame.quit()
