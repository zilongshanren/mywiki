---
title: 'Texture formats for 2D games, part 2: Palettes'
url: http://joostdevblog.blogspot.com/2015/11/texture-formats-for-2d-games-part-2.html
author: Joost van Dongen
published: '2015-11-13'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[introduction to texture formats](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)we are going to look at palette textures today. Palette textures are an interesting and underused option for 2D games. Using them is quite a hassle since normal videocards don't support them, but for certain art styles they offer high quality and small texture size.

Palette formats are similar to GIF files. The idea is that we have a palette, a list of all the colours in a specific texture. In the actual texture we don't store the colour of each pixel, but rather a reference to the palette. If the texture doesn't have a whole lot of colours we can get away with using only 256 different colours. References to these can be stored in 8 bits per pixel, so this format is 75% smaller than uncompressed RGBA.

![](../../assets/fd627495d40d83d6.gif)

Palette textures are particularly useful for cartoony styles with flat shading, since those have fewer colours per texture. If your textures have more than 256 colours, you can reduce the number of colours. Depending on the art style this loss in quality might be acceptable. For a style with lots of colours and gradients, it probably isn't.

Most textures in

[Swords & Soldiers 1](http://www.swordsandsoldiers.com)on Nintendo Wii were stored using palettes. Some textures even had few enough colours that we could get away with only 16 different colours in the entire texture. This means we needed only 4 bits per pixel. That's 87.5% smaller than uncompressed RGBA! This would bring a 4096x4096 texture down from 64mb to 8mb. Of course such heavy compression is only suitable for some art styles and some textures.

![](../../assets/378e245580c8d6d6.png)

![](../../assets/edd58dbbcbbfc515.png)

The big caveat is that most videocards don't support palette textures directly. Older videocards like the one of the Nintendo Wii support it, but none of the modern Nvidia, AMD or Intel cards do. Swords & Soldiers 1 was originally a Wii game so we could easily use palette textures there.

This doesn't mean that using palette textures is impossible, just that it's more involved. It's quite easy to write a pixel shader that uses the colour from a greyscale texture as an index for a lookup in a 1D palette texture.

The problem with doing this yourself is that you can't use texture filtering any more. Interpolating palette indices results in random colours. To implement standard bilinear filtering you need to sample and interpolate the colours yourself in the pixel shader. Including the lookups in the palette this means 8 texture reads per pixel. If you happen to also need trilinear filtering for mipmapping this increases to 16 texture reads per pixel. Luckily not all 2D games need mipmapping, but still: 8 texture reads per pixel is significant and costs performance. However, the fun part is that many 2D games have plenty of performance to waste. If this is the case for your game and you have the time to write a good pipeline for them, then palette textures might be an excellent choice.

![](../../assets/7d6232acbfd71515.gif)

An interesting side effect of reducing the number of colours for a palette texture is that it makes ZIPping the texture much more effective. With less colours in the texture there is less variation so it can be compressed more effectively. This only helps for download size and for the size of the texture on disk: videocards can't handle ZIPped textures so the texture needs to be unzipped before it goes into video memory.

We used this extensively in Swords & Soldiers 1 to reduce download size. Since the Nintendo Wii had an extremely small hard disk keeping the install size of the game small was really important. For this reason we reduced the number of colours even in cases where it didn't make the texture itself smaller. For example, the size in video memory is the same for a texture with 200 colours or 256 colours. However, the texture with only 200 colours can be ZIPped further. Often there is no visible quality loss when reducing the number of colours a bit further, so we did this with a lot of textures on the Wii version of Swords & Soldiers 1.

When saving an image for the web in the GIF format it's common to turn on dithering. Dithering makes a palette texture alternate between two different colours in a noisy pattern to achieve what looks like smoother gradients with fewer colours. This works quite well for the web, but is totally unsuitable for games. Dithering makes the art flicker like crazy when an object moves around, so in games it can only be used on objects that are rendered pixel perfect, like the backdrops in old adventure games.

![](../../assets/94787eb87366c3a8.png)

A huge benefit of palette textures is that team colours and colour variations can be done extremely efficiently. By simply swapping the palette you can change all the colours. This costs hardly any memory or additional performance.

In

[Awesomenauts](http://www.awesomenauts.com)we don't use palette textures so we have to store each character twice: once for the red team and once for the blue team. With palette textures this wouldn't have been necessary. To add to the fun this would also have allowed us to let the player customise his team colour (not that we would want that in a team-based game in which the visuals are all about readability). Lots of other fun tricks can be achieved through clever usage of palette swapping.

![](../../assets/70b717c045655d8e.jpg)

![](../../assets/f85da330b40c9feb.jpg)

Since palette textures aren't supported by videocards by default they are quite impractical to use. Their limitation of a maximum of 256 different colours per texture is also very limiting. However, with certain art styles this technique will give you powerful, lossless compression and easy colour swapping, unique benefits that no other texture format can provide.

See you next week for a look into the master: DXT texture compression!

*See also:*

-

-

-

-

[Texture formats for 2D games, part 1](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)-

[Texture formats for 2D games, part 3: DXT and PVRTC](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-3-dxt.html)-

Have you ever considered using 16-bit palettes. It would need max size of 256x256 palette. But it would still be net save on textures bigger than 512x256. It should be quite good for most of the textures but performance would be horrendous. Trashing texture cache all the time.

ReplyDeleteI think just using 16 bit colours already looks so good that I don't really see the point of 16 bit palettes. It is quite rare that the difference between 24 bit and 16 bit colours is visible and 16 bit palettes would only be relevant in such rare cases.

DeleteJoost thank you for your articles, I love reading them =)

ReplyDelete