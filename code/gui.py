import pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1600, 1000))

# Changing the title
pygame.display.set_caption('Control Pannel')

# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

x = 800
y = 500
vel = 10

run = True

# Astronaut
def astronaut(x,y):
    screen.blit(astronautImg,(x,y))

astronautImg = pygame.image.load('images/64astro.png')


# Pod A
def poda(x,y):
    screen.blit(pygame.image.load('images/oval.png'),(x,y))


while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= vel
    if keys[pygame.K_RIGHT]:
        x += vel
    if keys[pygame.K_UP]:
        y -= vel
    if keys[pygame.K_DOWN]:
        y += vel

    screen.fill((255,153,102))  # Fills the screen with black
    astronaut(x,y)
    poda(650,290)
    pygame.display.update()

pygame.quit()
