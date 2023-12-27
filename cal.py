# Imports
from datetime import datetime, timedelta
import itertools

# Globals
startend_file = "defaults/startend_days.txt"
vacation_days_file = "defaults/vacation_days.txt"
block_sched_file = "defaults/blockschedule.txt"

block_pattern = ['A', 'G', 'F', 'E', 'D', 'C', 'B']

today = datetime.now().date()

def firstlast():
    # First and Last Day
    startend = []
    with open(startend_file, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                startend.append(line.strip())

    start_date = datetime.strptime(startend[0], "%Y-%m-%d")
    end_date = datetime.strptime(startend[1], "%Y-%m-%d")
    
    return (start_date, end_date)

def rotsched():

    keydate = firstlast()
    start_date = keydate[0]
    end_date = keydate[1]

    # Vacation Days
    vacation_days = []
    with open(vacation_days_file, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                vacation_days.append(line.strip())

    # Create an empty dictionary to store the schedule
    schedule = {}

    # Generate the schedule for each weekday
    current_date = start_date
    block_index = 0  # Initialize the counter for block indexing
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Exclude weekends (Saturday: 5, Sunday: 6)
            date_str = current_date.strftime('%Y-%m-%d')
            if date_str not in vacation_days:
                block = block_pattern[block_index]
                schedule[current_date] = block
                block_index = (block_index + 1) % len(block_pattern)  # Increment and wrap around the block index
        current_date += timedelta(days=1)
    
    return schedule

def printer(schedule):
    # Print the generated schedule
    for date, block in schedule.items():
        print(f"{date.strftime('%Y-%m-%d')}")
        for clas, period in block.items():
            print(f"\t{clas} -- {period[0]}")

def schedmaker():
    a_day = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[]}
    b_day = {'B':[],'C':[],'D':[],'E':[],'F':[],'G':[]}
    c_day = {'C':[],'D':[],'E':[],'F':[],'G':[],'A':[]}
    d_day = {'D':[],'E':[],'F':[],'G':[],'A':[],'B':[]}
    e_day = {'E':[],'F':[],'G':[],'A':[],'B':[],'C':[]}
    f_day = {'F':[],'G':[],'A':[],'B':[],'C':[],'D':[]}
    g_day = {'G':[],'A':[],'B':[],'C':[],'D':[],'E':[]}
    schedule = rotsched()
    for date, block in schedule.items():
        if block == 'A':
           schedule[date] = a_day
        elif block == 'B':
            schedule[date] = b_day
        elif block == 'C':
            schedule[date] = c_day
        elif block == 'D':
            schedule[date] = d_day
        elif block == 'E':
            schedule[date] = e_day
        elif block == 'F':
            schedule[date] = f_day
        elif block == 'G':
            schedule[date] = g_day
    
    # Classes, PLCs, Duty
    PLC = [2,5]
    lunch = 4
    preps = [1,3,6]
    duty = ''

    blocklist = []
    with open(block_sched_file, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                blocklist.append(line.strip())

    for i in range(len(blocklist)):
        if blocklist[i] == 'DUTY':
            duty = chr(i+97).upper()

    ablock = [blocklist[0]]
    bblock = [blocklist[1]]
    cblock = [blocklist[2]]
    dblock = [blocklist[3]]
    eblock = [blocklist[4]]
    fblock = [blocklist[5]]
    gblock = [blocklist[6]]

    for date, agenda in schedule.items():
        # PLC
        for position in PLC:
            value = next(itertools.islice(agenda, position-1, position))
            if value == duty:
                schedule[date][duty] = ['PLC']
        # Lunch
        value = next(itertools.islice(agenda, lunch-1, lunch))
        if value == duty:
            schedule[date][duty] = ['DUTY']
        # Duty Preps
        for position in preps:
            value = next(itertools.islice(agenda, position-1, position))
            if value == duty:
                schedule[date][duty] = ['PREP']
        
        # Class 
        for block, info in agenda.items():
            if block == duty:
                pass
            else:
                if block == 'A':
                    agenda[block] = ablock
                elif block == 'B':
                    agenda[block] = bblock
                elif block == 'C':
                    agenda[block] = cblock
                elif block == 'D':
                    agenda[block] = dblock
                elif block == 'E':
                    agenda[block] = eblock
                elif block == 'F':
                    agenda[block] = fblock
                elif block == 'G':
                    agenda[block] = gblock

    return schedule
