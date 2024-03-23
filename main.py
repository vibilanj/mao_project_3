from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD
from formatting import convert_solution_to_schedule, show_schedule

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

sched = convert_solution_to_schedule(x, hours, activities)
show_schedule(sched)