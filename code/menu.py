from tkinter import *
from tkinter import ttk

'''
when using command to pass a parameter in a button 
you HAVE to use lambda
command=lambda:function(param)
'''


class State:
    def __init__(self):
        self.speed = "1"
        # First number represents the number of astronauts in pod A, second is pod B etc
        self.num_astros_arr = [1, 1, 1, 1]


class MainWindow:
    def __init__(self):
        # creates a tk window called root
        self.root = Tk()

        # Title on the window
        self.root.title("Test Scenario Generator")

        # Starting size and minimum size of the window
        self.root.geometry("1000x600")
        self.root.minsize(750, 450)

        self.entries = []

        self.canvas = Canvas()

    def render_main(self):
        self.canvas = Canvas(self.root, bg="grey")
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
        self.canvas = Canvas(self.root, bg="grey")
        # creates the frame with both the save and cancel buttons on them
        # pass in context so save knows where to store the information
        save_cancel_frame = init_save_cancel_frame(self.canvas, "astros")
        save_cancel_frame.place(relx=0.5, rely=0.85, relwidth=0.8, relheight=0.175, anchor="center")

        pod_name_arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "k"]
        for i in range(len(state.num_astros_arr)):
            pod_string = "Pod " + pod_name_arr[i] + ": "
            entry_frame = init_input_frame(self.canvas, pod_string)
            entry_frame.place(relx=0.5, rely=0.05+(i*0.09), relwidth=0.95, relheight=0.075, anchor="center")

        self.canvas.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.95, anchor="center")

    def destroy_canvas(self):
        self.canvas.destroy()

    def reload_main(self):
        self.destroy_canvas()
        self.render_main()


def init_input_frame(master, text):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    label = Label(frame, text=text, font=20)
    label.pack(side=LEFT, anchor=W)

    entry = Entry(frame, width=80)
    entry.pack(side=RIGHT, anchor=E)
    MainWindow.entries.append(entry)

    return frame


def init_save_cancel_frame(master, context):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    save_btn = Button(frame, text="SAVE", height=20, width=30, command=lambda: save(context), bg="green")
    save_btn.pack(side=LEFT, anchor=NE)

    cancel_btn = Button(frame, text="CANCEL", height=20, width=30, command=go_back, bg="red")
    cancel_btn.pack(side=RIGHT, anchor=NW)

    return frame


def init_load_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    # Create a label with the frame as the parent and then pack to the top
    text_intro = "Use the buttons to configure the test scenario"
    intro_lbl = Label(frame, text=text_intro)
    intro_lbl.pack(side=TOP, anchor=NW)

    # Creates a button with frame as the parents and then pack to bottom
    text_load = "Use a Saved Scenario"
    load_btn = Button(frame, text=text_load, height=10, width=30, command=load_scenario, bg="yellow")
    load_btn.pack(side=TOP, anchor=NE)

    return frame


def init_astro_config_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    text_astro_config = "Configure Astronaut Starting Position"
    astro_config_btn = Button(frame, text=text_astro_config, height=20, width=30, command=astro_config, bg="cyan")
    astro_config_btn.pack(side=TOP, anchor=CENTER, fill=BOTH)

    return frame


def init_astro_view_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    pod_name_arr = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "k"]
    text_astros = "Astronauts:\n"
    for i in range(len(state.num_astros_arr)):
        text_astros += "Pod " + pod_name_arr[i] + ": " + str(state.num_astros_arr[i]) + "\n"

    astros_lbl = Label(frame, text=text_astros)
    astros_lbl.pack(side=LEFT, anchor=NW)

    return frame


def init_speed_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    # Need to program logic so when the button is clicked it will cycle through set speeds
    text_set_speed = "Set speed: " + str(state.speed)
    set_speed_btn = Button(frame, text=text_set_speed, height=15, width=30, command=set_speed, bg="pink")
    set_speed_btn.pack(side=TOP, anchor=CENTER, fill=BOTH)

    return frame


def init_disaster_time_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    text_disaster = "Add a Disaster"
    disaster_btn = Button(frame, text=text_disaster, height=15, width=30, command=add_disaster, bg="red")
    disaster_btn.pack(side=LEFT, anchor=NW)

    text_time = "Add Wait Time"
    time_btn = Button(frame, text=text_time, height=15, width=30, command=add_time, bg="orange")
    time_btn.pack(side=RIGHT, anchor=NE)
    return frame


def init_timeline_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    # Add the various disasters here
    # No idea how to do this, probably using pack right with some padding?

    return frame


def init_save_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    text_save = "Save Scenario as: "
    save_lbl = Label(frame, text=text_save)
    save_lbl.pack(side=TOP, anchor=NW)

    save_ent = Entry(frame, width=50)
    save_ent.pack(side=TOP, anchor=NW)

    return frame


def init_save_button_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    text_button_save = "SAVE"
    save_btn = Button(frame, text=text_button_save, height=15, width=15, command=save_scenario, bg="#49A")
    save_btn.pack(side=TOP, anchor=N, fill=BOTH)

    return frame


def init_run_frame(master):
    # Creates a frame with the parent as the window
    frame = ttk.Frame(master)
    # Styling for the frame
    frame['padding'] = 5
    frame['relief'] = "sunken"

    run_btn = Button(frame, text="RUN", height=15, width=15, command=run_scenario, bg="green")
    run_btn.pack(side=TOP, anchor=N, fill=BOTH)

    return frame


def load_scenario():
    print("Load")


def astro_config():
    print("Astronaut configuration")
    MainWindow.destroy_canvas()
    MainWindow.render_astro_config()


def set_speed():
    # The values the speed multiplier will jump up in
    speeds = ["1", "1.5", "2", "3", "5", "10", "20"]

    # If speed is the highest value, change it to the lowest
    if state.speed == speeds[-1]:
        state.speed = speeds[0]

    else:
        for i in range(len(speeds)):
            if speeds[i] == state.speed:
                state.speed = speeds[i+1]
                break

    MainWindow.reload_main()


def add_disaster():
    print("Add a disaster")


def add_time():
    print("Add time")


def save_scenario():
    print("SAVE")


def run_scenario():
    print("Run Scenario")


def go_back():
    MainWindow.reload_main()


def save(context):
    if context == "astros":
        for i in range(len(MainWindow.entries)):
            state.num_astros_arr[i] = MainWindow.entries[i].get()

    else:
        print("Error while saving: no context")

    MainWindow.reload_main()


state = State()

# Creates the window and then runs mainloop on it
MainWindow = MainWindow()
MainWindow.render_main()
MainWindow.root.mainloop()
