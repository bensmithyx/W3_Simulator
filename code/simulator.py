import pygame, time, simulator

class Pod:
    def __init__(self, id, name, connecting_rooms, door_types, internal_pod, position, side_to_attach_door, orientation):
        self.pos = (0,0)
        self.side_to_attach_door = side_to_attach_door
        self.position = position
        self.orientation = orientation
        self.id = id
        self.name = name
        self.connecting_rooms = connecting_rooms
        self.door_types = door_types
        self.internal_pod = internal_pod
        self.colour = podcolour
        self.door_height = 100
        self.door_width = self.door_height/5
        # Checking if there is a pod within another one if there is it will add the connecting_rooms so it knows how to get to the pod
        if len(self.internal_pod):
            self.internal_top_door = internal_pod[0]
            self.internal_bottom_door = internal_pod[0]
        # If the pod is of type A it will assign the where the connecting_rooms lead to the variables so we can make a path to it
        if len(self.connecting_rooms) == 4:
            self.pod_type = 'A'
            self.radius = 190
            self.leftdoor = connecting_rooms[0]
            self.topdoor = connecting_rooms[1]
            self.rightdoor = connecting_rooms[2]
            self.bottomdoor = connecting_rooms[3]
        # If the pod is of type B it will assign where the connecting_rooms lead to the variables so we can make a path to it
        elif len(self.connecting_rooms) == 2:
            self.radius = 100
            self.pod_type = 'B'
            self.topdoor = connecting_rooms[0]
            self.bottomdoor = connecting_rooms[1]
        else:
            self.pod_type = 'unknown'

    def __repr__(self):
        # Shows the internal connecting_rooms (when a pod is inside another)
        show_internal_connecting_rooms = f"{f'Internal Top Door ({self.door_types[0]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n{f'Internal Bottom Door ({self.door_types[1]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n"
        # Depedending on the type is will display the pods attributes
        if self.pod_type == 'A':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nLeft Door ({self.door_types[0]}) = {self.leftdoor}\nTop Door ({self.door_types[1]}) = {self.topdoor}\nRight Door ({self.door_types[2]}) = {self.rightdoor}\nBottom Door ({self.door_types[3]}) = {self.bottomdoor}\n{show_internal_connecting_rooms if self.internal_pod else ''}"
        elif self.pod_type == 'B':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nTop Door ({self.door_types[0]}) = {self.topdoor}\nBottom Door ({self.door_types[1]}) = {self.bottomdoor}\n"

    def drawpod(self):
        if isinstance(self.position,tuple):
            self.pos = self.position
        else:
            # Checks which side of the existing pod the new pod is to be added to and finds the x,y cords for the new pod
            for pod in pods:
                if pod.id == self.position:
                    if 'left' == self.side_to_attach_door:
                        self.pos = (pod.pos[0]-pod.radius-self.radius,pod.pos[1])
                    elif 'top' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1]-pod.radius-self.radius)
                    elif 'right' == self.side_to_attach_door:
                        self.pos = (pod.pos[0]+pod.radius+self.radius,pod.pos[1])
                    elif 'bottom' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1]+pod.radius+self.radius)
                    elif 'center' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1])
        # Background of circle
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, 0)
        # Outline of circle
        pygame.draw.circle(screen, (0,0,0), self.pos, self.radius, 5)

        # Adds doors colours based on what type of door it is
        doorcolourdic = {'empty':(0,0,0),'normal':doorcolour,'airlock':lightblue}

        if self.orientation == 'left' or self.pod_type == 'A':
            # Left door
            pygame.draw.rect(screen,doorcolourdic[self.door_types[0]],(self.pos[0]-(self.radius+(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))
            # Right door
            pygame.draw.rect(screen,doorcolourdic[self.door_types[1]],(self.pos[0]+(self.radius-(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))

        if self.orientation == 'top' or self.pod_type == 'A':
            if self.pod_type == 'A':
                index1, index2 = 2, 3
            else:
                index1, index2 = 0, 1
            # Top door
            pygame.draw.rect(screen,doorcolourdic[self.door_types[index1]],(self.pos[0]-(self.door_height/2),self.pos[1]-(self.radius+(self.door_width/2)),self.door_height,self.door_width))
            # Bottom door
            pygame.draw.rect(screen,doorcolourdic[self.door_types[index2]],(self.pos[0]-(self.door_height/2),self.pos[1]+(self.radius-(self.door_width/2)),self.door_height,self.door_width))

class Astronaut:
    def __init__(self, id, x, y):
        self.id = id
        #self.PLD = PLD
        self.x = x
        self.y = y
        self.image = screen.blit(astronautImg,(x,y))

    def update_movement(self, xpos, ypos):
        self.image = screen.blit(astronautImg,(xpos,ypos))
        self.lastx = xpos
        self.lasty = ypos

pygame.init()

# Creating the screen
HEIGHT = 1600
WIDTH = 1000
screen = pygame.display.set_mode((HEIGHT, WIDTH))

# Changing the title
pygame.display.set_caption('Control Pannel')

# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

# Astronauts starting locations
x = 600
y = 475
vel = 30

# Colours
lightgrey = (170,170,170)
grey = (144,144,144)
colour = grey
doorcolour = (204,204,204)
open = (0,204,0)
closed = (153,0,0)
black = (0,0,0)
lightblue = (0,153,255)
podcolour = grey
# List of all the pods if a new one is to be added it can be done here
pods = [
        Pod(1,'Bio-Research',['outside','Engineering Workshop/Mining Operations/Storage'],['empty','airlock'],[],8,'bottom','top'),
        Pod(2,'Food Production',['empty','Connecting Corridor'],['empty','normal'],[],7,'bottom','top'),
        Pod(3,'Life Support/Power Plant/Recycling',['Connecting Corridor','outside'],['normal','airlock'],[],7,'top','top'),
        Pod(4,'Storage (External)',['outside','empty'],['airlock','empty'],[],(200, 800),'','top'),
        Pod(5,'Emergency Quarters',['empty','empty','empty','outside'],['empty','empty','empty','airlock'],[],(220, 250),'',''),
        Pod(6,'Living Quarters',['outside','empty','Connecting Corridor','empty'],['airlock','empty','normal','empty'],[],(600,500),'',''),
        Pod(7,'Connecting Corridor',['Living Quarters','Food Production','Engineering Workshop/Mining Operations/Storage','Life Support/Power Plant/Recycling'],['normal','normal','normal','normal'],['Comms And Control Centre'],6,'right',''),
        Pod(8,'Engineering Workshop/Mining Operations/Storage',['Connecting Corridor','Bio-Research','outside','empty'],['normal','airlock','airlock','empty'],[],7,'right',''),
        Pod(9,'Comms And Control Centre',['Connecting Corridor','Connecting Corridor'],['normal','normal'],[],7,'center','left'),
        ## Test pods to add to spacestation
        #Pod(10,'New Pod',['Living Quarters','outside'],['airlock','normal'],[],6,'top','top')]
        #Pod(11,'New Pod',['Living Quarters','outside'],['normal','airlock'],[],6,'center','left')]

# Finds the index of a certain pod based on it's name
def index(source):
    for i in range(0,len(pods)):
        if pods[i].name == source:
            return i

# Function to find the path from a source location to a target location
def findpath(source, target, newplace, path):
    path = path
    if not newplace:
        # Moves source location to start of array so that is the pod we are starting from
        pods.insert(0, pods.pop(index(source)))
    i = newplace
    # Checking if the target pod is attached to current pod
    if target in pods[i].connecting_rooms+pods[i].internal_pod:
        path.append(pods[i].name)
        path.append(target)
        return path
    else:
        path.append(pods[i].name)
        for door in pods[i].connecting_rooms+pods[i].internal_pod:
            # If the door has not been searched yet and it is not leading outside or empty it will re run the function to check all of that pods doors for the target
            if door not in ['empty','outside'] and door not in path:
                newplace = index(door)
                result =  findpath(source, target, newplace, path)
                if result == None:
                    del path[-1]
                else: return result

# Locks all doors in a given pod
def lockdown(pod):
    [print(f'\nLocking {door} door\n') if door != 'empty' else '' for door in pods[index(pod)].door_type]

# Making Astronauts
astronautImg = pygame.image.load('images/64astro.png')
astronauts = [Astronaut(1,x,y),Astronaut(2,820,490),Astronaut(3,1350,475)]
active_astronaut = 1
test = False
firsttime = False
run = True
while run:
    pygame.time.delay(100)
    # Check which key has been pressed
    keys = pygame.key.get_pressed()
    # Chaing the pos of the astronaut based on keypresses
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        x -= vel
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        x += vel
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        y -= vel
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        y += vel
    # Stops astronauts from going outside of the screen
    if x <=0: x = 0
    elif x >= 1550: x = 1550

    if y <=0: y = 0
    elif y >= 950: y = 950

    # Fills the screen just in case image doesn't load
    screen.fill((255,153,102))
    surface = pygame.image.load('images/surface.png')
    # Adding background image to screen
    screen.blit(surface,(0,0))

    # Draws the pods to the screen
    [pod.drawpod() for pod in pods]

    # Moves selected astronaut around the screen and keeps the others still
    for astronaut in astronauts:
        if active_astronaut == astronaut.id:
            if firsttime:
                try:
                    x, y = astronaut.lastx, astronaut.lasty
                except:
                    x, y = astronaut.x, astronaut.y
                firsttime = False
            astronaut.update_movement(x,y)
        else:
            try:
                astronaut.update_movement(astronaut.lastx,astronaut.lasty)
            except:
                astronaut.update_movement(astronaut.x,astronaut.y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            # Get position of mouse when mousebutton is clicked
            pos = pygame.mouse.get_pos()
            for astronaut in astronauts:
                if astronaut.image.collidepoint(pos):
                    # Setting which astronaut is to be moved using their id
                    print(astronaut.id)
                    active_astronaut = astronaut.id
                    firsttime = True

    # [yxis,xxis,width,height]
    if y > 350 and y < 590 and x > 350 and x < 440 and keys[pygame.K_e]:
        test = not test
    pygame.display.update()

pygame.quit()
