---
title: Conventions and nomenclature
url: https://apoorvaj.io/alpha-compositing-opengl-blending-and-premultiplied-alpha
published: '2019-06-15'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

Image compositing is the process of combining one or more images into
a single one. Compositing can be done in any number of ways, but a very
common way of doing it is to use the alpha channel for blending. Here,
alpha is loosely treated as
opacity. The
precise interpretation is more nuanced, as described in [ Interpreting
Alpha](http://jcgt.org/published/0004/02/03/paper-lowres.pdf) by Andrew Glassner.

This is the equivalent of the image produced when a layer is
composited on another layer with the “Normal” blend mode in Photoshop.
This technique was widely popularized by a seminal paper published in
1984. [ Compositing
Digital Images](https://keithp.com/~keithp/porterduff/p253-porter.pdf) by Thomas Porter and Tom Duff. This
compositing technique is so common these days that most people
conceptualize alpha as being transparency, instead of just a numeric
channel.

To simplify the discussion here, we’ll only talk about compositing
two images at a time. More images can be composited in exactly the same
way, one after the other. We’ll call the background image the
*destination*, since it is already present in the buffer we want
to composite on. We’ll call the foreground image the
*source*.

Each image has four channels: **R**ed,
**G**reen, **B**lue and
**A**lpha. (R_d, G_d, B_d,
A_d) are the destination image channels, (R_s, G_s, B_s, A_s) are the source image
channels, and (R, G, B, A) are the
resultant image channels.

For simplicity, we will assume that all channels lie in the range [0, 1].

If blending is not activated explicitly, OpenGL overwrites the destination with the source image by default. In order to enable and control blending, there are three main function calls:

[ glEnable(GL_BLEND)](http://docs.gl/gl2/glEnable)
activates blending.

[ glBlendEquation(mode)](http://docs.gl/gl2/glBlendEquation)
sets the blend mode. The blend mode dictates what is done with the
scaled source and destination values.

e.g. The most common blend mode, `GL_FUNC_ADD`

, evaluates
channels by addition. So R = R_s k_s + R_d
k_d. Green, Blue and Alpha channels are computed similarly.

`GL_FUNC_SUBTRACT`

, on the other hand, evaluates by
subtraction. So R = R_s k_s - R_d
k_d.

If you’re wondering what the k_s and kd variables are, that leads me to the third function.

[ glBlendFunc(k_s, k_d)](http://docs.gl/gl2/glBlendFunc): This function is used
to set the values of the scaling factors k_s and k_d
for source and destination respectively.


The following formula described in the Porter-Duff paper is used to get the final composited pixel colors:

\begin{aligned} A &= A_s + A_d (1 - A_s) \cr (R, G, B) &= \frac{(R_s, G_s, B_s) A_s + (R_d, G_d, B_d) \mathbf{A_d} (1 - A_s)}{A} \end{aligned}

Many times—for instance in a game frame—your background image is guaranteed to be fully opaque, meaning A_d=1. In this case, the formula becomes:

\begin{aligned} A &= A_s + (1 - A_s) = 1 \cr (R, G, B) &= (R_s, G_s, B_s) A_s + (R_d, G_d, B_d)(1 - A_s) \end{aligned}

In this case, you can set up OpenGL to do blending as follows:

With A_d \neq 1, the formula
seemingly breaks our OpenGL API. It needs *two* multiplications
instead of one: A_d and (1−A_s), and one final division by A.

How do we achieve this?

Pragmatic answer: If you can get away with it performance-wise, write a shader that samples two textures, and render to a third target texture with the composited result. The shader itself would look something like this:

uniform sampler2D tex_dst;
uniform sampler2D tex_src;
varying vec2 frag_uv;
void main() {
vec4 dst = texture2D(tex_dst, frag_uv);
vec4 src = texture2D(tex_src, frag_uv);
float final_alpha = src.a + dst.a * (1.0 - src.a);
gl_FragColor = vec4(
(src.rgb * src.a + dst.rgb * dst.a * (1.0 - src.a)) / final_alpha,
final_alpha
);
}


So, what’s the difference between a shader like this, and the OpenGL
blending API? The OpenGL blending API makes the computation happen on
specialized hardware located within the GPU sub-unit called the Render
Output Unit (ROP), [ Life
of a triangle - NVIDIA’s logical pipeline](https://developer.nvidia.com/content/life-triangle-nvidias-logical-pipeline) by Christoph Kubisch.
while our shader version executes on the shader execution
hardware (called a

Technically, executing on the ROP is faster because you are executing on specialized ROP hardware meant for blending (which ends up being used anyway, even in the shader case), and because you’re freeing up the shader cores to do other work.

Even the original Porter-Duff paper describes the “proper” optimization, i.e. premultiplied alpha. But the paper was written in a time where GPUs didn’t exist, and CPUs were slow.

Today, GPUs exist, CPU clock speeds are much higher, and we’re limited by memory access times more often than we are by computation. So, if you can get away with it, write a shader; it involves much less code than what I’m about to describe, and it probably runs fast enough.

Finally. Let’s see how to use hardware blending, even for non-opaque destinations.

Let’s look back to our initial formula, and move the denominator over to the left:

\begin{aligned} (R, G, B) &= \frac{(R_s, G_s, B_s) A_s + (R_d, G_d, B_d) A_d (1 - A_s)}{A} \cr \therefore \color{brown}{(R, G, B) A} &= \color{olive}{(R_s, G_s, B_s) A_s} + \color{magenta}{(R_d, G_d, B_d) A_d} (1 - A_s) \end{aligned}

When we load the source image, we
multiply its color channels by its alpha. We do the same when we load
the destination image. Now we can
use `GL_FUNC_ADD`

and
`glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)`

and get the
final image, but also in premultiplied
form.

We must reverse the premultiplication process by computing (\frac{R}{A}, \frac{G}{A}, \frac{B}{A}, A), if when want to use or save the composited result.

To recap premultiplied alpha, our pipeline now operates like this:

`glBlendEquation(GL_FUNC_ADD)`

, and
`glBlendFunc(GL_ONE, GL_ONE_MINUS_SRC_ALPHA)`

.Note that the simplest form of reversing premultiplication might
produce invalid color values when divided by zero alpha. This does not
matter if the resultant texture is sampled using point filtering, but it
is relevant otherwise. [ Alpha
Blending: To Pre or Not To Pre](https://developer.nvidia.com/content/alpha-blending-pre-or-not-pre) by John McDonald.