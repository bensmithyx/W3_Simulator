from tkinter import *

'''
Got issues with removing the items in the timeline
Whatever I do it always just removes the last one that was entered
Cannot think of a way to keep track of which button is associated with each item
Worst case scenario instead of just removing one item,
    it would be trivial to make a button that clears them all
'''


class State:
    def __init__(self):
        self.speed = "1x"
        # First number represents the number of astronauts in pod A, second is pod B etc
        self.num_astros_arr = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        # 2D array, first element being the disaster, second being the pod, then new array element
        # This also includes wait times in the format: ["TIME", <time to wait>]
        self.timeline = []


class MainWindow:
    def __init__(self):
        # creates a tk window called root
        self.root = Tk()

        # Title on the window
        self.root.title("Test Scenario Generator")

        # Starting size and minimum size of the window
        self.root.geometry("1000x600")
        self.root.minsize(750, 450)
        self.root.configure(bg='grey')
        self.entries = []

        self.canvas = Canvas()

    def render_main(self):
        self.canvas = Canvas(self.root, bg="grey",highlightthickness=0)
        self.entries = []

        # Create frames and then place them on the canvas
        load_frame = init_load_frame(self.canvas)
        load_frame.place(relx=0.5, rely=0.025, relwidth=0.95, relheight=0.1, anchor="n")

        astro_config_frame = init_astro_config_frame(self.canvas)
        astro_config_frame.place(relx=0.025, rely=0.15, relwidth=0.3, relheight=0.25, anchor="nw")

        astro_view_frame = init_astro_view_frame(self.canvas)
        astro_view_frame.place(relx=0.35, rely=0.15, relwidth=0.2, relheight=0.25, anchor="nw")

        speed_frame = init_speed_frame(self.canvas)
        speed_frame.place(relx=0.6, rely=0.15, relwidth=0.375, relheight=0.25, anchor="nw")

        disaster_time_frame = init_disaster_time_frame(self.canvas)
        disaster_time_frame.place(relx=0.5, rely=0.425, relwidth=0.6, relheight=0.15, anchor="n")

        timeline_frame = init_timeline_frame(self.canvas)
        timeline_frame.place(relx=0.5, rely=0.6, relwidth=0.95, relheight=0.25, anchor="n")

        save_frame = init_save_frame(self.canvas)
        save_frame.place(relx=0.025, rely=0.875, relwidth=0.3, relheight=0.1, anchor="nw")

        save_button_frame = init_save_button_frame(self.canvas)
        save_button_frame.place(relx=0.35, rely=0.875, relwidth=0.1, relheight=0.1, anchor="nw")

        run_button_frame = init_run_frame(self.canvas)
        run_button_frame.place(relx=0.8, rely=0.875, relwidth=0.15, relheight=0.1, anchor="nw")

        # Place the canvas in the centre of the screen with some padding around it
        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def render_astro_config(self):
        self.canvas = Canvas(self.root, bg="grey", highlightthickness=0)
        # creates the frame with both the save and cancel buttons on them
        # pass in context so save knows where to store the information
        save_cancel_frame = init_save_cancel_frame(self.canvas, "astros")
        save_cancel_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.175, anchor="center")

        pod_name_arr = ["Living Quarters", "Connecting Corridor", "Emergency Quarters", "Life Support/Power Plant/Recycling", "Food Production", "Engineering Workshop/Mining Operations/Storage", "Bio-Research", "Storage (External)", "Comms And Control Centre"]
        for i in range(len(state.num_astros_arr)):
            pod_string = pod_name_arr[i] + ": "
            entry_frame = init_input_frame(self.canvas, pod_string)
            entry_frame.place(relx=0.5, rely=0.05+(i*0.09), relwidth=0.95, relheight=0.075, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def render_disaster_config(self):
        self.canvas = Canvas(self.root, bg="grey", highlightthickness=0)
        # creates the frame with both the save and cancel buttons on them
        # pass in context so save knows where to store the information

        buttons_frame = init_disaster_button_frame(self.canvas)
        buttons_frame.place(relx=0.5, rely=0.05, relwidth=0.95, relheight=0.7, anchor="n")

        go_back_frame = init_go_back_frame(self.canvas)
        go_back_frame.place(relx=0.5, rely=0.85, relwidth=0.95, relheight=0.15, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def render_add_disaster(self, disaster):
        self.destroy_canvas()
        self.canvas = Canvas(self.root, bg="grey", highlightthickness=0)
        # creates the frame with both the save and cancel buttons on them
        # pass in context so save knows where to store the information

        input_text = disaster + ":"
        input_frame = init_input_frame(self.canvas, input_text)
        input_frame.place(relx=0.5, rely=0.7, relwidth=0.95, relheight=0.075, anchor="center")
        pod_name_arr = ["Living Quarters", "Connecting Corridor", "Emergency Quarters", "Life Support/Power Plant/Recycling", "Food Production", "Engineering Workshop/Mining Operations/Storage", "Bio-Research", "Storage (External)", "Comms And Control Centre"]
        newline = '\n'
        output = list([f'{index+1} - {pod}' for index, pod in enumerate(pod_name_arr)])
        instructions = Label(self.canvas,text=f"Please enter the pod the disaster should take place in{newline}{newline.join(output)}",font=20, bg='grey')
        instructions.place(relx=0.025, rely=0.05, relwidth=0.8, relheight=0.5, anchor="nw")

        save_cancel_frame = init_save_cancel_frame(self.canvas, disaster)
        save_cancel_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.175, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def render_add_time(self):
        self.destroy_canvas()
        self.canvas = Canvas(self.root, bg="grey", highlightthickness=0)
        # creates the frame with both the save and cancel buttons on them

        input_frame = init_input_frame(self.canvas, "Add how long to wait for, in seconds")
        input_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.075, anchor="center")

        save_cancel_frame = init_save_cancel_frame(self.canvas, "time")
        save_cancel_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.175, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def render_load_scenario(self):
        self.destroy_canvas()
        self.canvas = Canvas(self.root, bg="grey", highlightthickness=0)
        # creates the frame with both the save and cancel buttons on them

        input_frame = init_input_frame(self.canvas, "Enter the filename of the scenario you wish to load")
        input_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.075, anchor="center")

        save_cancel_frame = init_save_cancel_frame(self.canvas, "load")
        save_cancel_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.175, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def destroy_canvas(self):
        self.canvas.destroy()

    def reload_main(self):
        self.destroy_canvas()
        self.render_main()


def init_disaster_button_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    Grid.rowconfigure(frame, 0, weight=1)
    Grid.rowconfigure(frame, 1, weight=1)
    Grid.columnconfigure(frame, 0, weight=1)
    Grid.columnconfigure(frame, 1, weight=1)

    fire_btn = Button(frame, text="Fire", bg="orange", font=20,
                      command=lambda: MainWindow.render_add_disaster("fire"), highlightthickness=0)
    fire_btn.grid(row=0, column=0, sticky="news", padx=15, pady=15)

    bio_btn = Button(frame, text="Biohazard", bg="yellow", font=20,
                     command=lambda: MainWindow.render_add_disaster("bio"), highlightthickness=0)
    bio_btn.grid(row=0, column=1, sticky="news", padx=15, pady=15)

    air_btn = Button(frame, text="Air Hazard", bg="blue", font=20,
                     command=lambda: MainWindow.render_add_disaster("airquality"), highlightthickness=0)
    air_btn.grid(row=1, column=0, sticky="news", padx=15, pady=15)

    rad_btn = Button(frame, text="Radiation", bg="green", font=20,
                     command=lambda: MainWindow.render_add_disaster("radiation"), highlightthickness=0)
    rad_btn.grid(row=1, column=1, sticky="news", padx=15, pady=15)

    return frame


def init_add_time_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"


def init_input_frame(master, text):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    label = Label(frame, text=text, font=20, bg='grey')
    label.pack(side=LEFT, anchor=W)

    entry = Entry(frame, width=80)
    entry.pack(side=RIGHT, anchor=E)
    MainWindow.entries.append(entry)

    return frame


def init_go_back_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    cancel_btn = Button(frame, text="Go back", height=20, width=30, command=go_back, bg="red", highlightthickness=0)
    cancel_btn.pack(side=TOP, anchor=CENTER)

    return frame


def init_save_cancel_frame(master, context):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    save_btn = Button(frame, text="SAVE", height=20, width=30, command=lambda: save(context), bg="green", highlightthickness=0)
    save_btn.pack(side=LEFT, anchor=NE)

    cancel_btn = Button(frame, text="CANCEL", height=20, width=30, command=go_back, bg="red", highlightthickness=0)
    cancel_btn.pack(side=RIGHT, anchor=NW)

    return frame


def init_load_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    # Create a label with the frame as the parent and then pack to the top
    text_intro = "Use the buttons to configure the test scenario"
    intro_lbl = Label(frame, text=text_intro, bg='grey')
    intro_lbl.pack(side=TOP, anchor=NW)

    # Creates a button with frame as the parents and then pack to bottom
    text_load = "Use a Saved Scenario"
    load_btn = Button(frame, text=text_load, height=10, width=30, command=load_scenario, bg="yellow", highlightthickness=0)
    load_btn.pack(side=TOP, anchor=NE)

    return frame


def init_astro_config_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    text_astro_config = "Configure Astronaut Starting Position"
    astro_config_btn = Button(frame, text=text_astro_config, height=20, width=30, command=astro_config, bg="cyan", highlightthickness=0)
    astro_config_btn.pack(side=TOP, anchor=CENTER, fill=BOTH)

    return frame


def init_astro_view_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='lightgrey')
    # Styling for the frame

    frame['relief'] = "sunken"

    pod_name_arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "k"]
    text_astros = "Astronauts:"
    for i in range(len(state.num_astros_arr)):
        text_astros += "\nPod " + pod_name_arr[i] + ": " + str(state.num_astros_arr[i])

    astros_lbl = Label(frame, text=text_astros, bg='lightgrey')
    astros_lbl.pack(side=LEFT, anchor=NW)

    return frame


def init_speed_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    # Need to program logic so when the button is clicked it will cycle through set speeds
    text_set_speed = "Set speed: " + str(state.speed)
    set_speed_btn = Button(frame, text=text_set_speed, height=15, width=30, command=set_speed, bg="pink", highlightthickness=0, borderwidth=1)
    set_speed_btn.pack(side=TOP, anchor=CENTER, fill=BOTH)

    return frame


def init_disaster_time_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    text_disaster = "Add a Disaster"
    disaster_btn = Button(frame, text=text_disaster, height=15, width=30, command=disaster_config, bg="red", highlightthickness=0)
    disaster_btn.pack(side=LEFT, anchor=NW)

    text_time = "Add Wait Time"
    time_btn = Button(frame, text=text_time, height=15, width=30, command=add_time, bg="orange", highlightthickness=0)
    time_btn.pack(side=RIGHT, anchor=NE)
    return frame


def init_timeline_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='lightgrey')
    # Styling for the frame

    frame['relief'] = "sunken"

    for index, entry in enumerate(state.timeline, start=0):
        if entry[0] == "fire":
            colour = "orange"
        elif entry[0] == "bio":
            colour = "yellow"
        elif entry[0] == "airquality":
            colour = "blue"
        elif entry[0] == "radiation":
            colour = "green"
        elif entry[0] == "TIME":
            colour = "#fb7dff"
        else:
            print("Error: Invalid entry")
            colour = "red"

        if entry[0] != "TIME":
            text = entry[0].upper() + "\nin pod: " + entry[1]
        else:
            text = "Time to wait\n" + entry[1] + " seconds"

        disaster_lbl = Label(frame, text=text, width=15, height=15, bg=colour)

        btns = []

        class remove_btn:
            def __init__(self, index, label):
                self.label = label
                self.index = index
                self.btn = Button(self.label, text="X", bg="red",command=lambda: [state.timeline.pop(self.index), MainWindow.reload_main()], highlightthickness=0)
                self.label.pack(side=LEFT, anchor=E, padx=5, pady=5)
                self.btn.place(relx=0.95, rely=0.05, relwidth=0.2, relheight=0.2, anchor="ne")

        # !!! PROBLEM CODE IS HERE !!!
        btns.append(remove_btn(index, disaster_lbl))

    return frame


def init_save_frame(master):
    MainWindow.entries = []
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    text_save = "Save Scenario as: "
    save_lbl = Label(frame, text=text_save, bg='grey')
    save_lbl.pack(side=TOP, anchor=NW)

    save_ent = Entry(frame, width=50)
    MainWindow.entries.append(save_ent)
    save_ent.pack(side=TOP, anchor=NW)

    return frame


def init_save_button_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=0, bg='grey')
    # Styling for the frame

    frame['relief'] = "sunken"

    text_button_save = "SAVE"
    save_btn = Button(frame, text=text_button_save, height=15, width=15, command=save_scenario, bg="#49A", highlightthickness=0)
    save_btn.pack(side=TOP, anchor=N, fill=BOTH)

    return frame


def init_run_frame(master):
    # Creates a frame with the parent as the window
    frame = Frame(master, borderwidth=-30)
    # Styling for the frame
    #
    #frame['relief'] = "solid"

    run_btn = Button(frame, text="RUN", height=15, width=15, command=run_scenario, bg="green", highlightthickness=0)
    run_btn.pack(side=TOP, anchor=N, fill=BOTH)

    return frame


def load_scenario():
    MainWindow.entries = []
    MainWindow.destroy_canvas()
    MainWindow.render_load_scenario()


def astro_config():
    MainWindow.entries = []
    MainWindow.destroy_canvas()
    MainWindow.render_astro_config()


def set_speed():
    # The values the speed multiplier will jump up in
    speeds = ["1x", "2x", "4x", "6x", "8x"]

    # If speed is the highest value, change it to the lowest
    if state.speed == speeds[-1]:
        state.speed = speeds[0]

    else:
        for i in range(len(speeds)):
            if speeds[i] == state.speed:
                state.speed = speeds[i+1]
                break

    MainWindow.reload_main()


def disaster_config():
    MainWindow.entries = []
    MainWindow.destroy_canvas()
    MainWindow.render_disaster_config()


def add_time():
    MainWindow.entries = []
    MainWindow.destroy_canvas()
    MainWindow.render_add_time()


def save_scenario():
    text = state.speed + "\n" + str(state.num_astros_arr) + "\n" + str(state.timeline)
    filename = MainWindow.entries[0].get() + ".txt"
    with open(filename, 'w') as file:
        file.write(text)
        file.close()


def run_scenario():
    text = state.speed + "\n" + str(state.num_astros_arr) + "\n" + str(state.timeline)
    filename = ".scenario.txt"
    with open(filename, 'w') as file:
        file.write(text)
        file.close()
    MainWindow.root.destroy()


def go_back():
    MainWindow.reload_main()


def save(context):
    disaster_list = ['fire','bio','airquality','radiation','airpressure']
    disaster_array = []
    if context == "astros":
        for i in range(len(MainWindow.entries)):
            state.num_astros_arr[i] = MainWindow.entries[i].get()

    elif context == "time":
        to_append = ["TIME", MainWindow.entries[0].get()]
        state.timeline.append(to_append)

    elif context == "load":
        filename = MainWindow.entries[0].get()
        if ".txt" not in filename:
            filename += ".txt"
        load_state(filename)

    elif context in disaster_list:
        if context == disaster_list[0]:
            disaster_array = [disaster_list[0]]
        elif context == disaster_list[1]:
            disaster_array = [disaster_list[1]]
        elif context == disaster_list[2]:
            disaster_array = [disaster_list[2]]
        elif context == disaster_list[3]:
            disaster_array = [disaster_list[3]]
        else:
            print("ERROR: Not a valid disaster to save")

        disaster_array.append(MainWindow.entries[0].get())
        state.timeline.append(disaster_array)

    else:
        print("Error while saving: no context")

    MainWindow.reload_main()


def load_state(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        file.close()

    state.speed = lines[0].replace('\n', '')

    astros = lines[1].replace('[', '').replace(']', '').replace("'", '').replace(' ', '').replace('\n', '')
    astros_arr = astros.split(',')
    state.num_astros_arr = astros_arr

    disasters = lines[2].replace('[', '').replace(']', '').replace("'", '').replace(' ', '').replace('\n', '')
    disaster_arr = disasters.split(',')

    i = 0
    state.timeline = []
    while i < len(disaster_arr):
        to_append = [disaster_arr[i], disaster_arr[i+1]]
        state.timeline.append(to_append)
        i += 2

    MainWindow.reload_main()


state = State()

# Creates the window and then runs mainloop on it
MainWindow = MainWindow()
MainWindow.render_main()
MainWindow.root.mainloop()
