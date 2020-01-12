import RPi.GPIO as GPIO
#import scipy.signal as signal
import time
import collections
import numpy as np

np.set_printoptions(threshold = np.inf)

sensor = 32  # define the GPIO pin our sensor is attached to

GPIO.setmode(GPIO.BOARD)  # set GPIO numbering system to BCM
GPIO.setup(sensor, GPIO.IN)  # set our sensor pin to an input

sample = 2  # Number of tick counts between calculations
N_Windows = 1 #N windows per rotation
count = 0
delta = 0 
start = 0
end = 0
rpm = 0
global avg
avg = []


d = collections.deque(maxlen=50)
for i in xrange(50):
	d.append(0)
#h = sg.get_window('triang',3000)

def set_start():
    global start
    start = time.time()


def set_end():
    global end
    end = time.time()


def get_rpm(c):
    global count  # delcear the count variable global so we can edit it
    global avg
    if not count:
        set_start()  # create start time
        count = count + 1  # increase counter by 1
    else:
        count = count + 1

    if count == sample:
        set_end()  # create end time
        delta = end - start  # time taken to do a half rotation in seconds
        delta = delta / 60  # converted to minutes
        rpm = (1 / delta) / (960) #1:120 is the gear ratio
        #print delta
        d.append(rpm)
        avg = np.mean(d)
#        fil = sg.convolve(d,h/h.sum())
 #       print fil[2999] #sum(d)/len(d)
        #time.sleep(.001)
#        output = signal.lfilter(NUM,1,d)
        count = 0  # reset the count to 0






	# execute the get_rpm function when a HIGH signal is detected
GPIO.add_event_detect(sensor, GPIO.RISING, callback=get_rpm)

try:
    while True:  # create an infinte loop to keep the script running
        time.sleep(1)
        global avg
        print "L ", avg
        avg = 0
except KeyboardInterrupt:
    print "  Quit"
    GPIO.cleanup()
