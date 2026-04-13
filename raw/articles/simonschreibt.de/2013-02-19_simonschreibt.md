---
title: Simonschreibt.
url: https://simonschreibt.de/gat/assassins-creed-3-bouncing-light/
author: Simon
published: '2013-02-19'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

A basic outdoor light setup would contain a reddish sun and a blueish ambient light to fake some global illumination of the sky. But in [AC3](http://assassinscreed.ubi.com/ac3/en-us/index.aspx) i noticed a third source of light: bouncing light. It’s just the sun light coming back from the ground.

I don’t know how they did it, but i would guess they just created a third light on the opposite site of the sun & below the ground. Because you don’t want to have the ground shadows affected by this light.

![](../../assets/4ef8613d7d63c897.jpg)


![](../../assets/03037e206d99388e.jpg)

**Left**: Sun + blue ambient light source. **Right**: Sun + Ambient + “Bounce” light source.

I tried to find out if UDK has something like this in their light settings so you wouldn’t need to create a 3rd light source but i couldn’t find it on the first look. Feel free to drop a comment if you know how this is done on modern engines.

![](../../assets/ba0680151067ebbc.png)

[gamepat](http://gamepat.de/portfolio/)&

[Félix](http://felixenfeu.blogspot.de/)we have some links to look at! Visit the comment section (also for their text) or check the links directly:

[Crytek Global Illumination Paper](http://www.crytek.com/download/20100301_lpv.pdf)

[UDK GI Movie](http://www.youtube.com/watch?v=vPQ3BbuYVh8)

[Crytek GI Movie](http://www.youtube.com/watch?v=9WyOH23-fwo)

[Blender GI Movie](http://www.youtube.com/watch?v=xsV9Ln_TLa8)

[Mirrors Edge Light Presentation](http://fr.slideshare.net/DICEStudio/henrikgdc09-compat)

don’t know if Assassins has this (mught just be a cheap fake), but several engines now have indirect illumination:

http://www.crytek.com/download/20100301_lpv.pdf

http://www.youtube.com/watch?v=vPQ3BbuYVh8

http://www.youtube.com/watch?v=9WyOH23-fwo

Thanks :) I added these links to the post.

Really looks faked with a third light. Usually, light will bounce on an object using the color of what it bounced from. So with the color of the ground, the color bouncing should be brown’ish/green’ish.

UDK, Cryengine, frostbite, unity and all recent engine have GI (Even Naughty Dog engine looks like it has GI, especially in Last Of Us), and it works great, not like what’s in AC. Frostbite being the best exemple IMO (Last video Gamepat linked).

There is a nice exemple too being made in Blender : http://www.youtube.com/watch?v=xsV9Ln_TLa8

And there is the Mirror’s Edge trick :

http://fr.slideshare.net/DICEStudio/henrikgdc09-compat

Thank you! I added you links & name to the post :) The ME presentation is awesome. Would love to hear what they said during showing this :)

We have some bounced lighting from the flashlights in The Last of Us but our overall lighting is achieved through lightbaking and light probes that sample values at different locations and interpolate between them to apply color values to things in the environment. A full on runtime GI would most likely not be doable on the current hardware this game runs on.

Having a third light would not really be faking it because that light would have to be a dynamic process that would have to factor all sorts of color information. My guess (albeit still costly to store) would be light bakes with the data in a lookup table and interpolating between those values based on different factors like time of day and maybe if it was starting to rain with more cloud cover. All very stateful though. I feel like I’m being intrusive with my reply so I apologize for that :P

Hi Doug, first of all: you’re totally NOT intrusive! For me (and hopefully other readers too) it’s great when people comment here and even more great when they know something and share their knowledge!

So with lookup table you mean a small texture with some color values in (bright yellow, dark blue depending on day time) and every surface pointing away from the sun would be tinted with it?

Well the LUT would contain color information but it wouldn’t be in the form of a texture. Most likely just a bunch of numerical data that could be read as color information.I know that sounds like a texture still but i think its not as expensive as a texture on memory. The sun would be positioned in maybe three different positions. Early morning. Midday. And late evening. Then the lighting is all baked into 3 different maps and then all three of those maps then have their data stored in one single LUT. Then you would interpolate between the values based on the time of day is my guess. Of course then you might have the night cycles in there too. I’m only speculating here though.

Sounds logical :) Remembers me on a tech of color adjustement where you make a screenshot, change the colors how you like in Photoshop and then the game stores the difference somehow and is able to blend the different post process steps.

It’s not a problem to speculate, that’s what i’m doing here all the time. Until a developer of the specific project writes some comments and tells me how it “really” works. This is the best which can happen but unfortunately it happens not very often. So i’m very happy that you as a next gen dev share your knowledge with us :)

I guess a link to Michał Iwanicki’s SIGGRAPH 2013 presentation Lighting Technology of “The Last of Us” is appropriate in the context of this thread.

Wow, thanks for the link! :)

Yep that’s a cool and often used trick I guess. I also use a “bottom light” in 3dsMax when presenting assets. Its a quit subtile one, but I only use it to avoid 100% black shadows when working with directional lights.

This gives me the possibility to use very intensive shadows without loosing texture- or shape-information of my mesh.

Anyway, sweet you figured out that it’s used in games too.

Cheers

Oh i didn’t say that they did it that way. I have no idea, maybe they’ve some other fancy tech. But for me it looked like that and even if not, it’s a nice “fake” for engines without any GI calculation.

Hi, very nice. I love your site. Maybe this article about lighting in Crysis 3 is interesting for you. It is the same way you’re describing here, but in a more technical matter and with some other great techniques:

http://crytek.com/download/gdce2013_shining_the_light_on_crysis_3_donzallaz_final_plus_bonus.pdf

That PDF is just crazy! Have to read it in more detail later, but it’s so full of awesome tech details :) Thank you very much! And thank you also for liking my blog :)

Post up this article on AC4’s GI light probes! Probably how they did it in AC3 (with major improvements of course)

https://m.youtube.com/watch?v=SMTj3J4H6Gk&t=1m37s

thank you for the link! very cool!