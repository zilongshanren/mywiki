---
title: 'Mini: Code Golfing'
url: https://mini.gmshaders.com/p/code-golfing
author: Xor
published: '2022-08-26'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Code Golfing

### The process of creating minimal shaders

Good afternoon,

This tutorial is a little bit different. Today we're talking about "code golfing".

Code golfing is a coding exercise where you take a piece of code and try to shrink it down as small as possible.

Here's an example of a [shader](https://www.shadertoy.com/view/fstfR8) that is only 316 characters (excluding comments)!

Even a tiny shader like this can simulate pixels on a screen with separate RGB LEDs, a 3D perspective, and depth of field like it's filmed with a real camera. [A lot is possible in 280 characters](https://twitter.com/XorDev/status/1533542252944969728)!

## Why Code Golf?

Code golfing isn't necessary for everyone, but I'll give you a few reasons to consider trying it:

**Understanding:**Code golfing in any coding language will give a better understanding of how the language functions on a deeper level. You will learn all the quirks of syntax and alternative ways to use functions and data types. This knowledge can be applied everywhere!**Optimization:**It's not always the case, but oftentimes, shorter code is faster. When you look for different ways to approach a simple problem, you'll often uncover even simpler ways to solve it. Maybe you can compute something once and store it in a variable instead of recomputing it. When writing the screen shader above, I originally thought it needed to be done in two separate shaders, but I found a way to combine the bokeh with everything else.**Substitutions:**Did you know that`pow(length(x), 2.0) == dot(x,x)`

? How about`x - fract(x) == floor(x)`

? By experimentation, you will learn new logical or mathematical relationships between different functions that can save a lot of computation and greatly reduce your shader size at the same time. This is how I was able to write a[voxel renderer in 190 characters](https://twitter.com/XorDev/status/1505308218863632384)!**It's pretty cool:**And finally, it's pretty cool to be able to write these tiny programs that can generate beautiful images. It feels like magic, and people will probably call you a wizard.

So now that we've got some of the reasons out of the way, let's talk about how it's actually done.

## Tricks and Tips

Here are the steps I take when golfing a shader down, in no particular order:

**Reduce names:**It may be uncomfortable initially, but try getting used to single-letter variables and function names. You may sometimes forget what variables are for, but this is actually helpful for code golfing. It forces you to reread your code, and you'll often find better ways to write it when doing so. Like anything else, your memory will improve with practice, and over time you will establish some standards (for me: p=position, c=color, O=frag output, I = input, etc).**Reduce numbers:**This is pretty self-explanatory.`1.0 == 1.`

,`1000.0 == 1e3`

. Don't forget that with vector constructors, you can use any data type as an input and get converted ("cast") to the new type:`vec4(1.0, 1.0, 1.0, 1.0) == vec4(1)`

. If you're multiplying by`10.0`

, you could instead divide by`.1`

.**Minimize initializations:**If you have two floats "x" and "y", try to initialize them together like so:`float x = 0., y = 1.;`

. Look for opportunities to share data types. If you have a color vec3 and vec4, make them both vec4s. Avoid float/int conversions.**Avoid ifs:**If statements in GLSL take a bit of space, especially if you need an else if. Try using ternary instead. For example:`if (x>y) O = vec4(1,0,0,1); else O = vec4(0,1,0,1);`

becomes`O = x>y? vec4(1,0,0,1) : vec4(0,1,0,1);`

. Much shorter, and there's a lot you can do with it. You can even set multiple variables between`?`

and`:`

.**for(;;) > while():**for and while use the same number of characters, but for has a spot for initializing (before the first semi-colon) and a spot for the final step after each iteration (after the last semi-colon). These are free slots that can be used for lines that otherwise would have to end with a semicolon. Also, avoid using break, and use the condition spot instead! You can also remove the brackets if each line ends with a comma (so it doesn't work with nested for-loops).

Using those tricks will make a huge difference. I tested these tips on a random ShaderToy and reduced it by 40%!

## Common Equalities

Learning mathematical relationships between functions also makes an enormous difference. You don't need to memorize them, but try to understand how they relate to one another. Here are some useful equalities for substitutions that can be used in your code:

**General equalities:**

`floor(x) == x-fract(x)`


`ceil(x) == x+fract(-x)`


`fract(x) == x-floor(x)`


`mod(x,y) == x-floor(x/y)*y`


`abs(x) == x*sign(x)`


If x != 0.0 `sign(x) == x/abs(x)`


`step(x,y) == x>y ? 0.0 : 1.0`


If you know "x" will range from 0 to 1 (otherwise, clamp first):

`smoothstep(0., 1., x) == x*x*(3.-x-x)`


**Vectors:**

`dot(v,v) == pow(length(v),2.)`


`length(v) == sqrt(dot(v,v))`


`normalize(v) == v/length(v)`


`reflect(i, n) == i - dot(i, n+n) * n`


**Trig:**

`radians(d) == d/180.*PI`


`degrees(r) == r/PI*180.`


`cos(x) == sin(x+PI/2.)`


`sin(x) == cos(x-PI/2.)`


An approximation: `vec2(cos(x), sin(x)) ≈ cos(x+vec2(0,11))`


Another approximation: `mat2(cos(x), -sin(x), sin(x), cos(x)) ≈ mat2(cos(x+vec4(0,11,33,0)))`


## Conclusion

Hopefully, this can demystify the magic in those tiny tweet shaders and give you a clue to the process behind them. I had no formal education in math, but with a lot of time and practice, I managed to learn, so you can too.

I challenge you to write a tiny shader with the theme: Exclusive-OR. Please tag me. I'd love to see what you come up with.

Thanks,

-Xor