from typing import Tuple

import pygame, os, sys, random, time, scenario_gui
from pygame.locals import *

class Timer:
    def __init__(self, name, time, text, yxis):
        self.name = name
        self.time = time
        self.timetext = ''
        self.text = text
        self.yxis = yxis

    def display(self):
        screen.blit(font.render(self.text+self.timetext, True, (0, 0, 0)), (1500, self.yxis))

class Emergency:
    def __init__(self, pods, fire, air_quality, radiation, bio_hazard):
        self.fire = fire
        self.fire = 0                 # TURN ON FIRE EVENT #####IMPORTANT###
        self.air_quality = air_quality
        self.radiation = radiation
        self.bio_hazard = bio_hazard
        self.fire_supress = 0
        self.bio_supress = 0
        self.radiation_supress = 0
        self.ealarm = 0
        self.bio_hazard = 0
        self.bioalarm = 0
        self.radiation_hazard = 0
        self.radiationalarm = 0
        self.airalarm = 0
        self.air_quality_hazard = 1
        self.air_quality_suppress = 0

    def alarm(self, podname):
        #alarm_sound = pygame.mixer.Sound('sound/e_alarm.wav')

        if self.ealarm == 1:
            for timer in clocks:
                if timer.name == 'acms_20delay':
                    if timer.time == 0:
                        #alarm_sound.play()
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = red
                                lockdown(podname)

    def biobasealarm(self, podname):
        alarm_sound = pygame.mixer.Sound('sound/e_alarm.wav')

        if self.bioalarm == 1:
            for timer in clocks:
                if timer.name == 'bio_time':
                    if timer.time < 25:
                        alarm_sound.play()
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = red
                                lockdown(podname)

    def air_quality_alarm(self, podname):
       # alarm_sound = pygame.mixer.Sound('sound/e_alarm.wav')

        if self.airalarm == 1:
            for timer in clocks:
                if timer.name == 'air_time':
                    if timer.time < 25:
                       # alarm_sound.play()
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = red
                                lockdown(podname)

    def radiationbasealarm(self, podname):
       # alarm_sound = pygame.mixer.Sound('sound/e_alarm.wav')

        if self.radiationalarm == 1:
            for timer in clocks:
                if timer.name == 'radiation_time':
                    if timer.time < 25:
                       # alarm_sound.play()
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = red
                                lockdown(podname)

    def fire_event(self, podname):

        if self.fire == 1:
            for timer in clocks:
                if timer.name == 'acms_20delay':
                    self.ealarm = 1
                    self.alarm(podname)
                    if timer.time == 0:
                        self.fire_supress = 1
                        self.fire = 0
                        self.ealarm = 0

        if self.fire_supress == 1:
            for timer in clocks:
                if timer.name == 'fire':
                    if timer.time < 5:
                        self.fire_supress = 0
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = lightgrey

        for timer in clocks:
            if timer.name == 'fire':
                if timer.time == 0:
                    for pod in pods:
                        if pod.name == podname:
                            unlockdown(podname)


    def air_quality_event(self, podname):
        if self.air_quality_hazard == 1:
            for timer in clocks:
                if timer.name == 'air_time':
                    if timer.time < 15:
                        self.airalarm = 1
                        self.air_quality_alarm(podname)
                        if timer.time < 10:
                            self.air_quality_suppress = 1
                            self.air_quality_hazard = 0
                            self.airalarm = 0

        if self.air_quality_suppress == 1:
            for timer in clocks:
                if timer.name == 'air_time':
                    if timer.time < 5:
                        self.air_quality_suppress = 0
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = lightgrey

        for timer in clocks:
            if timer.name == 'air_time':
                if timer.time == 0:
                    for pod in pods:
                        if pod.name == podname:
                            unlockdown(podname)


    def bio_hazard_event(self, podname):

        if self.bio_hazard == 1:
            for timer in clocks:
                if timer.name == 'bio_time':
                    if timer.time < 15:
                        self.bioalarm = 1
                        self.biobasealarm(podname)
                        if timer.time < 10:
                            self.bio_supress = 1
                            self.bio_hazard = 0
                            self.bioalarm = 0


        if self.bio_supress == 1:
            for timer in clocks:
                if timer.name == 'bio_time':
                    if timer.time < 5:
                        self.bio_supress = 0
                        self.bioalarm = 0
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = lightgrey

        for timer in clocks:
            if timer.name == 'bio_time':
                if timer.time == 0:
                    for pod in pods:
                        if pod.name == podname:
                            unlockdown(podname)

    def radiation_event(self, podname):
        if self.radiation_hazard == 1:
            for timer in clocks:
                if timer.name == 'radiation_time':
                    if timer.time < 15:
                        self.radiationalarm = 1
                        self.radiationbasealarm(podname)
                        if timer.time < 10:
                            self.radiation_supress = 1
                            self.radiation_hazard = 0
                            self.radiationalarm = 0

        if self.radiation_supress == 1:
            for timer in clocks:
                if timer.name == 'radiation_time':
                    if timer.time < 5:
                        self.radiation_supress = 0
                        for pod in pods:
                            if pod.name == podname:
                                pod.colour = lightgrey

        for timer in clocks:
            if timer.name == 'radiation_time':
                if timer.time == 0:
                    for pod in pods:
                        if pod.name == podname:
                            unlockdown(podname)


class Doors():
    def __init__(self, pod_names):
        self.pod_names = pod_names
        self.lockdown = False

    def draw(self, pivot, angle, doorcolour):
        self.pivot = pivot
        self.angle = angle
        self.doorcolour = doorcolour
        if self.lockdown:
            self.doorcolour = closed
        # The original image will never be modified.
        IMAGE = pygame.Surface((140, 60), pygame.SRCALPHA)
        pygame.draw.rect(IMAGE, self.doorcolour, (20, 28, 50, 5))
        # This offset vector will be added to the pivot point, so the
        # resulting rect will be blitted at `rect.topleft + offset`.
        offset = pygame.math.Vector2(50, 0)
        # Rotated version of the image and the shifted rect.
        rotated_image, rect = rotate(IMAGE, self.angle, self.pivot, offset)
        screen.blit(rotated_image, rect)
        #pygame.draw.circle(screen, (30, 250, 70), pivot, 3)
        return self.angle

class Pod():
    def __init__(self, id, name, connecting_rooms, door_types, internal_pod, position, side_to_attach_door, orientation):
        self.dooradjustment = 0
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
        self.door_height = 60/scale
        self.door_width = (self.door_height/8)/scale
        self.rightdoorstate = False
        self.leftdoorstate = False
        self.topdoorstate = False
        self.bottomdoorstate = False
        # Adds doors colours based on what type of door it is
        self.doorcolourdic = {'empty':(0,0,0),'normal':doorcolour,'airlock':lightblue,'fakeairlock':lightblue}
        self.opendoorcolourdic = {'empty':(0,0,0),'normal':open,'airlock':lightblue,'fakeairlock':lightblue}
        self.leftangle = 90
        self.rightangle = 90
        self.topangle = 0
        self.bottomangle = 0

        # Checking if there is a pod within another one if there is it will add the connecting_rooms so it knows how to get to the pod
        if len(self.internal_pod):
            self.internal_top_door = internal_pod[0]
            self.internal_bottom_door = internal_pod[0]
        # If the pod is of type A it will assign the where the connecting_rooms lead to the variables so we can make a path to it
        if len(self.connecting_rooms) == 4:
            self.pod_type = 'A'
            self.radius = 190/scale
            self.leftdoor_pod = connecting_rooms[0]
            self.topdoor_pod = connecting_rooms[1]
            self.rightdoor_pod = connecting_rooms[2]
            self.bottomdoor_pod = connecting_rooms[3]
        # If the pod is of type B it will assign where the connecting_rooms lead to the variables so we can make a path to it
        elif len(self.connecting_rooms) == 2:
            if 'airlock' in self.name:
                self.radius = 60/scale
                self.pod_type = 'C'
                self.colour = '#EDFEFF'
            else:
                self.radius = 100/scale
                self.pod_type = 'B'
            self.topdoor_pod = connecting_rooms[0]
            self.bottomdoor_pod = connecting_rooms[1]
            self.leftdoor_pod = connecting_rooms[0]
            self.rightdoor_pod = connecting_rooms[1]
        else:
            self.pod_type = 'unknown'

        # Creating doors from class
        self.leftdoor = Doors([self.name,self.leftdoor_pod])
        self.rightdoor = Doors([self.name,self.rightdoor_pod])
        self.topdoor = Doors([self.name,self.topdoor_pod])
        self.bottomdoor = Doors([self.name,self.bottomdoor_pod])

    def __repr__(self):
        # Shows the internal connecting_rooms (when a pod is inside another)
        show_internal_connecting_rooms = f"{f'Internal Top Door ({self.door_types[0]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n{f'Internal Bottom Door ({self.door_types[1]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n"
        # Depedending on the type is will display the pods attributes
        if self.pod_type == 'A':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nLeft Door ({self.door_types[0]}) = {self.leftdoor_pod}\nTop Door ({self.door_types[1]}) = {self.topdoor_pod}\nRight Door ({self.door_types[2]}) = {self.rightdoor_pod}\nBottom Door ({self.door_types[3]}) = {self.bottomdoor_pod}\n{show_internal_connecting_rooms if self.internal_pod else ''}Connected to = {self.side_to_attach_door}\n"
        elif self.pod_type == 'B':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nTop Door ({self.door_types[0]}) = {self.topdoor_pod}\nBottom Door ({self.door_types[1]}) = {self.bottomdoor_pod}\nConnected to = {self.side_to_attach_door}\n"

    def closedoor(self, door_to_close):
        if self.orientation == 'left' or self.pod_type == 'A':
            if door_to_close == 'left':
                # Left door
                if self.leftangle < 90:
                    self.leftangle +=1
                else:
                    self.leftdoorstate = False
            elif door_to_close == 'right':
                # Right door
                if self.rightangle < 90:
                    self.rightangle +=1
                else:
                    self.rightdoorstate = False
        if self.orientation == 'top' or self.pod_type == 'A':
            if door_to_close  == 'top':
                # Top door
                if self.topangle > 0:
                    self.topangle -=1
                else:
                    self.topdoorstate = False
            elif door_to_close == 'bottom':
                # Bottom door
                if self.bottomangle > 0:
                    self.bottomangle -=1
                else:
                    self.bottomdoorstate = False

    def opendoor(self, door_to_open):
        if self.orientation == 'left' or self.pod_type == 'A':
            if door_to_open == 'left':
                if not self.leftdoor.lockdown:
                    if self.leftangle > 0:
                        self.leftangle -=1
                # Left door
            elif door_to_open == 'right':
                if not self.rightdoor.lockdown:
                    if self.rightangle > 0:
                        self.rightangle -=1
                # Right door
        if self.orientation == 'top' or self.pod_type == 'A':
            if door_to_open  == 'top':
                if not self.topdoor.lockdown:
                    if self.topangle < 90 :
                        self.topangle +=1
                # Top door
            elif door_to_open == 'bottom':
                if not self.bottomdoor.lockdown:
                    if self.bottomangle < 90:
                        self.bottomangle +=1
                # Bottom door

    def drawpod(self, x,y):
        if isinstance(self.position,tuple):
            self.pos = self.position
        else:
            # Checks which side of the existing pod the new pod is to be added to and finds the x,y cords for the new pod
            for pod in pods:
                if pod.id == self.position:
                    if 'left' == self.side_to_attach_door:
                        self.rightdoorstate = next((x for x in pods if x.name == self.rightdoor_pod), None).leftdoorstate
                        self.pos = (pod.pos[0]-pod.radius-self.radius+5,pod.pos[1])
                    elif 'right' == self.side_to_attach_door:
                        self.leftdoorstate = next((x for x in pods if x.name == self.leftdoor_pod), None).rightdoorstate
                        self.pos = (pod.pos[0]+pod.radius+self.radius-5,pod.pos[1])
                    elif 'top' == self.side_to_attach_door:
                        self.bottomdoorstate = next((x for x in pods if x.name == self.bottomdoor_pod), None).topdoorstate
                        self.pos = (pod.pos[0],pod.pos[1]-pod.radius-self.radius+5)
                    elif 'bottom' == self.side_to_attach_door:
                        self.topdoorstate = next((x for x in pods if x.name == self.topdoor_pod), None).bottomdoorstate
                        self.pos = (pod.pos[0],pod.pos[1]+pod.radius+self.radius-5)
                    elif 'center' == self.side_to_attach_door:
                        self.pos = (pod.pos[0],pod.pos[1])

        # Background of circle
        pygame.draw.circle(screen, self.colour, self.pos, self.radius, 0)
        # Outline of circle
        pygame.draw.circle(screen, (0,0,0), self.pos, self.radius, 5)

    def drawdoors(self):
        if self.orientation == 'left' or self.pod_type == 'A':
            if self.pod_type == 'A':
                index1, index2 = 0, 2
            else:
                index1, index2 = 0, 1
            self.leftdoorpos = self.pos[0]-(self.radius+(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height
            self.rightdoorpos = self.pos[0]+(self.radius-(self.door_width/2)),self.pos[1]-(self.door_height/2),self.door_width,self.door_height
            # Left door
            if self.side_to_attach_door != 'right' and self.door_types[index1] != 'empty':
                # Store the original center position of the surface.
                pivot = self.leftdoorpos[0]+self.dooradjustment,self.leftdoorpos[1]
                if self.leftangle != 90:
                    doorcolour = open
                else:
                    doorcolour = self.doorcolourdic[self.door_types[index1]]
                self.leftangle = self.leftdoor.draw(pivot, self.leftangle, doorcolour)

            # Right door
            if self.side_to_attach_door != 'left' and self.door_types[index2] != 'empty':
                pivot = [self.rightdoorpos[0]+self.dooradjustment,self.rightdoorpos[1]]
                if self.rightangle != 90:
                    doorcolour = open
                else:
                    doorcolour = self.doorcolourdic[self.door_types[index2]]
                self.rightangle = self.rightdoor.draw(pivot, self.rightangle, doorcolour)

        if self.orientation == 'top' or self.pod_type == 'A':
            if self.pod_type == 'A':
                index1, index2 = 1, 3
            else:
                index1, index2 = 0, 1
            self.topdoorpos = self.pos[0]-(self.door_height/2),self.pos[1]-(self.radius+(self.door_width/2)),self.door_height,self.door_width
            self.bottomdoorpos = self.pos[0]-(self.door_height/2),self.pos[1]+(self.radius-(self.door_width/2)),self.door_height,self.door_width
            # Positions of the left and right doors

            # Top door
            if self.side_to_attach_door != 'bottom' and self.door_types[index1] != 'empty':
                pivot = [self.topdoorpos[0]+self.dooradjustment,self.topdoorpos[1]]
                if self.topangle != 0:
                    doorcolour = open
                else:
                    doorcolour = self.doorcolourdic[self.door_types[index1]]
                self.topangle = self.topdoor.draw(pivot, self.topangle, doorcolour)

            # Bottom door
            if self.side_to_attach_door != 'top' and self.door_types[index2] != 'empty':
                pivot = [self.bottomdoorpos[0]+self.dooradjustment,self.bottomdoorpos[1]]
                if self.bottomangle != 0:
                    doorcolour = open
                else:
                    doorcolour = self.doorcolourdic[self.door_types[index2]]
                self.bottomangle = self.bottomdoor.draw(pivot, self.bottomangle, doorcolour)

class Astronaut(pygame.sprite.Sprite):
    def __init__(self, id, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = 2*int(scenario_gui.state.speed[0])
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
                DoorImg = pygame.image.load(f'images/{animation}/{image}.png')
                DoorImg = pygame.transform.scale(DoorImg, (int(DoorImg.get_width()*scale), int(DoorImg.get_height()*scale)))
                temp_list.append(DoorImg)
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
            if pod.pod_type == 'C':
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

def rotate(surface, angle, pivot, offset):
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

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
        if name in pod.leftdoor.pod_names:
            pod.leftdoor.lockdown = True
        if name in pod.rightdoor.pod_names:
            pod.rightdoor.lockdown = True
        if name in pod.topdoor.pod_names:
            pod.topdoor.lockdown = True
        if name in pod.bottomdoor.pod_names:
            pod.bottomdoor.lockdown = True

def unlockdown(name):
    for pod in pods:
        if name in pod.leftdoor.pod_names:
            pod.leftdoor.lockdown = False
        if name in pod.rightdoor.pod_names:
            pod.rightdoor.lockdown = False
        if name in pod.topdoor.pod_names:
            pod.topdoor.lockdown = False
        if name in pod.bottomdoor.pod_names:
            pod.bottomdoor.lockdown = False

def draw_background():
    # Fills the screen just in case image doesn't load
    screen.fill((255,153,102))
    # Adding background image to screen
    screen.blit(surface,(0,0))


def circle_surf(radius, color):  # cloudy view
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

def fire(podname):

    if fire1.fire == 1:

        for fireparticle1 in fireparticles1:
            fireparticle1[0][0] += fireparticle1[1][0]
            fireparticle1[0][1] += fireparticle1[1][1]
            fireparticle1[2] -= 0.2
            fireparticle1[1][1] += 0.2
            pygame.draw.circle(screen, (255, 0, 0), [int(fireparticle1[0][0]), int(fireparticle1[0][1])],
                               # respsonble for colour
                               int(fireparticle1[2]))
            if fireparticle1[2] <= 0:
                fireparticles1.remove(fireparticle1)


def firesupress(podname):
    if fire1.fire_supress == 1:

        for fireparticle in fireparticles:
            fireparticle[0][0] += fireparticle[1][0]
            fireparticle[0][1] += fireparticle[1][1]
            fireparticle[2] -= 0.2
            fireparticle[1][1] += 0.2

            radius = fireparticle[2] * 2
            screen.blit(circle_surf(radius, (255, 255, 255)),
                               (int(fireparticle[0][0] - radius), int(fireparticle[0][1] - radius)),
                               special_flags=BLEND_RGB_ADD)  # cloudy view
            if fireparticle[2] <= 0:
                fireparticles.remove(fireparticle)


def bio(podname):
    if bio1.bio_hazard == 1:

        for bioparticle1 in bioparticles1:
            bioparticle1[0][0] += bioparticle1[1][0]
            bioparticle1[0][1] += bioparticle1[1][1]
            bioparticle1[2] -= 0.2
            bioparticle1[1][1] += 0.2
            pygame.draw.circle(screen, (0, 255, 0), [int(bioparticle1[0][0]), int(bioparticle1[0][1])],
                               # respsonble for colour
                               int(bioparticle1[2]))
            if bioparticle1[2] <= 0:
                bioparticles1.remove(bioparticle1)


def biosupress(podname):
    if bio1.bio_supress == 1:

        for bioparticle in bioparticles:
            bioparticle[0][0] += bioparticle[1][0]
            bioparticle[0][1] += bioparticle[1][1]
            bioparticle[2] -= 0.2
            bioparticle[1][1] += 0.2

            radius = bioparticle[2] * 2
            screen.blit(circle_surf(radius, (255, 255, 255)),
                               (int(bioparticle[0][0] - radius), int(bioparticle[0][1] - radius)),
                               special_flags=BLEND_RGB_ADD)  # cloudy view
            if bioparticle[2] <= 0:
                bioparticles.remove(bioparticle)

def radiation(podname):
    if radiation1.radiation_hazard == 1:

        for radiationparticle1 in radiationparticles1:
            radiationparticle1[0][0] += radiationparticle1[1][0]
            radiationparticle1[0][1] += radiationparticle1[1][1]
            radiationparticle1[2] -= 0.2
            radiationparticle1[1][1] += 0.2
            pygame.draw.circle(screen, (128, 0, 128), [int(radiationparticle1[0][0]), int(radiationparticle1[0][1])],
                               # respsonble for colour
                               int(radiationparticle1[2]))
            if radiationparticle1[2] <= 0:
                radiationparticles1.remove(radiationparticle1)


def radiationsupress(podname):
    if radiation1.radiation_supress == 1:

        for radiationparticle in radiationparticles:
            radiationparticle[0][0] += radiationparticle[1][0]
            radiationparticle[0][1] += radiationparticle[1][1]
            radiationparticle[2] -= 0.2
            radiationparticle[1][1] += 0.2

            radius = radiationparticle[2] * 2
            screen.blit(circle_surf(radius, (255, 255, 255)),
                               (int(radiationparticle[0][0] - radius), int(radiationparticle[0][1] - radius)),
                               special_flags=BLEND_RGB_ADD)  # cloudy view
            if radiationparticle[2] <= 0:
                radiationparticles.remove(radiationparticle)

def air_quality(podname):
    if airquality1.air_quality_hazard == 1:

        for airqualityparticle1 in airqualityparticles1:
            airqualityparticle1[0][0] += airqualityparticle1[1][0]
            airqualityparticle1[0][1] += airqualityparticle1[1][1]
            airqualityparticle1[2] -= 0.2
            airqualityparticle1[1][1] += 0.2
            pygame.draw.circle(screen, (0, 64, 255), [int(airqualityparticle1[0][0]), int(airqualityparticle1[0][1])],
                               # respsonble for colour
                               int(airqualityparticle1[2]))
            if airqualityparticle1[2] <= 0:
                airqualityparticles1.remove(airqualityparticle1)


def air_quality_suppress_f(podname):
    if airquality1.air_quality_suppress == 1:

        for airqualityparticle in airqualityparticles:
            airqualityparticle[0][0] += airqualityparticle[1][0]
            airqualityparticle[0][1] += airqualityparticle[1][1]
            airqualityparticle[2] -= 0.2
            airqualityparticle[1][1] += 0.2

            radius = airqualityparticle[2] * 2
            screen.blit(circle_surf(radius, (255, 255, 255)),
                               (int(airqualityparticle[0][0] - radius), int(airqualityparticle[0][1] - radius)),
                               special_flags=BLEND_RGB_ADD)  # cloudy view
            if airqualityparticle[2] <= 0:
                airqualityparticles.remove(airqualityparticle)



print(scenario_gui.state.speed,scenario_gui.state.num_astros_arr,scenario_gui.state.timeline)
scale = 1.25
multiplier = 1
# Colours
lightgrey = (170, 170, 170)
grey = (144, 144, 144)
colour = grey
doorcolour = (220, 228, 228)
open = (0, 204, 0)
closed = (153, 0, 0)
black = (0, 0, 0)
lightblue = (0, 153, 255)
podcolour = lightgrey
red = (255, 0, 0)
# List of all the pods if a new one is to be added it can be done here
pods = [
        Pod(1,'Living Quarters',['airlock1','outside','Connecting Corridor','outside'],['fakeairlock','empty','normal','empty'],[],(550,450),'',''),
        Pod(2,'Connecting Corridor',['Living Quarters','Food Production','Engineering Workshop/Mining Operations/Storage','Life Support/Power Plant/Recycling'],['normal','normal','normal','normal'],['Comms And Control Centre'],1,'right',''),
        Pod(3,'Emergency Quarters',['outside','outside','outside','airlock4'],['empty','empty','empty','fakeairlock'],[],(220, 170),'',''),
        Pod(4,'Life Support/Power Plant/Recycling',['Connecting Corridor','airlock5'],['normal','fakeairlock'],[],2,'bottom','top'),
        Pod(5,'Food Production',['outside','Connecting Corridor'],['empty','normal'],[],2,'top','top'),
        Pod(6,'Engineering Workshop/Mining Operations/Storage',['Connecting Corridor','airlock3','airlock2','outside'],['normal','fakeairlock','fakeairlock','empty'],[],2,'right',''),
        Pod(7,'Bio-Research',['outside','airlock3'],['empty','fakeairlock'],[],12,'top','top'),
        Pod(8,'Storage (External)',['airlock5','outisde'],['fakeairlock','empty'],[],(200, 690),'','top'),
        Pod(9,'Comms And Control Centre',['Connecting Corridor','Connecting Corridor'],['normal','normal'],[],2,'center','left'),
        ## Test pods to add to spacestation
        Pod(10,'airlock1',['outside','Living Quarters'],['airlock','fakeairlock'],[],1,'left','left'),
        Pod(11,'airlock2',['Engineering Workshop/Mining Operations/Storage','outside'],['fakeairlock','airlock'],[],6,'right','left'),
        Pod(12,'airlock3',['Bio-Research','Engineering Workshop/Mining Operations/Storage'],['fakeairlock','fakeairlock'],[],6,'top','top'),
        Pod(13,'airlock4',['Emergency Quarters','outside'],['fakeairlock','airlock'],[],3,'bottom','top'),
        Pod(14,'airlock5',['outside','Storage (External)'],['airlock','fakeairlock'],[],8,'top','top'),
        Pod(15,'airlock5',['Life Support/Power Plant/Recycling','outside'],['fakeairlock','airlock'],[],4,'bottom','top')
        #Pod(11,'New Pod',['Living Quarters','outside'],['normal','airlock'],[],6,'center','left')
        ]

pygame.init()
# Creating the screen
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h))

# Changing the title
pygame.display.set_caption('Space Station Simulator')
# Adding icon
icon = pygame.image.load('images/space-station.png')
pygame.display.set_icon(icon)

# Making Astronauts
astronauts = [Astronaut(0,600,450,2/scale),Astronaut(1,820,450,2/scale),Astronaut(2,1350,450,2/scale),Astronaut(3,1100,445,2/scale)]

fire1 = Emergency(3, 1, 1, False, False)      #preset emergency allow for pod to go red
fire2 = Emergency(3, False, False, False, False)  #preset emergency allow for pod to go red
fire3 = Emergency(1, True, True, True, True)

bio1 = Emergency(5, 0, False, False, True)

radiation1 = Emergency(1, 1, False, False, True)

airquality1 = Emergency(1, 1, False, False, True)

clocks = [Timer('acms_20delay', 10, 'delay', 50), Timer('doors', 5, 'doors', 100), Timer('fire', 25, 'fire', 150),
          Timer('bio_time', 20, 'bio', 200), Timer('radiation_time', 20, 'radiation', 250), Timer('air_time', 20, 'air', 300)]


# Background Image
surface = pygame.image.load('images/surface.png')
surface = pygame.transform.scale(surface=surface, size=(info.current_w, info.current_h))
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
counter = 0

pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)
fireparticles = []
fireparticles1 = []
bioparticles = []
bioparticles1 = []
radiationparticles = []
radiationparticles1 = []
airqualityparticles = []
airqualityparticles1 = []

while run:


    counter +=1
    #for pod in pods:
    #    print(f'\nPod name = {pod.name}\nLeft state = {bcolors.WARNING if pod.leftdoorstate==True else bcolors.ENDC}{pod.leftdoorstate}{bcolors.ENDC}\nRight state = {bcolors.WARNING if pod.rightdoorstate==True else bcolors.ENDC}{pod.rightdoorstate}{bcolors.ENDC}\nTop state = {bcolors.WARNING if pod.topdoorstate==True else bcolors.ENDC}{pod.topdoorstate}{bcolors.ENDC}\nBottom State = {bcolors.WARNING if pod.bottomdoorstate==True else bcolors.ENDC}{pod.bottomdoorstate}{bcolors.ENDC}')
    clock.tick(FPS)
    keys = pygame.key.get_pressed()
    draw_background()

    # x,y cords of selected astronaut
    x, y = astronauts[active_astronaut].rect.centerx, astronauts[active_astronaut].rect.centery

    # Draws the pods to the screen
    [pod.drawpod(x,y) for pod in pods]
    # Drawing doors on the pods
    [pod.drawdoors() for pod in pods]

    internal_pod_check = ''

     # fire emergency
    firesupress('Living Quarters') #fire supress dont touch change location of supress below
    fire('Living Quarters') #display red fire
    fire1.fire_event('Living Quarters')# fire event

    # fire
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    fireparticles1.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    # add extra fire

    # fire suppresant
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    fireparticles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    fire2.fire_event('Engineering Workshop/Mining Operations/Storage')
    fire('Engineering Workshop/Mining Operations/Storage')
    firesupress('Engineering Workshop/Mining Operations/Storage')

    # fire
    for pod in pods:
        if pod.name == "Engineering Workshop/Mining Operations/Storage":
            mx, my = pod.pos[0], pod.pos[1]
            break
    fireparticles1.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    # add extra fire

    # fire suppresant
    for pod in pods:
        if pod.name == "Engineering Workshop/Mining Operations/Storage":
            mx, my = pod.pos[0], pod.pos[1]
            break
    fireparticles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    biosupress('Emergency Quarters')  # fire supress dont touch change location of supress below
    bio('Emergency Quarters')  # display red fire
    bio1.bio_hazard_event('Emergency Quarters')  # fire event

    # bio
    for pod in pods:
        if pod.name == "Emergency Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    bioparticles1.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    # add extra fire

    # bio suppresant
    for pod in pods:
        if pod.name == "Emergency Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    bioparticles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    radiation('Living Quarters')  # fire supress dont touch change location of supress below
    radiationsupress('Living Quarters')  # display red fire
    radiation1.radiation_event('Living Quarters')  # fire event

    # fire
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    radiationparticles1.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    # add extra fire

    # fire suppresant
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    radiationparticles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    air_quality('Living Quarters')  # fire supress dont touch change location of supress below
    air_quality_suppress_f('Living Quarters')  # display red fire
    airquality1.air_quality_event('Living Quarters')  # fire event

    # fire
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    airqualityparticles1.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
    # add extra fire

    # fire suppresant
    for pod in pods:
        if pod.name == "Living Quarters":
            mx, my = pod.pos[0], pod.pos[1]
            break
    airqualityparticles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

    internal_pods = {}
    for pod in pods:
        if len(pod.internal_pod):
            internal_pods[pod.name]=pod.internal_pod[0]

    if counter % (4/multiplier) == 0:
        for pod in pods:
            if pod.orientation == 'left' or pod.pod_type == 'A':
                if pod.pod_type == 'A':
                    index1, index2 = 0, 2
                else:
                    index1, index2 = 0, 1

                if keys[pygame.K_e]:
                    if pod.connecting_rooms[index1] != 'empty' and pod.side_to_attach_door != 'right':
                        if checkcollided(pod.leftdoorpos[0],pod.leftdoorpos[1],x,y):
                            pod.leftdoorstate = not pod.leftdoorstate
                    if pod.connecting_rooms[index2] != 'empty' and pod.side_to_attach_door != 'left':
                        if checkcollided(pod.rightdoorpos[0],pod.rightdoorpos[1],x,y):
                            pod.rightdoorstate = not pod.rightdoorstate

                if pod.connecting_rooms[index1] not in ['outside','empty']:
                    if pod.leftdoorstate == True and pod.rightdoorstate == False and pod.topdoorstate == False and pod.bottomdoorstate == False and pods[index(pod.connecting_rooms[index1])].leftdoorstate == False and pods[index(pod.connecting_rooms[index1])].topdoorstate == False and pods[index(pod.connecting_rooms[index1])].bottomdoorstate == False:
                        pod.opendoor('left')
                    else:
                        pod.closedoor('left')
                elif pod.connecting_rooms[index1] == 'outside':
                    if pod.leftdoorstate == True and pod.rightdoorstate == False and pod.topdoorstate == False and pod.bottomdoorstate == False:
                        pod.opendoor('left')
                    else:
                        pod.closedoor('left')
                if pod.connecting_rooms[index2] not in ['outside','empty']:
                    if pod.rightdoorstate == True and pod.leftdoorstate == False and pod.topdoorstate == False and pod.bottomdoorstate == False and pods[index(pod.connecting_rooms[index2])].rightdoorstate == False and pods[index(pod.connecting_rooms[index2])].topdoorstate == False and pods[index(pod.connecting_rooms[index2])].bottomdoorstate == False:
                        pod.opendoor('right')
                    else:
                        pod.closedoor('right')
                elif pod.connecting_rooms[index2] == 'outside':
                    if pod.rightdoorstate == True and pod.leftdoorstate == False and pod.topdoorstate == False and pod.bottomdoorstate == False:
                        pod.opendoor('right')
                    else:
                        pod.closedoor('right')

            if pod.orientation == 'top' or pod.pod_type == 'A':
                if pod.pod_type == 'A':
                    index1, index2 = 1, 3
                else:
                    index1, index2 = 0, 1

                if keys[pygame.K_e]:
                    if pod.connecting_rooms[index1] != 'empty' and pod.side_to_attach_door != 'bottom':
                        if checkcollided(pod.topdoorpos[0],pod.topdoorpos[1],x,y):
                            pod.topdoorstate = not pod.topdoorstate
                    if pod.connecting_rooms[index2] !=  'empty' and pod.side_to_attach_door != 'top':
                        if checkcollided(pod.bottomdoorpos[0],pod.bottomdoorpos[1],x,y):
                            pod.bottomdoorstate = not pod.bottomdoorstate

                if pod.connecting_rooms[index1] not in ['outside','empty']:
                    if pod.topdoorstate == True and pod.bottomdoorstate == False and pod.leftdoorstate == False and pod.rightdoorstate == False and pods[index(pod.connecting_rooms[index1])].topdoorstate == False and pods[index(pod.connecting_rooms[index1])].rightdoorstate == False and pods[index(pod.connecting_rooms[index1])].leftdoorstate == False:
                        pod.opendoor('top')
                    else:
                        #
                         pod.closedoor('top')
                elif pod.connecting_rooms[index1] == 'outside':
                    if pod.topdoorstate == True and pod.bottomdoorstate == False and pod.leftdoorstate == False and pod.rightdoorstate == False:
                        pod.opendoor('top')
                    else:
                        pod.closedoor('top')
                if pod.connecting_rooms[index2] not in ['outside', 'empty']:
                    if pod.bottomdoorstate == True and pod.topdoorstate == False and pod.leftdoorstate == False and pod.rightdoorstate == False and pods[index(pod.connecting_rooms[index2])].bottomdoorstate == False and pods[index(pod.connecting_rooms[index2])].rightdoorstate == False and pods[index(pod.connecting_rooms[index2])].leftdoorstate == False:
                        pod.opendoor('bottom')
                    else:
                        pod.closedoor('bottom')
                elif pod.connecting_rooms[index2] == 'outside':
                     if pod.bottomdoorstate == True and pod.topdoorstate == False and pod.leftdoorstate == False and pod.rightdoorstate == False:
                         pod.opendoor('bottom')
                     else:
                         pod.closedoor('bottom')

    '''for pod in pods:
        if pod.id in [1,2]:
            print(pod.name,pod.leftdoorstate,pod.rightdoorstate,pod.topdoorstate,pod.bottomdoorstate)'''

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
        if event.type == pygame.USEREVENT:
            for timer in clocks:
                timer.time -= 1
                timer.timetext = str(timer.time).rjust(3) if timer.time > 0 else '0'.rjust(3)
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
    for timer in clocks:
        timer.display()
    pygame.display.update()
pygame.quit()