---
title: 'ShaderQuest Part 6: Shaping functions'
url: https://halisavakis.com/shaderquest-part-6-shaping-functions/
published: '2021-09-12'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

## Patrons

The 6th part of ShaderQuest is brought to you by these awesome Patrons:

- Not Invader Zim
- orels1
- Sergey Gonchar
- Tiph’ (DN)

## Introduction

In the previous part we covered some info around the syntax of shader coding as well as some info on how colors work and behave in the context of shaders. But changing the color on a fragment shader can only get us so far. We can obviously get more visual information when we start using textures, but for now I want to cover some useful methods that can help you get more interesting procedural results and will come in handy in more ways than you can imagine.

These methods are also covered in [the book of ](https://thebookofshaders.com)[shaders](https://thebookofshaders.com/05/), the interactive editor of which is amazingly useful, so I definitely suggest checking it out as well.

For each method I will also include an embedded Shadertoy shader that you can open in a separate tab and change properties interactively to see how the methods work in detail. Just click on the name of the shader at the top of the Shadertoy window.

## Shaping functions

### Using UVs

It’s not uncommon that the methods below will be used using UV coordinates as their inputs. In environments like [Shadertoy](https://www.shadertoy.com) where you write GLSL fragment shaders, you have no geometry to use either way, so your UV coordinates represent the whole area of the output.

For clarity, the shaping functions below will be applied onto a quad that uses the full UV range on its one face. A visual representation of the UV coordinates looks like this:

![](../../assets/261beb4770d88083.png)

`float4(i.uv, 0.0, 1.0)`

in an unlit shaderHere, I’m outputting the value of the X component of the quad’s UVs as the value of the final color’s red channel, and the value of the U component of the quad’s UVs as the value of the final color’s green channel. You can notice how the coordinates match the colors:

- On the bottom left corner the color is black, because both components of the UV coordinates are 0 at the bottom left corner.
- On the top right corner the color is closer to yellow, because both components of the UV coordinates are 1 at the top right corner.
- Similarly, the bottom right corner is red because the UV coordinates there are equal to
`(1,0)`

, while the top left corner is green because the UV coordinates there are equal to`(0,1)`

.

Outputting the individual UV components as colors makes their behavior even more apparent.

#### UV.X

![](../../assets/56249f0f2b9607fa.png)

`float4(i.uv.xxx, 1.0)`

#### UV.y

![](../../assets/71a2cde66d472646.png)

`float4(i.uv.yyy, 1.0)`

When writing shaders for environments like Shadertoy or for image effects, the screen acts like a quad that covers the whole UV spectrum, so everything mentioned here can be applied there too.

### Step & Smoothstep

#### Step

**Step** is a very simple method that’s super useful for masking things in or out, or for when you just want to compare values.

**Step **receives two parameters, **a** and **b**.

- If
**b**is smaller than**a**,**step**returns 0 - If
**b**is bigger than or equal to**a**,**step**returns 1

Using **uv.x** as the second parameter and a threshold of **0.5** in a **step** call gives us the result you can see below.

![](../../assets/b60895ee2b9043f8.png)

`step(0.5, uv.x);`

And here’s an interactive Shadertoy shader demo. Try changing the “threshold” field to see how the output changes.

#### Smoothstep

**Smoothstep** is another very handy method, usually used when we don’t want to have a binary comparison like with **step**.

**Smoothstep** receives three parameters, **a**, **b**, and **x**.

- If
**x**is smaller than**a**,**smoothstep**returns 0 - If
**x**is bigger than**b**,**smoothstep**returns 1 - if
**x**is between**a**and**b**,**smoothstep**returns a smoothly interpolated value between 0 and 1, using this formula:`t*t*(3.0 - (2.0* t))`

, where**t**is the linear percentage of**x**between**a**and**b**. - If
**a**is equal to**b**,**smoothstep**behaves like**step**, but with more calculations.

**Example**

`smoothstep(0.25, 0.75, uv.x)`


![](../../assets/96dfb1616ff4651d.png)

**Shadertoy**

Try changing the **bottomThreshold** and **topThreshold **values and see how the output changes. Also, what happens if the value of **topThreshold** is smaller than the value of **bottomThreshold**?

#### Nodes

![](../../assets/4d78e84dcc9d4c75.png)

![](../../assets/9724813b2087c0bb.png)

![](../../assets/e2dd32b3e85777f7.png)

### Lerp / Mix

**Lerp** (in CG/HLSL) or **Mix** (in GLSL) is another super useful method. **Lerp** stands for **linear interpolation** and, while that name describes what it’s doing, **mix** is more accurate as to how it can be used; it’s a very handy method to mix different values or colors together.

**Lerp** takes 3 parameters, **a**, **b** and **t**.

- If
**t**is equal to 0,**lerp**returns**a** - If
**t**is equal to 1,**lerp**returns**b** - If
**t**is between 0 and 1,**lerp**returns a**linearly interpolated**value between**a**and**b**based on**t**. For example, if**t**is equal to 0.5,**lerp**will return the mean value of**a**and**b**->`(a + b) / 2`


**Lerp** essentially applies this formula:

`lerp(a, b, t) = (1 - t) * a + t * b`


Manually testing out different values for **t** can show you how the results above can occur.

The real power of **lerp** comes from using non-constant values for **t**, whether those come from the UV coordinates, a texture or, as we’ll see later in this post, time. As long as you can get a value going from 0 to 1 you can do cool stuff with **lerp** (same goes for other shaping functions too).

**Example**

`float3 col = lerp(float3(1,0,0), float3(0,1,0), uv.x)`


![](../../assets/fb3510f89ef07d6f.png)

**Shadertoy**

Try changing the colors to see how the gradient changes. You can also try different values for **t**, add or subtract values from it to see what changes in the blending.

#### Inverse lerp

**Inverse Lerp** has, as you can probably imagine, the inverse functionality of **lerp**. Instead of interpolating the input values, **inverse lerp** returns the **percentage** of an interpolated value in terms of its other two parameters.

**Inverse Lerp** takes 3 parameters, **a**, **b** and **x**:

- If
**x**is equal to**a**,**inverse lerp**returns**0** - If
**x**is equal to**b**,**inverse lerp**returns**1** - If
**x**is between**a**and**b**,**inverse lerp**essentially returns the value of**t**that you would require in a**lerp**function to get the value of**x**.

A lot of systems include an **inverse lerp **method or node, but hand-coded Unity shaders don’t, so you’d have to make it yourself:

float invLerp(float a, float b, float x) { return (x - a) / (b - a); }

#### Nodes

![](../../assets/a04c411cf272eb8b.png)

![](../../assets/fa5967573a94f074.png)

![](../../assets/fef3c518895dd792.png)

### Sine/Cosine

**Sine** and **Cosine** are especially useful methods to get interesting shapes, but they’re exceptionally useful when it comes to animated effects due to their periodic properties.

In terms of shapes and animated effects, **sine** and **cosine** can be used interchangeably since their difference is an offset in their phase, for which we usually won’t care.

**Sine** and **cosine** functions take **radians **as parameters, so it’s better to multiply your custom parameters with **π** or **τ** (which is equal to **2 * π**) so you can get more predictable results.

As you probably know from trigonometry:

sin(0) = 0 | cos(0) = 1 |
sin(π/2) = 1 | cos(π/2) = 0 |
sin(π) = 0 | cos(π) = -1 |
sin(3 * π / 2) = -1 | cos(3 * π / 2) = 0 |

It’s worth mentioning that the result of a **sine/cosine** function ranges from -1 to 1, so, depending on your use case, you might want to remap those values to a [0,1] range.

**Example**

`sin(uv.x * PI)`


![](../../assets/20bd76fbe01b4dd8.png)

It doesn’t look all that much like a sine wave but it does make sense if you think about it. Since I’m multiplying with **π** here, this is half a period of a sine wave, starting from 0, going to 1 and then going back to 0. Imagine that this result image is a height map and you’re looking down on a surface the height of which is determined by these values and you can better understand how this can look like a sine wave.

**Shadertoy**

There’s more things to play around with in this Shadertoy. Try changing the frequency and offset to see how the result changes. Also, try uncommenting the **step** method to get a better idea of the resulting values.

#### Nodes

![](../../assets/c05d33e9f1339566.png)

![](../../assets/57c360d2fee018af.png)

![](../../assets/f0050f95d43bdaf0.png)

**Frac/Fract**

**Frac** (in CG/HLSL) or **fract** (in GLSL) is another super useful periodic method that has a lot of applications in creating shapes, animated effects and even debugging.

**Frac** is fairly easy to understand: it’s a method that **returns the fractional part of its input**. Therefore, regardless of the input, the output will always range from 0 to 0.999…9.

The method is also quite useful for debugging purposes, as values that extend above one (like an object’s world position or depth) won’t be accurately displayed for users to understand what’s going on. Using **frac** will divide these values into intervals and make debugging easier.

When viewed in a graph, it presents this saw-tooth pattern:

![](../../assets/97a37e3dccdd1cd5.png)

`frac(x)`

In some cases, though, we don’t want this sudden drop from ~1.0 to 0, so we can actually convert its behavior to that of a triangular pulse with a few simple steps:

- Subtracting 0.5 from the result:

![](../../assets/38d773a6b85c9b95.png)

`frac(x) - 0.5`

- Taking the absolute value of that:

![](../../assets/d528be8df4f3b62c.png)

`abs(frac(x) - 0.5)`

- Multiplying by two:

![](../../assets/14fde71634198c76.png)

`abs(frac(x) - 0.5) * 2.0`

This gives us a wave that linearly goes from 0 to 1 in a periodic fashion.

**Examples**

`frac(uv.x * 4)`


![](../../assets/c413943d2d44da9a.png)

Since I’m multiplying uv.x by 4 you can see that the output is divided in these 4 gradients going from 0 to 1. If I didn’t multiply uv.x and simply wrote **frac(uv.x)** you wouldn’t see any difference from just outputting **uv.x**.

`abs(frac(uv.x * 2.0) - 0.5) * 2.0`


![](../../assets/07f280684b626366.png)

Here you can see how we can get some oscillating values going from 0 to 1, but the transition is much sharper than that of the sine example above, because the values from frac change linearly.

**Shadertoy**

You’ll find both versions of **frac** on this example shadertoy. Try changing the frequency or offsetting **uv.x** to see how **frac** reacts to that.

#### Nodes

![](../../assets/10817cef148c4565.png)

![](../../assets/a9853f959d033f7f.png)

![](../../assets/0b1d0b4258e66f77.png)

### Time

A lot of the value of shaders comes from their ability to animate effects using a **time** value, which usually corresponds to the time that passed since startup. It might seem like a small thing, but there’s no easy and elegant way to animate even simple effects on materials in a game engine without the use of shaders.

All the examples above, and more, can leverage **time** to animate their effects, by simply adding the **time** value to the input of the methods:

`sin(uv.x * PI + time)`


![](../../assets/a27d720cf1adda5d.gif)

Feel free to try adding the corresponding **time** value to other examples too, including the **shadertoy** ones.

It’s worth mentioning that the **time** value is being provided by the rendering environment so you might find it in different forms depending on the environment:

| Shadertoy | `iTime` | float value |
| Unity ShaderLab | `_Time` | float4 value where _Time.x = t/20 _Time.y = t _Time.z = t * 2 _Time.w = t * 3 |

#### Nodes

![](../../assets/8d6802e46f7e8c87.png)

![](../../assets/f790e8f1509b3284.png)

![](../../assets/f4b1e2e7f8bb2729.png)

### Misc functions

There are some other handy functions you can use in shaders, with which you’re probably already familiar:

#### Min/Max

`min(a,b) `

and `max(a,b)`

return the minimum or maximum value between a and b respectively.

#### Floor/Ceil

`floor(a)`

and `ceil(b)`

return the rounded value of the input **downwards** or **upwards** respectively. Some shader environments also provide the **round** method, to round the input parameter upwards or downwards based on its value.

## Conclusion

These methods are the very basic building blocks to create a wide range of effects in shaders without even the need for textures or other inputs. Mixing and matching these shaping functions can get you very far already, but the real fun starts when applying all these methods in combination with textures and geometry.

See you in the next part of ShaderQuest ❗