---
title: Fun With GLSL Compilers
url: http://hacksoflife.blogspot.com/2010/12/fun-with-glsl-compilers.html
author: Benjamin Supnik
published: '2010-12-22'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[ShaderAnalyzer](http://developer.amd.com/gpu/shader/pages/default.aspx); this Windows performance tool from ATI gives you a simple environment: you enter GLSL, hit compile, and look at the assembly that pops out. Perfect! (It also shows you execution cycles, but for my purposes, namely understanding what the compiler does for me, the assembly is key.)

Here are some things I have learned:

RV790 assembly is quite complex. (Thank goodness I don't have to code it myself.) ALU instructions consist of 5 scalar sub-instructions, only one of which can have transcendental opcodes. There's a bit of fine print;

[this](http://developer.amd.com/gpu/ATIStreamSDK/assets/R600-R700-Evergreen_Assembly_Language_Format.pdf)and[this](http://developer.amd.com/gpu_assets/R700-family_instruction_set_architecture.pdf)make useful reading. One thing to note: the ALU has a number of 'small' tricks (absolute value, negation, clamping) 'for free'. Sometimes the compiler will use these tricks, sometimes not.Generally, if you write vectorized code (e.g. uniform work on vec4) the scheduling will work out nicely. But the units of execution really are scaler, so it doesn't make sense to write work that isn't needed.

The compiler inlines pretty much everything, which is just fine by me. (I have no idea if recursion is legal in GLSL, I'd never use it in production, but when I wrote a recursive factorial function, the compiler simply inlined 127 iterations and called it a day. Awesome!)

The compiler understands a reasonable amount of constant folding, including (most importantly) multiply by zero. For example: I write an expensive albedo function: pow(gl_Color,gl_Color.aaaa) and multiply it by a light function that returns vec4(0.0). The result: the compiler nukes the entire code sequence and simply loads 0.

(BTW, pow is expensive - since only one of the five ALU slots can run log and exp, raising each color channel to a non-constant power takes eight instruction groups! Ouch.)

The compiler will remove conditional code when the condition is fully known at compile time. So for example, an if statement where the comparison comes from functions that return constants will be nuked, and one of its two clauses is deleted.

- The compiler does not seem to do inference, at least in the one case I looked at. By inference I mean: if (max(0.6,gl_FragColor.r) > 0.3) will (ignoring NaN logic) always be true, regardless of gl_FragColor. But for the compiler to know this, it has to make an inference - that is, it has to compare the range [0.6..inf) with 0.3. My understanding is that LLVM can do this kind of thing, but when I tried it in shader I simply got the full, expensive, conditional code. Moral of the story: use and apply your human brain. :-)

X-Plane's physical shader is based on conditional compilation - that is, for any given state vector of "tricks" we want to use, we recompile the shader with some #defines at the front which turn features on and off. The result is a large number of shaders, none of which need conditional logic in-shader. Fill rate isn't consumed by features we don't use. (This technique comes from our original use of GLSL to emulate and then improve on the fixed function pipeline. To match fixed-function performance, we had to 'compile out' anything we didn't use, particularly for first-gen DX9 hardware which doesn't give you conditional logic for free.

The problem with this technique (and you can see this in the X-Plane 9 shaders) is that it doesn't scale well with code size. For version 10 we've done a lot of shader work, and hand-optimizing the conditional logic is getting more and more difficult.

My conclusion from observing the compiler is that 99% of the time, I can relax a little bit and let the compiler take care of optimizing the shaders down. In particular, if I define functions for each stage of the shader and use conditional compilation to 'simplify' the rule, then the simple cases will boil down to very few instructions. For example:

float calc_spec()In this mess, our specularity function is subject to conditional removal for non-shiny materials. When we do this, not only is the actual specularity calc removed, but the compiler will figure out that 's' will alwys be 0.0 and nuke the MAD of shadow * specularity into the final lighting sum.

{

#if has_spec

return pow(max(0.0,dot(eye_nrm,sun-vec)),128.0);

#else

return 0.0;

#endif

}

void main()

{

....

float s = calc_spec();

gl_FragColor = albedo * lighting * shadow + ambient + shadow * vec4(s,s,s,0.0);

}

That's a trivial example, but it shows the principle of structuring the components separately and letting the compiler put the mess together.

As a final note: the compiler's optimization is not perfect; I suspect the above technique will 'leak' a few instructions in the simple cases relative to a one-off carefully hand-coded GLSL shader, and the GLSL isn't going to be quite as tight in a few cases as actually writing assembly.

But I can live with that, most of the time. We can always go and hand tune the performance cases that absolutely matter most, and the time saved working on the huge mess that is the conditional shader gives me the time to do that hand optimization where it is most important.

Recursion is not allowed, not even statically.

ReplyDelete