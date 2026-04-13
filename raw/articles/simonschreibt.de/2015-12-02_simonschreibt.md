---
title: Simonschreibt.
url: https://simonschreibt.de/gat/colorbanding/
author: Simon
published: '2015-12-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/a82dea8e362032d4.png)


![](../../assets/a82dea8e362032d4.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

I didn’t believe in color banding. I trusted some half-knowledge for years and now I write about it so that you don’t make the same mistake.

I’ll explain what color banding is and that texture-compression might look very similar – it’s important to recognize the difference to choose the right tools to fight it. But first I’ll give you a short overview why I got trapped in half-knowledge.


My Struggle

![](../../assets/61d1d3ad09e36a35.png)


I was like the dudes above when it came to Color Depth. With 24 Bit per pixel (smart people say 24 **bpp**) you get freakin’ **16.7 million** colors!

[Depending on where you look ](http://hypertextbook.com/facts/2006/JenniferLeong.shtml) they say that the human eye can distinguish up to **“only”** 10 Million colors. Without any clue about color depth and **RGB** color channels I said things like:

![](../../assets/34aa06f2ada4f633.png)


This let me struggle when suddenly graphic cards where able to calculate with **32**bpp. I still wouldn’t have any idea about color channels and especially not what an alpha channel could be. But I had enough half knowledge to say stuff like:

![](../../assets/cbd5772b1330df6f.png)


Nobody else in my “hood” would know more so my statement sounded well-grounded. Unfortunately with such a thinking it was **impossible** for me to explain these abrupt changes in the color:

I mean … we’re talking 24bpp bro’ – **more colors than you can see**!!!!111 How is this even possible?! With the years and by stopping myself from hiding behind half knowledge I found an answers:

24/32bpp isn’t enough, bro’!

24/32bpp is just the sum of 8bit for every of the three color channels (red, green and blue) and maybe an alpha channel.

8 Bits per channel.

That’s a maximum of 256 colors per channel – doesn’t sound **that** much anymore, right?

And if you now imagine a gradient reaching from black to white on a monitor with a resolution of 1920 pixels width you’ll quickly learn that you have to stretch your 256 colors so that you get ~8 pixels wide color bands (1920 pixels / 256 colors = 7.5 pixels per color).

![](../../assets/8cf9b28f4cf5cdd1.gif)


8 Pixels isn’t that much but most times you don’t have gradients going from one extreme to another. Here’s another gradient with only 30 shades and you can already see some banding.

![](../../assets/152fa434dd0ac80c.gif)


You can find all this dry theory in many other articles and after reading about the 256-colors-per-channel-limitation I though:

![](../../assets/11d90ee1ab5328df.png)


Fight Color Banding

If the problem really depends on the limitation of colors (and not from texture compression which is explained later) you can’t magically create more of them **but** you can use [Dithering](https://en.wikipedia.org/wiki/Dither) to hide the limitations!

“Dither is an intentionally applied form of noise […]” “[…] to ease the transition between two colors, without adding any new colors to the palette.”


–[wikipedia.org]&[pixeljoint.com]

What this basically does is shown below. I guess especially Retro-Pixel-Artists do such stuff every day but isn’t this amazing? What a great way to hide the actual color limitation.

Note that we game developers are in the lucky position that we can use such tricks while other industries really depend in accuracy. Here’s an interesting example:

“While dithering produces a visually smooth image, the pixels no longer correlate to the source data. This matters in mission critical applications like diagnostic imaging where a tumor may only be one or two pixels big.”


Source:[30-Bit Color Technology for NVIDIA® Quadro®]

If you are interested in technical details about dithering, make sure you read [Banding in Games: A Noisy Rant](http://loopit.dk/banding_in_games.pdf) and all the other links I posted in the “Links & Resources” section. But now let’s talk about a similar looking phenomenon:

It looks like Color Banding but it’s not!

It’s important too see what “real” color banding is and what only might **look** like it. Here are some examples for color banding imitators:

![](../../assets/ebe450f92e093152.png)

Example 1: Texture Compression

Now let’s get to a bigger part which might be a bit more common. If you take the texture blob below and use it even for **huge** effects like the haze around a sun or an aura around an explosion, all will be **fine**, even if this smallish texture gets scaled up drastically:

![](../../assets/384c710948b9ce85.png)

You might see some color banding but this is because of the limitations of the 256-color-per-channel-limitation (explained [above](https://simonschreibt.de#24bitIsntEnough)):

![](../../assets/d0acb93e13b38c56.png)


In the upper case you can’t do much but it gets ugly when game engines use **compressed** texture data (should be almost always the case) which means for [DXT1](http://blogs.msdn.com/b/shawnhar/archive/2008/10/28/texture-compression.aspx) for example that the texture will have 65536 colors (16bpp) instead of the possible 16.7 million (24bpp) and get some compression artifacts. The good news: The texture will need way less memory and most of the times still look pretty good.

Most of the times. In this example you can clearly see how the texture got more “wobbly” due the compression:

![](../../assets/09d2a3dec46ca37c.png)


In this case it’s easy to see that the compression is the problem. But with a shiny background and maybe seeing only a part of the texture (because it’s for example used as a huge haze) you might think:

![](../../assets/ebe450f92e093152.png)

**“Oh, that’s color banding. I can not do anything about it. It’s the limitation of the 24bpp!”**

But if you actually notice that in **THIS** case it is the **compression** which steals your colors, you can fight against it!

Four ways of fighting compression

Here I’ll present you some ways about what you can do against the compression problems:

1. The way of the smart Fox

You can read [this article](http://www.gamasutra.com/view/feature/130877/making_quality_game_textures.php?print=1) which describes really well how to optimize your image so that it looks well even **with** compression by using noise and precise color shifts.

2. No way. No compression.

If you have control over your pipeline you could **not** compress this special texture to avoid any compression artifacts and color shifts. This costs more space but if your texture isn’t too big and you don’t do this too often, it should be fine. Even if the texture is small and therefore contains not many color information, the graphic card will interpolate the values in-between very well. That’s why even small (uncompressed) textures work well for gradients.

![](../../assets/eed4b0c19f6d0fb7.png)


3. The Way of the furious Programmer

I **don’t** recommend this but of course you could just use a huge 2048x2048px blob texture to make the artifacts visually smaller. Besides of that programmers will give you a death-stare you can’t avoid tiny artifacts which might be visible when the texture is scaled up a lot. In addition there some greenish/reddish color shifting going on which can also be a distraction:

![](../../assets/b7ea8224c152b8f5.png)


Actually it’s really interesting that these color shift happen because not every color channel gets compressed with the same quality. With DXT1 for example the green channel gets 6 bit while red and blue only get 5 bit (makes 16 bit in total). This is because [the human eye is more sensitive when it comes to green values](https://en.wikipedia.org/wiki/High_color).

4. The way of the not existing texture

I learned a really smart trick from [Alex](http://www.abalakin.de/) which is to not use textures at all. Details are written down in an other article: [X:Rebirth – Geometric Lensflares](http://simonschreibt.de/gat/xrebirth-geometric-lensflares/). But for those who don’t like clicking links, here’s a preview:

And not to forget, the backgrounds in Homeworld were done via Vertex Color too! I wrote about this [here](http://simonschreibt.de/gat/homeworld-2-backgrounds/).

Example 2: Faceted Geometry

Another nice example which has nothing to do with color banding but with the shading of narrow polygons. Here’s what the author described it as:

“what the… oh”….not banding, just faceted geometry…


–[Banding in Games: A Noisy Rant]

That’s it!

Thank you for reading and let me know if you like the content of this article or if something is wrong or needs to be added.

![](../../assets/ba0680151067ebbc.png)

[MrEiwe](https://twitter.com/MrEiwe)for this link about

[hardware-dithering and framerate control in monitors](http://www.tftcentral.co.uk/featurescontent.htm#dithering). And here’s a huge article about

[realtime-compression and a lot explanation about DXT](http://www.nvidia.com/object/real-time-ycocg-dxt-compression.html)– Thanks for the link

[p1xelcoder](https://twitter.com/p1xelcoder).

![](../../assets/ba0680151067ebbc.png)

[Konrad – a friend of mine –](http://www.konradhoeffner.de)had an interesting idea which I would love to hear your opinion about. Instead of increasing all three of the RGB values simultaneously by +1 for creating a gradient, he mentioned to split it up and first add +1 to one channel, then add +1 to the next channel. Here’s an example:

![](../../assets/f4beb877806c6991.png)


At the top you see a standard color gradient (increased contrast for better visibility) where gray values are brightened up by adding +1 to all of the RGB channels.

At the bottom you see smaller color stripes where first the green channel gets +1 and then the blue channel. Of course this creates color where you intend to have only grey values but seeing it from far makes this detail less prominent.

![](../../assets/99ebba8cd221589b.png)


Here’s an [example with 1920 pixels width](https://data.simonschreibt.de/gat055/update2/gradient_full.png) (click the link or Right-Click on the image and choose “Open in Tab”). The upper area of the image is a standard gradient and the lower area is a version created with the mentioned method. To me it looks a bit more smoother seeing it from far.

What do you think about this method? Was it used somewhere already – Is there a name for it? Or is it not usable because of problems with compression, post-effects or something else?

p.s. after tweeting this update [pixelmager](https://twitter.com/pixelmager) responded with this [shaderToy link](https://www.shadertoy.com/view/4sjXWw) showing of several approaches to this topic. :,)


Links & Resources

**Color Banding & Perception**

[a01] [Banding in Games: A Noisy Rant](http://loopit.dk/banding_in_games.pdf)

[a02] [Number of Colors Distinguishable by the Human Eye](http://hypertextbook.com/facts/2006/JenniferLeong.shtml)

[a03] [Understanding the HP DreamColor 30-bit Panel](http://www.hp.com/united-states/campaigns/workstations/pdfs/lp2480zx-30-bit-panel.pdf)

[a04] [30-Bit Color Technology for NVIDIA® Quadro®](http://www.nvidia.com/docs/IO/40049/TB-04701-001_v02_new.pdf)

[a05] [High quality GIF with FFmpeg](http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html)

[d01] [Discussion: Is 32-bit color depth enough?](http://graphicdesign.stackexchange.com/questions/47133/is-32-bit-color-depth-enough)

**Compression**

[a06] [Making Quality Game Textures](http://www.gamasutra.com/view/feature/130877/making_quality_game_textures.php?print=1)

[a07] [DDS Types](http://www.poopinmymouth.com/tutorials/dds-types.html)

[a08] [Texture Compression](http://blogs.msdn.com/b/shawnhar/archive/2008/10/28/texture-compression.aspx)

[a09] [Real-Time Normal Map DXT Compression](http://www.nvidia.de/object/real-time-normal-map-dxt-compression.html)

[a10] [Texture Compression Techniques and Tips](http://www.gamasutra.com/view/feature/130906/texture_compression_techniques_and_.php)

[a11] [Real-Time YCoCg-DXT Compression](http://www.nvidia.com/object/real-time-ycocg-dxt-compression.html)

**Dithering**

[a12] [Wikipedia: Dither](https://en.wikipedia.org/wiki/Dither)

[a13] [How to fix color banding with dithering](http://www.anisopteragames.com/how-to-fix-color-banding-with-dithering/)

[a14] [HDR Dithering](http://sandervanrossen.blogspot.dk/2012/02/hdr-dithering.html)

[a15] [Dithering in Unreal](https://www.doomworld.com/vb/everything-else/69759-unreals-texture-dithering/)

[a16] [The Pixel Art Tutorial: Dithering](http://pixeljoint.com/forum/forum_posts.asp?TID=11299&PID=139320#139320)

[a17] [Dithering and Frame Rate Control (FRC)](http://www.tftcentral.co.uk/featurescontent.htm#dithering)

**sRGB, Gamma Correction, HDMI**

[a18] [GPU Gems 3: The Importance of Being Linear](http://http.developer.nvidia.com/GPUGems3/gpugems3_ch24.html)

[a19] [A Standard Default Color Space for the Internet – sRGB](http://www.w3.org/Graphics/Color/sRGB)

[a20] [HDMI Standard, Cables and Color Depth](http://www.kramerelectronics.com/downloads/white-papers/effects_of_color_depth_4.pdf)

[a21] [10 Bit Color support on NVidia GPUs](http://nvidia.custhelp.com/app/answers/detail/a_id/3011/~/10-bit-per-color-support-on-nvidia-geforce-gpus)

Awesome article as always, thank you very much.

The video is, as you said very relaxing and faster so I really like the concept but I also like to read an article as it’s easier to take the time to understand.

I don’t know if it’s possible to continue doing both. Maybe doing a small introduction videos illustrating the big lines would be cool but it might be hard for the viewers to avoid “Half-Knowledge” like : “Oh I looked at the video, I understood everything” :P

As far as I am concerned, I would maybe prefer the text for the reason explained before but if you do videos, I would look at them too. :)

Thanks for the feedback, it’s exactly as I see it and I’ve to see how much time I have. I guess it will be a mix. For more “dry” issues I might create videos and shorter articles with impressive tricks could stand for its own. But really good to hear your opinion! :)

Hey man, awesome article. You should follow some of the discussion on Hacker News: https://news.ycombinator.com/item?id=10667379

thanks! I’ve registered an account at hackernews and will add some of the links and tipps to the article. thank you for the hint :)

This is really awesome. Thank you for the article ^_^

Awesome article!

Now to answer your question: I prefer videos, almost always. For exactly the same reasons you’ve mentioned. That being said some text accompanying a video would be a big plus – links to other resources, for example. You could even add a Table of Content in the form of links your video with timestamps (so they direct to “chapters” in the video).

And, although it might be to much work, what you did here: video AND an article is the most perfect form – I can watch the video to familiarize myself with the topic and when the time comes to use your article in practice I can quickly follow the text version. I hope this makes sense.

Can’t wait to read (watch?) your next article :)

Thanks for your feedback! I see it the same way and hopefully have enough time to make article+video the next time too. Of course it depends on the topic – I guess if it’s a short article mostly consisting of images it should be OK if it’s only availiable in form of an article. We’ll see how it works out :)

Hello Simon,

I love all your posts, I think you are making a great labour finding out all these hacks. I have already read all!!

This is the last one you wrote for now and I just wanted to thank you for all your posts, they are really interesting and easy to read :D

I would like to ask you what do you mean by uncompressed textures, and how are GPUs are suppossed to interpolate the colours at the time they need to scale them.

Thank you!!

Juan.

Hi Juan, thanks for your comment and the kind words. :) Regarding your question: When you put a small texture on a polygon which is big on the screen (so that the texture is shown bigger than it’s original resolution) the graphic card interpolates between color values like desribed here: http://www.riemers.net/eng/Tutorials/DirectX/Csharp/Series2/tut11.php

This means you might be able to use a small texture with a gradient and even if this texture is big on the screen you wouldn’t see big pixes or aprupt color-changes since the graphic card would interpolate the values and smooth them out. I would expect that this works better with uncompressed textures since compression artifacts could disturb the “perfect” gradient texture.

I hope this was explained good enough. :,) If not, just continue asking!

Ahh, alright! I tried to add a small circular gradient texture (128×128 8bits per channel png) to a poly in UE4, but the card interpolated it badly….

At first I thought that if the image was not compressed, the results of the graphic card will be neat, but apparently my card, at least, used a intepolation similar to photoshop “nearest neighbour enlargement method”

Anyway, I thing that the best solution is what you used in X: Rebirth, that was f@*/% clever :D I love vertex painting!! :D

Feel free to attach an image of how your texture & the results looks. It sounds weird that you’ve no filtering enabled.

Hehe yeah I like it too how it was done in X:Rebirth :D Of course with textures you’ve a bit more freedom about the look of the lensflare and less geometry but yeah, it’s a cool idea. :)

The way you write your articles make them very easy and funny to read, I really enyoyed how you wrote the Zelda Wind Waker Guide! To be honest, for this article I did both: I first watched the video and then read the article, so, If you have the time and the energy to do both, we will probably have the time to watch and read both and you will reach more people!

Thanks man, good to hear your feedback :) Will see how much time I can spare for the future. :)

Hey Simon!

Very useful the video! allows me to keep working on something while listening and take periodic looks to the images when necessary, so… great! Article + video = perfect.

Thanks for taking the time to share some knowledge, as always ^-^

thanks for the feedback! glad you liked the video :)

I’ll just throw in this useless knowledge:

The “just use a much bigger image” trick is actually common practice on responsive websites, to support high-dpi screens. Like, if you have a Retina display with twice the pixel density than a desktop monitor, you use a twice as large image, and then let the browser scale it down. But because of that, you get away with a much higher compression ratio. One that would make the image really ugly, if you’d look at it at a 1:1 scale.

That’s interesting :) But don’t you look at it on a retina display at 1:1 scale?

Hi!

To have better quality PVRTC-compressed UI textures in PocketTroops we extracted alpha channel to separate texture, made it (alpha texture) twice smaller and 24bit uncompressed. That made UI look better and textures smaller at the same time, because all alpha’s are located in different R, G, B,A channels of alpha texture. You can check https://habrahabr.ru/post/259835/ it’s in russian but pictures help to understand the issue.

Neat idea. So even if you’ve some compression artifacts the shape of the UI element stayed clean and sharp? Sounds great!

True. This saved from artifacts on sprite borders, where alpha goes from 1 to 0.

Thanks for the article!

One of the things to keep in mind with banding is that there are a lot of causes, and they can work in conjunction to make banding more apparent– or sometimes they can work in conjunction to hide banding, just as dithering’s noise hides it.

For instance, try opening your Homeworld picture in an image editor. Select the bright color as foreground, select the dark color as background, and create a gradient right there on top of the picture. Where did the banding go?

The banding in the Homeworld picture isn’t a function of not enough colors in 32bpp. It might be a function of multiple drawing layers with gradients occurring in parallel lines. This tends to exacerbate banding. When you take an image and start to do math on it, addition and multiplication of additional layers, you accumulate rounding errors that make the final color depth much less than the color depth of any of its sources.

It might be gamma correction, especially in an image this dark. Let’s say your game uses gamma corrected lighting on uncorrected textures. The first thing you do is raise your texture’s color to the 2.2 power. When you’re done, you raise your final image to the 1/2.2 power. Let’s say you start with something like 8/255, then multiply it by a 0.5 diffuse factor. But what’s 4^(1/2.2), rounded? It’s the exact same thing as 5, 6, or 7– that is all, all of your texture values from 8-14 all collapse to the same final pixel color. In areas that dark, you’ve lost three quarters of your color depth! And this isn’t an uncommon situation, since creating uncorrected textures usually means having a dedicated, studio computer, which you can’t use to check Facebook or watch Netflix. (But in general, and done right, gamma correction is awesome, and you should use it.)

This is why, a lot of the time you want to use buffers with much higher depth than your final output. By using 16 bit (times 4, RGBA) floating point values for computing your colors, these issues almost completely disappear, even if you’re inputting from 256 shades of each hue, and outputting to 256 shades of each hue.

Thanks for your long comment! :) But I don’t understand this example: When I calculate 4^(1/2.2) I get ~1.877 – how do you end up with 5,6,7 or 8-14?

Actually, I screwed up with regards to gamma. But I’ll explain anyways.

4^(1/2.2) = 2. 5^(1/2.2) = 2. 6^(1/2.2) = 2. 7^(1/2.2) = 2. (On double checking, 8 rounds the other way.)

50% diffuse lighting, so your inputs are getting divided by two. 15-16->8, 13-14->7, 7-8->4.

I forgot to take into account the gamma expansion, the original x^2.2, which doesn’t leave you with a range of 4-7 anyways. The exact equation, input to output, for what I was describing is at http://www.wolframalpha.com/input/?i=floor((((x%2F255)%5E(2.2))*(0.5))%5E(1%2F2.2)*255) . There is loss of color depth, and there are places where one input texture values rounds up while the next rounds down (leading to loss of color depth, and risk of banding), but it’s not as bad as I originally (mis)calculated. (“Floor” is different rounding than what I was assuming earlier, but the exact style of rounding only affects where the problems occur, not that they occur.)

Thanks for the explanation!! Awesome :)

The technique of using off-grey hues to increase the apparent number of grey tones has been around for a long while. In digital photography circles, I’ve heard it called ‘pseudogrey’ after the 1999 usenet posting that can be seen here: http://r0k.us/graphics/pseudoGrey.html

However, the technique has been around for a long time, notably on 16-bit games, to increase the extremely limited number of grays, without sacrificing colours in a limited palette: because of the low colour-depth, the off-gray colours could be used as both grey tones and as colour, depending on how they were used/dithered.

This technique can be seen to great effect in the graphics of many 1990s Bitmap Brothers games, such as Speedball 2 (the best example I think, esp on Atari ST), Cadaver, Gods, and others. The technique is especially noticeable on the ST, where the palette size is further reduced. e.g. in Cadaver screenshots, notice how the same shade of green is used both to colour water and potions (and apply lighting effect), but also acts as a ‘gray’ tone in the UI and armour. Many of the colours in these games were picked to fall between the gray tones (and in some cases to fit in with colour ramps applied as key and fill-in lighting too). I remember examining the graphics from these games years ago to work out how it was done and marvelling at how clever the palette choices and artwork were… light years ahead of my own artwork where I struggled with the limited colour palettes.

Thanks man, I think this talk fits the topic really well: https://www.youtube.com/watch?v=aMcJ1Jvtef0

Writing here because you inquired for feedback, and also to say thanks :-)

I like both the video and the article side-by-side. They complement each-other well. Thank you for sharing your experience and I find it to be an informative and warm presentation.

I watched/listened to the video, then reviewed the article.

Thank for taking the time to give feedback :)