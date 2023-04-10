import tkinter
import customtkinter
from tkinter import font
from tkinter import ttk
from datetime import datetime, timedelta, time

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"

### for testing purposes 25-03-2023 17:05:15 ####
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("SLA Matrix")
        self.minsize(300, 200)
           
        self.grid_rowconfigure(0,weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.mainframe = customtkinter.CTkFrame(self, width=300, height=500)
        self.mainframe.grid(row=0, column=0, columnspan=3, padx=20, pady=20)
        self.mainframe.grid_rowconfigure((0,1,2,3), weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.mainframe, text="SLA MATRIX", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 0))                                

        ### Field Validations ###
        ### Create date validation ###
        def show_message1(error='', color='transparent'):
            self.label_error1.configure(text = error, fg_color=color)

        def validate1(value):
           try:
                if value == '' or datetime.strptime(value, "%d-%m-%Y %H:%M:%S"):
                    show_message1()
                    return True
                else:
                    show_message1('INVALID format = dd-mm-yyyy HH:MM:SS', 'red')
                    return False
           except ValueError:
               show_message1('INVALID format = dd-mm-yyyy HH:MM:SS', 'red')
               return False

        self.vcmd1 = (self.register(validate1), '%P') 
        
        ###Start time validation
        def show_message2(error='', color='transparent'):
            self.label_error2.configure(text = error, fg_color=color)
        
        def validate2(value):
            try:
                if value == '' or len(value) == 4 and datetime.strptime(value, '%H%M'):
                    show_message2()
                    return True
                else:
                    show_message2('INVALID fmt=HHMM', 'red')
                    return False
            except ValueError:
                show_message2('INVALID fmt=HHMM', 'red')
                return False

        self.vcmd2 = (self.register(validate2), '%P')
        ###
        ### end Time validate ###
        def show_message3(error='', color='transparent'):
            self.label_error3.configure(text = error, fg_color=color)
    
        def validate3(value):
            try:
                if value == '' or len(value) == 4 and datetime.strptime(value, '%H%M'):
                    show_message3()
                    return True
                else:
                    show_message3('INVALID fmt=HHMM', 'red')
                    return False
            except ValueError:
                show_message3('INVALID fmt=HHMM', 'red')
                return False

        self.vcmd3 = (self.register(validate3), '%P')
        ######
        
        ### Submit button function###
        def button_callback():
            self.textbox.delete("0.0", "end")
            en1 = self.entry1.get()
            en2 = self.entry2.get()
            en3 = self.entry3.get()
            com = self.combobox.get()
            try:
                if datetime.strptime(en2, '%H%M') and datetime.strptime(en3, '%H%M') and datetime.strptime(en1, "%d-%m-%Y %H:%M:%S") and str(com).isnumeric():
                    self.textbox.insert("0.0", getsla(self.entry1.get(),self.combobox.get(),self.entry2.get(), self.entry3.get()))
                else:
                    self.textbox.insert("0.0", "AN INPUT IS MISSING OR INVALID, PLEASE CHECK")
            except ValueError:
                self.textbox.insert("0.0", "AN INPUT IS INVALID, PLEASE CHECK")
                           
        ### GUI Main ###   
        self.my_frame = customtkinter.CTkFrame(master=self.mainframe)
        self.my_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0))                                                             
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.label1 = customtkinter.CTkLabel(master=self.my_frame, text="Copy/Paste SC create date/time", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        self.entry1 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd1, placeholder_text="1-1-2023 00:00:00")
        self.entry1.grid(row=1, column=0, columnspan=2, padx=0, pady=(5,0))
        self.label_error1 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent', height=10)
        self.label_error1.grid(row=2, column=0, columnspan=2, padx=1)        
        self.label2 = customtkinter.CTkLabel(master=self.my_frame, text="Customer Availability", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label2.grid(row=3, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="n")
        self.label3 = customtkinter.CTkLabel(master=self.my_frame, text="Start", justify="center")
        self.label3.grid(row=4, column=0, padx=20, pady=0)
        self.label4 = customtkinter.CTkLabel(master=self.my_frame, text="End", justify="center")
        self.label4.grid(row=4, column=1, padx=20, pady=0)
        self.entry2 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd2, placeholder_text="HHMM")
        self.entry2.grid(row=5, column=0, padx=20)
        self.label_error2 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent', height=10)
        self.label_error2.grid(row=6, column=0, padx=1)
        self.entry3 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd3, placeholder_text="HHMM")
        self.entry3.grid(row=5, column=1, padx=20)
        self.label_error3 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent', height=10)
        self.label_error3.grid(row=6, column=1, padx=1)
        self.label5 = customtkinter.CTkLabel(master=self.my_frame, text="Select SLA in Hours", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label5.grid(row=7, column=0, columnspan=2, padx=20, pady=0)
        self.combobox = customtkinter.CTkComboBox(master=self.my_frame,
                                     values=["4", "8", "12", "24"]
                                     )
        self.combobox.grid(row=8, columnspan=2, padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self.my_frame, command=button_callback, text="Get Calculated SLA", fg_color=('#028900'),border_width=2, border_color=('#028900'), hover_color=('#057103'), width=200, height=60, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=9, column=0, columnspan=2, padx=20, pady=(0,10))
        self.textbox = customtkinter.CTkTextbox(master=self.mainframe, width=200, height=60)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.switch_var = customtkinter.StringVar(value="off")
        self.switch_1 = customtkinter.CTkSwitch(master=self.mainframe, text="dark/light", command=self.switch_event,
                                   variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch_1.grid(row=3, column=0, padx=20, pady=20)
        self.label6 = customtkinter.CTkLabel(master=self.mainframe, text="SLA Matrix v0.3, Built and maintained by Brad Hart - d403298", font=customtkinter.CTkFont(size=10))
        self.label6.grid(row=3, column=1, padx=5, pady=(20,20), sticky="e")
        ### GUI end ###
        
        ### SLA Calculation Start ####

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
            Delay=" - Advise customer of delayed SLA, negotiate AH Appointment if customer requires."
            output=""


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

            def in_between(now, start, end):
                if start <= end:
                    return start <= now < end
                else: # over midnight e.g., 23:30-04:15
                    return start <= now or now < end

            def afterhourscheck(new_sla, message=""):
                if in_between(new_sla.time(), time(17), time(23,59)):
                    alternate = datetime.strftime(datetime.combine(new_sla.date(), time(11)) + timedelta(days=1), '%d-%m-%Y %H:%M:%S')
                    message = f" - New SLA is Afterhours! - Use {alternate} unless AH is organised with customer"
                    return new_sla, message
                elif in_between(new_sla.time(), time(0), time(7)):
                    alternate = datetime.strftime(datetime.combine(new_sla.date(), time(11)), '%d-%m-%Y %H:%M:%S')
                    message = f" - New SLA is Afterhours! - Use {alternate} unless AH is organised with customer"
                    return new_sla, message
                elif in_between(new_sla.time(), time(7), time(10)):
                    if datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
                        alternate = datetime.strftime(datetime.combine(new_sla.date(), end_delta) - timedelta(days=1), '%d-%m-%Y %H:%M:%S')
                        message = f" - SLA Falls between 7am-10am, change to {alternate}. If afterhours, follow after hours process."
                        return new_sla, message
                    else:
                        return new_sla, message
                else:
                    return new_sla, message

            def returnsla(new_sla, message=""):
                weekend_date, wknd_day = weekendcheck(new_sla)
                new_sla, message = afterhourscheck(new_sla, message)
                new_sla = new_sla.strftime('%d-%m-%Y %H:%M:%S')

                if weekend_date != "nope":
                    new_weekend_date = weekend_date.strftime('%d-%m-%Y %H:%M:%S')
                    weekendout = f"Calculated SLA {new_sla} is a {wknd_day}. Follow afterhours process or use {new_weekend_date} {message}"
                    print("print of message in weekend if: ", message)
                    return weekendout
                else:
                    print("print of message in nonweekendif", message)
                    sendit = f"New SLA = {new_sla}{message}"
                    return sendit

            #Calculate SLA consumed on first day of ticket creation
            #If the create date and time is greater than the available time, subtract the create time from the daily available time to get how much SLA is used on the first day.

            if create > datetime.combine(create.date(), start_time.time()) and create < datetime.combine(create.date(), end_time.time()):
                day1_sla = datetime.combine(create.date(), end_time.time()) - create
            elif create > datetime.combine(create.date(), end_time.time()) and create < datetime.combine(create.date(), start_time.time()) + timedelta(1):
                day1_sla = create - create
            else:
                day1_sla = end_time - start_time
            print("day 1 sla: ", day1_sla)
            #The remaining SLA is calculated by subtracting the day1 SLA usage from the total SLA (this can result in a negative number with short SLAs)
            sla_remainder = timedelta(hours=int(SLA)) - day1_sla
            print("sla_remainder: ", sla_remainder)

            # if sla goes into next day, add 1 day to the day counter
            # if remainder of SLA is negative and availability end time is more than 4 hours away, set new_sla as now + 4hours
            # This part of the script allows for 'NOW' dates and time for creation of new SLA... can be passed to rules.
            # if remainder of SLA is negative and availability end is less than 4 hours away, add 1 day and make sla 4 hours from next days start date

            if sla_remainder > timedelta(hours=int(0)):
                day_counter += 1
                print("sla remainder greater than zero day counter: ", day_counter)
            elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
                new_sla = now + timedelta(hours=4)
                print("If sla reminder less than zero, and datetime nowdate and customer endtime - now is greater than 4 hours, new sla= ", new_sla)
                output = returnsla(new_sla)       
            elif sla_remainder <= timedelta(0) and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
                new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1)
                print("sla remainder <= 0 and customers end date today is less than 4 hours from now - should send delay message")
                output = returnsla(new_sla, Delay)

            # function call to loop to add days as per customer availbility and remainder of sla after adding days.
            slacount, day_counter = adddays(start_time, end_time, sla_remainder, day_counter, slacount)

            #the reason for setting this as 'create.date and start time' is because we want the slacount to start from the customers available time
            #after the number of days have been added. this only comes into effect if the sla gets days added.
            new_sla = datetime.combine(create.date(), start_delta) + timedelta(days=day_counter) + slacount

            # if new sla expiry in the past make new sla 4 hours from now. Unless 4 hours from now is outside customer available times,push to customer start tomorrow
            if new_sla < now and datetime.combine(now_date, end_delta) - now > timedelta(hours=4):
                new_sla = now + timedelta(hours=4)
                print("if new sla in the past if statement no delay")
                output = returnsla(new_sla, )
            elif new_sla < now and datetime.combine(now_date, end_delta) - now < timedelta(hours=4):
                new_sla = datetime.combine(now_date, start_delta) + timedelta(days=1)
                print("if sla in the past if statement plus delay")
                output = returnsla(new_sla, Delay)
            else:
                output = returnsla(new_sla)

            return output


    def switch_event(self):
        if self.switch_var == "on":
            customtkinter.set_appearance_mode("Dark")
            self.switch_var = "off"
        else:
            customtkinter.set_appearance_mode("Light")
            self.switch_var = "on"
                
if __name__ == "__main__":
    app = App()
    app.mainloop()
