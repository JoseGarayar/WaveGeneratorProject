
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
ax = plt.axes(ylim=(0, 80))
line, = ax.plot([],[],lw=2) 

def formato_excel(t, x, yMAX,yMIN):
    ##file = open("/home/pi/data_log.csv", "a")
    #ubicacion = ''
    nombre_csv = 'data_wave '
    datetime = time.strftime("%d-%b-%Y %I:%M:%S%p")
    formato='.csv'
    file = open(nombre_csv+datetime+formato, "w")
    ##if os.stat("/home/pi/data_log.csv").st_size == 0:
    i = 0
    file.write("Time,level\n")
    for i in range(len(t)):
        file.write(str(t[i])+","+str(x[i])+"\n")
        file.flush()
    file.write("/////////////////,/////////////////"+"\n")
    file.write("Max:,"+str(yMAX)+"\n")
    file.write("Min:,"+str(yMIN)+"\n")
    file.write("Altura de la ola:,"+str(Height)+"\n")
    file.write("Periodo:,"+str(Period)+"\n")
    file.write("Frecuencia:,"+str(Hz)+"\n")
    
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

def Max_Min(t,y):
    global Height,Period,Hz
    Max = y.index(max(y))	
    Min = y.index(min(y))
    
    print "Maximo: ", y[Max] , "Minimo: " , y[Min]
    Height = y[Max] - y[Min]
    print "Altura de la ola: " , Height
    tiempo = t[Max]
    k = 0
    while True:
        if y[Max + k] - y[Max + k + 1] < 0:
            tiempo2 = t[Max + k]
            break
        k += 1
    print "tiempo2: ", tiempo2 , " Tiempo : ", tiempo
    Period = (tiempo2 - tiempo)*2
    Hz = 1/Period
    print "Periodo: " , Period
    print "Frecuencia: " , Hz

    return y[Max],y[Min]

def PlotData(t,y):
    ax.set_title('PlotData')
    ax.set_xlabel('Tiempo (s)')
    ax.set_ylabel('Distancia (cm)')
    ax.grid(True)
    ax.plot(t,y)
    plt.show()

    
    
if __name__ == "__main__":
    tmax = float(raw_input('Cuantos segundos debe medir el programa? '))
    t0_0=time.time()
    j = 0
    while True:
        j += 1
        dist = distance()
        print dist[0], "   ", dist[1]
        y_data.append(dist[1])
        t_data.append(dist[0])
        #time.sleep(0.05)
        if dist[0] > tmax:
            break

    [yMAX,yMIN] = Max_Min(t_data,y_data)

    formato_excel(y_data, t_data, yMAX, yMIN)
    
    PlotData(t_data,y_data)
    
    
