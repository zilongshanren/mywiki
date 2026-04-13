---
title: Simonschreibt.
url: https://simonschreibt.de/gat/cool-stuff-with-textures/
author: Simon
published: '2017-09-27'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

I gave this talk at the [Digital Art Conference 2017](https://www.dac-fra.com/) and it’s about how Textures can be used for other stuff than color. Almost all the content is based on a game I had the pleasure working on: [The Invisible Hours](http://www.tequilaworks.com/en/projects/the-invisible-hours/) from [Tequila Works](http://www.tequilaworks.com/).

Below the video you’ll find a lot of **extra content**.

![](../../assets/566be0c0eb1c3ad5.png)


![](../../assets/566be0c0eb1c3ad5.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Extra Content

Further information related to the talk can be found here. I prepared some tutorials and experiments which might be interesting to you if you liked the content of the talk.

Assets

I was allowed to publish the materials/meshes for the smoke, rain and the leaves. If there are problems with assigning material functions and textures, please have a look at the pictures which show how the materials are setup.

[Unreal Assets Zip Archive](https://data.simonschreibt.de/gat066/unreal_files.zip)

[Leaf Material (Picture)](https://data.simonschreibt.de/gat066/material_leaves_01.png)

[Rain Material (Picture)](https://data.simonschreibt.de/gat066/material_rain_01.png)

[Smoke Material (Picture)](https://data.simonschreibt.de/gat066/material_smoke_01.png)

Text

- If you liked the sprite sheet trick from
[Oskar](https://twitter.com/OskSta)(putting UVs into a texture)[you might like this article](https://simonschreibt.de/gat/007-legends-the-world/)with more information of how this “re-mapping” can be used. - I
[asked on Twitter about more ideas](https://twitter.com/simonschreibt/status/902254849882030082)how to use textures. There are many cool tricks mentioned in he answers!

Videos

Another great usecase for vectors in textures are flow maps! Here I describe how you have to setup a flow map material in Unreal:

![](../../assets/251c897cf52a2301.png)


![](../../assets/251c897cf52a2301.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Here you see an experiment I’m doing storing **two** images into **one** color channel of a texture which I mentioned during my talk:

![](../../assets/b38d0f7faaaa3a32.png)


![](../../assets/b38d0f7faaaa3a32.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

This video helps when you want to use Unreal to write the position of an object (like our cigarette) into a render target:

![](../../assets/ae6615a96e5419b1.png)


![](../../assets/ae6615a96e5419b1.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/ba0680151067ebbc.png)

That. Is. Just. Amazing!

Nice Dude… Thanks for sharing

Hei Simon

I’m so glad I found you ^^ your stuff is Hot!

I have a question concerning the smoke Effect.

When I displace the vertecies in the vertex shader, the normals will stay the same (this makes sense since im not tweaking them). But this gets problematic when I then try to do some fresnel in the fragment shader, since my normals still represent the original form of the mesh. I probably need to somehow recalculate them.

do you have a tip? maybe Unreal does this automatically, im using unity.

Kind Regards Jan

Yeah the re-calculation is always a problem. I didn’t do it for the smoke but it had to do it for the pintable. Open this article https://simonschreibt.de/gat/pintable/ and search for “re-calculate the normals”. You’ll find a little snipped from Unreal (ddx/ddy) and maybe you can replicate this in Unity?

Thank you!

I already thought that thats probably the way to go. Will definately give it a try.

Tried to recreate the Orb form Moira (Overwatch) with a Shader. The Haze is inspired by your smoke approach.

https://imgur.com/gallery/gN2J8

ty :)

Edit: I didnt recalculate the normals (might try to do that at some point using a geometryshader) but rather just faked it by setting the normal to the displacement. this also gives an interesting effect when applying some fresnel

oh cool! great work :) love it!

Hey Simon,

About the smoke effect, does storing the positions over time in an image actually improve performance over just using an array/list? Over some other data structure? What advantage does using an image have?

The problem is that I want to control/move every vertex and this I can only do via vertex shader as far as I know. And in those I don’t have access to arrays/lists or and I can’t control the verts via Blueprint. The only option I could imagine is to use bones and skin those to the vertices and then control the bones …