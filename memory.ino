#include <arduino.h>

// Simulated memory module for the Zilog Z80

// 16-bit address bus
#define A0 12
#define A1 14
#define A2 27
#define A3 26
#define A4 25
#define A5 33
#define A6 32
#define A7 35
#define A8 34
#define A9 39
#define A10 36
#define A11 21
#define A12 3
#define A13 1
#define A14 22
#define A15 23

// 8-bit data bus
#define D0 0
#define D1 2
#define D2 16
#define D3 18
#define D4 5
#define D5 19
#define D6 17
#define D7 4

// RPi controller channel A
#define CA 15
// channel B
#define CB 13

#define PAYLOAD_SIZE = 24

void setup() {
    Serial.begin(115200);

    pinMode(CA, INPUT);    
    pinMode(CB, OUTPUT);

    // wait for signal from RPi to begin
    while (true) {
        if (digitalRead(CA) == HIGH) {
            digitalWrite(CB, HIGH);
            delay(5);
            digitalWrite(CB, LOW);
            break;
        }
    }

    // begin reading in required frequency
    String binaryRate = "";
    while (binaryRate.length() < PAYLOAD_SIZE) {
        int bit = digitalRead(CA);
        binaryRate += (bitVal == HIGH ? "1" : "0");  
        // signal to RPi for next value
        digitalWrite(CB, HIGH);
        delay(5);
        digitalWrite(CB, LOW);
    }

    // reconfigure pin for memory controller
    pinMode(CB, INPUT);

    // convert binary polling rate to int
    long pollingRate = strtol(binaryRate.c_str(), NULL, 2);

    Serial.print("Received Polling Rate: ");
    Serial.println(pollingRate);
}

void loop() {
    // Main loop code
}
