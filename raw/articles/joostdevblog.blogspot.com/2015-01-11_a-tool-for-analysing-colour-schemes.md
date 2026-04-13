---
title: A tool for analysing colour schemes
url: http://joostdevblog.blogspot.com/2015/01/a-tool-for-analysing-colour-schemes.html
author: Joost van Dongen
published: '2015-01-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Color and Light: A Guide for the Realist Painter](http://www.amazon.com/Color-Light-Guide-Realist-Painter/dp/0740797719)by James Gurney. It contains a number of really interesting ideas about colour schemes, so I was curious how these relate to existing games. I was especially curious about

[Proun](http://www.proun-game.com): when creating the art for this game I did not know anything practical about colour theory. I just tweaked the colours until they looked good. Apparently this was successful, since reviewers were extremely positive about Proun's visuals and vibrant colours. How then do the colour schemes in Proun relate to Gurney's colour theories? To analyse this I have developed a simple little tool that visualises the colour scheme in an image. You can download the tool and source further in this post. So let's have look: what are Gurney's ideas and how do they relate to Proun's art?

The concept I found most interesting in Gurney's book is

*gamut mapping*. To understand this we first need to know the colour wheel. This shows all the colours in a circle. Towards the inside the colours desaturate towards grey. This means that the strongest colours are at the outside. The colour circle is independent of light/dark: each of those colours can still be made lighter or darker.

![](../../assets/9ba4cafa772c1026.jpg)

The idea is that you pick a few colours and only use the colours that can be mixed using those colours. This limits the number of colours that can be used in an artwork. Usually one would pick three colours. This creates a triangle on the colour wheel and we can only use the colours inside the triangle. The area of allowed colours is called the "gamut mask".

![](../../assets/269c1ec2db70f8c4.jpg)

The big revelation to me is that this means that only the three chosen primary colours can be fully saturated. All other colours will be less saturated since they cannot be on the outer rim of the colour wheel, no matter how bright the chosen primary colours are. This limits the colour usage and keeps an artwork from becoming a "fruit salad" as Gurney calls it.

![](../../assets/4bb2d8e7f9d869f5.jpg)

The colour gamut can even be on just one side of the colour wheel, greatly limiting the colour scheme in an artwork. While normally an artist would need to be careful not to use colours too much, when using a limiting gamut it becomes possible to aim for using the brightest colours allowed within the gamut and still achieve a harmonious whole.

I suppose experienced artists might have many other tricks to achieve good colour schemes, and there is probably some really good art that totally doesn't fit what Gurney explains. Nevertheless the colour gamuts seem like a very sensible and useful tool to me. This made me curious: how do the colour schemes in Proun relate to them?

To be able to exactly analyse the colour schemes of existing art I have hacked together a little C# tool: Joost's Colour Wheel Visualiser. It simply loads an image (JPG or PNG) and shows which parts of the colour wheel are used in that image. You can download the tool (including source code) here:

[Download Joost's Colour Wheel Visualiser.zip](http://www.proun-game.com/Oogst3D/BLOG/Joosts%20Colour%20Wheel%20Visualiser.zip)(24kB)

*(Note that a recent version of .NET is needed to run it.)*

Now that we have this tool, what do Proun's colour schemes look like? Let's have a look.

![](../../assets/e1128324b230ec27.jpg)

Surprisingly, it turns out that most of these form quite clear triangles. Apparently while searching for colours that look good together I accidentally used Gurney's theories quite exactly! I happen to even vary between the schemes he gives as examples: some gamuts are mostly on one side of the colour wheel, while others are quite exact complementary schemes.

One thing I was never really satisfied with in Proun is the colours of the opponents. Those are only seen all together at the very beginning of a race and I always felt like they didn't look good together. When analysing those colours using my Colour Wheel Visualiser it quickly becomes clear why. As you can see in the image below their colours are random splotches on the colour wheel, unrelated to the other colours in the image.

![](../../assets/ceac0688359e2dc8.jpg)

I think I might have been able to fix this problem by using different colours for the opponents depending on the track, so that I would have been able to match their colours to each track's colour scheme.

[Next time, Gadget](https://www.youtube.com/watch?v=-_2_cJxYYhM)!

I also tried my tool on screenshots from

[Awesomenauts](http://www.awesomenauts.com), which was designed by the

[Ronimo](http://www.ronimo-games.com)art team. In the images below you can see that the colour scheme is all over the place. It really is an explosion of colour, as is fitting for the over-the-top eighties themes of Awesomenauts. Nevertheless you can see that even in the top image the colour scheme ignores large parts of the colour wheel, so even there the colour usage is limited. I think our artists did a great job on the art for Awesomenauts, so this is a good example of how not all good art needs to keep to Gurney's colour gamuts.

![](../../assets/67ed11e7bcb1a73b.jpg)

Here are the colour schemes for a number of other games:

![](../../assets/1b124b2353205032.jpg)

By the way, note how in all the screenshots analysed in this blogpost Proun is the only game that uses the purple/pink/magenta area. This might be accidental, but it seems like this part of the colour wheel is used quite rarely in games.

I am going to try to use Gurney's ideas in the art for

[Cello Fortress](http://www.cellofortress.com). One particular challenge I see there is that the player's tanks should be immediately recognisable. I currently make the tanks stand out by using extremely bright colours for the tanks, but this will be difficult when using a limiting gamut according to Gurney's rules. I am quite curious how that ends up. If anyone has any tips on how to tackle this, then please let me know in the comments!

![](../../assets/8fda659ac9b48505.jpg)

Very cool, thanks for making that available…to PC users at least. IS there some way to run it from the web for us deprived Mac types?


ReplyDeleteBy the way, the color wheel is really more of a 3D sphere. Another challenge would be to find some way to display/navigate gamuts that way!

I think you might be able to run it on Mac and Linux already using Mono.


DeleteRepresenting all colours is indeed a 3D shape, not just a circle, but the idea Gurney explains is that you can make the colours lighter and darker freely. The gamut does not limit brightness, only saturation and hue.

Hi Joost, thanks for the interesting blog posts. I've enjoyed reading them for a while now.




DeleteThis post tickled my coding fancy, and I implemented a JavaScript version of a gamut mapper on my own blog at http://www.daedalus-development.net/blog-2/.

I look forward to your next post.

Cheers,

Rick

An online version is actually really nice, much more practical for actual use than my little tool. :)

DeleteI've cleaned up my tool a bit, and moved it to http://daedalus-development.net/web_apps/gamut_checker/

DeleteGreat informatin in this blog post.Thanks

ReplyDeleteAbout the colours in Cello Fortress.



ReplyDeleteFirst let me say, that I'm not sure, if the colours need to be changed. The background fits perfectly in Gurney's Ideas, so no need to worry about that. And the flashy tank-colouring has a valid reason, to be as far away from the gamut mask as possible.

That said, let's try to achiev harmonious colouring nevertheless.

One thing I thought of is to start with the flashy colours and gradually fade into the gamut mask, over time. Reason for this approach is, that on gameStart and when tanks respawn they need to pull attention. But while playing, the player has some overview, where his tank is, so it won't have to stand out and you could use that time that time to make it look more appealing.

But there are two potential problems I think of:

1st - I could imagine, that it could become more difficult for the cello-player to keep track of all tanks

2nd - The tank-players could interpret the colour-changing as some kind of feedback from the game mechanics, although it's only a visual thing.

just throwing in some Ideas. Hope there's anything useful within^^

Hmm, making the tanks change colour is an interesting idea! Instead of making it a big change they could also just fade from full saturation to a slightly duller saturation that fits within the gamut mask. That would fix the confusion this idea might give, I think.

DeleteIt's so cool. thanks a lot. :)


ReplyDeleteDid you try your tool on Gurney's image? I got a color scheme that isn't similar to Gurney's

I tried it now and the schemes indeed look quite different from what he draws, although roughly similar.



DeleteOne reason for differences is that I used the hue from standard a HSV calculation, which I think puts the colours on the wheel slightly differently from how Gurney puts them.

Another thing to realise is that the images in my post are scans of prints of photos. During photographing his work and then printing the colours will have slightly changed and during scanning again. They looked quite pale after scanning, so I pumped up the colours a bit in Photoshop for my blogpost. That means that four different steps happened from the original (photo, print, scan, Photoshop). The original colours are likely quite different.

Thanks for your reply~ :)

DeleteGreat colour-schemes and it is very convenient to work with them. I also wanted to thank Joost for the post "What most young programmers need to learn" - awesome! I would recomment it to all my friends (as we are all newb's in the sphere). If you are interested you may view here some of our latest works.

ReplyDeleteI came here simply because I googled "full RGB color wheel". By coincidence, the reason I wanted a full RGB color wheel was because I'm reading Gurney's book at the moment, and wanted to start analysing my own game Spryke's gamut areas.


ReplyDeleteNeedless to say, this is probably the best page on the internet I could have had the fortune to land on! Not only does it contain a RGB color wheel, but also an awesome tool to easily display gamuts from existing images. Thanks for your great work!

Nice to hear you like it! :D

DeleteI have been looking for some like this for awhile! Beautiful work, thank you! Curious, is there a way to set the wheel up as a CMY (YURMBY) color wheel vs a RBG traditional color wheel? Like seen here http://gurneyjourney.blogspot.com/2010/02/color-wheel-part-7.html

ReplyDeletenm, I think I'm mistaken. because heres a traditional. http://gurneyjourney.blogspot.com/2010/02/color-wheel-part-2.html

Deleteso I think it's perfect for what I need, though if you can confirm :)

I'm not sure what your question is. The two colour wheels you link have similar colours, but one has the red area a bit smaller and the blue area a bit wider than the other. Mine is similar to the "part7" link.

DeleteThe two color wheels are arranged differently. A traditional wheel with compliments across from each other (yellow from violet) and a CMY wheel (YURMBY) with yellow across from blue. The wheel you use for the tool, which does it follow or is it possible to swap it out?


DeleteThank you for your time.

There's no option to change the type of wheel in the program. I just had a quick look at my code and the colour wheel is based on standard HSV. I don't know how that translates to the traditional wheel or the CMY/YURMBY wheel.

DeleteThank you for your tools

ReplyDelete