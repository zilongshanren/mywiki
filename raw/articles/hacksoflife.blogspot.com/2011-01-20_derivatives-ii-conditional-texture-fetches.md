---
title: 'Derivatives II: Conditional Texture Fetches'
url: http://hacksoflife.blogspot.com/2011/01/derivatives-ii-conditional-texture.html
author: Benjamin Supnik
published: '2011-01-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://hacksoflife.blogspot.com/2011/01/derivatives-i-discontinuities-and.html)I described how OpenGL often calculates derivatives by differencing nearby pixels in a block. This can cause problems if our UV map has discontinuities.

Even weirder things happe if we use texture fetches inside an if statement. For example, this will produce some very weird results:

if(uv.x >= 0.0)You might think that if you use a texture a ramp of black on left, white on right, you'd get a ramp of texture and then the black texture would seamlessly transition into the hard-coded black from the else statement.

gl_FragColor = texture2D(my_sampler,uv);

else

gl_FragColor = vec4(0.0);

If your GPU and GLSL compiler are in a forgiving mood, this may work; if they are not, you may get a set of mid-gray artifact pixels at the transition point. The problem is this bit of fine print (from the

[GLSL 1.20.8 spec, section 8.8](http://www.opengl.org/registry/doc/GLSLangSpec.Full.1.20.8.pdf)):

The method may assume that the function evaluated is continuous. Therefore derivatives within the body of a non-uniform conditional are undefined.You can't take a derivative inside an if statement. (But since the results are undefined, the GPU can make your life more difficult by sometimes giving you useful results anyway. ) Recall from my past post that a texure2D fetch is like a texture2DGrad with derivatives of the texture coordinate expression. Since the derivative functions are invalid inside if statements, the derivatives passed to texture2D may be junk. In other words, this is bad:

if(stuff)but this is okay:

gl_FragColor = texture2D(tex,uv,dFdx(uv),dFdy(uv));

float dx = dFdx(uv);In other words, you have to use texture2DGrad to move the derivative calculation out of the if statement.

float dy = dFdy(uv);

if(stuff)

gl_FragColor = texture2DGrad(tex,uv,dx,dy);

Why Can't the GPU Get This Right (Except When It Does)

Artifacts due to incorrect derivative calculations inside incoherent texture fetches (that is, some pixels texture fetch, nearby ones don't, the derivative is hosed, and our texture fetch is therefore hosed) are definitely sensitive to the hardware, GLSL compiler, and driver, and I ended up switching out my Radeon and GeForce about 30 times before I wrapped my head around this issue.

This doesn't surprise me. The spec allows undefined behavior. Recall that the derivative is based on differencing the value of an expression across a 2x2 pixel group. To understand why conditionals and derivatives don't mix, we have to understand how modern GPUs handle conditional rasterization.

(What follows is based on

[my reading some docs on R700 assembly](http://hacksoflife.blogspot.com/2010/12/fun-with-glsl-compilers.html); it is best to think of it as a model for how GPUs can work, more or less; I am sure there are lots of subtleties to the R700 that I don't understand.)

The GPU rasterizes pixels in 2x2 blocks, with the same shader executed on four execution units in lock-step. That is, each pixel has its own intermediate registers and state, but all four pixels run the same instructions.

When the shader hits an if statement, the hardware sets a mask for each pixel indicating which pixels are "in" the if statement and which are not. The entire if statement is run on all hardware, but the results for the pixels that are not in the if statement are thrown out due to the mask.

If all four pixels hit the if statement the same way, only then can the GPU jump over the if statement, saving actual work.

So what happens if the if statement is being evaluated for some pixels and not others and we take a derivative? The answer is: lord knows! The expression we are calculating may be only partly updated, incorrect, or totally unavailable for some of the pixels.

Branch Coherence

As a side note, the property of the GPU to run the entire shader on all pixels when only some of them are using the if statement is why the GPU manufacturers will tell you that a conditional is only a performance win if it is

*coherent*- that is, if nearby pixels all branch in the same way. This is because when nearby pixels branch in different ways, the GPU must run all code and throw out some of the results.

## No comments:

## Post a Comment