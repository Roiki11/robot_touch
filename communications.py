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
            global baudRate

            port = "COM" + Ui.comPort1.text()
            baud = baudRate     
            ser2 = serial.Serial(port,baud)
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
            
            
        except:
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
          
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