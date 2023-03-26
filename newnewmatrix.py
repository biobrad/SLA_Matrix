import tkinter
import customtkinter
from tkinter import font
from tkinter import ttk
from datetime import datetime, timedelta

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
        self.mainframe.grid(row=0, column=0,columnspan=2, padx=20, pady=20)
        self.mainframe.grid_rowconfigure((0,1,2,3), weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.mainframe, text="SLA MATRIX", font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 0))                                

        ### Field Validations ###
        ### Start Time validate ###
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
        self.grid_columnconfigure((0,1), weight=1)
        self.label1 = customtkinter.CTkLabel(master=self.my_frame, text="Copy/Paste SC create date/time", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        self.entry1 = customtkinter.CTkEntry(master=self.my_frame, placeholder_text="1-1-2023 00:00:00", text_color="white")
        self.entry1.grid(row=1, column=0, columnspan=2, padx=0, pady=(5,0))
        self.label2 = customtkinter.CTkLabel(master=self.my_frame, text="Customer Availability", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label2.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="n")
        self.label3 = customtkinter.CTkLabel(master=self.my_frame, text="Start", justify="center")
        self.label3.grid(row=3, column=0, padx=20, pady=0)
        self.label4 = customtkinter.CTkLabel(master=self.my_frame, text="End", justify="center")
        self.label4.grid(row=3, column=1, padx=20, pady=0)
        self.entry2 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd2, placeholder_text="HHMM")
        self.entry2.grid(row=4, column=0, padx=20)
        self.label_error2 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent', height=10)
        self.label_error2.grid(row=5, column=0, padx=1)
        self.entry3 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd3, placeholder_text="HHMM")
        self.entry3.grid(row=4, column=1, padx=20)
        self.label_error3 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent', height=10)
        self.label_error3.grid(row=5, column=1, padx=1)
        self.label5 = customtkinter.CTkLabel(master=self.my_frame, text="Select SLA in Hours", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label5.grid(row=6, column=0, columnspan=2, padx=20, pady=0)
        self.combobox = customtkinter.CTkComboBox(master=self.my_frame,
                                     values=["4", "8", "12", "24"]
                                     )
        self.combobox.grid(row=7, columnspan=2, padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self.my_frame, command=button_callback, text="Get Calculated SLA", fg_color=('#028900'),border_width=2, border_color=('#028900'), hover_color=('#057103'), width=200, height=60, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=8, column=0, columnspan=2, padx=20, pady=(0,10))
        self.textbox = customtkinter.CTkTextbox(master=self.mainframe, width=200, height=60)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.label6 = customtkinter.CTkLabel(master=self, text="SLA Matrix v0.1, Built and mainted by Brad Hart - d403298", font=customtkinter.CTkFont(size=10))
        self.label6.grid(row=3, column=0, columnspan=2, padx=5, pady=(20,20), sticky="n")
        ### GUI end ###
        
        ### SLA Calculation Start ####
        
        def getsla(CASECREATEDATETIME, SLA, CUSTSTART, CUSTEND):
            #timezone = input(str("Which part of Australia? (North/NSW/Queensland/South/West): "))
            #print(CASECREATEDATETIME)
            create = datetime.strptime(CASECREATEDATETIME, "%d-%m-%Y %H:%M:%S")
            #create += datetime.datetime.create()
            # Define the start and end of the business day
            start_time = datetime.strptime(CUSTSTART, "%H%M")
            start_time = start_time.time()
            end_time = datetime.strptime(CUSTEND, "%H%M")
            end_time = end_time.time()

            # Get the case creation date and time
            #now = BEGIN #datetime.datetime.now(pytz.timezone('Australia/' + timezone))
            #print(f"Current time in {timezone} Australia is {now}")

            # If case create day is a weekend day (Saturday or Sunday), move to Monday
            if create.weekday() == 5:    # Saturday
                create += timedelta(days=2)
                create = datetime.combine(create.date(), start_time)
            elif create.weekday() == 6:  # Sunday
                create += timedelta(days=1)
                create = datetime.combine(create.date(), start_time)
            elif create.time() > end_time:
                create = datetime.combine(create.date() + timedelta(days=1), start_time)
            elif create.time() < start_time:
                create = datetime.combine(create.date(), start_time)

            #print("SLA Start Date and Time: " + str(create))

            # Set end of business hours for current day
            end_datetime = datetime.combine(create.date(), end_time)

            # Calculate remaining time in current business day
            time_remaining = timedelta(hours=int(SLA)) - (end_datetime - create)
            #print("time remaining: " + str(time_remaining))

            # If remaining time is less than 12 hours, add remaining time to start of next business day
            if time_remaining < timedelta(hours=int(SLA)):
                if create.weekday() == 4:
                    end_datetime = datetime.combine(create.date() + timedelta(days=3), start_time) + time_remaining
                elif create.weekday() != 4:
                    end_datetime = datetime.combine(create.date() + timedelta(days=1), start_time) + time_remaining

            # Print end date and time of SLA period
            return end_datetime.strftime('New SLA Date/time: %d-%m-%Y %H:%M:%S')

if __name__ == "__main__":
    app = App()
    app.mainloop()
