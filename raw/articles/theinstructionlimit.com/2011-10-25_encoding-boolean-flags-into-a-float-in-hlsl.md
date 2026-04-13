---
title: Encoding boolean flags into a float in HLSL
url: https://theinstructionlimit.com/encoding-boolean-flags-into-a-float-in-hlsl
author: Author Renaud Bédard
published: '2011-10-25'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

*(this applies to Shader Model 3 and lower)*

Hey! I’m still alive!

So, imagine you’re writing a shader instancing shader (sounds redundant, but that’s actually what they are) and you’re trying to pack a lot of data into a float4 or a float4x4 in order to maximize the amount of instances you can render in a single draw call.

My instances had many boolean flags that changed per-instance and that defined how they were lit or rendered. Things like whether or not they are fullbright (100% emissive), texture transform flags (repeating on x or y, more efficient to rebuild the texture matrix than pass it), etc.

Using one float out of your instance data matrix for each boolean is doable, but highly wasteful. A natural way to fit in many flags into an integer is to use a [bitfield](http://en.wikipedia.org/wiki/Bit_field), but there’s no integer arithmetic in HLSL, and they’re floating point values… how does one proceed?

Here’s how I did it.

## Application side

First, this is how I pack my data into floats from the application side (setting the effect parameter) :

int flags = (fullbright ? 1 : 0) | (clampTexture ? 2 : 0) | (xTextureRepeat ? 4 : 0) | (yTextureRepeat ? 8 : 0); Geometry.Instances[InstanceIndex] = new Matrix( p.X, Rotation.X, Scale.X, color.X, p.Y, Rotation.Y, Scale.Y, color.Y, p.Z, Rotation.Z, Scale.Z, color.Z, Animated ? Timing.Step : 0, Rotation.W, flags, Opacity);

Just putting an OR operator between the flags you wanna put, and keep the flag bits powers of two.

Ignore the rest of the matrix contents, they’re just here for show. (in my case : position, rotation, scale, color, opacity, animation frame and the flag collection).

A note on floating point : in a single-precision floating point number [as defined by the IEEE](http://en.wikipedia.org/wiki/Single_precision_floating-point_format), you’ve got 23 bits for the significand. That means you can theoretically put 23 flags in there! That’s a lot of data.

(also, considering the decimal point is floating, you can effectively put much more than 23 bits if some of them are mutually exclusive…!)

## Vertex shader

Now in the vertex shader, they get passed to an effect parameter through vertex shader constants, and here’s now the decoding works :

int flags = data[2][3]; bool fullbright = fmod(flags, 2) == 1; bool clampTexture = fmod(flags, 4) >= 2; bool xTextureRepeat = fmod(flags, 8) >= 4; bool yTextureRepeat = fmod(flags, 16) >= 8;

I know my flags reside in the 3rd row, 4th column of my matrix, so I grab ’em from that. Might as well cast them to an integer right now since I won’t be using decimals.

Then I can test for values by testing the remainder of the division of each power-of-two. There is no integer modulo intrinsic function in HLSL for Shader Models 3 and lesser, but the floating-point version works fine.

If I set the first (least significant) bit of a number and divide it by two, the remainder will be 1 if that bit is set. Basically, we test if that number is odd or even; odd means the bit is set.

For every other test, we can test whether the remainder is greater or equal to half the divisor. Effectively, we’re masking the bits greater than the one we’re testing, and testing remaining bits for the presence of the one we’re looking for. Here, if we test for the 3rd bit (from the LSB), so masking with 8 (1000 in binary) and testing against 4 (0100 in binary) :

0000 % 1000 = 0000 // 0 < 4, bit not set 0100 % 1000 = 0100 // 4 >= 4, bit set 1011 % 1000 = 0011 // 3 < 4, bit not set 1110 % 1000 = 0110 // 6 >= 4, bit set 1101 % 1000 = 0101 // 5 >= 4, bit set

Enjoy!

Nice tutorial.Thanks for sharing.

Really nice, thanks for that post! Helped me out

Just one question:

how would one implement a “shader instancing shader”?

:D

Sounds useful, but I’m not quite sure how to implement it best.. any quick reference to how you usually do that?

Depends on the graphics library you’re using… here’s an XNA sample that compares different DX9-era instancing approaches : http://xbox.create.msdn.com/en-US/education/catalog/sample/mesh_instancing