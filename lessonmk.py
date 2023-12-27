import json
import tkinter as tk
lesson_file = "lessons.json"
import colors

# Globals
colors = colors.getcolor()
button_color = colors[0]
button_color_ag = colors[1]
button_color_nw = colors[2]
label_color = colors[3]
window_color = colors[4]

#Return list of lesson dicts
def getlist():
    try:
        with open(lesson_file, "r") as jfile:
            lesson_data = json.load(jfile)
    except json.JSONDecodeError:
        lesson_data = []
    
    return lesson_data

# Opens Add Lesson Window
def add_lesson():

 # View Button
    def on_view():
        lesson_window = tk.Toplevel(window)
        lesson_window.title("Lessons")
            # Updates details and labels
        def update_label():
            for button in lesson_window.grid_slaves():
                if button.winfo_exists():
                    button.grid_forget()
            populate()
            lesson_window.update()
        # Remove lesson
        def on_click(classname, short, longg):
            def rm_less():
                data = getlist()
                new_lessons = []
                try:
                    for les in data:
                        if les['class'] == classname and les['short'] == short and les['long'] == longg:
                            pass
                        else:
                            new_lessons.append(les)
                    with open(lesson_file, "w") as jfile:
                        json.dump(new_lessons, jfile, indent=4)

                except NameError:
                    pass
                update_label()
                nwindow.destroy()
            def cancelit():
                update_label()
                nwindow.destroy()
            nwindow = tk.Toplevel()
            nwindow.title("Delete Lessons")
            nwindow.configure(bg=f'{window_color}')
    
            screen_width = nwindow.winfo_screenwidth()
            screen_height = nwindow.winfo_screenheight()
            
            label = tk.Label (nwindow, text="Are you sure you want to delete this lesson?", bg=f'{window_color}', fg='black')
            label.grid(row=0, columnspan=2, pady=20)

            delbutt = tk.Button(nwindow, text='Delete', command=rm_less, bg=f'{button_color}', fg='black')
            delbutt.grid(row=1, column=0, padx=10, pady=10, sticky='news')
            canbutt = tk.Button(nwindow, text="Cancel", command=cancelit, bg=f'{button_color}', fg='black')
            canbutt.grid(row=1, column=1, padx=10, pady=10, sticky='news')
            
            win_width = 370
            win_height = 130
            x = (screen_width // 2) - (win_width // 2)
            y = (screen_height // 2) - (win_height // 2)

            nwindow.geometry(f"{win_width}x{win_height}+{x}+{y}")

            
        
        def populate():
            lesson_list = getlist()

            classes = []
            
            # Make list of classes
            for less in lesson_list:
                if less['class'][:4] in classes:
                    pass
                else:
                    classes.append(less['class'][:4])
        
                # Canvas to hold buttons
            canvas = tk.Canvas(lesson_window, bg=f'{label_color}')
            canvas.grid(row=0, column=0, sticky='nsew')
            
            # Frame for buttons
            frame = tk.Frame(canvas, bg=f'{label_color}')
            canvas.create_window((0,0), window=frame, anchor='nw')
            
            # Scrollbar
            scrollbar = tk.Scrollbar(lesson_window, command=canvas.yview, bg=f'{window_color}')
            scrollbar.grid(row=0, column=1, sticky='ns')

            # Canvas + Scrollbar Config
            canvas.config(yscrollcommand=scrollbar.set)
        
            # Label columns with classes
            for i, row_label in enumerate(classes):
                label = tk.Label(frame, text=row_label, padx=10, pady=10, font=('Arial', 14), borderwidth=1, relief="ridge", bg=f'{label_color}', fg='black')
                label.grid(row=0, column=i, sticky='news')
            
            # Populate with lessons as buttons
            for i, col in enumerate(classes):
                count=1
                for j, less in enumerate(lesson_list):
                    if col == less['class'][:4]:
                        button = tk.Button(frame, text=f"{less['short']}\n"f"{less['long']}\n", wraplength=220, command=lambda a=less['class'], b=less['short'], c=less['long']: on_click(a,b,c), padx=12, pady=10, bg=f'{button_color}', width = 20, fg='black')
                        button.grid(row=count, column=i, sticky='news')
                        count+=1
                        
            # Update
            frame.update_idletasks()
            canvas.config(scrollregion=frame.bbox("all"))



                    # Window
        lesson_window.grid_rowconfigure(0, weight=1)
        lesson_window.grid_columnconfigure(0, weight=1)
        lesson_window.geometry("960x705")
        populate()
    # Submit Button
    def on_submit():
        
        # Exit Button
        def on_exit():
            window.destroy()

        # Save Button
        def on_save():
            try:
                new_lesson = {"class": class_s,"short": short_s,"long": long_str,"standard": standard_str, "skills": skills_ls, "text": text_str, "materials": materials_ls}
                lesson_list = getlist()
                lesson_list.append(new_lesson)
                with open(lesson_file, "w") as jfile:
                    json.dump(lesson_list, jfile, indent=4)
                popup = tk.Toplevel(window)
                popup.title("CONFIRMATION")

                label = tk.Label(popup, text="Lesson Added")
                label.pack(padx=20, pady=20)
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()

                desired_width = 200
                desired_height = 80

                x = (screen_width // 2) - (desired_width // 2)
                y = (screen_height // 2) - (desired_height // 2)

                popup.geometry(f"{desired_width}x{desired_height}+{x}+{y}")
            
            # If new_lesson failes to be made
            except NameError:
                popup = tk.Toplevel(window)
                popup.title("ERROR")
                label = tk.Label(popup, text="There was an error in the data. Lesson not added. Please re-submit.")
                label.pack(padx=20, pady=20)
                screen_width = window.winfo_screenwidth()
                screen_height = window.winfo_screenheight()

                desired_width = 560
                desired_height = 80

                x = (screen_width // 2) - (desired_width // 2)
                y = (screen_height // 2) - (desired_height // 2)

                popup.geometry(f"{desired_width}x{desired_height}+{x}+{y}")

        # Gets strings from textboxes

        class_str = class_input.get()
        if not class_str:
            class_str = "ERROR. Must Enter Class"
        else:
            class_s = class_str.upper()
        
        short_str = short_input.get()
        if not short_str:
            short_str = "ERROR. Must Enter Name"
        else:
            short_s = short_str
        
        long_str = long_input.get()
        if not long_str:
            long_str = "None"
        
        materials_str =  materials_input.get()
        if not materials_str:
            materials_str = "None"
        
        skills_str = skills_input.get()
        if not skills_str:
            links_str = "None"
              
        text_str = text_input.get()
        if not text_str:
            text_str = "None"

        standard_str = standard_input.get()
        if not standard_str:
            standard_str = "None"
        
        # Splits Into Lists
        
        skills_ls = [x.strip() for x in skills_str.split(',')]
        materials_ls = [x.strip() for x in materials_str.split(',')]

        
        # Checks Data
        string = f"Information:\n\n"f"Class: {class_str}\n"f"Name: {short_str}\n"f"Long: {long_str}\n"f"Standard: {standard_str}\n"f"Skills: {', '.join(str(x) for x in skills_ls)}\n"f"Text: {text_str}\n"f"Materials: {', '.join(str(x) for x in materials_ls)}\n"

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        desired_width = int(screen_width * 0.15)
        label_output.config(text=string, wraplength=400, justify='left')

        # Arranges Buttons
        button_confirm = tk.Button(window, text='SAVE', command=on_save, bg=f'{button_color}')
        button_cancel = tk.Button(window, text='EXIT', command=on_exit, bg=f'{button_color}')
        button_confirm.grid(row=10, column = 0, pady=20, sticky='s')
        button_cancel.grid(row=10, column = 1, pady=20, sticky='s')
    
    # Main Window
    window = tk.Tk()

    #window.geometry("600x1000")
    window.title("Add Lesson")

    # Makes Text-Entry with Labels 
    class_label = tk.Label(window, text="Class:", bg=f'{window_color}', fg='black')
    class_input = tk.Entry(window, bg=f'{label_color}', fg='black')
    
    short_label = tk.Label(window, text="Short name of lesson:", bg=f'{window_color}', fg='black')
    short_input = tk.Entry(window, bg=f'{label_color}', fg='black')

    long_label = tk.Label(window, text="Long description of lesson:", bg=f'{window_color}', fg='black')
    long_input = tk.Entry(window, bg=f'{label_color}', fg='black')

    standard_label = tk.Label(window, text="Enduring Understanding:", bg=f'{window_color}', fg='black')
    standard_input = tk.Entry(window, bg=f'{label_color}', fg='black')

    skills_label = tk.Label(window, text="Skills or Essential Knowledge:", bg=f'{window_color}', fg='black')
    skills_input = tk.Entry(window, bg=f'{label_color}', fg='black')

    text_label = tk.Label(window, text="Primary text to be used:", bg=f'{window_color}', fg='black')
    text_input = tk.Entry(window, bg=f'{label_color}', fg='black')
    
    materials_label = tk.Label(window, text="List of materials, sep. by commas:", bg=f'{window_color}', fg='black')
    materials_input = tk.Entry(window, bg=f'{label_color}', fg='black')
  
    button_submit = tk.Button(window, text="Submit", command=on_submit, bg=f'{button_color}', fg='black')

    button_view = tk.Button(window, text="View Lessons", command=on_view, bg=f'{button_color}', fg='black')

    label_output = tk.Label(window, text="", bg=f'{window_color}', fg='black')
    
    # Arranges to Grid
    class_label.grid(row=0, column=0, padx=5, pady=5)
    class_input.grid(row=0, column=1, padx=5, pady=5)
    
    short_label.grid(row=1, column=0, padx=5, pady=5)
    short_input.grid(row=1, column=1, padx=5, pady=5)
    
    long_label.grid(row=2, column=0, padx=5, pady=5)
    long_input.grid(row=2, column=1, padx=5, pady=5)

    standard_label.grid(row=3, column=0, padx=5, pady=5)
    standard_input.grid(row=3, column=1, padx=5, pady=5)

    skills_label.grid(row=4, column=0, padx=5, pady=5)
    skills_input.grid(row=4, column=1, padx=5, pady=5)
    
    text_label.grid(row=5, column=0, padx=5, pady=5)
    text_input.grid(row=5, column=1, padx=5, pady=5)

    materials_label.grid(row=6, column=0, padx=5, pady=5)
    materials_input.grid(row=6, column=1, padx=5, pady=5)

    button_submit.grid(row=7, column=1, pady=10)

    button_view.grid(row=7, column=0, pady=10, padx=5)
    label_output.grid(row=8, columnspan=2, pady=20)

    # Set the window size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    desired_width = int(screen_width * 0.3)
    desired_height = int(screen_height * 0.7)

    x = (screen_width // 2) - (desired_width // 2)
    y = (screen_height // 2) - (desired_height // 2)

    window.geometry(f"{desired_width}x{desired_height}+{x}+{y}")
    window.configure(bg=f'{window_color}')
    window.mainloop()



