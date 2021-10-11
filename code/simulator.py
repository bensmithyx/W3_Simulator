

class Pod:
    def __init__(self, name, doors, door_type, internal_pod):
        self.door_type = door_type
        self.internal_pod = internal_pod
        self.doors = doors
        self.name = name
        # Checking if there is a pod within another one if there is it will add the doors so it knows how to get to the pod
        if len(self.internal_pod):
            self.internal_top_door = internal_pod[0]
            self.internal_bottom_door = internal_pod[0]
        # If the pod is of type A it will assign the where the doors lead to the variables so we can make a path to it
        if len(self.doors) == 4:
            self.pod_type = 'A'
            self.leftdoor = doors[0]
            self.topdoor = doors[1]
            self.rightdoor = doors[2]
            self.bottomdoor = doors[3]
        # If the pod is of type B it will assign where the doors lead to the variables so we can make a path to it
        elif len(self.doors) == 2:
            self.pod_type = 'B'
            self.topdoor = doors[0]
            self.bottomdoor = doors[1]
        else:
            self.pod_type = 'unknown'

    def __repr__(self):
        # Shows the internal doors (when a pod is inside another)
        show_internal_doors = f"{f'Internal Top Door ({self.door_type[0]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n{f'Internal Bottom Door ({self.door_type[1]}) = ' + self.internal_pod[0] if self.internal_pod else ''}\n"
        # Depedending on the type is will display the pods attributes
        if self.pod_type == 'A':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nLeft Door ({self.door_type[0]}) = {self.leftdoor}\nTop Door ({self.door_type[1]}) = {self.topdoor}\nRight Door ({self.door_type[2]}) = {self.rightdoor}\nBottom Door ({self.door_type[3]}) = {self.bottomdoor}\n{show_internal_doors if self.internal_pod else ''}"
        elif self.pod_type == 'B':
            return f"Name = {self.name}\nPod Type = {self.pod_type}\nTop Door ({self.door_type[0]}) = {self.topdoor}\nBottom Door ({self.door_type[1]}) = {self.bottomdoor}\n"

# List of all the pods if a new one is to be added it can be done here
pods = [Pod('Living Quarters',['outside','empty','Connecting Corridor','empty'],['airlock','empty','normal','empty'],[]),Pod('Connecting Corridor',['Living Quarters','Food Production','Engineering Workshop/Mining Operations/Storage','Life Support/Power Plant/Recycling'],['normal','normal','normal','normal'],['Comms And Control Centre']),Pod('Comms And Control Centre',['Connecting Corridor','Connecting Corridor'],['normal','normal'],[]),Pod('Engineering Workshop/Mining Operations/Storage',['Connecting Corridor','Bio-Research','outside','empty'],['normal','airlock','airlock','empty'],[]),Pod('Bio-Research',['outside','Engineering Workshop/Mining Operations/Storage'],['empty','airlock'],[]),Pod('Food Production',['empty','Connecting Corridor'],['empty','normal'],[]),Pod('Life Support/Power Plant/Recycling',['Connecting Corridor','outside'],['normal','airlock'],[]),Pod('Storage (External)',['outside','empty'],['airlock','empty'],[]),Pod('Emergency Quarters',['empty','empty','empty','outside'],['empty','empty','empty','airlock'],[])]

# Displaying all pods and there attributes to the screen
[print(pod) for pod in pods]

# Finds the index of a certain pod based on it's name
def index(source):
    for i in range(0,len(pods)):
        if pods[i].name == source:
            return i

# Source and target locations for path finder
source = 'Living Quarters'
target = 'Bio-Research'

# Function to find the path from a source location to a target location
def findpath(source, target, newplace, path, recursive):
    path = path
    if not recursive:
        # Moves source location to start of array so that is the pod we are starting from
        pods.insert(0, pods.pop(index(source)))
    i = newplace
    # Checking if the target pod is attached to current pod
    if target in pods[i].doors+pods[i].internal_pod:
        path.append(pods[i].name)
        path.append(target)
        return path
    else:
        path.append(pods[i].name)
        for door in pods[i].doors+pods[i].internal_pod:
            # If the door has not been searched yet and it is not leading outside or empty it will re run the function to check all of that pods doors for the target
            if door not in ['empty','outside'] and door not in path:
                newplace = index(door)
                result =  findpath(source, target, newplace, path, 1)
                if result == None:
                    del path[-1]
                else: return result

# Takes the path as a variable
finalpath = findpath(source, target,0,[],0)
if finalpath != None:
    print(f'Source: {source}\nTarget: {target}\n{finalpath}')
else:
    print("Must go Outside")

# Locks all doors in a given pod
def lockdown(pod):
    [print(f'\nLocking {door} door\n') if door != 'empty' else '' for door in pods[index(pod)].door_type]

lockdown('Connecting Corridor')
