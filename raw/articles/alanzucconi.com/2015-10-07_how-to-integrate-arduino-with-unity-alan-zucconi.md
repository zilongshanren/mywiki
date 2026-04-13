---
title: How to integrate Arduino with Unity - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/07/how-to-integrate-arduino-with-unity/
author: Alan Zucconi
published: '2015-10-07'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

In this tutorial you will learn how Unity and Arduino can communicate using the serial port. This tutorial requires both C# and Arduino scripts; the labels

and will be used to avoid confusion.- Step 0:
[Configuring…](https://www.alanzucconi.com#step0) - Step 1:
[Opening…](https://www.alanzucconi.com#step1) - Step 2:
[Writing…](https://www.alanzucconi.com#step2) - Step 3:
[Reading…](https://www.alanzucconi.com#step3) - Step 4:
[Communicating…](https://www.alanzucconi.com#step4) [Conclusion](https://www.alanzucconi.com#conclusion)

The topic of connecting Arduino to Unity is further expanded in [Asynchronous Serial Communication](https://www.alanzucconi.com/?p=5844), where you can also download the entire Unity package.

The communication between Arduino and the PC is mediated using the serial port. This method is the default one to upload sketches, so we’ll be using it also to exchange messages with Unity. If this is the first time you are doing it, you’ll need to follow these extra steps.

![bbb](../../assets/af3af35d243514c8.png)

`SerialPort`

is the one that mediates such communication in C#. However, Unity doesn’t usually include the necessary libraries to use it. To compensate for this, we need to force Unity to include the full .NET 2.0 library in its executables:

- Go on
**Edit**|**Player Settings**to open the**PlayerSettings**in the inspector; - From
**Optimization**, look for**Api Compatibility Level**and select**.NET 2.0**.

[Steven Cogswell](http://awtfy.com/)‘s [ArduinoSerialCommand](https://github.com/scogswell/ArduinoSerialCommand) library. Follow these steps to install it:

- Download the entire repository by clicking “
[Download ZIP](https://github.com/scogswell/ArduinoSerialCommand/archive/master.zip)” from its GIT page; - Extract the ZIP file and place its content in
`C:\Users\<username>\Documents\Arduino\SerialCommand\`

(make sure that folder contains the SerialCommand.cpp file); - Restart the Arduino IDE.

*port*) and speed (also called *baud rate*).

using System.IO.Ports; stream = new SerialPort("COM4", 9600); stream.ReadTimeout = 50; stream.Open();

While the baud rate is determined by the Arduino code, we cannot chose the name for the serial port. It is automatically assigned by the OS depending on which device and port you are using.

**Now that **`SerialCommand`

has been installed, we can use it in our sketch. The library allows to specify commands that can be received on the serial port. For this toy example, we want to define a command called “PING”. When we receive such string from Unity, we’ll send a “PONG” back. Let’s start by defining the command; its code will be stored in the `pingHandler`

function.

#include <SoftwareSerial.h> #include <SerialCommand.h> SerialCommand sCmd; void setup() { Serial.begin(9600); while (!Serial); sCmd.addCommand("PING", pingHandler); }

The `9600`

used to initialise the serial port represents its baud rate. This value must match the one used in the C# script.

Writing a string to the serial port in C# is relatively easy.

public void WriteToArduino(string message) { stream.WriteLine(message); stream.BaseStream.Flush(); }

If there is a problem, `WriteLine`

will throw a `IOException`

(read more [here](https://msdn.microsoft.com/en-us/library/7ack4zyt(v=vs.110).aspx)). We flush the stream to make sure the data it sent to the Arduino, without any buffering. Following our toy protocol, we should send a “PING” to Arduino.

WriteToArduino("PING");

`SerialCommand`

library takes care of reading strings from the serial port for us. To do this, we need to update the `loop`

function.

void loop () { if (Serial.available() > 0) sCmd.readSerial(); }

The function `readSerial`

is the one where the magic happens; it reads strings from the serial port and invokes the right handler. If it receives a “PING”, it will execute `pingHandler`

:

void pingHandler (const char *command) { Serial.println("PONG"); }

This will write “PONG” on the serial port. You can also use `Serial.println`

to send data from Arduino to Unity at any time.

`stream.ReadLine()`

function.

public string ReadFromArduino (int timeout = 0) { stream.ReadTimeout = timeout; try { return stream.ReadLine(); } catch (TimeoutException e) { return null; } }

However, there’s a catch. How long do you want to wait for before considering the read failed? If you are waiting indefinitely for Arduino to send data, this might block the execution of your program. Reading from the serial port is, essentially, a *system call* and can introduce lag. A lot of lag. To avoid this, we should do very quick reads alternated by quick waits. In order to implement an asynchronous waiting mechanism, we have to use *coroutines*.

public IEnumerator AsynchronousReadFromArduino(Action<string> callback, Action fail = null, float timeout = float.PositiveInfinity) { DateTime initialTime = DateTime.Now; DateTime nowTime; TimeSpan diff = default(TimeSpan); string dataString = null; do { try { dataString = stream.ReadLine(); } catch (TimeoutException) { dataString = null; } if (dataString != null) { callback(dataString); yield break; // Terminates the Coroutine } else yield return null; // Wait for next frame nowTime = DateTime.Now; diff = nowTime - initialTime; } while (diff.Milliseconds < timeout); if (fail != null) fail(); yield return null; }

Which can be invoked like this:

StartCoroutine ( AsynchronousReadFromArduino ( (string s) => Debug.Log(s), // Callback () => Debug.LogError("Error!"), // Error callback 10000f // Timeout (milliseconds) ) );

The code below starts the `AsynchronousReadFromArduino`

coroutine, passing three arguments. The first one is a function (created on the spot) which get the string read from Arduino and logs it. The second one is a callback if the reading fails, and the third one is the timeout (10 seconds).

There are cases in which you might want to send parameters from Unity to Arduino. Let’s do this with an echo function.

void echoHandler () { char *arg; arg = sCmd.next(); if (arg != NULL) Serial.println(arg); else Serial.println("nothing to echo"); }

We can use the function `next`

to get the next argument provided on the serial command. For instance, if we send from Unity “ECHO message”, “message” will be the first parameter. If `next`

returns `NULL`

, it means there are no more parameters.

Now that all the pieces are here, you just have to implement your own communication protocol. Arduinos are usually used as sensors, constantly sending updates to Unity. If this is your case, you should not make the mistake of doing something like this:

void loop () { // Get data // ... Serial.println(data); }

Is very likely that this will overflow the serial port buffer, causing either a crash or a severe lag. What you should do instead is creating a protocol in which Arduino is sending data only when is queried by a “PING” from Unity. This ensures data is always fresh and minimises lags.

### Downloads

This article presented a simple, yet effective way to connect Arduino with Unity. The necessary files are available for download on Patreon, in two versions:

[Basic Version](https://www.patreon.com/posts/35519199): The Unity and Arduino code presented in this tutorial.[Advanced Version](https://www.patreon.com/posts/35519472): A complete library to fully integrate Unity and Arduino which users thread for an efficient two-ways asynchronous communication. This solution is discussed in the post titled[Asynchronous Serial Communication](https://www.alanzucconi.com/?p=5844).

Last year at GDC a guy approached me and asked my opinion about UNIDUINO, an extension to connect Arduino with Unity. It was only after I said something on the line of “*I would never pay so much to use it*” that he introduced himself as [the creator](https://twitter.com/edwonia). Despite this not-so-great start, our conversation highlighted an important issue when it comes to development: how much time are you willing to invest into something? Many software developers have little to no experience with hardware, and they rather spend €32 than a week of headaches to connect Unity to Arduino. To ~~mis~~quote [Mike Bithell](https://twitter.com/mikeBithell) during his talk at Develop Brighton a couple of years ago, some developers have “*more money than time*“, If you are going to use an Arduino for your project, you definitely need to invest some money in it. But if you think paying for an extension is out of your budget, this tutorial is definitely here to help. Despite not providing the full range of functions of UNIDUINO, it is surely a good starting point which will suit the majority of applications.

### ⭐ Recommended Unity Assets

#### How to start with Arduino

The most annoying part of working with hardware is that you’ll constantly need new components to build things. If you are new to Arduino, my advice is to start with the [Arduino Serial Starter](https://www.amazon.co.uk/gp/product/B009UKZV0A?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=12dc4625b3b7b0ba9041fbcedde89038&language=en_GB&ref_=as_li_ss_tl). It has a lot (I mean… a lot!) of components and it comes with some great instructions. If you have a little bit more experience, you might want to buy the components you need separately. In this case, the [Arduino Uno](https://www.amazon.co.uk/Arduino-A000066-ARDUINO-UNO-REV3/dp/B008GRTSV6?hvadid=696285193871&hvpos=&hvnetw=g&hvrand=4374145136306136551&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9198127&hvtargid=pla-2281435178098&psc=1&mcid=304462499042351b84f41e79bb5a5994&hvocijid=4374145136306136551-B008GRTSV6-&hvexpln=74&gad_source=1&linkCode=ll1&tag=alanzucc-21&linkId=47f5a1a343bd0159d9783be2d22e3825&language=en_GB&ref_=as_li_ss_tl) is the “default” option you should go for.

### 🪛 Recommended Components

If you have already experience with hardware, I advise you to start using [Teensy 4.1](https://www.amazon.co.uk/Teensy-4-1-Without-Pins/dp/B088D3FWR7?pd_rd_w=kiIHf&content-id=amzn1.sym.fd0b82fb-e9ae-42a5-94a3-41ec499cc326&pf_rd_p=fd0b82fb-e9ae-42a5-94a3-41ec499cc326&pf_rd_r=P0821BF3MGDAPC45QFP9&pd_rd_wg=JN4sE&pd_rd_r=177565f2-ed11-4588-aab2-bdd123eecce3&pd_rd_i=B088D3FWR7&psc=1&linkCode=ll1&tag=alanzucc-21&linkId=89c48a6cb2a909335ff6b7d71b6a122b&language=en_GB&ref_=as_li_ss_tl) instead. It’s a micro-controller fully compatible with the Arduino IDE. It’s compact and more powerful, although it usually doesn’t come with pins. I also suggest a book I particularly liked: [30 Arduino Projects for the Evil Genius](https://www.amazon.co.uk/gp/product/0071817727?ie=UTF8&linkCode=ll1&tag=alanzucc-21&linkId=720c6a0b762973d3badb285037108e46&language=en_GB&ref_=as_li_ss_tl). I got it few years ago and it helped me to understand how to use all the most common components.

## Leave a Reply Cancel reply