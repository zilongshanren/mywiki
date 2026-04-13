---
title: GPU Sorting - Alan Zucconi
url: https://www.alanzucconi.com/2017/12/13/gpu-sorting-2/
author: Alan Zucconi
published: '2017-12-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

![](../../assets/5cf52b1407cd74be.gif)

You can read the full series here:

- Part 1.
**GPU Sorting** - Part 2.
**GPU Sorting**

You can find a link to download the **Unity source code** at the end of this tutorial.

#### Introduction

In the previous part of this tutorial, we have discussed the limitations that we face when working in a parallel environment. Conceptually, the same shader code is executed on each pixel of a texture at the same time. While this is not necessarily what happens on a GPU, we cannot rely on the traditional assumptions that we take for granted on sequential machines.

The previous post introduced the **odd-even sort**, which is one of the simplest sorting algorithms that can be implemented on a GPU. It works by dividing the grouping the pixels on each line of a texture in groups of two. Each one is called a **swap couple**, and the shader swaps them if they are not already in order. The next step shifts the swap couples, and the process repeats. You can see this in the diagram below:

![](../../assets/ac1d55a5ee5d1c41.png)

As discussed before, the complexity of this algorithm is ![Rendered by QuickLaTeX.com \mathcal{O}\left(n\right)](../../assets/21591445bac158bc.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)


#### Shaders for Simulation

Shaders are usually used to process an input textures. Their result is visualised on the screen, leaving the original textures unaffected. What we want to do here is different, since we need the shader to keep iterating on the same texture. We have discussed how to do this extensive a previous series called [How to Use Shaders for Simulations](https://www.alanzucconi.com/?p=4539).

The idea behind this is to create two **render textures**, which are special textures amenable to shader manipulation. The diagram below shows how this process works.

![](../../assets/9e257b50b630e603.png)

The two render textures are cyclically swapped the shader pass can always use the previous one as the input and the other ones as the ouput.

This tutorial relies on the very implementation presented in [How to Use Shaders for Simulations](https://www.alanzucconi.com/?p=4539). If you have not read that tutorial yet, fear not. While we will focus on the sorting algorithm only, this is all you need to know:

float4 frag(vertOutput i) : COLOR { // X, Y coordinate of the pixel [0, _Pixels-1] float2 xy = (int2)(i.uv * _Pixels); float x = xy.x; float y = xy.y; // UV coordinate of the pixel [0,1] float2 uv = xy / _Pixels; // UV size of one pixel float s = 1.0 / _Pixels; ... }

The **fragment function** of the shader will contain the sorting code. The variable `uv`

indicates the UV coordinates of the current pixel being drawn, while `s`

represents the size of a pixel in UV space.

### ⭐ Recommended Unity Assets

#### Re-ordering the Swap Couple

In the previous part, we have introduced the concept **swap couple**. Pixels are grouped in couples, which are then sorted in a single shader pass. Let’s imagine having two nearby pixels, which colours ![Rendered by QuickLaTeX.com x](../../assets/53fb901d3b5ee71d.png)

![Rendered by QuickLaTeX.com y](../../assets/6cc181d8f36d0fd4.png)


![](../../assets/f202bc579b9b0748.png)

To do so, the pixel on the left side of the swap couple will sample the two pixels above, and pick ![Rendered by QuickLaTeX.com min\left(x,y\right)](../../assets/b1373e769cfb9807.png)


![](../../assets/2d0619b37bd7591d.png)

The position of the pixel does not only determine which operation to do. It also determines which pixels to sample. **Min pixels** need to sample the pixels at their current position and the one to their right. **Max pixels** need to sample the pixel on their left instead.

// Max operation float3 C = tex2D(_MainTex, uv).rgb; // Current pixel float3 L = tex2D(_MainTex, uv + fixed2(-s, 0)).rgb; // Left pixel result = max(L, C); // Min operation float3 C = tex2D(_MainTex, uv).rgb; // Current pixel float3 R = tex2D(_MainTex, uv + fixed2(+s, 0)).rgb; // Right result = max(C, R);

On top of that, the min and max pixels are swapped after each iteration. The diagram below shows which pixels perform a min operation (blue) and which one performs a max operation (red):

![](../../assets/b9332875d026c4c4.png)

The two determinant factors in deciding which operation to perform are the **iteration number** `_Iteration`

and the **element index** `x`

(or `y`

, if we are sorting columns instead of rows).

By looking at the diagram above, we can derive the final condition that determines whether we have to perform a min or max operation:

// Odd/Even Macros #define EVEN(x) (fmod((x),2)==0) #define ODD(x) (fmod((x),2)!=0) float3 C = tex2D(_MainTex, uv).rgb; // Centre if ( ( EVEN(_Iteration) && EVEN(x) ) || ( ODD (_Iteration) && ODD (x) ) ) { // Max operation float3 L = tex2D(_MainTex, uv + fixed2(-s, 0)).rgb; // Left result = max(L, C); } else { // Min operation float3 R = tex2D(_MainTex, uv + fixed2(+s, 0)).rgb; // Right result = min(C, R); }

That condition makes sure that during even iterations (the second, the fourth, …) pixels in an even position perform a max operation, and pixels in an odd position perform a min operation. On odd iterations (the first, the third, …) this is swapped.

For this effect to work, both render textures must be set to **Clamp**, as the shader code does not have any boundary conditions to prevent accessing pixels outside the texure.

#### Conclusion

You can find more sorting animations in this gallery:

You can read the full series here:

- Part 1.
**GPU Sorting** - Part 2.
**GPU Sorting**

#### Download

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can download all the assets necessary to reproduce a GPU sorting shader. There are two downloads available:

## Leave a Reply Cancel reply