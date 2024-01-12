import RPi.GPIO as GPIO
import time

# pin setup
_WAIT = 4       # OUT
_BUSREQ = 17    # OUT
_RESET = 27     # OUT
CLK = 22        # OUT
_NMI = 10       # OUT
_INT = 9        # OUT
CUT = 11       # OUT
_IORQ = 14      # IN
_MREQ = 15      # IN   
_HALT = 18      # IN
_RD = 23        # IN
_WR = 24        # IN
_BUSACK = 25    # IN
_M1 = 8         # IN
_RFSH = 7       # IN
SOUT = 12       # OUT

# z80 clock in Hz
FREQ = 1
HALF_PERIOD = 1 / (2 * FREQ)
# serial clock factor for memory != 0
SERIAL_STEPS = 10

# GPIO setup
GPIO.setmode(GPIO.BCM) # broadcom

GPIO.setup(_WAIT, GPIO.OUT)
GPIO.setup(_BUSREQ, GPIO.OUT)
GPIO.setup(_RESET, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(_NMI, GPIO.OUT)
GPIO.setup(_INT, GPIO.OUT)
GPIO.setup(CUT, GPIO.OUT)
GPIO.setup(SOUT, GPIO.OUT)

GPIO.output(_WAIT, GPIO.LOW)
GPIO.output(_BUSREQ, GPIO.LOW)
GPIO.output(_RESET, GPIO.LOW)
GPIO.output(CLK, GPIO.LOW)
GPIO.output(_NMI, GPIO.LOW)
GPIO.output(_INT, GPIO.LOW)
GPIO.output(CUT, GPIO.LOW)
GPIO.output(SOUT, GPIO.LOW)

GPIO.setup(_IORQ, GPIO.IN)
GPIO.setup(_MREQ, GPIO.IN)
GPIO.setup(_HALT, GPIO.IN)
GPIO.setup(_RD, GPIO.IN)
GPIO.setup(_WR, GPIO.IN)
GPIO.setup(_BUSACK, GPIO.IN)
GPIO.setup(_M1, GPIO.IN)
GPIO.setup(_RFSH, GPIO.IN)

def mem_double_mux(val):
    for i in range(val):
        GPIO.output(SOUT, GPIO.HIGH)
        time.sleep(HALF_PERIOD / SERIAL_STEPS)
        GPIO.output(SOUT, GPIO.LOW)
        time.sleep(HALF_PERIOD / SERIAL_STEPS)
    GPIO.output(CUT, GPIO.HIGH)


def onIORQ():
    pass

def onMREQ():
    pass

def onHALT():
    pass

def onRD():
    pass

def onWR():
    pass

def onBUSACK():
    pass

def onM1():
    pass

def onRFSH():
    pass

GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_IORQ), onIORQ, GPIO.FALLING);      
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_MREQ), onMREQ, GPIO.FALLING);      
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_HALT), onHALT, GPIO.FALLING);      
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_RD), onRD, GPIO.FALLING);          
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_WR), onWR, GPIO.FALLING);          
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_BUSACK), onBUSACK, GPIO.FALLING);  
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_M1), onM1, GPIO.FALLING);          
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_RFSH), onRFSH, GPIO.FALLING); 



# startup
try:
    while True:


        # Set GPIO HIGH
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(7, GPIO.LOW)
        time.sleep(HALF_PERIOD)

        # Set GPIO LOW
        GPIO.output(22, GPIO.LOW)
        GPIO.output(7, GPIO.HIGH)
        time.sleep(HALF_PERIOD)

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up on CTRL+C exit
