from constants import N_CHUNKS_PER_DAY, N_CHUNKS


def convert_solution_to_schedule(sol, activities):
    chunks = list(range(0, N_CHUNKS))
    schedule = []
    for c in chunks:
        for a in activities:
            if sol[c][a].value() == 1:
                schedule.append(a)
    return schedule


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


# Assumes that each chunk is 30 minutes
def convert_chunk_to_interval(chunk):
    # 0 -> 09:00 - 10:00
    # 8 -> 13:00 - 13:30
    day_chunk = chunk % N_CHUNKS_PER_DAY
    start_hour = 9 + int(day_chunk / 2)
    start_minute = "00" if day_chunk % 2 == 0 else "30"
    end_hour = start_hour if day_chunk % 2 == 0 else start_hour + 1
    end_minute = "00" if day_chunk % 2 == 1 else "30"
    return f"{start_hour:02d}:{start_minute} - {end_hour:02d}:{end_minute}"

def split_to_daily(schedule):
    n = N_CHUNKS_PER_DAY
    mon = schedule[:n]
    tue = schedule[n:n*2]
    wed = schedule[n*2:n*3]
    thu = schedule[n*3:n*4]
    fri = schedule[n*4:n*5]
    return mon, tue, wed, thu, fri


def show_schedule(schedule):
    print("               |  MON  |  TUE  |  WED  |  THU  |  FRI  |")
    print("--------------------------------------------------------")
    mon, tue, wed, thu, fri = split_to_daily(schedule)
    for c in range(0, N_CHUNKS_PER_DAY):
        interval = convert_chunk_to_interval(c)
        # NOTE: prints only the first 5 characters of the activity name
        mon_str = mon[c][:5]
        tue_str = tue[c][:5]
        wed_str = wed[c][:5]
        thu_str = thu[c][:5]
        fri_str = fri[c][:5]
        print(f" {interval} | {mon_str:>5} | {tue_str:>5} | {wed_str:>5} | {thu_str:>5} | {fri_str:>5} |")
