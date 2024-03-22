from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, PULP_CBC_CMD

hours = [
    "Monday_Hour_1",
    "Monday_Hour_2",
    "Monday_Hour_3",
    "Monday_Hour_4",
    "Monday_Hour_5",
    "Monday_Hour_6",
    "Monday_Hour_7",
    "Monday_Hour_8",
    "Tuesday_Hour_1",
    "Tuesday_Hour_2",
    "Tuesday_Hour_3",
    "Tuesday_Hour_4",
    "Tuesday_Hour_5",
    "Tuesday_Hour_6",
    "Tuesday_Hour_7",
    "Tuesday_Hour_8"
]

activities = ["class", "homework", "free_time"]

# Define the problem
prob = LpProblem("Schedule_Optimization", LpMaximize)

# Create a binary variable for each hour-activity pair
x = LpVariable.dicts("schedule", (hours, activities), cat='Binary')

# Objective function: maximize free time
prob += lpSum(x[h]["free_time"] for h in hours)

# Constraints: class from hour 1 to 2
for h in ["Monday_Hour_1", "Monday_Hour_2"]:
    prob += x[h]["class"] == 1

# Constraints: homework for 3 hours after class
prob += lpSum(x[h]["homework"] for h in hours) == 3

start_hour = "Monday_Hour_3"
start_index = hours.index(start_hour)
prob += lpSum(x[h]["homework"] for h in hours[:start_index]) == 0

deadline_hour = "Tuesday_Hour_4"
deadline_index = hours.index(deadline_hour)
prob += lpSum(x[h]["homework"] for h in hours[:deadline_index+1]) == 3


# Each hour can only have one activity
for h in hours:
    prob += lpSum(x[h][a] for a in activities) == 1

# Solve the problem
prob.solve(PULP_CBC_CMD(msg=0))

# Print the schedule
for h in hours:
    for a in activities:
        if x[h][a].value() == 1:
            print(f"{h}: {a}")