class communications:

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
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
            savePosData()
        except:
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
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


    def getRobotPosition():
        commandCalc = "GP"+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
        ser.write(commandCalc.encode())
        RobotCode = str(ser.readline())
        Pcode = RobotCode[2:4]
        if (Pcode == "01"):
            applyRobotCal(RobotCode)

    def monitorEncoders():
        global blockEncPosMove
        global blockEncPosCal
        while True:
            if blockEncPosMove == 0 and blockEncPosCal == 0:
                getRobotPosition()
                time.sleep(0.2)  