from pyomo.environ import *

# Create a concrete model
model = ConcreteModel()

# Define sets for hours and tasks
days = range(5)  # Assuming 5 days in a week
hours_per_day = range(8)  # Assuming 8 hours per day
hours = [(day, hour) for day in days for hour in hours_per_day]
tasks = ['Class_A', 'Class_B', 'Class_C', 'Assignment_A', 'Assignment_B']

# Define decision variables
model.x = Var(tasks, hours, within=Binary)

# Define class durations
class_durations = {'Class_A': 2, 'Class_B': 3, 'Class_C': 2}

# Define assignment durations and deadlines
assignment_durations = {'Assignment_A': 8, 'Assignment_B': 2}
assignment_deadlines = {'Assignment_A': 4 * 8 - 1, 'Assignment_B': 3 * 8 - 1}  # Deadline hour (index in hours list)

# Define constraints
# Ensure each task happens only once each hour
model.only_one_task_per_hour_constraint = ConstraintList()
for hour in hours:
    model.only_one_task_per_hour_constraint.add(sum(model.x[task, hour] for task in tasks) <= 1)

# Ensure classes are contiguous at the hour level
model.class_contiguity_constraint = ConstraintList()
for task in ['Class_A', 'Class_B', 'Class_C']:
    for day in days:
        for start_hour in range(len(hours_per_day) - class_durations[task] + 1):
            hours_in_block = [(day, start_hour + i) for i in range(class_durations[task])]
            model.class_contiguity_constraint.add(sum(model.x[task, hour] for hour in hours_in_block) == class_durations[task])

# Ensure assignments start after the corresponding classes
model.assignment_start_constraint = ConstraintList()
model.assignment_start_constraint.add(model.x['Assignment_A', (0, 0)] >= model.x['Class_A', (0, 0)])
model.assignment_start_constraint.add(model.x['Assignment_B', (2, 0)] >= model.x['Class_B', (1, 0)])

# Ensure assignments are completed by the deadlines
model.assignment_deadline_constraint = ConstraintList()
for task in ['Assignment_A', 'Assignment_B']:
    model.assignment_deadline_constraint.add(sum(model.x[task, hour] for hour in hours[:assignment_deadlines[task]+1]) >= assignment_durations[task])

# Define objective function (minimize the total number of tasks)
model.objective = Objective(expr=sum(model.x[task, hour] for task in tasks for hour in hours), sense=minimize)

# Solve the model
solver = SolverFactory('glpk')
solver.solve(model)

# Print the results
print("Optimal Schedule:")
for hour in hours:
    print("Day", hour[0], "Hour", hour[1], ':')
    for task in tasks:
        if model.x[task, hour].value == 1:
            print("  ", task)
