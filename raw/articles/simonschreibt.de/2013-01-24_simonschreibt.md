---
title: Simonschreibt.
url: https://simonschreibt.de/gat/world-of-warcraft-balloon/
author: Simon
published: '2013-01-24'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Especially [Mists of Pandaria](http://eu.battle.net/wow/de/game/mists-of-pandaria/) has absolutely stunning assets. One of the most beautiful ones, at least in my eyes, is the hot air balloon which brings you to Pandaria. Besides the fact that it looks great, it has an very interesting graphical feature: the yellow “glow” in the center of the balloon is at the center at any time. Independent from your viewing angle! This means, the “hot” yellow area can’t just be painted on the surface of the balloon. But how is this possible?

My first suggestion was, to create a shader with a red [Fresnel effect](http://wiki.thesimsresource.com/index.php?title=Ambient). This would “surround” the whole balloon with this red vignette and with a mask you could “cut” out the patterns.

Of course, I was wrong. First of all, with the help of [DirectX Ripper](http://www.deep-shadows.com/hax/3DRipperDX.htm) and the [WoW Modelviewer](https://wowmodelviewer.atlassian.net/wiki/display/WMV/Download+WoW+Model+Viewer) I found out interesting stuff. Here the textures:

![](../../assets/f91e2fba4556d978.jpg)

**Left**: diffuse texture **Right**: alpha channel of diffuse

The first one is like expected. BUT the second is interesting. This is the gradient the use for this effect I’m describing! But how? I checked the model of the balloon in the model viewer.

Bad news: the cool effect isn’t visible there. Bad News #2: I thought the big quad in the wireframe gives a nice hint how they did it, but it’s wrong…

![](../../assets/0a6081ffc40b7949.gif)


![](../../assets/f0e93d0643efe470.jpg)

**Good News**! Thanks to [Neox](http://polyphobia.de/), we all will know the solution in some seconds. Let me explain: The technique they (Blizzard) used, can be called [Lit Spheres Shading](http://www.cs.utah.edu/npr/papers/LitSphere_HTML/node3.html). Which seems to be “just” a remapping of colors (like the [Gradient Map](http://www.ctrlpaint.com/videos/gradient-map) in Photoshop). But during the Gradient Map is just a 1D gradient (left to right), the Lit Sphere Shader uses a 2D texture (seen above, left to right, top to bottom). If you don’t understand what i mean, just checkout the [thread](http://www.polycount.com/forum/showthread.php?t=68125) from [Peppi](http://peterboehme.blogspot.de/). He also wrote this awesome shader you can download and try out by your own.

As far as I understand, they use the normals (screen space) of the object to map the colors. The more the normals “look” away from the camera (at the sides of the sphere), the outer colors are grabbed from the texture. Of course, the colors in the center of the texture are used the more the normal “looks” to the camera.

![](../../assets/77fd1b48252b3ede.jpg)


![](../../assets/8c086b2bf7886be7.gif)


![](../../assets/5bd74fd57cf1329e.jpg)


![](../../assets/ba0680151067ebbc.png)

[Charles](http://www.charles-greivelding.com/index.htm)mentioned another really interesting way to do this effect: Inverted Fresnel. Even better: he provided shader code and images! Awesome! So here’s the code which not only gives you the iFresnel effect but also supports a mask:


half fresnel = pow(saturate(dot(normal, viewDir)),sizeoftheglow);
half mask = tex2D(mymask,uv).r; // mask stored in a the R channel

half3 color = half3(mycolor); // 0.4,.02,0.01 for example

half3 selfillumfresnel = fresnel* color+(bias* color)*mask;



Here’s his example out of the UE4 engine:

And he described that Half Life 2 did it already for special monsters like this … ant-thingie (it glows from the inside):

For more details, you can [read the original comment here](http://simonschreibt.de/gat/world-of-warcraft-balloon/#comment-395).

![](../../assets/ba0680151067ebbc.png)

my best bet would be a litsphere shader

Really looks like zbrush matcaps. Interesting effect :D

For the record, the viewport shader was written by Charles Hollemeersch – http://charles.hollemeersch.net/

so what’s the difference between this and fresnel effect? Doesn’t fresnel effect use normal vectors in vew space too?

Yes this is called fresnel not a little sphere, but it doesn’t matter. Cool blog!

I would say the main difference is, that you have no texture when using fresnel, isn’t it? As far as i know, you only use one color and the fresnel will use this color where it occurs. But with the lit sphere tech you have the chance to not only define a gradiant, even more you can use a real texture and define the left/right/top/bottom color of the “fresnel” effect. That’s what i would suggest.

This comment has been removed by a blog administrator.

Huh. I made this same effect for an earlier environment. I had these big round paper lights and was messing around in the UDK material editor for awhile.

I used a camera vector piped into the UV coords of the emissive texture, and added that to an emissive fresnel function. I also made a lerp between two emissive colors to have greater control over intensities/hues of the glow.

Later on, I stumbled on Jordan Walker’s Bathhouse scene and noticed he used a very similar method for his paper lanterns, except that he added a fresnel function to his diffuse material as well.

Neat to see how other people create the effect as well, though! :)

You’re right! I already knew the bathhouse scene but now i see that he also had this nice effect. Thanks for mentioning!

Feel free to drop a screenshot of your lamps :)

To do this with really low tech one could make a balloon with inverted faces as background, have all the ornaments and borders straigt in front with alpha and the glow set to cam in the middle. I can imagine this would work too.

On the other hand I remember we had an environment map setting on the shaders in Nebula1 at Project Nomads.

That would map each pixel according to the viewing direction. A face pointing directly at you shows the env map center, as it bends to a direction the mapping shifts there in UV space too. So if you mapped a glow to a sphere: It looked the same from any direction.

Your low tech approach definitaly should work – of course it needs more geometry and you have to be able to define faces which always are camera oriented (a feature not every engine supports….no idea why not :,) ).

Oh nice to hear that you worked on Project Nomads. Then you might know Bernd Diemer, right?

Hi,

To do this the most simple way for me is to use an inverted fresenl like this : half fresnel = pow(saturate(dot(normal, viewDir)),sizeoftheglow);

Then you’ll just have to mask it by a texture :

half fresnel = pow(saturate(dot(normal, viewDir)),sizeoftheglow);

half mask = tex2D(mymask,uv).r; // mask stored in a the R channel

half3 color = half3(mycolor); // 0.4,.02,0.01 for example

half3 selfillumfresnel = fresnel* color+(bias+ color)*mask;

Here you can see it in UE4 :

[img]https://dl.dropboxusercontent.com/u/1812933/IllumFresnel.jpg[/img]

With this you can control the size of the glow and color the result with a texture and add extra light/color with the bias.

First time I saw this effect was in Half-Life 2 episode 2 for the Antlion

[img]http://img3.wikia.nocookie.net/__cb20071014171816/half-life/en/images/3/3e/AcidAntlion.jpg[/img]

You can see here the glowing coming from the inside of the beast !

I think they used that same technique in Bioshock Infinite on the big balloon.

This how I would have do it myself :).

Nice blog I really like it !

Thanks man! I thought about inverted Fresnel sometime but didn’t have an idea how to do it – til now ;) I’ll pack you code and the pictures as an update to the article – for all the people not reading the comments :)

Glad you like my blog! Oh and i saw that you did space ships for Endless Space – Cool! I do Space Ships too for X Rebirth :)

You’re welcome :).

I’ve made a little mistake in the code at this line :

half3 selfillumfresnel = fresnel* color+(bias+ color)*mask;

It’s not bias+color but bias*color.

half3 selfillumfresnel = fresnel* color+(bias*color)*mask;

Sorry for that !

Yeah I did somespace ships was a good time :). X rebirth ? Awesome :).

Thanks for adding my thought to the article !

Thank you for the correction! I updated the article :)

yes,just dot(normal, viewDirection) can simulate this effect like rim light

but this is effect is not great because it’s not stylize(like cartoon), so if used such like cartoon stylize,will still use the look up texture tech.