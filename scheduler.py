from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
from constants import N_CHUNKS, EMPTY_NAME
from formatting import daytime_to_start_chunk


# Scheduler class that creates and stores the optimization problem and its
#   constraints. It takes a list of activities for initialization. Provides
#   methods to add events and tasks to the problem and solve it.
class Scheduler:
    def __init__(self, activities):
        self.chunks = list(range(0, N_CHUNKS))
        self.activities = activities

        # Defining the integer programming problem by creating binary
        #   variables for each timechunk-activity pair. The objective
        #   function is set to maximize free time.
        self.prob = LpProblem("Schedule_Optimization", LpMaximize)
        self.x = LpVariable.dicts("schedule", (self.chunks, activities), cat='Binary')
        self.prob += lpSum(self.x[c][EMPTY_NAME] for c in self.chunks)


    # Event are items that are fixed in time. They are defined by the
    #   name of the event, the start day-time and the ending day-time.
    def add_event(self, name, start_daytime, end_daytime):
        start = daytime_to_start_chunk(*start_daytime)
        end = daytime_to_start_chunk(*end_daytime)
        for c in range(start, end):
            self.prob += self.x[c][name] == 1


    # Tasks are items that are flexible and can be moved around by the
    #   scheduler. They are defined by the name of the task, the number of
    #   number of hours needed to complete the task, the starting day-time,
    #   and the deadline day-time.
    def add_task(self, name, time_required, start_daytime, end_daytime):
        start = daytime_to_start_chunk(*start_daytime)
        end = daytime_to_start_chunk(*end_daytime)
        chunks_required = time_required * 2
        self.prob += lpSum(self.x[c][name] for c in self.chunks) == chunks_required
        self.prob += lpSum(self.x[c][name] for c in self.chunks[:start]) == 0
        self.prob += lpSum(self.x[c][name] for c in self.chunks[:end]) == chunks_required


    # Adds the final constraint that each time chunk can only have one
    #   activity. Solves the integer programming problem and returns the
    #   solution.
    def solve(self):
        for c in self.chunks:
            self.prob += lpSum(self.x[c][a] for a in self.activities) == 1
        self.prob.solve(PULP_CBC_CMD(msg=0))
        return self.x
