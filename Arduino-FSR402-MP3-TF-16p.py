# MicroPython: FSR + MP3-TF-16P (DFPlayer) trigger
# - Scales ADC to 0..1023 so Arduino thresholds can be reused
# - Hysteresis: pressThreshold / releaseThreshold
# - Plays track 1 at volume 25 on press

from machine import Pin, ADC, UART
from time import sleep_ms

# ========= CONFIG (adjust to your board) =========
# ESP32-friendly defaults:
LED_PIN        = 2          # on many ESP32 boards (change if needed)
FSR_ADC_PIN    = 34         # ADC-capable pin (input-only on ESP32)
UART_ID        = 1          # 1 or 2 on ESP32; 0 on some boards
UART_TX_PIN    = 17         # goes to MP3 RX (through ~1k series resistor recommended)
UART_RX_PIN    = 16         # from MP3 TX

# Thresholds (same semantics as your Arduino version, 0..1023)
pressThreshold   = 900
releaseThreshold = 200

# MP3 settings
MP3_VOLUME = 25             # 0..30
TRACK_NUM  = 1              # plays 0001.mp3 in /mp3/ (module-dependent)
# ================================================

# ---- DFPlayer / MP3-TF-16P protocol helper ----
class MP3TF16P:
    # Packet: 0x7E FF 06 CMD 00 HH LL CKH CKL 0xEF
    # checksum = 0xFFFF - (sum of bytes from 0xFF to last data) + 1
    def __init__(self, uart):
        self.uart = uart

    def _send(self, cmd, param=0):
        high = (param >> 8) & 0xFF
        low  = param & 0xFF
        pkt = bytearray([0x7E, 0xFF, 0x06, cmd, 0x00, high, low, 0x00, 0x00, 0xEF])
        cs = 0xFFFF - sum(pkt[1:7]) + 1
        pkt[7] = (cs >> 8) & 0xFF
        pkt[8] = cs & 0xFF
        self.uart.write(pkt)

    def initialize(self):
        # Optional: reset / set device; usually just setting volume is fine
        # self._send(0x0C, 0)   # reset
        # sleep_ms(500)
        self.set_volume(MP3_VOLUME)

    def set_volume(self, vol):      # 0..30
        v = max(0, min(30, vol))
        self._send(0x06, v)

    def play_track_number(self, n):  # by index
        self._send(0x03, n)

    def play_folder_file(self, folder, file):
        # plays /<folder>/<file>.mp3 (folder 1..99, file 1..255)
        self._send(0x0F, (folder << 8) | file)

    def stop(self):
        self._send(0x16, 0)

# ---- ADC helper: normalize to 0..1023 regardless of board ----
class FSRReader:
    def __init__(self, pin_num):
        self.adc = ADC(Pin(pin_num))
        try:
            # ESP32 specifics
            self.adc.atten(ADC.ATTN_11DB)  # ~0..3.3V full scale
            self.adc.width(ADC.WIDTH_12BIT)  # 0..4095
            self._scale = 4095
        except Exception:
            # Pico / others: often 16-bit 0..65535
            self._scale = 65535

    def read_0_1023(self):
        raw = self.adc.read_u16() if hasattr(self.adc, "read_u16") else self.adc.read()
        return int((raw * 1023) // self._scale)

# ---- Init hardware ----
led = Pin(LED_PIN, Pin.OUT)
fsr = FSRReader(FSR_ADC_PIN)
uart = UART(UART_ID, baudrate=9600, tx=Pin(UART_TX_PIN), rx=Pin(UART_RX_PIN))
mp3 = MP3TF16P(uart)
mp3.initialize()

print("System ready — waiting for pressure...")

isPressed = False

# ---- Main loop ----
while True:
    fsrValue = fsr.read_0_1023()
    print("FSR value:", fsrValue)

    if (not isPressed) and (fsrValue > pressThreshold):
        isPressed = True
        print("Pressure detected! Playing sound…")
        led.value(1)
        mp3.set_volume(MP3_VOLUME)       # optional refresh
        mp3.play_track_number(TRACK_NUM) # plays 0001.mp3 (or #1 in root, module dependent)

    elif isPressed and (fsrValue < releaseThreshold):
        isPressed = False
        led.value(0)

    sleep_ms(100)
