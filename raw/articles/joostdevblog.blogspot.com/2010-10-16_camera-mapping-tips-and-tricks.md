---
title: Camera mapping tips and tricks
url: http://joostdevblog.blogspot.com/2010/10/camera-mapping-tips-and-tricks.html
author: Joost van Dongen
published: '2010-10-16'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**1. The**

*Camera map*modifierThis is the cheap and simple hint: 3D Studio MAX has a modifier specifically for doing camera mapping and it is called, surprisingly, the

*Camera map*modifier.

**2. Do not model object edges**

The edges of the object should come from the image itself, not from your model. The reason for this is that polygons have straight, hard edges, while drawings have more blurry and zigzagging edges. You cannot really create a blurry, brushed edge using polygons. Using the image's transparency for the edges also makes modelling a lot easier, since you don't have to model the objects as precisely. The image below shows that you can even just stretch the polygons as far as you like.

![](../../assets/20d844615a1cf29b.gif)

I guess with sharp photographs of buildings it may work to model object's edges, but with the kind of art I have been working with, doing object edges exclusively through image transparency looks way better.

**3. Split into many layers**

To use transparency, you will need to split the image into a lot of layers. This greatly depends on the type of scene you are doing, but in general, the more layers you have, the easier it is to make your 3D scene. For the Evil Pope I used three layers (head, body, thorns), while for Captain August I used a whopping 28 layers! Splitting the original image into all those layers and drawing the parts behind layers was a lot of work, but was also absolutely necessary to make it look good.

![](../../assets/180ca8557e325a6a.gif)

**4. Put a curve on everything**

If you map an entire character to a flat plane, then it will look like a cardboard cut-out as soon as the camera starts moving. Putting the arms and such in separate layers is important, but it also works wonders to simply bend objects to roughly mimic the shape of the real character. Don't overdo this, though, for if you look too far from the side at an object, it will squash the lines of the original drawing too much, decreasing the 2D effect.

![](../../assets/eb9aea08504a8b1e.gif)

**5. Animating after the mapping**

Once an object has been camera mapped, you can animate it any way you like. For the little video of August, I rigged the bodies and arms of the characters with bones to be able to rotate and bend their arms and heads. This works surprisingly well, without breaking the illusion of a 2D drawing. For the Evil Pope, I was even able to change the character's expression without using any new drawings. This was done by morphing the mesh of the face into different expressions. The only things that I animated with extra textures are blinking and closing eyes. Everything else is just morphing, bending and moving the 3D models.

Last words on camera mapping for the moment: I'm thinking of trying camera mapping in a small real-time 3D game prototype to create a totally unique and awesome graphical style. I'm looking for a concept artist to design that with, so if you think you can draw a lively outdoor environment in a rough, colourful impressionistic style, maybe a little bit like

[this](http://paperblue.net/?mid=g2&page=4&document_srl=24978)or

[this](http://ronimo.hku.nl/Joost/CarlWahl%20-%20butterfluff.jpg)or

[this](http://advarsky.deviantart.com/art/The-invention-of-fire-171699378?q=gallery:Advarsky/15282021&qo=22)or

[this](http://www.mathias-huber.com/images/dsf_1542_end_of_summer.jpg)or

[this](http://paperblue.net/?mid=g3&page=7&document_srl=25276), then please do contact me at joost@ronimo-games.com!

In the meanwhile, I've headed back to working on

[Proun](http://www.proun-game.com)for a while! :)

## No comments:

## Post a Comment