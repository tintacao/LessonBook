import cal
import itertools
import tkinter as tk
from datetime import datetime, timedelta
import lessonmk
import agendamk

import colors

import ctypes

## COMMENT OUT IF LINUX
#try: # >= win 8.1
#    ctypes.windll.shcore.SetProcessDpiAwareness(2)
#except: # win 8.0 or less
#    ctypes.windll.user32.SetProcessDPIAware()

# Globals
calendar = cal.schedmaker()
today = datetime.now()
colors = colors.getcolor()
button_color = colors[0]
button_color_ag = colors[1]
button_color_nw = colors[2]
label_color = colors[3]
window_color = colors[4]
button_color_red = colors[5]

firstlast = cal.firstlast()
start_date = firstlast[0]

# Functions

# Get monday for any given day of week
def getmon(date):
    weekday = date.weekday()
    first_day = date - timedelta(days=weekday)
    return first_day

# MAIN
def main():

    # Updates details and labels
    def update_label(date):
        for button in window.grid_slaves():
            if button.winfo_exists():
                button.grid_forget()
        populate(date)
        window.update()

    # Any time a class is clicked
    def button_click(classname, period, date, agenda):

        data = agendamk.getlist()
        lessons = data[1]
        agendas = data[0]
        
        # Adds lesson plan to selected day/class
        def add_plan():
            agendamk.add_agenda(classname, period, date)

        # Changes lesson plan to selected day/class
        def edit_plan():
            
            # Delete Button
            def deleteit():
                agendamk.rm_agenda(classname, period, date)
                nwindow.destroy()
                update_label(datetime.strptime(date, "%Y-%m-%d"))
            
            # Cancel Button
            def cancelit():
                nwindow.destroy()

            nwindow = tk.Toplevel()
            nwindow.title("Delete Lessons")
            nwindow.configure(bg=f'{window_color}')
    
            screen_width = nwindow.winfo_screenwidth()
            screen_height = nwindow.winfo_screenheight()
            
            label = tk.Label (nwindow, text="Are you sure you want to delete this lesson?", bg=f'{window_color}')
            label.grid(row=0, columnspan=2, pady=20)

            delbutt = tk.Button(nwindow, text='Delete', command=deleteit, bg=f'{button_color}')
            delbutt.grid(row=1, column=0, padx=10, pady=10, sticky='news')
            canbutt = tk.Button(nwindow, text="Cancel", command=cancelit, bg=f'{button_color}')
            canbutt.grid(row=1, column=1, padx=10, pady=10, sticky='news')
            
            win_width = 370
            win_height = 130
            x = (screen_width // 2) - (win_width // 2)
            y = (screen_height // 2) - (win_height // 2)

            nwindow.geometry(f"{win_width}x{win_height}+{x}+{y}")
            
        # Arranges Buttons
        if not agenda:
            button_addPlan = tk.Button(window, text='Add Lesson Plan', command=add_plan, bg=f'{button_color_nw}', width=15)
            lesson = ''
            button_addPlan.grid(row=10, columnspan=6, pady=5, sticky='s')
        else:
            button_editPlan = tk.Button(window, text='Delete Lesson Plan', command=edit_plan, bg=f'{button_color_nw}', width=15)
            button_editPlan.grid(row=10, columnspan=6, pady=5, sticky='s')
            for lesson_full in lessons:
                if lesson_full['short'] == agenda['lesson']:
                    lesson = lesson_full

        label_details = tk.Label(window, text='', bg=f'{window_color}', width=100, height=9)
        label_details.grid(row=8, rowspan=2, columnspan=6, pady=5)
        try:
            label_details.config(text=f"Lesson - \t\t{lesson['short']}\n"f"Description - \t{lesson['long']}\n"f"Standard - \t{lesson['standard']}\n"f"Skills - \t\t{', '.join(str(x) for x in lesson['skills'])}\n"f"Text - \t\t{lesson['text']}\n"f"Materials - \t{', '.join(str(x) for x in lesson['materials'])}", justify="left", bg=f'{window_color}')
        except TypeError:
             label_details.config(text=f"\t{period}\n"f"\t{classname}\n"f"\t{date}")


                
    # Creates buttons and labels    
    def populate(inputday):
        data = agendamk.getlist()
        lessons = data[1]
        agendas = data[0]

        # Define the labels for rows and columns
        row_labels = ['1', '2', '3', '4\nLunch', '5', '6']

        ####### INPUT DATE

        weekstart = getmon(inputday)
        column_days = [(weekstart + timedelta(days=i)) for i in range(5)]
        column_labels = [(weekstart + timedelta(days=i)).strftime("%a \n%b %d") for i in range(5)]
        
        def add_lesson():
            lessonmk.add_lesson()
        
        # North West Buttons
        month_frame = tk.Frame(window)
        month_frame.config(bg=f'{window_color}')
        month_frame.grid(rowspan=2, column=0, sticky='nsew', padx=5, pady=5)
        
        # Next Week
        monthbutt = tk.Button(month_frame, text="Next Week", command= lambda d=(weekstart + timedelta(days=7)): update_label(d), bg=f'{button_color_nw}')
        
        # Last Week
        monthbutt2 = tk.Button(month_frame, text ="Last Week", command= lambda d=(weekstart - timedelta(days=7)): update_label(d), bg=f'{button_color_nw}')
        
        monthbutt.grid(row=1, column=1, pady=5, padx=5)
        monthbutt2.grid(row=1, column=0, pady=5)
        
        lessonadd = tk.Button(month_frame, text="Add Lesson", command=add_lesson, bg=f'{button_color_nw}')
        lessonadd.grid(row=0, columnspan=2, padx=0, pady=20, sticky='nsew')
        
        # Month Title
        titleTop = tk.Label(window, text=inputday.strftime("%B"), font=("Helvetica",24), bg=f'{window_color}')
        titleTop.grid(row=0, columnspan=6, pady=10)

        # Create and place the row labels
        for i, row_label in enumerate(row_labels):
            label = tk.Label(window, text=row_label, padx=10, pady=10, font=('Arial', 14), borderwidth=1, relief="ridge", bg=f'{label_color}')
            label.grid(row=i+2, column=0, sticky='news')

        # Create and place the column labels
        for i, col_label in enumerate(column_labels):
            label = tk.Label(window, text=col_label, padx=0, pady=10, font=('Arial', 12), borderwidth=1, relief="ridge", bg=f'{label_color}')
            label.grid(row=1, column=i+1, sticky='news')

        # Empty totals of class per week
        acount=0
        bcount=0
        ccount=0
        dcount=0
        ecount=0
        fcount=0
        gcount=0
        # Create and place the buttons
        for i, row in enumerate(row_labels):
            for k, col in enumerate(column_days):
                for day, sched in calendar.items():
                    if day == col:
                        period = next(itertools.islice(sched, i, i+1))
                        classname = sched[period][0]
                        # Count classes per week
                        if period == 'A':
                            acount+=1
                        elif period == 'B':
                            bcount+=1
                        elif period == 'C':
                            ccount+=1
                        elif period == 'D':
                            dcount+=1
                        elif period == 'E':
                            ecount+=1
                        elif period == 'F':
                            fcount+=1
                        elif period == 'G':
                            gcount+=1
                        # Checks if assignment is there
                        if not agendas:
                            agenda_new = {}
                            agenda_str = '----'
                            button_str = button_color
                        else:
                            for agenda_value in agendas:
                                date_str = day.strftime("%Y-%m-%d")
                                if agenda_value['class'] == classname and agenda_value['period'] == period and agenda_value['date'] == date_str:
                                    agenda_new = agenda_value
                                    agenda_str = agenda_new['lesson']
                                    if agenda_str == "NO SCHOOL":
                                        button_str = button_color_red
                                    elif "ABSENT" in agenda_str:
                                        button_str = button_color_red
                                    else:
                                        button_str = button_color_ag
                                    break
                                else:
                                    agenda_new = {}
                                    agenda_str = '----'
                                    button_str = button_color
                        
                        button = tk.Button(window, text=f"{period}\n{classname}\n{agenda_str}", command=lambda b=period, a=classname, c=day.strftime("%Y-%m-%d"), d=agenda_new: button_click(a, b, c, d), padx=10, pady=10, wraplength=175, bg=f'{button_str}')
                        button.grid(row=i+2, column=k+1, sticky='news')


        # Configure grid weights for even spacing
        for i in range(len(row_labels) + 5):
            window.grid_rowconfigure(i, weight=1, minsize=60)
        for i in range(len(column_labels) + 0):
            window.grid_columnconfigure(i+1, weight=1, uniform='column', minsize=50)        

        # Set lunch block to be higher
        window.grid_rowconfigure(5, weight=1, minsize=60)
        window.grid_rowconfigure(0, weight=1, minsize=90)
        window.grid_rowconfigure(1, weight=1, minsize=70)

        
        # Update button
        update_button = tk.Button(window, text="Update", command=lambda d=weekstart: update_label(d), bg=f'{button_color_nw}')
        update_button.grid(row=10, columnspan = 4, pady=5)
        
        label_details = tk.Label(window, text='\n\n\n\n\n\n\n\n', bg=f'{window_color}')
        label_details.grid(row=8, rowspan=2, columnspan=6, pady=10)

        label_totals = tk.Label(window, text=f'A -- {acount}\nB -- {bcount}\nC -- {ccount}\nD -- {dcount}\nE -- {ecount}\nF -- {fcount}\nG -- {gcount}', bg=f'{window_color}', font=('Arial', 14), padx=10, pady=20)
        label_totals.grid(row=8, column=0)
    
    # Create the tkinter window
    window = tk.Tk()

    # Set the window size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    desired_width = int(screen_width * 1)
    desired_height = int(screen_height * 0.9)

    x = (screen_width // 2) - (desired_width // 2)
    y = (screen_height // 2) - (desired_height // 2)

    window.geometry(f"{desired_width}x{desired_height}+{x}+0")
    #window.attributes("-fullscreen", True) 

    window.configure(bg=f'{window_color}')

    window
    
    today_year = today.year
    today_month = today.month
    today_day = today.day
    today_vari = f"{today_year}-{today_month}-{today_day}"
    today_date = datetime.strptime(today_vari, "%Y-%m-%d")


    populate(today_date)
    
    # Run the tkinter event loop
    window.mainloop()

main()
