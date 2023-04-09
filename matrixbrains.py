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
    
    # if sla goes into next day, add 1 day to the day counter
    # if remainder of SLA is negative and availability end time is more than 4 hours away, set new_sla as now + 4hours
    # This part of the script allows for 'NOW' dates and time for creation of new SLA... can be passed to rules.
    ## (this step may need revisiting to allow for after hours (or a flag created)) if remainder of SLA is negative and availability end is less than 4 hours away, add 1 day and make sla 4 hours from next days start date
    
    if sla_remainder > timedelta(hours=int(0)):
        day_counter += 1
    elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
        new_sla = now + timedelta(hours=4)
        return new_sla.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')
    elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
        new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1, hours=4)
        return new_sla.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')
        
    #loop to add days as per customer availbility and remainder of sla after adding days.
    
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
    new_sla = datetime.combine(create.date(), start_delta) + timedelta(days=day_counter) + slacount
    
    # if new sla ends up in the past make it 4 hours from now. Unless 4 hours from now is outside customer available times, then push it out to 4 hours from customer availability tomorrow.
    if new_sla < now and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
        new_sla = now + timedelta(hours=4)
        return new_sla.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')
    elif new_sla < now and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
        new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1, hours=4)
        return new_sla.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')
    
    return new_sla.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')
    
    
#Rules from old matrix
#if SLA falls = 7am-10am then make latest available the day before IF greater than 4 hours to cust COB 
#If > 4 hours to cust COB & SLA falls AH on that day, make SLA cust COB
#If SLA falls before 10am next day & < 4 hours to COB push to cust start next day (7am or greater) & display to user "advise cust of delayed SLA, negotiate AH Appointment if customer requires."
#If restoration before customer COB, leave restoration as is
#If afterhours required recommit to customers close of business.
#If 24*7 Add after hours tick box rules and public holidays/weekends... kill me
    
    
