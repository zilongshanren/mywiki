---
title: Old Movie Shader Graph - Game Dev Bill
url: https://gamedevbill.com/old-movie-shader-graph/
author: Bill
published: '2020-09-28'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Old Movie shade graph title](../../assets/b7d10014855ceaaf.png)

Old movie effects can take many forms. Some are just black and white, some sepia. Some have dirt & noise that causes bright spots, some cause dark spots. The old movie shader graph we’ll make today will be sepia with dark dirt, but as I go I’ll point out where we could adjust that.

This old movie shader graph tutorial exists to accompany [the YouTube video below (or watch on YouTube)](https://youtu.be/4apbNiPC3yQ). This has enough detail to stand on its own, but is built as a supplement. For many of my videos, the written version has more detail, but today it’s actually the opposite. This tutorial just fits really well in a visual medium, so the YouTube tutorial may make things clearer in places than this written one can.

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

Old movies have a certain grand appeal. If you’ve never watched some of Georges Méliès films, I highly recommend heading down that rabbit hole. If I’d planned ahead better, I’d be wearing [this shirt ](https://www.amazon.com/gp/product/B078V3NCQM/ref=as_li_tl?ie=UTF8&tag=gamedevbill0e-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B078V3NCQM&linkId=9d5d9ace981a958ee4f897ad5ffc6b2e)in my video.

The scene in my video above and screenshots below uses [Gaia 2](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn) and [(free) flatcar train kit](https://assetstore.unity.com/packages/3d/vehicles/land/flatcar-kit-1-75881?aid=1011l3QFn). If you get anything out of this tutorial, I’d love a [subscribe on my youtube channel](https://www.youtube.com/channel/UC__2zJ9MPxfA943H13K6x8g) or a [follow on twitter](https://twitter.com/gamedevbill). Both are also good places to ask for help if anything isn’t working right.

## Setup

There are two bits of setup I want to mention before we get into the old timey shader graph.

The first is post processing. At a minimum, you need to make sure the vignette effect is on. Or add that effect into the shader yourself if you prefer, but I’m going to have mine on. In addition to vignette, it’s likely worth turning on film grain. It’ll add a bit of noise on top of our dirt that helps sell the effect. Lastly I have depth blur on, but that’s more about my scene than this effect.

![post processing settings](../../assets/1825114c47e7e8c1.png)

The second bit of setup is creating a blit system that can run our shader graph as a full screen effect. How to set up full screen shader effects in all renderers is covered on my [previous tutorial here](https://gamedevbill.com/full-screen-shaders-in-unity/). Though, it’s worth noting that only URP supports using a shader graph in this way. For HDRP you’d need to make this a code shader.

## Old Movie Shader Graph

All told there will be four steps to pull off this effect: sepia, screen flicker, spots, and lines.

### Sepia

Step one of our effect will be to fix the colors. This can be done as either black and white, or sepia. Since sepia is just a black and white image tinted to be a little tan, I’m going with sepia. That way if you want it to be black and white, you can just skip the tinting step.

To make the color black and white, feed it into a Dot Product node with the inputs of (0.3, 0.59, 0.11, 0). To remind you what a dot product does, this will take the input RGB and spit out: (R * 0.3 + G * 0.59 + B * 0.11). This is similar to an average, but is clearly weighted most strongly to the G, near one third R, and very little B. This has to do with how the human eye perceives color. If you did a true average (one third each) the image would often look wrong, depending on your scene.

For the tint, multiply the black and white by a color node. A responsible developer would make the color used to tint an input to the shader. So, you should probably do that, as I bet you are more responsible than I.

![Sepia section of shader graph](../../assets/b0824e5cf7e684d9.png)


![Sepia section of shader graph](../../assets/b0824e5cf7e684d9.png)

![](../../assets/62009b2cf3748d92.png)

### Screen Flicker

The next step will be to flicker the screen occasionally. I want to pull off an effect where the screen spends most of its time at the full brightness, but occasionally dips down below that. Start with a Time node fed into a multiply. It’s quite rare that I want Time output without some scale to it, and even when I do, it’s nice to have the multiply there for easy tweaking.

Then feed the scaled time into a Simple Noise node. By feeding a single (time) value into the UV input of the noise method, I’ll get the same random value across the entire screen. This random value will be between 0 and 1.

Next feed that noise into a smoothstep. The larger edge, I’m setting to 0.4. This affects how often the effect occurs. Since our noise is random, it’ll be below 0.4 about 40% of the time. So 60% of the time the screen is normal, 40% of the time it has some hint of flicker.

The smaller number, I’m setting to 0. This determines how strong the affect is. Setting it to 0 keeps it as a relatively subtle effect. If, for example, I set it to 0.39 (while the larger number was 0.4), then any time the noise was above 0.4 it’d be white, and below 0.39 it’d be black, with a ramp in the super narrow window in between. This means generally if the effect was happening, it’d be at full power. In my version, it’ll be random how powerful it is.

![flicker section of shader graph](../../assets/c1c605693dbe4322.png)


![flicker section of shader graph](../../assets/c1c605693dbe4322.png)

### Screen Spots

To pull off the occasional falling spot, create a Voronoi node. The UV manipulation here is the same as my [heat haze](https://gamedevbill.com/heat-haze-shader-graph/) tutorial, where I keep X unchanged, but move Y over time. The difference to the heat haze is that I’m doing an Add to the Y, where I did a Subtract in heat haze. That’s because in heat haze, I wanted the effect to seemingly rise, and here I want it to fall.

Then feed that noise into a step with a very small value. That will result in 0 most of the time, and 1 in very small spots.

Since I want dark spots, I can multiply this by my color. If I wanted white spots, I’d feed this into a one-minus, and then add it to the color.

![old timey spots shader](../../assets/7f1e7e50dabe0028.png)


![old timey spots shader](../../assets/7f1e7e50dabe0028.png)

### Screen Lines

The math for the random lines is conceptually very similar to the spots. The key difference is multiplying X by something large, and Y by something small. The X growth makes the lines skinny, and the Y shrinking makes them taller.

I’m also feeding this into a Simple Noise instead of Vornoi. Voronoi is primed for circle-y noise, and Simple Noise is better set up for boxy noise. So which noise you use does matter.

![](../../assets/6036178205362c87.png)


![](../../assets/6036178205362c87.png)

![](../../assets/aa7e0b89855e505a.png)

## Wrapping Up

As I said in the intro, this was built as a supplement to the YouTube version. Please reach out there if you have any questions or concerns. And a subscribe is always appreciated.

Full graph:

![](../../assets/368f263a99bfb97b.png)


![](../../assets/368f263a99bfb97b.png)

Web [hosting provided by BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

*Do something. Make progress. Have fun.*