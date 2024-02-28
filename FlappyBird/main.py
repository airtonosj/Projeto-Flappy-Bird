import pygame
import os
import random

SCREEN_WIDTH = 500
SCREEN_HEIGH = 800

IMAGE_PIPE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'pipe.png')))
IMAGE_BASE = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'base.png')))
IMAGE_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bg.png')))
IMAGE_BIRD = [
  pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird1.png'))),
  pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird2.png'))),
  pygame.transform.scale2x(pygame.image.load(os.path.join('images', 'bird3.png')))]

pygame.font.init()
FONT_POINTS = pygame.font.SysFont('arial', 50)

class Bird:
  IMG = IMAGE_BIRD
  ROTATION_MAX = 25
  SPEED_ROTATION = 20
  TIME_ANIMATION = 5

  def __init__(self, x,y):
    self.x = x
    self.y = y
    self.angle = 0
    self.speed = 0
    self.height = self.y
    self.time = 0
    self.count_image = 0
    self.image = self.IMG[0]

  def jump(self):
    self.speed = -10.5
    self.time = 0
    self.height = self.y

  def move(self):
    self.time += 1 
    d = 1.5*(self.time**2) + self.speed * self.time

    if d > 16:
      d = 16
    
    elif d < 0:
      d -= 2

    self.y = self.y + d

    if d < 0 or self.y < (self.height + 50):
      if self.angle < self.ROTATION_MAX:
        self.angle = self.ROTATION_MAX

      else:
        if self.angle > -90:
          self.angle -= self.SPEED_ROTATION

  def draw(self, screen):
    self.count_image += 1
    
    if self.count_image < self.TIME_ANIMATION:
      self.image = self.IMG[0]
    elif self.count_image < self.TIME_ANIMATION*2:
      self.image = self.IMG[1]
    elif self.count_image < self.TIME_ANIMATION*3:
      self.image = self.IMG[2]
    elif self.count_image < self.TIME_ANIMATION*4:
      self.image = self.IMG[1]
    elif self.count_image < self.TIME_ANIMATION*5:
      self.image = self.IMG[0]
      self.count_image = 0

    if self.angle <= -80:
      self.image = self.IMG[1]
      self.count_image = self.TIME_ANIMATION*2

    rotated_image = pygame.transform.rotate(self.image, self.angle)
    pos_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
    retangle = rotated_image.get_rect(center=pos_center_image)
    screen.blit(rotated_image, retangle.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.image)

class Pipe:
  DISTANCE = 200
  SPEED = 5

  def __init__(self, x):
    self.x = x
    self.height = 0
    self.pos_top = 0
    self.pos_base = 0
    self.PIPE_BASE = IMAGE_PIPE
    self.PIPE_TOP = pygame.transform.flip(IMAGE_PIPE, False, True)
    self.passed = False
    self.set_height()
  
  def set_height(self):
    self.height = random.randrange(50 , 450)
    self.pos_top = self.height - self.PIPE_TOP.get_height()
    self.pos_base = self.height + self.DISTANCE

  def move(self):
    self.x -= self.SPEED

  def draw(self, screen):
    screen.blit(self.PIPE_TOP, (self.x, self.pos_top))
    screen.blit(self.PIPE_BASE, (self.x, self.pos_base))

  def collide(self, bird):
    bird_mask = bird.get_mask()
    top_mask = pygame.mask.from_surface(self.PIPE_TOP)
    base_mask = pygame.mask.from_surface(self.PIPE_BASE)

    distance_top = (self.x - bird.x, self.pos_top - round(bird.y))
    distance_base = (self.x - bird.x, self.pos_base - round(bird.y))

    top_point = bird_mask.overlap(top_mask, distance_top)
    base_point = bird_mask.overlap(base_mask, distance_base)

    if base_point or top_point:
      return True
    else:
      return False
      

class Base:
  SPEED = 5
  WIDHT = IMAGE_BASE.get_width()
  IMAGE = IMAGE_BASE

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.WIDHT

  def move(self):
    self.x1 -= self.SPEED
    self.x2 -= self.SPEED

    if self.x1 + self.WIDHT < 0:
      self.x1 = self.WIDHT
    if self.x2 + self.WIDHT < 0:
      self.x2 = self.WIDHT

  def draw(self, screen):
    screen.blit(self.IMAGE, (self.x1, self.y))
    screen.blit(self.IMAGE, (self.x2, self.y))

def draw_screen(screen, birds, pipes, base, points):
  screen.blit(IMAGE_BACKGROUND, (0,0))
  for bird in birds:
    bird.draw(screen)
  for pipe in pipes:
    pipe.draw(screen)

  text = FONT_POINTS.render(f"Points: {points}", 1, (255, 255, 255))
  screen.blit(text, (SCREEN_WIDTH - 10 - text.get_width(), 10))
  base.draw(screen)
  pygame.display.update()

def  main():
  birds = [Bird(230, 350)]
  base = Base(730)
  pipes = [Pipe(700)]
  screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGH))
  points = 0
  clock = pygame.time.Clock()

  running = True
  while running:
    clock.tick(60)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          for bird in birds:
            bird.jump()
            
    for bird in birds:
      bird.move()
    base.move()

    add_pipe = False
    remove_pipes = []
    for pipe in pipes:
      for i, bird in enumerate(birds):
        if pipe.collide(bird):
          birds.pop(i)
        if not pipe.passed and bird.x > pipe.x:
          pipe.passed = True
          add_pipe = True
      pipe.move()
      
      if pipe.x + pipe.PIPE_TOP.get_width() < 0:
        remove_pipes.append(pipe)

    if add_pipe:
      points += 1
      pipes.append(Pipe(600))
    for pipe in remove_pipes:
      pipes.remove(pipe)

    for i, bird in enumerate(birds):
      if bird.y + bird.image.get_height() > SCREEN_HEIGH or bird.y < 0:
        birds.pop(i)
    
    draw_screen(screen, birds, pipes, base, points)
    
    

if __name__ == '__main__':
  main()