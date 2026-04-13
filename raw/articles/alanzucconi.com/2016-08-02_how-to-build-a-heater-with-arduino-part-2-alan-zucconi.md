---
title: How to Build a Heater with Arduino - Part 2 - Alan Zucconi
url: https://www.alanzucconi.com/2016/08/02/arduino-heater-2/
author: Alan Zucconi
published: '2016-08-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This is the second part of a tutorial that will teach you how to build a portable heating device with Arduino. In this post, we will explore how to control a heating resistor with Arduino. This allows to keep your setup at the desired temperature.

[Introduction](https://www.alanzucconi.com#introduction)- Step 1.
[Choosing the Sensor](https://www.alanzucconi.com#step1) - Step 2.
[Powering the Heater](https://www.alanzucconi.com#step2) - Step 3.
[Calculating the Base Resistance](https://www.alanzucconi.com#step3) - Step 4.
[Connecting the Components](https://www.alanzucconi.com#step4) - Step 5.
[The Code](https://www.alanzucconi.com#step5) [Conclusion](https://www.alanzucconi.com#conclusion)

In the first part of this tutorial, [How to Build a Heater with Arduino – Part 1](https://www.alanzucconi.com/?p=5344), we’ve discussed how to create and calibrate the component that will generate the heat. The problem so far is that there is no control over the temperature. If you’ve done your calculation correctly and respected the wattage of your resistors, there is no risk of overheating. However, there’s nothing that prevents your resistors from getting hotter than what you initially intended. This is particularly true if there is no ventilation, or if the heater is in direct contact with a surface that does not dissipate heat very well. The correct (and safe) approach to solve this problem is to introduce a sensor to measure the temperature. If it’s too cold, we’re turning the heating on; if it’s too hot, we’re turning it off. Please, keep in mind that what seems a trivial problem is in actuality incredibly challenging. Designing a responsive device that control an actuator (the heater) based on the reading of a sensor (the temperature) can be a major engineering challenge. This tutorial will provide a very simple solution, and point out how the design can be improved with a little bit of extra Maths.

Is important to understand that when it comes to temperature, there are a large number of choices. It’s important to understand that different sensors are based on different technologies, hence come with differed limitations and advantages. The main two classes of temperature sensors that are mostly used are **integrated circuits** and **thermistors**. Distinguishing them is very easy: the former have three pins, the latter only two.

![4472743](../../assets/e29527620305b2e2.jpg)

Like the name suggests, thermistors are components which resistance value is very sensitive to temperature changes. Then a voltage difference is applied to its ends, its resistance will vary in response to changes in temperature. Thermistors are somehow a pain to use, since they require additional resistors and a deeper understanding of electronics. The relationship between resistance and temperature is in fact calculated using the [Steinhart-Hart](https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation) equation, which can be scary at first.

![images-4](../../assets/cb3047616e1deb40.jpg)

For the above-mentioned reasons, this tutorial will focus on the more Arduino-friendly integrated circuit sensors. For this tutorial, I have used the very common [LM35](https://www.amazon.co.uk/Bridgold-Analogue-Precision-Centigrade-Temperature/dp/B07Y7FCZYB?crid=1ZUEPIB7GTT6M&dib=eyJ2IjoiMSJ9.I_1J7TG--f2ZZCPbz-6P3k9X91KxE3pBCb9x-0Pazg2LM_C4NL2hiOM4JNhycmnWGCg-Lgw-6bGUwK1YHyZZH5b0NFqjtmKwk7nehcDXea2SQ23uC9ZeUtvkH2kWiRSYv6C1kt2sX_ZMU7yGYORj8_UXiddpGO1oQbeSRB-6vimCCd8ZQZPgZJmbtCl0_7ld1PYxLjtMWdMsGh7vP5eaMHab2WuHY-VL1suwV_QXekGx6jKxpulGCVvZjXORXYs7iWcGyrzBE9OnQg21wm6PESSkzttLW_zBoonaZ-PR0h0.3_3004Ks-AFImg2xJKAPhKPvVtdAaj8DNq8tYteILXc&dib_tag=se&keywords=lm35&qid=1724356374&sprefix=lm35%2Caps%2C104&sr=8-18&linkCode=ll1&tag=alanzucc-21&linkId=a38b4183f3a5e87d2389b7264b8720cc&language=en_GB&ref_=as_li_ss_tl). Two pins are reserved for the reference voltage (ground and 5V); the voltage on the other one will vary between these two, depending on the temperature.

If you want to expand your knowledge on sensors, [Arduino sensor temperature comparison](http://www.homautomation.org/2014/02/18/arduino-temperature-sensor-comparison/) has ready-to-use recipes for the most used sensor types.

As seen in the previous part of this tutorial, the heater we have designed is likely to require much more current than the one that Arduino can provide. For this reason, it has to be powered separately. A safe and reliable option is to use a traditional phone charger. They usually range from 5V to 9V, and have a limit on the amount of current they can provide. This makes them perfect for this application, as they operate in the a safe range. If you need a serious heating device, you can power you heater directly from the main, although this is going to be very dangerous.

![4191WLdikjL](../../assets/8724daa38a661ecb.jpg)

The problem we have now is to control the flow of current to the heater, using Arduino. This is the perfect time to use a **transistor**. Transistors are, de-facto, switches. They allow or prevent the flow of current in one direction, based on a specific input. We can use Arduino to turn the switch on and off based on the reading from the sensor. The one I am using for this project is a [TIP120](https://www.amazon.co.uk/Adafruit-TIP120-Power-Darlington-Transistors/dp/B00NAY1IBS?ie=UTF8&qid=1470134631&sr=8-1&keywords=TIP120&linkCode=ll1&tag=alanzucc-21&linkId=d8e759faf8f97d9719a29c5966d8e77f&language=en_GB&ref_=as_li_ss_tl), which can operate high voltages. Make sure you have one that can be controller by the voltage provided by an Arduino.

The previous part of this tutorial referred to a battery-operated heater. The new schematics will assume that power comes from a phone charger instead. This changes the input voltage from ![Rendered by QuickLaTeX.com 9V](../../assets/97de3250d26ca499.png)

![Rendered by QuickLaTeX.com 5V](../../assets/130628906f28dea9.png)

![Rendered by QuickLaTeX.com 4W](../../assets/bd1ea882371b5e79.png)

![Rendered by QuickLaTeX.com 6.25\Omega](../../assets/127a0d70d5e1ca85.png)

![Rendered by QuickLaTeX.com 50\Omega](../../assets/4a27d179e401711c.png)

![Rendered by QuickLaTeX.com 0.8A=\frac{5V}{6.25\Omega}](../../assets/6debcfcc97f05532.png)

![Rendered by QuickLaTeX.com 0.5A](../../assets/de32b194375b7ca0.png)


It’s common practice to wire a resistor to the base of the transistor. This is the prevent an excessive flow of current that might damage both the transistor and the Arduino. Most designs use resistors between ![Rendered by QuickLaTeX.com 1K\Omega](../../assets/06cdb2ddc4466deb.png)

![Rendered by QuickLaTeX.com 10K\Omega](../../assets/f20c6da20f65548b.png)


![Rendered by QuickLaTeX.com \[R_B = \left(V_{CC}-V_{BE}\right) \frac{DC_{gain}}{I_C}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-f0876009fb5b3989db9d130703001cdd_l3.png)


Where:


: the base resistance to connect to the transistor base;

: the voltage provided to the base (for Arduino:

);

: the voltage of the transistor when fully on (see below);

: the load current the transistor has to withstand (as calculated previosuly:

);

: the gain of the transistor, when subjected to a current of

amps (see below).

To calculate the ![Rendered by QuickLaTeX.com DC_{gain}](../../assets/3ea373c9c5b21e02.png)

[TIP120 datahseet](https://cdn-shop.adafruit.com/datasheets/TIP120.pdf)) that the [TIP120](https://www.amazon.co.uk/Adafruit-TIP120-Power-Darlington-Transistors/dp/B00NAY1IBS?ie=UTF8&qid=1470134631&sr=8-1&keywords=TIP120&linkCode=ll1&tag=alanzucc-21&linkId=d8e759faf8f97d9719a29c5966d8e77f&language=en_GB&ref_=as_li_ss_tl) has a ![Rendered by QuickLaTeX.com DC_{gain}](../../assets/3ea373c9c5b21e02.png)

![Rendered by QuickLaTeX.com 0.8A](../../assets/27c2883d633bb736.png)

![Rendered by QuickLaTeX.com V_{BE}](../../assets/b5c73550c3062215.png)

![Rendered by QuickLaTeX.com 1.5V](../../assets/fb98f142de5ead22.png)


![gain](../../assets/8ea22327517bc0eb.png)

By plugging all the numbers, we can calculate that ![Rendered by QuickLaTeX.com R_B=13125\Omega](../../assets/7541904fc96caf20.png)

[13KΩ](https://www.amazon.co.uk/UMTMedia%C2%AE-30pcs-13k-ohm-Electronic/dp/B0CM6QY3QR?crid=16UH0DKFDQMCU&dib=eyJ2IjoiMSJ9.XWM1QxP_sJSScXO-78bnZHMS0-M01VbR9rRrIQqw4f2ZJpu1iO2f1ARwgZo2t-UON9MxWjeRUxObuLeRmhbM8vQ_yrIQyEBFdgBh_WVXPXmBv4D7LcIl6b9I7bxsJ-vH8EBUooGMCYk4TXTp4gPmW1nWrmCoLsQBrak70MuC4rMpbAAbvmZy7IMEUTDOXsZL2ilx8mFRbGeKywiq0oiZLXciWjXgYeLItK4XTfPVlJFuKztY6XdhYfyW3ysLxr6IJCK40drPINDlmfeoIV02L7hqDooK1hVbVO8p6mDrgtU._wIdmSXt_zbpbNuoEu4egQ9R8zrdjqIfPIflJCAvUyo&dib_tag=se&keywords=13k%2Bohm%2Bresistor&qid=1724356614&sprefix=13k%2Bohm%2Bresistor%2Caps%2C85&sr=8-8&th=1&linkCode=ll1&tag=alanzucc-21&linkId=8c8836f38a4c41ae3ed238eb8a370248&language=en_GB&ref_=as_li_ss_tl) resistor.

### 🪛 Recommended Components

The following diagram shows how all the components have been wired up. The transistor used, [TIP120](https://www.amazon.co.uk/Adafruit-TIP120-Power-Darlington-Transistors/dp/B00NAY1IBS?ie=UTF8&qid=1470134631&sr=8-1&keywords=TIP120&linkCode=ll1&tag=alanzucc-21&linkId=d8e759faf8f97d9719a29c5966d8e77f&language=en_GB&ref_=as_li_ss_tl), is a NPN; it means that its emitter pin must be grounded.

![heater_bb](../../assets/cda4f053b37c76d6.png)

Remember that in order for this design to work, you have to keep the temperature sensor close to the heating elements.

The final part is to write the logic that operates our heater. During every iteration, Arduino samples the temperature from the sensor and switches the transistor accordingly.

#define PIN_SENSOR A1 #define PIN_SWITCH 9 float target = 30; void setup() { pinMode(PIN_SENSOR, INPUT); pinMode(PIN_SWITCH, OUTPUT); Serial.begin(9600); } float getTemperature() { float data = analogRead(PIN_SENSOR); return (5.0 * data * 100.0) / 1024.0; // Celsius } void loop() { // Temperature read float c = getTemperature(); Serial.print("Temperature: "); Serial.println(c); // Regulation if (c > target) { digitalWrite(PIN_SWITCH, LOW); Serial.print("\tHeater OFF"); } else { digitalWrite(PIN_SWITCH, HIGH); Serial.print("\tHeater ON"); } delay(5000); }

The equation to read the temperature from the [LM35](https://www.amazon.co.uk/Bridgold-Analogue-Precision-Centigrade-Temperature/dp/B07Y7FCZYB?crid=1ZUEPIB7GTT6M&dib=eyJ2IjoiMSJ9.I_1J7TG--f2ZZCPbz-6P3k9X91KxE3pBCb9x-0Pazg2LM_C4NL2hiOM4JNhycmnWGCg-Lgw-6bGUwK1YHyZZH5b0NFqjtmKwk7nehcDXea2SQ23uC9ZeUtvkH2kWiRSYv6C1kt2sX_ZMU7yGYORj8_UXiddpGO1oQbeSRB-6vimCCd8ZQZPgZJmbtCl0_7ld1PYxLjtMWdMsGh7vP5eaMHab2WuHY-VL1suwV_QXekGx6jKxpulGCVvZjXORXYs7iWcGyrzBE9OnQg21wm6PESSkzttLW_zBoonaZ-PR0h0.3_3004Ks-AFImg2xJKAPhKPvVtdAaj8DNq8tYteILXc&dib_tag=se&keywords=lm35&qid=1724356374&sprefix=lm35%2Caps%2C104&sr=8-18&linkCode=ll1&tag=alanzucc-21&linkId=a38b4183f3a5e87d2389b7264b8720cc&language=en_GB&ref_=as_li_ss_tl) comes from the official documentation on Arduino Playground ([LM35 Higher Resolution](http://playground.arduino.cc/Main/LM35HigherResolution)).

The code provided in this tutorial is simple, possibly too simple for this application. The sensor used is unreliable, making the system excessively sensitive to temperature small oscillations and noise. A better approach would be to take repeated samples over a longer period of time. Averaging them reduces the effect of noise on the final measure. If you want an optimal solution, however, you can use a **Kalman filter**. It’s a powerful tool that allows to attenuate and to remove noise from sensors. To read more about it, check the tutorial [A Gentle Introduction to Kalman Filters](https://www.alanzucconi.com/?p=1787).

Secondly, even the way the heater is controller can be improved. There are several techniques to control an actuator based on a sensor reading. A common approach is to use a **PID controller**. This will be the topic of a future tutorial.

## Leave a Reply Cancel reply