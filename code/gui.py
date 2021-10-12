import pygame

pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1400, 1000))

# Changing the title
pygame.display.set_caption('Control Pannel')

# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

# Astronaut
astronautImg = pygame.image.load('images/32astro.png')
astronautX = 370
astronautY = 480

oval =  pygame.image.load('images/oval.png')
image1 = pygame.image.load('images/dry-clean.png')
image2 = pygame.image.load('images/full-moon.png')
image3 = pygame.image.load('images/rec.png')

def astronaut():
    screen.blit(astronautImg,(astronautX,astronautY))

# GUI loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        screen.fill((255,153,102))
        astronaut()
        screen.blit(oval, (300, 200))
        pygame.display.update()
