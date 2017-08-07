#imports modules
import pandas as pd
import pyautogui as auto
import glob
import datetime
import time
import pickle
import os


#allows for a failsafe to break the program
auto.PAUSE = 1
auto.FAILSAFE = True

while True:
    #sets all the parameters for the program loop
    ##########################################################################start
    
    #set temperature logging start button position
    print('\n\n')
    print('  Welcome to thermalGUI for the SSTDR program automation.  '.center(240,'#'))
    input('Place the mouse over the start button and hit enter.'.center(80))
    logStart = auto.position()
    
    
    startTemp = input('What is the starting temperature?: '.center(80)) or 80
    tempIncriment = input('What is the temperature incriment?: '.center(80)) or 10
    numIncriments = input('How many temperature points do you want to record?:'.center(80)) or 1
    print('Please enter the file path for the temperature logs.'.center(79), 'Hit enter for default:'.center(80))
    tempFiles = input() or 'c:\\users\\jmajor\\desktop\\new'
    
    #creates a class to be used for each step of the SSTDR program
    class automate:
        
                location = 0 #stores location for movement function
                duration = .2 #the duration in seconds for the mouse to move locations
                message = 'print' #the default message for the type function
                move = 0     #uses the move function when value is changed to 1
                click = 0    #uses the click function when value is changed to 1
                doubleclick = 0    #uses the click function when value is changed to 1
                dateTime = 0
                pri = 0      #uses the print function when value is changed to 1
                enter = 0    #uses the enter function when the value is changed to 1 
                ctrlA = 0
                ctrlC = 0
                ctrlV = 0
                progPause = 0
                sleeper = 1
                MHz = 1
                
                #this definition contains all the functions 
                def doStuff(self):
                    if self.move == 1:
                        auto.moveTo(self.location, duration = self.duration) 
                        auto.click()
                        
                    elif self.doubleclick == 1:
                        auto.moveTo(self.location, duration = self.duration)
                        auto.click(clicks=2)
                        
                    elif self.pri == 1:
                        auto.typewrite(self.message, interval = .1)
                        print(self.message)
                        
                    elif self.dateTime == 1:
                        fileDate = datetime.datetime.now().strftime("%Y-%m-%d")
                        auto.typewrite('%s__%s_degC_%sMHz' %(fileDate,temp, self.MHz), interval = .05) #writes file with date, time, and temperature the test was run at
                            
                    elif self.enter == 1:
                        auto.hotkey('enter')
                        
                    elif self.ctrlA == 1:
                        auto.hotkey('ctrl', 'a')
                        
                    elif self.ctrlC == 1:
                        auto.hotkey('ctrl', 'c')
                        
                    elif self.ctrlV == 1:
                        auto.hotkey('ctrl', 'v')
                        
                    elif self.progPause == 1:
                        time.sleep(int(self.sleeper))
                        
    def measureTemp():
        #Starts and ends temperature logging
        auto.moveTo(logStart, duration = 2)
        auto.click(logStart,)
        auto.moveRel(110,0, duration = 2)
        auto.click()
        
        #This lists all the files within a directory
        fileList = (glob.glob(tempFiles + '\*.log'))
        lastFileNum = len(fileList) - 1
        #print(fileList[lastFileNum]) #Used for debugging
        
        #This reads the temp log and analizes the data
        data = pd.read_table(fileList[lastFileNum] , skiprows = 6)
        last = float(data.Temp.tail(1))
        print("Last temp: ",last)
        print("Rounded last temp: ", round(last))
        print("Set temp: ",temp, "\n")
        
        
        #Deletes the temp file so the folder doesn't fill up
        os.remove(fileList[0])

        return last
        
                        
                        
    #this variable will contain all the step objects    
    step = []        
    rs = 0 #used to run saved steps
    #This loop alows the user to enter multiple steps
    while True:
            
            step.append(automate()) #creates a new object for each step at the begining of the loop
            
            x = input('\nWhat would you like to do with this step: \n1 = Move to and click a location, \n2 = Move to and double click a location, \n3 = Prints a file name with the date, \n4 = ctrl a,\n5 = Pause, \ns = Save steps, \nrs = Run saved steps, \nr = Run steps\n')
            
            
            #this if block changes the variables in the object to determin which function is run
            if x == '1':
                step[len(step) - 1].location = auto.position()
                step[len(step) - 1].move = 1
                print(step[len(step) - 1].location)
            
#            elif x == '2': 
#                step[len(step) -1].message = input('Enter a message to print: ')
#                step[len(step) - 1].pri = 1
            
#            elif x == '3': 
#                step[len(step) - 1].enter = 1
                     
            elif x == '2': 
                step[len(step) - 1].location = auto.position()
                step[len(step) - 1].doubleclick = 1
                     
            elif x == '3': 
                step[len(step) - 1].MHz = input('Enter the step frequency')
                
                step[len(step) - 1].dateTime = 1

            elif x == '4': 
                step[len(step) - 1].ctrlA = 1

#            elif x == '7': 
#                step[len(step) - 1].ctrlC = 1
#
#            elif x == '8': 
#                step[len(step) - 1].ctrlV = 1
                     
            elif x == '5': 
                step[len(step) - 1].progPause = 1
                step[len(step) - 1].sleeper = input('Enter the amount of time to pause: ')
                
            elif x == 's':
                with open('company_data.pkl', 'wb') as output:
                    for g in range(len(step)-1):
                        pickle.dump(step[g], output, pickle.HIGHEST_PROTOCOL)
                
            elif x == 'rs':
                rs = 1
                break
            
            #breaks the loop when the user wants to run the steps         
            elif x == 'r':
                break
        
            else:
                print('\n\n**Please select a valid option**\n\n')
############################################################################end
    
    
    
    
    
    
    temp = int(startTemp) 
    endloop = 0 #argument for ending the loop 
    
    input('\nHit enter to start the program\n')
    
#    if rs !=1:        
#        l = input('How many times would you like these steps to run?\n') or '1'
    
    while True and rs != 1:
         
        
        last = measureTemp()
        
        #checks if the last recorded temperature equals the set point
        if round(last) >= temp -1 and round(last) <= temp + 1: #Use the >= and <= to set temperature range
        
            #runs each of the SSTDR program steps
            ##################################################################start
            for i in range(int(len(step) - 1)): #this loop call each step object sequentially
                step[i].doStuff() 
            ####################################################################end
            
            
               
                
            print('\nSSTDR program run at %s degrees' %temp)
            
            temp += int(tempIncriment) #incriments the set temperature
            
            endloop += 1 #incriments the endloop argument
            
        if endloop == int(numIncriments): #how many incriemtns of 25 degreees to do
            break
        
    while True and rs == 1:
         
        last = measureTemp()
    
        
        #checks if the last recorded temperature equals the set point
        if round(last) >= temp -1 and round(last) <= temp + 1: #Use the >= and <= to set temperature range

            #Runs steps from saved file in the same directory
            ##################################################################
            stepsFromSaved = []
            b = 0
            with open('company_data.pkl', 'rb') as i:
                while True:
                            
                    stepsFromSaved.append(None)
                    try:
                           stepsFromSaved[b] = pickle.load(i)
                    except EOFError:
                        break
                    b += 1
                            
                for g in range(len(stepsFromSaved) - 1):
                        stepsFromSaved[g].doStuff()
            ###################################################################    
            print('\nSSTDR program run at %s degrees' %temp)
            
            temp += int(tempIncriment) #incriments the set temperature
            
            endloop += 1 #incriments the endloop argument
            
        if endloop == int(numIncriments): #how many incriemtns of 25 degreees to do
            break
        
    endProgram = input('\nWould you like to run the program again? y\\n: '.center(40))
    if endProgram == 'n':
        break
print('\nEnd of program')     
    
