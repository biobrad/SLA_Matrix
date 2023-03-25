import tkinter
import customtkinter
from tkinter import font
from tkinter import ttk
from datetime import datetime

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("500x600")
        self.title("SLA Matrix")
        self.minsize(300, 200)
           
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.mainframe = customtkinter.CTkFrame(self, width=300, height=500)
        self.mainframe.grid(row=0, column=0,columnspan=2, padx=20, pady=20)
        self.mainframe.grid_rowconfigure((0,1,2), weight=1)
        self.mainframe.grid_columnconfigure(0, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.mainframe, text="SLA MATRIX", fg_color=("white", "#3399FF"), corner_radius=8, font=customtkinter.CTkFont(size=30, weight="bold"))
        self.logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 0))
        self.my_frame = customtkinter.CTkFrame(master=self.mainframe)
        self.my_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0))                                                                    
      
        self.sla_var = ""
        self.datentime = ""
        self.starttime = ""
        self.endtime = ""

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
        
        def combobox_callback(choice):
            self.sla_var = choice
        
        def button_callback(datentime, sla_var, starttime, endtime):
            print("create: " + datentime, "SLA: " + sla_var, "Start: " + starttime, "End: " + endtime)
                                                                              
        self.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        self.grid_columnconfigure((0,1), weight=1)
        self.label1 = customtkinter.CTkLabel(master=self.my_frame, text="Copy/Paste SC create date/time", fg_color=("white", "#3399FF"), corner_radius=8, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label1.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 0))
        self.entry1 = customtkinter.CTkEntry(master=self.my_frame, placeholder_text="1-1-2023 00:00:00", text_color="white")
        self.entry1.grid(row=1, column=0, columnspan=2, padx=0, pady=(5,0))
        self.label2 = customtkinter.CTkLabel(master=self.my_frame, text="Customer Availability", fg_color=("white", "#3399FF"), corner_radius=8, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label2.grid(row=2, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="n")
        self.label3 = customtkinter.CTkLabel(master=self.my_frame, text="Start", justify="center")
        self.label3.grid(row=3, column=0, padx=20, pady=0)
        self.label4 = customtkinter.CTkLabel(master=self.my_frame, text="End", justify="center")
        self.label4.grid(row=3, column=1, padx=20, pady=0)
        self.entry2 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd2, placeholder_text="HHMM")
        self.entry2.grid(row=4, column=0, padx=20)
        
        self.label_error2 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent')
        self.label_error2.grid(row=5, column=0, padx=1)
        
        self.entry3 = customtkinter.CTkEntry(master=self.my_frame, validate="focusout", validatecommand=self.vcmd3, placeholder_text="HHMM")
        self.entry3.grid(row=4, column=1, padx=20)
        
        self.label_error3 = customtkinter.CTkLabel(self.my_frame, text="", fg_color='transparent')
        self.label_error3.grid(row=5, column=1, padx=1)
        
        self.label5 = customtkinter.CTkLabel(master=self.my_frame, text="Select SLA in Hours", fg_color=("white", "#3399FF"), corner_radius=8, font=customtkinter.CTkFont(size=15, weight="bold"))
        self.label5.grid(row=6, column=0, columnspan=2, padx=20, pady=0)
        self.combobox = customtkinter.CTkComboBox(master=self.my_frame,
                                     values=["4", "8", "12", "24"],
                                     command=combobox_callback,
                                     variable=self.sla_var)
        self.combobox.grid(row=7, columnspan=2, padx=20, pady=10)
        self.button = customtkinter.CTkButton(master=self.my_frame, command=button_callback, text="Get Calculated SLA", width=200, height=60, fg_color=("white", "green"), font=customtkinter.CTkFont(size=15, weight="bold"))
        self.button.grid(row=8, column=0, columnspan=2, padx=20, pady=(0,10))
        self.textbox = customtkinter.CTkTextbox(master=self.mainframe, width=200, height=60)
        self.textbox.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")
        self.textbox.configure(state="disabled")

   

if __name__ == "__main__":
    app = App()
    app.mainloop()
