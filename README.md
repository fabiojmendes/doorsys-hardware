<!-- vim: set tw=80: -->

# Doorsys Hardware

This repo contains the designs for the custom PCB for the doorsys device.

Earlier versions of this project used a esp32 relay board and a soldered
protoboard. That wasn't very clean as you can see in the [pictures](#pictures)

## Schematics

After transitioning from the esp32 chip in favor of the esp32-c3 for better
compatibility with rust (esp32-c3 is based on the RISC-V architecture) a custom
board was necessary.

This board design is based on the reference implementation provided by the
esp32-c3 wroom module [datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-c3-wroom-02_datasheet_en.pdf)
.

### Important remarks

- A DCDC regulator is used to drop the voltage from 12v used by the door lock to
  the 3v3 used by the esp chip
- The onboard relay is driven by a transistor and contains flyback diodes to
  manage the voltage spikes coming from the lock
- GPIO 4 and 5 are connected D0 and D1 respectively hey on the keypad
- GPIO 10 is connected to the relay for door activation
- Headers for the uart and usb ports are available

![Schematics](./assets/schematic.png)

## PCB

Here is the PCB design

![PCB Top](./assets/pcb-top.png)
![PCB Bottom](./assets/pcb-bottom.png)

## Pictures
