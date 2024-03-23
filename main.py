from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from formatting import convert_solution_to_schedule, show_schedule
from constants import N_CHUNKS, N_CHUNKS_PER_DAY, EMPTY_NAME
from parse import parse_schedule

chunks = list(range(0, N_CHUNKS)) 

# NOTE: Activity names must be provided first before adding events and tasks as
# they are required to create the binary variables for the problem > One of the
# reasons why it is better to read the schedule from a file
activities, event_args, task_args = parse_schedule()

# Define the problem by creating binary variables for each hour-activity pair
# and setting the objective function to maximize free time
prob = LpProblem("Schedule_Optimization", LpMaximize)
x = LpVariable.dicts("schedule", (chunks, activities), cat='Binary')
prob += lpSum(x[c][EMPTY_NAME] for c in chunks)

# NOTE: Assumes that each chunk is 30 minutes
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

for event_args in event_args:
    add_event(prob, *event_args)

# ADDING TASKS
# Tasks are items that are flexible and can be moved around
# They are defined by the number of HOURS needed, the earliest start hour, and the latest end hour
def add_task(prob, name, time_required, start_daytime, end_daytime):
    start = daytime_to_start_chunk(*start_daytime)
    end = daytime_to_start_chunk(*end_daytime)
    chunks_required = time_required * 2

    # Number of hours required
    prob += lpSum(x[c][name] for c in chunks) == chunks_required
    # Task can only be started after the start hour
    prob += lpSum(x[c][name] for c in chunks[:start]) == 0
    # Task must be finished before the end hour
    prob += lpSum(x[c][name] for c in chunks[:end]) == chunks_required

for task_args in task_args:
    add_task(prob, *task_args)

# Constriant: Each hour can only have one activity
for c in chunks:
    prob += lpSum(x[c][a] for a in activities) == 1

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

sched = convert_solution_to_schedule(x, chunks, activities)
show_schedule(sched)

# NOTE: doesn't check if the schedule is possible to be optimized, or whether all the constraints are met