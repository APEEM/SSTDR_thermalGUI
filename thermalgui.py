#imports modules
import pandas as pd
import pyautogui as auto
import glob
import datetime
import clipboard

#allows for a failsafe to break the program
auto.PAUSE = 1
auto.FAILSAFE = True

while True:
    #sets all the parameters for the program loop
    ##########################################################################start
    
    #set temperature logging start button position
    print('  Welcome to thermalGUI for the SSTDR program automation.  '.center(240,'#'))
    input('Place the mouse over the start button and hit enter.'.center(80))
    logStart = auto.position()
    
    
    startTemp = input('What is the starting temperature?: '.center(80)) or 80
    tempIncriment = input('What is the temperature incriment?: '.center(80)) or 10
    numIncriments = input('How many temperature points do you want to record?:'.center(80)) or 1
    
    
    #creates a class to be used for each step of the SSTDR program
    class automate:
        
                location = 0 #stores location for movement function
                duration = 1 #the duration in seconds for the mouse to move locations
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
                
                #this definition contains all the functions 
                def doStuff(self):
                    if self.move == 1:
                        auto.moveTo(self.location, duration = self.duration) 
                        auto.click()
                        
                    elif self.doubleclick == 1:
                        auto.click(clicks=2)
                        
                    elif self.pri == 1:
                        auto.typewrite(self.message, interval = .1)
                        print(self.message)
                        
                    elif self.dateTime == 1:
                        fileDate = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        auto.typewrite('file_%s degrees_%s' %(temp,fileDate), interval = .1) #writes file with date, time, and temperature the test was run at
                            
                    elif self.enter == 1:
                        auto.hotkey('enter')
                        
                    elif self.ctrlA == 1:
                        auto.hotkey('ctrl', 'a')
                        
                    elif self.ctrlC == 1:
                        auto.hotkey('ctrl', 'c')
                        
                    elif self.ctrlV == 1:
                        auto.hotkey('ctrl', 'v')
                        
    
    #this variable will contain all the step objects    
    step = []        
                
    #This loop alows the user to enter multiple steps
    while True:
            
            step.append(automate()) #creates a new object for each step at the begining of the loop
            
            x = input('\nWhat would you like to do with this step: \n1=set location and click, \n2=type a message, \n3=hit enter, \n4=double click, \n5=prints a file name with the date and time, \n6=ctrlA, \n7=ctrlC, \n8=ctrlV, \n9=run steps\n')
            
            
            #this if block changes the variables in the object to determin which function is run
            if x == '1':
                step[len(step) - 1].location = auto.position()
                step[len(step) - 1].move = 1
                print(step[len(step) - 1].location)
            
            elif x == '2': 
                step[len(step) -1].message = input('Enter a message to print: ')
                step[len(step) - 1].pri = 1
            
            elif x == '3': 
                step[len(step) - 1].enter = 1
                     
            elif x == '4': 
                step[len(step) - 1].doubleclick = 1
                     
            elif x == '5': 
                step[len(step) - 1].dateTime = 1

            elif x == '6': 
                step[len(step) - 1].ctrlA = 1

            elif x == '7': 
                step[len(step) - 1].ctrlC = 1

            elif x == '8': 
                step[len(step) - 1].ctrlV = 1
            
            #breaks the loop when the user wants to run the steps         
            elif x == '9':
                break
        
            else:
                print('\n\n**Please select a valid option**\n\n')
############################################################################end
    
    
    
    
    
    
    temp = int(startTemp) 
    endloop = 0 #argument for ending the loop 
    
    input('\nHit enter to start the program\n')
    
    #locates the temperature log file directory and automatically sets glob to read from it
    x = auto.locateCenterOnScreen('directory.png')
    auto.moveTo(x, duration = 1)
    auto.moveRel(0, 45, duration = 1)
    auto.click(clicks=2)
    auto.hotkey('ctrl', 'a')
    auto.hotkey('ctrl', 'c')
    tempFiles = clipboard.paste()
    
    while True:
         
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
        
        
    endProgram = input('\nWould you like to run the program again? y\\n: '.center(40))
    if endProgram == 'n':
        break
print('\nEnd of program')     
    