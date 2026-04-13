---
title: Retro CRT distortion effect in Flixel 2.5 - Alan Zucconi
url: https://www.alanzucconi.com/2012/01/31/retro-crt-distortion-effect-in-flixel-2-5/
author: Alan Zucconi
published: '2012-01-31'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

A couple of weeks ago I started using the [ Flixel Framework](http://flixel.org), a set of class and libraries in ActionScript3 to effectively design videogames in Flash. Flixel is suggested to all the programmers who want to create games with a retro-style flavour. Although there is a huge support community that actively works on Flixel, finding the right effect is not always easy. After looking for few hours desperately trying to find a way to implement a CRT distortion effect, I decided to create it myself! The result is a class called “

*RetroEffect*“.

The inspiration for this work comes from a great article by ** Cadin Batrack**, called “

**“. Although, the version I create is integrated to Flixel 2.5, and has several performance improvements that makes is lighter to execute with a high framerate. In old CRT monitors, the image is composite using three different colour layers. When they are not perfectly synchronised, the result is something like this one:**

[Create a retro CRT distortion effect using RGB shifting](http://active.tutsplus.com/tutorials/effects/create-a-retro-crt-distortion-effect-using-rgb-shifting)*Retro CRT distortion effect by Cadin Batrack*

The way this effect is implemented consists in extracting the red, green and blue channel from the original image and re-drawing them a little bit distorted. The solution proposed by Cadin Batrack uses the [Tweener](http://hosted.zeh.com.br/tweener/docs/en-us/) library. Despite its being really effective, is also extremely heavy and its usage is not advisable where performance should be an issue. I used a very light version that simply cause the channel to “oscillate” following a sinusoidal path. The effect does not reach the same *yeah-yeah level of awesomeness*, but it can be a good base for further versions.

The code that does the trick is;

[sourcecode language=”as3″]

&lt;br /&gt;<br /><br />

// Red channel ——————————————&lt;br /&gt;<br /><br />

_buffer.fillRect(source.rect, 0xFF000000);&lt;br /&gt;<br /><br />

_buffer.copyChannel&lt;br /&gt;<br /><br />

( source, source.rect, _zeroPoint,&lt;br /&gt;<br /><br />

BitmapDataChannel.RED, BitmapDataChannel.RED );&lt;br /&gt;<br /><br />

_bitmap.alpha = randRange(8, 10) / 10;&lt;/p&gt;<br /><br />

&lt;p&gt;_distortion.a = sinusoid(_counter + 0 / 5, 0.99, 1.00 , 0.5);&lt;br /&gt;<br /><br />

_distortion.d = sinusoid(_counter + 2 / 5, 1, 1.01 , 0.5);&lt;br /&gt;<br /><br />

_output.draw(_bitmap, _distortion, null, null, null, true);&lt;/p&gt;<br /><br />

&lt;p&gt;// Green channel ——————————————&lt;br /&gt;<br /><br />

_buffer.fillRect(source.rect, 0xFF000000);&lt;br /&gt;<br /><br />

_buffer.copyChannel&lt;br /&gt;<br /><br />

( source, source.rect, _zeroPoint,&lt;br /&gt;<br /><br />

BitmapDataChannel.GREEN, BitmapDataChannel.GREEN);&lt;br /&gt;<br /><br />

_bitmap.alpha = randRange(8, 10) / 10;&lt;/p&gt;<br /><br />

&lt;p&gt;_distortion.a = sinusoid(_counter + 1 / 5, 0.99, 1.00 , 0.5);&lt;br /&gt;<br /><br />

_distortion.d = sinusoid(_counter + 1 / 5, 1, 1.01 , 0.5);&lt;br /&gt;<br /><br />

_output.draw(_bitmap, _distortion, null, BlendMode.SCREEN, null, true);&lt;/p&gt;<br /><br />

&lt;p&gt;// Blue channel ——————————————&lt;br /&gt;<br /><br />

_buffer.fillRect(source.rect, 0xFF000000);&lt;br /&gt;<br /><br />

_buffer.copyChannel&lt;br /&gt;<br /><br />

( source, source.rect, _zeroPoint,&lt;br /&gt;<br /><br />

BitmapDataChannel.BLUE, BitmapDataChannel.BLUE );&lt;br /&gt;<br /><br />

_bitmap.alpha = randRange(8, 10)/10;&lt;/p&gt;<br /><br />

&lt;p&gt;_distortion.a = sinusoid(_counter + 2 / 5, 0.99, 1.00 , 0.5);&lt;br /&gt;<br /><br />

_distortion.d = sinusoid(_counter + 0 / 5, 1, 1.01 , 0.5);&lt;br /&gt;<br /><br />

_output.draw(_bitmap, _distortion, null, BlendMode.SCREEN, null, true);&lt;br /&gt;<br /><br />

[/sourcecode]

Colour channels are copied into “*_buffer*“, and all the drawing operations are made into a temporary “*BitmapData*” called “*_output*“. The sinusoid curve is feed with a counter “*_counter*” that indicates the number of seconds elapsed from the beginning of the game. You can play with the [matrix parameters](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/geom/Matrix.html) to obtain different types of effects.

The usage of this class is quite easy. It must be added as a normal sprite, specifying the camera that will be rendered with the retro CRT distortion effect. In the example below, the standard camera has been used.

[sourcecode language=”as3″]&lt;br /&gt;<br /><br />

var retroEffect : RetroEffect = new RetroEffect(FlxG.camera);&lt;br /&gt;<br /><br />

add(retroEffect);&lt;br /&gt;<br /><br />

[/sourcecode]

You can download the “*RetroEffect*” class compatible with Flixel 2.5 from [here](https://www.alanzucconi.com/wp-content/uploads/RetroEffect.rar).

## Leave a Reply Cancel reply