---
title: 'XNG: GIFs, but better, and also magical'
url: https://blog.mecheye.net/2014/10/xng-gifs-but-better-and-also-magical/
author: Jasper St Pierre
published: '2014-10-17'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

It might seem like the GIF format is the best we’ll ever see in terms of simple animations. It’s a quite interesting format, but it doesn’t come without its downsides: quite old LZW-based compression, a limited color palette, and no support for using old image data in new locations.

Two competing specifications for animations were developed: APNG and MNG. The two camps have fought wildly and we’ve never gotten a resolution, and different browsers support different formats. So, for the widest range of compatibility, we have just been using GIF… until now.

I have developed a new image format which I’m calling “XNG”, which doesn’t have any of these restrictions, and has the possibility to support more complex features, and works in existing browsers today. It doesn’t require any new features like `<canvas>`

or `<video>`

or any JavaScript libraries at all. In fact, it works without any JavaScript enabled at all. I’ve tested it in both Firefox and Chrome, and it works quite well in either. Just embed it like any other image, e.g. `<img src="myanimation.xng">`

.

It’s magic.

Have a few examples:

I’ve been looking for other examples as well. If you have any cool videos you’d like to see made into XNGs, write a comment and I’ll try to convert it. I wrote out all of these XNG files out by hand.

Over the next few days, I’ll talk a bit more about XNG. I hope all you hackers out there look into it and notice what I’m doing: I think there’s certainly a lot of unexplored ideas in what I’ve developed. We can push this envelope further.

**EDIT**: Yes, guys, I see all your comments. Sorry, I’ve been busy with other stuff, and haven’t gotten a chance to moderate all of them. I wasn’t ever able to reproduce the bug in Firefox about the image hanging, but Mario Klingemann found a neat trick to get Firefox to behave, and I’ve applied it to all three XNGs above.

SVG with base64 embedded JPEGs for each frame. Neat idea, but they don’t seem to work that well in Firefox (stuttering or stopping altogether).

why not just use a video codec?

Because that doesn’t work in an <img>

Neat hack. But yea, Firefox ruined your party :)

I’m using FireFox and everything looks great. I DO have Flash enabled. When I did not lots of videos and animated GIFs did not work.

Too bad this is all manual, it’s very cool stuff.

Do they have any kind of delta compression between frames? Otherwise I can see filesizes being quite big, which is kind of why people use GIFs so much.

I didn’t write any in my example XNGs, but it would be entirely possible to implement GIF-style temporal compression.

That’s a clever idea. The only thing that I find a bit worrying is the resulting file size. But I think there might be some optimizations possible – did you already try to only overlay smaller images that contain just the parts that actually change from one frame to another?

I’ve played a bit with the SVG and it seems to me like Firefox does behave a little bit more responsive if instead of animating the “visibility” property of the images the “width” gets changed. The changes in the format would be to remove the width=”100%” from the tags and change the tags to – it also shaves of a few more bytes from the overall file size.

Whoa, thanks! I’ve updated all three XNGs to fix this.

For the demo purpose I’d recommend redesigning the gangnam style example to utilize a couple of tricks that are possible thanks to the way this is set up. The first frame of the animation could have been turned into a “background” and the animation could have just been the very center of the image where things are changing. Doing this you could utilize having different jpeg compression qualities for parts of the animation.

But I fear that this type of animation is rather useless for larger animated images. I’d imagine that there will be some interest in using this for small lossless animations, like YouTube’s occasionally animated logo, where JavaScript is not an option however for larger images “xng” will just take up too much data and that won’t be helped by the fact that it cannot be displayed until it is fully loaded.

I think that GZip tends to take care of a lot of that (the Gangnam Style XNG is the smallest one), but yeah, there’s plenty of possibilities for optimization by doing sub-image updates or similar.

From the sounds of it, you’re on your way to re-inventing Motion JPEG. (I’m not ragging you when I say that.)

I developed simple chrome app to make XNG file.

It also able to extract image from video and convert it into XNG format.

You can fork @ https://github.com/mdfirthous/xng-maker

Would this support alpha transparency? I’m trying to find a better solution for a transparent gif animation because I have an animated client logo that appears over a gradient background and when the page gets resized the gradient color behind the image also changes. Trying to use a single color dither to transparency doesn’t work so hot with the gif format in this instance. I tried to convince my boss to go with a static png instead but he’ll have none of it, lol.

You probably want to use a video tag and WebM, which can support alpha transparency.

Hi! i was saw this post a while ago, and i notice dont have any notice about this awesome format. Only i have a few questions:

this support the all features of apng format?

you release a program or tutorial to make xng “images”?

This will be a open source?

Besides that i hope you did it, because i wait since i read this blog a time ago :)

Thanks for your awesome advance!

Congratulations, you’ve made my Firefox to lag to death while trying to view these hackish pictures. Double EPIC WIN achievement is: you did it without Java Script and/or video or canvas since I have interactive stuff disabled by default.

It is quite an achievement to push browser to its limits by using only “passive” content without obvious scripts and so on. Mere attempt to view page with hackish pictures makes browser to choke, even without JS/vid/canvas.

How the hell you do that? CSS tricks over png file regions? Either way, I’m sorry but “proper” animations play MUCH faster, be it apng or gif or even full blown webm/vp9 from youtube.

Wow, it’s like you didn’t even read any of the above comments =))))