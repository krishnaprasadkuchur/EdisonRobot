from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_adafruitms1438 as upmAdafruitms1438

def main():
    # Import header values
    I2CBus = upmAdafruitms1438.ADAFRUITMS1438_I2C_BUS
    I2CAddr = upmAdafruitms1438.ADAFRUITMS1438_DEFAULT_I2C_ADDR

    M1Motor = upmAdafruitms1438.AdafruitMS1438.MOTOR_M1
    M4Motor = upmAdafruitms1438.AdafruitMS1438.MOTOR_M4
    MotorDirCW = upmAdafruitms1438.AdafruitMS1438.DIR_CW
    MotorDirCCW = upmAdafruitms1438.AdafruitMS1438.DIR_CCW

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
        myMotorShield.disableMotor(M4Motor)
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
    myMotorShield.disableMotor(M4Motor)

    # set speed at 50%
    myMotorShield.setMotorSpeed(M1Motor, 90)
    myMotorShield.setMotorSpeed(M4Motor, 90)
    myMotorShield.setMotorDirection(M1Motor, MotorDirCW)
    myMotorShield.setMotorDirection(M4Motor, MotorDirCCW)

    print ("Spin M1 and M4 at half speed for 3 seconds, "
    "then reverse for 3 seconds.")
    myMotorShield.enableMotor(M1Motor)
    myMotorShield.enableMotor(M4Motor)
    while(1):
        time.sleep(3)
        myMotorShield.setMotorDirection(M1Motor, MotorDirCW)
        myMotorShield.setMotorDirection(M4Motor, MotorDirCCW)
        time.sleep(3)
        print("Reversing M1 and M4")
        myMotorShield.setMotorDirection(M1Motor, MotorDirCCW)
        myMotorShield.setMotorDirection(M4Motor, MotorDirCW)

    print("Stopping M1 and M4")

    # exitHandler runs automatically

if __name__ == '__main__':
    main()
