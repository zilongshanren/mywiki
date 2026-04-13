---
title: Simonschreibt.
url: https://simonschreibt.de/gat/sacred-2-pulse-shader/
author: Simon
published: '2013-02-05'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

A light has two states: **ON **and **OFF**. To define a blinking light you have to define a time it shall be on and a time it shall be off. But in [Sacred 2](http://www.sacred2.com/) we had the additional parameter “delay”. I’ll explain it later. First, watch how the shader looked in the game.

What you see here, is our pulse shader. The color the glowing part was set in the diffuse texture. The intensity was defined in the specular alpha. *But* this shader used an additional RGB “pulse” texture:

This is the texture of the asset you saw above. Below the big version (RGB) you can see the separate channels. And every one has a special meaning:


R: Delay

G: Length ON

B: Length OFF

You need a basic time constant, let’s say: 1s. This is your maximum duration a pixel can be on/off. A color value of 255 would mean: 1 second duration.

To make a blinking light, you don’t need the delay value (R channel). You could make the green & blue channel white (on/off length would be equal) and it would look like this:

![](../../assets/27071032dd5602f0.gif)


![](../../assets/19b3f09efb4153ee.gif)


“But Uncle Simon…why do you waste a channel for this delay thingie, when you only need two channels to do the blinking?”


You need this delay parameter for doing these “moving” light animation you saw in the first picture. Because, every light strip shall be on/off for the *same *time but *at* a different time.

An nice note about Sacred: you can extract the zip files in the \pak\ folder to get all the DDS files. Also you can read every shader because the uncompiled versions lay in the shader directory.

Found the shader and got some ideas. Do I interpret correctly that xyz is rgb when it comes to delay/on/off values?

R: Delay

G: Length ON

B: Length OFF

is it that what you meant?

Yes, but in the shader code RGB isn’t used, but XYZ is. And it is used in places where RGB should have been used.

I’m not a coder but i would assume that :)

In GLSL a vector has several access points which are able to point to the same value, for instance ‘xyz’ is the same as ‘rgb’. You are also able to ‘swizzle’ these values for instance ‘zxy’ or ‘brg’.

Thank you for clearing this out :)

I just discovered this blog. Let me just say it’s an amazingly useful resource :D

I have one question though: I’ve implemented a shader for this in the past and just used a gradient “glow map”. The way it works is more or less like but with 2 numbers indicating a range where the glow will show (for instance, 0.5 to 0.8). I then send these values to the shader every frame and I can control precisely which ranges get lit up. Why do you think they used such a “complex” method?

Thanks you very much! Good to hear that you like what i’m doing.

I’m not sure if i totally understood what you did with your shader. In the case of Sacred i guess it was the solution which offered most control without tweaking any values in the shader. But that’s just a guess. Of course i worked on Sacred 2, but i wasn’t there when the Shader was “born”. :)

Now that I’m looking at this more closely I noticed this way makes it a lot easier to implement more complex effects. Nevertheless I quickly rebuilt my own glow shader and recorded an example of it working with a really simple scenario. Keep in mind this was just thrown together for demo purposes.

Eeeh it seems the link was missing on that last post for some reason: http://imgur.com/a/Q6Mql

Thanks for this example!

One advantage of the “more complex” Sacred 2 solution could be, that you can define the blinking frequency/”off time”. As far as i get it, you would cycle in your shader with the same timing all the time, right? So you could paint some LEDs but the blinking frequency would always stay the same for all LEDs (independent if they are “marked” e.g. with rgb(10,10,10) or rgb(60,60,60)). But to be honest: this is a feature not many games would need :)