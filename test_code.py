import board
import displayio
import terminalio
from adafruit_display_text import label
import time
import analogio
import gc

import board
import time
import digitalio
import simpleio

from keypad import ShiftRegisterKeys

k = ShiftRegisterKeys(
    clock=board.BUTTON_CLOCK,
    data=board.BUTTON_OUT,
    latch=board.BUTTON_LATCH,
    key_count=8,
    value_when_pressed=True,
)

# Set up the display
display = board.DISPLAY

# Control brightness (0.0 to 1.0)
display.brightness = 0.2  # Reduces to 30% brightness

# Create a display group
main_group = displayio.Group()
display.root_group = main_group

# Create some text
text = label.Label(
    terminalio.FONT,
    text="bat",
    color=0x00bb77,  # White
    x=10,
    y=10
)
text.anchor_point = (0.5, 0.5)  # Center the text
main_group.append(text)

mem_usage = gc.mem_alloc() / (gc.mem_alloc()+gc.mem_free()) * 100

mem = label.Label(
    terminalio.FONT,
    text="mem: {:.2f}%".format(mem_usage),
    color=0x00bb77,  # White
    x=10,
    y=20
)
mem.anchor_point = (0.5, 0.5)  # Center the text
main_group.append(mem)

bat = analogio.AnalogIn(board.A6)

# enable the pybadge speaker
speakerEnable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speakerEnable.switch_to_output(value=True)

# For a more complex example with battery info:
while True:
    event = k.events.get()

    if event is not None and event.pressed and event.key_number == 1:
        simpleio.tone(board.A0, 100, 0.05, 0.1)

    # Update display with battery info
    val = bat.value * 3.3 / 65536 * 2
    per = ((3.87132 - 3.2) / (4.2-3.2))*100
    text.text = f"bat: {per:.2f}%"
    mem_usage = gc.mem_alloc() / (gc.mem_alloc()+gc.mem_free()) * 100
    mem.text = f"mem: {mem_usage:.2f}%"
    time.sleep(1/60)
