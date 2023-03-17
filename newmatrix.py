import pynecone as pc
from datetime import datetime
from .slascript import getsla

SLA = ["24", "12", "8", "4"]

class State(pc.State):
    """"Base State"""
    datentime: str = ""
    custSLA: int = ""
    custstart: str = ""
    custend: int = ""
    slareturn: str = ""
    input1: int
    input2: int
    
    def senditbish(self):
        self.slareturn
        self.slareturn=getsla(self.datentime, self.custSLA, self.custstart, self.custend)
        #return slareturn
        
    def validate_time(custstart):
        try:
            if len(custstart) == 4: 
                datetime.strptime(custstart, '%H%M')
            return False
        else: return True
        
        except ValueError:
            return True    
    
def start_input(custstart):
    return pc.input(
        on_blur=State.set_custstart,
        in_invalid=validate_time(State.custstart),
        is_required=True,
        error_border_color="red",
        color="black",
        bg="white"
        )

def end_input(custend):
    return pc.number_input(
        on_change=State.set_custend,
        max_=2359,
        min_=0000,
        keep_within_range=True,
        is_required=True,
        color="black",
        bg="white"
        )



def displayselections():
    return pc.container(
            pc.vstack(
            pc.text("Selections",as_="b"),
            pc.text("Case create date/time:"),
            pc.text(State.datentime),
            pc.text("SLA Selected: " + State.custSLA),
            pc.text("Cust availability"),
            pc.text("From: ",State.custstart, "until: ",State.custend),
            ),
            color="white"
    )
     
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
                    placeholder="1/1/1111 00:00:00",
                    on_blur=State.set_datentime,
                    is_required=True,
                    color="black",
                    bg="white",
                    ),
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
                    start_input(State.custstart),
                    end_input(State.custend),
                    ),
                margin_top="1rem",
                ),
            pc.box(
                displayselections(),
                border_radius="sm",
                border_color="white",
                border_width="thin",
                padding=1,
                width="80%",
                center_content=True
            ),
            pc.button(
                "Calculate SLA",
                color_scheme="green",
                size="lg",
                on_click=State.senditbish,
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
        height="85vh",
        center_content=True,
        bg="#1D2330",
        borderRadius="15px",
        boxShadow="41px -41px 82px #0d0f15, -41px 41px 82px #2d374b",
        )
    
    #main stack to return
    _main = pc.container(
        login_container,
        #stack Settings
        center_content=True,
        justifyContent="centre",
        maxWidth="auto",
        height="100vh",
        bg="#1D2330"
    )

    #return the main stack
    return _main

# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
