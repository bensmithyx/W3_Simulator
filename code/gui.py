import pygame

pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Changing the title
pygame.display.set_caption('Control Pannel')

# Adding icon

# GUI loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
