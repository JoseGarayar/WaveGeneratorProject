#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
import RPi.GPIO as GPIO
import os
MAXPTS = 50
trigger = 23
echo = 24
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

yv = []
tv = []
sound_speed = 343000  # cm/s

y_data = []
t_data = []

fig = plt.figure()
ax = plt.axes(xlim=(0,10), ylim=(0, 100))
line, = ax.plot([],[],lw=2) 

def formato_excel(t, x):
    ##file = open("/home/pi/data_log.csv", "a")
    #ubicacion = ''
    nombre_csv = 'data_wave.csv'
    file = open(nombre_csv, "a")
    ##if os.stat("/home/pi/data_log.csv").st_size == 0:
    if os.stat(nombre_csv).st_size == 0:
            #file.write("Time,Sensor1,Sensor2,Sensor3,Sensor4,Sensor5\n")
            file.write("Time,level\n")
    #while i<200:
    else:
        for i in range(len(t)):
        #now = datetime.now()
            file.write(str(t[i])+","+str(x[i])+"\n")
            file.flush()
    file.close()


def distance():
    global tstart
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    t0 = time.time()
    tf = time.time()

    while GPIO.input(echo)==0:
        t0 = time.time()
    while GPIO.input(echo)==1:
        tf = time.time()

    time_elapsed = tf - t0
    d = (time_elapsed*sound_speed)/2
    return [(tf+t0)/2 - t0_0, d/10]

def update(i):
    global tv, yv
    try:
        dist = distance()
        if dist:
            print i, " > ",dist[0], "   ", dist[1]
            yv.append(dist[1])
            tv.append(dist[0])
            y_data.append(dist[1])
            t_data.append(dist[0])
            #formato_excel(dist[0], dist[1])
            if i>MAXPTS:
                yv = yv[-MAXPTS:]
                tv = tv[-MAXPTS:]
                ax.set_xlim(tv[0]-0.05, tv[-1]+0.05)
            line.set_data(tv, yv)
        return line,
    except KeyboardInterrupt:
        GPIO.cleanup()
        print "...Fin"

def main():
    ani = animation.FuncAnimation(fig, update, interval=120, blit=True)
    plt.show()

if __name__ == "__main__":
    t0_0=time.time()
    
    main()
    formato_excel(t_data, y_data)


