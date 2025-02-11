import pygame
import time

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
# Criando o objeto Font. O primeiro argumento é uma string que indica a fonte a ser utilizada.
# O valor None faz com que o pygame use sua fonte padrão. O segundo argumento indica o tamanho da fonte.
font = pygame.font.Font(None, 40)

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
  # Define o texto e cria sua superfície. O segundo argumento indica o uso ou não de anti-aliasing.
  # O terceiro argumento indica a cor do texto.

  if newlevel:
    overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
    overlay.fill((255, 0, 0, 128))  # RGBA: vermelho com 50% de transparência
    pygame.display.flip()
    soundnewlevel1.play()
    time.sleep(1)
    surface_level = font.render(f"Nível: {level}", True, 'white')
    surface_maxlevel = font.render(f"Recorde: {maxlevel}", True, 'white')
    text_render_x = (width // 2) - surface_level.get_width() // 2
    text_render_y = (height // 2) - surface_level.get_height() // 2
    screen.blit(surface_level, (text_render_x - 30, text_render_y - 17))
    screen.blit(surface_maxlevel, (text_render_x - 30, text_render_y + 17))
    pygame.display.flip()
    soundnewlevel2.play()
    time.sleep(1)
    soundnewlevel1.play()
    newlevel = False
  screen.fill((0, 0, 0))
  # Desenha o texto na posição x, y
  pygame.display.flip() # Desenha o quadro atual na tela
  clock.tick(60)
