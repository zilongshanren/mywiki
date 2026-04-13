---
title: Making an HD 2D game look good on an SD television
url: http://joostdevblog.blogspot.com/2011/11/making-hd-2d-game-look-good-on-sd.html
author: Joost van Dongen
published: '2011-11-19'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Awesomenauts](http://www.awesomenauts.com)and

[Swords & Soldiers](http://www.swordsandsoldiers.com)are both 2D games that have been designed for high resolution HD screens. So how do they look on old CRT televisions with their low SD resolutions? The obvious answer seems to be that they should automatically look great: the art is super crisp, because it was designed for a higher resolution. However, what you may not realise, is that

*too crisp*is not a good thing!

The problem lies in anti-aliasing, and in graphical details. Anything that the artists have drawn that is only 1 pixel wide in HD, will start to flicker on an SD screen. This happens for the simple reason that not every pixel will be shown on an SD TV. The art has been made for 1920x1080 pixels on the screen, and only 720x576 of those will be shown on an SD television. As a character moves over the screen, his details will flicker in and out of view as they are sometimes on a pixel, and sometimes in between two pixels.

![](../../assets/3b62bdf19a1bf619.jpg)

This is especially problematic for anti-aliasing: in a 2D game, anti-aliasing of edges is drawn in Photoshop and doesn't require any work from the game. But on an SD television, the pixels that make the anti-aliasing may fall in between two screen pixels, meaning that anti-aliasing is often entirely lost.

![](../../assets/ace214ee32722953.gif)

(Note that this is a problem that is specific to 2D games: in 3D mipmapping is used to solve this problem, and anti-aliasing is rendered in real-time by the videocard.)

So when we render our HD 2D graphics to an SD television, they look noisy and too crisp. Now how do we solve that?

The solution is actually pretty simple. To get an image that is both smooth and sharp in SD, we use an easy trick in both Awesomenauts and Swords & Soldiers: on SD televisions, the game is rendered at a higher resolution than what is shown on the screen, and then sampled back to the lower screen resolution. This is a standard technique in non real-time rendering and is called supersampling.

So first we render the game at a higher resolution (1080x864 instead of 720x576). Then this high resolution image is rendered to the screen by sampling the area beneath each screen pixel. For each screen pixel, I take four samples from the high resolution image and use the average of that. This way really small details are not lost. Instead, they become more subtle, since they are averaged with the pixels around them.

![](../../assets/735b019ef3d8fd50.jpg)

So what resolution do we use for the high resolution image that we sample from? Easiest would be to use twice the screen resolution, but that requires rendering at 1440x1152, which is really high and wastes a lot of performance. I experimented a bit, and it turns out that rendering at 1.5 times the resolution is already enough to get smooth graphics.

This is a good thing, because twice times the resolution does tend to become quite expensive. In fact, at some point SD TVs had a

*lower*framerate than 720p HD TVs, which is why I started experimenting with the exact resolutions to find a better trade-off between performance and quality. At 1.5 times the resolution, the framerate is smooth again.

![](../../assets/41a7156c4cdd5e7e.jpg)

The results look good, and they mean that I don't have to bother with storing all textures on different resolutions for HD and SD televisions, which keeps our art pipeline simple.

This post may seem to be about a really minor detail, but on old SD televisions, this really makes a big difference. Without this technique, both Swords & Soldiers and Awesomenauts didn't look good on low resolutions.

I find it really interesting that if you want to make a quality game, you really need to worry about all kinds of seemingly small details. All those little things in coding, art, sound and design are what makes a game polished, and this post has been about just one little example of the kind of polishing we do on our games.

Next week, I expect to have something really cool to show here, so see you then! ^_^

Heh, and consoles are meant to be easy, because you only have one set of hardware to worry about, rather than testing on a million different CPU/GPU/OS combinations. Goes to show there's always *something* that will muck you up!

ReplyDeleteHaha, yeah, but compared to PC, they still are really easy on the graphics side! :)

ReplyDeletereally interesting! This solution seems well suited to consoles where the hardware is standardized so you know what the performance will be.





ReplyDeleteOne point I have - why not re-sample the 2d graphics when you load them instead of the whole screen at run-time?

Re-sampling at load time rather than render time would definitely use less memory and have higher frame rate, but the technical implementation would be a pain where the new texture sizes were funny numbers, etc.

The full screen super-sampling is just easier to develop and has perfectly acceptable performance?

One thing I really like about your posts is the focus on your real world experience - a lot of programmers would not be able to resist going overboard on an interesting problem on this, but your judgement seems to strike a great balance between solving the problem well but not letting yourself waste time.

Rescaling on load would work as well, but has three rather serious problems:







ReplyDelete1. More work: textures are saved as DDS. To do this, I would have to decode DDS, rescale, and then encode as DDS again. Especially encoding DDS is pretty difficult (gotta choose the correct values), so I would have to include an additional library to do this.

2. Lower quality: DDS works better if the amount of detail is low relative to the resolution. Halving the resolution thus doubles the problems with DDS compression. This is especially visible on animating characters.

3. Loading time problems: we have 200mb of textures. Decoding all of those, then rescaling, and then encoding as DDS again, simply takes a lot of time.

So rescaling on load is definitely worse than rescaling outside the game in the asset pipeline.

Also, this would not win any relevant memory, since the game already fits in memory in HD, so reducing beyond that for SD is useless.

And since SD wins performance versus HD already for the lower resolution, performance issues are no reason to not do the real-time rescaling.

Yes i agree your approach is the correct one, especially for consoles. My only comment is that you could achieve (1) by rendering to texture with a simple multisampling shader rather than sample the textures in software. But i am not arguing, supersampling the entire scene makes sense, is simple, robust, and probably has other hidden advantages.

ReplyDeleteI am not sure I understand what you mean? Of course I use a shader to do all the sampling, since this all happens on the GPU. What do you mean exactly?

ReplyDeleteTo resample the textures at load time, so that they match the screen resolution, you could render to texture using the hardware rather than decode the DDS format in software and sample it using software.






ReplyDeleteWhat I am suggesting is that at load time, you render each 2d DDS file to an off screen texture, one by one. This way you use the hardware pipeline to do the sampling one at load time, rather than every frame.

for_each(texture)

{

texture = load_dds(filename);

actual_texture_for_rendering_the_game = create_texture(x, y);

// set up render target, surface etc. here

set_render_target_texture(actual_texture_for_rendering_the_game);

// use your multisampling shader here to get good sampling

render_quad_with_texture(texture);

release(texture);

}

Obviously, for the XBox, a waste of time where there is no problem with performance. It is also a lot of messing around at load time with render surfaces etc. and even on the PC where scalability may be an issue, 2d rendering probably isn't going to be the bottle neck.

I only really mentioned this alternative to point out that I thought you were showing good practice in finding a solution and running with it, rather than falling into the trap of exploring every possibility.

I think your posts are really valuable to a lot of people, keep blogging!

Ah, in that sense! I guess when I would want to create lower resolution textures during loading, this could indeed be a nice optimisation to make it go faster. :)

ReplyDeleteThis is a really cool. I've had similar problems when taking a game designed for iPad down to iPhone or small Android phones. This might help alot.



ReplyDeleteDo you do things differently when working on PAL vs NTSC resolutions?

Also, are you filling the entire screen? It seems like it would be difficult to find a good way to fit everything on a 4:3 layout when it was designed to look great in widescreen mode.