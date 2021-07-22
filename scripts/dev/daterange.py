from datetime import datetime, time, timedelta

now = datetime.now()

start = datetime.combine(now.date(), time(18, 0))
end1 = timedelta(hours=5)
end2 = timedelta(hours=12)

go1 = datetime.combine(now.date(), time(15, 0))
go2 = datetime.combine(now.date(), time(20, 0))
go3 = datetime.combine(now.date(), time(1, 0)) + timedelta(days=1)
go4 = datetime.combine(now.date(), time(8, 0)) + timedelta(days=1)


def time_in_range(go, end):
    global start
    now = go
    stop = start + end
    if now < start:
        print(f"{now} is before {start}, so I'm waiting")
    elif now >= start and now <= stop:
        print(f"{now} is after {start} and before {stop}, so I'm recording")
    else:
        start = start + timedelta(days=1)
        print(
            f"{now} is after {start} and {stop}, so I'm setting the next start to {start} and waiting"
        )


time_in_range(go1, end1)
time_in_range(go2, end1)
time_in_range(go3, end1)
time_in_range(go4, end1)

start = datetime.combine(now.date(), time(18, 0))

time_in_range(go1, end2)
time_in_range(go2, end2)
time_in_range(go3, end2)
time_in_range(go4, end2)
