---
title: 'Depth of field blur: the Swiss army knife that improved even the framerate
  of Awesomenauts'
url: http://joostdevblog.blogspot.com/2012/04/depth-of-field-blur-swiss-army-knife.html
author: Joost van Dongen
published: '2012-04-09'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Proun](http://www.proun-game.com)(for which I discussed the depth of field blur in

[one of my very first blog posts](http://joostdevblog.blogspot.com/2010/09/depth-of-field-blur-in-proun.html)). However, while making

[Awesomenauts](http://www.awesomenauts.com), I learned that it is much more than just a graphics effect. In fact, it even improved the framerate a

*lot*!

![](../../assets/fd5b0e053b9c20bf.jpg)

Initially we didn't have depth of field blur in Awesomenauts, but then the first trailers of the beautiful

[Rayman Origins](http://www.youtube.com/watch?v=MvhwWXF-LfU)were released, and they have some levels where they add a ton of depth of field blur to the backgrounds, which looks great. So we wanted something similar, especially as these kinds of effects help make a 2D game look more like "triple A 2D" (for as much as that is an existing term).

![](../../assets/ccd155ab1ddfaafb.jpg)

Unlike in 3D, doing depth of field blur in 2D is actually incredibly simple. You can just render the furthest objects to a separate texture, blur that, and then render the closer objects on top of that. Since depth of field blur suggests depth to the player, in Awesomenauts I do this a couple of times at different depths, so that the furthest objects get more depth of field blur than closer objects, and thus look like they are further away. This sense of depth works really strongly in combination with the parallaxing and coloured fog that we use on far-away objects.

![](../../assets/f8b3a02b7f381501.jpg)

However, depth of field blur is not just a good looking graphics effect. It also serves an important gameplay purpose. Awesomenauts is quite a chaotic game. This chaos is part of the fun, but amidst that it is very important to make the graphics as clear and readable as possible. Background objects don't have any gameplay impact in Awesomenauts, so by blurring them, we can make them more subtle and make the characters and bullets stand out more.

![](../../assets/27323847047655e3.jpg)

Readability was actually also an important reason why I added depth of field blur to Proun. Because Proun lacks detailed material textures and recognisable objects, it is difficult to judge the distance towards an object. Depth of field blur compensates for this and makes sure the player always focusses on the nearest obstacles, as those are the only ones that are sharp.

However, depth of field blur is usually also a very expensive effect in terms of performance. Since in Proun the rest of the graphics are incredibly simple and fast to render, the depth of field blur easily accounts for 90% of the total time spent rendering a frame. In 'normal' 3D games this is of course a lot less, but depth of field blur remains a rather expensive effect to render.

However, to my own surprise, in Awesomenauts I actually managed to

*double*the framerate using depth of field blur! The reason for this is that our artists use lots of really large fog gradient textures to make the backgrounds look further away and modify their colours. This looks great, but causes an immense performance hit, because these large fog objects on top of each other require an enormous amount of transparent pixels to be rendered. I have not actually measured this, but I wouldn't be surprised if the overdraw in Awesomenauts may be something like 10!

(Overdraw is how many times on average you need to render a single pixel to get the final image. Ideally, this would be 1, so that you render each pixel exactly once. A higher overdraw generally means a lower framerate, so in 3D, there are tons of interesting techniques to decrease it.)

![](../../assets/0de069162f51659f.jpg)

These fog layers turned out to be a big performance problem in Awesomenauts. At some point the game ran at only 15fps on the Playstation 3, which is a far stretch from the 60fps we were targeting at. We did lots of different optimisations to reach 60fps, but the depth of field blur turned out to be the biggest life saver here. Since I was blurring the backgrounds anyway, I simply made the choice to only render them at the really low resolution of 640x360. This does not reduce overdraw, but simply decreases the number of pixels enormously. To improve the framerate even further, I also moved the depth of field blur forward a bit, so that even the closest background objects got blurred and thus got rendered at a low resolution. Because of the blur, this low resolution looks perfectly fine and smooth in combination with the HD foreground.

![](../../assets/b18119d63459d1b8.jpg)

This does introduce some subtle flickering in the background as really small objects alternate between being on and in between pixels, but this is only visible if you look for it and know where to look.

I suppose parts of this approach can be (and probably already are) used for 3D graphics as well to do more efficient depth of field blur, although in 3D a lot of technical difficulties come into play to correctly handle objects that stretch into the distance, and thus are partially far away and partially nearby.

So for Awesomenauts, depth of field blur was a true Swiss army knife: it turned out to not only make the game look better and make the visuals more readable, but it also turned out to improve the framerate greatly! :)

Simple concept with a huge effect. Thanks for sharing!

ReplyDeleteFound on Hacker News

What blur algorithm are you using?

ReplyDeleteIt is a two-pass blur: first I do a vertical blur, then a horizontal blur, in total resulting in a real 2D blur.



DeleteA single blur pass is done by simply taking a couple of samples and getting a weighted average. The weights are not gaussian: I played around with the values a bit until it looked best for our game. The biggest blur takes five samples per pass and the weights are 0.85, 0.95, 1, 0.95, 0.85.

To get extra samples with half the performance cost, I enable bilinear filtering and take the samples exactly in between two pixels. This way the filtering effectually gives me two samples in a single read from the texture. So the five samples I mentioned above really blur using 9 pixels from the rendertexture (the centre sample is at the centre of a pixel).

That is, you effectively weigh the nine texels involved as (.85, .85, .95, .95, 1., .95, .95, .85, .85)?




DeleteTo do so, you sample exactly halfway between the texels? I guess it wouldn't be worth it with these subtle weights, but would I be correct in assuming that you can differently weigh the two-texels-with-one-sample by shifting the texcoord closer to one or the other?

Why do you use a separate sample to get precisely the centre texel? For symmetry of the kernel? You could adjust the weights accordingly. Or you could not care that your blur translates by half a texel. But I guess a tenth sample isn't much of an improvement over nine anyway.

In any case, depth of field for the win. Next time make a cool lens blur...

Indeed, that boils down to the numbers you mention. The subtle differences you mention would probably be an improvement, but one that is so subtle that it is totally invisible. I played around with the values a bit and I chose these numbers have exactly the right amount of blur that I wanted.


DeleteWhen you say "lens blur", you mean Bokeh, right? What is the common method of making that? Someone explained it to me recently and the explanation was exactly what I was already doing in Proun, yet I don't see cool Bokeh effects in Proun. Is the trick that lens blur only gives a useful effect when combined with extreme HDRI?

Yes - you really start to see highlights blooming only when you have HDR images with pixel values over 1.0. Doing the blurring in a photometrically linear colourspace helps too - blurring in a normal gamma-corrected image tends to make the dark areas "grow" more than they would in reality.



DeleteFor a lens blur you'd use a more defined filter kernel as well, like a disk or hexagon rather than a soft gaussian blob.

Love the look of Proun!

When I said "lens blur" I specifically had Photoshop's Lens Blur in mind. (Which, as implemented, is a disaster in terms of runtime, but that's besides the point.) I'm not quite sure what it does. In general, I just mean more high-quality-photography/cinema-like depth of field. One might use the term bokeh in this context.





DeleteWithout having made careful study of it, here are some of my impressions.

Part of the look seems to involve a non-spherical kernel and in particular a non-separable kernel. (In the sense that your current blur *is* separated into an X pass and a Y pass.) Pentagons and hexagons seem common.

Part of it seems to be a really big kernel.

The effect is most visible on small bright picture elements, because this shows the shape of the kernel. However, even on images where it doesn't quite stand out in this way, I would say there's a difference in feel between Photoshop's Lens Blur and, say, its Gaussian Blur. I guess your Kind-of-square blur might actually be closer to the Lens Blur one already.

Hey, maybe you could try rotating your samples by, say, 30 degrees. Who says the sample directions need to be axis aligned, yes? Just perpendicular. Or for a diamond-shaped effect maybe not even perpendicular... (Maybe I'm missing a technical detail here.) Could have in interesting look.

Without careful inspection, it seems to me that with Lens Blur, light bleeds into dark more than the other way around.

That still sounds very much like what I did with Proun, which also doesn't have seperable blur and doesn't have any gaussian falloff in the blur. I think the main thing keeping Proun from having this effect is that my HDRI only goes to something like 1.4 there and to get those really bright disks, I think I would need to go to 10 or something like that.


Delete@Lewis Saunders:

Colour spaces are something I should look into more, someone else also recently told me they are really important for getting a good look. I am still kind of struggling with how that would make the art pipeline very complex if I would want sRGB textures. I guess it would be easier to use sRGB just for the post effects. :)

It feels wrong to me that there is so much overdraw just for 2D fog effects. The artists may be authoring in a dozen discrete fog planes, but surely it should be feasible to combine those into fewer passes - surely all you're doing is lerping to a constant colour known at asset creation time, right?

ReplyDeleteYou are absolutely right, this fog could be done in a much more efficient way, for example using multi-texturing and applying the fog gradient directly to the objects instead of rendering fog as a separate object. However, that would require creating new tools for it, since the artists created hundreds or even thousands of background objects and they want complete control over what fog goes where at what depth and with which texture.


DeleteI looked into what they were doing and it turned out the tools required to both make that work well for them and give me efficient rendering were too much work to make. Especially since depth of field blur fixed it so easily anyway. :)

I am a new amateur photographer, and Blog articles like these help me to improve my photography.


ReplyDeletethanks

http://photographyguide99.blogspot.in/2012/09/depth-of-field.html