import os
import random
import requests
import tkinter
import customtkinter
from tkinter import font
from tkinter import ttk
from datetime import datetime, timedelta, time
import holidays
import webbrowser
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("700x500")
        self.title("SLA Matrix")
        self.minsize(300, 200)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        
        self.sidebar_button_event = ""
        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="ENM Tools", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text = "SLA Matrix", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text = "Cooble Groodle", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        #self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        #self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        #self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        #self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        #self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        #self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        #self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        #self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.switch_var = customtkinter.StringVar(value="off")
        self.switch_1 = customtkinter.CTkSwitch(
            master=self.sidebar_frame,
            text="dark/light",
            command=self.switch_event,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
        )
        self.switch_1.grid(row=4, column=0, padx=20, pady=5)
        
        
        self.mainframe = customtkinter.CTkFrame(self, width=300, height=500)
        self.mainframe.grid(row=0, column=1, columnspan=3, padx=20, pady=10)
        self.mainframe.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.mainframe,
            text="SLA MATRIX",
            font=customtkinter.CTkFont(size=30, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, columnspan=2)
        
        
        #Version Check Variables
        self.current_version = '0.7.0'
        self.api_url = 'http://10.194.193.96:8000'
        self.download_url = 'https://confluence.tools.telstra.com/display/IPDA/SYSTEMS+-+SLA+MATRIX+-+v0.6+Guide'
        
        ### Send usage data ###
              
        def send_usage_data(self):
            n = random.random()
            rand = str(n)
            rannum = rand[3:10]

            url = "https://vogeneric-ops-vo-ip-trig-01.splunk-ngworkflow.puma.corp.telstra.com/vogeneric"

            username = os.getlogin()
            payload = {"search_name": "SLA_BOT", "result": {"SNI": "SNI"+rannum, "username": username, "version": self.current_version}}
            
            try:
                response = requests.post(url, json=payload, verify=False, timeout=0.1)
            except requests.exceptions.RequestException as e:
                pass

        ### Field Validations ###
        ### Create date validation ###
        def show_message1(error="", color="transparent"):
            self.label_error1.configure(text=error, fg_color=color)

        def validate1(value):
            try:
                if value == "" or datetime.strptime(value, "%d-%m-%Y %H:%M:%S"):
                    show_message1()
                    return True
                else:
                    show_message1("INVALID format = dd-mm-yyyy HH:MM:SS", "red")
                    return False
            except ValueError:
                show_message1("INVALID format = dd-mm-yyyy HH:MM:SS", "red")
                return False

        self.vcmd1 = (self.register(validate1), "%P")

        ###Start time validation
        def show_message2(error="", color="transparent"):
            self.label_error2.configure(text=error, fg_color=color)

        def validate2(value):
            try:
                if value == "" or len(value) == 4 and datetime.strptime(value, "%H%M"):
                    show_message2()
                    return True
                else:
                    show_message2("INVALID fmt=HHMM", "red")
                    return False
            except ValueError:
                show_message2("INVALID fmt=HHMM", "red")
                return False

        self.vcmd2 = (self.register(validate2), "%P")

        ###
        ### end Time validate ###
        def show_message3(error="", color="transparent"):
            self.label_error3.configure(text=error, fg_color=color)

        def validate3(value):
            try:
                if value == "" or len(value) == 4 and datetime.strptime(value, "%H%M"):
                    show_message3()
                    return True
                else:
                    show_message3("INVALID fmt=HHMM", "red")
                    return False
            except ValueError:
                show_message3("INVALID fmt=HHMM", "red")
                return False

        self.vcmd3 = (self.register(validate3), "%P")
        ######

        ### Submit button function###
        def button_callback(*args):
            self.textbox.delete("0.0", "end")
            en1 = self.entry1.get()
            en2 = self.entry2.get()
            en3 = self.entry3.get()
            com = self.combobox.get()
            
            send_usage_data(self)
            
            try:
                if (
                    datetime.strptime(en2, "%H%M")
                    and datetime.strptime(en3, "%H%M")
                    and datetime.strptime(en1, "%d-%m-%Y %H:%M:%S")
                    and str(com).isnumeric()
                ):
                    self.textbox.insert(
                        "0.0",
                        get_sla(
                            self.entry1.get(),
                            self.combobox.get(),
                            self.entry2.get(),
                            self.entry3.get(),
                        ),
                    )
                else:
                    self.textbox.insert(
                        "0.0", "AN INPUT IS MISSING OR INVALID, PLEASE CHECK"
                    )
            except ValueError:
                self.textbox.insert("0.0", "AN INPUT IS INVALID, PLEASE CHECK")

        def copy():
            # copy selected text to clipboard
            self.clipboard_clear()
            self.clipboard_append(self.selection_get())
        
        ### GUI Main ###
        self.my_frame = customtkinter.CTkFrame(master=self.mainframe)
        self.my_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=5)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.label1 = customtkinter.CTkLabel(
            master=self.my_frame,
            text="Copy/Paste SC create date/time",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.label1.grid(row=0, column=0, columnspan=2, padx=20, pady=5)
        self.entry1 = customtkinter.CTkEntry(
            master=self.my_frame,
            validate="focusout",
            validatecommand=self.vcmd1,
            placeholder_text="1-1-2023 00:00:00",
        )
        self.entry1.grid(row=1, column=0, columnspan=2, padx=0)

        self.RightClickMenu1 = tkinter.Menu(
            self.entry1,
            tearoff=False,
            background="#565b5e",
            fg="white",
            font=("", 11),
            borderwidth=0,
            bd=0,
        )
        self.RightClickMenu1.add_command(
            label="Paste",
            command=lambda: self.entry1.insert(tkinter.END, self.clipboard_get()),
        )
        self.RightClickMenu1.add_command(label="Copy", command=copy)
        self.entry1.bind(
            "<Button-3>", lambda event: do_popup(event, frame=self.RightClickMenu1)
        )
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.label_error1 = customtkinter.CTkLabel(
            self.my_frame, text="", fg_color="transparent", height=10
        )
        self.label_error1.grid(row=2, column=0, columnspan=2, padx=1)
        self.label2 = customtkinter.CTkLabel(
            master=self.my_frame,
            text="Customer Availability",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.label2.grid(
            row=3, column=0, columnspan=2, padx=20, sticky="n"
        )
        self.label3 = customtkinter.CTkLabel(
            master=self.my_frame, text="Start", justify="center"
        )
        self.label3.grid(row=4, column=0, padx=20, pady=0)
        self.label4 = customtkinter.CTkLabel(
            master=self.my_frame, text="End", justify="center"
        )
        self.label4.grid(row=4, column=1, padx=20, pady=0)
        self.entry2 = customtkinter.CTkEntry(
            master=self.my_frame,
            validate="focusout",
            validatecommand=self.vcmd2,
            placeholder_text="HHMM",
        )
        self.entry2.grid(row=5, column=0, padx=20)

        self.RightClickMenu2 = tkinter.Menu(
            self.entry2,
            tearoff=False,
            background="#565b5e",
            fg="white",
            font=("", 11),
            borderwidth=0,
            bd=0,
        )
        self.RightClickMenu2.add_command(
            label="Paste",
            command=lambda: self.entry2.insert(tkinter.END, self.clipboard_get()),
        )
        self.RightClickMenu2.add_command(label="Copy", command=copy)
        self.entry2.bind(
            "<Button-3>", lambda event: do_popup(event, frame=self.RightClickMenu2)
        )
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.label_error2 = customtkinter.CTkLabel(
            self.my_frame, text="", fg_color="transparent", height=10
        )
        self.label_error2.grid(row=6, column=0, padx=1)
        self.entry3 = customtkinter.CTkEntry(
            master=self.my_frame,
            validate="focusout",
            validatecommand=self.vcmd3,
            placeholder_text="HHMM",
        )
        self.entry3.grid(row=5, column=1, padx=20)

        self.RightClickMenu3 = tkinter.Menu(
            self.entry3,
            tearoff=False,
            background="#565b5e",
            fg="white",
            font=("", 11),
            borderwidth=0,
            bd=0,
        )
        self.RightClickMenu3.add_command(
            label="Paste",
            command=lambda: self.entry3.insert(tkinter.END, self.clipboard_get()),
        )
        self.RightClickMenu3.add_command(label="Copy", command=copy)
        self.entry3.bind(
            "<Button-3>", lambda event: do_popup(event, frame=self.RightClickMenu3)
        )
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.label_error3 = customtkinter.CTkLabel(
            self.my_frame, text="", fg_color="transparent", height=10
        )
        self.label_error3.grid(row=6, column=1, padx=1)
        self.label5 = customtkinter.CTkLabel(
            master=self.my_frame,
            text="Select SLA in Hours",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )
        self.label5.grid(row=7, column=0, columnspan=2, padx=20, pady=0)
        self.combobox = customtkinter.CTkComboBox(
            master=self.my_frame, values=["12", "24", "4", "8"]
        )
        self.combobox.grid(row=8, columnspan=2, padx=20, pady=(0,5))
        self.button = customtkinter.CTkButton(
            master=self.my_frame,
            command=button_callback,
            text="Get Calculated SLA",
            fg_color=("#028900"),
            border_width=2,
            border_color=("#028900"),
            hover_color=("#057103"),
            width=200,
            height=60,
            font=customtkinter.CTkFont(size=15, weight="bold")
            )
        self.button.bind('<Return>', command=button_callback)
        self.button.grid(row=9, column=0, columnspan=2, padx=20, pady=(0, 10))
        self.textbox = customtkinter.CTkTextbox(
            master=self.mainframe, width=240, height=60
        )
        self.textbox.grid(
            row=2, column=0, columnspan=2, padx=20, sticky="ew"
        )

        self.RightClickMenu4 = tkinter.Menu(
            self.textbox,
            tearoff=False,
            font=("", 11),
            background="#565b5e",
            fg="white",
            borderwidth=0,
            bd=0,
        )
        self.RightClickMenu4.add_command(label="Copy", command=copy)
        self.textbox.bind(
            "<Button-3>", lambda event: do_popup(event, frame=self.RightClickMenu4)
        )
        self.bind("<1>", lambda event: event.widget.focus_set())

        self.update_button = customtkinter.CTkButton(
            master=self.mainframe, 
            text="Matrix Update Available! Click to Download", 
            command=self.open_download_url,
            fg_color=("#FF0000"),
            border_width=2,
            border_color=("#df0000"),
            hover_color=("#c20000"),
            font=customtkinter.CTkFont(size=15, weight="bold")
            )
        self.update_button.grid(row=3, column=0)
        self.update_button.grid_forget()

        self.label6 = customtkinter.CTkLabel(
            master=self.mainframe,
            text=f"SLA Matrix v{self.current_version}, Built and maintained by Brad Hart - d403298",
            font=customtkinter.CTkFont(size=10),
        )
        self.label6.grid(row=4, column=1, padx=5, pady=5, sticky="e")
        ### GUI end ###

        ### SLA Calculation Start ####

        def get_sla(case_created_at, sla, cust_start, cust_end):
            # Addition of days based on remaining SLA function
            def add_days(hours_avail, remainder, day_counter, sla_count):
                sla_count = remainder
                while sla_count > timedelta(0):
                    if sla_count - hours_avail <= timedelta(0):
                        break
                    else:
                        sla_count -= hours_avail
                        day_counter = day_counter + 1
                return sla_count, day_counter

            def weekend_check(weekend_date):
                if weekend_date.weekday() == 5:  # Saturday
                    day = "Saturday"
                    weekend_date = weekend_date + timedelta(days=2)
                elif weekend_date.weekday() == 6:  # Sunday
                    day = "Sunday"
                    weekend_date = weekend_date + timedelta(days=1)
                return weekend_date, day

            def is_time_between(now, start, end):
                if start <= end:
                    return start <= now < end
                else:  # over midnight e.g., 23:30-04:15
                    return start <= now or now < end

            #checking for new SLA time between 7pm and 11am
            def check_seven_to_seven(new_sla):
                message = ""
                print("new_sla = ", new_sla)
                if new_sla.time() >= time(19) or new_sla.time() < time(11):
                    if new_sla.time() < time(11):
                        alternate = datetime.strftime(datetime.combine(new_sla.date(), time(11)), "%d-%m-%Y %H:%M:%S")
                    else:
                        alternate = datetime.strftime(datetime.combine(new_sla.date(), time(11)), "%d-%m-%Y %H:%M:%S") + timedelta(days=1)
                    string_newsla = datetime.strftime(new_sla, "%d-%m-%Y %H:%M:%S")
                    message = f"\nThe original New SLA {string_newsla} is between 7pm and\n11am. Use {alternate} or follow afterhours process"

                alternate = datetime.strptime(alternate, "%d-%m-%Y %H:%M:%S")

                return alternate, message

            def next_business_day(date):
                while True:
                    if date.weekday() >= 5 or date in au_holidays:
                        date += timedelta(days=1)
                    else:
                        return date

            #Management of SLA if afterhours or weekends or public holidays. Also changes SLA time to customer start time if necessary
            def return_sla(new_sla, message=""):
                original_sla = new_sla
                wknd_day=''
                pub_hol=''

                if is_time_between(new_sla.time(), time(19), time(11)):
                    new_sla, message = check_seven_to_seven(new_sla)

                if new_sla.weekday() >= 5:
                    new_sla, wknd_day = weekend_check(new_sla)

                if new_sla in au_holidays:
                    new_sla = next_business_day(new_sla)
                    sla_string = datetime.strftime(new_sla, "%d-%m-%Y %H:%M:%S")
                    pub_hol = f"impacted by Public Holiday.\nFollow afterhours process or use {sla_string}"

                print("New SLA: ", new_sla)

                if new_sla.time() < start_time:
                    new_sla = datetime.combine(new_sla.date(), start_time)

                new_sla = new_sla.strftime("%d-%m-%Y %H:%M:%S")
                original_sla = original_sla.strftime("%d-%m-%Y %H:%M:%S")

                if wknd_day != '' and pub_hol == '':
                    message = f" is a {wknd_day} Follow afterhours process or use {new_sla}"
                    send_it = f"New SLA = {original_sla} {message}"
                elif wknd_day == '' and pub_hol != '':
                    message = pub_hol
                    send_it = f"New SLA = {original_sla} {message}"
                elif wknd_day != '' and pub_hol != '':
                    message = f"Impacted by Weekend \"{wknd_day}\" and Public Holiday \nUse {new_sla} or follow afterhours process"
                    send_it = f"New SLA = {original_sla} {message}"
                elif wknd_day == '' and pub_hol == '':
                    send_it = f"New SLA = {new_sla} {message}"

                return send_it

            # Main function starts here
            # Variables
            case_created = datetime.strptime(case_created_at, "%d-%m-%Y %H:%M:%S")
            start_time = datetime.strptime(cust_start, "%H%M").time()
            end_time = datetime.strptime(cust_end, "%H%M").time()
            now = datetime.now()

            #Validity check
            if start_time > end_time:
                return "Cust availability start time cannot be greater than end time.\nIf after hours is required, follow after hours process"

            #more variables
            hours_avail = datetime.combine(now.date(), end_time) - datetime.combine(now.date(), start_time)
            day_counter = 0
            sla_count = 0
            au_holidays = holidays.AU()

            #Calculation of first days SLA usage
            if case_created > datetime.combine(case_created.date(), start_time) and case_created < datetime.combine(case_created.date(), end_time):
                day1_sla = datetime.combine(case_created.date(), end_time) - case_created
            else:
                day1_sla = datetime.combine(case_created.date(), end_time) - datetime.combine(case_created.date(), start_time) 

            sla_remainder = timedelta(hours=int(sla)) - day1_sla

            print("sla remainder: ", sla_remainder)

            #management of remaining SLA time
            if sla_remainder > timedelta(hours=int(0)):
                day_counter += 1
            elif sla_remainder <= timedelta(0) and datetime.combine(now.date(), end_time) - now > timedelta(hours=4):
                new_sla = now + timedelta(hours=4)
                output = return_sla(new_sla)
            else:
                new_sla = datetime.combine(now.date(), start_time) + timedelta(days=1)
                output = return_sla(new_sla, "Advise customer of delayed SLA, negotiate AH Appointment if customer requires.")

            #sending remaining SLA hours to add days function
            sla_count, day_counter = add_days(hours_avail, sla_remainder, day_counter, sla_count)
            new_sla = datetime.combine(case_created.date(), start_time) + timedelta(days=day_counter) + sla_count

            #Management of SLA if SLA falls today
            if new_sla < now and datetime.combine(now.date(), end_time) - now > timedelta(hours=4):
                new_sla = now + timedelta(hours=4)
                output = return_sla(new_sla)
            elif new_sla < now and datetime.combine(now.date(), end_time) - now < timedelta(hours=4):
                new_sla = datetime.combine(now.date(), start_time) + timedelta(days=1)
                output = return_sla(new_sla, "Advise customer of delayed SLA, negotiate AH Appointment if customer requires.")
            else:
                output = return_sla(new_sla)

            return output

        #Version check command (checks on launch)
        self.check_for_updates()
        
        def do_popup(event, frame):
            try:
                frame.tk_popup(event.x_root, event.y_root)
            finally:
                frame.grab_release()

    def check_for_updates(self):
        try:
            response = requests.get(self.api_url, timeout=0.1)
            latest_version = response.json()['version']
            self.download_url = response.json()['url']
        except requests.exceptions.RequestException as e:
            latest_version = self.current_version
            print(e)
        if self.compare_versions(self.current_version, latest_version):
            self.update_button.grid(row = 3, column=0, columnspan=2, padx=0, pady=(5,0))  # Show the update button if an update is available

    def open_download_url(self):
        webbrowser.open(self.download_url)

    @staticmethod
    def compare_versions(current_version, latest_version):
        current_version_parts = [int(part) for part in current_version.split('.')]
        latest_version_parts = [int(part) for part in latest_version.split('.')]
        for current, latest in zip(current_version_parts, latest_version_parts):
            if current < latest:
                return True
            elif current > latest:
                return False
        return len(current_version_parts) < len(latest_version_parts)

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


#to build - auto-py-to-exe
#pyinstaller --noconfirm --onedir --windowed --icon "C:/Users/bradh/OneDrive/Desktop/matrixicons/bx-calendar-star-blue-blue (1).ico" --add-data "C:/Users/bradh/miniconda3/envs/tkinter/Lib/site-packages/customtkinter;customtkinter/"  "C:/Users/bradh/OneDrive/Documents/D_Drive/programming files/tkinter/newmatrix.py"
