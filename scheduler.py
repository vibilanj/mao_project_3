from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
from constants import N_CHUNKS, EMPTY_NAME
from formatting import daytime_to_start_chunk


class Scheduler:
    def __init__(self, activities):
        self.chunks = list(range(0, N_CHUNKS))
        self.activities = activities

        # Define the problem by creating binary variables for each hour-activity pair
        # and setting the objective function to maximize free time
        self.prob = LpProblem("Schedule_Optimization", LpMaximize)
        self.x = LpVariable.dicts("schedule", (self.chunks, activities), cat='Binary')
        self.prob += lpSum(self.x[c][EMPTY_NAME] for c in self.chunks)


    # ADDING EVENTS: Event are items that are fixed and cannot be changed.
    #   They are defined by the start hour and UP TO the end hour 
    def add_event(self, name, start_daytime, end_daytime):
        start = daytime_to_start_chunk(*start_daytime)
        end = daytime_to_start_chunk(*end_daytime)
        for c in range(start, end):
            self.prob += self.x[c][name] == 1


    # ADDING TASKS: Tasks are items that are flexible and can be moved around.
    #   They are defined by the number of HOURS needed, the earliest start hour,
    #   and the latest end hour
    def add_task(self, name, time_required, start_daytime, end_daytime):
        start = daytime_to_start_chunk(*start_daytime)
        end = daytime_to_start_chunk(*end_daytime)
        chunks_required = time_required * 2

        # Number of hours required
        self.prob += lpSum(self.x[c][name] for c in self.chunks) == chunks_required
        # Task can only be started after the start hour
        self.prob += lpSum(self.x[c][name] for c in self.chunks[:start]) == 0
        # Task must be finished before the end hour
        self.prob += lpSum(self.x[c][name] for c in self.chunks[:end]) == chunks_required


    def solve(self):
        # Constriant: Each hour can only have one activity
        for c in self.chunks:
            self.prob += lpSum(self.x[c][a] for a in self.activities) == 1

        self.prob.solve(PULP_CBC_CMD(msg=0))
        return self.x
