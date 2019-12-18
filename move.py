class move:
  def MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code):
        global commandCalc
        global blockEncPosMove
        blockEncPosMove = 1
        CalcRevKin(CX,CY,CZ,CRx,CRy,CRz,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz)
        MoveNew(J1out,J2out,J3out,J4out,J5out,J6out,newSpeed,ACCdur,ACCspd,DECdur,DECspd,Track,Code)
        blockEncPosMove = 0
        if Code == 2 or Code == 3:
            return(commandCalc)
  def MoveNew(J1out,J2out,J3out,J4out,J5out,J6out,newSpeed,ACCdur,ACCspd,DECdur,DECspd,Track,Code):
        global xboxUse
        if xboxUse != 1:
            almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
            almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
        global J1AngCur
        global J2AngCur
        global J3AngCur
        global J4AngCur
        global J5AngCur
        global J6AngCur
        global J1StepCur
        global J2StepCur
        global J3StepCur
        global J4StepCur
        global J5StepCur
        global J6StepCur
        global TrackcurPos
        global TrackLength
        global TrackStepLim
        global commandCalc  
        J1newAng = J1out
        J2newAng = J2out
        J3newAng = J3out
        J4newAng = J4out
        J5newAng = J5out
        J6newAng = J6out
        TrackNew = Track
        ###CHECK WITHIN ANGLE LIMITS
        #if (J1newAng < J1NegAngLim or J1newAng > J1PosAngLim) or (J2newAng < J2NegAngLim or J2newAng > J2PosAngLim) or (J3newAng < J3NegAngLim or J3newAng > J3PosAngLim) or (J4newAng < J4NegAngLim or J4newAng > J4PosAngLim) or (J5newAng < J5NegAngLim or J5newAng > J5PosAngLim) or (J6newAng < J6NegAngLim or J6newAng > J6PosAngLim or TrackNew < 0 or TrackNew > TrackLength):
            #almStatusLab.config(text="AXIS LIMIT", bg = "red")
            #almStatusLab2.config(text="AXIS LIMIT", bg = "red")
            #tab1.runTrue = 0
        if (J1newAng < J1NegAngLim or J1newAng > J1PosAngLim): 
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        elif (J2newAng < J2NegAngLim or J2newAng > J2PosAngLim): 
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        elif (J3newAng < J3NegAngLim or J3newAng > J3PosAngLim): 
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        elif (J4newAng < J4NegAngLim or J4newAng > J4PosAngLim): 
           
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        elif (J5newAng < J5NegAngLim or J5newAng > J5PosAngLim): 
           
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        elif (J6newAng < J6NegAngLim or J6newAng > J6PosAngLim): 
            
            Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
            
        else:  
            ##J1 calc##
            if (float(J1newAng) >= float(J1AngCur)):   
                #calc pos dir output
                if (J1motdir == "0"):
                    J1drivedir = "1"
                else:
                    J1drivedir = "0"
                J1dir = J1drivedir
                J1calcAng = float(J1newAng) - float(J1AngCur)
                J1steps = int(J1calcAng / J1DegPerStep)
                if Code != 3:
                    J1StepCur = J1StepCur + J1steps #Invert       
                    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
                J1steps = str(J1steps) 
            elif (float(J1newAng) < float(J1AngCur)):
                J1dir = J1motdir
                J1calcAng = float(J1AngCur) - float(J1newAng)
                J1steps = int(J1calcAng / J1DegPerStep)
                if Code != 3:
                    J1StepCur = J1StepCur - J1steps #Invert       
                    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
                J1steps = str(J1steps) 
            ##J2 calc##
            if (float(J2newAng) >= float(J2AngCur)):   
            #calc pos dir output
                if (J2motdir == "0"):
                    J2drivedir = "1"
                else:
                    J2drivedir = "0"
                J2dir = J2drivedir
                J2calcAng = float(J2newAng) - float(J2AngCur)
                J2steps = int(J2calcAng / J2DegPerStep)
                if Code != 3:
                    J2StepCur = J2StepCur + J2steps #Invert       
                    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
                J2steps = str(J2steps) 
            elif (float(J2newAng) < float(J2AngCur)):
                J2dir = J2motdir
                J2calcAng = float(J2AngCur) - float(J2newAng)
                J2steps = int(J2calcAng / J2DegPerStep)
                if Code != 3:
                    J2StepCur = J2StepCur - J2steps #Invert       
                    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
                J2steps = str(J2steps) 
            ##J3 calc##
            if (float(J3newAng) >= float(J3AngCur)):   
            #calc pos dir output
                if (J3motdir == "0"):
                    J3drivedir = "1"
                else:
                    J3drivedir = "0"
                J3dir = J3drivedir
                J3calcAng = float(J3newAng) - float(J3AngCur)
                J3steps = int(J3calcAng / J3DegPerStep)
                if Code != 3:
                    J3StepCur = J3StepCur + J3steps #Invert       
                    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
                J3steps = str(J3steps) 
            elif (float(J3newAng) < float(J3AngCur)):
                J3dir = J3motdir
                J3calcAng = float(J3AngCur) - float(J3newAng)
                J3steps = int(J3calcAng / J3DegPerStep)
                if Code != 3:
                    J3StepCur = J3StepCur - J3steps #Invert       
                    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
                J3steps = str(J3steps) 
            ##J4 calc##
            if (float(J4newAng) >= float(J4AngCur)):   
            #calc pos dir output
                if (J4motdir == "0"):
                    J4drivedir = "1"
                else:
                    J4drivedir = "0"
                J4dir = J4drivedir
                J4calcAng = float(J4newAng) - float(J4AngCur)
                J4steps = int(J4calcAng / J4DegPerStep)
                if Code != 3:
                    J4StepCur = J4StepCur + J4steps #Invert       
                    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
                J4steps = str(J4steps) 
            elif (float(J4newAng) < float(J4AngCur)):
                J4dir = J4motdir
                J4calcAng = float(J4AngCur) - float(J4newAng)
                J4steps = int(J4calcAng / J4DegPerStep)
                if Code != 3:
                    J4StepCur = J4StepCur - J4steps #Invert       
                    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
                J4steps = str(J4steps) 
            ##J5 calc##
            if (float(J5newAng) >= float(J5AngCur)):   
            #calc pos dir output
                if (J5motdir == "0"):
                    J5drivedir = "1"
                else:
                    J5drivedir = "0"
                J5dir = J5drivedir
                J5calcAng = float(J5newAng) - float(J5AngCur)
                J5steps = int(J5calcAng / J5DegPerStep)
                if Code != 3:
                    J5StepCur = J5StepCur + J5steps #Invert       
                    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
                J5steps = str(J5steps) 
            elif (float(J5newAng) < float(J5AngCur)):
                J5dir = J5motdir
                J5calcAng = float(J5AngCur) - float(J5newAng)
                J5steps = int(J5calcAng / J5DegPerStep)
                if Code != 3:
                    J5StepCur = J5StepCur - J5steps #Invert       
                    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
                J5steps = str(J5steps) 
            ##J6 calc##
            if (float(J6newAng) >= float(J6AngCur)):   
            #calc pos dir output
                if (J6motdir == "0"):
                    J6drivedir = "1"
                else:
                    J6drivedir = "0"
                J6dir = J6drivedir
                J6calcAng = float(J6newAng) - float(J6AngCur)
                J6steps = int(J6calcAng / J6DegPerStep)
                if Code != 3:
                    J6StepCur = J6StepCur + J6steps #Invert       
                    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
                J6steps = str(J6steps) 
            elif (float(J6newAng) < float(J6AngCur)):
                J6dir = J6motdir
                J6calcAng = float(J6AngCur) - float(J6newAng)
                J6steps = int(J6calcAng / J6DegPerStep)
                if Code != 3:
                    J6StepCur = J6StepCur - J6steps #Invert       
                    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
                J6steps = str(J6steps)
            ##Track calc##
            if (TrackNew >= TrackcurPos):
                TRdir = "1"
                TRdist = TrackNew - TrackcurPos
                TRstep = str(int((TrackStepLim/TrackLength)*TRdist))
            else:
                TRdir = "0"
                TRdist = TrackcurPos - TrackNew	
                TRstep = str(int((TrackStepLim/TrackLength)*TRdist))
            TrackcurPos = TrackNew
            TrackcurEntryField.delete(0, 'end')  
            TrackcurEntryField.insert(0,str(TrackcurPos))
            commandCalc = "MJA"+J1dir+J1steps+"B"+J2dir+J2steps+"C"+J3dir+J3steps+"D"+J4dir+J4steps+"E"+J5dir+J5steps+"F"+J6dir+J6steps+"T"+TRdir+TRstep+"S"+newSpeed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
            if Code == 0:
                ser.write(commandCalc.encode())
                ser.flushInput()
                time.sleep(.01)
                #ser.read() 
                RobotCode = str(ser.readline())
                Pcode = RobotCode[2:4]
                if (Pcode == "01"):
                    applyRobotCal(RobotCode)       
            CalcFwdKin()
            DisplaySteps()
            savePosData() 
            if Code == 2 or Code == 3 :
                return(commandCalc)	

  def executeRow():
        global J1AngCur
        global J2AngCur
        global J3AngCur
        global J4AngCur
        global J5AngCur
        global J6AngCur
        global J1StepCur
        global J2StepCur
        global J3StepCur
        global J4StepCur
        global J5StepCur
        global J6StepCur
        global calStat
        global rowinproc
        global LineDist
        global Xv
        global Yv
        global Zv
        global commandCalc
        global blockEncPosCal
        selRow = tab1.progView.curselection()[0]
        tab1.progView.see(selRow+2)
        data = list(map(int, tab1.progView.curselection()))
        command=tab1.progView.get(data[0])
        cmdType=command[:6]
        ##Call Program##
        if (cmdType == "Call P"):
            tab1.lastRow = tab1.progView.curselection()[0]
            tab1.lastProg = ProgEntryField.get()
            programIndex = command.find("Program -")
            progNum = str(command[programIndex+10:])
            ProgEntryField.delete(0, 'end')
            ProgEntryField.insert(0,progNum)
            loadProg()
            time.sleep(.4) 
            index = 0
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index) 
        ##Return Program##
        if (cmdType == "Return"):
            lastRow = tab1.lastRow
            lastProg = tab1.lastProg
            ProgEntryField.delete(0, 'end')
            ProgEntryField.insert(0,lastProg)
            loadProg()
            time.sleep(.4) 
            index = 0
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(lastRow)  
        ##Servo Command##
        if (cmdType == "Servo "):
            servoIndex = command.find("number ")
            posIndex = command.find("position: ")
            servoNum = str(command[servoIndex+7:posIndex-4])
            servoPos = str(command[posIndex+10:])
            command = "SV"+servoNum+"P"+servoPos+"\n"
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            ser2.read() 
        ##If Input On Jump to Tab##
        if (cmdType == "If On "):
            inputIndex = command.find("Input-")
            tabIndex = command.find("Tab-")
            inputNum = str(command[inputIndex+6:tabIndex-9])
            tabNum = str(command[tabIndex+4:])
            command = "JFX"+inputNum+"T"+tabNum+"\n"   
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            value = ser2.readline()
            if (value == b'T'):
                index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
                index = index-1
                tab1.progView.selection_clear(0, END)
                tab1.progView.select_set(index)
        ##If Input Off Jump to Tab##
        if (cmdType == "If Off"):
            inputIndex = command.find("Input-")
            tabIndex = command.find("Tab-")
            inputNum = str(command[inputIndex+6:tabIndex-9])
            tabNum = str(command[tabIndex+4:])
            command = "JFX"+inputNum+"T"+tabNum+"\n"   
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            value = ser2.readline()
            if (value == b'F'):
                index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
                index = index-1
                tab1.progView.selection_clear(0, END)
                tab1.progView.select_set(index)
        ##Jump to Row##
        if (cmdType == "Jump T"):
            tabIndex = command.find("Tab-")
            tabNum = str(command[tabIndex+4:])
            index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
            tab1.progView.selection_clear(0, END)
            tab1.progView.select_set(index)  
        ##Set Output ON Command##
        if (cmdType == "Out On"):
            outputIndex = command.find("Out On = ")
            outputNum = str(command[outputIndex+9:])
            command = "ONX"+outputNum+"\n"
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            ser2.read() 
        ##Set Output OFF Command##
        if (cmdType == "Out Of"):
            outputIndex = command.find("Out Off = ")
            outputNum = str(command[outputIndex+10:])
            command = "OFX"+outputNum+"\n"
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            ser2.read() 
        ##Wait Input ON Command##
        if (cmdType == "Wait I"):
            inputIndex = command.find("Wait Input On = ")
            inputNum = str(command[inputIndex+16:])
            command = "WIN"+inputNum+"\n"
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            ser2.read() 
        ##Wait Input OFF Command##
        if (cmdType == "Wait O"):
            inputIndex = command.find("Wait Off Input = ")
            inputNum = str(command[inputIndex+17:])
            command = "WON"+inputNum+"\n"
            ser2.write(command.encode())
            ser2.flushInput()
            time.sleep(.2)
            ser2.read() 
        ##Wait Time Command##
        if (cmdType == "Wait T"):
            timeIndex = command.find("Wait Time = ")
            timeSeconds = str(command[timeIndex+12:])
            command = "WTS"+timeSeconds+"\n"
            ser.write(command.encode())
            ser.flushInput()
            time.sleep(.2)
            ser.read() 
        ##Set Register##  
        if (cmdType == "Regist"):
            regNumIndex = command.find("Register ")
            regEqIndex = command.find(" = ")
            regNumVal = str(command[regNumIndex+9:regEqIndex])
            regEntry = "R"+regNumVal+"EntryField"
            testOper = str(command[regEqIndex+3:regEqIndex+5])
            if (testOper == "++"):
                regCEqVal = str(command[regEqIndex+5:])
                curRegVal = eval(regEntry).get()
                regEqVal = str(int(regCEqVal)+int(curRegVal))      
            elif (testOper == "--"):
                regCEqVal = str(command[regEqIndex+5:])
                curRegVal = eval(regEntry).get()
                regEqVal = str(int(curRegVal)-int(regCEqVal))
            else:
                regEqVal = str(command[regEqIndex+3:])    
                eval(regEntry).delete(0, 'end')
                eval(regEntry).insert(0,regEqVal)
        ##Set Stor Position##  
        if (cmdType == "Store "):
            regNumIndex = command.find("Store Position ")
            regElIndex = command.find("Element")
            regEqIndex = command.find(" = ")
            regNumVal = str(command[regNumIndex+15:regElIndex-1])
            regNumEl = str(command[regElIndex+8:regEqIndex])
            regEntry = "SP_"+regNumVal+"_E"+regNumEl+"_EntryField"
            testOper = str(command[regEqIndex+3:regEqIndex+5])
            if (testOper == "++"):
                regCEqVal = str(command[regEqIndex+4:])
                curRegVal = eval(regEntry).get()
                regEqVal = str(float(regCEqVal)+float(curRegVal))      
            elif (testOper == "--"):
                regCEqVal = str(command[regEqIndex+5:])
                curRegVal = eval(regEntry).get()
                regEqVal = str(float(curRegVal)-float(regCEqVal))
            else:
                regEqVal = str(command[regEqIndex+3:])    
                eval(regEntry).delete(0, 'end')
                eval(regEntry).insert(0,regEqVal)
        ## Get Vision ##
        if (cmdType == "Get Vi"):
            testvis()	
        ##If Register Jump to Row##
        if (cmdType == "If Reg"):
            regIndex = command.find("If Register ")
            regEqIndex = command.find(" = ")
            regJmpIndex = command.find(" Jump to Tab ")    
            regNum = str(command[regIndex+12:regEqIndex])
            regEq = str(command[regEqIndex+3:regJmpIndex])
            tabNum = str(command[regJmpIndex+13:])
            regEntry = "R"+regNum+"EntryField"
            curRegVal = eval(regEntry).get()
            if (curRegVal == regEq):
                index = tab1.progView.get(0, "end").index("Tab Number " + tabNum)
                tab1.progView.selection_clear(0, END)
                tab1.progView.select_set(index)  
        ##Calibrate Command##   
        if (cmdType == "Calibr"):
            calRobotAll()
            if (calStat == 0):
                stopProg()
        ##Move J Command##  
        if (cmdType == "Move J"):  
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
        ##Offs J Command##  
        if (cmdType == "OFFS J"): 
            SPnewInex = command.find("[SP:")  
            SPendInex = command.find("] [")
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
            SP = str(command[SPnewInex+4:SPendInex])
            CXa = eval("SP_"+SP+"_E1_EntryField").get()
            CYa = eval("SP_"+SP+"_E2_EntryField").get()
            CZa = eval("SP_"+SP+"_E3_EntryField").get()
            CRxa = eval("SP_"+SP+"_E4_EntryField").get()
            CRya = eval("SP_"+SP+"_E5_EntryField").get()
            CRza = eval("SP_"+SP+"_E6_EntryField").get()
            CX = float(CXa) + float(command[J1newIndex+3:J2newIndex-1])
            CY = float(CYa) + float(command[J2newIndex+3:J3newIndex-1])
            CZ = float(CZa) + float(command[J3newIndex+3:J4newIndex-1])
            CRx = float(CRxa) + float(command[J4newIndex+3:J5newIndex-1])
            CRy = float(CRya) + float(command[J5newIndex+3:J6newIndex-1])
            CRz = float(CRza) + float(command[J6newIndex+3:TRnewIndex-1])
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
        ##Move SP Command##  
        if (cmdType == "Move S"): 
            SPnewInex = command.find("[SP:")  
            SPendInex = command.find("] [")
            TRnewIndex = command.find("T) ")	
            SpeedIndex = command.find("Speed-")
            ACCdurIndex = command.find("Ad")
            ACCspdIndex = command.find("As")
            DECdurIndex = command.find("Dd")
            DECspdIndex = command.find("Ds")
            WristConfIndex = command.find("$")
            SP = str(command[SPnewInex+4:SPendInex])
            CX = float(eval("SP_"+SP+"_E1_EntryField").get())
            CY = float(eval("SP_"+SP+"_E2_EntryField").get())
            CZ = float(eval("SP_"+SP+"_E3_EntryField").get())
            CRx = float(eval("SP_"+SP+"_E4_EntryField").get())
            CRy = float(eval("SP_"+SP+"_E5_EntryField").get())
            CRz = float(eval("SP_"+SP+"_E6_EntryField").get())
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
        ##OFFS SP Command##  
        if (cmdType == "OFFS S"): 
            SPnewInex = command.find("[SP:")  
            SPendInex = command.find("] offs")
            SP2newInex = command.find("[*SP:")  
            SP2endInex = command.find("]  [")
            TRnewIndex = command.find("T) ")	
            SpeedIndex = command.find("Speed-")
            ACCdurIndex = command.find("Ad")
            ACCspdIndex = command.find("As")
            DECdurIndex = command.find("Dd")
            DECspdIndex = command.find("Ds")
            WristConfIndex = command.find("$")
            SP = str(command[SPnewInex+4:SPendInex])
            SP2 = str(command[SP2newInex+5:SP2endInex])
            CX = float(eval("SP_"+SP+"_E1_EntryField").get()) + float(eval("SP_"+SP2+"_E1_EntryField").get())
            CY = float(eval("SP_"+SP+"_E2_EntryField").get()) + float(eval("SP_"+SP2+"_E2_EntryField").get())
            CZ = float(eval("SP_"+SP+"_E3_EntryField").get()) + float(eval("SP_"+SP2+"_E3_EntryField").get())
            CRx = float(eval("SP_"+SP+"_E4_EntryField").get()) + float(eval("SP_"+SP2+"_E4_EntryField").get())
            CRy = float(eval("SP_"+SP+"_E5_EntryField").get()) + float(eval("SP_"+SP2+"_E5_EntryField").get())
            CRz = float(eval("SP_"+SP+"_E6_EntryField").get()) + float(eval("SP_"+SP2+"_E6_EntryField").get())	
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
        ##Move L Command##  
        if (cmdType == "Move L"): 
            blockEncPosCal = 1  
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
            CalcLinDist(CX,CY,CZ)
            CalcLinVect(CX,CY,CZ)
            numWayPts = 10
            #numWayPts = int(LineDist/2)
            Xstart = XcurPos
            Ystart = YcurPos
            Zstart = ZcurPos
            Rxstart = RxcurPos
            Rystart = RycurPos
            Rzstart = RzcurPos
            
            ## SPEEDS
            #ACCpts = numWayPts * (int(ACCdur)/100)
            #ACCpctInc = 100 / int(ACCpts)
            #numDECpts = (numWayPts * (int(DECdur)/100))
            #DECpts = numWayPts - numDECpts
            #DECpctInc = 100 / int(numDECpts)
            #minACC = int(newSpeed)*(int(ACCspd)/100)
            #minDEC = int(newSpeed)*(int(DECspd)/100)
            
            lACCspd = "100"
            lDECspd = "100"
            lACCdur = "1"
            lDECdur = "1"     
            
            ##GENERATE WAYPOINTS CMD	
            WayPtsCMD = "ML"+str(numWayPts)
            ser.write(WayPtsCMD.encode())
            ser.flushInput()
            time.sleep(.01)
            for i in range(numWayPts+1):
                curWayDis = (1 / numWayPts) * i
            lCX = Xstart + (Xv * curWayDis)
            lCY = Ystart + (Yv * curWayDis)
            lCZ = Zstart + (Zv * curWayDis)
            
            #if i < ACCpts:
            #  tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
            #  if float(tempSpeed) < minACC:
            #    tempSpeed = str(round(minACC,2))
            #elif i > DECpts:
            #  tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
            #  if float(tempSpeed) < minDEC:
            #    tempSpeed = str(round(minDEC,2))
            #else:
            #  tempSpeed = newSpeed



            Code = 2
                
            MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
            ser.write(commandCalc.encode())  
            ser.flushInput()
            RobotCode = str(ser.readline())
            Pcode = RobotCode[2:4]
            if (Pcode == "01"):
                applyRobotCal(RobotCode) 
            blockEncPosCal = 0
            move.getRobotPosition()    
            
            
            
        ##Move A Command##  
        if (cmdType == "Move A"):
            subCmd=command[:10]
            if (subCmd == "Move A Mid" or subCmd == "Move A End"):
                almStatusLab.config(text="Move A must start with a Beg followed by Mid & End", bg = "red")
                almStatusLab2.config(text="Move A must start with a Beg followed by Mid & End", bg = "red")
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
            CXbeg = float(command[J1newIndex+3:J2newIndex-1])
            CYbeg = float(command[J2newIndex+3:J3newIndex-1])
            CZbeg = float(command[J3newIndex+3:J4newIndex-1])
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
            ##read next row for Mid position	
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index('end')
            for row in range (0,selRow):
                tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
            tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
            for row in range (selRow+1,last):
                tab1.progView.itemconfig(row, {'fg': 'black'})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow+2)
            data = list(map(int, tab1.progView.curselection()))
            command=tab1.progView.get(data[0])
            J1newIndex = command.find("X) ")
            J2newIndex = command.find("Y) ")
            J3newIndex = command.find("Z) ")
            CXmid = float(command[J1newIndex+3:J2newIndex-1])
            CYmid = float(command[J2newIndex+3:J3newIndex-1])
            CZmid = float(command[J3newIndex+3:J4newIndex-1])	
            ##read next row for End position	
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index('end')
            for row in range (0,selRow):
                tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
            tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
            for row in range (selRow+1,last):
                tab1.progView.itemconfig(row, {'fg': 'black'})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow+2)
            data = list(map(int, tab1.progView.curselection()))
            command=tab1.progView.get(data[0])
            J1newIndex = command.find("X) ")
            J2newIndex = command.find("Y) ")
            J3newIndex = command.find("Z) ")
            CXend = float(command[J1newIndex+3:J2newIndex-1])
            CYend = float(command[J2newIndex+3:J3newIndex-1])
            CZend = float(command[J3newIndex+3:J4newIndex-1])
            ### FIND CENTER AND RADIUS OF CIRCLE
            A = np.array([CXbeg, CYbeg, CZbeg])
            B = np.array([CXmid, CYmid, CZmid])
            C = np.array([CXend, CYend, CZend])
            a = np.linalg.norm(C - B)
            b = np.linalg.norm(C - A)
            c = np.linalg.norm(B - A)
            s = (a + b + c) / 2
            R = a*b*c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
            b1 = a*a * (b*b + c*c - a*a)
            b2 = b*b * (a*a + c*c - b*b)
            b3 = c*c * (a*a + b*b - c*c)
            P = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))
            P /= b1 + b2 + b3
            Px = P[0]
            Py = P[1]
            Pz = P[2]
            ###SHIFT POINTS TO ORIGIN
            sCXbeg = CXbeg - Px
            sCYbeg = CYbeg - Py
            sCZbeg = CZbeg - Pz
            sCXmid = CXmid - Px
            sCYmid = CYmid - Py
            sCZmid = CZmid - Pz
            sCXend = CXend - Px
            sCYend = CYend - Py
            sCZend = CZend - Pz
            ###FIND CROSS PRODUCT 
            a_vec = np.array([sCXbeg, sCYbeg, sCZbeg])/np.linalg.norm(np.array([sCXbeg, sCYbeg, sCZbeg]))
            b_vec = np.array([sCXend, sCYend, sCZend])/np.linalg.norm(np.array([sCXend, sCYend, sCZend]))
            axis = np.cross(a_vec, b_vec)
            ab_angle = np.arccos(np.dot(a_vec,b_vec))
            ab_angle_Deg = math.degrees(ab_angle)
            ###FIND ANGLE & NUM WAYPOINTS
            numWayPts = int(ab_angle_Deg / 1)
            #numWayPts = 100
            theta_Deg = (ab_angle_Deg / (numWayPts+1))
            ###DEFINE START VECTOR
            v = [sCXbeg, sCYbeg, sCZbeg]  
            ###MOVE TO BEGINING OF ARC
            Code = 0
            MoveXYZ(CXbeg,CYbeg,CZbeg,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
            
            ## SPEEDS
            #ACCpts = numWayPts * (int(ACCdur)/100)
            #ACCpctInc = 100 / int(ACCpts)
            #numDECpts = (numWayPts * (int(DECdur)/100))
            #DECpts = numWayPts - numDECpts
            #DECpctInc = 100 / int(numDECpts)
            #minACC = int(newSpeed)*(int(ACCspd)/100)
            #minDEC = int(newSpeed)*(int(DECspd)/100)
            
            lACCspd = "100"
            lDECspd = "100"
            lACCdur = "1"
            lDECdur = "1"  
            
            ##GENERATE WAYPOINTS CMD	
            WayPtsCMD = "ML"+str(numWayPts)
            ser.write(WayPtsCMD.encode())
            ser.flushInput()

            ###LOOP FIND ALL POINTS IN ARC
            cur_deg = theta_Deg
            ###START LOOP	
            for i in range(numWayPts+1):
                theta = math.radians(cur_deg) 
            new_pt = np.dot(kinematics.rotation_matrix(axis, theta), v)
            lCX = round(new_pt[0] + Px,2)
            lCY = round(new_pt[1] + Py,2)
            lCZ = round(new_pt[2] + Pz,2)  
            cur_deg += theta_Deg
            
            #if i < ACCpts:
            #  tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
            #  if float(tempSpeed) < minACC:
            #    tempSpeed = str(round(minACC,2))
            #elif i > DECpts:
            #  tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
            #  if float(tempSpeed) < minDEC:
            #    tempSpeed = str(round(minDEC,2))
            #else:
            #tempSpeed = newSpeed
                
            if i >= numWayPts:  
                Code = 3
            else:
                Code = 2
                
            MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
            ser.write(commandCalc.encode())	  
            ser.flushInput()
            time.sleep(.01)
            ser.read()
            ser.flushInput()
            ser.read()
            getRobotPosition()         
            
            
        ##Move C Command##  
        if (cmdType == "Move C"):
            blockEncPosCal = 1
            subCmd=command[:10]
            if (subCmd == "Move C Sta" or subCmd == "Move C Pla"):
                almStatusLab.config(text="Move C must start with a Center followed by Start & Plane", bg = "red")
                almStatusLab2.config(text="Move C must start with a Center followed by Start & Plane", bg = "red")
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
            CXbeg = float(command[J1newIndex+3:J2newIndex-1])
            CYbeg = float(command[J2newIndex+3:J3newIndex-1])
            CZbeg = float(command[J3newIndex+3:J4newIndex-1])
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
            ##read next row for Mid position	
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index('end')
            for row in range (0,selRow):
                tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
            tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
            for row in range (selRow+1,last):
                tab1.progView.itemconfig(row, {'fg': 'black'})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow+2)
            data = list(map(int, tab1.progView.curselection()))
            command=tab1.progView.get(data[0])
            J1newIndex = command.find("X) ")
            J2newIndex = command.find("Y) ")
            J3newIndex = command.find("Z) ")
            CXmid = float(command[J1newIndex+3:J2newIndex-1])
            CYmid = float(command[J2newIndex+3:J3newIndex-1])
            CZmid = float(command[J3newIndex+3:J4newIndex-1])	
            ##read next row for End position	
            curRow = tab1.progView.curselection()[0]
            selRow = tab1.progView.curselection()[0]
            last = tab1.progView.index('end')
            for row in range (0,selRow):
                tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
            tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
            for row in range (selRow+1,last):
                tab1.progView.itemconfig(row, {'fg': 'black'})
            tab1.progView.selection_clear(0, END)
            selRow += 1
            tab1.progView.select_set(selRow)
            curRow += 1
            selRow = tab1.progView.curselection()[0]
            tab1.progView.see(selRow+2)
            data = list(map(int, tab1.progView.curselection()))
            command=tab1.progView.get(data[0])
            J1newIndex = command.find("X) ")
            J2newIndex = command.find("Y) ")
            J3newIndex = command.find("Z) ")
            CXend = float(command[J1newIndex+3:J2newIndex-1])
            CYend = float(command[J2newIndex+3:J3newIndex-1])
            CZend = float(command[J3newIndex+3:J4newIndex-1])
            ###SHIFT POINTS TO ORIGIN
            sCXmid = CXmid - CXbeg
            sCYmid = CYmid - CYbeg
            sCZmid = CZmid - CZbeg
            sCXend = CXend - CXbeg
            sCYend = CYend - CYbeg
            sCZend = CZend - CZbeg
            ###FIND CROSS PRODUCT 
            a_vec = np.array([sCXmid, sCYmid, sCZmid])/np.linalg.norm(np.array([sCXmid, sCYmid, sCZmid]))
            b_vec = np.array([sCXend, sCYend, sCZend])/np.linalg.norm(np.array([sCXend, sCYend, sCZend]))
            axis = np.cross(a_vec, b_vec)
            ab_angle = np.arccos(np.dot(a_vec,b_vec))
            ab_angle_Deg = math.degrees(ab_angle)
            ###FIND ANGLE & NUM WAYPOINTS
            #numWayPts = 220
            numWayPts = 120
            theta_Deg = (360 / (numWayPts))
            ###DEFINE START VECTOR
            v = [sCXmid, sCYmid, sCZmid]  
            ###MOVE TO BEGINING OF ARC
            Code = 0
            MoveXYZ(CXmid,CYmid,CZmid,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
            
            #removed 9-12-19
            ## SPEEDS
            ACCpts = numWayPts * (int(ACCdur)/100)
            ACCpctInc = 100 / int(ACCpts)
            numDECpts = (numWayPts * (int(DECdur)/100))
            DECpts = numWayPts - numDECpts
            DECpctInc = 100 / int(numDECpts)
            minACC = int(newSpeed)*(int(ACCspd)/100)
            minDEC = int(newSpeed)*(int(DECspd)/100)
            
            lACCspd = "100"
            lDECspd = "100"
            lACCdur = "1"
            lDECdur = "1"  
            
            ##GENERATE WAYPOINTS CMD	
            WayPtsCMD = "MC"+str(numWayPts)
            ser.write(WayPtsCMD.encode())
            ser.flushInput()
            time.sleep(.02)
            
            ###LOOP FIND ALL POINTS IN ARC
            cur_deg = theta_Deg
            ###START LOOP
            i = 0	
            for i in range(numWayPts+1):
                theta = math.radians(cur_deg) 
            new_pt = np.dot(kinematics.rotation_matrix(axis, theta), v)
            lCX = round(new_pt[0] + CXbeg,2)
            lCY = round(new_pt[1] + CYbeg,2)
            lCZ = round(new_pt[2] + CZbeg,2)  
            cur_deg += theta_Deg
            
            #removed 9-12-19
            if i < ACCpts:
                tempSpeed = str(round(((i * (ACCpctInc/100))*int(newSpeed)),2))
                if float(tempSpeed) < minACC:
                    tempSpeed = str(round(minACC,2))
            elif i > DECpts:
                tempSpeed = str(round((((numWayPts - i) * (DECpctInc/100))*int(newSpeed)),2))
                if float(tempSpeed) < minDEC:
                    tempSpeed = str(round(minDEC,2))
            else:
                tempSpeed = newSpeed
                
            if i >= numWayPts:  
                Code = 3
            else:
                Code = 2
            
            MoveXYZ(lCX,lCY,lCZ,CRx,CRy,CRz,newSpeed,lACCdur,lACCspd,lDECdur,lDECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
            ser.write(commandCalc.encode())
            ser.flushInput()
            RobotCode = str(ser.readline())
            Pcode = RobotCode[2:4]
            if (Pcode == "01"):
                applyRobotCal(RobotCode)   
            #ser.flushInput()
            #ser.read()
            blockEncPosCal = 0
            getRobotPosition() 
            
            rowinproc = 0  	 

    def ServoCom(servo, servoPos):
        
        if servo == 0:
                command = "SV0P"+servoPos+"\n"
        elif servo == 1:
                command = "SV1P"+servoPos+"\n"
        elif servo == 2:
                command = "SV2P"+servoPos+"\n"
        elif servo == 3:
                command = "SV3P"+servoPos+"\n"
                
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(.2)
        ser2.read()


    def DO_on(output):
        outputNum = output
        command = "ONX"+outputNum+"\n"
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(.2)
        ser2.read() 


    def DO_off(output):
        outputNum = output
        command = "OFX"+outputNum+"\n"
        ser2.write(command.encode())
        ser2.flushInput()
        time.sleep(.2)
        ser2.read() 

    def jogJoint(joint):
        global JogStepsStat
        global J1StepCur
        global J2StepCur
        global J3StepCur
        global J4StepCur
        global J5StepCur
        global J6StepCur

        if joint = J1:
            
            NegAngLim = J1NegAngLim
            AngCur = global J1AngCur
            motdir = J1motdir
            stepCur = J1StepCur
            DegsPerStep = J1DegPerStep

        elif joint = J2:
            
            NegAngLim = J1NegAngLim
            AngCur = global J2AngCur
            motdir = J2motdir
            stepCur = J2StepCur
            DegsPerStep = J2DegPerStep

        elif joint = J3:
            
            NegAngLim = J2NegAngLim
            AngCur = global J2AngCur
            motdir = J2motdir
            stepCur = J2StepCur
            DegsPerStep = J2DegPerStep

        elif joint = J4:
            
            NegAngLim = J3NegAngLim
            AngCur = global J3AngCur
            motdir = J3motdir
            stepCur = J3StepCur
            DegsPerStep = J3DegPerStep

        elif joint = J5:
            
            NegAngLim = J1NegAngLim
            AngCur = global J5AngCur
            motdir = J5motdir
            stepCur = J5StepCur
            DegsPerStep = J5DegPerStep

        elif joint = J6:
            
            NegAngLim = J1NegAngLim
            AngCur = global J6AngCur
            motdir = J6motdir
            stepCur = J6StepCur
            DegsPerStep = J6DegPerStep
            



        global xboxUse
        if xboxUse != 1:
            almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
            almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
        Speed = speedEntryField.get()
        ACCdur = ACCdurField.get()
        ACCspd = ACCspeedField.get()
        DECdur = DECdurField.get()
        DECspd = DECspeedField.get()
        Degs = float(J1jogDegsEntryField.get())

        if JogStepsStat.get() == 0:
            jogSteps = int(Degs/DegPerStep)
        else:
            #switch from degs to steps
            jogSteps = Degs
            Degs = Degs*DegPerStep
        if (Degs <= -(NegAngLim - AngCur)):   
            StepCur = StepCur - int(jogSteps)
            AngCur = round(NegAngLim + (StepCur * DegPerStep),2)

            if joint==J1:
            global J1AngCur=AngCur
            elif joint=J2:
            global J2AngCur=AngCur
            elif joint==J3:
            global J3AngCur=AngCur
            elif joint==J4:
            global J4AngCur=AngCur
            elif joint==J5:
            global J5AngCur=AngCur
            elif joint==J6:
            global J6AngCur=AngCur
            
            savePosData()
            CalcFwdKin()
            command = "MJA"+motdir+str(jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
            ser.write(command.encode())    
            ser.flushInput()
            time.sleep(.2)
            #ser.read()
            RobotCode = str(ser.readline())
            Pcode = RobotCode[2:4]
            if (Pcode == "01"):
                applyRobotCal(RobotCode)         
            else:
    
                Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    
        DisplaySteps()



    
