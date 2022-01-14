import pygame, os
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
        self.rightdoorstate = False
        self.leftdoorstate = False
        self.topdoorstate = False
        self.bottomdoorstate = False
        # Adds doors colours based on what type of door it is
        self.doorcolourdic = {'empty':(0,0,0),'normal':doorcolour,'airlock':lightblue}
        self.opendoorcolourdic = {'empty':(0,0,0),'normal':(0,255,0),'airlock':(0,255,0)}

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
        self.topdoorpos = (self.pos[0]-(self.door_height/2),self.pos[1]-(self.radius+(self.door_width/2)),self.door_height,self.door_width)
        self.bottomdoorpos = (self.pos[0]-(self.door_height/2),self.pos[1]+(self.radius-(self.door_width/2)),self.door_height,self.door_width)
        # Positions of the left and right doors
        self.leftdoorpos = self.pos[0]-(self.radius+(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height
        self.rightdoorpos = self.pos[0]+(self.radius-(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height

    def __repr__(self):
        # Shows the internal connecting_rooms (when a pod is inside another)
        show_internal_connecting_rooms = f"{f'Internal Top Door ({self.door_types[0]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n{f'Internal Bottom Door ({self.door_types[1]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n"
        # Depedending on the type is will display the pods attributes
        if self.pod_type == 'A':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nLeft Door ({self.door_types[0]}) = {self.leftdoor}\nTop Door ({self.door_types[1]}) = {self.topdoor}\nRight Door ({self.door_types[2]}) = {self.rightdoor}\nBottom Door ({self.door_types[3]}) = {self.bottomdoor}\n{show_internal_connecting_rooms if self.internal_pod else ''}"
        elif self.pod_type == 'B':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nTop Door ({self.door_types[0]}) = {self.topdoor}\nBottom Door ({self.door_types[1]}) = {self.bottomdoor}\n"

    def closedoor(self, door_to_close):
        if self.pod_type == 'A':
            index1, index2 = 0, 2
        else:
            index1, index2 = 0, 1
        if self.orientation == 'left' or self.pod_type == 'A':
            if door_to_close == 'left':
                # Left door
                pygame.draw.rect(screen,self.doorcolourdic[self.door_types[index1]],(self.pos[0]-(self.radius+(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))
            elif door_to_close == 'right':
                # Right door
                pygame.draw.rect(screen,self.doorcolourdic[self.door_types[index2]],(self.pos[0]+(self.radius-(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))
        if self.orientation == 'top' or self.pod_type == 'A':
            if self.pod_type == 'A':
                index1, index2 = 1, 3
            else:
                index1, index2 = 0, 1
            if door_to_close  == 'top':
                # Top door
                pygame.draw.rect(screen,self.doorcolourdic[self.door_types[index1]],(self.pos[0]-(self.door_height/2),self.pos[1]-(self.radius+(self.door_width/2)),self.door_height,self.door_width))
            elif door_to_close == 'bottom':
                # Bottom door
                pygame.draw.rect(screen,self.doorcolourdic[self.door_types[index2]],(self.pos[0]-(self.door_height/2),self.pos[1]+(self.radius-(self.door_width/2)),self.door_height,self.door_width))

    def opendoor(self, door_to_open):
        if self.pod_type == 'A':
            index1, index2 = 0, 2
        else:
            index1, index2 = 0, 1
        if self.orientation == 'left' or self.pod_type == 'A':
            if door_to_open == 'left':
                # Left door
                self.leftdoordraw = pygame.draw.rect(screen,self.opendoorcolourdic[self.door_types[index1]],(self.pos[0]-(self.radius+(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))
            elif door_to_open == 'right':
                # Right door
                pygame.draw.rect(screen,self.opendoorcolourdic[self.door_types[index2]],(self.pos[0]+(self.radius-(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height))
        if self.orientation == 'top' or self.pod_type == 'A':
            if self.pod_type == 'A':
                index1, index2 = 1, 3
            else:
                index1, index2 = 0, 1
            if door_to_open  == 'top':
                # Top door
                pygame.draw.rect(screen,self.opendoorcolourdic[self.door_types[index1]],(self.pos[0]-(self.door_height/2),self.pos[1]-(self.radius+(self.door_width/2)),self.door_height,self.door_width))
            elif door_to_open == 'bottom':
                # Bottom door
                pygame.draw.rect(screen,self.opendoorcolourdic[self.door_types[index2]],(self.pos[0]-(self.door_height/2),self.pos[1]+(self.radius-(self.door_width/2)),self.door_height,self.door_width))

    def drawpod(self, x,y):
        if isinstance(self.position,tuple):
            self.pos = self.position
        else:
            # Checks which side of the existing pod the new pod is to be added to and finds the x,y cords for the new pod
            for pod in pods:
                if pod.id == self.position:
                    if 'left' == self.side_to_attach_door:
                        self.pos = (pod.pos[0]-pod.radius-self.radius+5,pod.pos[1])
                    elif 'top' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1]-pod.radius-self.radius+5)
                    elif 'right' == self.side_to_attach_door:
                        self.pos = (pod.pos[0]+pod.radius+self.radius-5,pod.pos[1])
                    elif 'bottom' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1]+pod.radius+self.radius-5)
                    elif 'center' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1])
        # Background of circle
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, 0)
        # Outline of circle
        pygame.draw.circle(screen, (0,0,0), self.pos, self.radius, 5)


class Astronaut(pygame.sprite.Sprite):
    def __init__(self, id, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.health = 100
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.id = id
        self.switch = True
        # Index 0 is IDLE animations
        animation_types = ['astronautidle', 'astronautrunning','astronautdead','astronautrunningdown','astronautrunningup']
        for animation in animation_types:
            temp_list = []
            number_of_frames = len(os.listdir(f'images/{animation}'))
            for image in range(number_of_frames):
                astronautImg = pygame.image.load(f'images/{animation}/{image}.png')
                astronautImg = pygame.transform.scale(astronautImg, (int(astronautImg.get_width()*scale), int(astronautImg.get_height()*scale)))
                temp_list.append(astronautImg)
            self.animation_list.append(temp_list)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.speed = 0
            self.update_action(2)

    def move(self):
        # Reset movment variables
        dx = 0
        dy = 0
        check = False
        check1 = False
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if moving_up:
            dy = -self.speed
        if moving_down:
            dy = self.speed

        # Stop astronaut from going off screen
        if self.rect.bottom + dy > 1000:
            dy = 1000 - self.rect.bottom
        if self.rect.top + dy < 0:
            dy = 0 + self.rect.top
        if self.rect.left + dx < 0:
            dx = 0 + self.rect.left
        if self.rect.right + dx > 1600:
            dx = 1600 - self.rect.right

        if self.switch:
            # Checks if astronaut is in pod walls
            for pod in pods:
                if inside_pod(self.rect.centerx+dx, self.rect.centery+dy, pod.pos[0], pod.pos[1], pod.radius):
                    check = True
                    break

        elif not self.switch:
            # Checks if astronaut is in pod walls
            for pod in pods:
                if inside_pod(self.rect.centerx+dx, self.rect.centery+dy, pod.pos[0], pod.pos[1], pod.radius):
                    check = False
                    break
                else:
                    check = True

        # Gets the positions of all the airlock doors so it can check if a astronaut is trying to get to one
        airlock_door_positions = []
        for pod in pods:
            if pod.pod_type == 'A':
                for index, door in enumerate([pod.leftdoorpos,pod.topdoorpos,pod.rightdoorpos,pod.bottomdoorpos]):
                    if pod.door_types[index] == 'airlock' and pod.connecting_rooms[index] == 'outside':
                            airlock_door_positions.append(door)

            elif pod.pod_type == 'B':
                if pod.door_types[0] == 'airlock' and pod.connecting_rooms[0] == 'outside':
                    try:
                        airlock_door_positions.append(pod.leftdoorpos)
                    except:
                        airlock_door_positions.append(pod.topdoorpos)
                elif pod.door_types[1] == 'airlock' and pod.connecting_rooms[1] == 'outside':
                    try:
                        airlock_door_positions.append(pod.rightdoorpos)
                    except:
                        airlock_door_positions.append(pod.bottomdoorpos)

        # Checks if astronaut is at an airlock door and wants to open it to get outside
        for pos in airlock_door_positions:
            if self.rect.colliderect(pos) and trigger_door:
                check = True
                check1 = True

        if check1:
            self.switch = not self.switch

        if kill:
            self.health = 0

        if check:
            # Update rectangle position
            self.rect.x += dx
            self.rect.y += dy
            self.PLD = (self.rect.x,self.rect.y)

    def update_animation(self):
        cooldown = 100
        # Update image depending on current frame
        self.image = self.animation_list[self.action][self.frame_index]
        # Check if enough time has past since last update
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        # If the animation list runs out then loop back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            # If action is 2 (death) don't loop animation
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # Checks if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Checks if player is inside a certain pod
def inside_pod(x, y, centerx, centery, radius):
    if (x - centerx)**2 + (y - centery)**2 < radius**2:
        return True
    else:
        return False

# Checks if player is outside a pod
def outside_pod(x, y, centerx, centery, radius):
    if (x - centerx)**2 + (y - centery)**2 > radius**2:
        return True
    else:
        return False

def checkcollided(x1,y1, x2, y2):
    distance = ((x2-x1)**2 + (y2-y1)**2)**0.5
    if distance < 50:
        return True
    else:
        return False

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
def lockdown(name):
    for pod in pods:
        if pod.name == name:
            [pod.closedoor(x) for x in ['left','right','top','bottom']]


def draw_background():
    # Fills the screen just in case image doesn't load
    screen.fill((255,153,102))
    # Adding background image to screen
    screen.blit(surface,(0,0))

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
        Pod(1,'Bio-Research',['outside','Engineering Workshop/Mining Operations/Storage'],['empty','airlock'],[],8,'top','top'),
        Pod(2,'Food Production',['outside','Connecting Corridor'],['empty','normal'],[],7,'top','top'),
        Pod(3,'Life Support/Power Plant/Recycling',['Connecting Corridor','outside'],['normal','airlock'],[],7,'bottom','top'),
        Pod(4,'Storage (External)',['outside','outisde'],['airlock','empty'],[],(200, 800),'','top'),
        Pod(5,'Emergency Quarters',['outside','outside','outside','outside'],['empty','empty','empty','airlock'],[],(220, 250),'',''),
        Pod(6,'Living Quarters',['outside','outside','Connecting Corridor','outside'],['airlock','empty','normal','empty'],[],(600,500),'',''),
        Pod(7,'Connecting Corridor',['Living Quarters','Food Production','Engineering Workshop/Mining Operations/Storage','Life Support/Power Plant/Recycling'],['normal','normal','normal','normal'],['Comms And Control Centre'],6,'right',''),
        Pod(8,'Engineering Workshop/Mining Operations/Storage',['Connecting Corridor','Bio-Research','outside','outside'],['normal','airlock','airlock','empty'],[],7,'right',''),
        Pod(9,'Comms And Control Centre',['Connecting Corridor','Connecting Corridor'],['normal','normal'],[],7,'center','left')]
        ## Test pods to add to spacestation
        #Pod(10,'New Pod',['Living Quarters','outside'],['airlock','normal'],[],6,'top','top')]
        #Pod(11,'New Pod',['Living Quarters','outside'],['normal','airlock'],[],6,'center','left')]

pygame.init()
# Creating the screen 1600
WIDTH = 1000
HEIGHT = int(WIDTH*1.6)
screen = pygame.display.set_mode((HEIGHT, WIDTH))

# Changing the title
pygame.display.set_caption('Space Station Simulator')
# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

# Making Astronauts
astronauts = [Astronaut(0,600,475,2,3.5),Astronaut(1,820,490,2,3.5),Astronaut(2,1350,475,2,3.5)]

# Background Image
surface = pygame.image.load('images/surface.png')

clock = pygame.time.Clock()
FPS = 60

moving_left = False
moving_right = False
moving_up = False
moving_down = False
trigger_door = False
kill = False
active_astronaut = 0
run = True

while run:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    draw_background()

    # x,y cords of selected astronaut
    x, y = astronauts[active_astronaut].rect.centerx, astronauts[active_astronaut].rect.centery

    # Draws the pods to the screen
    [pod.drawpod(x,y) for pod in pods]

    for pod in pods:
        if pod.orientation == 'left' or pod.pod_type == 'A':
            if pod.pod_type == 'A':
                index1, index2 = 0, 2
            else:
                index1, index2 = 0, 1
            # Positions of the left and right doors
            pod.leftdoorpos = pod.pos[0]-(pod.radius+(pod.door_width/2)),pod.pos[1]-(pod.door_height/2),pod.door_width,pod.door_height
            pod.rightdoorpos = pod.pos[0]+(pod.radius-(pod.door_width/2)),pod.pos[1]-(pod.door_height/2),pod.door_width,pod.door_height

            if keys[pygame.K_e]:
                if pod.connecting_rooms[index2] not in ['outside','empty']:
                    if checkcollided(pod.rightdoorpos[0],pod.rightdoorpos[1],x,y) and pod.leftdoorstate == False and pods[index(pod.connecting_rooms[index2])].rightdoorstate == False:
                        pod.rightdoorstate = not pod.rightdoorstate
                else:
                    if checkcollided(pod.rightdoorpos[0],pod.rightdoorpos[1],x,y) and pod.leftdoorstate == False:
                        pod.rightdoorstate = not pod.rightdoorstate
                if pod.connecting_rooms[index1] not in ['outside','empty']:
                    if checkcollided(pod.leftdoorpos[0],pod.leftdoorpos[1],x,y) and pod.rightdoorstate == False and pods[index(pod.connecting_rooms[index1])].leftdoorstate == False:
                        pod.leftdoorstate = not pod.leftdoorstate
                else:
                    if checkcollided(pod.leftdoorpos[0],pod.leftdoorpos[1],x,y) and pod.rightdoorstate == False:
                        pod.leftdoorstate = not pod.leftdoorstate

            if pod.connecting_rooms[index1] not in ['outside','empty']:
                pod.opendoor('left') if pod.leftdoorstate == True and pod.rightdoorstate == False and pods[index(pod.connecting_rooms[index1])].leftdoorstate == False else pod.closedoor('left')
            else:
                pod.opendoor('left') if pod.leftdoorstate == True and pod.rightdoorstate == False else pod.closedoor('left')
            if pod.connecting_rooms[index2] not in ['outside','empty']:
                    pod.opendoor('right') if pod.rightdoorstate == True and pod.leftdoorstate == False and pods[index(pod.connecting_rooms[index2])].rightdoorstate == False else pod.closedoor('right')
            else:
                pod.opendoor('right') if pod.rightdoorstate == True and pod.leftdoorstate == False else pod.closedoor('right')

        if pod.orientation == 'top' or pod.pod_type == 'A':
            if pod.pod_type == 'A':
                index1, index2 = 1, 3
            else:
                index1, index2 = 0, 1
                # Positions of the top and bottom doors
            pod.topdoorpos = (pod.pos[0]-(pod.door_height/2),pod.pos[1]-(pod.radius+(pod.door_width/2)),pod.door_height,pod.door_width)
            pod.bottomdoorpos = (pod.pos[0]-(pod.door_height/2),pod.pos[1]+(pod.radius-(pod.door_width/2)),pod.door_height,pod.door_width)

            if keys[pygame.K_e]:
                if pod.connecting_rooms[index1] not in ['outside','empty']:
                    if checkcollided(pod.topdoorpos[0],pod.topdoorpos[1],x,y) and pod.bottomdoorstate == False and pods[index(pod.connecting_rooms[index1])].topdoorstate == False:
                        pod.topdoorstate = not pod.topdoorstate
                else:
                    if checkcollided(pod.topdoorpos[0],pod.topdoorpos[1],x,y) and pod.bottomdoorstate == False:
                        pod.topdoorstate = not pod.topdoorstate
                if pod.connecting_rooms[index2] not in ['outside','empty']:
                    if checkcollided(pod.bottomdoorpos[0],pod.bottomdoorpos[1],x,y) and pod.topdoorstate == False and pods[index(pod.connecting_rooms[index2])].bottomdoorstate == False:
                        pod.bottomdoorstate = not pod.bottomdoorstate
                else:
                    if checkcollided(pod.bottomdoorpos[0],pod.bottomdoorpos[1],x,y) and pod.topdoorstate == False:
                        pod.bottomdoorstate = not pod.bottomdoorstate

            if pod.connecting_rooms[index1] not in ['outside','empty']:
                pod.opendoor('top') if pod.topdoorstate == True and pod.bottomdoorstate == False and pods[index(pod.connecting_rooms[index1])].topdoorstate == False else pod.closedoor('top')
            else:
                pod.opendoor('top') if pod.topdoorstate == True and pod.bottomdoorstate == False else pod.closedoor('top')
            if pod.connecting_rooms[index2] not in ['outside','empty']:
                pod.opendoor('bottom') if pod.bottomdoorstate == True and pod.topdoorstate == False and pods[index(pod.connecting_rooms[index2])].bottomdoorstate == False else pod.closedoor('bottom')
            else:
                pod.opendoor('bottom') if pod.bottomdoorstate == True and pod.topdoorstate == False else pod.closedoor('bottom')

    # Draws the astronauts to the screen
    [astronaut.draw() for astronaut in astronauts]

    # Updating selected astronauts movement
    astronauts[active_astronaut].update()
    astronauts[active_astronaut].draw()

    if astronauts[active_astronaut].alive:
        # Update astronauts[active_astronaut] actions
        if moving_left or moving_right:
            # 1 means running left or right
            astronauts[active_astronaut].update_action(1)
        elif moving_down:
            # 3 is running down
            astronauts[active_astronaut].update_action(3)
        elif moving_up:
            # 4 is runnig up
            astronauts[active_astronaut].update_action(4)
        else:
            # 0 means idle
            astronauts[active_astronaut].update_action(0)
        astronauts[active_astronaut].move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Keyboard keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_e:
                trigger_door = True
            if event.key == pygame.K_k:
                kill = True
        # Keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False
            if event.key == pygame.K_e:
                trigger_door = False
            if event.key == pygame.K_k:
                kill = False
        if event.type == pygame.MOUSEBUTTONUP:
            # Get position of mouse when mousebutton is clicked
            mouse_position = pygame.mouse.get_pos()
            for astronaut in astronauts:
                if astronaut.rect.collidepoint(mouse_position):
                    # Setting which astronaut is to be moved using their id
                    active_astronaut = astronaut.id
    pygame.display.update()
pygame.quit()
