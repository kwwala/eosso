import pygame
import time

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
# Criando o objeto Font. O primeiro argumento é uma string que indica a fonte a ser utilizada.
# O valor None faz com que o pygame use sua fonte padrão. O segundo argumento indica o tamanho da fonte.
font = pygame.font.Font(None, 40)

width, height = screen.get_size()

level = 12
maxlevel = 100
newlevel = True


width, height = screen.get_size()

soundnewlevel1 = pygame.mixer.Sound('sounds/newlevel1.wav')
soundnewlevel2 = pygame.mixer.Sound('sounds/newlevel2.wav')


while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
  screen.fill((0, 0, 0)) # apaga o quadro atual
  screen.fill((0, 0, 0))
  outline = pygame.Rect((8, 8), (width - 16, height - 16))
  pygame.draw.rect(outline, "white", 8, 24)
  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
