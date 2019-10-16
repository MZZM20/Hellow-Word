import RPi.GPIO as GPIO
import time

relayPin = [11, 18]

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(relayPin, GPIO.OUT)
    # GPIO.output(relayPin, GPIO.HIGH)

def loop():
    GPIO.output(relayPin, GPIO.HIGH)
    # GPIO.output(relayPin[1], GPIO.HIGH)
    #time.sleep(2)

def destroy():
    GPIO.output(relayPin, GPIO.HIGH)
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    loop()
    destroy()
