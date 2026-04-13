---
title: Math in Art - Game Dev Bill
url: https://gamedevbill.com/math-in-art/
author: Bill
published: '2020-09-21'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![Math in Art title](../../assets/3efa6b901ba162eb.png)

This article will cover how to maximize your shader graphs by feeding extra data in through your art – by hiding math in art.

This is a rewrite of [an older article](https://gamedevbill.com/shader-series-4-colors-as-math/), but has been updated to focus on shader graph. It is intended to be a companion piece to [the following youtube video (linked in case embed is broken)](https://youtu.be/FOVrzTAGWNE) :

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

The above video, and some screenshots below, use a free [medeival pixel art pack.](https://assetstore.unity.com/packages/2d/environments/medieval-pixel-art-asset-free-130131?aid=1011l3QFn) The video also uses a great [Bob Ross t-shirt, in case you need it](https://www.amazon.com/gp/product/B01MUGO6KD/ref=as_li_tl?ie=UTF8&tag=gamedevbill0e-20&camp=1789&creative=9325&linkCode=as2&creativeASIN=B01MUGO6KD&linkId=5f896a32f6b9d790cfce7b918cffac24).

Using a texture to store data enables you to provide your shader with four chunks of data (in the RGBA channels) unique every single pixel on your screen. Today I’ll cover three examples: a normal map, noise textures, and positional data.

## Surface Maps

The most common use of math hidden in colors is surface maps. So common in fact, that you may forget those bluish hues are indeed just data. These are things like a normal map, bump map, or height map.

The normal map is probably the most interesting one to discuss. It encodes a 3D vector (xyz) into the color. The way it can do this in full 3D space is to take values that are in the range -1 to +1 and shrink them into 0 to 1. So a color of 0.5 represents 0 in the decoded vector.

Given your perspective of the surface (x is left/right, y is up/down and z is coming out at you), only x and y can have the full range of values. -1 to 1 in the vector, which encodes to 0 and 1 in color. The z value on the other hand, is pointing towards you, so it’s always positive. Here the vector of 0 to 1 encodes to a blue value between 0.5 and 1. Hence normal maps always looking bluish.

## Normals

Without needing much help from us, normal maps can provide some lighting trickery to add detail to an otherwise flat surface.

![Spherical normal map](../../assets/7cc0c6bd7da4fe34.png)

To sample this in a shader graph, use a sampler as you would for any texture, but tell the sampler that it’s sampling a normal map texture.

![normal sampling shader graph](../../assets/92e6f3f7cc151a62.png)


![normal sampling shader graph](../../assets/92e6f3f7cc151a62.png)

### Normals From Art

To create normal maps based on art, you can tell Unity that the texture is a normal map, and select “Create from Grayscale”. Unity will read the texture as grayscale, and treat the values as if they were height. Then it converts that to normals.

![convert image to normal map](../../assets/9535596e72fb0d2c.png)

In my example, I am sampling both the sphere based normals, and one I generated from an image. To combine them, use the Normal Blend node. In the screenshot below I also have a Normalize node. This isn’t technically necessary here, but I always like to re-normalize anytime I’m doing math to my normal data.

![normal blend shader graph](../../assets/fe288f4315940ff6.png)


![normal blend shader graph](../../assets/fe288f4315940ff6.png)

I can take these normals, and put them on a sprite to get a lit effect. Below you can see that the sprite, though flat, will appear spherical and lit.

![normal-lit result](../../assets/4bdd028053c33a84.png)

The full graph to achieve this look is below. Most of the other nodes are unrelated to hiding data in the colors, so I won’t go into them. Watch the YouTube version for more info on the rest of the graph.

Note that the below graph uses a Cartesian Coordinate node, [which is available on the asset store here](https://assetstore.unity.com/packages/vfx/shaders/cartesian-coordinate-shader-graph-node-158568?aid=1011l3QFn).

![full normal sphere graph](../../assets/628f92340089570e.png)


![full normal sphere graph](../../assets/628f92340089570e.png)

## Noise in Textures

The next example of hiding data in art I’ll discuss is noise textures. There are ways to calculate noise on the fly, but sometimes it’s either easier or more efficient to sample it.

For this example, I’ll be using the cloudy texture below.

![cloudy noise texture](../../assets/e4bc87103d4ccd22.png)


![cloudy noise texture](../../assets/e4bc87103d4ccd22.png)

### Dissolve Effect

The above cloud texture can be used for a lot of things, but a common use for something like that is a dissolve effect (or materialize, which is just a reverse-dissolve).

Here I’ll be having the image slowly disappear from above, but with the noise texture affecting the edges. Below is the section of graph that samples my noise texture, and generates a dissolving area that it feeds into the alpha channel.

![cloud based dissolve](../../assets/cdf7be9189d74b2d.png)

Taking that alpha output, I’ll mention one more trick when doing dissolves: dimming edges. Take the alpha value I’m feeding in, and multiply it by something large, and then clamp it in the range zero to one. This creates a value that starts at zero, quickly ramps from zero to one at the edge of the shape, and then holds at one.

![dissolve and dim graph](../../assets/224f94275a253727.png)

Combining all these things creates the full graph below:

![full dissolve and dim graph](../../assets/544f3f539880a67f.png)

![dissolve result](../../assets/e01d477735bba932.gif)

## Positional Data

A third example of hiding data in art is to hide information specific to positions of the screen. For this I’ll take samples from my [heat haze tutorial](https://gamedevbill.com/heat-haze-shader-graph/), and [my intro to shader graph video](https://youtu.be/FLVNfBQgeQc).

What I’d like to do in combining them, is make my heat haze only affect the parts of the screen around the flames. Obviously to do that, I need to know where my flames are. This is where the “positional data in art” comes in.

![evolution of positional data](../../assets/75ead7fda8f9f836.png)

To combine two shaders, it’s generally best to convert one to a sub-graph. In the heat haze example, most of the graph was focused on the haze effect, and part was activating where to do the effect. This makes for a clean spot to sub-graph. Take everything in that old graph except the activating part and convert it to a sub graph.

Then, taking the graph from the intro video, replace the texture sampler with the heat haze sub-graph (this does sampling internally). Here’s what he graph looks like with the activator set to 1, which will heat-haze the entire screen.

To now activate the effect in only some parts of the screen, sample the positional-data texture, and feed that into the subgraph.

![sample activation heat haze graph](../../assets/e5af6f01721fc010.png)

![conditional heat haze result](../../assets/97309dc01b780982.gif)

## Conclusion

That wraps things up. Again, this is mainly here as a supplement to the [YouTube video it’s paired with](https://youtu.be/FOVrzTAGWNE). For more context, be sure to check that video out, and please subscribe to [my channel](https://www.youtube.com/channel/UC__2zJ9MPxfA943H13K6x8g).