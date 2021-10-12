import pygame, time, simulator
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((1600, 1000))

# Changing the title
pygame.display.set_caption('Control Pannel')

# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

x, x2 = 800, 1000
y, y2 = 500, 500
vel = 30

run = True

# Astronaut
def astronaut(x,y):
    screen.blit(astronautImg,(x,y))

astronautImg = pygame.image.load('images/64astro.png')

# Colours
lightgrey = (170,170,170)
grey = (144,144,144)
colour = grey
doorcolour = (204,204,204)
open = (0,204,0)
closed = (153,0,0)
black = (0,0,0)
lightblue = (0,153,255)

doorcolourdic = {'empty':(0,0,0),'normal':doorcolour,'airlock':lightblue}

class Circle:
    def __init__(self, id, colour, position, radius, borderwidth):
        self.id = id
        self.colour = colour
        self.position = position
        self.radius = radius
        self.borderwidth = borderwidth

    def drawcircle(self):
        pygame.draw.circle(screen, self.colour, self.position, self.radius, self.borderwidth)

class Door:
    def __init__(self, id, name, colour, position):
            self.id = id
            self.name = name
            self.colour = colour
            self.position = position
            for pod in simulator.pods:
                if pod.id == self.id and pod.pod_type == 'A':
                    if 'left' in self.name:
                        self.colour = doorcolourdic[pod.door_type[0]]
                    elif 'top' in self.name:
                        self.colour = doorcolourdic[pod.door_type[1]]
                    elif 'right' in self.name:
                        self.colour = doorcolourdic[pod.door_type[2]]
                    elif 'bottom' in self.name:
                        self.colour = doorcolourdic[pod.door_type[3]]
                elif pod.id == self.id and pod.pod_type == 'B':
                    if 'top' in self.name:
                        self.colour = doorcolourdic[pod.door_type[0]]
                    elif 'bottom' in self.name:
                        self.colour = doorcolourdic[pod.door_type[1]]
    def drawdoor(self):
        pygame.draw.rect(screen,self.colour,self.position)

# Making circles to draw the pods
pods_to_draw = [Circle('living_quarters_background',colour,(600,500),190,0),Circle('living_quarters_outline',black,(600,500),190,5),Circle('connecting_corridor_background',colour, (980, 500), 190, 0),Circle('connecting_corridor_outline',black, (980, 500), 190, 5),Circle('Engineering_background',colour, (1360, 500), 190, 0),Circle('Engineering_outline',black, (1360, 500), 190, 5),Circle('food_production_background',black, (980, 500), 100, 5),Circle('food_production_outline',colour, (980, 215), 100, 0),Circle('life_support_background',black, (980, 215), 100, 5),Circle('life_support_outline',colour, (980, 785), 100, 0),Circle('comms_and_control_centre_background',colour, (980, 785), 100, 0),Circle('comms_and_control_centre_outline',black, (980, 785), 100, 5),Circle('bio-research_background',colour, (1360, 215), 100, 0),Circle('bio-research_outline',black, (1360, 215), 100, 5),Circle('storage_(external)_background',colour, (200, 800), 100, 0),Circle('storage_(external)_outline',black, (200, 800), 100, 5),Circle('emergency_quarters_background',colour,(200, 200), 100, 0),Circle('emergency_quarters_outline',black,(200, 200), 100, 5)]

# Making the doors
doors_to_draw = [Door(1,'living_quarters_left_door',doorcolour,(410,425,30,150)),Door(1,'living_quarters_top_door',doorcolour,(525,300,150,30)),Door(1,'living_quarters_right_door',doorcolour,(780,425,30,150)),Door(1,'living_quarters_bottom_door',doorcolour,(525,670,150,30))]

test = False
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
    if x <=0:
        x = 0
    elif x >= 1550:
        x = 1550
    if y <=0:
        y = 0
    elif y >= 950:
        y = 950


    if keys[pygame.K_a]:
        x2 -= vel
    if keys[pygame.K_d]:
        x2 += vel
    if keys[pygame.K_w]:
        y2 -= vel
    if keys[pygame.K_s]:
        y2 += vel
    if x2 <=0:
        x2 = 0
    elif x2 >= 1550:
        x2 = 1550
    if y2 <=0:
        y2 = 0
    elif y2 >= 950:
        y2 = 950

    screen.fill((255,153,102))  # Fills the screen with black
    surface = pygame.image.load('images/surface.png')
    screen.blit(surface,(0,0))

    for pod in pods_to_draw:
        if pod.id == 'living_quarters_background':
            if test:
                pod.colour = lightgrey
            else:
                pod.colour = colour
        Circle.drawcircle(pod)

    for door in doors_to_draw:
        if door.id == 'living_quarters_left_door':
            if test:
                door.colour = open
            else:
                door.colour = closed
        Door.drawdoor(door)

    astronaut(x,y)
    astronaut(x2,y2)
    # [yxis,xxis,width,height]
    if y > 350 and y < 590 and x > 350 and x < 440 and keys[pygame.K_e]:
        test = not test
    if y2 > 350 and y2 < 590 and x2 > 350 and x2 < 440 and keys[pygame.K_e]:
        test = not test


    pygame.display.update()

pygame.quit()
