import RPi.GPIO as GPIO
import time

# System to handle communication between a Z80 CPU 
# and memory emulated on an ESP32 (which does not
# have enough pins on its own)

# pin setup
_WAIT = 4       # OUT
_BUSREQ = 17    # OUT
_RESET = 27     # OUT
CLK = 22        # OUT
_NMI = 10       # OUT
_INT = 9        # OUT
ENCODER_A = 11  # OUT
_IORQ = 14      # IN
_MREQ = 15      # IN   
_HALT = 18      # IN
_RD = 23        # IN
_WR = 24        # IN
_BUSACK = 25    # IN
_M1 = 8         # IN
_RFSH = 7       # IN
ENCODER_B = 12  # OUT

# Z80 clock in Hz
FREQ = 1
HALF_PERIOD = 1 / (2 * FREQ)
# because there are not enough pins on the ESP32, 
# it needs to synchronize with the RPi to fully
# communicate with the Z80
MEMORY_POLLING_RATE = FREQ * 4
PAYLOAD_SIZE = 24

# synchronizes the ESP32 with the RPi through a serial connection
def synchronize_esp32():
    GPIO.setup(ENCODER_A, GPIO.OUT)
    GPIO.setup(ENCODER_B, GPIO.IN)
    GPIO.output(ENCODER_A, 1)
    # wait for ESP32 to signal that it is on
    while GPIO.input(ENCODER_B) < 1:
        pass
    GPIO.output(ENCODER_A, 0)
    time.sleep(0.01)
    # start the serial transfer of the required clock speed
    binary_rate = bin(MEMORY_POLLING_RATE)[2:].zfill(24)
    for b in binary_rate:
        GPIO.output(ENCODER_A, b)
        # wait for confirmation
        while GPIO.input(ENCODER_B) < 1:
            pass
        time.sleep(0.01)
    print(f'Communicating with ESP32 at {MEMORY_POLLING_RATE} Hz.')

# synchronize now before reconfiguring the pins
synchronize_esp32()

# GPIO setup
GPIO.setmode(GPIO.BCM) # broadcom
# outputs
GPIO.setup(_WAIT, GPIO.OUT)
GPIO.setup(_BUSREQ, GPIO.OUT)
GPIO.setup(_RESET, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(_NMI, GPIO.OUT)
GPIO.setup(_INT, GPIO.OUT)
GPIO.setup(ENCODER_A, GPIO.OUT)
GPIO.setup(ENCODER_B, GPIO.OUT)
# make sure pins are low
GPIO.output(_WAIT, 0)
GPIO.output(_BUSREQ, 0)
GPIO.output(_RESET, 0)
GPIO.output(CLK, 0)
GPIO.output(_NMI, 0)
GPIO.output(_INT, 0)
GPIO.output(ENCODER_A, 0)
GPIO.output(ENCODER_B, 0)
# inputs
GPIO.setup(_IORQ, GPIO.IN)
GPIO.setup(_MREQ, GPIO.IN)
GPIO.setup(_HALT, GPIO.IN)
GPIO.setup(_RD, GPIO.IN)
GPIO.setup(_WR, GPIO.IN)
GPIO.setup(_BUSACK, GPIO.IN)
GPIO.setup(_M1, GPIO.IN)
GPIO.setup(_RFSH, GPIO.IN)

# takes in op code from interrupts eg. and encodes it into 
# two successive 2 bit combinations to pass values 0-15
# into the 2 remaining pins on the ESP32 in big endian
def mem_ins_encoder(val):
    val = bin(val)[2:]
    GPIO.output(ENCODER_A, val[0])
    GPIO.output(ENCODER_B, val[1])
    time.sleep(1 / MEMORY_POLLING_RATE)
    GPIO.output(ENCODER_A, val[2])
    GPIO.output(ENCODER_B, val[3])
    time.sleep(1 / MEMORY_POLLING_RATE)
    GPIO.output(ENCODER_A, 0)
    GPIO.output(ENCODER_B, 0)

# set up the interrupts for the Z80 memory controls
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_IORQ), lambda: mem_ins_encoder(1), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_MREQ), lambda: mem_ins_encoder(2), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_HALT), lambda: mem_ins_encoder(3), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_RD), lambda: mem_ins_encoder(4), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_WR), lambda: mem_ins_encoder(5), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_BUSACK), lambda: mem_ins_encoder(6), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_M1), lambda: mem_ins_encoder(7), GPIO.FALLING)
GPIO.attachInterrupt(GPIO.digitalPinToInterrupt(_RFSH), lambda: mem_ins_encoder(8), GPIO.FALLING)

def tick_clock():
    GPIO.output(CLK, 1)
    time.sleep(HALF_PERIOD / 1.1)
    GPIO.output(CLK, 0)
    time.sleep(HALF_PERIOD / 1.1)

# startup
try:
    last_time = time.time()
    while True:
        current_time = time.time()
        deltatime = current_time - last_time

        if deltatime >= HALF_PERIOD:
            tick_clock()

            last_time = current_time
            sleep_time = max(0, HALF_PERIOD - (time.time() - current_time))
            time.sleep(sleep_time)

        

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up on CTRL+C exit
