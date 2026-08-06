import time
import board
import digitalio
import neopixel
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# --- Configuration Setup ---
# Initialize the 3 NeoPixel LEDs chained on Pin D0
NUM_PIXELS = 3
pixels = neopixel.NeoPixel(board.D0, NUM_PIXELS, brightness=0.2, auto_write=True)

# Initialize the computer media control link
cc = ConsumerControl()

# Define button pins based on your KiCad schematic (Pins D1, D2, D3)
button_pins = [board.D1, board.D2, board.D3]
buttons = []

# Configure buttons with internal Pull-Up resistors (for Ground connections)
for pin in button_pins:
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    buttons.append(btn)

# Define what each physical key does
KEY_COMMANDS = [
    ConsumerControlCode.VOLUME_DECREMENT,  # Key 1: Lower volume
    ConsumerControlCode.PLAY_PAUSE,        # Key 2: Play or Pause media
    ConsumerControlCode.VOLUME_INCREMENT   # Key 3: Raise volume
]

# Define standby indicator colors for the LEDs (Red, Green, Blue)
STANDBY_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255)     # Blue
]

# Flash effect color when a button gets pressed
PRESS_COLOR = (255, 255, 255) # Bright White

# Set initial LED colors
for i in range(NUM_PIXELS):
    pixels[i] = STANDBY_COLORS[i]

# --- Main Program Loop ---
while True:
    for i in range(3):
        # Because we used a Pull-Up connection to ground, "False" means pressed!
        if not buttons[i].value:
            # 1. Turn the LED white to show it registered the click
            pixels[i] = PRESS_COLOR
            
            # 2. Execute the media command to your computer
            cc.send(KEY_COMMANDS[i])
            
            # 3. Wait a tiny moment to prevent double-clicking ghost taps
            time.sleep(0.2)
            
            # 4. Return the LED back to its original standby color
            pixels[i] = STANDBY_COLORS[i]
            
    time.sleep(0.01) # Tiny delay to keep the processor running smoothly
