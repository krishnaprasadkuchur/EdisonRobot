import time
from upm import pyupm_mic as upmMicrophone

def main():
    # Attach microphone to analog port A2
    myMic = upmMicrophone.Microphone(2)
    threshContext = upmMicrophone.thresholdContext()
    threshContext.averageReading = 0
    threshContext.runningAverage = 0
    threshContext.averagedOver = 2

    # Infinite loop, ends when script is cancelled
    # Repeatedly, take a sample every 2 microseconds;
    # find the average of 128 samples; and
    # print a running graph of dots as averages
    while(1):
        buffer = upmMicrophone.uint16Array(8)
        len = myMic.getSampledWindow(2, 8, buffer);
        if len:
            thresh = myMic.findThreshold(threshContext, 800, buffer, len)
            if(thresh):
                print("Threshold is ", thresh)
                myMic.printGraph(threshContext)

    # Delete the upmMicrophone object
    del myMic

if __name__ == '__main__':
    main()
