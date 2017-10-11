import pygame


pygame.init()
framerate = 10
screenDimension = (640,480) 
screen = pygame.display.set_mode(screenDimension)
pygame.display.set_caption("Awesome team")
background = screen.convert()
clock = pygame.time.Clock()


for a in xrange(200):
    
    pygame.draw.rect(background, (0,0,0), (0,0, screenDimension[0],screenDimension[1]))
    
    pygame.draw.rect(background, (120,31,142), (a,a,100,200))
    screen.blit(background, (0,0))
    pygame.display.flip()
    clock.tick(framerate)
      