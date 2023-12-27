import json
import tkinter as tk
import colors

# Globals
colors = colors.getcolor()
button_color = colors[0]
button_color_ag = colors[1]
button_color_nw = colors[2]
label_color = colors[3]
window_color = colors[4]

agenda_file = "agenda.json"
lessons_file = "lessons.json"
#agenda = {'class' : classname, 'period': period, 'date': date, 'lesson': lesson_name}

def getlist():
    try:
        with open(agenda_file, "r") as jfile:
            agenda_data = json.load(jfile)
    except json.JSONDecodeError:
        agenda_data = []
    
    try:
        with open(lessons_file, "r") as ffile:
            lesson_data = json.load(ffile)
    except json.JSONDecodeError:
        lesson_data = []
    
    return (agenda_data, lesson_data)

def add_agenda(classname, period, date):
    data = getlist()
    agendas = data[0]
    lessons_unorg = data[1]
    lessons = sorted(lessons_unorg, key=lambda d: d['short'].lower())

    def lesson_select(lesson):
        try:
            name = lesson['short']
            agenda = {'class': classname, 'period': period, 'date': date, 'lesson': name}
            agendas.append(agenda)
            with open(agenda_file, "w") as jfile:
                json.dump(agendas, jfile, indent=4)

        except NameError:
            pass
        window.destroy()
            
    # Main Window
    window = tk.Tk()
    window.title("Available Lessons")

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Canvas to hold buttons
    canvas = tk.Canvas(window, bg=f'{label_color}')
    canvas.grid(row=0, column=0, sticky='nsew')
    
    # Frame for buttons
    frame = tk.Frame(canvas, bg=f'{label_color}')
    canvas.create_window((0,0), window=frame, anchor='nw')
    
    # Scrollbar
    scrollbar = tk.Scrollbar(window, command=canvas.yview, bg=f'{window_color}')
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Canvas + Scrollbar Config
    canvas.config(yscrollcommand=scrollbar.set)


    # Label
    label = tk.Label(frame, text="Select a Lesson", bg=f'{label_color}')
    label.grid(row=0, column=0, padx=10, pady=10)

    # Create Buttons
    for i, lesson in enumerate(lessons):
        if lesson['class'][:3].upper() == classname[:3].upper():
            button = tk.Button(frame, text=lesson['short'], command=lambda less = lesson: lesson_select(less), padx=10, pady=10,  wraplength=175, bg=f'{button_color}')
            button.grid(row=i+1, column=0, padx=25, pady=5, sticky='news')
    
    # Update
    frame.update_idletasks()
    canvas.config(scrollregion=frame.bbox("all"))

    # Mousewheel
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    
    # Window
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    win_width = 260
    win_height = 500
    x = (screen_width // 2) - (win_width // 2)
    y = (screen_height // 2) - (win_height // 2)
    window.geometry(f"{win_width}x{win_height}+{x}+{y}")
    window.configure(bg=f'{window_color}')
    
    window.mainloop()

def rm_agenda(classname, period, date):
    data = getlist()
    agendas = data[0]
    new_agendas = []
    try:
        for agen in agendas:
            if agen['class'] == classname and agen['period'] == period and agen['date'] == date:
                pass
            else:
                new_agendas.append(agen)
        with open(agenda_file, "w") as jfile:
            json.dump(new_agendas, jfile, indent=4)

    except NameError:
        pass

