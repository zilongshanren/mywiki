---
title: 'Derivatives I: Discontinuities and Gradients'
url: http://hacksoflife.blogspot.com/2011/01/derivatives-i-discontinuities-and.html
author: Benjamin Supnik
published: '2011-01-20'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

How does OpenGL know what mipmap level to use when you sample a texture in your GLSL shader with texture2D? The answer is that this:

texture2D(my_texture,uv);actually does something like this:

texture2DGrad(my_texture,uv,dFdx(uv),dFdy(uv));In other words, texture2D takes the derivative of your input texture coordinates and uses those derivatives to decide which mipmap level to access. The larger the derivatives, the lower mipmap level. (The actual implementation is more complicated.)

Before continuing, a brief exercise in visualization. Imagine a cube with a single square face visible to us (parallel to the screen). The cube face is textured with a single 256x256 texture. If we zoom the camera so that the cube takes 256x256 screen pixesl, the derivative of the UV map between any two pixels on screen is about 1/256 in both directions, and we want the highest level mipmap. If we zoom out so that the cube takes up only 2x2 pixels, the derivative is about 1.0 in both directions - and we want the lowest mipmap level.

Where Do Derivatives Come From?

The GLSL derivative functions are usually implemented by differencing - that is, the GPU takes a block of 2x2 pixels and differences the variable or expression passed to dFdx and dFdy, to calculate an 'approximate' derivative. Many GPUs rasterize 2x2 clusters of pixels at a time, with the shader instructions for the four pixels run in lock-step, so the hardware can be set up to efficiently "cross" the four texels to find our derivatives.

This means that if there is a discontinuity between those pixels, the derivative may be, well, surprising. For example, consider something like this:

vec2 uv = gl_TexCoord[0].st;What happens if two of the pixels in our 2x2 block have uv.x > 0.5 and the other two don't? well, the answer is that uv.y will be 0.25 bigger for some but not all textures, and the derivative of uv.y will be very big! This in turn will cause texture2D to fetch a low mipmap level, much lower than any other 2x2 pixels that are "coherent". (Coherent here means all 4 pixels have the same boolean answer to the if conditional.)

if(uv.x > 0.5) uv.y += 0.25;

gl_FragColor = texture2D(my_sampler, uv);

One way to think of this is: since the derivatives are found by looking at actual pixels on screen, a discontinuity is seen by the derivative function as a really low-res UV map, and thus a low mipmap level is selected.

Fixing The Derivative

So what can we do? We can provide OpenGL with an expression whose derivative is about the same as our real texture coordinates, but without discontinuities. For example, we can rewrite our above example like this:

vec2 uv = gl_TexCoord[0].st;Our actual texture samples come from a discontinuous UV map, but our derivative comes from the original continuous function.

if(uv.x > 0.5) uv.y += 0.25;

gl_FragColor = texture2DGrad(my_sampler, uv,dFdx(gl_TexCoord[0].st),dFdy(gl_TexCoord[0].st));

Breaking Continuity

I first ran across this while working on the 'tile' shader for X-Plane 10. The tile shader breaks each texture into a sub-grid of tiles and then randomly swizzles the tiles, like a number puzzle that someone has been scrambled. The tile shader hides repetitions in the shader, and (because it runs in shader) it doesn't require additionally tessellating geometry, saving vertex count.

(Using fragment ops to save vertex count might seem strange, but in this case, our base mesh is already heavily cut up based on other criteria; having the texture swizzle run orthogonally lets us subdivide the mesh based on other, unrelated criteria.)

Without texture2DGrad, we would get a set of 2x2 pixel dark pixels at the edge of the tiles. The tiles are induced via some math that includes a floor() function to separate our tile number from our location within the tile. The floor function can induce discontinuities even without conditional logic, because floor is not a continuous function.

Great info!


ReplyDeleteThe discontinuities also very often come into play when you do anything "deferred style". For example, deferred shading/lighting, deferred decals and so on; anything where you compute UVs based on the depth buffer. I ran into this a while ago as well: http://aras-p.info/blog/2010/01/07/screenspace-vs-mip-mapping/

Yep - a classic 2x2 derivative artifact. :-)

ReplyDeleteJust a small correction on:









ReplyDelete"If we zoom out so that the cube takes up only 2x2 pixels, the derivative is about 1.0 in both directions - and we want the lowest mipmap level."

Actually it's 0.5. Your samples will be 0.25 and 0.75 or the like.

Manual derivatives are cool. Here's a pretty unusual and in particular useless shader. Differencing is really only fully continuous for affine inputs. But most of the time your texture coordinates will be projective (even if you don't see them like that because OpenGL unprojects them for you). That leads to another kind of 2x2 blocking, so here's the Fix of all Fixes, that just happens to be as good as invisible: :-)

(If your mip levels are messed up, or you're visualizing the LOD, it's quite obvious.)

#version 120

#extension GL_EXT_gpu_shader4 : require

#define VISUALIZE_LOD 1 // making the irrelevant relevant

#define SMOOTHER 1 // fix blocks

#define MANUAL_LOD 0 // perform grad to lod in shader, as the visualization code already uses it... this is actually a somewhat visible sharpness difference because cards tend to approximate it in various ways, and it breaks anisotropic filtering

uniform sampler2D tex;

varying vec3 texcoord; // stq packed in stp

void main()

{

#if SMOOTHER

vec3 linear = gl_FragCoord.w * texcoord;

vec3 lx = dFdx(linear), ly = dFdy(linear);

vec2 proj = linear.st / linear.p;

vec2 px = (lx.st - lx.p * proj) / linear.p;

vec2 py = (ly.st - ly.p * proj) / linear.p;

#else

vec2 proj = texcoord.st / texcoord.p;

vec2 px = dFdx(proj), py = dFdy(proj);

#endif

#if VISUALIZE_LOD || MANUAL_LOD

vec2 size = textureSize2D(tex, 0);

vec2 px2 = size * px, py2 = size * py;

float lod = 0.5 * log2(max(dot(px2, px2), dot(py2, py2)));

#endif

#if VISUALIZE_LOD

gl_FragColor = vec4(vec3(fract(lod)), 1);

#elif MANUAL_LOD

gl_FragColor = texture2DLod(tex, proj, lod);

#else

gl_FragColor = texture2DGrad(tex, proj, px, py);

#endif

}

Hi Jonathan, you are right re: the derivative...I sort of hand-waved around the 2x2 case...in particular, where our samples are depend on the grid alignment of pixels to vertices. If our vertices lie on pixel sample centers, then our samples would actually be 0.0 and 1.0, but our derivative would still be 0.5...this happens when the cube is misaligned with the screen grid.

ReplyDeleteBen: I'm not sure I get what you mean. You mean if you shrink the square so it's still rasterized as 2x2 pixels, but is in fact almost 1x1? Then it's the 1x1 that counts for everything except pixel count, and it would be more accurate to call it that. It's all about the underlying idealized shape. But I probably misunderstood what you really meant.

ReplyDeleteI am just saying that a 2x2 pixel box can have a derivative of 1.0 without being sampled at 0.25 and 0.75 at the UV space. It could be sampled at about 0.0 and 0.5, for example, depending on the alignment of the box and the screen grid.

ReplyDeleteI only used the screen-aligned 0.25 and 0.75 as an example. You could have 0.0 and 0.5 or 0.4 and 0.9 or whatever. But the derivative will always be 0.5? Where's that derivative of 1.0 coming from?

ReplyDeleteSigh...typo..the above should read: deriv can be 0.5 even when the samples are not 0.25 and 0.75.

ReplyDeleteOh, okay, that clears it up then. Now go and finish v10! :-D

ReplyDeleteJust a note, the OpenGL pipeline newsletter from 2006 explained this derivative issue:

ReplyDeletehttp://www.opengl.org/pipeline/article/vol001_5/