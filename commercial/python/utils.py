
def calc_elapse_time(s_time, e_time):
    elapsed_time = e_time - s_time
    elapsed_hour = int(elapsed_time // 3600)
    elapsed_minute = int((elapsed_time % 3600) // 60)
    elapsed_second = int((elapsed_time % 3600 % 60))
    return f'{elapsed_hour}h {elapsed_minute}m {elapsed_second}s'

def elapse_time(elapsed_time):
    elapsed_hour = int(elapsed_time // 3600)
    elapsed_minute = int((elapsed_time % 3600) // 60)
    elapsed_second = int((elapsed_time % 3600 % 60))
    return f'{elapsed_hour}h {elapsed_minute}m {elapsed_second}s'
