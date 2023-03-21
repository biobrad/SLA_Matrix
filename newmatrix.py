import pynecone as pc
from datetime import datetime

SLA = ["24", "12", "8", "4"]

class State(pc.State):
    """"Base State"""
    datentime: str = ""
    custSLA: int = ""
    custstart: str = ""
    custend: int = ""
    slareturn: str = ""
    button: bool = False
    input1: bool = False
    input2: bool = False
    input3: bool = False
    
    def senditbish(self):
        self.slareturn
        self.slareturn=getsla(self.datentime, self.custSLA, self.custstart, self.custend)

    def set_datentime(self, datentime):
        self.button
        self.input3
        try:
            datetime.strptime(datentime, "%d-%m-%Y %H:%M:%S")
            self.button = False
            self.datentime = datentime
            self.input3 = False
        except ValueError:
            self.button = True
            self.datentime = "INVALID ENTRY"
            self.input3 = True
    
    def set_custstart(self, custstart):
        self.button
        self.input1
        try:
            if len(custstart) == 4: 
                datetime.strptime(custstart, '%H%M')
                self.button = False
                self.custstart = custstart
                self.input1 = False
            else:
                self.button = True
                self.custstart = "INVALID"
                self.input1 = True
        except ValueError:
            self.button = True
            self.custstart = "INVALID"
            self.input1 = True

    def set_custend(self, custend):
        self.button
        self.input2
        try:
            if len(custend) == 4: 
                datetime.strptime(custend, '%H%M')
                self.button = False
                self.custend = custend
                self.input2 = False
            else:
                self.button = True
                self.custend = "INVALID"
                self.input2 = True
        except ValueError:
            self.button = True
            self.custend = "INVALID"
            self.input2 = True

def start_input(custstart):
    return pc.input(
        on_change=State.set_custstart,
        is_required=True,
        is_invalid=State.input1,
        error_border_color="red",
        variant = "outline",
        color="black",
        bg="white",
        size="sm"
        )

def end_input(custend):
    return pc.input(
        on_change=State.set_custend,
        is_required=True,
        is_invalid=State.input2,
        error_border_color="red",
        variant = "outline",
        color="black",
        bg="white",
        size="sm"
        )

def getsla(CASECREATEDATETIME, SLA, CUSTSTART, CUSTEND):
    #timezone = input(str("Which part of Australia? (North/NSW/Queensland/South/West): "))
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

def index():
    login_container = pc.container(
        pc.vstack(
            pc.container(height="20px"),
            pc.container(
                pc.text(
                    "Field SLA Matrix",
                    fontSize="28px",
                    color="white",
                    fontweight="bold",
                    letterSpacing="0px",
                    ),
                #text settings
                width="250px",
                center_content=True,
                ),
            pc.container(
                pc.text(
                    "Copy/Paste SC case create date and time"
                    ),
                pc.input(
                    placeholder="1-1-1111 00:00:00",
                    on_change=State.set_datentime,
                    is_required=True,
                    color="black",
                    bg="white",
                    is_invalid=State.input3,
                    error_border_color="red",
                    variant = "outline",
                    size="sm"
                    ),
                pc.text("Create date/time: ", State.datentime, color="white"),
                pc.text(
                    "Select Customer SLA (in hours)",
                    margin_top="1rem"
                    ),
                pc.select(
                    SLA,
                    placeholder="Select SLA",
                    on_change=State.set_custSLA,
                    is_required=True,
                    color="black",
                    bg="white"
                    ),
                center_content=True,
                color="white",
                ),
            pc.container(
                pc.text(
                    "Enter customer availability hours (start/end)",
                    color="white",
                    center_content=True,
                    ),
                pc.hstack(
                    pc.vstack(
                        start_input(State.custstart),
                        pc.text("From: ",State.custstart, color="white"),
                    ),
                    pc.vstack(
                        end_input(State.custend),
                        pc.text("Until: ", State.custend, color="white")
                    ),
                    ),
                ),
            pc.button(
                "Calculate SLA",
                color_scheme="green",
                size="lg",
                on_click=State.senditbish,
                is_disabled=State.button,
                margin_top="1rem",
                ),
            pc.box(
                pc.vstack(
                    pc.text("Calculated SLA", color="white"),
                    pc.text(State.slareturn, color="white"),
                    border_radius="15px",
                    border_color="green",
                    border_width="thick",
                    padding=10,
                    center_content=True
                    ),
                ),
            ),
        #container settings
        width="400px",
        height="70vh",
        center_content=True,
        bg="#1D2330",
        borderRadius="15px",
        boxShadow="41px -41px 82px #0d0f15, -41px 41px 82px #2d374b",
        margin_top="3rem",
        )
    
    #main stack to return
    _main = pc.container(
        login_container,
        #stack Settings
        center_content=True,
        justifyContent="centre",
        maxWidth="auto",
        height="100vh",
        bg="#1D2330",
    )

    #return the main stack
    return _main

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
