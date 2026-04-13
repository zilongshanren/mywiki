---
title: How To Destroy an Arduino Board - Alan Zucconi
url: https://www.alanzucconi.com/2016/09/17/how-to-destroy-an-arduino-board/
author: Alan Zucconi
published: '2016-09-17'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Developers that are approaching electronics for the very first time have a lesson to learn; and this usually happens the hard way. Wiring a circuit incorrectly, and you can potentially destroy your Arduino board. When it comes to mistakes, hardware is generally not as forgiving as software. This tutorial shows the most common ways you can accidentally destroy an Arduino board; and how to avoid it.

[Applying overvoltage to power pins](https://www.alanzucconi.com#part1)[Drawing too much current from the board](https://www.alanzucconi.com#part2)[Shorting pins](https://www.alanzucconi.com#part3)[Inductive loads without flyback diodes](https://www.alanzucconi.com#part4)[EEPROM wear](https://www.alanzucconi.com#part5)

- Apply >

to power jack - Apply >

to Vin pin - Apply >

to 5V pin - Apply >

to 3V3 pin

There are several ways in which an Arduino board can be powered. If you are using an external power supply, you can plug the barrel connector into the board’s power jack. A standard Arduino Uno board comes with a voltage regulator. Arduino generally tolerate any voltage between ![Rendered by QuickLaTeX.com 6V](../../assets/4c436b2be22f5ad6.png)

![Rendered by QuickLaTeX.com 20V](../../assets/93f755ded1d3362b.png)

![Rendered by QuickLaTeX.com 7V](../../assets/7de1c3016c29740e.png)

![Rendered by QuickLaTeX.com 12V](../../assets/2ce933eb6e8de730.png)


Alternatively, you can power an Arduino directly connecting its **Vin** and **GND** pins to a power supply. You can also power the board via the **5V** and **3V3** pins. Conversely to **Vin**, those two pins are not attached to a voltage regulator. Providing a different voltage to the one requires can potentially break the board.

![48912-arduinouno_r3_front](../../assets/0c8a4e6ea52b9182.jpg)

- Drawing >

from 5V pin - Drawing >

from a I/O pin - Drawing >

from all I/O pins - Drawing >
![Rendered by QuickLaTeX.com 500mA](../../assets/f214558ff91e5fbf.png)


Many examples from the Arduino Playground shows board powering LEDs and other small electrical components. In order for this to work, current must be draw directly from the board. Each I/O pin is rated for a maximum of ![Rendered by QuickLaTeX.com 40mA](../../assets/3487351ec97c24cb.png)

![Rendered by QuickLaTeX.com 20mA](../../assets/81fb4ede51a8338d.png)


Devices that require a lot of current (such as motors) should never be powered directly from an Arduino. The correct approach is to attach an external power supply to the motor, controlled by a transistor. The I/O pins might not be powerful enough to control a motor, but they can be used to drive a transistor’s base.

Even if all of your pins are providing the recommended ![Rendered by QuickLaTeX.com 20mA](../../assets/81fb4ede51a8338d.png)

![Rendered by QuickLaTeX.com 200mA](../../assets/d7f49b2cd201b5f7.png)


Lastly, Arduino comes with a ![Rendered by QuickLaTeX.com 500mA](../../assets/f214558ff91e5fbf.png)


- Shorting Vin pin to ground
- Shorting I/O pins to ground
- Shorting I/O pins to each other

A shortcircuit occurs when voltage is allowed to travel to a path that, by mistake, has very low resistance. Connecting two pins with different voltage without a resistor in between them is usually enough to cause a shortcircuit. The problem with shortcircuits is that they allow potentially large current to dissipate over a wire. This often results in overheating or current spikes that can damage the board.

There are several ways to cause a shortcircuit with an Arduino. Connecting a power pin (such as **Vin**) directly to the ground will allow more than ![Rendered by QuickLaTeX.com 200mA](../../assets/d7f49b2cd201b5f7.png)

[10 Ways to Destroy an Arduino](http://www.rugged-circuits.com/10-ways-to-destroy-an-arduino/) shows detailed schematics of why this happens.

![method01](../../assets/8ae4ca8e8f02eae8.gif)

When LEDs stop receiving power, they simply stop emitting light. This is not the case with other electrical components. Some of them, once depowered, will induce back currents directely towards your board. This typically happens with motors; the reason lies in the way they are built. Within most motors there is a solenoid, which is a conductive coil used to generate a magnetic field. When depowered, the magnetic field inside the coil induces an opposite current back into the coil. This spike lasts for a very short period of time, but can be very dangerous for your electronics.

The way to solve this problem is to use a [flyback diode](https://en.wikipedia.org/wiki/Flyback_diode). A diode is a component that allows current to flow only in a one direction. By attaching a diode (D1, below) to in parallel to a solenoid (L1, below), you can prevent current to flow backwards.

![solenoid-1](../../assets/750af7b927064ceb.png)

The Arduino Playground has a detailed tutorial on how to work with [solenoids](http://playground.arduino.cc/Learning/SolenoidTutorial).

Every board comes with a memory chip that allows to store data even without power. Those chips are called EPPROM, and they allow only a limited number of writing operations. With time, EEPROM memories literally wear out, and it is impossible to override or erase their content. Before you start panicking, it’s important to notice that the ATmega328 EEPROM that is integrated in an Arduino board is rated for 100.000 write cycles. If you’re using the board for your DIY projects, EEPROM wear will never be an issue for you.

Applications that writes data continuously must take into account this limitation. The 100.000 cycles limit refers to a single memory location. You can dramatically reduce EEPROM wear if you cycle your writes on different locations, instead of writing at the same address.

The extended EEPROM library, [EEPROMex](http://playground.arduino.cc/Code/EEPROMex), allows to set a limit on the numbers of writing operations you can perform.

EEPROM.setMaxAllowedWrites(MAX_ALLOWED_WRITES);

There are quite a lot of independent projects ([here](http://hackaday.com/2011/05/16/destroying-an-arduinos-eeprom/) and [here](http://dangerousprototypes.com/blog/2010/06/07/flash-destroyer-dead-at-11-49-million/)) that aimed to find out how many cycles are actually supported by an ATmega328. Continuous writes finally destroyed the EEPROM after more than a month, with more than 1.000.000 cycles.

## Leave a Reply Cancel reply