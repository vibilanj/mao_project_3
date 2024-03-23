from constants import N_CHUNKS_PER_DAY

# TODO: cleanup signatures

def convert_solution_to_schedule(sol, chunks, activities):
    schedule = []
    for c in chunks:
        for a in activities:
            if sol[c][a].value() == 1:
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
    n = N_CHUNKS_PER_DAY
    mon = make_daily_sparse_schedule(sched[:n])
    tue = make_daily_sparse_schedule(sched[n:n*2])
    wed = make_daily_sparse_schedule(sched[n*2:n*3])
    thu = make_daily_sparse_schedule(sched[n*3:n*4])
    fri = make_daily_sparse_schedule(sched[n*4:n*5])
    return mon, tue, wed, thu, fri

def make_full_schedule(sched):
    n = N_CHUNKS_PER_DAY
    mon = sched[:n]
    tue = sched[n:n*2]
    wed = sched[n*2:n*3]
    thu = sched[n*3:n*4]
    fri = sched[n*4:n*5]
    return mon, tue, wed, thu, fri

# Assumes that each chunk is 30 minutes
def convert_chunk_to_time(chunk):
    # 0 -> 09:00 - 10:00
    # 8 -> 13:00 - 13:30
    day_chunk = chunk % N_CHUNKS_PER_DAY
    start_hour = 9 + int(day_chunk / 2)
    start_minute = "00" if day_chunk % 2 == 0 else "30"
    end_hour = start_hour if day_chunk % 2 == 0 else start_hour + 1
    end_minute = "00" if day_chunk % 2 == 1 else "30"
    return f"{start_hour:02d}:{start_minute} - {end_hour:02d}:{end_minute}"

def show_schedule(schedule):
    #               |  MON  |  TUE  |  WED  |  THU  |  FRI  |
    #--------------------------------------------------------
    # 09:00 - 10:00 |       |_     _|_     _|_     _|_     _|
    # 10:00 - 11:00 |_ABCDE_|_     _|_     _|_     _|_     _|

    # mon, tue, wed, thu, fri = make_full_sparse_schedule(schedule)
    mon, tue, wed, thu, fri = make_full_schedule(schedule)

    print("               |  MON  |  TUE  |  WED  |  THU  |  FRI  |")
    print("--------------------------------------------------------")
    for i in range(0, N_CHUNKS_PER_DAY):
        time = convert_chunk_to_time(i)
        # NOTE: prints only the first 5 characters of the activity name
        print(f" {time} | {mon[i][:5]:>5} | {tue[i][:5]:>5} | {wed[i][:5]:>5} | {thu[i][:5]:>5} | {fri[i][:5]:>5} |")