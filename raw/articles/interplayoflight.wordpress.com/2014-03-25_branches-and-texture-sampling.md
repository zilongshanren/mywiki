---
title: Branches and texture sampling
url: https://interplayoflight.wordpress.com/2014/03/25/branches-and-texture-sampling/
author: Kostas Anagnostou
published: '2014-03-25'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

This is a quick one to share my recent experience with branching and texture sampling in a relatively heavy screen-space shader from our codebase. The (HLSL) shader loaded a texture and used a channel as a mask to early out to avoid the heavy computation and many texture reads that followed. Typically we’d use a discard to early out, but in that case the shader needed to output a meaningful value in all cases.

The shader worked fine, but we noticed that the mask did not seem to have an impact on the performance, i.e. the shader seemed to do work (inferred by the cost) even in areas where it shouldn’t. At first we couldn’t see why, but then it struck us when we viewed the produced shader assembly code.

The problem was this: the second branch of the if-statement was using (many) tex2D commands with **shader calculated **uv coordinates to perform the texture sampling, something like (greatly simplified of course):

sampler texSampler1; sampler texSampler2; float mix; float4 PS( PS_IN input ) : COLOR { float4 mask = tex2D(texSampler1, input.uv); if (mask.w > 0.5) { return float4(mask.rgb,1); } else { float2 uv = input.uv * 2; float3 colour = tex2D(texSampler2, uv).rgb; return float4( colour, 1); } }

To understand why this is a problem, consider that in order for texture sampling to work correctly it needs to know about the rate of change (or gradient) of a pixel neighbourhood. This information helps the texture sampler decide which mip to use. To calculate the gradient a minimum of a 2×2 pixel area (or quad) is needed. When we use branching in a pixel shader, each of the 2×2 area pixels can follow a different path, meaning that gradient calculation is undefined (since we are calculating the uv coordinates in the shader).

When the compiler comes across a tex2D with shader-generated uv coordinates in an if-branch I doesn’t know what to do with it so it can do one of the following: A) reorder tex2d calls to move them outside the if-statement if possible. B) flatten the if-statement by calculating both branches and choosing the final value with a compare. C) throw an error. I have seen both A and B happen in different shaders in our code base. The third option is mentioned in the [official D3D doc](http://msdn.microsoft.com/en-us/library/windows/desktop/ff471389%28v=vs.85%29.aspx) although it hasn’t happened in my case. Both A and B options do not have an impact on the result of the shader, they can affect performance severely though as in our case.

The following snippet, which is the assembly produced by the HLSL code above, demostrates this. In this case the compiler has chosen to flatten the branches, calculate both paths and choose what to return with a cmp.

def c0, 0.5, 1, 0, 0 dcl_texcoord v0.xy dcl_2d s0 dcl_2d s1 add r0.xy, v0, v0 texld r0, r0, s1 texld r1, v0, s0 add r0.w, -r1.w, c0.x cmp oC0.xyz, r0.w, r0, r1 mov oC0.w, c0.y

The solution to this problem is to either use [tex2Dlod,](http://msdn.microsoft.com/en-us/library/windows/desktop/bb509680%28v=vs.85%29.aspx) setting the mip level or keep tex2D and [provide the gradient information](http://msdn.microsoft.com/en-us/library/windows/desktop/ff471389%28v=vs.85%29.aspx) ourselves as tex2D(sampler, uv, dx, dy). This way the compiler does not come across any undefined behaviour.

The following code lets the compiler keep the if-branches as intended, by using a tex2Dlod:

sampler texSampler1; sampler texSampler2; float mix; float4 PS( PS_IN input ) : COLOR { float4 mask = tex2D(texSampler1, input.uv); if (mask.w > 0.5) { return float4(mask.rgb,1); } else { float4 uv = float4(input.uv * 2, 0 ,0); float3 colour = tex2Dlod(texSampler2, uv).rgb; return float4( colour, 1); } }

Something the produced assembly code confirms.

def c0, 0.5, 2, 0, 1 dcl_texcoord v0.xy dcl_2d s0 dcl_2d s1 texld r0, v0, s0 if_lt c0.x, r0.w mov oC0.xyz, r0 mov oC0.w, c0.w else mul r0, c0.yyzz, v0.xyxx texldl r0, r0, s1 mov oC0.xyz, r0 mov oC0.w, c0.w endif

A third option would be to calculate the uv coordinates (as many sets as we need/afford) in the vertex shader and pass them down to the pixel shader to use in the branch **unmodified**.

The above discussion is true for both branches and loops of course.

There is a lesson to be learned here as well, it is always worth inspecting the produced shader assembly to catch any inefficiencies such as those early instead of relying on the compiler to always do the right thing.




Ran into this myself a few months ago. I think if you specify an explicit branch using the [Branch] attribute, then D3D will throw a compilation error.

Indeed, thanks, one should always use the HLSL attributes (branch, loop, flatten, unroll etc) to declare their intention to the compiler and catch errors like these. The message of the post was more towards inspecting your low level code and don’t rely on the compiler. :-)

Thanks for the article. Saved me a lot of headache. I ran into the exact problem and [branch] generated an error: ” cannot have divergent gradient operations inside flow control”. Put that flag here so it’ll get picked up in a search

-Tom