from datetime import datetime, time
from datetime import timedelta

def getsla(CASECREATEDATETIME, SLA, CUSTSTART, CUSTEND):
    #timezone = input(str("Which part of Australia? (North/NSW/Queensland/South/West): "))
    #print(CASECREATEDATETIME)
    create = datetime.strptime(CASECREATEDATETIME, "%d-%m-%Y %H:%M:%S")
    #create += datetime.datetime.create()
    # Define the start and end of the business day
    start_time = datetime.strptime(CUSTSTART, "%H%M")
    start_time_today = datetime.combine(datetime.now(), start_time.time())
    end_time = datetime.strptime(CUSTEND, "%H%M")
    end_time_today = datetime.combine(datetime.now(), end_time.time())
    start_delta = datetime.time(start_time)
    end_delta = datetime.time(end_time)
    now = datetime.now()   
    now_date = now.date() 
    now_delta = datetime.time(now)
    day_counter = 0
    slacount = 0
    new_sla=""
    
    #Calculate SLA consumed on first day of ticket creation
    #If the create date and time is greater than the available time, subtract the create time from the daily available time to get how much SLA is used on the first day.
    
    if create > datetime.combine(create.date(), start_time.time()):
        day1_sla = datetime.combine(create.date(), end_time.time()) - create
    else:
        day1_sla = end_time - start_time
    
    #The remaining SLA is calculated by subtracting the day1 SLA usage from the total SLA (this can result in a negative number with short SLAs)
    sla_remainder = timedelta(hours=int(SLA)) - day1_sla
    print(sla_remainder)
    
    # if sla goes into next day, add 1 day to the day counter
    # if remainder of SLA is negative and availability end time is more than 4 hours away, set new_sla as now + 4hours
    ## (this step may need revisiting to allow for after hours (or a flag created)) if remainder of SLA is negative and availability end is less than 4 hours away, add 1 day and make sla 4 hours from next days start date
    
    if sla_remainder > timedelta(hours=int(0)):
        day_counter += 1
    elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
        new_sla = now + timedelta(hours=4)
        return new_sla
    elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
        new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1, hours=4)
        return new_sla
        
    #loop to add days as per customer availbility and remainder of slacount
    def adddays(start, end, remainder, day_counter, slacount):
        hoursavail = end - start
        slacount = remainder
        
        while slacount > timedelta(0):
            if slacount - hoursavail <= timedelta(0):
                break
            else:
                slacount -= hoursavail
                day_counter = day_counter + 1
        return slacount, day_counter
    
    slacount, day_counter = adddays(start_time, end_time, sla_remainder, day_counter, slacount)
        
    #the reason for setting this as 'create.date and start time' is because we want the slacount to start from the customers available time
    #after the number of days have been added. this only comes into effect if the sla gets days added.
    new_sla = datetime.combine(create.date, start_delta) + timedelta(days=day_counter) + slacount
    if new_sla > now:
        kill myself.
    
    print(type(slacount))
    print(str(new_sla))
    
    # rules and public holidays/weekends... kill me
