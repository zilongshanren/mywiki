---
title: DirectX9 vs depth resolve
url: http://c0de517e.blogspot.com/2012/03/directx9-vs-depth-resolve.html
published: '2012-03-17'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

GDC 2012 is over and I bet there are a lot of interesting new techniques to discuss and analyze. I didn't start this work yet (actually I still have to catch up with a few other conferences first, from Siggraph Asia to Eurographics I've not been doing my homework much lately) but what I love when I read papers is not really the application of a given concept (which in scientific papers is often presented in such a biased way that is hard even for experts to really understand the merits of a given implementation), but to find new ideas that can spark new applications.

One such paper was for sure the

[Variance Shadow Map](http://www.punkuser.net/vsm/)paper by Donnelly and Lauritzen, which thought statistically illiterate people like me (I know probability, but I'm really a novice when it comes to statistics) a couple of things about means, averages and how these can be used in computer graphics.After reading that paper a few notions should stick in your mind. The average over a comparison versus comparison over average is one, which applies directly to occlusion, but more in general, that you can summarize a population of samples in a few statistics, which are nicely additive.

If that is the case, then you can apply what you learned in other contexts, with varying degrees of success. And this brings us to the lame technique of the month... As you might know,

[DirectX 9 is a bitch when it comes to depth buffer resolves](http://aras-p.info/texts/D3D9GPUHacks.html). Never-mind reading MSAA depth samples, even accessing depth information is pretty much hopeless unless you want to do hardware PCF shadows. So you end up writing to a colour R32F target your depth, and as you don't have MSAA sample access even in that case, if you want to do some depth-aware effects like SSAO or soft-particles, you're in a lot of pain.Assuming you don't want to pay the ridiculous price of having to do a depth-prepass, with an extra R32F rendertarget, to then throw it away and not be able to use it as a early-depth priming for your next MSAA passes, your depth samples will be summed and averaged, while what you really would like is to compute a min-max buffer or something like that.

Something like that... We have average... We want to know something about these averaged samples... Mhm... Variance to the rescue? Let's try... This is a small test I did in a few hours, so it's not going to be cool. The whole point of this post is not to show a cool implementation but to stress that you should learn meta-techniques, not stress on implementations...

So here it is. I had a grayscale scene (shading = depth because I'm lazy) and on top of it I laid down two "depth fog" passes with a very very sharp falloff (the green and red thingies). That's because a sharp function applied to the depth is what you want to stress the worst case of fetching the average depth at object boundaries instead of the correct one.

This is what it looks accessing the MSAA R32F depth, averaged:

Notice the horrible edges...

This is how it looks by computing mean and variance in a 16bit ARGB buffer, and then offsetting the depth used in the fog computation by some function of the variance. This is to "emulate" a min-max buffer, where we choose only one of the two endpoints, which works for many effects (i.e. preferring the foreground).

Better, even in the jpeg compressed image... Even better, if we compute out of the variance two depths, then compute the fog with both endpoints, and average, as it would be more correct even having a full min-max buffer...

Detail... Good enough :)

## 3 comments:

Rendering R32F for depth manually is pretty much not needed these days. Just use INTZ format and then you'll be able to sample the depth buffer as a texture (details in my D3D9 Hacks page that you linked to already).


MSAA depth on D3D9 is still a major pain however.

Could you help me solving a shadow mapping issue with wine and directx 9?



If you can please contact me on freenode using IRC, my nick is tizbac

Unknown: Sorry, my knowledge of wine is almost zero, and I don't really frequent IRC anymore.

Post a Comment