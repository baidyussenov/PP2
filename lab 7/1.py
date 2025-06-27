import pygame
import sys
import datetime


pygame.init()
screen = pygame.display.set_mode((1400, 950))
clock = pygame.time.Clock()


background = pygame.image.load("clock.png")
right_arm = pygame.image.load("rightarm.png")
left_arm = pygame.image.load("leftarm.png")    


center = (699, 990)


rw, rh = right_arm.get_size()
lw, lh = left_arm.get_size()

def blit_rotate(image, pos, origin, angle):
    
    image_rect = image.get_rect(topleft=(pos[0] - origin[0], pos[1] - origin[1]))
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)
    screen.blit(rotated_image, rotated_rect.topleft)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = datetime.datetime.now()

  
    seconds = now.second + now.microsecond / 950000
    minutes = now.minute + seconds / 60


    angle_sec = -seconds * 6             
    angle_min = -minutes * 6 + 670
   
    screen.blit(background, (0, 0))

    blit_rotate(right_arm, center, (rw / 2, rh * 0.95), angle_min)

    
    blit_rotate(left_arm, center, (lw / 2, lh * 0.95), angle_sec)

   
    pygame.draw.circle(screen, (0, 255, 0), center, 5)

    pygame.display.flip()
    clock.tick(60)