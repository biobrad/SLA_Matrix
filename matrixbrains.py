from datetime import datetime, time
from datetime import timedelta

##TODO - flag in tkinter if hours outside of 7am-7pm for customer availablity that afterhours should be negotiated with customer and 
#not to use matrix (grey out submit)

def getsla(CASECREATEDATETIME, SLA, CUSTSTART, CUSTEND):
    create = datetime.strptime(CASECREATEDATETIME, "%d-%m-%Y %H:%M:%S")
    start_time = datetime.strptime(CUSTSTART, "%H%M")
    end_time = datetime.strptime(CUSTEND, "%H%M")
    start_delta = datetime.time(start_time)
    end_delta = datetime.time(end_time)
    now = datetime.now()   
    now_date = now.date() 
    day_counter = 0
    slacount = 0
    new_sla=""
    weekend_date=""
    wknd_day=""
    Delay="\nAdvise cust of delayed SLA, negotiate AH Appointment if customer requires."
    
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
    
    def weekendcheck(weekend_date):
        if weekend_date.weekday() == 5:    # Saturday
            day = "Saturday"
            weekend_date = datetime.combine(weekend_date.date(), start_delta) + timedelta(days=2)
            return weekend_date, day 
        elif weekend_date.weekday() == 6:  # Sunday
            day = "Sunday"
            weekend_date = datetime.combine(weekend_date.date(), start_delta) + timedelta(days=1)
            return weekend_date, day
        else:
            return "nope", "nope"
    
    def returnsla(weekend_date, wknd_day, new_sla, message=""):
        new_sla = new_sla.strftime('%d-%m-%Y %H:%M:%S')
        if weekend_date != "nope":
            new_weekend_date = weekend_date.strftime('%d-%m-%Y %H:%M:%S')
            weekendout = f"Calculated SLA {new_sla} is a {wknd_day}. Follow afterhours process or use {new_weekend_date} {message}"
            return weekendout
        else:
            sendit = f"New SLA = {new_sla} {message}"
            return sendit
    
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
        weekend_date, wknd_day = weekendcheck(new_sla)
        returnsla(weekend_date, wknd_day, new_sla)       
    elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
        new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1)
        weekend_date, wknd_day = weekendcheck(new_sla)
        returnsla(weekend_date, wknd_day, new_sla, Delay)
        
    # function call to loop to add days as per customer availbility and remainder of sla after adding days.
    slacount, day_counter = adddays(start_time, end_time, sla_remainder, day_counter, slacount)
    #the reason for setting this as 'create.date and start time' is because we want the slacount to start from the customers available time
    #after the number of days have been added. this only comes into effect if the sla gets days added.
    new_sla = datetime.combine(create.date(), start_delta) + timedelta(days=day_counter) + slacount
    
    # if new sla expiry in the past make new sla 4 hours from now. Unless 4 hours from now is outside customer available times,push to customer start tomorrow
    if new_sla < now and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
        new_sla = now + timedelta(hours=4)
        weekend_date, wknd_day = weekendcheck(new_sla)
        returnsla(weekend_date, wknd_day, new_sla)
    elif new_sla < now and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
        new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1)
        weekend_date, wknd_day = weekendcheck(new_sla)
        returnsla(weekend_date, wknd_day, new_sla, Delay)
    
    def afterhourscheck(startTime, endTime, checkTime):
        if startTime < endTime: 
            return nowTime >= startTime and nowTime <= endTime 
        else: 
            #Over midnight: 
            return nowTime >= startTime or nowTime <= endTime 
    
    weekend_date, wknd_day = weekendcheck(new_sla)
    return returnsla(weekend_date, wknd_day, new_sla)
    
    
    
#Rules from old matrix
#if SLA falls = 7am-10am then make latest available the day before IF greater than 4 hours to cust COB 
#If > 4 hours to cust COB & SLA falls AH on that day, make SLA cust COB
#If SLA falls before 10am next day & < 4 hours to COB push to cust start next day (7am or greater) & display to user 
# "advise cust of delayed SLA, negotiate AH Appointment if customer requires."
#If restoration before customer COB, leave restoration as is
#If afterhours required recommit to customers close of business.
#If 24*7 Add after hours tick box rules and public holidays/weekends..
