from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from formatting import convert_solution_to_schedule, show_schedule
from constants import N_CHUNKS, N_CHUNKS_PER_DAY

# TODO: move constants to constants file
chunks = list(range(0, N_CHUNKS)) 

empty_name = "_"
activities = [empty_name]

# Activity names must be provided first before adding events and tasks as 
# they are required to create the binary variables for the problem
def add_activity(name):
    activities.append(name)

add_activity("MaO")
add_activity("CMPS")
add_activity("HDMA")
add_activity("PLDI")
add_activity("Lunch")

add_activity("HW1")

# Define the problem
# Create a binary variable for each hour-activity pair
# Objective function: maximize free time
prob = LpProblem("Schedule_Optimization", LpMaximize)
x = LpVariable.dicts("schedule", (chunks, activities), cat='Binary')
prob += lpSum(x[c][empty_name] for c in chunks)

# Assumes that each chunk is 30 minutes
def daytime_to_start_chunk(day, time):
    # ("Monday", 9) -> 0
    # ("Tuesday", 12) -> 11
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    chunk_index = days.index(day) * N_CHUNKS_PER_DAY

    hour, minute = time.split(":")
    chunk_index += (int(hour) - 9) * 2
    chunk_index += 1 if int(minute) == 30 else 0
    return chunk_index

# ADDING EVENTS
# Event are items that are fixed and cannot be changed
# They are defined by the start hour and UP TO the end hour 
def add_event(prob, name, start_daytime, end_daytime):
    start = daytime_to_start_chunk(*start_daytime)
    end = daytime_to_start_chunk(*end_daytime)
    for c in range(start, end):
        prob += x[c][name] == 1

add_event(prob, "MaO", ("Tuesday", "13:00"), ("Tuesday", "14:30"))
add_event(prob, "MaO", ("Friday", "13:00"), ("Friday", "14:30"))

add_event(prob, "CMPS", ("Monday", "09:00"), ("Monday", "10:30"))
add_event(prob, "CMPS", ("Thursday", "09:00"), ("Thursday", "10:30"))

add_event(prob, "HDMA", ("Wednesday", "14:30"), ("Wednesday", "17:30"))

add_event(prob, "PLDI", ("Monday", "10:30"), ("Monday", "12:00"))
add_event(prob, "PLDI", ("Thursday", "10:30"), ("Thursday", "12:00"))

add_event(prob, "Lunch", ("Monday", "12:00"), ("Monday", "13:00"))
add_event(prob, "Lunch", ("Tuesday", "12:00"), ("Tuesday", "13:00"))
add_event(prob, "Lunch", ("Wednesday", "12:00"), ("Wednesday", "13:00"))
add_event(prob, "Lunch", ("Thursday", "12:00"), ("Thursday", "13:00"))
add_event(prob, "Lunch", ("Friday", "12:00"), ("Friday", "13:00"))

# ADDING TASKS
# Tasks are items that are flexible and can be moved around
# They are defined by the number of HOURS needed, the earliest start hour, and the latest end hour
def add_task(prob, name, time_required, start_daytime, end_daytime):
    start = daytime_to_start_chunk(*start_daytime)
    end = daytime_to_start_chunk(*end_daytime)
    chunks_required = time_required * 2

    # Constraints: homework for 3 hours after class
    prob += lpSum(x[c][name] for c in chunks) == chunks_required
    # After start hour
    prob += lpSum(x[c][name] for c in chunks[:start]) == 0
    # Up to and including deadline hour
    prob += lpSum(x[c][name] for c in chunks[:end]) == chunks_required

# Adding constraint for task HW1 that takes 3 hours and starts after 11 on Monday with
# a deadline at 12 on Tuesday
add_task(prob, "HW1", 10, ("Monday", "10:30"), ("Thursday", "19:00"))

# Constriant: Each hour can only have one activity
for c in chunks:
    prob += lpSum(x[c][a] for a in activities) == 1

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

# Print the schedule
# for c in chunks:
#     for a in activities:
#         if x[c][a].value() == 1:
#             print(f"{c}: {a}")

sched = convert_solution_to_schedule(x, chunks, activities)
show_schedule(sched)