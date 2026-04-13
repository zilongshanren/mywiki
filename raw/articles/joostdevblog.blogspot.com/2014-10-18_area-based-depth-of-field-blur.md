---
title: Area based depth of field blur
url: http://joostdevblog.blogspot.com/2014/10/area-based-depth-of-field-blur.html
author: Joost van Dongen
published: '2014-10-18'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Cello Fortress](http://www.cellofortress.com)I came up with a new technique for depth of field blur: area based depth of field blur. As far as I know this is not an existing technique so today I would like to explain how it works.

The visual style for Cello Fortress is far from finished at the moment, but I decided early on that I wanted strong depth of field blur to play a major role. I had already implemented depth of field blur for

[Proun](http://www.proun-game.com)(which by the way is coming to 3DS, iOS and Android soon!) and I copied that to Cello Fortress. Proun does not have blur on the foreground, so I added that and tried it in-game. The result turned out to not work at all, as you can see in this image (be sure to click the image for a larger version, since this is difficult to see in these small blog-sized images):

![](../../assets/faddd1f22ce459f2.jpg)



![](../../assets/faddd1f22ce459f2.jpg)

*click for larger image*The problem is that with standard depth of field blur, only one specific distance to the camera is sharp. In Cello Fortress the camera looks down on the battlefield diagonally, which means that that specific distance looks like a circle. Even weirder is that the part of the screen that is closest to the camera is almost at the centre of the screen: that is the spot the camera hangs exactly above. The result is that both the edges of the screen and the centre are blurred. Of course it is totally undesired that the centre of the gameplay would be blurry.

A simple solution I then tried was to broaden the area that is sharp:

![](../../assets/afc135c140276325.jpg)



![](../../assets/afc135c140276325.jpg)

*click for larger image*![](../../assets/b0e3ad22f85829f1.jpg)



![](../../assets/b0e3ad22f85829f1.jpg)

*click for larger image*The goal was to have strong depth of field blur as a core part of the visual style for Cello Fortress. So far we either have depth of field blur that interferes with the gameplay, or no depth of field blur at all in the foreground. We need something better:

![](../../assets/88a8b7fbd2366d55.jpg)

Once I drew where I wanted blur I realised that this is a simple shape: in world space this is just a simple axis-aligned box. So I implemented a shader that calculates the strength of the depth of field blur based on its distance to that 3D box, instead of distance to the camera. The result is exactly what I was looking for:

![](../../assets/7e2b7c9d56738fe4.jpg)



![](../../assets/7e2b7c9d56738fe4.jpg)

*Click for larger image.**Note that the effect is exaggerated in the smaller screenshot above, the full-res version has the normal, slightly less extreme blur.*

A big benefit of this technique is that tweaking it is really straightforward, and that it is independent on the camera. I can easily set the sharp area from code based on the gameplay situation. It also gives me precise control over the height at which the blur starts.

Technically area based blur is quite easy to do. The depth of field blur shader already uses a render-texture that contains the depth of each pixel to the camera. I don't use this depth for anything else, so I can put any value I like there. The pixel shader can easily be adjusted to calculate depth in a different way.

![](../../assets/dafda85594cb3a57.jpg)

This concept can also be applied to other shapes than boxes. For example, you can also have a sphere within which everything is sharp, while everything outside that sphere is blurred. One can even have several such spheres. How about a visual style where everything is blurred except for the areas around the characters? I think some other interesting visual styles can be made this way, especially in combination with very strong blur.

I have seen some games that use non-distance based depth of field blur, like the beautiful

[Below](http://vimeo.com/68314832), which seems to simply blur the top and bottom of the screen. I am not aware of games that use a 3D area as I use it. Let me know if there are other games that already do this.

The fun of writing your own shaders is that you can bend them to do whatever you want, including weird and unrealistic effects like doing my depth of field blur based on a 3D box area. Feel free to use this idea in your own games, and I'd love to hear from you if try it out!

## No comments:

## Post a Comment