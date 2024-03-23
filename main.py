from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from formatting import convert_solution_to_schedule, show_schedule

n_chunks = 40
chunks = list(range(0, n_chunks)) 

empty_name = "_"
activities = [empty_name]

# Activity names must be provided first before adding events and tasks as 
# they are required to create the binary variables for the problem
def add_activity(name):
    activities.append(name)

add_activity("MaO")
add_activity("HW1")

# Define the problem
# Create a binary variable for each hour-activity pair
# Objective function: maximize free time
prob = LpProblem("Schedule_Optimization", LpMaximize)
x = LpVariable.dicts("schedule", (chunks, activities), cat='Binary')
prob += lpSum(x[c][empty_name] for c in chunks)

def daytime_to_start_chunk(day, time):
    # ("Monday", 9) -> 0
    # ("Tuesday", 12) -> 11
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_start = days.index(day) * 8
    return day_start + time - 9

# ADDING EVENTS
# Event are items that are fixed and cannot be changed
# They are defined by the start hour and UP TO the end hour 
def add_event(prob, name, start_daytime, end_daytime):
    start = daytime_to_start_chunk(*start_daytime)
    end = daytime_to_start_chunk(*end_daytime)
    for c in range(start, end):
        prob += x[c][name] == 1

# Adding constraint for class MaO from 09 to 11 on Monday
add_event(prob, "MaO", ("Monday", 9), ("Monday", 11))
add_event(prob, "MaO", ("Thursday", 9), ("Thursday", 11))

# ADDING TASKS
# Tasks are items that are flexible and can be moved around
# They are defined by the number of hours needed, the earliest start hour, and the latest end hour
def add_task(prob, name, time_required, start_daytime, end_daytime):
    start = daytime_to_start_chunk(*start_daytime)
    end = daytime_to_start_chunk(*end_daytime)

    # Constraints: homework for 3 hours after class
    prob += lpSum(x[c][name] for c in chunks) == time_required
    # After start hour
    prob += lpSum(x[c][name] for c in chunks[:start]) == 0
    # Up to and including deadline hour
    prob += lpSum(x[c][name] for c in chunks[:end]) == 3

# Adding constraint for task HW1 that takes 3 hours and starts after 11 on Monday with
# a deadline at 12 on Tuesday
add_task(prob, "HW1", 3, ("Monday", 11), ("Tuesday", 12))

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