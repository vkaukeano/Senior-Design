import time
import os
import RPi.GPIO as GPIO
import math
GPIO.setmode(GPIO.BOARD)
##For Line Following
LOGGER = 1
Lpin = 3
Rpin =  5
TRIG = 35
ECHO = 37
L = 60
k = .1
Xo = 35
GPIO.setwarnings(False)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(Lpin, GPIO.IN)
GPIO.setup(Rpin, GPIO.IN)
current_speed = 0
current_speed2 = 0

##For PWM
RW_PIN = 18;
LW_PIN = 13;
RW_ENA = 16;
LW_ENA = 11;
GPIO.setup(RW_PIN,GPIO.OUT) # Right Wheel 
GPIO.setup(RW_ENA,GPIO.OUT) # Right Wheel 
GPIO.output(RW_ENA, 1)
GPIO.setup(LW_PIN,GPIO.OUT) # Left Wheel
GPIO.setup(LW_ENA,GPIO.OUT) # Left Wheel
GPIO.output(LW_ENA, 1)

#initialize PWM 
r = GPIO.PWM(RW_PIN,50) # Arguments are pin and frequency
r.start(0) # Argument is initial duty cycle, it should be 0
l = GPIO.PWM(LW_PIN,50) # Arguments are pin and frequency
l.start(0) # Argument is initial duty cycle, it should be 0


pulse_start = 0
while True:
	GPIO.output(TRIG, False)
	time.sleep(.5)  # Should be 2 seconds? Inside or outside Loop? ##
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	while GPIO.input(ECHO) == 0:  # FIX THIS ###
		pulse_start = time.time()
	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17150
		distance = round(distance, 20)

#		print("DISTANCE", distance)

		duty = distance / .5
		
	
		if(duty > 60):
			duty = 60
		if(duty < 0):
			duty = 0

	if (current_speed >= duty):
		for i in range(int(duty),int(current_speed),1):
			current_speed -= 1
			exp = math.exp(-k * (current_speed - Xo))
			current_speed2 = (L / (1 + exp))
#		if(current_speed > 60):
#			current_speed = 60
			if(current_speed2 < 10):
				r.ChangeDutyCycle(0)
				l.ChangeDutyCycle(0)		
			if(current_speed2 > 10):
				r.ChangeDutyCycle(current_speed2)
				l.ChangeDutyCycle(current_speed2)
			time.sleep(.01)


	if (current_speed <= duty):
		for i in range(int(current_speed),int(duty),1):
			print current_speed
			current_speed += 1
			exp = math.exp(-k * (current_speed - Xo))
			current_speed2 = (L / (1 + exp))
#		if(current_speed > 60):
#			current_speed = 60
#		if(current_speed < 0):
#			current_speed = 0
			r.ChangeDutyCycle(current_speed2)
			l.ChangeDutyCycle(current_speed2)
		print current_speed2

	if (GPIO.input(Lpin) == True):
		print('STOP LEFT WHEEL!!!')
		r.ChangeDutyCycle(0)
		#time.sleep(.25)
	else:
		r.ChangeDutyCycle(current_speed2)

	if (GPIO.input(Rpin) == True):
		print('STOP RIGHT WHEEL!!!')
		l.ChangeDutyCycle(0)
		#time.sleep(.25)
	else:
		l.ChangeDutyCycle(current_speed2)
		time.sleep(.01)

	current_speed = duty
#	time.sleep(1)
#try:
 #   while True:  # create an infinte loop to keep the script running
  #      time.sleep(.001)
   #     global distance
    #    print "Distance ", distance
     #   avg = 0
#except KeyboardInterrupt:
   # print "  Quit"
    #GPIO.cleanup()
