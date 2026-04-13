---
title: How to hack any IR remote controller - Alan Zucconi
url: https://www.alanzucconi.com/2015/08/19/how-to-hack-any-ir-remote-controller/
author: Alan Zucconi
published: '2015-08-19'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you haven’t heard of Air Swimmers before, you probably had a miserable life. Air Swimmers are inflatable foil balloons made in the shape of fish. But what makes them really awesome is the fact that they can be remotely controlled to fly around in a room. One of my friends, [Claudio](https://www.linkedin.com/in/santinic), developed an ~~obsession~~ interest for them; and that’s when we decided to create our own *hackuarium*.

The idea was simple: buying a bunch of Air Swimmers, hacking into their controllers and running a swarm simulation to control them. If you’re interested in doing the same and you have a basic knowledge of electronics …you’re reading the right post. At the end of this article you can find the links to buy all the necessary components.

### How it works…

![ir sniffer (1)](../../assets/d7c0431186569b5b.png)

The first step is to understand how the remote controller works. Every controller has an IR sensor and it usually works with a proprietary protocol. We wanted to use a modular approach which enables us to set up new fish with little to no work. For that reason, we decided to sniff the IR packets sent by the remote controller, so that we could then replay them at will.

This technique is often referred as *sniffing*, since the device we’ll build will detects IR messages which were not originally directed to it. This particular approach works perfectly with the majority of IR remotes and devices, since there is no actual processing involved. Every time you push a button on the remote, you’re sending the same message; the receiver ignores where the message comes from and just executes it.

### Step 1: Building the IR receiver

![ir2_bb2](../../assets/4f90dfe2fe0d411b.png)

The circuit above uses a an Arduino Uno board connected to an IR receiver (in black). There are several types of IR receivers; for this tutorial is important to use a digital receiver (like the [TSOP4838](https://www.amazon.co.uk/gp/product/B00PJ80S14?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=fe4d7a0febfb05ca27e7169dfa713936&language=en_GB&ref_=as_li_ss_tl)) and not an IR photocell . A digital receiver is sensitive to 38KHz IR signals; if it detects one, it’ll output a low voltage (0 volt), or a high one (5 volt) otherwise. A photocell, instead, acts like a variable resistor and its voltage output linearly mirrors the amount of IR light is has been exposed to. Remotes typically work on digital signals and that’s why we’ll a digital receiver.

The schematics show that I also used an IR emitter. It’s important to couple it with the right resistors; too high and it won’t turn on, too low and it will burn. IR diodes typically requires [180Ω resistors](https://www.amazon.co.uk/gp/product/B004S12XHU?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=ace6ba7bb58476d9e8e164a1187cc6c3&language=en_GB&ref_=as_li_ss_tl). Double check on your datasheets to be sure!

To decode the digital signals that the IR receiver will produce, we’ve been using a library called [Arduino-IRremote](https://github.com/shirriff/Arduino-IRremote), which comes with several demos and examples. Once you’ve installed the library, you can test your setup with [this](https://github.com/shirriff/Arduino-IRremote/blob/master/examples/IRrecvDemo/IRrecvDemo.ino) code.

#include <IRremote.h> int RECV_PIN = 11; IRrecv irrecv(RECV_PIN); decode_results results; void setup() { Serial.begin(9600); irrecv.enableIRIn(); // Start the receiver } void loop() { if (irrecv.decode(&results)) { Serial.println(results.value, HEX); irrecv.resume(); // Receive the next value } delay(100); }

The pin referred in **line 3** must match the one you have used for your IR receiver. **Line 14 **decodes the raw data stored into `results`

, either from `irrecv.enableIRn()`

or `irrecv.resume()`

. Once started, the program should display data when exposed to the light or a remote controller.

### Step 2: Sniffing the code

So far, the setup is already able to sniff packets. `irrecv.decode`

, in fact, shows these packets in a Human-readable format, But if we need to re-send them, the actual raw data has to be extracted and converted in a format which is compatible with `irsend`

. The following code, inspired by [this one](https://github.com/j0hnds/sketchbook/blob/master/libraries/IRremote/examples/IRrecord/IRrecord.pde), converts the inputs read from the receiver into a list of integer, separated by commas.

// Storage for the raw data unsigned int rawCodes[35]; int codeLen; void loop() { if (irrecv.decode(&results)) { extractRaw(&results); // Displays the raw codes for (int i = 0; i < codeLen; i ++) { Serial.print(rawCodes[i]); Serial.print(", "); } Serial.println(); irrecv.resume(); // Receive the next value } delay(100); } // Extracts the raw data void extractRaw (decode_results *results) { codeLen = results->rawlen - 1; // To store raw codes: // Drop first value (gap) // Convert from ticks to microseconds // Tweak marks shorter, and spaces longer // to cancel out IR receiver distortion for (int i = 1; i <= codeLen; i++) if (i % 2) // Mark rawCodes[i - 1] = results->rawbuf[i]*USECPERTICK - MARK_EXCESS; else // Space rawCodes[i - 1] = results->rawbuf[i]*USECPERTICK + MARK_EXCESS; }

If working correctly, it should now display something like this:

1800, 400, 200, 400, 250, 350, 250, 1800, 400, 200, 400, 250, 350, 250, 1800, 400, 200, 400, 250, 350, 250,

### Step 3: Sending the signal back

The numbers printed are the exact values that need to be sent to `irsend.sendRaw`

. The only thing you’ll have to do is to store them into an array.

// Original: "1800, 400, 200, 400, 250, 350, 250," unsigned int code [] = { 1800, 400, 200, 400, 250, 350, 250 };

Air Swimmers have several controls: left, right, dive up and dive down. You have to sniff all of these inputs and save them into different arrays.

It is interesting to notice that some remote controllers are sending the same code, over and over again for a certain period of time. Errors in IR signals are very common, so that might be a technique to ensure that at least one of them reaches the target. If that’s an intended behaviour you want to replicate, you can use the following code.

// Sends a previously sniffer IR signal void sendCmd (unsigned int * code, unsigned long duration) { unsigned long timeStart = millis(); do { irsend.sendRaw(code, codeLen, 38); // 38KHz delay(40); } while (millis() <= timeStart + duration); delay(40); }

**Line 6** is the one which actually sends the code. `irsend`

is configured to use the pin 3.

### What went wrong…

The IR sniffer works amazingly well. Adding a new Air Swimmer to the swarm is relatively easy, but it need to manually detect and configure the IR messages for each signal. We wrote a web interface to monitor and control the fish remotely, and that works as well. The only problem we experienced is the fact that Air Swimmers are incredibly challenging to control. When they are in big space, they’re really impressive. But in a small room the precision you get is too low to have a real swarm simulation. Moving them randomly doesn’t seem different at all. The real issue with them is that they’re very sensitive to air flows and temperature changes. They can suddenly move making virtually impossible to know their position without an external monitoring system. Helium naturally leaks, so after twelve hours you need to fill the balloon again. Oh, and one of the Air Swimmers exploded. I mean, it literally exploded.

### Conclusion

This post explained how to hack an unknown remote controller by sniffing its IR packets. For the vast majority of applications, there is no need to understand the protocol used; messages are often independent and have no protection or timestamp. This is perfect to control a TV, a garage door or (like we did) a bunch or Air Swimmers.

#### The components

Providing that you already have an Arduino, this project can be done with less than $10. If you want to experiment with IR remotes, I advise you to get these [10 pairs of IR LEDs and IR Receivers](https://www.amazon.co.uk/Gikfun-Infrared-Emission-Receiver-Arduino/dp/B07D9C5WYS?crid=1P2S6MCQ7VMA&dib=eyJ2IjoiMSJ9.hRCubFYtBSs5_P30yI5j3jU63dZ7dFuewYDf6WOAdW1p60U6irJqWSQ3uyWLTjY6MxavEdk9iUGVGnQN4SgyAyTJVEyWKilIkHYrXXlgjktSujZN5PTp0T4y10KUZ7kdeHHDVgtoZr2ozSshyD8KO7H0N3DI8dfTxvzq6F-5TUZdhWkhBenitQ7zsDmHbtLENl0dLfrTJoEWfHn5XkfpcCKbNNu92nB5akR-9KuRYkjfJhrF9nxyilROsNHFcDKLtUMy_oLsAnr1MgHcJuNm2GeYJi0vL8q6m4093wHzX04.YwTUfOLyKZK89tIimRG9NCUcP_KJS4rzkTWv7NMEYWs&dib_tag=se&keywords=Infrared+Diode+LED+IR+Emission+and+Receiver&qid=1724357094&s=industrial&sprefix=infrared+diode+led+ir+emission+and+receiver%2Cindustrial%2C73&sr=1-3&linkCode=ll1&tag=alanzucc-21&linkId=0c1288a88d0b7cee814161622844926a&language=en_GB&ref_=as_li_ss_tl), which comes with all that you need. Alternatively, you can get the [TSOP4838](https://www.amazon.co.uk/gp/product/B00PJ80S14?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=fe4d7a0febfb05ca27e7169dfa713936&language=en_GB&ref_=as_li_ss_tl) which are qualitatively better. Resistors are incredibly cheap: I have used [180Ω](https://www.amazon.co.uk/gp/product/B004S12XHU?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=ace6ba7bb58476d9e8e164a1187cc6c3&language=en_GB&ref_=as_li_ss_tl) ones for this tutorial.

### 🪛 Recommended Components

#### Other resources

[Akkana Peck](http://shallowsky.com/blog/hardware/arduino-shark.html)‘s hacked the actual remote of an Air Swimmer and integrated it with an Arduino board;[Nano Air Swimmer](http://www.instructables.com/id/Nano-Air-Swimmer/): an instructable to create you own air swimmer for few dollars;[Brain-Controller Shark Attack](http://eeghacker.blogspot.co.uk/2015/03/brain-controlled-shark-attack.html): a more sophisticated way of controlling an air swimmer using EEG;[Operation Autonomous Flying Shark](http://www.benjones.us/operation-autonomous-flying-shark/): a more laborious approach to decode the actual protocol of the Air Swimmers;[Arduino-Air-Swimmers](https://github.com/cmptrgeekken/Arduino-Air-Swimmers): an extension of the standard controller of the Air Swimmers. This project refers to a specific producer and may not work with all types of Air Swimmers;[Augmenting the IR Controller for a Remote Control Flying Shark](http://geekken.net/wp-content/uploads/2013/03/Masters-Project-Report-Anonymized.pdf): a detailed explanation of how to decode the protocol of an Air Swimmer.

## Leave a Reply Cancel reply