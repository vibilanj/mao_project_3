from constants import N_CHUNKS_PER_DAY, N_CHUNKS


# Converts the day and time to the index of the chunk where the activity starts.
def daytime_to_start_chunk(day, time):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    chunk_index = days.index(day) * N_CHUNKS_PER_DAY
    hour, minute = time.split(":")
    chunk_index += (int(hour) - 9) * 2
    chunk_index += 1 if int(minute) == 30 else 0
    return chunk_index


# Converts the index of the chunk to the time interval where the activity takes
#   place. Assumes that each chunk is 30 minutes starting from 09:00.
def convert_chunk_to_interval(chunk):
    day_chunk = chunk % N_CHUNKS_PER_DAY
    start_hour = 9 + int(day_chunk / 2)
    start_minute = "00" if day_chunk % 2 == 0 else "30"
    end_hour = start_hour if day_chunk % 2 == 0 else start_hour + 1
    end_minute = "00" if day_chunk % 2 == 1 else "30"
    return f"{start_hour:02d}:{start_minute} - {end_hour:02d}:{end_minute}"


# Splits the weekly schedule into daily schedules.
def split_to_daily(schedule):
    n = N_CHUNKS_PER_DAY
    mon = schedule[:n]
    tue = schedule[n:n*2]
    wed = schedule[n*2:n*3]
    thu = schedule[n*3:n*4]
    fri = schedule[n*4:n*5]
    return mon, tue, wed, thu, fri


# Prints the schedule in a human-readable format. Names are truncated to
#   five characters.
def show_schedule(schedule):
    print("               |  MON  |  TUE  |  WED  |  THU  |  FRI  |")
    print("--------------------------------------------------------")
    mon, tue, wed, thu, fri = split_to_daily(schedule)
    for c in range(0, N_CHUNKS_PER_DAY):
        interval = convert_chunk_to_interval(c)
        mon_str = mon[c][:5]
        tue_str = tue[c][:5]
        wed_str = wed[c][:5]
        thu_str = thu[c][:5]
        fri_str = fri[c][:5]
        print(f" {interval} | {mon_str:>5} | {tue_str:>5} | {wed_str:>5} | {thu_str:>5} | {fri_str:>5} |")
