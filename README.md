# Modelling and Optimization Project 3

## Introduction

This project is a scheduling tool that helps students plan their weekly schedules efficiently. The tool takes into account various constraints such as class timings, assignment openings, and assignment deadlines to generate an optimized schedule. The core functionality of the program involves formulating the scheduling problem as an integer programming model, where classes and assignments are represented as decision variables. Constraints are defined and the objective function is designed to maximize free time.

## Implementation Details

The project is implemented in Python. Initially, I was planning to use the `pyomo` library to model and solve the integer programming problem. However, I found that the `pulp` library is more user-friendly and easier to work with for this project. Therefore, I decided to use the `pulp` library to model and solve the scheduling problem.

Another change I made was to read the schedule requirements from a text file instead of taking user input directly. This makes it easier for the user to input complex schedules and constraints without having to interact with the program through a command line interface. The program reads the schedule requirements from the file and generates an optimized schedule based on the constraints and preferences provided.

Here are the descriptions of the five Python files and the input file. Furthermore, the code in each file is documented with comments to explain each part in greater detail.

### `constants.py`

This file contains the constants used throughout the program. The constants include the number of time chunks per day, the total number of time chunks, and the name that represents unscheduled time chunks.

### `parse.py`

This file contains the `ScheduleParser` class which reads the schedule requirements from the file, validates them and stores them in a structured format. The class is used by the main program by providing it with the file name and calling the `parse_schedule` method. This method reads the file, cleans the lines and constructs the list of activites, and the list of arguments required to add events (using the `handle_event` method) and tasks (using the `handle_task` method) to the problem. The specifics regarding the validation and creation of the structured data are explained in the comments in the file.

### `scheduler.py`

This file contains the `Scheduler` class which is responsible for creating the integer programming model, adding the constraints and the objective function, and solving the model. The class is used by the main program by providing it with the list of activites. This allows the class to initialize the integer programming model with the binary variables for each time chunk and activity pair. The objective function is also defined at this stage to maximize the free time.

Then, the main program uses the `add_event` and `add_task` methods to add the events and tasks to the model. For each event, the constaints that the event must take place between the specified starting and ending time chunks is added to the problem. For each task, the constraint that the task must have enough time chunks assigned to it between the specified starting and ending time chunks is added to the problem.

Initially, there were three constraints for each task with each constraint being added separately. There was a constraint that the task must have no time chunks assigned to it before the starting time chunk, a constraint that the task must have enough time chunks assigned to it before the ending time chunk, and a constraint that the task must have no time chunks assigned to it after the ending time chunk.

However, I found that combining the three constraints into a single constraint that specifies the range of time chunks for the task improved the performance of the scheduler. This higlights the importance of formulating the problem correctly and efficiently.

Lastly, the main program calls the `solve` method. First, this method adds the final constraint that each time chunk can only have a single activity. Then, the inbuilt `PULP_CBC_CMD` solver is used solves the integer programming model. Finally, the method returns the optimized schedule as a list of assigned activities.

### `formatting.py`

This file contains the functions related to the formatting of the different data types used in the project. The `daytime_to_start_chunk` function takes in a day and time and returns the index of the chunk with the interval that starts at that time. It is used to parse the schedule requirements file. The `convert_chunk_to_interval` function takes in a chunk index and returns the start and end times of the interval that the chunk represents. This is used by the `show_schedule` function which takes in the list of assigned activities and prints the schedule in a human-readable format.

### `main.py`

This file is the main runner file. It contains the command line argument parsing logic and the main program flow. The user can provide the schedule requirements file as a command line argument with the `--schedule` flag. Additionally, the user can run the program with the `-h` flag to see the help message and the available arguments.

If no file is provided, the program reads the schedule requirements from the `schedule.txt` file by default. The default file contains sample schedule requirements in a structured format with detailed comments on how to add events and tasks to the schedule.

The program then reads the schedule requirements from the file using the `ScheduleParser` class. With this data, it can then create and add constraints to the integer programming model using the `Scheduler` class. Lastly, it solves the problem to generate the optimized schedule. The schedule is then printed to the terminal in a human-readable format.

### `schedule.txt`

This file contains the sample schedule requirements that the program reads by default. The file is structured with comments to explain how to add events and tasks to the schedule. The file contains sample data for a student's weekly schedule with classes, assignments, and other activities.

## Further Improvements

## Notes:
1. Activity names must be provided first before adding events and tasks as they are required to create the binary variables for the problem. This is one of the reasons why it is better to read the schedule from a file.
2. The program doesn't check if the schedule is possible to be optimized, or whether the provided solution meets all the constraints.
3. The program might break when too many tasks and events are added. Other solvers are available within PuLP, but they are not as user-friendly as the default solver. They would have to be installed by the user and linked to the program. However, these solvers might be better at handling large problems.

## How to Run

### Setting up the environment

1. Ensure that you have a working install of Python 3.11.8.
2. Navigate to the directory containing the project in your terminal.
3. Create a Python virtual environment by running `python3 -m venv .venv`.
4. Use the virtual environment with `source .venv/bin/activate`.
5. Install the necessary packages using `pip install -r requirements.txt`.

### Running the program

1. Navigate to the project directory.
2. Make sure that the virtual environment is activated. If it is not, use `source .venv/bin/activate`.
3. Run the program using `python main.py` and pass in any optional arguments.
    - You can use the `-h` flag to see the help message and the available arguments.
4. By default, the program will read the schedule requirements from the `schedule.txt` file.
    - You can instead  provide a different file by using the `--schedule` argument.
    - An example command would be `python main.py --schedule my_schedule.txt`. This would read the schedule requirements from the `my_schedule.txt` file.
4. View the schedule created by the integer programming solver in the terminal output.
