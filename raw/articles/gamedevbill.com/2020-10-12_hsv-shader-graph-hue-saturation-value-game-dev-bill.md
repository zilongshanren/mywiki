---
title: HSV Shader Graph - Hue Saturation Value - Game Dev Bill
url: https://gamedevbill.com/hsv-shader-graph/
author: Bill
published: '2020-10-12'
source_blog: Game Dev Bill
source_site: https://gamedevbill.com/
category: game programming
fetched: '2026-04-13'
---

![HSV Title Image](../../assets/b98171b4f7535bfa.png)

There are a number of ways to mathematically represent a color. In computer graphics, RGB is by far the most common – Red, Green Blue. Second to that is HSV – Hue, Saturation, Value. This tutorial will go through how to make HSV shader graph nodes to convert between the two, and why you would want to.

This article has a matching [video you YouTube you can find here](https://youtu.be/-CY00eMlTcw). The resulting nodes are available [on github here](https://github.com/gamedevbill/Tutorials/tree/master/HSV_Nodes).

Note that the written article below focuses primarily on the HSV math and graph. The video, on the other hand, covers this math at a higher level, and primarily focuses on examples of using the HSV nodes.

Unity’s shader graph includes one node called Hue. It’s actually a hue shift shader. It does RGB to HSV, adjusts the hue, then converts back, all internal to the node. This covers the majority of HSV needs, so it’s ~~understandable that they didn’t provide nodes giving you raw access to all the HSV values.~~ Edit: Unity does provide a [node to do this conversion](https://docs.unity3d.com/Packages/com.unity.shadergraph@6.9/manual/Colorspace-Conversion-Node.html). So if following along with samples, it’s likely better to use their nodes than mine.

For those moving from [Amplify](https://assetstore.unity.com/packages/tools/visual-scripting/amplify-shader-editor-68570?aid=1011l3QFn), it has the two raw nodes, and leaves a hue-shift operation up to the user to implement

*This article may contain affiliate links, mistakes, or bad puns. Please read the *[disclaimer](https://gamedevbill.com/disclaimer/) for more information.

[disclaimer](https://gamedevbill.com/disclaimer/)for more information.

The butterfly in the title image and screenshots below was [from the asset store here](https://assetstore.unity.com/packages/3d/characters/animals/insects/butterfly-animated-58355?aid=1011l3QFn). The content in the video is from [Gaia 2](https://assetstore.unity.com/packages/tools/terrain/gaia-2-terrain-scene-generator-42618?aid=1011l3QFn) and [this free dragon](https://assetstore.unity.com/packages/3d/characters/creatures/dragon-the-soul-eater-and-dragon-boar-77121?aid=1011l3QFn). Please reply to the [YouTube video](https://youtu.be/-CY00eMlTcw), or ping me on [Twitter ](https://twitter.com/gamedevbill)with any comments or questions.

## What is HSV

If you’ve been working with shaders and game code for a while, you should be pretty familiar with RGB. That’s how color data is stored-in and passed-through any shader. Even the final value returned from a fragment shader is done in RGBA (red, green, blue, alpha).

To understand the how and why of using HSV, we need a brief intro to what it is. While [wikipedia](https://en.wikipedia.org/wiki/HSL_and_HSV) has a good visualization of how all three aspects interact, I prefer a simpler mental mode. That of the color picker.

![](../../assets/d1a15244c8e3d743.png)

This is an HSV picker. You may never have realized it, but HSV fits really well into how we think about colors, which is why color pickers are generally built around HSV, not RGB. If you were comparing two colors in the real world, you’d first think about their Hue. This is represented by the rainbow on the right. Then, if hue’s matched, you’d think about how vibrant the color was (saturation) and how bright it was (value).

## When do you need HSV shader graph nodes

There are a lot of different reasons you’d need a HSV shader graph nodes. The most common of which is that you want to do math on your colors in a way that suits the HSV color space. For example, if you are trying to help customers that are colorblind, you can either crank the saturation up everywhere (which would help someone like me), or allow the user to specify which hue’s they can’t see, and then you selectively hue shift just those. Battlefield 4 & 1 did essentially this, though for some reason [Battlefield V](https://amzn.to/30T2uqm) dropped the colorblind mode.

Another situation is where your source color data is in HSV. Such as rendering a custom color picker. Here your input would be HSV, and you convert to RGB before shader completion.

HSV logic can be especially helpful during full screen effects. It can be easier to do a chroma-key identification using the Hue. For info on how to apply shader graphs to full screen post-processing, see [my article on the subject](https://gamedevbill.com/full-screen-shaders-in-unity/).

## How to make an HSV shader graph

The math to convert back and forth can be a bit complicated, which is why it’s written about so much. Today I’ll cover the concepts at a high level, then jump straight to the optimized version when creating the HSV shader graph nodes.

### Inefficient RGB to HSV

#### Value Calculation

The first thing you’d do in a brute force computation would be determine what the largest of the RGB values is. Whatever that max is, happens to be your Value output.

#### Saturation Calculation

After calculating Value (max) you then work out the minimum of the RGB inputs. The Saturation is simply (max-min)/max. Note, if actually calculating this, add a small amount to the divisor to avoid a divide by zero. Or simply say if(max==0) Saturation = 1.

#### Hue Calculation

This is where the expensive math comes in.

//adding 1e-20f to avoid divide by zero... float delta = rgb_max - rgb_min + 1e-20f; float hue; if (r == rgb_max) hue = (g - b) / delta; else if (g == rgb_max) hue = 2 + (b - r) / delta; else hue = 4 + (r - g) / delta; if (hue < 0) hue += 6; h = hue / 6;

Essentially, this boils down to, subtracting the two channels that are not the max, and dividing that by the (max-min) we were able to use earlier. What makes this so expensive is that shaders are not good at branching logic.

### Efficient RGB to HSV Shader

This efficient shader is seen in several places online, but seems to have [originated here](http://lolengine.net/blog/2013/07/27/rgb-to-hsv-in-glsl). I’ll convert it to an RGB to HSV shader graph node step by step.

First we just set up some constant values we’ll need later.

float3 rgb2hsv(float3 rgbIn) { float4 K = float4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);

![](../../assets/aa5d1e3169661c02.png)


![](../../assets/aa5d1e3169661c02.png)

Next we take the inputs, and the constants, and feed them through some weird lerp/step functions. Remember step(a,b) returns 0 if b < a, and 1 otherwise. Which means feeding that into a lerp is sorta like an if() to work out which input is bigger. By feeding the results of the first lerp/step into the second, we’re able to work out which of the RGB inputs is largest.

//Two values P & Q created from input & constants float4 P = lerp(float4(rgbIn.bg, K.wz), float4(rgbIn.gb, K.xy), step(rgbIn.b, rgbIn.g)); float4 Q = lerp(float4(P.xyw, rgbIn.r), float4(rgbIn.r, P.yzx), step(P.x, rgbIn.r));

![](../../assets/dcd5e9cb6effd6e9.png)


![](../../assets/dcd5e9cb6effd6e9.png)

Calculate the delta we mentioned in the concept section (max – min).

float d = Q.x - min(Q.w, Q.y);

![](../../assets/4b3317331af59141.png)


![](../../assets/4b3317331af59141.png)

Lastly we take all that, and combine it to make our result.

float e = 1.0e-10; //to avoid divide by zero return float3( abs(Q.z + (Q.w - q.y) / (6.0 * d + e)), //H d / (Q.x + e), //S Q.x); //V

![](../../assets/14e6f04f3207c527.png)


![](../../assets/14e6f04f3207c527.png)

And lastly the full graph.

![](../../assets/3f28133a8f5b4726.png)


![](../../assets/3f28133a8f5b4726.png)

### Efficient HSV to RGB Shader

The HSV to RGB conversion is simpler than the other way around. So I’m going to skip the inefficient version and just jump to efficiency.

Similar to RGB to HSV, we first set up some constant values we’ll need later.

float3 hsv2rgb(float3 rgb) { float4 K = float4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);

![](../../assets/d5c8ad3d5fd65cad.png)


![](../../assets/d5c8ad3d5fd65cad.png)

Then we calculate the relative RGB values. Using just the hue (noted here as rgb.xxx), we can work out what the final RGB would be if Saturation and Value were both 1.

float3 p = abs(frac(rgb.xxx + K.xyz) * 6.0 - K.www);

![](../../assets/66c732a8c280b57d.png)


![](../../assets/66c732a8c280b57d.png)

Lastly we use a Lerp to determine how the saturation should affect the RGB values. Then we multiply by Value to set the brightness of the final result.

return rgb.z * lerp(K.xxx, clamp(p - K.xxx, 0.0, 1.0), rgb.y);

![](../../assets/8cd279c342b7be5b.png)


![](../../assets/8cd279c342b7be5b.png)

And lastly the full graph.

![](../../assets/4462971886fc10c2.png)


![](../../assets/4462971886fc10c2.png)

## Usage Example

I’ll cover two usage examples here. The first is not very practical, but I showed it in my [full-screen shader post](https://gamedevbill.com/full-screen-shaders-in-unity/), so might as well describe it here. The will be a little more useful, keying off of Hue to drive some logic.

### Full Screen Example

This example is a bit contrived. In my full screen tutorial, I chose to make an effect that makes part of the screen black and white, and leaves the rest unchanged. For URP, I chose to do that based on saturation. Essentially, this takes the most vibrant parts of the screen, and makes them pop even more by dulling the less vibrant parts.

Where to draw the line is defined in this graph by an input I’ve called Saturationness. That’s totally a word. Ish.

float3 startRGB = tex2D(_MainTex, iTexCoord.uv).rgb; float3 hsv = rgb2hsv(startRGB); //note I can’t do hsv.s. To get the second channel I have to ask for // .g, even though it’s not green I’m getting out. float mult = smoothstep(Saturationness, Saturationness+0.01, hsv.g); hsv.g = hsv.g * mult; float3 endRGB = hsv2rgb(hsv);

![](../../assets/344be6f7772c884d.png)


![](../../assets/344be6f7772c884d.png)

![](../../assets/96512da12da3b288.png)

### Single Model Example

Now for a bit more practical example. There are several more in [the YouTube video](https://www.youtube.com/watch?v=-CY00eMlTcw), so I’m going to keep it simple here.

I’m going to take a two-color butterfly (green-ish and blue-ish) and hue shift only one of the colors (the blue-ish). I’ll do it by converting to HSV, using H to determine which areas to shift, then shifting H and converting back to RGB.

Technically I could do this by checking for the right color using the RGB input, and then calling the provided HueShift node. The downside of this is that it’s often far more complicated to identify a particular color in RGB than in HSV.

![](../../assets/75229060817ba926.png)


![](../../assets/75229060817ba926.png)

![](../../assets/09b7e24513553b81.png)

## Wrapping It Up

This was one of the more mathematical posts I’ve done, but luckily you don’t really need to understand the math. In many other posts, an understanding is required to utilize and extend the shader. Here you can just use the shaders as is to get in and out of HSV. As a reminder, the nodes are up [on github here.](https://github.com/gamedevbill/Tutorials/tree/master/HSV_Nodes)

What you do with those values is up to you.

### References

The optimized version of this logic is all over the internet. From my research, the originator is [here](http://lolengine.net/blog/2013/07/27/rgb-to-hsv-in-glsl), this is also the most concise.

For a more verbose writeup, with some examples, I really liked [this one by Ronja](https://www.ronja-tutorials.com/2019/04/16/hsv-colorspace.html).

Academics are welcome to read up on raw theory [here](https://en.wikipedia.org/wiki/HSL_and_HSV).

Web hosting [provided by BlueHost](https://www.bluehost.com/track/gamedevbill/AboutMe).

*Do something. Make progress. Have fun.*