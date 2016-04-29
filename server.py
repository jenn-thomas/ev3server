import threading
import thread
import webbrowser
import BaseHTTPServer
import SimpleHTTPServer
import time
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir,sep,listdir
import os,sys
import json

FILE = '/index.html'
PORT = 80

#LED path
ledpath = '/sys/class/leds/ev3-{}:{}:ev3dev/'
ledbright = ledpath +'brightness'

#motor definitions
motorAttached = '/sys/class/tacho-motor/'
motorpath = '/sys/class/tacho-motor/{}/'
setMotorSpeed = motorpath + 'duty_cycle_sp'
runMotor = motorpath + 'command'
# check if this is true 
checkMotorPort = motorpath + 'address' 

#sensor definitions
sensorpath = '/sys/class/lego-sensor/{}/'
sensorValue = sensorpath + 'value0'
sensorAttached = '/sys/class/lego-sensor/'
checkSensorPort = sensorpath + 'port_name'
drivername = sensorpath + 'driver_name'

class TestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """The test example handler."""

    def do_POST(self):
        """Handle a post request by returning the square of the number."""
        length = int(self.headers.getheader('content-length')) 
        otype=self.headers.getheader('content-type')
        data_string = self.rfile.read(length)
        data=json.loads(data_string)
        print length
        print data_string
        print otype
        if data['device']=='led':
            data1=data['led1']
            data2=data['led2']
            data3=data['led3']
            data4=data['led4']
            LED = open(ledbright.format('right0','red'),"w",0)
            LED.write(data1 + '\n')
            LED.close
            LED = open(ledbright.format('left0','red'),"w",0)
            LED.write(data2 + '\n')
            LED.close
            LED = open(ledbright.format('right1','green'),"w",0)
            LED.write(data3 + '\n')
            LED.close
            LED = open(ledbright.format('left1','green'),"w",0)
            LED.write(data4 + '\n')
            LED.close

        elif data['device']=='motor':
            # motor dictionary {'actual Ev3 port':'motor0'}
            #speedArray=[data['motor0'],data['motor1'],data['motor2'],data['motor3']]
            #print speedArray
            existingMotors = os.listdir(motorAttached)
            print existingMotors
            print len(existingMotors)
            MOTORS = {} # reset/create dictionary
                        
            for i in range(0,len(existingMotors)):
                try:
                    motorRead = open(checkMotorPort.format(existingMotors[i])) 
                    print motorRead
                    mo = motorRead.read()
                    print mo
                    motorRead.close
                    MOTORS[mo[3]] = existingMotors[i] # add to dictionary
                except IOError:
                    print "no motor"
            print MOTORS
            for i in range(0,3):
                port = changePort(i)
                print port                               
                if port in MOTORS: # if motor exists in port 
                    speed = 'Speed{}'.format(i)
                    motor = open(setMotorSpeed.format(MOTORS[port]),"w",0)
                    motor.write(data['motor{}'.format(i)] + '\n')
                    motor.close
                    if data['cmd']=='run':
                        motor = open(runMotor.format(MOTORS[port]),"w",0)
                        motor.write('run-forever')
                    else:# stop motor
                        motor = open(runMotor.format(MOTORS[port]),"w",0)
                        motor.write('stop')
                        motor.close
                        
               
                        

#HOW DO WE MAKE THIS CONTINUOUS?
#HOW DO WE MAKE THIS FOR MULTIPLE SENSOR READINGS? create then print and array of strings? 
        elif data['device'] =='sensor':
            # sensor dictionary {'actual Ev3 port':'sensor0'}
            existingSensors = os.listdir(sensorAttached)
            print existingSensors
            print len(existingSensors)

            SENSORS = {} # reset dictionary

            for i in range(0,len(existingSensors)):
                try:
                    senRead = open(checkSensorPort.format(existingSensors[i])) 
                    print senRead
                    mo = senRead.read()
                    print mo
                    senRead.close
                    SENSORS[mo[2]] = existingSensors[i] # add to dictionary
                except IOError:
                    print "no sensor"
            print SENSORS

            data = {}; # dictionary containing all available sensor measurements
            
            for i in SENSORS:
                # read sensor value
                Sens = open(sensorValue.format(SENSORS[i]))
                theValue = Sens.read()
                Sens.close
                print theValue

                # ask what sensor is plugged in - theSensor
                # FIX THIS PERMISSION DENIED (ERROR 13) sometimes
                sensor = open(drivername.format(SENSORS[i]))
                print sensor
                theSensor = sensor.read()
                sensor.close
                print theSensor
                print type(theSensor)
                print len(theSensor)
                data[senNameChange(theSensor)] = theValue

    # send back sensor values to appropriate space on webpage                 
        self.send_response(200)
        self.end_headers()
        data['success']='Operation Successful'
        print type(data)
        data = json.dumps(data)
        print data
        self.wfile.write(data)
        
def changePort(portNum):
        if portNum in range(0,3):
                if portNum == 0:
                        value = 'A'
                elif portNum == 1:
                        value = 'B'
                elif portNum == 2:
                        value = 'C'
                elif portNum == 3:
                        value = 'D'
                else:
                        value = ''
                return value
            
def WebServerThread():                  
        try:
                #Create a web server and define the handler to manage the
                #incoming request
                server_address = ("", PORT)
                server = BaseHTTPServer.HTTPServer(server_address, TestHandler)
                print 'Started httpserver on port ' , PORT
                
                #Wait forever for incoming htto requests
                server.serve_forever()

        except KeyboardInterrupt:
                print '^C received, shutting down the web server'
                server.socket.close()
                

def senNameChange(name):
    print name 
    print type(name)
    # returns [sensor name, units]
    # ultrasonic sensor
    #print (name == s)
    if name.find('lego-ev3-us') == 0:
        return 'ultrasonic sensor'
                    
    # gyro sensor   
    elif name.find('lego-ev3-gyro')==0:
        return 'gyro sensor'
                                    
    # touch sensor 
    elif name.find('lego-ev3-touch')==0:
        return 'touch sensor'
                                   
    # ir sensor 
    elif name.find('lego-ev3-ir')==0:
        return 'IR sensor'
                                                 
     # color sensor
    elif name.find('lego-ev3-color')==0:
        return 'color sensor'
    
    # unknown sensor
    else:
        return 'unknown sensor'
    

def units(sensorName):
    if name == 'ultrasonic sensor':
        return 'cm'
                    
    # gyro sensor   
    elif name == 'gyro sensor':
        return 'degrees'
                                    
    # touch sensor 
    elif name == 'touch sensor':
        return ''
                                   
    # ir sensor 
    elif name == 'IR sensor':
        return 'percent'
                                                 
     # color sensor
    elif name == 'color sensor':
        return 'percent'
    
    # unknown sensor
    else:
        return ''


if __name__ == "__main__":
    WebServerThread()
'''
while True:
        time.sleep(0.5)
   
   
'''
