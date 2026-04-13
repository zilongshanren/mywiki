---
title: Simonschreibt.
url: https://simonschreibt.de/gat/windows-ac-row-ininite/
author: Simon
published: '2014-04-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

I’m neither a carpenter nor a stalker but i strongly love windows. Allow me to show you the most advanced windows i ever saw a game.

![](https://data.simonschreibt.de/gat048/banner_windows_ac.jpg)


The NPCs in [Assassins Creed 3](http://assassinscreed.ubi.com/ac3/en-us/index.aspx) definitely suspect that [Connor](http://assassinscreed.wikia.com/wiki/Ratonhnhak%C3%A9:ton) is a stalker because we made him stare at windows for hours in the [last article about windows.](http://simonschreibt.de/gat/assassins-creed-3-windows/) Just for you to remember, this is how windows looked in the game:

The interior is like a smooth texture which tiles and is moved via [Bump Offset Mapping](http://en.wikipedia.org/wiki/Parallax_mapping) to fake some parallax movement. At least i believe so, because there’s a guy who explains [how it can be done in UDK](https://www.youtube.com/watch?v=F7N2QDCx7kY).

For [Assassins Creed](http://assassinscreed.ubi.com/en-gb/home/) this “blurry” texture is in my eyes the perfect solution because it gives the glass a frosted/milky look which totally fits into the time where the game plays – but there are other ways to do windows and this article is about those.

![](../../assets/c2d339354e51fe32.jpg)


[Saints Row](http://www.saintsrow.com/de) is a crazy game. Even the windows are crazy (good)! Some windows have a similar parallax effect like in Assassins Creed – but with *sharp* textures instead of smooth ones. I wouldn’t have thought that it works *that* well:

Texture-Time! what you see is the “Barber (Night)” texture (see below) but isn’t there something missing? Yes, the posters!

They are a layer on top of the room texture. Below you can find the poster-texture.

Even now when i write this article and look at the GIF i’m just thinking “Wow…works so great!”. Only in really narrow angles it gets visible that *something* is weird with the interior.

Also nice: when you have closer look you can see that the texture is tiling (like in Assassins Creed) and even this looks perfectly OK, because it results in a room corner. Nothing weird about that, right? Below a non-ingame demonstration of that effect:

Here an ingame-example. Works great, doesn’t it?

I hope you like it as much as i do. :) But we’re not done yet! Let’s visit Elizabeth.

![](../../assets/766834c057851d7b.jpg)


Now let’s get to one of the most advanced windows implementations. What do you see here?:

It just looks like a wooden room containing some objects at billboards/planes to get some nice prallax effects, right? But not only Lino suspected something here:

Sidenode for those who don’t know the game: The level designers placed points where Elizabeth can interact with the environment – a really cool feature! But what she’s not doing (but Lino did) is looking at this from another angle:

That’s unexpected, isn’t it? If would be “just” glass + billboards, shouldn’t we

**a)** see through to the other side and

**b)** still notice the billboards ?

Short answer: It’s another crazy shader trick. Except from looking at the geometry-wireframe i found the “proof” in one of the textures. I did a subtle mark:

I’m not sure what the other channels are about (i suspect it’s the glass distortion because you only need two channels for such a normal map) but the red channel definitely marks the eagle-area which looks like a sprite/billboard. And how does the actual texture looks, which is controlled/masked by this channel?

But wait! When the eagle-area moves a bit faster than the four guys in the background (when i strafe around)…why is there no gap? Like when you photoshop an image and want to move an object, you have to cut it out, move it and then *fill* the now uncovered area with something…that’s why there’s another texture just for the background:

Except from the exciting double-use of (i think) bump-offsets for the *two* parallax-layers, there are two other interesting details:

**1.** If we look at the following GIF (again) we’ll see that the glass has kind of a [total-reflection](http://en.wikipedia.org/wiki/Total_external_reflection) (you can’t look “inside” anymore from narrow angles, you just see a blueish reflection). In my eyes this is a good way to

**a)** make the glass look more realistic

**b)** avoid any visible texture-deformation at narrow angels like we could observe in SR3.

**2.** The eagle-area turns at the player-camera even if it’s not a “real” billboard! How cool is that? Look carefully and you’ll see that it’s always oriented to you:

So we saw epic shaders crafted by code magicians but … why? Why not just use a “simple” glas shader and build the interior by hand? I’m sure there are more answers to this but i see two major reasons:

**1.** Adding such a shader to a surface and let the code do the rest is surely extremely time saving in comparison to building all this by hand. Especially when it comes to global changes where you want to change all windows/interiors at once.

**2.** Transparency. To render transparent objects is expensive and produces artifacts e.g. in combination with fog (see [this article](http://simonschreibt.de/gat/assassins-creed-3-lod-blending/) as an example). I don’t know if the above shaders are cheaper than doing it with real transparency, but at least i would assume that you don’t run into sorting problems – which would be a good thing, right? :)

As every time, feel free to comment or [mail](mailto:simon@simonschreibt.de) or [twitter](https://twitter.com/simonschreibt) me and share your knowledge. :) I’m sure there are a lot people out there which can explain in detail why it’s better to do it the mentioned way.

You got to the end of this article. Thank you very much for taking the time!

* Thx again to InvisGhost and Lino for suggesting the topic

* Thx Knobby and Minimaul for all the help in the SR3 Forum

* Thx to all for reading, commenting and supporting me :,)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[bgolus made a post](https://twitter.com/bgolus/status/764746158145101825)how he re-created the interior mapping of Sim City 5:

Then Layla ported it to Unreal and [posted about it here:](https://twitter.com/LaylaCode/status/765894999552716800)

In the meantime, [dekaf](https://twitter.com/dekaf/status/907702515105329152) shared [this link](http://www.andrewwillmott.com/talks/from-aaa-to-indie) where you can get details about how the interior mapping was done in Sim City 5. Here is the video (slides are linked in the description):

![](../../assets/41b26ce6e8d2ef74.png)


![](../../assets/41b26ce6e8d2ef74.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

And as if this wouldn’t be enough already, [Alex S posted this](https://twitter.com/aStrkl/status/859800496751747074) nice interior mapping based on a reflection probe:

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

Thanks to [Ian](https://twitter.com/PolygonCherub) for giving is the Shader Forge Code and a huge image of the whole shader network which shows the implementation of the interior mapping.

[Shader Forge Code](https://data.simonschreibt.de/gat048/update5/InteriorMap_SF.shader) (right-click, save as)

[Shader Forge Network as JPG](https://data.simonschreibt.de/gat048/update5/shader_full.jpg)

[interior_2d.png](https://data.simonschreibt.de/gat048/update5/interior_2d.png)

[interior_2d_Atlas.png](https://data.simonschreibt.de/gat048/update5/interior_2d_Atlas.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[a long post about their interior mapping](https://blog.scssoft.com/2025/02/under-hood-parallax-interiors.html)! They made a ton of research and even a new tool so that the artists can easily define the UVs for all those windows.

Here’s some more backstory on this concept from back in 2008.

http://www.humus.name/index.php?page=3D&ID=80

Originally conceived by Oogst on the Orge3D forums.

Thanks for sharing the link! I did mention the Oogst article in the AC3 Windows article but this is a nice addition! I think the concept is a bit different because it seems that in AC/SR/BS they “just” use parallax offset mapping instead of simulating real geometry via pixel shader like Oogst.

I would love to see a game which does “real” interior mapping like Oogst … but i never heard of any game doing this. Did you?

Another awesome article Simon! The windows thing was funny :) Are you going to start using WebM instead of gifs? Much better suited for this kind of content.

Thank you very much :) Regarding the WebM: I’ve to read a bit about it and find out how i can convert my files into WebM, host them on my server and how it works with playing that kind of stuff. But i have to do that because GIF is just pretty big. I already did visit some websites but don’t want to host my data on their servers.

I applaud you, detective.

Thank you, but the main detectives where Lino & invisGhost who originally spotted the windows :)

Hallo,

Wann dürfen wir denn mit einem neuen Artikel rechnen? Freu mich schon darauf

Und falls du dich für klein Thema entscheiden kannst, ich finde derzeit Layeed materials in unreal 4 in Verbindung mit pbr sehr interessant.

Lg

Florian

Hi Florian,

da fragst du was. Ich arbeite fast jeden Tag daran aber irgendwie komme ich nicht gut vorran. Das nächste Thema wird etwas technischer und da will ich keinen Käse erzählen. Das danach, erfordert viel Arbeit im Bezug auf die Bilder bzw. Animationen. Naja, aber ich bin dran! Layered Materials wird auf jeden Fall ein Teilaspekt des nächsten Artikels. Du meinst sicher den Trick aus der UDK-Demo, indem sie Multi-Materialien in einem Shader bündeln um Draw Calls zu sparen?

Lg,

Simon

Hallo

Bin schon sehr gespannt auf deinen Artikel und danke für all die großartigen Artikel!

Ich spreche davon: https://docs.unrealengine.com/latest/INT/Engine/Rendering/Materials/LayeredMaterials/index.html

Lg

Florian

Gern geschehen, ich hoffe du magst du folgenden Artikel auch so gern. :) Vielen Dank für den Link. Das ist wirklich eine schicke Technik!

Ich bin mir sicher das mir auch dein nächster Artikel gefallen wird :)

Hier noch ein Link der dich zu dem Thema interessiern könnte:

http://blog.selfshadow.com/publications/s2013-shading-course/rad/s2013_pbs_rad_slides.pdf (70mb!)

Hierbei geht es um die Erstellung der materials via layered materials im Spiel Order 1886.

lg

Florian

Vielen Dank für den Link. Das ist ja der Wahnsinn! Will … auch …

Deus Ex Human Revolution also features some sort of cubemap windows that look good from a distance. I think they even look better that the ones on games like Watch Dogs.

Really? Do you have an example video (of Deus Ex)? Would be great to see it in motion :)

Hi,

Deus Ex: Mankind Divided using same technique. https://youtu.be/U0Rl4y1t07Y I saw it also in Borderlands 2. Cool trick.

Thanks for your articles. Very interesting. :-)

that looks really nice :) are you sure it’s not “just” a translucent plane with another one below? i mean, it could be both but in this special area maybe the didn’t need to build such an advanced shader? or did you already investigate and see that’s only one plane with a fancy shader applied?

I can’t investigate more because the game has unreadable sources. But it could be as you said there are two planes. The top one has alpha transparency and second is facing your camera position. Something like billboards.

When I play the game in the future and visit the same place I can try to find out more :)

There is also this amazing work by Gil Damoiseaux

https://twitter.com/Gaxil/status/1046705089342296065?s=19

Thank you so, so much, this was so incredibly useful for my research into Bioshock Infinite’s SFX and very informative! I credited you throughout it :) https://www.tumblr.com/bioshockblueprint/744138627128442880/parallax-effect-in-bioshock-infinite?source=share