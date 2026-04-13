---
title: 'My take on shaders: Color grading with Look-up Textures (LUT)'
url: https://halisavakis.com/my-take-on-shaders-color-grading-with-look-up-textures-lut/
published: '2019-01-14'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

I was having trouble for a while coming up with an interesting enough shader topic for this blog post, and then [Ronja](https://twitter.com/totallyRonja) (whose [tutorials](https://www.ronja-tutorials.com) you should absolutely check out btw) suggested a neat thing with which I had some experience: Color grading with Look-up textures (hereafter mentioned as LUTs). I had to implement a custom image effect for that in our VR game, [PaulPaul](http://halisavakis.com/portfolio/paul-paul/), as the post-processing stack’s didn’t work since we were using single-pass stereo rendering. Therefore, it was a cool thing to go into.

Before I show some code, let me first give a quick explanation of how LUTs work: The whole idea is that we map the scene’s color to a new color based on a color-cube. Since “cubes” is not an image format Photoshop’s familiar with, we have to settle for something like an unwrapped version of said cube. You have probably already come across this weird texture, which looks something like this:

![](../../assets/d6f0a920894d4d8a.png)

The premise of color grading using LUTs is somewhat straightforward, but to get a closer look let’s dive into a hypothetical world where the color blue doesn’t exist (a.k.a. Eiffel 65’s hell). If we were to map all our 2-channel colors into a texture, we would just need a square texture and just be done with it. A simple way to do that would be to map the red channel to the X axis (where left is 0 and right is 1) and the green to the Y axis of the texture (where down is 0 and up is 1). And we would end up with something close to this:

![](../../assets/39132fdb5719e40e.png)

Now, I know it’s hard to see, but let me assure you that this texture looks a lot like these first tiny squares in the LUT above!

Returning into our blue-ful world, we have to face the challenge of doing something like that for our blue channel. Therefore, what we do is quantizing the blue channel into 32 segments. So, basically, each square in the LUT matches a portion of the blue channel. The first one corresponds to blue values from 0 to 0.125, the second one from 0.126 to 0.25 and so on, and so forth. You might stop and think here something along the lines of “whoa, how come the other channels get the whole range from 0 to 1 and blue has to get quantized to 32 segments??? Isn’t that.. color-channel..ist?”. That’s probably the intuitive response (at least that was mine), but as we know, this is computers; there’s no “whole range”. If you notice, each of the **32** squares above are at a resolution of **32**x**32**. See the pattern? The blue channel goes from 0 to 1 via a sequence of squares which doesn’t seem as smooth, but the red and green channels go from 0 to 1 via a sequence of squares too; tiny squares called **pixels**. So every channel is quantized and all is well with the world.

Let’s check some code now:

Shader "Hidden/LUTColorGrading"
{
Properties
{
_MainTex ("Texture", 2D) = "white" {}
_LUT("LUT", 2D) = "white" {}
_Contribution("Contribution", Range(0, 1)) = 1
}
SubShader
{
// No culling or depth
Cull Off ZWrite Off ZTest Always
Pass
{
CGPROGRAM
#pragma vertex vert
#pragma fragment frag
#include "UnityCG.cginc"
#define COLORS 32.0
struct appdata
{
float4 vertex : POSITION;
float2 uv : TEXCOORD0;
};
struct v2f
{
float2 uv : TEXCOORD0;
float4 vertex : SV_POSITION;
};
v2f vert (appdata v)
{
v2f o;
o.vertex = UnityObjectToClipPos(v.vertex);
o.uv = v.uv;
return o;
}
sampler2D _MainTex;
sampler2D _LUT;
float4 _LUT_TexelSize;
float _Contribution;
fixed4 frag (v2f i) : SV_Target
{
float maxColor = COLORS - 1.0;
fixed4 col = saturate(tex2D(_MainTex, i.uv));
float halfColX = 0.5 / _LUT_TexelSize.z;
float halfColY = 0.5 / _LUT_TexelSize.w;
float threshold = maxColor / COLORS;
float xOffset = halfColX + col.r * threshold / COLORS;
float yOffset = halfColY + col.g * threshold;
float cell = floor(col.b * maxColor);
float2 lutPos = float2(cell / COLORS + xOffset, yOffset);
float4 gradedCol = tex2D(_LUT, lutPos);
return lerp(col, gradedCol, _Contribution);
}
ENDCG
}
}
}



Properties look simple enough: we just need our LUT and I’ve added a contribution slider, so that we can adjust how much the LUT contributes to the color grading. Also, in line 22 I define how many colors there will be on our LUT. It’s usually 32 or 16, but it should work for other numbers too.

The vertex shader doesn’t need any changing, so I go ahead and redeclare my fields in lines 44-47. Notice, however, that in line 46 I also declare a float4 named “_LUT_TexelSize”. Now, I have no idea whether or not I’ve mentioned that before, but I might as well do it again: Adding a float4 with the name of a sampler2D followed by “_TexelSize”, gives us a nice field with the dimensions of the texture and the size of their texels. More on that in [Unity’s documentation](https://docs.unity3d.com/Manual/SL-PropertiesInPrograms.html).

In the fragment shader, first thing I do in line 51 is declare a float the value of which corresponds to the number of colors in our LUT (let’s say 32 like the one above) minus one (so 31 in this case). We’re gonna hang on to that cause we’ll need that later.

In line 52 I get the scene’s color, but with a twist: I use “saturate” on the color so that my color values don’t get over 1.0 (or less than 0). This is kind of important, because we map the colors from 0 to 1, so if we have values above 1, we’ll get some nasty artifacts. This is also why this tonemapping technique is applied to LDR images instead of HDR, since it has to cut down the high-range values.

Lines 53 and 54 give me half of the texel size of my LUT, for the X and Y axis respectively. The point of having these is precision in the sampling of the LUT. Finally, I declare a field called “threshold”, which basically corresponds to (COLORS – 1) / COLORS, so, in our case 31/32. This, again, is used for precision and to ensure that we won’t go beyond the LUT’s limits.

In lines 57-59 I calculate the offsets for the sampling of the LUT. The offset of the red channel is equal to: half a texel + the channel value * threshold / COLORS. So, if we have the LUT above, that would be: 0.5/1024 + col.r * (31/32) / 32 = 0.5 / 1024 + (col.r * 31) / 1024 = (0.5 + col.r * 31) / 1024. Seems like a weird number, but think of it like this: if the value of red is 0 that would correspond to 0.5 / 1024, so half a texel to the right from the left of the LUT. If it was 1, that would correspond to 31.5 / 1024, which is half a texel to the left of the first square in the LUT. So far we haven’t taken the blue channel into account, so we’re just in the domain of the first LUT square.

For the green channel it’s a bit more intuitive: 0.5/32 + col.g * 31/32, which gives a minimum of 0.5/32 (half a texel from the bottom) and a maximum of 31.5/32 (half a texel from the top).

Finally, we get the cell of the LUT by quantizing the blue channel, going from 0 to 31. Therefore, the “cell” field will give an integer from 0 to 31, depending on the value of the blue channel.

To get the UV coordinates on the LUT that correspond to the scene color in line 61, all we have to do is use the offsets above: the X coordinate will be determined by the cell number divided by the number of colors (so that it starts from the start of the first cell and goes all the way to the start of the last cell) plus the X offset. The Y coordinate is just the yOffset calculated above.

After I sample the LUT in line 62, I use Lerp with it and the original color, based on the “_Contribution” field to return the final color.

## Generating and importing LUTs

When importing LUTs in Unity you have to be extra careful with the import settings. We’re talking about textures that you sample **by the texel**. You can’t afford half a bad pixel if you don’t want any artifacts. The import settings that do the trick for me look like this:

![](../../assets/c9c3ff44f2e0f936.png)

As far as creating LUTs is concerned, there are plenty of tutorials online, but the gist is this:

You open a screenshot of your game to Photoshop (or your photo editing software of choice) and stick the neutral LUT on it like so:

![](../../assets/dd45946e87002b2d.png)

You do your color adjusments and stuff on it, also affecting the LUT, so you end up with something like this:

![](https://i2.wp.com/halisavakis.com/wp-content/uploads/2019/01/with_lut.png?fit=1024%2C576)

You export your LUT and that’s it! Here’s the LUT used here to play around:

![](../../assets/87790f752f8a00a1.png)

I believe that’s it for now. See you in the [next one](https://halisavakis.com/my-take-on-shaders-ui-sdf-icon-shader/), which I hope will not take as long as this one! ^^”