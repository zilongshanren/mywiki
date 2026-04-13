---
title: 'Premultiplication: Pros and Cons'
url: http://hacksoflife.blogspot.com/2010/10/premultiplication-pros-and-cons.html
author: Benjamin Supnik
published: '2010-10-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I realized today that premultiplied alpha could fix a nasty artifact that we sometimes get in X-Plane: "tree ring".*


The bug is this: imagine you have two texels in your texture. The left one is transparent, and the right one is opaque green (a tree). What is the RGB "behind" the transparent one? Let's call it junk.


When this texture is sampled with linear filtering, the graphics card will do the wrong thing: it will blend the two texels by channel to come up with a texel sample that is a mix of green + junk in the RGB channel and a translucent alpha channel. Thus at the edges of our alpha-blended tree, we will see a 'ring' of junk leaking into the texture.


The traditional work-around (and the one we use for X-Plane) is to ensure that the RGB behind the transparent parts of the texture contains something valid that we wouldn't mind seeing, e.g. "more green". This is not an ideal work-around because Photoshop will put white in this space when alpha reaches 0%, so most artists will have to manually fix this problem over and over (and it's not an easy problem to see since the erroneous color is behind a 0% alpha pixel).


If we used pre-multiplied alpha, this would not be a problem. With premultiplied alpha, the RGB pixels are already multiplied by the alpha channel; thus the transparent pixel is by definition black (0% alpha * any RGB = 0,0,0 = black). Thus when we blend green and black we get "darker green", which is the appropriate pre-multiplied color for a linear sampling at the edge of our tree. Simply put, premultiplying puts the alpha multiply before linear interpolation, which i what we want.


Compression?


I can think of a possible reason to not use pre-multiplied alpha in production art assets: texture compression. If I have a solid green tree with an alpha channel, my texture compressor uses all of its "color bits" to get that green color right. But if I premultiply, those color bits are now storing both the color and the effect of alpha (the darkening). I may get some color distortion on my tree because the compressor is trying to get the pre-multiplied alpha right.


In other words, a non-premultiplied texture may compress better. Ideally I'd like my compressor to be alpha-aware, that is, optimize the color under the opaque part at the expense of what is under the transparent part.


The Rest Of the Story


Obviously we're not going to change X-Plane to premultiplication given so many art assets out there. But there is more to the story too.


The * up there is that there is a second, significantly worse cause of "rings" on trees: z-buffer artifacts. The z-buffer doesn't handle translucency very well (and by that I mean it doesn't handle it at all). If our trees contain translucent edges due to linear filtering, we get Z put down over the translucent parts, and that cuts out any 3-d building or additional trees behind them. The result is "blue rings" where the sky shows through what should be a forest.


The solution is the one we use in practice: we turn off blending entirely and simply test the texels - they are in or out. We still use linear filtering though, so that the alpha edge of our tree isn't square and jagged, so we would see a ring if we have bogus color underneath the transparent parts of the trees. Since in practice we almost always ship DXT compressed textures, the compression argument against pre-multiplication holds.

Would it not be sensbile to store cached textures with premultiplication on disk when xp is loading? marking them up with the unique path to the texture, resolution and the file's mtime all tucked into a hash.

ReplyDeleteWe've given some thought to caching interim scenery products, but it would have to be a big win, since it introduces a source of unreliability (e.g. behavior changes depending on cache status). Since textures are going to be used compressed for most users, the DDS file is already exactly what we want.

ReplyDelete