import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
DC_PIN = 23
RES_PIN = 24
CS_PIN = 25

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 8000000

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DC_PIN, GPIO.OUT)
GPIO.setup(RES_PIN, GPIO.OUT)
GPIO.setup(CS_PIN, GPIO.OUT)

# Reset the display
def reset_display():
    GPIO.output(RES_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RES_PIN, GPIO.HIGH)
    time.sleep(0.1)

# Send command to the display
def send_command(command):
    GPIO.output(DC_PIN, GPIO.LOW)
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.xfer2(command)
    GPIO.output(CS_PIN, GPIO.HIGH)

# Send data to the display
def send_data(data):
    GPIO.output(DC_PIN, GPIO.HIGH)
    GPIO.output(CS_PIN, GPIO.LOW)
    spi.xfer2(data)
    GPIO.output(CS_PIN, GPIO.HIGH)

# Initialize the display
def init_display():
    reset_display()
    send_command([0x01])  # Software reset
    time.sleep(0.12)
    send_command([0x11])  # Sleep out
    time.sleep(0.12)
    send_command([0x3A, 0x05])  # Interface pixel format
    send_command([0x21])  # Inversion on
    send_command([0x29])  # Display on

# Main function
def main():
    init_display()
    # Fill the screen with a color (e.g., red)
    for _ in range(240 * 240):
        send_data([0xFF, 0x00, 0x00])  # Red color in RGB565 format

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        spi.close()
        GPIO.cleanup()
