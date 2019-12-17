class calibration():

    def applyRobotCal(RobotCode):
        global J1NegAngLim
        global J1PosAngLim
        global J1StepLim
        global J1DegPerStep
        global J1StepCur
        global J1AngCur
        global J2NegAngLim
        global J2PosAngLim
        global J2StepLim
        global J2DegPerStep
        global J2StepCur
        global J2AngCur
        global J3NegAngLim
        global J3PosAngLim
        global J3StepLim
        global J3DegPerStep
        global J3StepCur
        global J3AngCur
        global J4NegAngLim
        global J4PosAngLim
        global J4StepLim
        global J4DegPerStep
        global J4StepCur
        global J4AngCur
        global J5NegAngLim
        global J5PosAngLim
        global J5StepLim
        global J5DegPerStep
        global J5StepCur
        global J5AngCur
        global J6NegAngLim
        global J6PosAngLim
        global J6StepLim
        global J6DegPerStep
        global J6StepCur
        global J6AngCur
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        J1fault = RobotCode[4:5]
        J2fault = RobotCode[5:6]
        J3fault = RobotCode[6:7]
        J4fault = RobotCode[7:8]
        J5fault = RobotCode[8:9]
        J6fault = RobotCode[9:10]
        J1index = RobotCode.find('A')
        J2index = RobotCode.find('B')
        J3index = RobotCode.find('C')
        J4index = RobotCode.find('D')
        J5index = RobotCode.find('E')
        J6index = RobotCode.find('F')
        if (J1OpenLoopStat.get() == 0):
            if (J1fault == "1"):
                almStatusLab.config(text="J1 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J1 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J1 COLLISION OR OUT OF CALIBRATION")
                J1StepCur = int(RobotCode[J1index+1:J2index])
                J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
                J1curAngEntryField.delete(0, 'end')
                J1curAngEntryField.insert(0,str(J1AngCur))
                stopProg()
        if (J2OpenLoopStat.get() == 0):    
            if (J2fault == "1"):
                almStatusLab.config(text="J2 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J2 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J2 COLLISION OR OUT OF CALIBRATION")
                J2StepCur = int(RobotCode[J2index+1:J3index])
                J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
                J2curAngEntryField.delete(0, 'end')
                J2curAngEntryField.insert(0,str(J2AngCur))
                stopProg()
        if (J3OpenLoopStat.get() == 0):    
            if (J3fault == "1"):
                almStatusLab.config(text="J3 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J3 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J3 COLLISION OR OUT OF CALIBRATION")
                J3StepCur = int(RobotCode[J3index+1:J4index])
                J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
                J3curAngEntryField.delete(0, 'end')
                J3curAngEntryField.insert(0,str(J3AngCur))
                stopProg()
        if (J4OpenLoopStat.get() == 0):    
            if (J4fault == "1"):
                almStatusLab.config(text="J4 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J4 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J4 COLLISION OR OUT OF CALIBRATION")
                J4StepCur = int(RobotCode[J4index+1:J5index])
                J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
                J4curAngEntryField.delete(0, 'end')
                J4curAngEntryField.insert(0,str(J4AngCur))
                stopProg()
        if (J5OpenLoopStat.get() == 0):    
            if (J5fault == "1"):
                almStatusLab.config(text="J5 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J5 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J5 COLLISION OR OUT OF CALIBRATION")
                J5StepCur = int(RobotCode[J5index+1:J6index])
                J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
                J5curAngEntryField.delete(0, 'end')
                J5curAngEntryField.insert(0,str(J5AngCur))
                stopProg()      
        if (J6OpenLoopStat.get() == 0):    
            if (J6fault == "1"):
                almStatusLab.config(text="J6 COLLISION OR OUT OF CALIBRATION", bg = "red")
                almStatusLab2.config(text="J6 COLLISION OR OUT OF CALIBRATION", bg = "red")
                tab6.ElogView.insert(END, Curtime+" - "+"J6 COLLISION OR OUT OF CALIBRATION")
                J6StepCur = int(RobotCode[J6index+1:-5])
                J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
                J6curAngEntryField.delete(0, 'end')
                J6curAngEntryField.insert(0,str(J6AngCur))
                stopProg()
        CalcFwdKin()
        DisplaySteps()
        savePosData()
        value=tab6.ElogView.get(0,END)
        pickle.dump(value,open("ErrorLog","wb"))



    def calRobotAll():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "111110"
        speed = "50"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J1caldir == J1motdir):
            J1caldrive = "1"
        else:
            J1caldrive = "0"      
        if(J2caldir == J2motdir):
            J2caldrive = "1"
        else:
            J2caldrive = "0" 
        if(J3caldir == J3motdir):
            J3caldrive = "1"
        else:
            J3caldrive = "0" 
        if(J4caldir == J4motdir):
            J4caldrive = "1"
        else:
            J4caldrive = "0" 	
        if(J5caldir == J5motdir):
            J5caldrive = "1"
        else:
            J5caldrive = "0" 	
        if(J6caldir == J6motdir):
            J6caldrive = "1"
        else:
            J6caldrive = "0"        
        command = "MJA"+J1caldrive+"500"+"B"+J2caldrive+"500"+"C"+J3caldrive+"500"+"D"+J4caldrive+"500"+"E"+J5caldrive+"500"+"F"+J6caldrive+"0"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)
        gotoRestPos()
        calaxis = "000001"
        speed = "50"
        calRobot(calaxis,speed)
        command = "MJA"+J1caldrive+"0"+"B"+J2caldrive+"0"+"C"+J3caldrive+"0"+"D"+J4caldrive+"0"+"E"+J5caldrive+"0"+"F"+J6caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        calaxis = "000001"
        speed = "8"
        time.sleep(1)
        calRobot(calaxis,speed)
        gotoRestPos()
        almStatusLab.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")
        almStatusLab2.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")	
        blockEncPosCal = 0 

    def calRobotJ1():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "100000"
        speed = "20"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J1caldir == J1motdir):
            J1caldrive = "1"
        else:
            J1caldrive = "0"            
        command = "MJA"+J1caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)
        blockEncPosCal = 0 

    def calRobotJ2():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "010000"
        speed = "40"
        calRobot(calaxis,speed)
        ### calc correct calibration direction    
        if(J2caldir == J2motdir):
            J2caldrive = "1"
        else:
            J2caldrive = "0"     
        command = "MJB"+J2caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)  
        blockEncPosCal = 0 

    def calRobotJ3():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "001000"
        speed = "40"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J3caldir == J3motdir):
            J3caldrive = "1"
        else:
            J3caldrive = "0"        
        command = "MJC"+J3caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)  
        blockEncPosCal = 0 

    def calRobotJ4():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "000100"
        speed = "40"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J4caldir == J4motdir):
            J4caldrive = "1"
        else:
            J4caldrive = "0" 	   
        command = "MJD"+J4caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)
        blockEncPosCal = 0   

    def calRobotJ5():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "000010"
        speed = "40"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J5caldir == J5motdir):
            J5caldrive = "1"
        else:
            J5caldrive = "0" 	       
        command = "MJE"+J5caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)
        blockEncPosCal = 0   

    def calRobotJ6():
        global blockEncPosCal
        blockEncPosCal = 1
        calaxis = "000001"
        speed = "40"
        calRobot(calaxis,speed)
        ### calc correct calibration direction
        if(J6caldir == J6motdir):
            J6caldrive = "1"
        else:
            J6caldrive = "0"        
        command = "MJF"+J6caldrive+"500"+"S15G10H10I10K10"+"\n"
        ser.write(command.encode())
        ser.flushInput()
        speed = "8"
        time.sleep(2.5)
        calRobot(calaxis,speed)
        blockEncPosCal = 0  
            
        

    def calRobot(calaxis,speed):
        J1axis = calaxis[:-5]
        J2axis = calaxis[1:-4]
        J3axis = calaxis[2:-3]
        J4axis = calaxis[3:-2]
        J5axis = calaxis[4:-1]
        J6axis = calaxis[5:]
        ###
        if (J1axis == "1"):
            J1step = str(J1StepLim)
        else:
            J1step = "0"
        if (J2axis == "1"):
            J2step = str(J2StepLim)
        else:
            J2step = "0" 	
        if (J3axis == "1"):
            J3step = str(J3StepLim)
        else:
            J3step = "0" 	
        if (J4axis == "1"):
            J4step = str(J4StepLim)
        else:
            J4step = "0" 
        if (J5axis == "1"):
            J5step = str(J5StepLim)
        else:
            J5step = "0" 
        if (J6axis == "1"):
            J6step = str(J6StepLim)
        else:
            J6step = "0" 	
        ### calc correct calibration direction
        if(J1caldir == J1motdir):
            J1caldrive = "0"
        else:
            J1caldrive = "1"      
        if(J2caldir == J2motdir):
            J2caldrive = "0"
        else:
            J2caldrive = "1" 
        if(J3caldir == J3motdir):
            J3caldrive = "0"
        else:
            J3caldrive = "1" 
        if(J4caldir == J4motdir):
            J4caldrive = "0"
        else:
            J4caldrive = "1" 	
        if(J5caldir == J5motdir):
            J5caldrive = "0"
        else:
            J5caldrive = "1" 	
        if(J6caldir == J6motdir):
            J6caldrive = "0"
        else:
            J6caldrive = "1"    
        command = "LL"+"A"+J1caldrive+J1step+"B"+J2caldrive+J2step+"C"+J3caldrive+J3step+"D"+J4caldrive+J4step+"E"+J5caldrive+J5step+"F"+J6caldrive+J6step+"S"+str(speed)+"\n"  
        ser.write(command.encode())
        ser.flushInput()
        calvalue = ser.read()
        global calStat
        if (calvalue == b'P'):
            calStat = 1
            calibration.delete(0, END)
            ##J1##
            global J1StepCur
            global J1AngCur
            if (J1axis == "1"):
                if (J1caldir == "0"):
                    J1StepCur = 0
                    J1AngCur = J1NegAngLim
                else:
                    J1StepCur = J1StepLim
                    J1AngCur = J1PosAngLim
                J1curAngEntryField.delete(0, 'end')
                J1curAngEntryField.insert(0,str(J1AngCur))
            ###########
            ##J2##
            global J2StepCur
            global J2AngCur
            if (J2axis == "1"):
                if (J2caldir == "0"):
                    J2StepCur = 0
                    J2AngCur = J2NegAngLim
                else:
                    J2StepCur = J2StepLim
                    J2AngCur = J2PosAngLim
                J2curAngEntryField.delete(0, 'end')
                J2curAngEntryField.insert(0,str(J2AngCur))
            ###########
            ##J3##
            global J3StepCur
            global J3AngCur
            if (J3axis == "1"):
                if (J3caldir == "0"):
                    J3StepCur = 0
                    J3AngCur = J3NegAngLim
                else:
                    J3StepCur = J3StepLim
                    J3AngCur = J3PosAngLim
                J3curAngEntryField.delete(0, 'end')
                J3curAngEntryField.insert(0,str(J3AngCur))
            ###########
            ##J4##
            global J4StepCur
            global J4AngCur
            if (J4axis == "1"):
                if (J4caldir == "0"):
                    J4StepCur = 0
                    J4AngCur = J4NegAngLim
                else:
                    J4StepCur = J4StepLim
                    J4AngCur = J4PosAngLim
                J4curAngEntryField.delete(0, 'end')
                J4curAngEntryField.insert(0,str(J4AngCur))
            ###########	
            ##J5##
            global J5StepCur
            global J5AngCur
            if (J5axis == "1"):
                if (J5caldir == "0"):
                    J5StepCur = 0
                    J5AngCur = J5NegAngLim
                else:
                    J5StepCur = J5StepLim
                    J5AngCur = J5PosAngLim
                J5curAngEntryField.delete(0, 'end')
                J5curAngEntryField.insert(0,str(J5AngCur))
            ###########	
            ##J6##
            global J6StepCur
            global J6AngCur
            if (J6axis == "1"):
                if (J6caldir == "0"):
                    J6StepCur = 0
                    J6AngCur = J6NegAngLim
                else:
                    J6StepCur = J6StepLim
                    J6AngCur = J6PosAngLim
                J6curAngEntryField.delete(0, 'end')
                J6curAngEntryField.insert(0,str(J6AngCur))
            ###########		
            value=calibration.get(0,END)
            pickle.dump(value,open("ARbot.cal","wb"))
            almStatusLab.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")
            almStatusLab2.config(text='CALIBRATION SUCCESSFUL', bg = "cornflowerblue")	
            DisplaySteps()
        else:
            if (calvalue == b'F'):
                calStat = 0
                almStatusLab.config(text="CALIBRATION FAILED", bg = "red")
                almStatusLab2.config(text="CALIBRATION FAILED", bg = "red")
            else:
                almStatusLab.config(text="NO CAL FEEDBACK FROM ARDUINO", bg = "red")
                almStatusLab2.config(text="NO CAL FEEDBACK FROM ARDUINO", bg = "red")	  
        CalcFwdKin()	  
        savePosData()
        command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
        ser.write(command.encode())
        ser.flushInput()


    def calRobotMid():
        Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
        calibration.delete(0, END)
        ##J1##
        global J1StepCur
        global J1AngCur
        J1StepCur = J1StepLim/2
        J1AngCur = 0
        J1curAngEntryField.delete(0, 'end')
        J1curAngEntryField.insert(0,str(J1AngCur))
        ###########
        ##J2## j2 goes to -90 given axis not centered
        global J2StepCur
        global J2AngCur
        J2StepCur = (J2StepLim/abs(J2NegAngLim))*(abs(J2NegAngLim)-90)
        J2AngCur = -90
        J2curAngEntryField.delete(0, 'end')
        J2curAngEntryField.insert(0,str(J2AngCur))
        ###########
        ##J3##  j3 goes to 1 given axis not centered
        global J3StepCur
        global J3AngCur
        J3StepCur = 0
        J3AngCur = 1.05
        J3curAngEntryField.delete(0, 'end')
        J3curAngEntryField.insert(0,str(J3AngCur))
        ###########
        ##J4##
        global J4StepCur
        global J4AngCur
        J4StepCur = J4StepLim/2
        J4AngCur = 0
        J4curAngEntryField.delete(0, 'end')
        J4curAngEntryField.insert(0,str(J4AngCur))
        ###########
        ##J5##
        global J5StepCur
        global J5AngCur
        J5StepCur = J5StepLim/2
        J5AngCur = 0
        J5curAngEntryField.delete(0, 'end')
        J5curAngEntryField.insert(0,str(J5AngCur))
        ###########
        ##J6##
        global J6StepCur
        global J6AngCur
        J6StepCur = J6StepLim/2
        J6AngCur = 0
        J6curAngEntryField.delete(0, 'end')
        J6curAngEntryField.insert(0,str(J6AngCur))
        ###########
        ##J7##
        global TrackStepLim
        global TrackcurPos
        global TrackLength
        TrackStepLim = TrackStepLim/2
        TrackcurPos = TrackLength/2
        TrackcurEntryField.delete(0, 'end')
        TrackcurEntryField.insert(0,str(TrackcurPos))
        ###########  
        value=calibration.get(0,END)
        pickle.dump(value,open("ARbot.cal","wb"))
        almStatusLab.config(text="CALIBRATED TO REST POSITION", bg = "orange")
        almStatusLab2.config(text="CALIBRATED TO REST POSITION", bg = "orange")
        tab6.ElogView.insert(END, Curtime+" - "+"CALIBRATED TO REST POSITION")
        CalcFwdKin()
        DisplaySteps()
        savePosData()
        command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
        ser.write(command.encode())
        ser.flushInput()

    def savePosData():
        calibration.delete(0, END)
        calibration.insert(END, J1StepCur)
        calibration.insert(END, J1AngCur)
        calibration.insert(END, J2StepCur)
        calibration.insert(END, J2AngCur)
        calibration.insert(END, J3StepCur)
        calibration.insert(END, J3AngCur)
        calibration.insert(END, J4StepCur)
        calibration.insert(END, J4AngCur)
        calibration.insert(END, J5StepCur)
        calibration.insert(END, J5AngCur)
        calibration.insert(END, J6StepCur)
        calibration.insert(END, J6AngCur)
        calibration.insert(END, comPortEntryField.get())  
        calibration.insert(END, ProgEntryField.get())
        calibration.insert(END, servo0onEntryField.get())
        calibration.insert(END, servo0offEntryField.get())
        calibration.insert(END, servo1onEntryField.get())
        calibration.insert(END, servo1offEntryField.get())
        calibration.insert(END, DO1onEntryField.get())
        calibration.insert(END, DO1offEntryField.get())
        calibration.insert(END, DO2onEntryField.get())
        calibration.insert(END, DO2offEntryField.get())
        calibration.insert(END, UFxEntryField.get())
        calibration.insert(END, UFyEntryField.get())
        calibration.insert(END, UFzEntryField.get())
        calibration.insert(END, UFrxEntryField.get())
        calibration.insert(END, UFryEntryField.get())
        calibration.insert(END, UFrzEntryField.get())
        calibration.insert(END, TFxEntryField.get())
        calibration.insert(END, TFyEntryField.get())
        calibration.insert(END, TFzEntryField.get())
        calibration.insert(END, TFrxEntryField.get())
        calibration.insert(END, TFryEntryField.get())
        calibration.insert(END, TFrzEntryField.get())
        calibration.insert(END, fineCalEntryField.get())
        calibration.insert(END, J1NegAngLimEntryField.get())
        calibration.insert(END, J1PosAngLimEntryField.get())
        calibration.insert(END, J1StepLimEntryField.get())
        calibration.insert(END, J2NegAngLimEntryField.get())
        calibration.insert(END, J2PosAngLimEntryField.get())
        calibration.insert(END, J2StepLimEntryField.get())
        calibration.insert(END, J3NegAngLimEntryField.get())
        calibration.insert(END, J3PosAngLimEntryField.get())
        calibration.insert(END, J3StepLimEntryField.get())
        calibration.insert(END, J4NegAngLimEntryField.get())
        calibration.insert(END, J4PosAngLimEntryField.get())
        calibration.insert(END, J4StepLimEntryField.get())
        calibration.insert(END, J5NegAngLimEntryField.get())
        calibration.insert(END, J5PosAngLimEntryField.get())
        calibration.insert(END, J5StepLimEntryField.get())
        calibration.insert(END, J6NegAngLimEntryField.get())
        calibration.insert(END, J6PosAngLimEntryField.get())
        calibration.insert(END, J6StepLimEntryField.get())
        calibration.insert(END, DHr1EntryField.get())
        calibration.insert(END, DHr2EntryField.get())
        calibration.insert(END, DHr3EntryField.get())
        calibration.insert(END, DHr4EntryField.get())
        calibration.insert(END, DHr5EntryField.get())
        calibration.insert(END, DHr6EntryField.get())
        calibration.insert(END, DHa1EntryField.get())
        calibration.insert(END, DHa2EntryField.get())
        calibration.insert(END, DHa3EntryField.get())
        calibration.insert(END, DHa4EntryField.get())
        calibration.insert(END, DHa5EntryField.get())
        calibration.insert(END, DHa6EntryField.get())
        calibration.insert(END, DHd1EntryField.get())
        calibration.insert(END, DHd2EntryField.get())
        calibration.insert(END, DHd3EntryField.get())
        calibration.insert(END, DHd4EntryField.get())
        calibration.insert(END, DHd5EntryField.get())
        calibration.insert(END, DHd6EntryField.get())
        calibration.insert(END, DHt1EntryField.get())
        calibration.insert(END, DHt2EntryField.get())
        calibration.insert(END, DHt3EntryField.get())
        calibration.insert(END, DHt4EntryField.get())
        calibration.insert(END, DHt5EntryField.get())
        calibration.insert(END, DHt6EntryField.get())
        calibration.insert(END, CalDirEntryField.get())
        calibration.insert(END, MotDirEntryField.get())
        calibration.insert(END, TrackcurEntryField.get())
        calibration.insert(END, TrackLengthEntryField.get())
        calibration.insert(END, TrackStepLimEntryField.get())
        calibration.insert(END, VisFileLocEntryField.get())
        calibration.insert(END, visoptions.get())
        calibration.insert(END, VisPicOxPEntryField.get())
        calibration.insert(END, VisPicOxMEntryField.get())
        calibration.insert(END, VisPicOyPEntryField.get())
        calibration.insert(END, VisPicOyMEntryField.get())
        calibration.insert(END, VisPicXPEntryField.get())
        calibration.insert(END, VisPicXMEntryField.get())
        calibration.insert(END, VisPicYPEntryField.get())
        calibration.insert(END, VisPicYMEntryField.get())
        calibration.insert(END, com2PortEntryField.get())
        calibration.insert(END, J1OpenLoopVal)
        calibration.insert(END, J2OpenLoopVal)
        calibration.insert(END, J3OpenLoopVal)
        calibration.insert(END, J4OpenLoopVal)
        calibration.insert(END, J5OpenLoopVal)
        calibration.insert(END, J6OpenLoopVal)
        ###########
        value=calibration.get(0,END)
        pickle.dump(value,open("ARbot.cal","wb"))

    def SaveAndApplyCalibration():
        global J1NegAngLim
        global J1PosAngLim
        global J1StepLim
        global J1DegPerStep
        global J1StepCur
        global J1AngCur
        global J2NegAngLim
        global J2PosAngLim
        global J2StepLim
        global J2DegPerStep
        global J2StepCur
        global J2AngCur
        global J2NegAngLim
        global J2PosAngLim
        global J2StepLim
        global J2DegPerStep
        global J2StepCur
        global J2AngCur
        global J3NegAngLim
        global J3PosAngLim
        global J3StepLim
        global J3DegPerStep
        global J3StepCur
        global J3AngCur
        global J4NegAngLim
        global J4PosAngLim
        global J4StepLim
        global J4DegPerStep
        global J4StepCur
        global J4AngCur
        global J5NegAngLim
        global J5PosAngLim
        global J5StepLim
        global J5DegPerStep
        global J5StepCur
        global J5AngCur
        global J6NegAngLim
        global J6PosAngLim
        global J6StepLim
        global J6DegPerStep
        global J6StepCur
        global J6AngCur
        global XcurPos
        global YcurPos
        global ZcurPos
        global RxcurPos
        global RycurPos
        global RzcurPos
        global DHr1
        global DHr2
        global DHr3
        global DHr4
        global DHr5
        global DHr6
        global DHa1
        global DHa2
        global DHa3
        global DHa4
        global DHa5
        global DHa6
        global DHd1
        global DHd2
        global DHd3
        global DHd4
        global DHd5
        global DHd6
        global DHt1
        global DHt2
        global DHt3
        global DHt4
        global DHt5
        global DHt6
        global CalDir
        global J1caldir
        global J2caldir
        global J3caldir
        global J4caldir
        global J5caldir
        global J6caldir 
        global MotDir
        global J1motdir
        global J2motdir
        global J3motdir
        global J4motdir
        global J5motdir
        global J6motdir
        global TrackcurPos
        global TrackLength
        global TrackStepLim
        global VisFileLoc
        global VisProg
        global VisOrigXpix
        global VisOrigXmm
        global VisOrigYpix
        global VisOrigYmm
        global VisEndXpix
        global VisEndXmm
        global VisEndYpix
        global VisEndYmm 
        global J1OpenLoopVal
        global J2OpenLoopVal
        global J3OpenLoopVal
        global J4OpenLoopVal
        global J5OpenLoopVal
        global J6OpenLoopVal 
        ###joint variables
        J1NegAngLim = float(J1NegAngLimEntryField.get())
        J1PosAngLim = float(J1PosAngLimEntryField.get())
        J1StepLim = int(J1StepLimEntryField.get())
        J1DegPerStep = float((J1PosAngLim - J1NegAngLim)/float(J1StepLim))
        J2NegAngLim = float(J2NegAngLimEntryField.get())
        J2PosAngLim = float(J2PosAngLimEntryField.get())
        J2StepLim = int(J2StepLimEntryField.get())
        J2DegPerStep = float((J2PosAngLim - J2NegAngLim)/float(J2StepLim))
        J3NegAngLim = float(J3NegAngLimEntryField.get())
        J3PosAngLim = float(J3PosAngLimEntryField.get())
        J3StepLim = int(J3StepLimEntryField.get())
        J3DegPerStep = float((J3PosAngLim - J3NegAngLim)/float(J3StepLim))
        J4NegAngLim = float(J4NegAngLimEntryField.get())
        J4PosAngLim = float(J4PosAngLimEntryField.get())
        J4StepLim = int(J4StepLimEntryField.get())
        J4DegPerStep = float((J4PosAngLim - J4NegAngLim)/float(J4StepLim))
        J5NegAngLim = float(J5NegAngLimEntryField.get())
        J5PosAngLim = float(J5PosAngLimEntryField.get())
        J5StepLim = int(J5StepLimEntryField.get())
        J5DegPerStep = float((J5PosAngLim - J5NegAngLim)/float(J5StepLim))
        J6NegAngLim = float(J6NegAngLimEntryField.get())
        J6PosAngLim = float(J6PosAngLimEntryField.get())
        J6StepLim = int(J6StepLimEntryField.get())
        J6DegPerStep = float((J6PosAngLim - J6NegAngLim)/float(J6StepLim))
        ####AXIS LIMITS LABELS GREEN######
        AxLimCol = "OliveDrab4"
        J1PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J1PosAngLim)))
        J1PlimLab.place(x=685, y=10)
        J1NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J1NegAngLim)))
        J1NlimLab.place(x=635, y=10)
        J2PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J2PosAngLim)))
        J2PlimLab.place(x=780, y=10)
        J2NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J2NegAngLim)))
        J2NlimLab.place(x=725, y=10)
        J3PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J3PosAngLim)))
        J3PlimLab.place(x=868, y=10)
        J3NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J3NegAngLim)))
        J3NlimLab.place(x=825, y=10)
        J4PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J4PosAngLim)))
        J4PlimLab.place(x=960, y=10)
        J4NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J4NegAngLim)))
        J4NlimLab.place(x=905, y=10)
        J5PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J5PosAngLim)))
        J5PlimLab.place(x=1050, y=10)
        J5NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J5NegAngLim)))
        J5NlimLab.place(x=995, y=10)
        J6PlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = "+"+str(int(J6PosAngLim)))
        J6PlimLab.place(x=1140, y=10)
        J6NlimLab = Label(tab1, font=("Arial", 8), fg=AxLimCol, text = str(int(J6NegAngLim)))
        J6NlimLab.place(x=1085, y=10)
        DHr1 = float(DHr1EntryField.get())
        DHr2 = float(DHr2EntryField.get())
        DHr3 = float(DHr3EntryField.get())
        DHr4 = float(DHr4EntryField.get())
        DHr5 = float(DHr5EntryField.get())
        DHr6 = float(DHr6EntryField.get())
        DHa1 = float(DHa1EntryField.get())
        DHa2 = float(DHa2EntryField.get())
        DHa3 = float(DHa3EntryField.get())
        DHa4 = float(DHa4EntryField.get())
        DHa5 = float(DHa5EntryField.get())
        DHa6 = float(DHa6EntryField.get())
        DHd1 = float(DHd1EntryField.get())
        DHd2 = float(DHd2EntryField.get())
        DHd3 = float(DHd3EntryField.get())
        DHd4 = float(DHd4EntryField.get())
        DHd5 = float(DHd5EntryField.get())
        DHd6 = float(DHd6EntryField.get())
        DHt1 = float(DHt1EntryField.get())
        DHt2 = float(DHt2EntryField.get())
        DHt3 = float(DHt3EntryField.get())
        DHt4 = float(DHt4EntryField.get())
        DHt5 = float(DHt5EntryField.get())
        DHt6 = float(DHt6EntryField.get())
        CalDir = CalDirEntryField.get()
        J1caldir = CalDir[:-5]
        J2caldir = CalDir[1:-4]
        J3caldir = CalDir[2:-3]
        J4caldir = CalDir[3:-2]
        J5caldir = CalDir[4:-1]
        J6caldir = CalDir[5:] 
        MotDir = MotDirEntryField.get()
        J1motdir = MotDir[:-5]
        J2motdir = MotDir[1:-4]
        J3motdir = MotDir[2:-3]
        J4motdir = MotDir[3:-2]
        J5motdir = MotDir[4:-1]
        J6motdir = MotDir[5:]
        TrackcurPos = float(TrackcurEntryField.get())
        TrackLength = float(TrackLengthEntryField.get())
        TrackStepLim = float(TrackStepLimEntryField.get())
        VisFileLoc = VisFileLocEntryField.get()
        VisProg = visoptions.get()
        VisOrigXpix = float(VisPicOxPEntryField.get())
        VisOrigXmm  = float(VisPicOxMEntryField.get())
        VisOrigYpix = float(VisPicOyPEntryField.get())
        VisOrigYmm  = float(VisPicOyMEntryField.get())
        VisEndXpix  = float(VisPicXPEntryField.get())
        VisEndXmm   = float(VisPicXMEntryField.get())
        VisEndYpix  = float(VisPicYPEntryField.get())
        VisEndYmm   = float(VisPicYMEntryField.get())
        J1OpenLoopVal = int(J1OpenLoopStat.get())
        J2OpenLoopVal = int(J2OpenLoopStat.get())
        J3OpenLoopVal = int(J3OpenLoopStat.get())
        J4OpenLoopVal = int(J4OpenLoopStat.get())
        J5OpenLoopVal = int(J5OpenLoopStat.get())
        J6OpenLoopVal = int(J6OpenLoopStat.get())

        savePosData()
        

    def gotoFineCalPos():
        command = fineCalEntryField.get() 
        J1newIndex = command.find("X) ")
        J2newIndex = command.find("Y) ")
        J3newIndex = command.find("Z) ")
        J4newIndex = command.find("W) ")
        J5newIndex = command.find("P) ")
        J6newIndex = command.find("R) ")
        TRnewIndex = command.find("T) ")	
        SpeedIndex = command.find("Speed-")
        ACCdurIndex = command.find("Ad")
        ACCspdIndex = command.find("As")
        DECdurIndex = command.find("Dd")
        DECspdIndex = command.find("Ds")
        WristConfIndex = command.find("$")
        CX = float(command[J1newIndex+3:J2newIndex-1])
        CY = float(command[J2newIndex+3:J3newIndex-1])
        CZ = float(command[J3newIndex+3:J4newIndex-1])
        CRx = float(command[J4newIndex+3:J5newIndex-1])
        CRy = float(command[J5newIndex+3:J6newIndex-1])
        CRz = float(command[J6newIndex+3:TRnewIndex-1])
        Track = float(command[TRnewIndex+3:SpeedIndex-1])
        newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
        ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
        ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
        DECdur = command[DECdurIndex+3:DECspdIndex-1]
        DECspd = command[DECspdIndex+3:WristConfIndex-1]
        WC = command[WristConfIndex+1:]
        TCX = 0
        TCY = 0 
        TCZ = 0
        TCRx = 0
        TCRy = 0
        TCRz = 0
        Code = 0  
        MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
        almStatusLab.config(text="MOVED TO FINE CALIBRATION POSITION", bg = "yellow")
        almStatusLab2.config(text="MOVED TO FINE CALIBRATION POSITION", bg = "yellow")
        
        
    def gotoRestPos():
        command = "Move J [*]  X) 68.944   Y) 0.0   Z) 733.607   W) -90.0   P) 1.05   R) -90.0   T) 201.5   Speed-50 Ad 15 As 10 Dd 20 Ds 5 $F" 
        J1newIndex = command.find("X) ")
        J2newIndex = command.find("Y) ")
        J3newIndex = command.find("Z) ")
        J4newIndex = command.find("W) ")
        J5newIndex = command.find("P) ")
        J6newIndex = command.find("R) ")
        TRnewIndex = command.find("T) ")	
        SpeedIndex = command.find("Speed-")
        ACCdurIndex = command.find("Ad")
        ACCspdIndex = command.find("As")
        DECdurIndex = command.find("Dd")
        DECspdIndex = command.find("Ds")
        WristConfIndex = command.find("$")
        CX = float(command[J1newIndex+3:J2newIndex-1])
        CY = float(command[J2newIndex+3:J3newIndex-1])
        CZ = float(command[J3newIndex+3:J4newIndex-1])
        CRx = float(command[J4newIndex+3:J5newIndex-1])
        CRy = float(command[J5newIndex+3:J6newIndex-1])
        CRz = float(command[J6newIndex+3:TRnewIndex-1])
        Track = float(command[TRnewIndex+3:SpeedIndex-1])
        newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
        ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
        ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
        DECdur = command[DECdurIndex+3:DECspdIndex-1]
        DECspd = command[DECspdIndex+3:WristConfIndex-1]
        WC = command[WristConfIndex+1:]
        TCX = 0
        TCY = 0 
        TCZ = 0
        TCRx = 0
        TCRy = 0
        TCRz = 0
        Code = 0  
        MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

        
    def exeFineCalPos():
        global J1StepCur
        global J2StepCur
        global J3StepCur
        global J4StepCur
        global J5StepCur
        global J6StepCur
        command = fineCalEntryField.get() 
        J1newIndex = command.find("X) ")
        J2newIndex = command.find("Y) ")
        J3newIndex = command.find("Z) ")
        J4newIndex = command.find("W) ")
        J5newIndex = command.find("P) ")
        J6newIndex = command.find("R) ")
        TRnewIndex = command.find("T) ")	
        SpeedIndex = command.find("Speed-")
        ACCdurIndex = command.find("Ad")
        ACCspdIndex = command.find("As")
        DECdurIndex = command.find("Dd")
        DECspdIndex = command.find("Ds")
        WristConfIndex = command.find("$")
        CX = float(command[J1newIndex+3:J2newIndex-1])
        CY = float(command[J2newIndex+3:J3newIndex-1])
        CZ = float(command[J3newIndex+3:J4newIndex-1])
        CRx = float(command[J4newIndex+3:J5newIndex-1])
        CRy = float(command[J5newIndex+3:J6newIndex-1])
        CRz = float(command[J6newIndex+3:TRnewIndex-1])
        Track = float(command[TRnewIndex+3:SpeedIndex-1])
        newSpeed = str(command[SpeedIndex+6:ACCdurIndex-1])
        ACCdur = command[ACCdurIndex+3:ACCspdIndex-1]
        ACCspd = command[ACCspdIndex+3:DECdurIndex-1]
        DECdur = command[DECdurIndex+3:DECspdIndex-1]
        DECspd = command[DECspdIndex+3:WristConfIndex-1]
        WC = command[WristConfIndex+1:]
        TCX = 0
        TCY = 0 
        TCZ = 0
        TCRx = 0
        TCRy = 0
        TCRz = 0
        Code = 1  
        MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
        almStatusLab.config(text="CALIBRATED TO FINE CALIBRATE POSITION", bg = "orange")
        almStatusLab2.config(text="CALIBRATED TO FINE CALIBRATE POSITION", bg = "orange")  
        CalcFwdKin()
        DisplaySteps()
        savePosData()
        command = "LM"+"A"+str(J1StepCur)+"B"+str(J2StepCur)+"C"+str(J3StepCur)+"D"+str(J4StepCur)+"E"+str(J5StepCur)+"F"+str(J6StepCur)+"\n"  
        ser.write(command.encode())
        ser.flushInput()

    def CalTrackPos():
        global TrackcurPos  
        TrackcurPos = 0 
        TrackcurEntryField.delete(0, 'end')  
        TrackcurEntryField.insert(0,str(TrackcurPos))
        savePosData()   
        
        
    