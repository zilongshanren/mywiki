---
title: Everything You Need to Know About LEDs - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/21/everything-you-need-to-know-about-leds/
author: Alan Zucconi
published: '2015-10-21'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Many game developers are easily scared by electronics. Even if Arduino has shifted most of the workload on its software side, there are applications which still need a good knowledge of circuitry. This post will teach how to use LEDs, from the most basic model to the most advanced one:

- Part 0.
[Theory](https://www.alanzucconi.com#part0) - Part 1.
[Basic LED](https://www.alanzucconi.com#part1) - Part 2.
[RGB LED](https://www.alanzucconi.com#part2) - Part 3.
[Neopixel strip](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

LEDs are perfect for creative projects, and they can be also be used to create entire games, such as the mesmerising [Line Wobbler](http://aipanic.com/projects/wobbler).

This post belongs to a series of tutorials aiming to teach game developers how to build their own alternative game controllers:

[How to integrate Arduino with Unity](https://www.alanzucconi.com/2015/10/07/how-to-integrate-arduino-with-unity/)[How to build a distance sensor](https://www.alanzucconi.com/2015/10/14/how-to-build-a-distance-sensor-with-arduino/)[How to hack any IR remote controller](https://www.alanzucconi.com/2015/08/19/how-to-hack-any-ir-remote-controller/)

### 🪛 Recommended Components

LED is the acronym for **Light-Emitting Diode**. As the name suggests, it is a component that emits light. The term *diode* indicates an electric component which allows current to flow only in one direction. Hence, all diodes have a polarity, meaning that they have a positive (**anode**) and a negative (**cathode**) side. An LED is generally used in **forward bias condition**, meaning that its positive side is attached to the positive side of the circuit. In order to work, the LED requires a certain voltage which is referred as **forward voltage** or ![Rendered by QuickLaTeX.com V_F](../../assets/104a83fe0644ffec.png)

**forward current**, or ![Rendered by QuickLaTeX.com I_F](../../assets/1bc09187e216e7de.png)


![hgfhfg](../../assets/647cf00666f1143a.png)

#### Current limiting resistor

As mentioned in the previous section, LEDs draw all the current they receive. Unless you provide a way to limit this amount, it’s very likely any LED will burn when connected to a battery. This is why LEDs are commonly coupled with **resistors**, which allows to regulate the amount of current received. Is important to pick a resistor which will ensure that only an amount of current equal to ![Rendered by QuickLaTeX.com If](../../assets/8f9383f251d4dc99.png)

**Ohm’s Law** relates current, voltage and resistance as ![Rendered by QuickLaTeX.com R=\frac{V}{I}](../../assets/f920fb242ec3c621.png)

![Rendered by QuickLaTeX.com V=V_{battery}-V_{F}](../../assets/44197c7835a62ad2.png)

![Rendered by QuickLaTeX.com I_F](../../assets/1bc09187e216e7de.png)

![Rendered by QuickLaTeX.com I = \frac{I_f}{1000}](../../assets/7bf1762f855138c3.png)

![Rendered by QuickLaTeX.com V_{battery}=5V](../../assets/c8a8133c40ee347c.png)


![Rendered by QuickLaTeX.com \[R=\frac{V_{battery} - V_F}{\frac{I_F}{1000}}=\frac{3V}{0.02A}=150\Omega\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2fe3efc257ee6bb6681b8c5bf326370a_l3.png)


You can refer to the following table to know which resistor you should use:

For more complicates circuits, you can also refer to this [LED calculator](http://led.linear1.org/1led.wiz).

Basic LEDs usually come in a transparent epoxy case, which also works as a lens. The positive side, called anode, is recognisable because is connected to a longer pin. Alternatively, the cathode side of the LED is always flat.

![LED,_5mm,_green_(en).svg](../../assets/196fb1e2c6f261e0.png)

Once you have identified the positive and negative sides, you can attach it to an [Arduino Uno](https://www.amazon.co.uk/Arduino-A000066-ARDUINO-UNO-REV3/dp/B008GRTSV6?&linkCode=ll1&tag=alanzucc-21&linkId=f0e512d9ba7e856e8f7738baf5252176&language=en_GB&ref_=as_li_ss_tl) providing that you have the right resistor.

![led1_bb](../../assets/d8b457603ba0d2a6.png)

By connecting your LED to the 5V output, it will always be on. If you want to be able to turn it on and off, you should attach it to a pin and use `digitalWrite`

to write `HIGH`

or `LOW`

to it. The following code is taken from the [Blink](https://www.arduino.cc/en/Tutorial/Blink) sketch from Arduino:

void setup() { pinMode(3, OUTPUT); } void loop() { digitalWrite(3, HIGH); delay(1000); digitalWrite(3, LOW); delay(1000); }

Colour is not the only thing you should look for when buying LEDs. The brightness, for instance, is a very important parameter. Typical LEDs are rated 20mA, while very bright ones tend to be rated at 50mA or 100mA.

### 🪛 Recommended Components

#### Pulse Width Modulation

As a general rule, is safe to provide less current than the one indicated in ![Rendered by QuickLaTeX.com I_F](../../assets/1bc09187e216e7de.png)

**pulse width modulation**. Arduino has a function called `analogWrite`

, which is used to output square waves made alternating `LOW`

and `HIGH`

voltages. The period of a square wave in Arduino, also called **duty cycle**, is approximately 2ms, meaning that Arduino has a frequency of 500Hz. The parameter provided to `analogWrite`

determines how much time of the duty cycle is spent outputting a `HIGH`

value.

![pwm](../../assets/85b48b691db0c5d2.gif)

When `analogWrite`

is used on an LED, it turns it on and off very fast. The human eye cannot refresh fast enough to see the LED blinking at 500Hz, so the duty cycle is perceived as a difference in brightness. Arduino comes with a sketch called [Fade](https://www.arduino.cc/en/Tutorial/Fade) which uses PWM to fade an LED in and out:

int led = 9; int brightness = 0; int fadeAmount = 5; void setup() { pinMode(led, OUTPUT); } void loop() { analogWrite(led, brightness); brightness = brightness + fadeAmount; if (brightness == 0 || brightness == 255) fadeAmount = -fadeAmount ; delay(30); }

PWM is the standard way used to change the brightness of LEDs in Arduino, but is only available on certain pins. The ones which can be used for PWM have a tilde next to them.

The actual components that emits light inside an LED is tiny. So tiny that there are components which can fit three of them in the same space. The most commonly used is the [RGB LED](https://www.amazon.co.uk/gp/product/B005VMDROS?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=9af261d5ac0ab47009b2757e7ae7428b&language=en_GB&ref_=as_li_ss_tl), which has four pins. One is a shared ground, while the other three drive the R, G, and B components. They are, de-fact, three independent LEDs and requires three different PWM pins to be controlled. Each one requires its own resistor.

![led2_bb](../../assets/94b49e2a6e589216.png)

int pin_r = 9; int pin_g = 10; int pin_b = 11; void changeColour (int r, int g, int b) { analogWrite(pin_r, r); analogWrite(pin_g, g); analogWrite(pin_b, b); }

The problem with RGB LEDs is that each one of them requires three PMW pins. Arduino Uno as only six, meaning that only two RGB LEDs can actually be used at the same time. If you want to connected dozens or hundreds of RGB LEDs, another approach is needed. Adafruit has created [Neopixel strip](https://www.amazon.co.uk/gp/product/B00SLYAHSW?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=f6001e3b33bcef6bd9c0e5869d7cd9ea&language=en_GB&ref_=as_li_ss_tl), which requires only three pins to drive several individual RGB LEDs. Using NeoPixels is a little bit more complicated.

![led3_bb](../../assets/85a61c5a480840d5.png)

**Power supply.**Each pixel in a NeoPixel strip draws 60mA when is shining at full brightness; Arduino can only provide 500mA thought its 5V pin. If you are using more than 8 pixels, you need an external 5V power supply. Since NeoPixels are very sensitive to voltage fluctuation, you should put a capacitor between the positive and negative sides of the power supply. Capacitors takes time to charge, and offer protection from spikes. Adafruit suggests to use a[1000µF, 6.3V capacitor](https://www.amazon.co.uk/Electrolytic-Capacitor-1500-Radial-Leaded/dp/B00UHS664O?crid=18FCT5R89SVBU&dib=eyJ2IjoiMSJ9.UUQ3VzbmALEvSgA2gKnmCDMP7cgHiv0pn9DypLbH9mQVMGMNfbNbD11W8yRq0oWHwh3JmwIcIbyFWideuQVGf38FCUwCy8JRcjhLKMDFN15FmySzf6nurytd0kmDpSwDUAWleIeGt2G--7ZhODCgS_s0IQgd8R69OrYlmpEoV3IaI85Mw3LuVgAJZD3aPePaX0-kGzTv2cchRtXFHIehdoKd8ffOGLH2cDj2umT0ZxrKBryjXeRDPhOtS9MgB2ucbYKGgBDSCXmrc1xgJjrauiaKLo_LtCO4QH9V5CljZfY.b1ZlN7FndFginvBTaRQXaHSALSSBpCuNcbDZKifgqbs&dib_tag=se&keywords=1000+%C2%B5F%2C+6.3V+capacitor&qid=1724335452&s=industrial&sprefix=1000+%C2%B5f+6.3v+capacitor%2Cindustrial%2C69&sr=1-5&linkCode=ll1&tag=alanzucc-21&linkId=652cf1961b4df5d945ff8ca9f01705c5&language=en_GB&ref_=as_li_ss_tl). On some models, the 5V and ground pins are called VDD and VSS, respectively.**Data input.**Neopixels require a[470Ω resistor](https://www.amazon.co.uk/gp/product/B004S12JQA?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=12b0f41941147fe3fd410ffcb4cb1683&language=en_GB&ref_=as_li_ss_tl)on its data line, marked as DIN. It is very important that the grounds of the Arduino and the power supply are aligned. To do this, you should connect both grounds together.**The library.**In order to use the NeoPixel strip, you need to download and install[its library](https://github.com/adafruit/Adafruit_NeoPixel). If you are not familiar with the procedure, you should follow the installation steps[here](https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library).**Initialisation.**Once the library is installed, the NeoPixel strip can be used. The following code initialises a strip of 60 pixels, connected through pin 6.

#include <Adafruit_NeoPixel.h> Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, 6); // (pixels, pin) void setup() { strip.begin(); strip.setBrightness(255); // Full brightness strip.show(); // All pixels off }

**Code.**NeoPixel LEDs can be addressed individually with the function`setPixelColor`

. To commit the chances, you have to invoke the`show`

function.

strip.setPixelColor(n, red, green, blue); strip.show();

NeoPixels are a rather sophisticated piece of technology. On the [Adafruit](https://learn.adafruit.com/adafruit-neopixel-uberguide/overview) website you can find more information how to use them.

The LEDs used in Adafruit components looks very different from the ones presented in the previous sections. They are often called SMD LEDs, which stands for **Surface Mounted Device**.

### 🪛 Recommended Components

### Conclusion

There are so many things you can do with LEDs, especially RGB ones. Adafruit NeoPixels can be rather expensive, but there are so many incredible things you can build of of them.

#### Other resources

[LED Throwies](http://www.instructables.com/id/LED-Throwies/): How to use LEDs and coin batteries;[LED basics](https://www.baldengineer.com/led-basics.html): A very nice article which explains how to use LEDs;[Resistors for LEDs](http://www.evilmadscientist.com/2012/resistors-for-leds/): A more detailed guide on how to use resistors for LEDs;[Wallet-size LED Resistance Calculator](http://www.evilmadscientist.com/2009/wallet-size-led-resistance-calculator): An old fashioned resistance calculator made out of paper.

## Leave a Reply Cancel reply