from tkinter import *
from tkinter.ttk import *
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, messagebox, HORIZONTAL
import sys
from threading import Thread, Lock
import re
import matplotlib.pyplot as plt
import serial

class RunGUI:
	
	def __init__(self, master):
		
		self.CURRENTGEAR = "3"
		self.CURRENTSPEED = "30"
		self.CURRENTRPM = "20"
		self.CURRENTOIL = "0"
		self.CURRENTGPSX = "0"
		self.CURRENTGPSY = "0"
		self.CURRENTTORQUE = "0"
		self.CURRENTENGINELOAD = "0"
		self.CURRENTRUNTIME = "0"
		self.CURRENTINTAKETEMP = "0"
		self.CURRENTACCELX = "0"
		self.CURRENTACCELY = "0"
		self.CURRENTACCELZ = "0"
	
		#threads active booleans
		self.listenRaceBoolean = False
		self.listenStatsBoolean = False
		#self.listenGraph = False

		self.master = master
		master.title("Smart Car Plus Plus")

		#define any colors that are going to be used across the app
		self.buttonClickedColor = '#696969'
		self.buttonUnclick = '#A9A9A9'

		#create the buttons
		self.raceBtn = Button(master, text="Race", command=lambda: self.runRaceMode())
		self.statsBtn = Button(master, text="Stats", command=lambda: self.statsMode())
		self.graphBtn = Button(master, text="Graph", command=lambda: self.startGraph())

		#Racemode Init
		self.currentGearLbl = Label(master, text="  Gear:", font=("Helvetica", 16), fg="red")
		self.currentGearLbl.config( height = 3, width = 6 )
		self.speedLbl = Label(master, text="Speed:", font=("Helvetica", 16), fg="red")
		self.speedLbl.config( height = 3, width = 6 )
		self.rpmLbl = Label(master, text="  RPM:", font=("Helvetica", 16), fg="red")
		self.rpmLbl.config( height = 3, width = 6 )
		self.currentGear = Label(master, text="0", font=("Helvetica", 16), fg="red")
		self.currentGear.config( height = 3, width = 3 )

		#Stats Init
		self.currentOilTempLbl = Label(master, text="Oil Temperature:", font=("Helvetica", 15), fg="red")
		self.statsRpmLbl = Label(master, text="     Current RPM:", font=("Helvetica", 15), fg="red")
		self.statsSpeedLbl = Label(master, text="   Current Speed:", font=("Helvetica", 15), fg="red")
		self.statsGpsLbl = Label(master, text="      Current GPS:", font=("Helvetica", 15), fg="red")
		self.statsTorque = Label(master, text="  Current Torque:", font=("Helvetica", 15), fg="red")
		self.statsAccelerometerData = Label(master, text="    accelerometer:", font=("Helvetica", 15), fg="red")
		self.statsEngineLoad = Label(master, text="        engine load:", font=("Helvetica", 15), fg="red")
		self.statsRuntime = Label(master, text="              Runtime:", font=("Helvetica", 15), fg="red")
		self.statsIntakeTemp = Label(master, text="        Intake Temp:", font=("Helvetica", 15), fg="red")

		#stats values
		self.statsOilValue = Label(master, text="0 F", font=("Helvetica", 15), fg="red")
		self.statsRpmValue = Label(master, text="234", font=("Helvetica", 15), fg="red")
		self.statsSpeedValue = Label(master, text="60 mph", font=("Helvetica", 15), fg="red")
		self.statsGpsValue = Label(master, text="(-3454, 3432233)", font=("Helvetica", 15), fg="red")
		self.statsTorqueValue = Label(master, text="500", font=("Helvetica", 15), fg="red")
		self.statsAccelerometerDataValue = Label(master, text="30", font=("Helvetica", 15), fg="red")
		self.statsEngineLoadValue = Label(master, text="60%", font=("Helvetica", 15), fg="red")
		self.statsRuntimeValue = Label(master, text="0.3 hr", font=("Helvetica", 15), fg="red")
		self.statsIntakeTempValue = Label(master, text="30 F", font=("Helvetica", 15), fg="red")
		

		#progress bar intit
		self.speedProgress = Progressbar(master,orient=HORIZONTAL,length=250,mode='determinate')
		self.rpmProgress = Progressbar(master,orient=HORIZONTAL,length=250,mode='determinate')	


		#make graph image
		#self.startGraph()
		#self.graphImage = PhotoImage(file="g.png")

		#serial read thread
		serialRead = Thread(target= self.readSerialVals)
		serialRead.start()

		#create layout and lunch racemode
		self.createLayouts()
		self.runRaceMode()

	def createLayouts(self):
		#set the button sizes and colors
		self.raceBtn.config( height = 0, width = 17 )
		self.statsBtn.config( height = 0, width = 17 )
		self.graphBtn.config( height = 0, width = 17 )
		self.raceBtn.configure(background=self.buttonClickedColor)
		self.statsBtn.configure(background=self.buttonUnclick)
		self.graphBtn.configure(background=self.buttonUnclick)
		
		# LAYOUT

		#buttons
		self.raceBtn.grid(row=2, column=0)
		self.statsBtn.grid(row=2, column=2)
		self.graphBtn.grid(row=2, column=3)

		#racemode layout setup 
		self.currentGearLbl.grid(row = 3, sticky=W)
		self.currentGear.grid(row=3, column=2, columnspan=2, sticky=W)
		self.speedLbl.grid(row=4, sticky=W)
		self.rpmLbl.grid(row=5, sticky=W)

		#Stats layout
		self.currentOilTempLbl.grid(row=3, column=0, columnspan=2, sticky=W)
		self.statsRpmLbl.grid(row=4, column=0, columnspan=2, sticky=W)
		self.statsSpeedLbl.grid(row=5, column=0, columnspan=2, sticky=W)
		self.statsGpsLbl.grid(row=6, column=0, columnspan=2, sticky=W)
		self.statsTorque.grid(row=7, column=0, columnspan=2, sticky=W)
		self.statsAccelerometerData.grid(row=8, column=0, columnspan=2, sticky=W)
		self.statsEngineLoad.grid(row=9, column=0, columnspan=2, sticky=W)
		self.statsRuntime.grid(row=10, column=0, columnspan=2, sticky=W)
		self.statsIntakeTemp.grid(row=11, column=0, columnspan=2, sticky=W)

		#stats value layouts
		self.statsOilValue.grid(row=3, column=3, columnspan=2, sticky=W)
		self.statsRpmValue.grid(row=4, column=3, columnspan=2, sticky=W)
		self.statsSpeedValue.grid(row=5, column=3, columnspan=2, sticky=W)
		self.statsGpsValue.grid(row=6, column=3, columnspan=2, sticky=W)
		self.statsTorqueValue.grid(row=7, column=3, columnspan=2, sticky=W)
		self.statsAccelerometerDataValue.grid(row=8, column=3, columnspan=2, sticky=W)
		self.statsEngineLoadValue.grid(row=9, column=3, columnspan=2, sticky=W)
		self.statsRuntimeValue.grid(row=10, column=3, columnspan=2, sticky=W)
		self.statsIntakeTempValue.grid(row=11, column=3, columnspan=2, sticky=W)

		#image layout
		#self.graphImage.grid(row=0, column=0, columnspan=4, rowspan=4,sticky=W+E+N+S)


		#progress bar
		self.speedProgress.grid(row=4, column=2, columnspan=3, sticky=W)
		self.rpmProgress.grid(row=5, column=2, columnspan=3, sticky=W)

	#function preforms racemode opperations
	def runRaceMode(self):
		self.clearFrame()
		self.setupRaceMode()
		self.raceBtn.configure(background= self.buttonClickedColor)

		#progress bar
		self.speedProgress.grid(row=4, column=2, columnspan=3, sticky=W)
		self.rpmProgress.grid(row=5, column=2, columnspan=3, sticky=W)

		#start the thread
		raceModeListeners = Thread(target= self.listenRace)
		self.listenRaceBoolean = True
		raceModeListeners.start()
		
		

	#function performs stats mode actions
	def statsMode(self):
		self.clearFrame()
		self.statsBtn.configure(background= self.buttonClickedColor)
		self.setupStatsMode()

		#start the listening thread
		statsListener = Thread(target= self.listenStats)
		self.listenStatsBoolean = True
		statsListener.start()

	#function launches the graph
	def startGraph(self):
		self.clearFrame()
		self.graphBtn.configure(background= self.buttonClickedColor)
		self.listenGraph = True
		self.launchGraph([1,2,3,4,5,6,7,8,9])

	#function launches the graph 
	def launchGraph(self, numToPlot):
		plt.plot(numToPlot)
		plt.ylabel('Speed')
		#plt.savefig('g.png')
		#graphImage.grid(row=0, column=0, columnspan=4, rowspan=4,sticky=W+E+N+S)



	#function listens for racing values to change or not
	def listenRace(self):
		while(self.listenRaceBoolean):
			self.currentGear.configure(text = self.CURRENTGEAR)
			self.rpmProgress['value'] = (int(self.CURRENTRPM)/40)
			self.speedProgress['value'] = int(self.CURRENTSPEED)

	#function listens for the stats to change
	def listenStats(self):
		
		#listen and set all values
		while(self.listenStatsBoolean):
			self.statsOilValue.configure(text = self.CURRENTOIL)
			self.statsRpmValue.configure(text = self.CURRENTRPM)
			self.statsSpeedValue.configure(text = self.CURRENTSPEED)
			self.statsGpsValue.configure(text = "(" + self.CURRENTGPSX + ", " + self.CURRENTGPSY + ")")
			self.statsTorqueValue.configure(text = self.CURRENTTORQUE)
			self.statsAccelerometerDataValue.configure(text = "(" + self.CURRENTACCELX + ", " + self.CURRENTACCELY +  ", " + self.CURRENTACCELZ + ")" )
			self.statsEngineLoadValue.configure(text = self.CURRENTENGINELOAD)
			self.statsRuntimeValue.configure(text = self.CURRENTRUNTIME)
			self.statsIntakeTempValue.configure(text = self.CURRENTINTAKETEMP)

	#fucntion runs on its own thread throughout all of runtime
	def readSerialVals(self):
		count = 0

		port = self.getPortNumber()
		#setup the port
		if (port == -1):
			print ("failed to find valid port")
			return
		
		ser = serial.Serial('/dev/ttyACM' + str(port), 9600)

		while True:
			data = ser.readline()
			if data != b'0':
				if count > 7:
					
					data = data.decode("utf-8") 
					data = re.sub("[\{\}]", "", data)
					data = data.split(';')

					try:
						if (data[0] == '0'):
							self.CURRENTRPM = data[1]
							self.CURRENTSPEED = data[2]
							self.CURRENTINTAKETEMP = data[4]
							self.CURRENTOIL = data[5]
							self.CURRENTTORQUE = data[7]
						elif (data[0] == '1'):
							self.CURRENTGPSX = data[1]
							self.CURRENTGPSY = data[2]
							self.CURRENTACCELX = data[3]
							self.CURRENTACCELY = data[4]
							self.CURRENTACCELZ = data[5]
					except:
						print ("something went wrong data not up to date")
					#print(data)
				count += 1
		

	def getPortNumber(self):
		#check all ports to make sure it always runs on plug in
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600)
			return 0
		except:
			print("failed to use port 0.  reverting to port 1")
		try:
			ser = serial.Serial('/dev/ttyACM1', 9600)
			return 1
		except:
			print("failed to use port 1.  reverting to port 2")
		try:
			ser = serial.Serial('/dev/ttyAC20', 9600)
			return 2
		except:
			print("failed to use port 2.  reverting to port 3")
		try:
			ser = serial.Serial('/dev/ttyACM3', 9600)
			return 3
		except:
			print("failed to use port 3. error,  no port found")
			return - 1
																				#this is all setup code
	#function sets up stats paghe
	def setupStatsMode(self):
		self.currentOilTempLbl.grid()
		self.statsRpmLbl.grid()
		self.statsSpeedLbl.grid()
		self.statsGpsLbl.grid()
		self.statsTorque.grid()
		self.statsAccelerometerData.grid()
		self.statsEngineLoad.grid()
		self.statsRuntime.grid()
		self.statsIntakeTemp.grid()

		#stats values
		self.statsOilValue.grid(row=3, column=2, columnspan=2, sticky=W)
		self.statsRpmValue.grid(row=4, column=2, columnspan=2, sticky=W)
		self.statsSpeedValue.grid(row=5, column=2, columnspan=2, sticky=W)
		self.statsGpsValue.grid(row=6, column=2, columnspan=2, sticky=W)
		self.statsTorqueValue.grid(row=7, column=2, columnspan=2, sticky=W)
		self.statsAccelerometerDataValue.grid(row=8, column=2, columnspan=2, sticky=W)
		self.statsEngineLoadValue.grid(row=9, column=2, columnspan=2, sticky=W)
		self.statsRuntimeValue.grid(row=10, column=2, columnspan=2, sticky=W)
		self.statsIntakeTempValue.grid(row=11, column=2, columnspan=2, sticky=W)

	#code to resetup all views
	def setupRaceMode(self):
		self.currentGearLbl.grid()
		self.speedLbl.grid()
		self.rpmLbl.grid()
		self.currentGear.grid(row=3, column=2, columnspan=2, sticky=W)
		self.speedProgress.grid()
		self.rpmProgress.grid()

	#add to this everytime u add item to GUI to clear between shows
	def clearFrame(self):
		#reset all button background colors
		self.raceBtn.configure(background= self.buttonUnclick)
		self.statsBtn.configure(background=self.buttonUnclick)
		self.graphBtn.configure(background=self.buttonUnclick)

		#clear the race frame
		self.currentGearLbl.grid_forget()
		self.speedLbl.grid_forget()
		self.rpmLbl.grid_forget()
		self.currentGear.grid_forget()
		self.speedProgress.grid_forget()
		self.rpmProgress.grid_forget()

		#clear the stats frame
		self.currentOilTempLbl.grid_forget()
		self.statsRpmLbl.grid_forget()
		self.statsSpeedLbl.grid_forget()
		self.statsGpsLbl.grid_forget()
		self.statsTorque.grid_forget()
		self.statsAccelerometerData.grid_forget()
		self.statsEngineLoad.grid_forget()
		self.statsRuntime.grid_forget()
		self.statsIntakeTemp.grid_forget()
		#remove stats values
		self.statsOilValue.grid_forget()
		self.statsRpmValue.grid_forget()
		self.statsSpeedValue.grid_forget()
		self.statsGpsValue.grid_forget()
		self.statsTorqueValue.grid_forget()
		self.statsAccelerometerDataValue.grid_forget()
		self.statsEngineLoadValue.grid_forget()
		self.statsRuntimeValue.grid_forget()
		self.statsIntakeTempValue.grid_forget()

		#remove the graph image 
		#self.graphImage.grid_forget()
		
		#kill all current threads
		self.listenRaceBoolean = False
		self.listenStatsBoolean = False
		#self.listenGraph = False

root = Tk()
root.attributes('-fullscreen', True)
my_gui = RunGUI(root)
root.mainloop()
