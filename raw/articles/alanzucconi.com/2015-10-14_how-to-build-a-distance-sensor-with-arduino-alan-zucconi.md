---
title: How to build a distance sensor with Arduino - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/14/how-to-build-a-distance-sensor-with-arduino/
author: Alan Zucconi
published: '2015-10-14'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

You can safely say that when it comes to electronics, there are countless ways to measure distances. This tutorial will explain how to build an inexpensive IR distance sensor under $8, perfect for close measurements and motion detectors.

- Step 0:
[The theory](https://www.alanzucconi.com#step0) - Step 1:
[The circuit](https://www.alanzucconi.com#step1) - Step 2:
[The calibration](https://www.alanzucconi.com#step2) - Step 3:
[The reading](https://www.alanzucconi.com#step3) [Conclusion](https://www.alanzucconi.com#conclusion)[Further projects…](https://www.alanzucconi.com#extra)

You will need:

[Arduino Uno](https://www.amazon.co.uk/Arduino-A000066-ARDUINO-UNO-REV3/dp/B008GRTSV6?adgrpid=164748899670&dib=eyJ2IjoiMSJ9.o7pOqJX-cYWA46ycp0koCivPY0QTRmL2SDpj5wQrXxHCjzxKPS2kSAh0ksXFcWyN6MTEWFAAuyj3v0FylKTVUmySvk4-KznEQIAm7ZQxWnNpz7E0hv6A99ZPVYM0boR46_ZOmLcAp4G6iWqXbBBE9RAoTNQrtUtzC41Sc0_8jBbAYuFa3kTOBNb53Vk7gkDyN7cKyOsZzIo_dmcL1gqjnVz3iR9TpCpLxJ-OKbG0zkE.Q4ROBntvx1FaKZGMDV51goFkAko0KTiTB5StZ9kXyoM&dib_tag=se&gad_source=1&hvadid=696352506158&hvdev=c&hvexpln=69&hvlocphy=9198127&hvnetw=g&hvocijid=3627056942662284107--&hvqmt=e&hvrand=3627056942662284107&hvtargid=kwd-305607388733&hydadcr=19074_2281153&keywords=arduino+uno+amazon&qid=1724351478&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&linkCode=ll1&tag=alanzucc-21&linkId=aaca12b932ba24d92f072c32085a6a01&language=en_GB&ref_=as_li_ss_tl)[IR photodiode receiver](https://www.amazon.co.uk/gp/product/B00NQ6S50M?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=1bbff9f5495e8e95d42a11b502080648&language=en_GB&ref_=as_li_ss_tl)[IR emitters](https://www.amazon.co.uk/sourcingmap-Infrared-Launch-Emission-Emitting/dp/B00WW6K7T4?crid=16KHS1PLH7CWO&dib=eyJ2IjoiMSJ9.S_EXFPsgVNwBTV2UyFaUJ-I9bFogcFF6DAwYuAbqrg4zSdh0R2w54TC7H8kqohhXMB36NVDSW5eoX34PFbrd12O7CrP1vouTTfttb-kgjswAfEBjf8T4cMv_9Zuwdyk7DuMODsXjQ6ExzI4dzw05VsgAJVhD9qRs-KX524WMjiTBoSQu3wOAof_WBqsTTm1WflQIEq-DqRMMHuOso6koyZQRDA_QumgZmMVQbHaFPpM650kkugJ_EK46euzSXOXIyl47Q5kQ_DNR8Z32nbsE9tpOQIc0KAAIDLaE_CiEDI8.hK4eCTWP5wWrM2_0DBe9fFDo_IK9aEpkrPZhE0SV4H4&dib_tag=se&keywords=led+ir&qid=1724335143&s=industrial&sprefix=led+ir%2Cindustrial%2C89&sr=1-8&linkCode=ll1&tag=alanzucc-21&linkId=2df76a5080f8163719d3619f07bf95b9&language=en_GB&ref_=as_li_ss_tl)- Resistors:
[18Ω](https://www.amazon.co.uk/HUABAN-50PCS-Watts-Metal-Resistor/dp/B08BFWZT73?crid=2CKYR3PAUTG7O&dib=eyJ2IjoiMSJ9.avHzI6Fylx-8symxnZNc6kG-o_rLAI6o9ShbG7KV8H4-4Nr4RLOW-2H6bvt6jlflag-JOZZWEnx-JWI9OtGTnT5dzDwiNv6twAUXXkEkTdmZxDCelkolfdfP2JRFOnCVDY6GNQgS90PTKk_iHIsIi4hbcszhJRVDTQCiYN3ZveEFXgp5KeHoAkiABSksb6eeM1kccYBC03txXxQyMn0dKC4rT5xhZ6AnMLeB2j5psvNCApXSug2luzEupQxtvetWsGHPR5Otrz8rsWWLfrZc5RHAlZ0lGMUxZtFwt294a64.M8pOlYRVNS-L29HR8DR_NjrvQkhBJBUPfUftvFIt7Rc&dib_tag=se&keywords=18%2Bohm%2Bresistors&qid=1724351579&sprefix=18%2Bohm%2Bresistors%2Caps%2C81&sr=8-7&th=1&linkCode=ll1&tag=alanzucc-21&linkId=b1c39030f723f2295bc6739acde047e4&language=en_GB&ref_=as_li_ss_tl),[39Ω](https://www.amazon.co.uk/EDGELEC-39-ohm-%C2%B11-Resistance/dp/B07HDGX5LV?crid=W56BUOFY69PQ&dib=eyJ2IjoiMSJ9.GfHhpSVlKkTMXqahkaCXHwkRGVXrZ2zHqjGecoe2OZaDDW6k89fk0HGi4-D1p75S0yhePNQd2VBrkXJY5i2infoDUvYF99VBCPY3dQTiTvSeLMRnZNppaj09UU1vf6iAi2gvmUEfTKANaa2lG8F8umSvVf5U4A27YVlSCnxy-nJMRmJK_CFDA8Ar2Lf_mvoXftl2HqkEHrgJa0XCwen72grLFyUQsyj_9fKPp4qWOf09VZ2EjNnwxOf5fB6fBlQH6kCLGW3pc3JBcgAnIYMmS40rZ4jIxW6DFkdz_ciN26I.H6tuDfNA8T2qjDp_NiFp4NXyK1ayZAkQea7KADSeN10&dib_tag=se&keywords=39%2Bohm%2Bresistors&qid=1724351865&sprefix=39%2Bohm%2Bresistors%2Caps%2C84&sr=8-5&th=1&linkCode=ll1&tag=alanzucc-21&linkId=a61a8ceee7a17bcda4c01aac7199ea08&language=en_GB&ref_=as_li_ss_tl).

You can download the final Arduino code [here](https://drive.google.com/file/d/0B4nCcaMlgxV2VGZ5amVsQmtzU1U/view?usp=sharing).

![altctrl](../../assets/e6545f6a90eb98b8.jpg)

This post is part of a longer series of tutorial about alternative games controllers.

- Part 1.
[How to integrate Arduino with Unity](https://www.alanzucconi.com/2015/10/07/how-to-integrate-arduino-with-unity/) - Part 2.
[How to hack any IR controller](https://www.alanzucconi.com/2015/08/19/how-to-hack-any-ir-remote-controller/)

If you are going to create an alternative game controller yourself, you should definitely look into [ALT.CTRL.GDC](http://www.gdconf.com/news/submit_your_unique_alternative.html). It’s one of the most fresh and intriguing exhibitions at GDC, and is all dedicated to innovative ways to interact with games.

![dodeface](../../assets/ac35843c2fc1fd99.jpg)

At the heart of this sensor there are two IR LEDs. One emits light, the other receives it. When an object is close to the sensor, it will inevitably reflect some of the IR light. This is detected by the Arduino, and translated into a distance measurement. The Human eye does not pick up infrared light; this sensor will look invisible, even though it can be extremely bright in the IR spectrum. There are many things that can go wrong with this approach; IR light can be erroneously picked up from another source, or the objects is not reflective enough. This picture shows a face of the DodecaLEDron, an alternative game controller which is based on the same principle.

### 🪛 Recommended Components

This circuit has three LEDs. The bottom ones are [IR emitters](https://www.amazon.co.uk/sourcingmap-Infrared-Launch-Emission-Emitting/dp/B00WW6K7T4?crid=16KHS1PLH7CWO&dib=eyJ2IjoiMSJ9.S_EXFPsgVNwBTV2UyFaUJ-I9bFogcFF6DAwYuAbqrg4zSdh0R2w54TC7H8kqohhXMB36NVDSW5eoX34PFbrd12O7CrP1vouTTfttb-kgjswAfEBjf8T4cMv_9Zuwdyk7DuMODsXjQ6ExzI4dzw05VsgAJVhD9qRs-KX524WMjiTBoSQu3wOAof_WBqsTTm1WflQIEq-DqRMMHuOso6koyZQRDA_QumgZmMVQbHaFPpM650kkugJ_EK46euzSXOXIyl47Q5kQ_DNR8Z32nbsE9tpOQIc0KAAIDLaE_CiEDI8.hK4eCTWP5wWrM2_0DBe9fFDo_IK9aEpkrPZhE0SV4H4&dib_tag=se&keywords=led+ir&qid=1724335143&s=industrial&sprefix=led+ir%2Cindustrial%2C89&sr=1-8&linkCode=ll1&tag=alanzucc-21&linkId=2df76a5080f8163719d3619f07bf95b9&language=en_GB&ref_=as_li_ss_tl); the top one is an [IR photodiode receiver](https://www.amazon.co.uk/gp/product/B00NQ6S50M?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=1bbff9f5495e8e95d42a11b502080648&language=en_GB&ref_=as_li_ss_tl). It is important to use *photodiodes*, and not *phototransistors*. Both types are IR receiver which change their resistance according to how much light they sense. However, while the latter works like a digital switch: it either sense IR or it doesn’t. For this project we need a photodiode because we actually need to measure the quantity of light received.

![ir distance_bb](../../assets/573c3410edc9ebd3.png)

To measure the amount of light sensed from the IR receiver, we measure the drop of voltage on its resistor. When the photodiode receives light, it allows current to flow from the 5V to the GND pin; little to no current then flows back to A0. On the other hand, when the diode is in darkness and doesn’t let current flow, A0 reads a high voltage. For this project you have to use an *analog input* (A0-A5).

For this circuit to work properly, you have to find the right resistors to use. I’ve used [LED calculator](http://led.linear1.org/led.wiz) for this. You need to know the forward current (*V*) and forward voltage (*If*) of your LEDs, which are always indicated in their datasheets.

The moist naive way you can read data from the circuit is the following:

void setup () { pinMode(A0, INPUT); } void loop () { int distance = analogRead(A0) Serial.println(distance); }

Most of the tutorials I’ve found which explains how to do IR distance sensors stop here. As a software engineer, I believe we can do much, much more on the software side. First of all, the distance readings of this sensor are likely to be affected by the IR background noise in your room. Almost every artificial light source is visible in the IR spectrum, causing interferences with our sensor. A more sophisticated approach to solve this problem is to calibrate the light background in your environment. To do this, we can sample the input from the sensor when (1) no object is nearby and (2) an object is very close. This provides a baseline calibration which depends on the light in the room.

int sensorPin = A0; int duration = 1000; int calibrationZero; int calibrationOne; void setup () { pinMode(sensorPin, INPUT); // Far Serial.print("Far calibration..."); delay(duration); int sensorCumulativeValue = 0; int reads = 0; unsigned long timeStart = millis(); do { delay(20); sensorCumulativeValue += analogRead(sensorPin); reads ++; } while (millis() <= timeStart + duration); calibrationZero = sensorCumulativeValue / reads; Serial.print(calibrationZero); Serial.println(); // Close Serial.print("Close calibration..."); delay(duration); sensorCumulativeValue = 0; reads = 0; timeStart = millis(); do { delay(20); sensorCumulativeValue += analogRead(sensorPin); reads ++; } while (millis() <= timeStart + duration); calibrationOne = sensorCumulativeValue / reads; Serial.print(calibrationOne); Serial.println(); }

This new `setup`

function is divided in two seconds, to calibrate the sensor for far and nearby objects, respectively. The variable `duration`

determines how long each calibration phase lasts. This is important because single readings are prone to error, but averaging them over a longer time interval provides more reliable data. The result of the calibration is stored in `calibrationZero`

and `calibrationOne`

, which will be used later to correct our readings.

Reading from the sensor works in a similar fashion. We repeat a certain numbers of readings over a long time interval, and average them out to make sure about their reliability.

int getDistanceReading (int readings = 5) { int sensorCumulativeValue = 0; for (int i = 0; i < readings; i ++) { delay(20); sensorCumulativeValue += analogRead(sensorPin); } int distance = map ( sensorCumulativeValue / readings, sensorCalibrationZero, sensorCalibrationOne, 0, 255 ); return constrain(distance, 0, 255); }

**Lines 8-13** use the function `map`

to rescale the readings between 0 and 255. These two values corresponds to the amount of IR light received during the two calibration steps.

Finally, to use this code:

void loop () { int distance = getDistanceReading (); Serial.println(distance); }

It’s worth noticing that your code can be quite jumpy and unreliable. An interesting approach to remove noise from your readings is by adopting a [Kalman filter](https://www.alanzucconi.com/2022/07/24/kalman-filter-1/), which has been discussed in details in a previous post.

### 🪛 Recommended Components

This post explored how to use IR light to sense short distances. I have used this technique to create an omni-direction controller called DodecaLEDron. It features 11 distance sensors, all fitting in a £10 budget. Since I required so many analog inputs, I had to use an [Arduino Mega](https://www.amazon.co.uk/ARDUINO-MEGA-2560-REV3-A000067/dp/B0046AMGW0?dib=eyJ2IjoiMSJ9.SXI9i_xtDDI-m7txpC56hTtUvBuLVBG4k6-5DNntyHrgaPOhcETZPOFG1NihFF5kAXJy_iqcb42DyxVtDi8987Leyds73M9O5035gYm9pyJ0-tCGHePIlafAbJ44YYYZQK4gdV9cIAD9FNRFu4SKXoR3PRKfAvtBychOEocRMoWQ8a0uwSLW4exyex7jv4GOHyG6h1sDRQA0JFmdcJ3dEwKOTvCrQjj6ylWB7-BXe3g.ZiuejTosJJEzc5AWg8z0ODnDZ-lA6cYdJzc-ArjUUDk&dib_tag=se&keywords=arduino+mega&qid=1724351167&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&linkCode=ll1&tag=alanzucc-21&linkId=fe11e0029fc844bac34e9a511ffeecaa&language=en_GB&ref_=as_li_ss_tl) rather than an Arduino One.

There are many other techniques which are more reliable and fully Arduino-compatible. If you only to detect motion, you can use a [PIR sensor](https://www.amazon.co.uk/Detector-HC-SR312-Pyroelectric-Infrared-Automatic/dp/B07XLKTQMG?adgrpid=160479669026&dib=eyJ2IjoiMSJ9.L3i-foryQKyea-wh3gOe7r_5brmQ9vUsWIPmoMLC-5L7px3f8-hgRHXuIiNVcebSTa6b2EgW6xKDmFtNFlHin1SsPBnimaks0dGH7tL-LMShV73L20rPkK5rE_G-Pns6AvtCMeGu4pLEebOUcyzFZE-OCWEA8LjN6b3T1bnJH8Uwds3l9I2KTu3N7vw8eRkbyDtEQVnJYBkyKhnCSGqaLMbSB1N8tQlir6OVZNkeoUR4XykK_mUW2jUnaiHab1xJcjTI4vhueW2ZAxeqjyelyJeNF1dJnNzUbGxQ_L6NkEs.bNksQimQD6go7_zflzLlnqspgGTDRy8kdU8moiDtM50&dib_tag=se&gad_source=1&hvadid=696342256711&hvdev=c&hvexpln=69&hvlocphy=9198127&hvnetw=g&hvocijid=8404869757923197368--&hvqmt=b&hvrand=8404869757923197368&hvtargid=kwd-301323375065&hydadcr=5086_2287848&keywords=pir+motion+sensor+module&qid=1724351206&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1&linkCode=ll1&tag=alanzucc-21&linkId=005cdeab71f0f2173524e0933dd70b92&language=en_GB&ref_=as_li_ss_tl) (Passive InfraRed). For more advanced projects, my favourite component is the [ultrasonic module](https://www.amazon.co.uk/dp/B07TKVPPHF?_encoding=UTF8&psc=1&linkCode=ll1&tag=alanzucc-21&linkId=fac70010c50716e040b433d173d89459&language=en_GB&ref_=as_li_ss_tl) which is, de-facto, a small sonar. By using the Doppler effect you can also calculate the speed of the object it detects. For large scale applications, such as localisation within a building, you could use [Bluetooth iBeacons](https://www.amazon.co.uk/gp/product/B00KEN2DHQ?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=ae80a52e33e8325a77f31be077374236&language=en_GB&ref_=as_li_ss_tl); I’ll explain how to use them in a future post.

## Leave a Reply Cancel reply