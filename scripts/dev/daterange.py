from datetime import datetime, time, timedelta

now = datetime.combine(datetime.now().date()+timedelta(days=0),time(8,0))

params = {"-START-": time(5,0), "-END-": time(12,0)}

def time_in_range(start, end, x):
    today = datetime.now().date()
    if start < end:
        strt = datetime.combine(today,start)
        endt = datetime.combine(today,end)
    elif end < start:
        strt = datetime.combine(today,start)
        endt = datetime.combine(today+timedelta(days=1),end)
    result = x >= strt and x <= endt
    return result

print(time_in_range(params["-START-"],params["-END-"], now))