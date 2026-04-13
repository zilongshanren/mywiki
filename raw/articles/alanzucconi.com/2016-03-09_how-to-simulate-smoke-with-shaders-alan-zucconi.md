---
title: How to Simulate Smoke with Shaders - Alan Zucconi
url: https://www.alanzucconi.com/2016/03/09/simulate-smoke-with-shaders/
author: Alan Zucconi
published: '2016-03-09'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post will show how to simulate the diffusion of smoke using shaders. This part of the tutorial focuses on the Maths and the code necessary to recreate the smoke effect. To learn how to set up your project, check out the first part: [How to Use Shaders For Simulations](https://www.alanzucconi.com/2016/03/02/4539/).

![texture6](../../assets/3f63f45da503c812.gif)

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[The Maths](https://www.alanzucconi.com#part1) - Part 2.
[The Shader](https://www.alanzucconi.com#part2) - Part 3.
[Simulating Turbulences](https://www.alanzucconi.com#part3) [Conclusion & Downloads](https://www.alanzucconi.com#conclusion)

![smoke1](../../assets/e91becc5951a13fb.gif)

Creating realistic smoke in games has always been a challenge. The reason behind this is the fact that the large scale behaviour of smoke is determined by the complex interactions of billions of tiny particles, floating in air. Throughout the history of game development there have been many attempts to simulate smoke, mostly based either on particles or trails (animation below).Neither of these, however, are able to reproduce with fidelity the actual behaviours of a fluid when exposed to perturbations. To compensate for that, we need to simulate fluid dynamics. Like it happens with physics, you don’t actually need to simulate *every* aspects of fluid dynamics; you want something that looks good, but that is not too computational intensive.

### Part 1. The Maths

There are two main approaches to fluid dynamics: Lagrangian and Eulerian. While the former uses virtual particles to simulate the moving particles in a fluid, the latter divides the space into a grid. For this tutorial, we will focus on a simple grid-based smoke simulation. The value of each cell ![Rendered by QuickLaTeX.com x,y](../../assets/dabd93dc3af0815e.png)

![Rendered by QuickLaTeX.com F_{x,y}](../../assets/6dbd7a23be23756c.png)


Another assumption we introduce is that a cell can exchange flow only with its four immediate neighbours. This given a good approximation and reduces the number of texture lookups we need to perform for each pixel to five.

There are two components that determines how diffusion works. The first one is the incoming flow ![Rendered by QuickLaTeX.com F^{in}](../../assets/879c4515e101597d.png)


![Rendered by QuickLaTeX.com \[F^{in}_{x,y}=\frac{F^{out}_{x+1,y} +F^{out}_{x,y+1} +F^{out}_{x-1,y} +F^{out}_{x,y-1} }{4}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-8ad6525c7fe482b03f1deecb5e82a3f3_l3.png)


The outgoing flow of each cell is divided equally to its four neighbours, hence the ![Rendered by QuickLaTeX.com \frac{1}{4}](../../assets/f54c2c877abf9ead.png)


The second component is the the outgoing flow ![Rendered by QuickLaTeX.com F^{out}](../../assets/c4525e55fd0c5027.png)

![Rendered by QuickLaTeX.com f](../../assets/34bd71f58bee3f54.png)


![Rendered by QuickLaTeX.com \[F^{out}_{x,y}= f \cdot F_{x,y}\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-09edce21ecb29d70eef0d7f3bdefdb2f_l3.png)


To sum it up, the net balance of ![Rendered by QuickLaTeX.com F_{x,y}](../../assets/6dbd7a23be23756c.png)


![Rendered by QuickLaTeX.com \[F^{in+out}_{x,y}=f\cdot\left(\frac{F_{x+1,y} +F_{x,y+1} +F_{x-1,y} +F_{x,y-1} }{4} +F_{x,y} \right)\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-85334ca4687b8087849b77095a6919af_l3.png)


The post [How to Use Shaders for Simulations](https://www.alanzucconi.com/2016/02/28/4539/) shows how a fragment shader can be used to iterate over a texture. We will use the same technique, encoding the flow (or amount of smoke) into the alpha channel of the main texture `_MainTex`

. This allows to easily integrate a smoke effect into your game by simply overlaying a textured quad.

#### Grid representation

The first problem we encounter is the fact that we are using a grid-based approach, but this is a concept that is not present in a shader. Yes, images are indeed made out of pixels, but this is a concept that is not that easily accessible in a fragment shader. If we are using a standard Unity quad for this experiment, the pixels drawn by the shader are addressed by the quad UV. By knowing the size of the render texture we are using, we can use the value to find out which pixels we’re currently drawing. As a general approach, we will force the UV values of the fragment shader to assume values at fixed intervals, simulating a grid:

fixed2 uv = round(i.uv * _Pixels) / _Pixels; half s = 1 / _Pixels;

The variable `s`

indicates the distance between two cells. Now we can sample a texture like we can do with a grid:

// Neighbour cells float cl = tex2D(_MainTex, uv + fixed2(-s, 0)).a; // F[x-1, y ]: Centre Left float tc = tex2D(_MainTex, uv + fixed2( 0, -s)).a; // F[x, y-1]: Top Centre float cc = tex2D(_MainTex, uv + fixed2( 0, 0)).a; // F[x, y ]: Centre Centre float bc = tex2D(_MainTex, uv + fixed2( 0, +s)).a; // F[x, y+1]: Bottom Centre float cr = tex2D(_MainTex, uv + fixed2(+s, 0)).a; // F[x+1, y ]: Centre Right

If you prefer, you can use a more intuitive grid-like notation:

#define ARRAY(T,X,Y) (tex2D((T), uv + fixed2(s*(X), s*(Y)))) float cc = ARRAY(_MainTex, 0,0).a; // F[x+0, y+0]: Centre Centre

The last step is to implement the diffusion step:

float4 frag (v2f_img i) : COLOR { // Cell centre fixed2 uv = round(i.uv * _Pixels) / _Pixels; // Neighbour cells half s = 1 / _Pixels; float cl = tex2D(_MainTex, uv + fixed2(-s, 0)).a; // Centre Left float tc = tex2D(_MainTex, uv + fixed2(-0, -s)).a; // Top Centre float cc = tex2D(_MainTex, uv + fixed2(0, 0)).a; // Centre Centre float bc = tex2D(_MainTex, uv + fixed2(0, +s)).a; // Bottom Centre float cr = tex2D(_MainTex, uv + fixed2(+s, 0)).a; // Centre Right // Diffusion step float factor = _Dissipation * ( 0.25 * (cl + tc + bc + cr) - cc ); cc += factor; return float4(1, 1, 1, cc); }

Running this exact fragment shader, however, will not work as expected. Floating point arithmetic will collapse small numbers to zero, eventually stopping the smoke from flowing. To avoid this, [Omar Shehata](https://twitter.com/omar4ur) suggests in [How to Write a Smoke Shader](http://gamedevelopment.tutsplus.com/tutorials/how-to-write-a-smoke-shader--cms-25587) to enforce a minimum flowing quantity:

// Minimum flow if (factor >= -_Minimum && factor < 0.0) factor = -_Minimum; cc += factor;

![smoke2](../../assets/8db4678f71f6ced6.gif)

This provides a nice fluid dynamic which uniformly diffuses smoke in every direction, until it disspates.

### ⭐ Recommended Unity Assets

The formula derived causes smoke to diffuse uniformly and in all directions. If we want the smoke to move up, we need to promote transmission to the upper cell.

![texture6](../../assets/3f63f45da503c812.gif)

In general, we can add four coefficients for each cell (![Rendered by QuickLaTeX.com L_{x,y}](../../assets/cb84a12a3b846d14.png)

![Rendered by QuickLaTeX.com R_{x,y}](../../assets/758a800dce49c549.png)

![Rendered by QuickLaTeX.com D_{x,y}](../../assets/b98ac24b29e2fbec.png)

![Rendered by QuickLaTeX.com U_{x,y}](../../assets/a8ce07c8dda22bd4.png)


![Rendered by QuickLaTeX.com \[F^{in+out}_{x,y} =f \cdot \left[\begin{matrix}F_{x+1,y} L_{x+1,y} +F_{x,y+1} D_{x,y+1} +F_{x-1,y} R_{x-1,y} +F_{x,y-1} U_{x,y-1} +\\+F_{x,y}\left( L_{x,y}+R_{x,y}+D_{x,y}+U_{x,y} \right)\end{matrix}\right ]\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-2c1a8fb0cf5055911776343942107b44_l3.png)


When ![Rendered by QuickLaTeX.com L_{x,y}=R_{x,y}=D_{x,y}=U_{x,y}=\frac{1}{4}](../../assets/b118f94cb22e9353.png)

![Rendered by QuickLaTeX.com U_{x,y}](../../assets/a8ce07c8dda22bd4.png)


All the four coefficients can be baked into an additional texture, called `_VelocityTex`

, which accommodates ![Rendered by QuickLaTeX.com L_{x,y}](../../assets/cb84a12a3b846d14.png)

![Rendered by QuickLaTeX.com R_{x,y}](../../assets/758a800dce49c549.png)

![Rendered by QuickLaTeX.com D_{x,y}](../../assets/b98ac24b29e2fbec.png)

![Rendered by QuickLaTeX.com U_{x,y}](../../assets/a8ce07c8dda22bd4.png)


The technique shown in this tutorial is perfect to simulate diffusion phenomenon. Both smoke, water and temperature follows a similar pattern. The series Creeper World bases its gameplay entirely on a similar approach; a sentient blob is expanding, following exactly the diffusion algorithm explored in this tutorial.

What is really missing from this effect is the relationship between the float and the velocity. Our solution keeps these two entities separate, but in a real scenario this is not the case. The state of the art solution when it comes to fluid simulation is given by the [Navier-Stoke equations](https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations), which described fluid dynamics with incredible precision. Unfortunately, they are rather complicated and GPU intensive. For a primer on this technique, you can refer to [Fast Fluid Dynamics Simulation on the GPU](http://http.developer.nvidia.com/GPUGems/gpugems_ch38.html).

You can download the full Unity project of this tutorial [here](https://www.patreon.com/posts/13678744/).

**The next part of this tutorial ( How to Simulate Cellular Automata with Shaders) will iterate on grid-based technique to implement one of the most interesting cellular automata: Conway’s Game of Life. Cellular automata will be used in a later tutorial to simulate the flow of water.**

#### Other resources

- Part 1.
[How to Use Shaders for Simulations](https://www.alanzucconi.com/2016/03/02/4539/) - Part 2.
**How to Simulate Smoke with Shaders** - Part 3.
[How to Simulate Cellular Automata with Shaders](https://www.alanzucconi.com/?p=4643)

## Leave a Reply Cancel reply