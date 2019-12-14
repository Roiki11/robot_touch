class communications():

    def setCom(): 
        try:
            global ser 
            global J1StepCur
            global J2StepCur
            global J3StepCur
            global J4StepCur
            global J5StepCur
            global J6StepCur    
            port = "COM" + comPortEntryField.get()  
            baud = 115200    
            ser = serial.Serial(port,baud)
            almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
            almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            tab6.ElogView.insert(END, Curtime+" - COMMUNICATIONS STARTED WITH TEENSY 3.5")
            value=tab6.ElogView.get(0,END)
            pickle.dump(value,open("ErrorLog","wb"))
            savePosData()
        except:
            almStatusLab.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5", bg = "yellow")
            almStatusLab2.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5", bg = "yellow")
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            tab6.ElogView.insert(END, Curtime+" - UNABLE TO ESTABLISH COMMUNICATIONS WITH TEENSY 3.5")
            value=tab6.ElogView.get(0,END)
            pickle.dump(value,open("ErrorLog","wb"))
            savePosData()

    def setCom2(): 
        try:
            global ser2 
            global J1StepCur
            global J2StepCur
            global J3StepCur
            global J4StepCur
            global J5StepCur
            global J6StepCur    
            port = "COM" + com2PortEntryField.get()  
            baud = 115200    
            ser2 = serial.Serial(port,baud)
            almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
            almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            tab6.ElogView.insert(END, Curtime+" - COMMUNICATIONS STARTED WITH MEGA 2560")
            value=tab6.ElogView.get(0,END)
            pickle.dump(value,open("ErrorLog","wb"))
            savePosData()
        except:
            almStatusLab.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560", bg = "yellow")
            almStatusLab2.config(text="UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560", bg = "yellow")
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            tab6.ElogView.insert(END, Curtime+" - UNABLE TO ESTABLISH COMMUNICATIONS WITH MEGA 2560")
            value=tab6.ElogView.get(0,END)
            pickle.dump(value,open("ErrorLog","wb"))
            savePosData()