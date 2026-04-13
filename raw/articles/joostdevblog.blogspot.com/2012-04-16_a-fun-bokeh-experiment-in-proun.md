---
title: A fun Bokeh experiment in Proun
url: http://joostdevblog.blogspot.com/2012/04/fun-bokeh-experiment-in-proun.html
author: Joost van Dongen
published: '2012-04-16'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[last week](http://joostdevblog.blogspot.com/2012/04/depth-of-field-blur-swiss-army-knife.html)and discussing it in the comments got my mind back on the "Bokeh" effect. Bokeh is an advanced form of depth of field blur that is currently used in lots of tech demos to show what the next console generation will be capable of. So that got me curious again as to how Bokeh is made. I have been experimenting with it in

[Proun](http://www.proun-game.com)and have some nice images to share!

Bokeh is the effect that when there is strong depth of field blur, bright lights in the background become bright spots, often visible as circles or hexagons. This is a real lens effect that can also be seen in photographs, and it looks pretty cool, since it adds some definition to an otherwise completely blurry depth of field blur effect.

A nice example of rendering Bokeh on the videocard can be found in Epic's

[Samaritan](http://www.youtube.com/watch?v=XgS67BwPfFY)demo. Although the style and look of this demo don't really appeal to me, Epic shows lots of really cool effects here that they think will be possible on the next console generation. That essentially means that these effects are already possible on current high-end PC videocards, and thus they managed to make this run on a single GPU this year.

![](../../assets/74e34df7189bd4dd.jpg)

I was curious about this and wondered how Bokeh is implemented. It turns out there are several techniques to do it, but the simplest seems to be to simply have a really large depth of field blur area, with usually either a circular or a hexagonal shape. So you just take lots of samples in a large area for the depth of field blur, and that's it.

The caveat here is that to get a good framerate, most games use a couple of tricks to render depth of field blur efficiently: blur is calculated in separate horizontal and vertical passes, which massively reduces the number of samples needed for a smooth blur effect. Also, the blur areas are usually kept relatively small to be able to calculate them quicker.

[Awesomenauts](http://www.awesomenauts.com)is no exception to this, but Proun actually is: Proun already has a much more advanced form of depth of field blur than most current games and to my surprise it turned out it basically already does the Bokeh effect.

So why are we not seeing those circular splotches in Proun then? The reason is rather simple: Bokeh is seen when small but very bright spots are being rendered with depth of field blur. Proun does not have any really bright and visible lights or spots, so there is nothing that could cause these circles to appear!

![](../../assets/c9d7c60c3bebc8b6.jpg)

Another problem is that Proun's HDRI is limited too much for Bokeh. HDRI is the effect that colours can be brighter than the standard 0-255 range that Photoshop and your monitor usually use. Of course, brighter colours than 255 are simply capped by the monitor, since it cannot show anything above 255, but when blurring in-game, colours brighter than 255 become really important. I wrote

[a blogpost](http://joostdevblog.blogspot.com/2010/09/overbright-colours-blur-and-faking-it.html)about that a long time ago and an image I made then explains it rather well:

![](../../assets/ea19447e9338ff8f.jpg)

Now the problem is that in Proun I have used a trick to get HDRI without costing any performance. This trick, however, limited the HDRI to 400, which is above 255, but not far enough above it to really get these bright Bokeh spots. That's another reason why we are not seeing any Bokeh in Proun.

So as an experiment to see Bokeh, I have used a little trick: I just treat all the brightest pixels as if they are even brighter. In the depth of field blur shader, whenever I encounter a colour that is brighter than 300, I multiply it by 100, as if it were really 30.000, which is insanely bright. And indeed, now the Bokeh splotches suddenly become visible!

Since I have cheated this a bit, the splotches are not nice round circles, but still, it is clearly the same effect. It is a dirty hack and thus doesn't look as good as scenes and effects that are really designed for Bokeh, but it does have a funny effect. Here is an example of what my first experiment looked like in Proun:

![](../../assets/4f1c786539cc8378.jpg)

However, with all those coloured objects in Proun, there are few spots that are actually bright

*white*. So to get more Bokeh, I changed it to handle the red, green and blue channels separately. Now if a spot is bright red, it will create a red Bokeh circle. The way I did this is probably even more hacky and fake, but it actually looks pretty awesome!

![](../../assets/4ff0dd8a54f321b9.jpg)

![](../../assets/43f877ce624a779c.jpg)

![](../../assets/e12492e0b32c7c62.jpg)

![](../../assets/479c78a1e4fab25a.jpg)

I also tried to find the limitations of my Bokeh implementation:

![](../../assets/de416ba6930729a5.jpg)

Unfortunately, this hack breaks all kinds of things in Proun and doesn't really work all that well with the rest of the graphics. So I don't think this is actually an improvement for Proun, but I do think this was a fun experiment! :)

![](../../assets/323dcfc2e92459ce.jpg)

And, since Bokeh is all the hype now, I can finally say that

*I too*have implemented it... ;)

Yeah!

An alternative technique which I've seen used recently is to not rely simply on blurring but to actually draw iris-shapes in the bright spots. Those shapes can be rendered using one triangle if you make sure the iris-texture fits exactly inside its area.

ReplyDeleteYeah, I read about generating those triangles as well, but apparently it had insanely low framerate, while my implementation happily runs in real-time on my PC with a 1.5 year old GPU. The problem of drawing these triangles is finding where to draw them and then creating them, which can be done entirely in shaders, but takes a lot of performance, as far as I saw.

DeleteYes, insanely low framerates tend to be the problem with these techniques :)



DeleteBtw, the technique you're now using can also be adapted to give more faceted iris shapes. Among others, the Tri-Ace team have been documenting these techniques: http://www.slideshare.net/DAMSIGNUP/so4-flexible-shadermanagmentandpostprocessing

I'm also eagerly awaiting the first GPU implementation of that accurate lens-flare paper that's been floating around! These kind of techniques really help to make 'real' what is inherently 'unreal', like the abstract shapes of Proun.

As for other shapes than circles: I have a long list with the positions of all the samples I take, so I could indeed easily give the Bokeh any other shape (like a hexagon) by simply arranging the samples differently. I could even make the hilarious heart-shaped Bokeh shown here: http://www.diyphotography.net/diy_create_your_own_bokeh


Delete;)

Ooh, time to get my scissors out :)

DeleteAn interesting read as always :)

ReplyDelete