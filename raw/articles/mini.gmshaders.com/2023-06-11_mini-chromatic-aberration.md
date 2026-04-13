---
title: 'Mini: Chromatic Aberration'
url: https://mini.gmshaders.com/p/gm-shaders-mini-chromatic-aberration
author: Xor
published: '2023-06-11'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Chromatic Aberration

### Exploring 5 different color shifting effects for games!

Good day,

Today, I want to talk about “[Chromatic Aberration](https://en.wikipedia.org/wiki/Chromatic_aberration)”.

This is a fairly common post-processing effect. Some people love it, some hate it. When done carelessly, it can be distracting, but when used tastefully, it can add a ton to the visual style of your game (especially great for black-and-white games). You can use it to convey urgency (e.g. being spotted or damaged), or it can be used for cinematic emphasis. In any case, I’ll give you the tools you need to make your version as you see fit. Let’s begin!

## Color Shift

The simplest technique is to sample the texture 3 times for each of the RGB components offsetting each sample. For example, you might do:

```
#define OFFSET vec2(0.01,0.01) //Could be uniform
//Set RGBA channels to 1
vec4 color = vec4(1.0);
//Sample RGB channels individually with offsets
color.r = texture2D(gm_BaseTexture, v_vTexcoord - OFFSET).r;
color.g = texture2D(gm_BaseTexture, v_vTexcoord ).g;
color.b = texture2D(gm_BaseTexture, v_vTexcoord + OFFSET).b;
```


This may be fine for a more abstract art style. It’s frequently used to make glitch effects, however, for a more natural look, I like to use a few more samples to blend between them. Here’s an exaggerated illustration:

This looks a lot closer to the photo reference above and gives a nice styled look! Of course, you should be careful to not overdo it (I’d always recommend adding a setting for disabling it).

To achieve this effect, I sampled multiple points in the offset direction, giving each a different RGB weight:

`vec4 weight = vec4(i, 1.0 - abs(i*2.0 - 1.0), 1.0 - i, 0.5);`



“i” starts at 0.0 with the first sample and reaches 1.0 with the last sample. So the first sample is fully blue, but as we move along, we decrease the blue level, increase the green in the middle, and at the end, we get to red. Plotting it looks like this:

Here’s my code for smoothly blended chromatic aberration:

```
#define SAMPLES 10.0; //Number of color shift samples (Even!)
#define OFFSET vec2(0.01,0.01) //Could be uniform
//Color sample and weight sums for weighted average
vec4 color_sum = vec4(0);
vec4 weight_sum = vec4(0);
//Iterate through samples (should be an even number)
for(float i = 0.0; i<=1.0; i+=1.0/SAMPLES)
{
//Sample texture coordinates with offset (-0.5 to +0.5)
vec2 coord = v_vTexcoord + (i-0.5) * OFFSET;
//Sample texture at coordinates
vec4 color = texture2D(gm_BaseTexture, coord);
//Get separate weight values for each channel
//R ranges from 0 to 1, G from 0 to 1 to 0 and B from 1 to 0
vec4 weight = vec4(i, 1.0 - abs(i*2.0 - 1.0), 1.0 - i, 0.5);
//Add color (squared for gamma) with weight factors
color_sum += color * color * weight;
//Add weight totals for averaging
weight_sum += weight;
}
//Compute average (sqrt for gamma decoding)
gl_FragColor = sqrt(color_sum / weight_sum);
```


I’ll include a live ShaderToy demo at the end.

### Direction

If you have a keen eye, you might have noticed my RGB shift illustration showed color shifting in a straight line, while the smoothly blended version blends outward from a single point. This is because I used two different methods for computing the uv offset.

**Linear blending **is done by using the same offset vector for all pixels like so:

`vec2 coord = uv + (i-0.5) * OFFSET;`



**Radial blending** works by interpolating/extrapolating the uvs to a target point.

We can use [mix](https://gmshaders.com/glossary/?load=mix) (or lerp) starting from the pixel uv the target, in our case the center which is always vec2(0.5). Here’s my formula:

`vec2 coord = mix(uv, vec2(0.5), (i-0.5) * OFFSET);`



By using the sample index, “i”, which ranges from 0 to 1, the amount of shift towards the target. We want to make sure the middle sample is unchanged, so we can subtract 0.5 from “i”. Since i-0.5 ranges from -0.5 to +0.5, the samples range from 50% away from the target, to 50% toward the target! This is way too much sample spread and would look extremely blurry so we much multiply this by an “OFFSET” intensity which should be a small value somewhere around 0.01 (resulting in 50*0.01% or 0.5% sample spread).

There’s a third type I want to briefly mention:

**Twist blending** samples in a line perpendicular to the center, giving the appearance of twisting. I’ll leave this one here as a challenge for you to dissect if you wish to:

```
vec2 ratio = res.yx/res.y;
vec2 coord = uv + vec2(uv.y-0.5, 0.5-uv.x) * ratio * ratio * (i-.5) * OFFSET;
```


Resolution is used here for correcting the aspect ratio but isn’t strictly necessary.

### Contrast

Because this effect uses many samples blended together, you may experience more blurring than you’d like to get that juicy color separation. I’ve found that adding contrast to the color weights is a great way to get more color with less sample spreading. I do this with a mix by blending the weights away from the average gray value:

```
#define CONTRAST 2.0 //1 = default
vec4 weight = vec4(i, 1.0 - abs(i*2.0 - 1.0), 1.0 - i, 0.5);
weight = mix(vec4(0.5), weight, CONTRAST);
```


The concept here is similar to what we did with the radial blending only this time we’re doing it with color. A “CONTRAST” value of 0.0 means no color variation between pixels, while a value of 2.0 means twice the color variation!

I’d recommend keeping a contrast value between 0 and 2, but you’re welcome to play around with other values!

## Chromatic Motion

Before I go, I want to show you a cool version I found while writing one of my tiny shaders. This is a different way to add motion blur and give it color.

I’m calling this effect “Chromatic Motion”. Basically, I just set the red channel to the desired grayscale value, but I set the green and blue channels to the red and green channels of the last frame. This has the effect of red leading motion and blue trailing behind 2 frames. Add a little bit of temporal noise for even smoother transitions.

[This looks particularly great in 3D](https://www.shadertoy.com/view/cdG3Wd) with steady camera movement because the color separation varies with parallax.

I’ve published my [Chromatic Motion code here](https://www.shadertoy.com/view/dlKSW3) for anyone interested.

## Conclusion

Chromatic Aberration has many different variations for all sorts of occasions. Many of the principles covered here are shared in other common effects like motion blur, depth of field blurs, and radial blurs. I especially like the trick for adding contrast to the color weights because that can be used in so many different ways. I also use weighted averages all the time and this is just one of many great examples where it is handy to understand.

Check out the [full ShaderToy example here](https://www.shadertoy.com/view/DtGSRt)!

Thanks for reading! Enjoy the rest of your day!