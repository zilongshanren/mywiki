---
title: How to Build a Heater with Arduino - Part 1 - Alan Zucconi
url: https://www.alanzucconi.com/2016/08/02/arduino-heater-1/
author: Alan Zucconi
published: '2016-08-02'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This tutorial will explain how to build a portable heating device with Arduino. If you’re an amateur astronomer, this can be the perfect way to prevent the formation of dew on your mirrors and lenses. In my specific case, I’ve built one of those mini heaters to warm up a formicarium. Whether it’s for your feet or for your cold-blooded pets, building a heater is easy and cheap.

[Introduction](https://www.alanzucconi.com#introduction)[The Theory](https://www.alanzucconi.com#step0)- Step 1.
[Dissipating the Heat](https://www.alanzucconi.com#step1) - Step 2.
[Building the Ladder](https://www.alanzucconi.com#step2) - Step 3.
[Switiching to Main](https://www.alanzucconi.com#step3) [Conclusion](https://www.alanzucconi.com#step4)

The second part of this tutorial ([How to Build a Heater with Arduino – Part 2](https://www.alanzucconi.com/?p=5369)) will explain how to use a temperature sensor to maintain a desired temperature.

It’s safe to assume that we’re all familiar with electric heating devices. Whether it’s a toaster or an oven, the underlying mechanism is the same. The current drawn from the socket is somehow transformed into heat. This phenomenon occurs even in situations in which is not desirable. Your laptop, for example, can warm up significantly when is performing intensive computation. The flow of electricity seems to be somehow related to heat. As a massive oversimplification, this happens due to a property of all materials, called **electrical resistance**. You can imagine the resistance as an obstacle that the current has to overcome when flowing through a conductor. **Resistors** are electrical components designed to have a specific resistance. When attached to a battery, resistors will dissipate some of the energy they receive as heat. In a nutshell: resistors get hot. How hot they can get, mostly depends on the amount of current that flows through them.

The temperature of a resistor depends on many factors, from the room temperature to the rate at which air is flowing. The resulting increase in temperature can be hard to predict and to replicate reliably. Generally speaking, is not very useful to describe the heat produced by an electrical component in terms of degrees. What is more reliable is the amount of power that is dissipated, which is measured in **Watts**. But how “hot” is a Watt? The question doesn’t really make sense in its current formulation; but you can still get your head around it if you think about the following scenario. A traditional light bulb converts only 10% of the energy it receives into light; the rest is dissipated into heat. A ![Rendered by QuickLaTeX.com 60W](../../assets/897d83e531cd04dc.png)

![Rendered by QuickLaTeX.com 54W=60W*90\%](../../assets/c3f466c699d0d0c0.png)


For the purpose of this tutorial, we want to create a heater that dissipates ![Rendered by QuickLaTeX.com 3W](../../assets/74e20041b3b31428.png)

![Rendered by QuickLaTeX.com 9V](../../assets/97de3250d26ca499.png)


![Rendered by QuickLaTeX.com \[V=I\cdot R\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-c92a49fc33c53645d395378560e9a847_l3.png)


![Rendered by QuickLaTeX.com \[P = V\cdot I\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-33b46b89c61b1c32487b70e57cdb6b45_l3.png)


The first one relates the voltage of a circuit (![Rendered by QuickLaTeX.com Volt](../../assets/059d3b58c4a1084c.png)

![Rendered by QuickLaTeX.com Ampere](../../assets/ff80161391352997.png)

![Rendered by QuickLaTeX.com Ohm](../../assets/4511e86f7b3e6ece.png)

![Rendered by QuickLaTeX.com Watt](../../assets/cfc7e5d76b553154.png)


We can merge the two to obtain a single equation that has exactly what we need:

![Rendered by QuickLaTeX.com \[R=\frac{V^2}{P}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-cb3417fa23c15f1fb932f60c147a2cb9_l3.png)


By plugging the values from our setup, we discover that a resistance of ![Rendered by QuickLaTeX.com 27\Omega = \frac{9V^2}{3W}](../../assets/702bdd156a9f8b77.png)

![Rendered by QuickLaTeX.com 3W](../../assets/74e20041b3b31428.png)

![Rendered by QuickLaTeX.com 9V](../../assets/97de3250d26ca499.png)


### 🪛 Recommended Components

If we decide to use a single resistor, we’re forcing it to dissipate all those 3 Watts of power. Standard resistors are usually graded for ![Rendered by QuickLaTeX.com \frac{1}{4}](../../assets/f54c2c877abf9ead.png)

![Rendered by QuickLaTeX.com \frac{1}{2}](../../assets/5eb02ffe6fc76818.png)


The easiest solution to overheating is simply dissipating those ![Rendered by QuickLaTeX.com 3W](../../assets/74e20041b3b31428.png)

![Rendered by QuickLaTeX.com \frac{1}{2}=0.5](../../assets/fe31bad32149af5f.png)

![Rendered by QuickLaTeX.com 6=\frac{3W}{0.5W}](../../assets/a161a3ae05c31ab5.png)

![Rendered by QuickLaTeX.com 0.5W](../../assets/bb15918ae13be77b.png)

![Rendered by QuickLaTeX.com 0.49W](../../assets/33636701ced0ed8e.png)


We now know that we need 12 resistors, and that they have to somehow sum up to ![Rendered by QuickLaTeX.com 29\Omega](../../assets/36762254e863b9c7.png)

![Rendered by QuickLaTeX.com 2.41\Omega=\frac{29\Omega}{12}](../../assets/5eb2cf188ac1cab9.png)


Heating strips are usually made by connecting all the resistance in parallel, arranged in what is called a **resistor ladder**. To do this, each resistor will need ![Rendered by QuickLaTeX.com 348\Omega = 29\Omega \cdot 12](../../assets/94ec75f3f0fd0070.png)


![IMG_20160731_130421](../../assets/d6bff8f278b91094.jpg)

Depending on the resistors that are available to you, your setup might be slightly different. I ended up using twelve ![Rendered by QuickLaTeX.com 330\Omega](../../assets/088753956428c5d9.png)

![Rendered by QuickLaTeX.com \frac{1}{2}W](../../assets/e7dec0ee21a9f5e1.png)

![Rendered by QuickLaTeX.com 2.9W](../../assets/c9f02626c74e8417.png)


![wire1](../../assets/b5f9d37f043d4ff3.gif)

A standard ![Rendered by QuickLaTeX.com 9V](../../assets/97de3250d26ca499.png)

![Rendered by QuickLaTeX.com 500mAh](../../assets/cf6ab76b5d52e840.png)

![Rendered by QuickLaTeX.com 0.5A](../../assets/de32b194375b7ca0.png)

![Rendered by QuickLaTeX.com 0.3A=\frac{3W}{9V}](../../assets/ec3b4049559408f5.png)

![Rendered by QuickLaTeX.com 9V](../../assets/97de3250d26ca499.png)

![Rendered by QuickLaTeX.com 1.7h=\frac{0.5A}{0.3A}](../../assets/dce232dc95be1208.png)


Working with electricity can be dangerous. When you’re sure that your design works, you can improve it by providing power from the socket. The main supply voltage in the UK is 240V; touching a bare wire can kill you. If you want to be safe and worry about about running out of power, you should connect your resistor ladder to a phone charger. Chargers are usually rater for ![Rendered by QuickLaTeX.com 5V](../../assets/130628906f28dea9.png)

![Rendered by QuickLaTeX.com 0.5A](../../assets/de32b194375b7ca0.png)

![Rendered by QuickLaTeX.com 500mA](../../assets/f214558ff91e5fbf.png)


If you’re looking for a quick, plug-and-play equation, this is what you need:

- Decide how many Watts of power

you need to dissipate; - Check the wattage

of your resistors; - Check the voltage

of your power supply; - Calculate how much resistance you need to dissipate the desired power:

; - Calculate how many resistors you need:

; - Calculate the resistance

you need for the

resistors in your ladder:

.

The next part of this tutorial will show how to add a temperature sensor to the design to keep the temperature stable.

## Leave a Reply Cancel reply