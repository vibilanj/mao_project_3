from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

n_hours = 40
hours = list(range(0, n_hours)) 

activities = ["free", "class", "hw"]

# Define the problem
prob = LpProblem("Schedule_Optimization", LpMaximize)

# Create a binary variable for each hour-activity pair
x = LpVariable.dicts("schedule", (hours, activities), cat='Binary')

# Objective function: maximize free time
prob += lpSum(x[h]["free"] for h in hours)

# Constraints: class from hour 1 to 2
for h in range(0, 2):
    prob += x[h]["class"] == 1

# Constraints: homework for 3 hours after class
prob += lpSum(x[h]["hw"] for h in hours) == 3

# After start hour
start_hour = 2
prob += lpSum(x[h]["hw"] for h in hours[:start_hour]) == 0

# Up to and including deadline hour
deadline_hour = 6
prob += lpSum(x[h]["hw"] for h in hours[:deadline_hour]) == 3

# Each hour can only have one activity
for h in hours:
    prob += lpSum(x[h][a] for a in activities) == 1

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

# Print the schedule
# for h in hours:
#     for a in activities:
#         if x[h][a].value() == 1:
#             print(f"{h}: {a}")

def convert_solution_to_schedule(sol):
    schedule = []
    for h in hours:
        for a in activities:
            if sol[h][a].value() == 1:
                schedule.append(a)
    return schedule

def make_daily_sparse_schedule(day_sched):
    current_activity = day_sched[0]
    sparse_schedule = []
    for i in range(1, len(day_sched)):
        if day_sched[i] != current_activity:
            sparse_schedule.append(current_activity)
            current_activity = day_sched[i]
        else:
            sparse_schedule.append("")
    sparse_schedule.append(current_activity)
    return sparse_schedule


def make_full_sparse_schedule(sched):
    mon = make_daily_sparse_schedule(sched[:8])
    tue = make_daily_sparse_schedule(sched[8:16])
    wed = make_daily_sparse_schedule(sched[16:24])
    thu = make_daily_sparse_schedule(sched[24:32])
    fri = make_daily_sparse_schedule(sched[32:40])
    return mon, tue, wed, thu, fri

def convert_chunk_to_time(chunk):
    # 1 -> 09:00 - 10:00
    # 2 -> 10:00 - 11:00
    # 3 -> 11:00 - 12:00
    # 4 -> 12:00 - 13:00
    # 5 -> 13:00 - 14:00
    # 6 -> 14:00 - 15:00
    # 7 -> 15:00 - 16:00
    # 8 -> 16:00 - 17:00
    hour = chunk % 8
    start = 9 + hour
    end = start + 1
    return f"{start:02d}:00 - {end:02d}:00"


def show_schedule(sol):
    #               |  MON  |  TUE  |  WED  |  THU  |  FRI  |
    #--------------------------------------------------------
    # 09:00 - 10:00 |       |_     _|_     _|_     _|_     _|
    # 10:00 - 11:00 |_ABCDE_|_     _|_     _|_     _|_     _|

    schedule = convert_solution_to_schedule(sol)
    mon, tue, wed, thu, fri = make_full_sparse_schedule(schedule)

    print("               |  MON  |  TUE  |  WED  |  THU  |  FRI  |")
    print("--------------------------------------------------------")
    for i in range(0, 8):
        time = convert_chunk_to_time(i)
        print(f" {time} | {mon[i]:>5} | {tue[i]:>5} | {wed[i]:>5} | {thu[i]:>5} | {fri[i]:>5} |")

show_schedule(x)