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
import pickle
import serial
import time
import threading
import queue
import math
import tkinter.messagebox
import webbrowser
import numpy as np
import datetime




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
 
def J1jogNeg():
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
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
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
  if (J1Degs <= -(J1NegAngLim - J1AngCur)):   
    J1StepCur = J1StepCur - int(J1jogSteps)
    J1AngCur = round(J1NegAngLim + (J1StepCur * J1DegPerStep),2)
    J1curAngEntryField.delete(0, 'end')
    J1curAngEntryField.insert(0,str(J1AngCur))
    savePosData()
    CalcFwdKin()
    command = "MJA"+J1motdir+str(J1jogSteps)+"S"+Speed+"G"+ACCdur+"H"+ACCspd+"I"+DECdur+"K"+DECspd+"U"+str(J1StepCur)+"V"+str(J2StepCur)+"W"+str(J3StepCur)+"X"+str(J4StepCur)+"Y"+str(J5StepCur)+"Z"+str(J6StepCur)+"\n"
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
    almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
    almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
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
  
def TXjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos
  CY = YcurPos 
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0 - float(TXjogEntryField.get())
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

def TYjogNeg():
  almStatusLab.config(text="SYSTEM READY", bg = "cornflowerblue")
  almStatusLab2.config(text="SYSTEM READY", bg = "cornflowerblue")
  CX = XcurPos 
  CY = YcurPos
  CZ = ZcurPos
  CRx = RxcurPos
  CRy = RycurPos
  CRz = RzcurPos
  TCX = 0
  TCY = 0 - float(TYjogEntryField.get()) 
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

def TZjogNeg():
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
  TCZ = 0 - float(TZjogEntryField.get())
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

calibration = Listbox(tab2,width=20,height=60)
#calibration.place(x=160,y=170)


try:
  Cal = pickle.load(open("ARbot.cal","rb"))
except:
  Cal = "0"
  pickle.dump(Cal,open("ARbot.cal","wb"))
for item in Cal:
  calibration.insert(END,item)
J1StepCur   =calibration.get("0")
J1AngCur    =calibration.get("1")
J2StepCur   =calibration.get("2")
J2AngCur    =calibration.get("3")
J3StepCur   =calibration.get("4")
J3AngCur    =calibration.get("5")
J4StepCur   =calibration.get("6")
J4AngCur    =calibration.get("7")
J5StepCur   =calibration.get("8")
J5AngCur    =calibration.get("9")
J6StepCur   =calibration.get("10")
J6AngCur    =calibration.get("11")
comPort     =calibration.get("12")
Prog        =calibration.get("13")
Servo0on    =calibration.get("14")
Servo0off   =calibration.get("15")
Servo1on    =calibration.get("16")
Servo1off   =calibration.get("17")
DO1on       =calibration.get("18")
DO1off      =calibration.get("19")
DO2on       =calibration.get("20")
DO2off      =calibration.get("21")
UFx         =calibration.get("22")
UFy         =calibration.get("23")
UFz         =calibration.get("24")
UFrx        =calibration.get("25")
UFry        =calibration.get("26")
UFrz        =calibration.get("27")
TFx         =calibration.get("28")
TFy         =calibration.get("29")
TFz         =calibration.get("30")
TFrx        =calibration.get("31")
TFry        =calibration.get("32")
TFrz        =calibration.get("33")
FineCalPos  =calibration.get("34")
J1NegAngLim =calibration.get("35")
J1PosAngLim =calibration.get("36")
J1StepLim   =calibration.get("37")
J2NegAngLim =calibration.get("38")
J2PosAngLim =calibration.get("39")
J2StepLim   =calibration.get("40")
J3NegAngLim =calibration.get("41")
J3PosAngLim =calibration.get("42")
J3StepLim   =calibration.get("43")
J4NegAngLim =calibration.get("44")
J4PosAngLim =calibration.get("45")
J4StepLim   =calibration.get("46")
J5NegAngLim =calibration.get("47")
J5PosAngLim =calibration.get("48")
J5StepLim   =calibration.get("49")
J6NegAngLim =calibration.get("50")
J6PosAngLim =calibration.get("51")
J6StepLim   =calibration.get("52")
DHr1        =calibration.get("53")
DHr2        =calibration.get("54")
DHr3        =calibration.get("55")
DHr4        =calibration.get("56")
DHr5        =calibration.get("57")
DHr6        =calibration.get("58")
DHa1        =calibration.get("59")
DHa2        =calibration.get("60")
DHa3        =calibration.get("61")
DHa4        =calibration.get("62")
DHa5        =calibration.get("63")
DHa6        =calibration.get("64")
DHd1        =calibration.get("65")
DHd2        =calibration.get("66")
DHd3        =calibration.get("67")
DHd4        =calibration.get("68")
DHd5        =calibration.get("69")
DHd6        =calibration.get("70")
DHt1        =calibration.get("71")
DHt2        =calibration.get("72")
DHt3        =calibration.get("73")
DHt4        =calibration.get("74")
DHt5        =calibration.get("75")
DHt6        =calibration.get("76")
CalDir      =calibration.get("77")
MotDir      =calibration.get("78")
TrackcurPos =calibration.get("79")
TrackLength =calibration.get("80")
TrackStepLim=calibration.get("81")
VisFileLoc  =calibration.get("82")
VisProg     =calibration.get("83")
VisOrigXpix =calibration.get("84")
VisOrigXmm  =calibration.get("85")
VisOrigYpix =calibration.get("86")
VisOrigYmm  =calibration.get("87")
VisEndXpix  =calibration.get("88")
VisEndXmm   =calibration.get("89")
VisEndYpix  =calibration.get("90")
VisEndYmm   =calibration.get("91")
com2Port    =calibration.get("92")
J1OpenLoopVal=calibration.get("93")
J2OpenLoopVal=calibration.get("94")
J3OpenLoopVal=calibration.get("95")
J4OpenLoopVal=calibration.get("96")
J5OpenLoopVal=calibration.get("97")
J6OpenLoopVal=calibration.get("98")


####

J1curAngEntryField.insert(0,str(J1AngCur))
J2curAngEntryField.insert(0,str(J2AngCur))
J3curAngEntryField.insert(0,str(J3AngCur))
J4curAngEntryField.insert(0,str(J4AngCur))
J5curAngEntryField.insert(0,str(J5AngCur))
J6curAngEntryField.insert(0,str(J6AngCur))
comPortEntryField.insert(0,str(comPort))
com2PortEntryField.insert(0,str(com2Port))
speedEntryField.insert(0,"25")
ACCdurField.insert(0,"15")
ACCspeedField.insert(0,"10")
DECdurField.insert(0,"20")
DECspeedField.insert(0,"5")
ProgEntryField.insert(0,(Prog))
SavePosEntryField.insert(0,"1")
J1jogDegsEntryField.insert(0,"10")
J2jogDegsEntryField.insert(0,"10")
J3jogDegsEntryField.insert(0,"10")
J4jogDegsEntryField.insert(0,"10")
J5jogDegsEntryField.insert(0,"10")
J6jogDegsEntryField.insert(0,"10")
XjogEntryField.insert(0,"20")
YjogEntryField.insert(0,"20")
ZjogEntryField.insert(0,"20")
RxjogEntryField.insert(0,"20")
RyjogEntryField.insert(0,"20")
RzjogEntryField.insert(0,"20")
TXjogEntryField.insert(0,"20")
TYjogEntryField.insert(0,"20")
TZjogEntryField.insert(0,"20")
TRxjogEntryField.insert(0,"20")
TRyjogEntryField.insert(0,"20")
TRzjogEntryField.insert(0,"20")
R1EntryField.insert(0,"0")
R2EntryField.insert(0,"0")
R3EntryField.insert(0,"0")
R4EntryField.insert(0,"0")
R5EntryField.insert(0,"0")
R6EntryField.insert(0,"0")
R7EntryField.insert(0,"0")
R8EntryField.insert(0,"0")
R9EntryField.insert(0,"0")
R10EntryField.insert(0,"0")
R11EntryField.insert(0,"0")
R12EntryField.insert(0,"0")
R13EntryField.insert(0,"0")
R14EntryField.insert(0,"0")
R15EntryField.insert(0,"0")
R16EntryField.insert(0,"0")
SP_1_E1_EntryField.insert(0,"0")
SP_2_E1_EntryField.insert(0,"0")
SP_3_E1_EntryField.insert(0,"0")
SP_4_E1_EntryField.insert(0,"0")
SP_5_E1_EntryField.insert(0,"0")
SP_6_E1_EntryField.insert(0,"0")
SP_7_E1_EntryField.insert(0,"0")
SP_8_E1_EntryField.insert(0,"0")
SP_9_E1_EntryField.insert(0,"0")
SP_10_E1_EntryField.insert(0,"0")
SP_11_E1_EntryField.insert(0,"0")
SP_12_E1_EntryField.insert(0,"0")
SP_13_E1_EntryField.insert(0,"0")
SP_14_E1_EntryField.insert(0,"0")
SP_15_E1_EntryField.insert(0,"0")
SP_16_E1_EntryField.insert(0,"0")
SP_1_E2_EntryField.insert(0,"0")
SP_2_E2_EntryField.insert(0,"0")
SP_3_E2_EntryField.insert(0,"0")
SP_4_E2_EntryField.insert(0,"0")
SP_5_E2_EntryField.insert(0,"0")
SP_6_E2_EntryField.insert(0,"0")
SP_7_E2_EntryField.insert(0,"0")
SP_8_E2_EntryField.insert(0,"0")
SP_9_E2_EntryField.insert(0,"0")
SP_10_E2_EntryField.insert(0,"0")
SP_11_E2_EntryField.insert(0,"0")
SP_12_E2_EntryField.insert(0,"0")
SP_13_E2_EntryField.insert(0,"0")
SP_14_E2_EntryField.insert(0,"0")
SP_15_E2_EntryField.insert(0,"0")
SP_16_E2_EntryField.insert(0,"0")
SP_1_E3_EntryField.insert(0,"0")
SP_2_E3_EntryField.insert(0,"0")
SP_3_E3_EntryField.insert(0,"0")
SP_4_E3_EntryField.insert(0,"0")
SP_5_E3_EntryField.insert(0,"0")
SP_6_E3_EntryField.insert(0,"0")
SP_7_E3_EntryField.insert(0,"0")
SP_8_E3_EntryField.insert(0,"0")
SP_9_E3_EntryField.insert(0,"0")
SP_10_E3_EntryField.insert(0,"0")
SP_11_E3_EntryField.insert(0,"0")
SP_12_E3_EntryField.insert(0,"0")
SP_13_E3_EntryField.insert(0,"0")
SP_14_E3_EntryField.insert(0,"0")
SP_15_E3_EntryField.insert(0,"0")
SP_16_E3_EntryField.insert(0,"0")
SP_1_E4_EntryField.insert(0,"0")
SP_2_E4_EntryField.insert(0,"0")
SP_3_E4_EntryField.insert(0,"0")
SP_4_E4_EntryField.insert(0,"0")
SP_5_E4_EntryField.insert(0,"0")
SP_6_E4_EntryField.insert(0,"0")
SP_7_E4_EntryField.insert(0,"0")
SP_8_E4_EntryField.insert(0,"0")
SP_9_E4_EntryField.insert(0,"0")
SP_10_E4_EntryField.insert(0,"0")
SP_11_E4_EntryField.insert(0,"0")
SP_12_E4_EntryField.insert(0,"0")
SP_13_E4_EntryField.insert(0,"0")
SP_14_E4_EntryField.insert(0,"0")
SP_15_E4_EntryField.insert(0,"0")
SP_16_E4_EntryField.insert(0,"0")
SP_1_E5_EntryField.insert(0,"0")
SP_2_E5_EntryField.insert(0,"0")
SP_3_E5_EntryField.insert(0,"0")
SP_4_E5_EntryField.insert(0,"0")
SP_5_E5_EntryField.insert(0,"0")
SP_6_E5_EntryField.insert(0,"0")
SP_7_E5_EntryField.insert(0,"0")
SP_8_E5_EntryField.insert(0,"0")
SP_9_E5_EntryField.insert(0,"0")
SP_10_E5_EntryField.insert(0,"0")
SP_11_E5_EntryField.insert(0,"0")
SP_12_E5_EntryField.insert(0,"0")
SP_13_E5_EntryField.insert(0,"0")
SP_14_E5_EntryField.insert(0,"0")
SP_15_E5_EntryField.insert(0,"0")
SP_16_E5_EntryField.insert(0,"0")
SP_1_E6_EntryField.insert(0,"0")
SP_2_E6_EntryField.insert(0,"0")
SP_3_E6_EntryField.insert(0,"0")
SP_4_E6_EntryField.insert(0,"0")
SP_5_E6_EntryField.insert(0,"0")
SP_6_E6_EntryField.insert(0,"0")
SP_7_E6_EntryField.insert(0,"0")
SP_8_E6_EntryField.insert(0,"0")
SP_9_E6_EntryField.insert(0,"0")
SP_10_E6_EntryField.insert(0,"0")
SP_11_E6_EntryField.insert(0,"0")
SP_12_E6_EntryField.insert(0,"0")
SP_13_E6_EntryField.insert(0,"0")
SP_14_E6_EntryField.insert(0,"0")
SP_15_E6_EntryField.insert(0,"0")
SP_16_E6_EntryField.insert(0,"0")
servo0onEntryField.insert(0,str(Servo0on))
servo0offEntryField.insert(0,str(Servo0off))
servo1onEntryField.insert(0,str(Servo1on))
servo1offEntryField.insert(0,str(Servo1off))
DO1onEntryField.insert(0,str(DO1on))
DO1offEntryField.insert(0,str(DO1off))
DO2onEntryField.insert(0,str(DO2on))
DO2offEntryField.insert(0,str(DO2off))
UFxEntryField.insert(0,str(UFx))
UFyEntryField.insert(0,str(UFy))
UFzEntryField.insert(0,str(UFz))
UFrxEntryField.insert(0,str(UFrx))
UFryEntryField.insert(0,str(UFry))
UFrzEntryField.insert(0,str(UFrz))
TFxEntryField.insert(0,str(TFx))
TFyEntryField.insert(0,str(TFy))
TFzEntryField.insert(0,str(TFz))
TFrxEntryField.insert(0,str(TFrx))
TFryEntryField.insert(0,str(TFry))
TFrzEntryField.insert(0,str(TFrz))
fineCalEntryField.insert(0,str(FineCalPos))
J1NegAngLimEntryField.insert(0,str(J1NegAngLim))
J1PosAngLimEntryField.insert(0,str(J1PosAngLim))
J1StepLimEntryField.insert(0,str(J1StepLim))
J2NegAngLimEntryField.insert(0,str(J2NegAngLim))
J2PosAngLimEntryField.insert(0,str(J2PosAngLim))
J2StepLimEntryField.insert(0,str(J2StepLim))
J3NegAngLimEntryField.insert(0,str(J3NegAngLim))
J3PosAngLimEntryField.insert(0,str(J3PosAngLim))
J3StepLimEntryField.insert(0,str(J3StepLim))
J4NegAngLimEntryField.insert(0,str(J4NegAngLim))
J4PosAngLimEntryField.insert(0,str(J4PosAngLim))
J4StepLimEntryField.insert(0,str(J4StepLim))
J5NegAngLimEntryField.insert(0,str(J5NegAngLim))
J5PosAngLimEntryField.insert(0,str(J5PosAngLim))
J5StepLimEntryField.insert(0,str(J5StepLim))
J6NegAngLimEntryField.insert(0,str(J6NegAngLim))
J6PosAngLimEntryField.insert(0,str(J6PosAngLim))
J6StepLimEntryField.insert(0,str(J6StepLim))
DHr1EntryField.insert(0,str(DHr1))
DHr2EntryField.insert(0,str(DHr2))
DHr3EntryField.insert(0,str(DHr3))
DHr4EntryField.insert(0,str(DHr4))
DHr5EntryField.insert(0,str(DHr5))
DHr6EntryField.insert(0,str(DHr6))
DHa1EntryField.insert(0,str(DHa1))
DHa2EntryField.insert(0,str(DHa2))
DHa3EntryField.insert(0,str(DHa3))
DHa4EntryField.insert(0,str(DHa4))
DHa5EntryField.insert(0,str(DHa5))
DHa6EntryField.insert(0,str(DHa6))
DHd1EntryField.insert(0,str(DHd1))
DHd2EntryField.insert(0,str(DHd2))
DHd3EntryField.insert(0,str(DHd3))
DHd4EntryField.insert(0,str(DHd4))
DHd5EntryField.insert(0,str(DHd5))
DHd6EntryField.insert(0,str(DHd6))
DHt1EntryField.insert(0,str(DHt1))
DHt2EntryField.insert(0,str(DHt2))
DHt3EntryField.insert(0,str(DHt3))
DHt4EntryField.insert(0,str(DHt4))
DHt5EntryField.insert(0,str(DHt5))
DHt6EntryField.insert(0,str(DHt6))
CalDirEntryField.insert(0,str(CalDir))
MotDirEntryField.insert(0,str(MotDir))
TrackcurEntryField.insert(0,str(TrackcurPos))
TrackjogEntryField.insert(0,"10")
TrackLengthEntryField.insert(0,str(TrackLength))
TrackStepLimEntryField.insert(0,str(TrackStepLim))
VisFileLocEntryField.insert(0,str(VisFileLoc))
visoptions.set(VisProg)
VisPicOxPEntryField.insert(0,str(VisOrigXpix))
VisPicOxMEntryField.insert(0,str(VisOrigXmm))
VisPicOyPEntryField.insert(0,str(VisOrigYpix))
VisPicOyMEntryField.insert(0,str(VisOrigYmm))
VisPicXPEntryField.insert(0,str(VisEndXpix))
VisPicXMEntryField.insert(0,str(VisEndXmm))
VisPicYPEntryField.insert(0,str(VisEndYpix))
VisPicYMEntryField.insert(0,str(VisEndYmm))
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

global blockEncPosCal
blockEncPosCal = 0
global blockEncPosMove
blockEncPosMove = 0
  
monitor = threading.Thread(target=monitorEnc)
monitor.start()

tab1.mainloop()




#manEntryField.delete(0, 'end')
#manEntryField.insert(0,value)