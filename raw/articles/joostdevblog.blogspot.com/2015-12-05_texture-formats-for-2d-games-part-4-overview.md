---
title: 'Texture formats for 2D games, part 4: Overview'
url: http://joostdevblog.blogspot.com/2015/12/texture-formats-for-2d-games-part-4.html
author: Joost van Dongen
published: '2015-12-05'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[last](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)

[three](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-2.html)

[blogposts](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-3-dxt.html)I've discussed the details of various texture formats. Now that we've seen them, it's time for an overview. Below you'll find a big table that lists the properties of a lot of different formats and shows their results. I'll also discuss some final considerations on performance.

The important thing here is to realize that there is no perfect solution: every choice has its own drawbacks, so even with the same art style you might end up with different texture formats depending on the platform. These are the main arguments to consider:

- Quality
- Size in video memory
- Size on disk
- Download size
- Loading time
- Framerate
- Development time

Most of these are pretty obvious and I've already discussed

*quality*and

*size in video memory*extensively in my previous posts. The reason I'm listing them here is that it's important to keep in mind that you can mix and match formats for different goals.

There are also more complex things that might matter to specific games, but if things like memory bandwidth are an issue then you are probably making an extremely complex game and hopefully know more about it than I do anyway.

Let me give an example of mixing formats to achieve a specific combination of desired properties. For the original version of

[Swords & Soldiers 1](http://www.swordsandsoldiers.com)on the Nintendo Wii we wanted to minimize size on disk and size in video memory. In video memory we used palette textures, but on disk we also ZIPped those. ZIP cannot be used by the videocard but it makes textures a

*lot*smaller. The downside of this is that unZIPping costs additional loading time when starting the game. However, I didn't care much about loading times because the Wii was quite fast compared to the amount of disk space available for downloadable games, so loading times were going to be fine anyway.

Here's the big overview this blogpost is all about. It compares DXT, ETC, PVRTC, palettes and several more basic formats. Creating these was a

*lot*of work so you'd better click them for a good look! ;)

![](../../assets/aa89b8ce263ddbaa.gif)


![](../../assets/aa89b8ce263ddbaa.gif)

*Click for full resolution*![](../../assets/16a2398c309bca07.jpg)


![](../../assets/16a2398c309bca07.jpg)

*Click for full resolution*If there are any mistakes in the descriptions please let me know in the comments so that I may correct them!

An interesting note here is that Android devices differ so much that texture format support varies from phone to phone. Apparently the solution is to either only use ETC1 and uncompressed formats (since those are supported on all Android devices), or to create different versions of the game using different texture formats per type of phone.

It's important to realise that not everything is always what it seems. The benefit of saving your exact texture format on disk (through DDS or TGA instead of something like JPEG) is that you can load the texture right into video memory. You might think this means fast loading times, but this is not always the case: if reading from disk is slow (for example when reading from a DVD) then this might turn out to be a bottleneck. If your processor is fast and your disk is slow then using ZIP or JPEG might actually give you faster loading times, despite the additional processing needed. Note that in the case of Swords & Soldiers 1 this was not the case: the Wii had a small but very fast hard disk.

One final consideration I'd like to mention is framerate. In most cases texture formats don't really influence framerate: the performance bottlenecks are usually fillrate, polygon count, post processing or something on the CPU. As long as all the textures being used all fit into video memory simultaneously they won't influence performance much. As soon as you grow out of video memory however, you're in trouble. On console your game might crash or show broken graphics due to this. On PC you're less likely to see anything so obvious: PC drivers can start swapping textures between video memory and normal RAM. This is devastating to performance but you might not notice this if you're working on a fast development PC. Be sure to keep a close watch on your texture budgets, even if everything seems to still work fine on your own PC!

Texture formats can also influence fillrate. When reading the texture it might get cache misses, slowing down the GPU. I won't go into too much detail here, but the thing to keep in mind is that making your textures much higher resolution than how they're shown in-game might reduce the framerate. If you zoom in and out a lot then mipmapping is a good solution to solve this. It also helps a lot to use a texture format with few bits per pixel, like DXT1.

Some hardware (including some of the current gen consoles) also support tiled textures. Normally a “tiling texture” refers to a texture that can be repeated, but that shouldn't be confused with tiled texture formats: tiled textures in this case refer to a certain memory layout of the texture that reduces cache misses. I won't go into detail on that here either, but if you're running into performance problems due to slow texture reads it might be worthwhile to check whether your specific platform supports tiled texture formats.

Each game and platform has its own requirements and I hope this series of posts has helped you understand the various options for handling textures. Finally, for those who don't have time to seriously look into this and just want some quick and dirty advice: if you're on PC or console DXT1 is usually the best option, or DXT5 if you need alpha.

*See also:*

-

-

-

-

[Texture formats for 2D games, part 1](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-1.html)-

[Texture formats for 2D games, part 2: Palettes](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-2.html)-

[Texture formats for 2D games, part 3: DXT and PVRTC](http://joostdevblog.blogspot.nl/2015/11/texture-formats-for-2d-games-part-3-dxt.html)*PS. We're looking for interns for the coming period! We have openings in the fields of C++ coding and 2D art! Check here for more info:*

Great series! Thank you so much for writing it. : )

ReplyDelete^_^

DeleteIn your table you say that non-pow2 PVRTC1 textures are supported by iOS since 8.0. Can you point me to official documentation regarding that fact? I was looking around but couldn't find anything.

ReplyDeleteAn experienced iOS dev told me so. I just checked and I also can't find any documentation on that. I'll ask him whether he has any references on this.

DeleteSuch a beautiful series. Thank you very much.

ReplyDelete