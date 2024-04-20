import time
import pygame
import numpy as np

# COLORS
# 0: Background
# 1: Grid
# 2: Die cell
# 3: Alive cell
COLORS = [(10,10,10), (40,40,40), (170,170,170), (255,255,255)]


def update(screen, cells, size, is_progress=False):
  newCell = np.zeros((cells.shape[0], cells.shape[1]))

  for row, col in np.ndindex(cells.shape):
    count = 0
    color = COLORS[0] if cells[row, col] == 0 else COLORS[3]

    # Count 8 neighbors if not 0 then add to count
    for i in range(-1, 2):
      for j in range(-1, 2):
        if i == 0 and j == 0:
          continue
        if cells[(row+i)%size, (col+j)%size] != 0:
          count += 1


    # If cell is alive
    if cells[row, col] != 0:
      if count < 2 or count > 3 and is_progress:
        color = COLORS[2]
      elif 2 <= count <= 3:
        newCell[row, col] = 1
        if is_progress:
          color = COLORS[3]
    else:
      if count == 3:
        newCell[row, col] = 1
        if is_progress:
          color = COLORS[3]

    pygame.draw.rect(screen, color, (col*size, row*size, size-1, size-1))
  return newCell

def main():
  pygame.init()
  screen = pygame.display.set_mode((800, 600))

  cells = np.zeros((60,80))
  screen.fill(COLORS[1])
  update(screen, cells, 10)

  pygame.display.flip()
  pygame.display.update()

  running = False

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        return
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          running = not running
          update(screen, cells, 10)
          pygame.display.update()
      if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        cells[y//10, x//10] = 1
        update(screen, cells, 10)
        pygame.display.update()
    screen.fill(COLORS[1])

    if running:
      cells = update(screen, cells, 10, True)
      pygame.display.update()
      time.sleep(0.001)

if __name__ == "__main__":
  main()






# REFERENCES
# https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
# https://youtu.be/cRWg2SWuXtM