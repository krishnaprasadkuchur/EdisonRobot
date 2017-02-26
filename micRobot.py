from __future__ import print_function
from upm import pyupm_mic as upmMicrophone
import time, sys, signal, atexit
from upm import pyupm_adafruitms1438 as upmAdafruitms1438

def main():
    # Import header values
    I2CBus = upmAdafruitms1438.ADAFRUITMS1438_I2C_BUS
    I2CAddr = upmAdafruitms1438.ADAFRUITMS1438_DEFAULT_I2C_ADDR

    M1Motor = upmAdafruitms1438.AdafruitMS1438.MOTOR_M1
    MotorDirCW = upmAdafruitms1438.AdafruitMS1438.DIR_CW
    MotorDirCCW = upmAdafruitms1438.AdafruitMS1438.DIR_CCW
    
    # Attach microphone to analog port A2
    myMic = upmMicrophone.Microphone(2)
    threshContext = upmMicrophone.thresholdContext()
    threshContext.averageReading = 0
    threshContext.runningAverage = 0
    threshContext.averagedOver = 2
    
    # Instantiate an Adafruit MS 1438 on I2C bus 0
    myMotorShield = upmAdafruitms1438.AdafruitMS1438(I2CBus, I2CAddr)

    ## Exit handlers ##
    # This stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit,
    # including functions from myMotorShield
    def exitHandler():
        myMotorShield.disableMotor(M1Motor)
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    # Setup for use with a DC motor connected to the M3 port

    # set a PWM period of 50Hz
    myMotorShield.setPWMPeriod(50)

    # disable first, to be safe
    myMotorShield.disableMotor(M1Motor)

    # set speed at 50%
    myMotorShield.setMotorSpeed(M1Motor, 50)
    myMotorShield.setMotorDirection(M1Motor, MotorDirCW)

    print ("Reverse wheel direction with sound")
    rotFlag = False
    while(1):
        buffer = upmMicrophone.uint16Array(8)
        len = myMic.getSampledWindow(2, 8, buffer);
        if len:
            thresh = myMic.findThreshold(threshContext, 800, buffer, len)
            if(thresh):
                print("Threshold is ", thresh)
                myMic.printGraph(threshContext)
                myMotorShield.enableMotor(M1Motor)
                if (rotFlag):
                    rotFlag = False
                    myMotorShield.setMotorDirection(M1Motor, MotorDirCW)
                    continue
                else:
                    rotFlag = True
                    myMotorShield.setMotorDirection(M1Motor, MotorDirCCW)
                    continue
        time.sleep(3)
        myMotorShield.disableMotor(M1Motor)
    # Delete the upmMicrophone object
    del myMic
    
    print("Stopping M1")

    # exitHandler runs automatically

if __name__ == '__main__':
    main()
