############################################################################
## ARCS ver 1.0 ###########################################################
############################################################################
""" ARCS - Annin Robot Control Software
    Copyright (c) 2019, Chris Annin
    All rights reserved.

    You are free to share, copy and redistribute in any medium
    or format.  You are free to remix, transform and build upon
    this material.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        * Redistribution of this software in source or binary forms shall be free
          of all charges or fees to the recipient of this software.
        * Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in the
          documentation and/or other materials provided with the distribution.
        * you must give appropriate credit and indicate if changes were made. You may do
          so in any reasonable manner, but not in any way that suggests the
          licensor endorses you or your use.
		* Selling robots, robot parts, or any versions of robots or software based on this 
		  work is strictly prohibited.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
    ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL CHRIS ANNIN BE LIABLE FOR ANY
    DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
    ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
    (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    chris.annin@gmail.com
"""
##########################################################################
### VERSION DOC ##########################################################
##########################################################################
''' 

'''
##########################################################################
##########################################################################
import configparser
import serial
import time
import queue
import math
import numpy as np
import datetime

import calibration
import move
import kinematics
import xbox
import communications




global JogStepsStat
JogStepsStat = IntVar()
global J1OpenLoopStat
J1OpenLoopStat = IntVar()
global J2OpenLoopStat
J2OpenLoopStat = IntVar()
global J3OpenLoopStat
J3OpenLoopStat = IntVar()
global J4OpenLoopStat
J4OpenLoopStat = IntVar()
global J5OpenLoopStat
J5OpenLoopStat = IntVar()
global J6OpenLoopStat
J6OpenLoopStat = IntVar()


global xboxUse

###############################################################################################################################################################
### COMMUNICATION DEFS ################################################################################################################# COMMUNICATION DEFS ###
###############################################################################################################################################################







###############################################################################################################################################################  
### EXECUTION DEFS ######################################################################################################################### EXECUTION DEFS ###  
############################################################################################################################################################### 

def runProg():
  def threadProg():
    global rowinproc
    try:
      curRow = tab1.progView.curselection()[0]
      if (curRow == 0):
        curRow=1
    except:
      curRow=1
      tab1.progView.selection_clear(0, END)
      tab1.progView.select_set(curRow)
    tab1.runTrue = 1
    while tab1.runTrue == 1:
      if (tab1.runTrue == 0):
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
      else:
        runStatusLab.config(text='PROGRAM RUNNING', bg = "green")
      rowinproc = 1
      executeRow()
      time.sleep(.02)	  
      selRow = tab1.progView.curselection()[0]
      last = tab1.progView.index('end')
      #removed color row coding due to speed
      #for row in range (0,selRow):
      #  tab1.progView.itemconfig(row, {'fg': 'dodger blue'})
      #tab1.progView.itemconfig(selRow, {'fg': 'blue2'})
      #for row in range (selRow+1,last):
      #  tab1.progView.itemconfig(row, {'fg': 'black'})
      tab1.progView.selection_clear(0, END)
      selRow += 1
      tab1.progView.select_set(selRow)
      curRow += 1
      try:
        selRow = tab1.progView.curselection()[0]
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,selRow)
      except:
        curRowEntryField.delete(0, 'end')
        curRowEntryField.insert(0,"---") 
        tab1.runTrue = 0
        runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  t = threading.Thread(target=threadProg)
  t.start()
  
def stepFwd():
    executeRow() 
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
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")
 
def stepRev():
    executeRow()  
    selRow = tab1.progView.curselection()[0]
    last = tab1.progView.index('end')
    for row in range (0,selRow):
      tab1.progView.itemconfig(row, {'fg': 'black'})
    tab1.progView.itemconfig(selRow, {'fg': 'red'})
    for row in range (selRow+1,last):
      tab1.progView.itemconfig(row, {'fg': 'tomato2'})
    tab1.progView.selection_clear(0, END)
    selRow -= 1
    tab1.progView.select_set(selRow)
    time.sleep(.2)
    try:
      selRow = tab1.progView.curselection()[0]
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,selRow)
    except:
      curRowEntryField.delete(0, 'end')
      curRowEntryField.insert(0,"---")  
    
def stopProg():
  lastProg = ""
  tab1.runTrue = 0 
  if (tab1.runTrue == 0):
    runStatusLab.config(text='PROGRAM STOPPED', bg = "red")
  else:
    runStatusLab.config(text='PROGRAM RUNNING', bg = "green")  
  

  
##############################################################################################################################################################
### BUTTON JOGGING DEFS ############################################################################################################## BUTTON JOGGING DEFS ###
##############################################################################################################################################################  
 





  
def ChgDis(val):
  curSpd = int(J1jogDegsEntryField.get())
  if curSpd >=100 and val == 0:
    curSpd = 100 
  elif curSpd < 5 and val == 0:  
    curSpd += 1
  elif val == 0:
    curSpd += 5   
  if curSpd <=1 and val == 1:
    curSpd = 1 
  elif curSpd <= 5 and val == 1:  
    curSpd -= 1
  elif val == 1:
    curSpd -= 5
  elif val == 2:
    curSpd = 5  
  J1jogDegsEntryField.delete(0, 'end')
  J2jogDegsEntryField.delete(0, 'end')
  J3jogDegsEntryField.delete(0, 'end')
  J4jogDegsEntryField.delete(0, 'end')
  J5jogDegsEntryField.delete(0, 'end')
  J6jogDegsEntryField.delete(0, 'end')
  XjogEntryField.delete(0, 'end')
  YjogEntryField.delete(0, 'end')
  ZjogEntryField.delete(0, 'end')
  RxjogEntryField.delete(0, 'end')
  RyjogEntryField.delete(0, 'end')
  RzjogEntryField.delete(0, 'end')
  TXjogEntryField.delete(0, 'end')
  TYjogEntryField.delete(0, 'end')
  TZjogEntryField.delete(0, 'end')
  TRxjogEntryField.delete(0, 'end')
  TRyjogEntryField.delete(0, 'end')
  TRzjogEntryField.delete(0, 'end')
  J1jogDegsEntryField.insert(0,str(curSpd))
  J2jogDegsEntryField.insert(0,str(curSpd))
  J3jogDegsEntryField.insert(0,str(curSpd))
  J4jogDegsEntryField.insert(0,str(curSpd))
  J5jogDegsEntryField.insert(0,str(curSpd))
  J6jogDegsEntryField.insert(0,str(curSpd))
  XjogEntryField.insert(0,str(curSpd))
  YjogEntryField.insert(0,str(curSpd))
  ZjogEntryField.insert(0,str(curSpd))
  RxjogEntryField.insert(0,str(curSpd))
  RyjogEntryField.insert(0,str(curSpd))
  RzjogEntryField.insert(0,str(curSpd))
  TXjogEntryField.insert(0,str(curSpd))
  TYjogEntryField.insert(0,str(curSpd))
  TZjogEntryField.insert(0,str(curSpd))
  TRxjogEntryField.insert(0,str(curSpd))
  TRyjogEntryField.insert(0,str(curSpd))
  TRzjogEntryField.insert(0,str(curSpd))
  time.sleep(.3)  


def ChgSpd(val):
  curSpd = int(speedEntryField.get())
  if curSpd >=100 and val == 0:
    curSpd = 100 
  elif curSpd < 5 and val == 0:  
    curSpd += 1
  elif val == 0:
    curSpd += 5   
  if curSpd <=1 and val == 1:
    curSpd = 1 
  elif curSpd <= 5 and val == 1:  
    curSpd -= 1
  elif val == 1:
    curSpd -= 5
  elif val == 2:
    curSpd = 5  
  speedEntryField.delete(0, 'end')    
  speedEntryField.insert(0,str(curSpd))  
 
def jogFunction(joint,direction):
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur

  if joint == J1:
    
    NegAngLim = J1NegAngLim
    AngCur = J1AngCur
    motdir = J1motdir
    stepCur = J1StepCur
    DegsPerStep = J1DegPerStep

  elif joint == J2:
    
    NegAngLim = J1NegAngLim
    AngCur = J2AngCur
    motdir = J2motdir
    stepCur = J2StepCur
    DegsPerStep = J2DegPerStep

  elif joint == J3:
    
    NegAngLim = J2NegAngLim
    AngCur = J2AngCur
    motdir = J2motdir
    stepCur = J2StepCur
    DegsPerStep = J2DegPerStep

  elif joint == J4:
    
    NegAngLim = J3NegAngLim
    AngCur = J3AngCur
    motdir = J3motdir
    stepCur = J3StepCur
    DegsPerStep = J3DegPerStep

  elif joint == J5:
    
    NegAngLim = J1NegAngLim
    AngCur = J5AngCur
    motdir = J5motdir
    stepCur = J5StepCur
    DegsPerStep = J5DegPerStep

  elif joint == J6:
    
    NegAngLim = J1NegAngLim
    AngCur = J6AngCur
    motdir = J6motdir
    stepCur = J6StepCur
    DegsPerStep = J6DegPerStep
    



  global xboxUse
  if xboxUse != 1:
    
  Speed = robot_speed
  ACCdur = accel_Duration
  ACCspd = accel_Speed
  DECdur = decel_Duration
  DECspd = decel_Speed
  Degs = float(Ui.jog_incremet_slider.value)
  if JogStepsStat.get() == 0:
    jogSteps = int(Degs/DegPerStep)
  else:
    #switch from degs to steps
    jogSteps = Degs
    Degs = Degs*DegPerStep
  if direction == 0 (Degs <= -(NegAngLim - AngCur)): 
    
    StepCur = StepCur - int(jogSteps)
    AngCur = round(NegAngLim + (StepCur * DegPerStep),2)

    if joint==J1:
        J1AngCur=AngCur
    elif joint==J2:
        J2AngCur=AngCur
    elif joint==J3:
        J3AngCur=AngCur
    elif joint==J4:
        J4AngCur=AngCur
    elif joint==J5:
        J5AngCur=AngCur
    elif joint==J6:
        J6AngCur=AngCur
    
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


  elif direction == 1 and (J1Degs <= (J1PosAngLim - J1AngCur)):
    J1StepCur = J1StepCur + int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJA"+J1drivedir+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
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
    

def J1jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J1AngCur
  global xboxUse
  if xboxUse != 1:
    pass
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1Degs = float(J1jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J1jogSteps = int(J1Degs/J1DegPerStep)
  else:
    #switch from degs to steps
    J1jogSteps = J1Degs
    J1Degs = J1Degs*J1DegPerStep
  #calc pos dir output
  if (J1motdir == "0"):
    J1drivedir = "1"
  else:
    J1drivedir = "0"	
  if (J1Degs <= (J1PosAngLim - J1AngCur)):   
    J1StepCur = J1StepCur + int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJA"+J1drivedir+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode)  
  else:
    almStatusLab.config(text="J1 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J1 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J1 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J2jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J2AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    #switch from degs to steps
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  if (J2Degs <= -(J2NegAngLim - J2AngCur)):  
    J2StepCur = J2StepCur - int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJB"+J2motdir+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J2 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J2 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J2jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J2AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J2Degs = float(J2jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J2jogSteps = int(J2Degs/J2DegPerStep)
  else:
    #switch from degs to steps
    J2jogSteps = J2Degs
    J2Degs = J2Degs*J2DegPerStep
  #calc pos dir output
  if (J2motdir == "0"):
    J2drivedir = "1"
  else:
    J2drivedir = "0"	
  if (J2Degs <= (J2PosAngLim - J2AngCur)):  
    J2StepCur = J2StepCur + int(J2jogSteps)
    J2AngCur = round(J2NegAngLim + (J2StepCur * J2DegPerStep),2)
    J2curAngEntryField.delete(0, 'end')
    J2curAngEntryField.insert(0,str(J2AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJB"+J2drivedir+str(J2jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J2 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J2 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J2 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()
   
def J3jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J3AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    #switch from degs to steps
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  if (J3Degs <= -(J3NegAngLim - J3AngCur)): 
    J3StepCur = J3StepCur - int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJC"+J3motdir+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J3 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J3 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J3jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J3AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J3Degs = float(J3jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J3jogSteps = int(J3Degs/J3DegPerStep)
  else:
    #switch from degs to steps
    J3jogSteps = J3Degs
    J3Degs = J3Degs*J3DegPerStep
  #calc pos dir output
  if (J3motdir == "0"):
    J3drivedir = "1"
  else:
    J3drivedir = "0"	
  if (J3Degs <= (J3PosAngLim - J3AngCur)):  
    J3StepCur = J3StepCur + int(J3jogSteps)
    J3AngCur = round(J3NegAngLim + (J3StepCur * J3DegPerStep),2)
    J3curAngEntryField.delete(0, 'end')
    J3curAngEntryField.insert(0,str(J3AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJC"+J3drivedir+str(J3jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J3 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J3 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J3 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J4jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J4AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:
    #switch from degs to steps
    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  if (J4Degs <= -(J4NegAngLim - J4AngCur)):  
    J4StepCur = J4StepCur - int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJD"+J4motdir+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J4 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J4 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J4jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J4AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J4Degs = float(J4jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J4jogSteps = int(J4Degs/J4DegPerStep)
  else:
    #switch from degs to steps
    J4jogSteps = J4Degs
    J4Degs = J4Degs*J4DegPerStep
  #calc pos dir output
  if (J4motdir == "0"):
    J4drivedir = "1"
  else:
    J4drivedir = "0"	
  if (J4Degs <= (J4PosAngLim - J4AngCur)):  
    J4StepCur = J4StepCur + int(J4jogSteps)
    J4AngCur = round(J4NegAngLim + (J4StepCur * J4DegPerStep),2)
    J4curAngEntryField.delete(0, 'end')
    J4curAngEntryField.insert(0,str(J4AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJD"+J4drivedir+str(J4jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J4 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J4 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J4 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()  
   
def J5jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J5AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    #switch from degs to steps
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  if (J5Degs <= -(J5NegAngLim - J5AngCur)):  
    J5StepCur = J5StepCur - int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJE"+J5motdir+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J5 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J5 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J5jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J5AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J5Degs = float(J5jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J5jogSteps = int(J5Degs/J5DegPerStep)
  else:
    #switch from degs to steps
    J5jogSteps = J5Degs
    J5Degs = J5Degs*J5DegPerStep
  #calc pos dir output
  if (J5motdir == "0"):
    J5drivedir = "1"
  else:
    J5drivedir = "0"	
  if (J5Degs <= (J5PosAngLim - J5AngCur)):  
    J5StepCur = J5StepCur + int(J5jogSteps)
    J5AngCur = round(J5NegAngLim + (J5StepCur * J5DegPerStep),2)
    J5curAngEntryField.delete(0, 'end')
    J5curAngEntryField.insert(0,str(J5AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJE"+J5drivedir+str(J5jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J5 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J5 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J5 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()
   
def J6jogNeg():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J6AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    #switch from degs to steps
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  if (J6Degs <= -(J6NegAngLim - J6AngCur)):  
    J6StepCur = J6StepCur - int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJF"+J6motdir+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J6 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J6 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def J6jogPos():
  global JogStepsStat
  global J1StepCur
  global J2StepCur
  global J3StepCur
  global J4StepCur
  global J5StepCur
  global J6StepCur
  global J6AngCur
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J6Degs = float(J6jogDegsEntryField.get())
  if JogStepsStat.get() == 0:
    J6jogSteps = int(J6Degs/J6DegPerStep)
  else:
    #switch from degs to steps
    J6jogSteps = J6Degs
    J6Degs = J6Degs*J6DegPerStep
  #calc pos dir output
  if (J6motdir == "0"):
    J6drivedir = "1"
  else:
    J6drivedir = "0"	
  if (J6Degs <= (J6PosAngLim - J6AngCur)): 
    J6StepCur = J6StepCur + int(J6jogSteps)
    J6AngCur = round(J6NegAngLim + (J6StepCur * J6DegPerStep),2)
    J6curAngEntryField.delete(0, 'end')
    J6curAngEntryField.insert(0,str(J6AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJF"+J6drivedir+str(J6jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
    ser.write(command.encode())	
    ser.flushInput()
    time.sleep(.2)
    #ser.read()
    RobotCode = str(ser.readline())
    Pcode = RobotCode[2:4]
    if (Pcode == "01"):
      applyRobotCal(RobotCode) 
  else:
    almStatusLab.config(text="J6 AXIS LIMIT", bg = "red")
    almStatusLab2.config(text="J6 AXIS LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"J6 AXIS LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))
  DisplaySteps()

def XjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos - float(XjogEntryField.get())
  CY = YcurPos 
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def YjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos - float(YjogEntryField.get())
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def ZjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos - float(ZjogEntryField.get())
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RxjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos - float(RxjogEntryField.get())
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RyjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos - float(RyjogEntryField.get())
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RzjogNeg():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos - float(RzjogEntryField.get())
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def XjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos + float(XjogEntryField.get())
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def YjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos + float(YjogEntryField.get())
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def ZjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos + float(ZjogEntryField.get())
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RxjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos + float(RxjogEntryField.get())
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RyjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos + float(RyjogEntryField.get())
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def RzjogPos():
  global xboxUse
  if xboxUse != 1:
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos + float(RzjogEntryField.get())
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0  
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TrackjogNeg():
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  if xboxUse != 1:  
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CT = float(TrackjogEntryField.get())
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  if JogStepsStat.get() == 1:
    TrackSteps = TrackjogEntryField.get()
  else:
    TrackSteps = str(int((TrackStepLim/TrackLength)*CT))
  if (TrackcurPos - (float(TrackSteps) * (TrackLength/TrackStepLim)) >= 0):
    command = "MJT0"+TrackSteps+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()  	
    TrackcurPos = TrackcurPos - (float(TrackSteps) * (TrackLength/TrackStepLim))
    TrackcurEntryField.delete(0, 'end')  
    TrackcurEntryField.insert(0,str(TrackcurPos))
    savePosData()
  else:
    almStatusLab.config(text="TRACK NEG TRAVEL LIMIT", bg = "red")
    almStatusLab2.config(text="TRACK NEG TRAVEL LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"TRACK NEG TRAVEL LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))

def TrackjogPos():
  global TrackcurPos
  global TrackLength
  global TrackStepLim
  if xboxUse != 1:  
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CT = float(TrackjogEntryField.get())
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  if JogStepsStat.get() == 1:
    TrackSteps = TrackjogEntryField.get()
  else:
    TrackSteps = str(int((TrackStepLim/TrackLength)*CT))
  if (TrackcurPos + (float(TrackSteps) * (TrackLength/TrackStepLim)) <= TrackLength):
    command = "MJT1"+TrackSteps+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"\n"
    ser.write(command.encode())    
    ser.flushInput()
    time.sleep(.2)
    ser.read()
    TrackcurPos = TrackcurPos + (float(TrackSteps) * (TrackLength/TrackStepLim))
    TrackcurEntryField.delete(0, 'end')  
    TrackcurEntryField.insert(0,str(TrackcurPos))
    savePosData()
  else:
    almStatusLab.config(text="TRACK POS TRAVEL LIMIT", bg = "red")
    almStatusLab2.config(text="TRACK POS TRAVEL LIMIT", bg = "red")
    Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
    tab6.ElogView.insert(END, Curtime+" - "+"TRACK POS TRAVEL LIMIT")
    value=tab6.ElogView.get(0,END)
    pickle.dump(value,open("ErrorLog","wb"))    
  
def cartesianJogNeg(point1, point2):
  
  CX = XcurPos
  CY = YcurPos 
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = o
  Code = 0  
  if point1 == T and point2 == X:
    TCX = 0 - float(TXjogEntryField.get())
    Track = float(TrackcurEntryField.get())

  elif point1 == T and point2 == Y:
    TCY = 0 - float(TYjogEntryField.get()) 
    Track = float(TrackcurEntryField.get())

  elif point1 == T and point2 == Z:
    TCRx = 0 - float(TYjogEntryField.get()) 
    Track = float(TrackcurEntryField.get())

  elif point1 == T and point2 == Y:
    TCY = 0 - float(TYjogEntryField.get()) 
    Track = float(TrackcurEntryField.get())

  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)



def TRxjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0 - float(TRxjogEntryField.get())
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRyjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0 - float(TRyjogEntryField.get())
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRzjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 - float(TRzjogEntryField.get())
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TXjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0 + float(TXjogEntryField.get())
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TYjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 + float(TYjogEntryField.get()) 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TZjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0 + float(TZjogEntryField.get())
  TCRx = 0
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRxjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0 + float(TRxjogEntryField.get())
  TCRy = 0
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRyjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0 + float(TRyjogEntryField.get())
  TCRz = 0
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)

def TRzjogPos():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 
  TCZ = 0
  TCRx = 0
  TCRy = 0
  TCRz = 0 + float(TRzjogEntryField.get())
  Track = float(TrackcurEntryField.get())
  Code = 0
  newSpeed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()  
  MoveXYZ(CX,CY,CZ,CRx,CRy,CRz,newSpeed,ACCdur,ACCspd,DECdur,DECspd,WC,TCX,TCY,TCZ,TCRx,TCRy,TCRz,Track,Code)
  
  
##############################################################################################################################################################  
### TEACH DEFS ################################################################################################################################ TEACH DEFS ###
##############################################################################################################################################################  

def teachInsertBelSelected():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  movetype = options.get()
  if(movetype == "OFFS J"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move SP"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
    newPos = movetype + " [*]  T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "OFFS SP"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"] offs [*SP:"+str(int(SavePosEntryField.get())+1)+"] "
    newPos = movetype + " [*]  T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move J"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move L"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move A Beg"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move A Mid"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite                 
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move A End"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move C Center"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Move C Start"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite                 
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))	
  elif(movetype == "Move C Plane"):
    newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite
    tab1.progView.insert(selRow, newPos) 
    tab1.progView.selection_clear(0, END)
    tab1.progView.select_set(selRow)
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))
  elif(movetype == "Teach SP"):
    SP = str(SavePosEntryField.get())
    SPE6 = "Store Position "+SP+" Element 6 = "+str(round(RzcurPos,3))         
    tab1.progView.insert(selRow, SPE6)	
    SPE5 = "Store Position "+SP+" Element 5 = "+str(round(RycurPos,3))            
    tab1.progView.insert(selRow, SPE5)
    SPE4 = "Store Position "+SP+" Element 4 = "+str(round(RxcurPos,3))           
    tab1.progView.insert(selRow, SPE4)	
    SPE3 = "Store Position "+SP+" Element 3 = "+str(round(ZcurPos,3))        
    tab1.progView.insert(selRow, SPE3)	
    SPE2 = "Store Position "+SP+" Element 2 = "+str(round(YcurPos,3))            
    tab1.progView.insert(selRow, SPE2)	
    SPE1 = "Store Position "+SP+" Element 1 = "+str(round(XcurPos,3))         
    tab1.progView.insert(selRow, SPE1)   	
    value=tab1.progView.get(0,END)
    pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachReplaceSelected():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos  
  selRow = tab1.progView.curselection()[0]
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  movetype = options.get()
  if(movetype[:-2]== "OFFS"):
    movetype = movetype+" [SP:"+str(SavePosEntryField.get())+"]"
  newPos = movetype + " [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
  tab1.progView.insert(selRow, newPos)
  selection = tab1.progView.curselection()
  tab1.progView.delete(selection[0]) 
  tab1.progView.select_set(selRow)
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def teachFineCal():
  global XcurPos
  global YcurPos
  global ZcurPos
  global RxcurPos
  global RycurPos
  global RzcurPos
  global WC
  global TrackcurPos
  Speed = speedEntryField.get()
  ACCdur = ACCdurField.get()
  ACCspd = ACCspeedField.get()
  DECdur = DECdurField.get()
  DECspd = DECspeedField.get()
  J1AngWrite = str(round(XcurPos,3))
  J2AngWrite = str(round(YcurPos,3))
  J3AngWrite = str(round(ZcurPos,3))
  J4AngWrite = str(round(RxcurPos,3))
  J5AngWrite = str(round(RycurPos,3))
  J6AngWrite = str(round(RzcurPos,3))
  TrackPosWrite = str(round(TrackcurPos,3))
  newPos = "Move J [*]  X) "+J1AngWrite+"   Y) "+J2AngWrite+"   Z) "+J3AngWrite+"   W) "+J4AngWrite+"   P) "+J5AngWrite+"   R) "+J6AngWrite+"   T) "+TrackPosWrite+"   Speed-"+Speed+" Ad "+ACCdur+" As "+ACCspd+" Dd "+DECdur+" Ds "+DECspd+ " $"+WC              
  fineCalEntryField.delete(0, 'end')   
  fineCalEntryField.insert(0,str(newPos))
  savePosData()
  almStatusLab.config(text="NEW FINE CALIBRATION POSITION TAUGHT", bg = "blue")
  almStatusLab2.config(text="NEW FINE CALIBRATION POSITION TAUGHT", bg = "blue")
  Curtime = datetime.datetime.now().strftime("%B %d %Y - %I:%M%p")
  tab6.ElogView.insert(END, Curtime+" - "+"NEW FINE CALIBRATION POSITION TAUGHT")
  value=tab6.ElogView.get(0,END)
  pickle.dump(value,open("ErrorLog","wb"))
 

############################################################################################################################################################## 
### PROGRAM FUNCTION DEFS ########################################################################################################## PROGRAM FUNCTION DEFS ###
############################################################################################################################################################## 
  
def deleteitem():
  selRow = tab1.progView.curselection()[0]
  selection = tab1.progView.curselection()  
  tab1.progView.delete(selection[0])
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))  
  
def manInsItem():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow) 
  tab1.progView.insert(selRow, manEntryField.get())
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow) 
  selRow = tab1.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)
  tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def manReplItem():
  #selRow = curRowEntryField.get()
  selRow = tab1.progView.curselection()[0]
  tab1.progView.delete(selRow) 
  tab1.progView.insert(selRow, manEntryField.get())
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  tab1.progView.itemconfig(selRow, {'fg': 'darkgreen'})  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def waitTime():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  seconds = waitTimeEntryField.get()
  newTime = "Wait Time = "+seconds               
  tab1.progView.insert(selRow, newTime)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))


def waitInputOn():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  input = waitInputEntryField.get()
  newInput = "Wait Input On = "+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def waitInputOff():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  input = waitInputOffEntryField.get()
  newInput = "Wait Off Input = "+input              
  tab1.progView.insert(selRow, newInput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOn():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  output = outputOnEntryField.get()
  newOutput = "Out On = "+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def setOutputOff():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  output = outputOffEntryField.get()
  newOutput = "Out Off = "+output              
  tab1.progView.insert(selRow, newOutput)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def tabNumber():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  tabNum = tabNumEntryField.get()
  tabins = "Tab Number "+tabNum              
  tab1.progView.insert(selRow, tabins) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def jumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  tabNum = jumpTabEntryField.get()
  tabjmp = "Jump Tab-"+tabNum              
  tab1.progView.insert(selRow, tabjmp) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
 
def getvision():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  value = "Get Vision"
  tab1.progView.insert(selRow, value) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END)
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  
def IfOnjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  inpNum = IfOnjumpInputTabEntryField.get()
  tabNum = IfOnjumpNumberTabEntryField.get()
  tabjmp = "If On Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  tab1.progView.insert(selRow, tabjmp)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def IfOffjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  inpNum = IfOffjumpInputTabEntryField.get()
  tabNum = IfOffjumpNumberTabEntryField.get()
  tabjmp = "If Off Jump - Input-"+inpNum+" Jump to Tab-"+tabNum             
  tab1.progView.insert(selRow, tabjmp) 
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def Servo():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  servoNum = servoNumEntryField.get()
  servoPos = servoPosEntryField.get()
  servoins = "Servo number "+servoNum+" to position: "+servoPos              
  tab1.progView.insert(selRow, servoins)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow) 
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def loadProg():
  progframe=Frame(tab1)
  progframe.place(x=7,y=174)
  #progframe.pack(side=RIGHT, fill=Y)
  scrollbar = Scrollbar(progframe) 
  scrollbar.pack(side=RIGHT, fill=Y)
  tab1.progView = Listbox(progframe,width=84,height=31, yscrollcommand=scrollbar.set)
  tab1.progView.bind('<<ListboxSelect>>', progViewselect)
  try:
    Prog = pickle.load(open(ProgEntryField.get(),"rb"))
  except:
    try:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open(ProgEntryField.get(),"wb"))    
    except:
      Prog = ['##BEGINNING OF PROGRAM##','Tab Number 1']
      pickle.dump(Prog,open("new","wb"))
      ProgEntryField.insert(0,"new")
  time.sleep(.2)
  for item in Prog:
    tab1.progView.insert(END,item) 
  tab1.progView.pack()
  scrollbar.config(command=tab1.progView.yview)
  savePosData()

def insertCallProg():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  newProg = changeProgEntryField.get()
  changeProg = "Call Program - "+newProg            
  tab1.progView.insert(selRow, changeProg)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def insertReturn():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  value = "Return"           
  tab1.progView.insert(selRow, value)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)  
  value=tab1.progView.get(0,END)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))

def IfRegjumpTab():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = regNumJmpEntryField.get()
  regEqNum = regEqJmpEntryField.get()
  tabNum = regTabJmpEntryField.get()
  tabjmp = "If Register "+regNum+" = "+regEqNum+" Jump to Tab "+ tabNum            
  tab1.progView.insert(selRow, tabjmp)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def insertRegister():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = regNumEntryField.get()
  regCmd = regEqEntryField.get()
  regIns = "Register "+regNum+" = "+regCmd             
  tab1.progView.insert(selRow, regIns)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
  
def storPos():
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  regNum = storPosNumEntryField.get()
  regElmnt = storPosElEntryField.get()
  regCmd = storPosValEntryField.get()
  regIns = "Store Position "+regNum+" Element "+regElmnt+" = "+regCmd             
  tab1.progView.insert(selRow, regIns)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')
  
def insCalibrate():  
  try:
    selRow = tab1.progView.curselection()[0]
    selRow += 1
  except:
    last = tab1.progView.index('end')
    selRow = last
    tab1.progView.select_set(selRow)
  insCal = "Calibrate Robot"          
  tab1.progView.insert(selRow, insCal)   
  value=tab1.progView.get(0,END)
  tab1.progView.selection_clear(0, END) 
  tab1.progView.select_set(selRow)
  pickle.dump(value,open(ProgEntryField.get(),"wb"))
  tabNumEntryField.delete(0, 'end')

def progViewselect(e):
  selRow = tab1.progView.curselection()[0]
  curRowEntryField.delete(0, 'end')
  curRowEntryField.insert(0,selRow)
  

def getSel():
  selRow = tab1.progView.curselection()[0]
  tab1.progView.see(selRow+2)
  data = list(map(int, tab1.progView.curselection()))
  command=tab1.progView.get(data[0])
  manEntryField.delete(0, 'end')
  manEntryField.insert(0, command)  
  

  
def TestString():
  message = testSendEntryField.get()
  command = "TM"+message+"\n"
  ser2.write(command.encode())
  ser2.flushInput()
  time.sleep(0)
  echo = ser2.readline()
  testRecEntryField.delete(0, 'end')
  testRecEntryField.insert(0,echo)  

def ClearTestString():
  testRecEntryField.delete(0, 'end')
  
def CalcLinDist(X2,Y2,Z2):
  global XcurPos
  global YcurPos
  global ZcurPos
  global LineDist
  X1 = XcurPos
  Y1 = YcurPos
  Z1 = ZcurPos
  LineDist = (((X2-X1)**2)+((Y2-Y1)**2)+((Z2-Z1)**2))**.5
  return (LineDist)

def CalcLinVect(X2,Y2,Z2):
  global XcurPos
  global YcurPos
  global ZcurPos
  global Xv
  global Yv
  global Zv
  X1 = XcurPos
  Y1 = YcurPos
  Z1 = ZcurPos
  Xv = X2-X1
  Yv = Y2-Y1
  Zv = Z2-Z1
  return (Xv,Yv,Zv)  

def CalcLinWayPt(CX,CY,CZ,curWayPt,):
  global XcurPos
  global YcurPos
  global ZcurPos

 

##############################################################################################################################################################
### KINEMATIC DEFS ######################################################################################################################## KINEMATIC DEFS ###
##############################################################################################################################################################


  
  
##############################################################################################################################################################  
### MOVE DEFS ################################################################################################################################## MOVE DEFS ###  
##############################################################################################################################################################  
  

	
	
##############################################################################################################################################################	
### CALIBRATION & SAVE DEFS ###################################################################################################### CALIBRATION & SAVE DEFS ###
##############################################################################################################################################################	


	
	

###VISION DEFS###################################################################
#################################################################################	
 

 
  




##############################################################################################################################################################
### OPEN CAL FILE AND LOAD LIST ##############################################################################################################################
##############################################################################################################################################################

def openCalFile(filepath):
  global J1StepCur  
  global JJ1AngCur   
  global JJ2StepCur  
  global JJ2AngCur   
  global JJ3StepCur  
  global JJ3AngCur   
  global J4StepCur  
  global  J4AngCur   
  global JJ5StepCur  
  global JJ5AngCur   
  global JJ6StepCur  
  global JJ6AngCur   
  global JcomPort     
  global Jcom2Port   
  global JProg       
  global JServo0on   
  global JServo0off  
  global JServo1on   
  global JServo1off  
  global JDO1on      
  global JDO1off     
  global JDO2on      
  global JDO2off     
  global JUFx        
  global JUFy        
  global JUFz        
  global JUFrx       
  global JUFry       
  global JUFrz       
  global JTFx        
  global JTFy        
  global JTFz        
  global JTFrx       
  global JTFry       
  global JTFrz       
  global JFineCalPos 

  global JJ1NegAngLim
  global JJ1PosAngLim 
  global JJ1StepLim  
  global JJ2NegAngLim 
  global JJ2PosAngLim 
  global JJ2StepLim   
  global JJ3NegAngLim 
  global J J3PosAngLim 
  global JJ3StepLim   
  global JJ4NegAngLim 
  global JJ4PosAngLim 
  global JJ4StepLim   
  global JJ5NegAngLim 
  global JJ5PosAngLim 
  global JJ5StepLim   
  global JJ6NegAngLim 
  global JJ6PosAngLim 
  global JJ5StepLim   

  global  DHa1        
  global  DHa2        
  global DHa3        
  global DHa4        
  global DHa5        
  global DHa6        
  global DHr1       
  global DHr2        
  global DHr3       
  global DHr4        
  global DHr5        
  global DHr6        
  global DHd1        
  global DHd2        
  global  DHd3        
  global  DHd4       
  global  DHd5        
  global  DHd6        
  global  DHt1       
  global  DHt2        
  global  DHt3        
  global  DHt4        
  global  DHt5        
  global  DHt6        


  global  CalDir     
  global MotDir     
  global  TrackcurPos 
  global TrackLength 
  global TrackStepLim
  global VisFileLoc  
  global VisProg  
  global  VisOrigXpix
  global  VisOrigXmm  
  global VisOrigYpix
  global  VisOrigYmm
  global  VisEndXpix 
  global  VisEndXmm  
  global  VisEndYpix  
  global  VisEndYmm   

  config = configparser.ConfigParser()
  config.read(filepath)

  try:
        with open('config.ini') as f:
           config.read(f)
  except IOError:
        config.add_section('General')
        config.add_section('DH parameters')
        config.add_section('Limits')
        config.add_section('Track')
        config.add_section('Visual')
        with open('config.ini', 'w') as configfile:
          config.write(configfile)
 
  J1StepCur   =config['']['']
  J1AngCur    =config['']['']
  J2StepCur   =config['']['']
  J2AngCur    =config['']['']
  J3StepCur   =config['']['']
  J3AngCur    =config['']['']
  J4StepCur   =config['']['']
  J4AngCur    =config['']['']
  J5StepCur   =config['']['']
  J5AngCur    =config['']['']
  J6StepCur   =config['']['']
  J6AngCur    =config['']['']
  comPort     =config['General']['comPort1']
  com2Port    =config['General']['comPort2']
  buadRate    =config['General']['baudrate']
  Prog        =config['']['']
  Servo0on    =config['']['']
  Servo0off   =config['']['']
  Servo1on    =config['']['']
  Servo1off   =config['']['']
  DO1on       =config['']['']
  DO1off      =config['']['']
  DO2on       =config['']['']
  DO2off      =config['']['']
  UFx         =config['world_frame']['x']
  UFy         =config['world_frame']['y']
  UFz         =config['world_frame']['z']
  UFrx        =config['world_frame']['rx']
  UFry        =config['world_frame']['ry']
  UFrz        =config['world_frame']['rz']
  TFx         =config['tool_frame']['x']
  TFy         =config['tool_frame']['y']
  TFz         =config['tool_frame']['z']
  TFrx        =config['tool_frame']['rx']
  TFry        =config['tool_frame']['ry']
  TFrz        =config['tool_frame']['rz']
  FineCalPos  =config['']['']

  J1NegAngLim =float(config['Limits']['J1_Neg_Angle_Limit'])
  J1PosAngLim =float(config['Limits']['J1_Pos_Angle_Limit'])
  J1StepLim   =float(config['Limits']['J1_Step_limit'])
  J2NegAngLim =float(config['Limits']['J2_Neg_Angle_limit'])
  J2PosAngLim =float(config['Limits']['J2_Pos_Angle_limit'])
  J2StepLim   =float(config['Limits']['J2_Step_limit'])
  J3NegAngLim =float(config['Limits']['J3_Neg_Angle_limit'])
  J3PosAngLim =float(config['Limits']['J3_Pos_Angle_limit'])
  J3StepLim   =float(config['Limits']['J3_Step_limit'])
  J4NegAngLim =float(config['Limits']['J4_Neg_Angle_limit'])
  J4PosAngLim =float(config['Limits']['J4_Pos_Angle_limit'])
  J4StepLim   =float(config['Limits']['J4_Step_limit'])
  J5NegAngLim =float(config['Limits']['J5_Neg_Angle_limit'])
  J5PosAngLim =float(config['Limits']['J5_Pos_Angle_limit'])
  J5StepLim   =float(config['Limits']['J5_Step_limit'])
  J6NegAngLim =float(config['Limits']['J6_Neg_Angle_limit'])
  J6PosAngLim =float(config['Limits']['J6_Pos_Angle_limit'])
  J5StepLim   =float(config['Limits']['J6_Step_limit'])

  DHa1        =float(config['DH parameters']['DHa1'])
  DHa2        =float(config['DH parameters']['DHa2'])
  DHa3        =float(config['DH parameters']['DHa3'])
  DHa4        =float(config['DH parameters']['DHa4'])
  DHa5        =float(config['DH parameters']['DHa5'])
  DHa6        =float(config['DH parameters']['DHa6'])
  DHr1        =float(config['DH parameters']['DHr1'])
  DHr2        =float(config['DH parameters']['DHr2'])
  DHr3        =float(config['DH parameters']['DHr3'])
  DHr4        =float(config['DH parameters']['DHr4'])
  DHr5        =float(config['DH parameters']['DHr5'])
  DHr6        =float(config['DH parameters']['DHr6'])
  DHd1        =float(config['DH parameters']['DHd1'])
  DHd2        =float(config['DH parameters']['DHd2'])
  DHd3        =float(config['DH parameters']['DHd3'])
  DHd4        =float(config['DH parameters']['DHd4'])
  DHd5        =float(config['DH parameters']['DHd5'])
  DHd6        =float(config['DH parameters']['DHd6'])
  DHt1        =float(config['DH parameters']['DHt1'])
  DHt2        =float(config['DH parameters']['DHt2'])
  DHt3        =float(config['DH parameters']['DHt3'])
  DHt4        =float(config['DH parameters']['DHt4'])
  DHt5        =float(config['DH parameters']['DHt5'])
  DHt6        =float(config['DH parameters']['DHt6'])


  CalDir      'General']['Calibration_direction']
  MotDir      'General']['Motion_direction']
  TrackcurPos =float(config['Track'][''])
  TrackLength =float(config['Track']['Track_legth'])
  TrackStepLim=float(config['Track']['Track_step_limit'])

  VisFileLoc  'Visual']['Vis_File_Location']
  VisProg     'Visual'][''])
  VisOrigXpix 'Visual']['origin_x_pixels']
  VisOrigXmm  'Visual']['origin_x_mm']
  VisOrigYpix 'Visual']['origin_y_pixels']
  VisOrigYmm  'Visual']['origin_y_mm']
  VisEndXpix  'Visual']['end_x_pixels']
  VisEndXmm   'Visual']['end_x_mm']
  VisEndYpix  'Visual']['end_y_pixels']
  VisEndYmm   'Visual']['end_y_mm']

  
  J1OpenLoopVal=config['']['']
  J2OpenLoopVal=config['']['']
  J3OpenLoopVal=config['']['']
  J4OpenLoopVal=config['']['']
  J5OpenLoopVal=config['']['']
  J6OpenLoopVal=config['']['']

  Ui.comPort1.setText(comPort)
  Ui.comPort2.setText(com2Port)
  

  Ui.dh_alpha1.setText(Dha1)
  Ui.dh_alpha2.setText(Dha2)
  Ui.dh_alpha3.setText(Dha3)
  Ui.dh_alpha4.setText(Dha4)
  Ui.dh_alpha5.setText(Dha5)
  Ui.dh_alpha6.setText(Dha6)

  Ui.dh_a1.setText(DHr1)
  Ui.dh_a2.setText(DHr2)
  Ui.dh_a3.setText(DHr3)
  Ui.dh_a4.setText(DHr4)
  Ui.dh_a5.setText(DHr5)
  Ui.dh_a6.setText(DHr6)

  Ui.dh_d1.setText(DHd1)
  Ui.dh_d2.setText(DHd2)
  Ui.dh_d3.setText(DHd3)
  Ui.dh_d4.setText(DHd4)
  Ui.dh_d5.setText(DHd5)
  Ui.dh_d6.setText(DHd6)

  Ui.dh_theta1.setText(DHt1)
  Ui.dh_theta2.setText(DHt2)
  Ui.dh_theta3.setText(DHt3)
  Ui.dh_theta4.setText(DHt4)
  Ui.dh_theta5.setText(DHt5)
  Ui.dh_theta6.setText(DHt6)


def saveConfig(self):

  config = configparser.ConfigParser()
  

  config[''][''] = J1StepCur  
  config[''][''] = J1AngCur    
  config[''][''] = J2StepCur   
  config[''][''] = J2AngCur    
  config[''][''] = J3StepCur   
  config[''][''] = J3AngCur    
  config[''][''] = J4StepCur   
  config[''][''] = J4AngCur    
  config[''][''] = J5StepCur   
  config[''][''] = J5AngCur    
  config[''][''] = J6StepCur   
  config[''][''] = J6AngCur    
  config['General']['comPort1'] = comPort     
  config['General']['comPort2'] = com2Port 
  config[''][''] = Prog        
  config[''][''] = Servo0on    
  config[''][''] = Servo0off   
  config[''][''] = Servo1on    
  config[''][''] = Servo1off   
  config[''][''] = DO1on       
  config[''][''] = DO1off      
  config[''][''] = DO2on       
  config[''][''] = DO2off      
  config[''][''] = UFx         
  config[''][''] = UFy         
  config[''][''] = UFz         
  config[''][''] = UFrx        
  config[''][''] = UFry        
  config[''][''] = UFrz        
  config[''][''] = TFx         
  config[''][''] = TFy         
  config[''][''] = TFz         
  config[''][''] = TFrx        
  config[''][''] = TFry        
  config[''][''] = TFrz        
  config[''][''] = FineCalPos  

  config['Limits']['J1_Neg_Angle_Limit'] = J1NegAngLim 
  config['Limits']['J1_Pos_Angle_Limit'] = J1PosAngLim 
  config['Limits']['J1_Step_limit'] = J1StepLim 
  config['Limits']['J2_Neg_Angle_limit'] = J2NegAngLim 
  config['Limits']['J2_Pos_Angle_limit'] = J2PosAngLim 
  config['Limits']['J2_Step_limit'] = J2StepLim   
  config['Limits']['J3_Neg_Angle_limit'] = J3NegAngLim 
  config['Limits']['J3_Pos_Angle_limit'] = J3PosAngLim
  config['Limits']['J3_Step_limit'] = J3StepLim  
  config['Limits']['J4_Neg_Angle_limit'] = J4NegAngLim
  config['Limits']['J4_Pos_Angle_limit'] = J4PosAngLim 
  config['Limits']['J4_Step_limit'] = J4StepLim
  config['Limits']['J5_Neg_Angle_limit'] = J5NegAngLim 
  config['Limits']['J5_Pos_Angle_limit'] = J5PosAngLim 
  config['Limits']['J5_Step_limit'] = J5StepLim
  config['Limits']['J6_Neg_Angle_limit'] = J6NegAngLim 
  config['Limits']['J6_Pos_Angle_limit'] = J6PosAngLim 
  config['Limits']['J6_Step_limit'] = J5StepLim

  config['DH parameters']['DHa1'] = DHa1
  config['DH parameters']['DHa2'] = DHa2
  config['DH parameters']['DHa3'] = DHa3
  config['DH parameters']['DHa4'] = DHa4
  config['DH parameters']['DHa5'] = DHa5
  config['DH parameters']['DHa6'] = DHa6
  config['DH parameters']['DHr1'] = DHr1
  config['DH parameters']['DHr2'] = DHr2
  config['DH parameters']['DHr3'] = DHr3
  config['DH parameters']['DHr4'] = DHr4
  config['DH parameters']['DHr5'] = DHr5
  config['DH parameters']['DHr6'] = DHr6
  config['DH parameters']['DHd1'] = DHd1
  config['DH parameters']['DHd2'] = DHd2
  config['DH parameters']['DHd3'] = DHd3
  config['DH parameters']['DHd4'] = DHd4
  config['DH parameters']['DHd5'] = DHd5
  config['DH parameters']['DHd6'] = DHd6
  config['DH parameters']['DHt1'] = DHt1
  config['DH parameters']['DHt2'] = DHt2
  config['DH parameters']['DHt3'] = DHt3
  config['DH parameters']['DHt4'] = DHt4
  config['DH parameters']['DHt5'] = DHt5
  config['DH parameters']['DHt6'] = DHt6


 config['General']['Calibration_direction'] =  CalDir
 config['General']['Motion_direction'] =  MotDir
config['Track'][''] =   TrackcurPos  
  TrackLength  config['Track']['Track_legth'])
  TrackStepLim config['Track']['Track_step_limit'])

  VisFileLoc  =(config['Visual']['Vis_File_Location']
  VisProg     =(config['Visual'][''])
  VisOrigXpix =(config['Visual']['origin_x_pixels']
  VisOrigXmm  =(config['Visual']['origin_x_mm']
  VisOrigYpix =(config['Visual']['origin_y_pixels']
  VisOrigYmm  =(config['Visual']['origin_y_mm']
  VisEndXpix  =(config['Visual']['end_x_pixels']
  VisEndXmm   =(config['Visual']['end_x_mm']
  VisEndYpix  =(config['Visual']['end_y_pixels']
  VisEndYmm   =(config['Visual']['end_y_mm']

  
  J1OpenLoopVal
  J2OpenLoopVal
  J3OpenLoopVal
  J4OpenLoopVal
  J5OpenLoopVal
  J6OpenLoopVal



  with open('config.ini', 'w') as configfile:
          config.write(configfile)
####

if (J1OpenLoopVal == 1):
  J1OpenLoopCbut.select()
if (J2OpenLoopVal == 1):
  J2OpenLoopCbut.select()
if (J3OpenLoopVal == 1):
  J3OpenLoopCbut.select()
if (J4OpenLoopVal == 1):
  J4OpenLoopCbut.select()
if (J5OpenLoopVal == 1):
  J5OpenLoopCbut.select()
if (J6OpenLoopVal == 1):
  J6OpenLoopCbut.select()  
  

SaveAndApplyCalibration()
DisplaySteps()
CalcFwdKin()
setCom()
setCom2()


loadProg()
msg = "ANNIN ROBOTICS SOFTWARE AND MODELS ARE FREE:\n\
\n\
*for personal use.\n\
*for educational use.\n\
*for building your own robot(s).\n\
*for automating your own business.\n\
\n\
IT IS NOT OK TO RESELL THIS SOFTWARE\n\
FOR A PROFIT - IT MUST REMAIN FREE.\n\
\n\
IT IS NOT OK TO SELL AR2 ROBOTS,\n\
ROBOT PARTS, OR ANY OTHER VERSION \n\
OF ROBOT OR SOFTWARE BASED ON THE \n\
AR2 ROBOT DESIGN FOR PROFIT.\n\
\n\
Copyright (c) 2019, Chris Annin"

tkinter.messagebox.showwarning("ARCS License / Copyright notice", msg)
xboxUse = 0

