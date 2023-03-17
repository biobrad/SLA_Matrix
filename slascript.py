import datetime
#import pytz

def getsla(CASECREATEDATETIME, SLA, CUSTSTART, CUSTEND):
    
    #timezone = input(str("Which part of Australia? (North/NSW/Queensland/South/West): "))
    print(CASECREATEDATETIME)
    create = datetime.datetime.strptime(CASECREATEDATETIME, "%d-%m-%Y %H:%M:%S")
    #create += datetime.datetime.create()
    # Define the start and end of the business day
    start_time = datetime.datetime.strptime(CUSTSTART, "%H%M")
    start_time = start_time.time()
    end_time = datetime.datetime.strptime(CUSTEND, "%H%M")
    end_time = end_time.time()
    
    # Get the case creation date and time
    #now = BEGIN #datetime.datetime.now(pytz.timezone('Australia/' + timezone))
    #print(f"Current time in {timezone} Australia is {now}")

    # If case create day is a weekend day (Saturday or Sunday), move to Monday
    if create.weekday() == 5:    # Saturday
        create += datetime.timedelta(days=2)
        create = datetime.datetime.combine(create.date(), start_time)
    elif create.weekday() == 6:  # Sunday
        create += datetime.timedelta(days=1)
        create = datetime.datetime.combine(create.date(), start_time)
    elif create.time() > end_time:
        create = datetime.datetime.combine(create.date() + datetime.timedelta(days=1), start_time)
    elif create.time() < start_time:
        create = datetime.datetime.combine(create.date(), start_time)

    #print("SLA Start Date and Time: " + str(create))

    # Set end of business hours for current day
    end_datetime = datetime.datetime.combine(create.date(), end_time)

    # Calculate remaining time in current business day
    time_remaining = datetime.timedelta(hours=int(SLA)) - (end_datetime - create)
    #print("time remaining: " + str(time_remaining))

    # If remaining time is less than 12 hours, add remaining time to start of next business day
    if time_remaining < datetime.timedelta(hours=int(SLA)):
        if create.weekday() == 4:
            end_datetime = datetime.datetime.combine(create.date() + datetime.timedelta(days=3), start_time) + time_remaining
        elif create.weekday() != 4:
            end_datetime = datetime.datetime.combine(create.date() + datetime.timedelta(days=1), start_time) + time_remaining

    # Print end date and time of SLA period
    return(str(end_datetime))