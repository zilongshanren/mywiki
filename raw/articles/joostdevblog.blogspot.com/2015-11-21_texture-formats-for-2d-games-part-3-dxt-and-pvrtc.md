---
title: 'Texture formats for 2D games, part 3: DXT and PVRTC'
url: http://joostdevblog.blogspot.com/2015/11/texture-formats-for-2d-games-part-3-dxt.html
author: Joost van Dongen
published: '2015-11-21'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers II](http://www.swordsandsoldiers2.com)and

[Awesomenauts](http://www.awesomenauts.com). DXT is easy to use but provides some weird compression artefacts, so a good understanding of how it works is very useful for both artists and graphics programmers. Since DXT is not supported on iOS I will also shortly discuss the quite similar PVRTC format. This is part 3 in my short series on texture formats for 2D games. Here are

[part 1](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)and

[part 2](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-2.html).

Note that DXT is often also referred to as DDS because DXT textures are usually saved as .DDS files. DXT is also known as

[S3 Texture Compression](https://en.wikipedia.org/wiki/S3_Texture_Compression).

There are several versions of DXT. The most versatile type is DXT5, which stores an alpha channel that can be used for transparency. DXT5 uses only 8 bits per pixel, making it 75% smaller than full 32bit RGBA. If no alpha is needed or only on/off alpha, DXT1 can be used, which is even smaller: 4 bits per pixel, making it 87.5% smaller than RGBA. That's quite a spectacular win, so where's the catch?

The downside is that DXT can bring serious quality loss due to how it compresses textures. The quality impact of this compression heavily depends on the type of art: some textures will look really bad but in most cases it will look fine as long as you don't zoom in on the compression. Zooming in that far is not common in 2D games so DXT is very usable despite the quality loss.

![](../../assets/8fb98aa6196f6362.png)

The most basic type of DXT is DXT1. Here's how it works:

![](../../assets/1e5e906eae6d4fc2.gif)

This means that if a single 4x4 block contains few different colours, there won't be any significant compression artefacts. Having more colours inside the block is also fine if those colours are near the others. For example, if the block stores red and yellow then it can also store orange well since that is in between. Heavy artefacts occur if the block contains more really different colours. For example, if a 4x4 block contains red, green and black, then one of those will be lost and replaced by one of the others (whichever is nearest to reduce the artefacts).

![](../../assets/41d4d1e4454782ca.gif)

This sounds absolutely horrible, but the fun part is that we are only talking about tiny 4x4 blocks here. In practice few blocks contain many different colours, and even if they do the next block will be able to choose different colours, so artefacts usually remain small. In practice in 2D games DXT artefacts will mostly appear in spots where three coloured areas touch each other, and around thin outlines. Have a good look at the image below to get an idea of which situations result in serious artefacts and which are fine.

![](../../assets/becbf1c662a632c7.png)

As you can see above, if your art contains lots of thin outlines it will be damaged severely by DXT1. However, fixing this by going from DXT1 to 24bit RGB makes your textures 6 times bigger. Auch! Luckily there is an awesome compromise: if you store your DXT texture at a slightly higher resolution it will look a lot better and still be smaller than RGB. Upscaling makes the outlines (or other small details) thicker, greatly reducing the artefacts. If you make your texture 41% wider and higher it becomes twice as big, which is still 3 times smaller than RGB. As a huge bonus you also get sharper textures, so this probably looks way better than the lower resolution RGB texture would have. We've used this trick in Awesomenauts on all the characters: they're stored a bit higher than required for a 1920x1080 screen to reduce artefacts.

![](../../assets/bd892d2c4dc6f321.png)

![](../../assets/e717c072a422ccfb.png)

The format I've explained so far is DXT1, while DXT5 is what you'll want to use most. Colour is stored in the exact same way in DXT1 and DXT5. The difference is that DXT1 only has 1 bit alpha, while DXT5 can also store partially transparent pixels. DXT5 stores alpha in the same way as colour, so it stores two alpha values per block. Per pixel it stores an interpolation value for the alpha. So in total DXT5 stores two colours and two alpha values per block, and for each pixel one interpolation value for the colour and one for the alpha. This makes DXT5 exactly twice as big as DXT1 and results in high quality alpha/transparency.

There's also DXT3, but in practice I've so far never found it useful. DXT3 does not store two alpha values to interpolate between: instead it just uses 4 bits per pixel to directly store alpha per pixel. Since it's only 4 bits this means DXT3's smallest alpha step is 16. In other words: DXT3 is really bad at doing subtle alpha gradients, but really good at doing strong alpha contrasts (like object outlines). Since DXT5 is already good enough at doing strong alpha contrasts I've so far never used DXT3 in an actual game.

DXT1 can also store alpha, but only 1 bit alpha, so only on/off. A clever yet simple trick is used for this. Remember that each 4x4 block stores two colours. If the first colour is brighter than the second colour, then a block can store four different colours: the two main colours and two interpolated colours. This is how I explained it above. If however the first colour is darker than the second colour, then the block can store only three different colours. The fourth colour is used for fully transparent pixels. This results in slightly less colour quality around edges in the texture. Unfortunately it's only 1 bit alpha, so any anti-aliasing on object edges is lost.

![](../../assets/2fa0e58b7cdffeea.png)

There is another type of quality loss happening with DXT compression that I haven't mentioned yet. Colours are stored with 16 bits instead of the full 24 bits. This means that on top of the compression artefacts already mentioned we also get less colour depth. For most textures this is not a problem, but for subtle gradients it is. For this reason in Awesomenauts and Swords & Soldiers II we don't store pure gradients using DXT. We use simple 24 bit TGA instead. This is much bigger, but gradients are usually very thin, so storing a bunch of 256x1 textures with less compression is no problem.

![](../../assets/45bf53db3262c72f.png)

Since DXT is used by so many games there are plenty of tools and plugins to work with it. For example, Nvidia has released a free

[Photoshop plugin](https://developer.nvidia.com/nvidia-texture-tools-adobe-photoshop)for handling DDS files. When using this for 2D games, be sure to turn off mipmaps to save some more texture space (unless you actually need those mipmaps of course). Image browsing tool

[XnView](http://www.xnview.com/en/)supports DXT right away and I've heard there's even a plugin for Windows to see thumbnails of DXT files directly in Windows Explorer.

A fun aside here is that we've tried writing our own DXT compression tool to achieve DXT with less visual artefacts specifically for 2D games. We indeed managed to slightly reduce compression artefacts, but at the cost of more flickering in animations, so we ended up not using our own DXT compression tool. Maybe I'll get around to writing about that some day, let me know if you're specifically interested in this.

An important note on DXT is that iOS doesn't support the DXT format. Instead it has PVRTC. I haven't made any iOS games myself (

[Proun+](http://www.proun-game.com)and

[Swords & Soldiers 1](http://www.swordsandsoldiers.com)were ported to iOS by respectively

[Engine Software](http://engine-software.com/)and

[Two Tribes](http://twotribes.com/)) so I don't personally have any experience with PVRTC). The rough concepts are pretty similar though. The big difference is that PVRTC doesn't have the little 4x4 block artefacts that DXT produces. Instead, PVRTC's compression artefacts come in the form of a slight blurriness.

One trick to improve quality with PVRTC is the same as with DXT: saving at a slightly higher resolution than what you really need will massively reduce the compression artefacts. Aaron Oostdijk from

[Gamistry](http://www.gamistrygames.com/)(creators of the mobile hits

[Gold Diggers](https://www.youtube.com/watch?v=VSOZwighEpI)and

[Munch Time](https://www.youtube.com/watch?v=TUM7bpq3sb8)) mentions it also helps a lot to first smear the RGB colours our across the transparent areas. “

*A tool called Solidify B does this very nicely. And sometimes a light dither after that will improve results even more.*” Note that I didn't use those tricks when compressing the image below.

![](../../assets/6dacee69718ac8bf.png)

On iOS you get the additional requirements that textures need to be square (same width and height) and power-of-two (16, 32, 64, 128, 256, 512, etc.). In many cases these two extra requirements demand a huge waste of texture space, unless you work around them through clever usage of texture atlases. On PC and console these requirements have been abolished around a decade ago, making efficient texture usage much easier there.

DXT results in serious compression artefacts but it provides such powerful compression that it is by far the best option for the vast majority of games. Next week I'll wrap up this series on texture formats by giving a big overview of all the formats discussed. See you then!

*See also:*

-

-

-

-

[Texture formats for 2D games, part 1](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)-

[Texture formats for 2D games, part 2: Palettes](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-2.html)-

I find that dithering 24-bit colour in 16 bits makes even gradients almost indistinguishable.

ReplyDeleteGreat article. Very informative.


ReplyDeleteIf I understood correctly only two colors are stored per block in DXT1. When is the interpolation producing the two additional middle colors performed then? Is it done by the renderer?

I'd be interested in knowing more about your custom DXT tool adventure.

The videocard performs the interpolation whenever you grab a colour in the pixel shader. So it really goes into video memory like this. Videocards have low-level hardware support for DXT.

DeletePNG SHALL REIN SUPREME FOR IT IS THE SUPERIOR FORMAT.

ReplyDeleteLol, as explained in this series PNG is not supported on videocards, so it is only relevant for storage on disk, not during actual gameplay.

Delete