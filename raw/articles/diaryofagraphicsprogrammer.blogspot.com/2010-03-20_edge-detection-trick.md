---
title: Edge Detection Trick
url: http://diaryofagraphicsprogrammer.blogspot.com/2010/03/edge-detection-trick.html
author: Wolfgang Engel
published: '2010-03-20'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Benualdo posted in the Light Pre-Pass Thread a cool trick on how to detect edges to run a per-sample shader for MSAA (just in case centroid sampling doesn't work for you). Here it is:

----------

another stupid trick for edge detection pass on platforms that support sampling the MSAA surface with linear sampling: sample the normal buffer twice, once with POINT sampling and once with LINEAR sampling. Use clip(-abs(L-P)+eps). The linear sampled value should be used to compute the lighting of "non-MSAA" texels in the same shader to avoid an extra pass.

----------

eps is a small threshold value to bias the texkill test so that when the multisampled normals are only a little different then we could use the averaged value to perform the lighting at non-MSAA resolution during the first pass as an optimization.

## 14 comments:

For the epsilon bias optimization to work with previous trick the linear depth value should be also in the same texture (typically xyz= normal.xyz and w = linear depth) or we could fall into the 'almost same normal but very different Z' case. (I forgot it in previous post but on PC it is almost always the case anyway)







I have another funny edge detection trick I used one year ago for antialiasing on PS3. It was not for MSAA but for some kind of EDAA for forward renderer that needed edge detection te be done onto the final color buffer.

Bind a small (preferably swizzled and DXT1) volume texture with 0/255 into mipmap zero and 255/255 into other mipmap levels then use rgb values from the backbuffer as 3D texture coordinates. (both textures can be read with point filtering)

PS_OUTPUT PS_EdgeDetectVolumeTex(...)

{

half4 color1 = tex2D(backbuffer, uv.zw);

half4 color2 = tex2D(backbuffer, uv.xy);

half edge1 = tex3D(volumeTex, color1.rgb);

half edge2 = tex3D(volumeTex, color2.rgb);

return half4(color.rgb, -edge1-edge2);

}

and enable alpha test with alpha > 0 (it saves one TEXKILL shader instruction) so that if edge1 or edge2 is not 0/255 then the texel is discarded.

The trick for those who didn't get it has to do with how the hardware selects the mipmap level. In our case

the mipmap level will depend on "how fast" the rgb values are changing into a 2x2 texel quad. Is is done twice so that the result is accurate else it couls miss some edges between two texels into two different 2x2 texel quads.

And why you can't just use ddx/ddy on the color, instead of doing this mipmap trick?

I am still not sure how it can work....







The idea suggests to sample two points; one with linear and another with point. I guess the position of the linear sampling should be on the middle of a pixel to get the average value, while the point sampling should be at one of the sampling positions on the MSAA surface.

On 4xMSAA surface, there will be 4 sampling points. I wonder which one I should sample with the point sampler.

My best guess is that the assumption of the idea is to use 2xMSAA not 4xMSAA.

The calculation clip(-abs(L-P)+epsilon) doesn't detect edge but detect non-edge. It may need to be clip( abs(L-P)-epsilon ), instead.

Please also note that we cannot decide whether a pixel includes edge or not only with normal values. Even if normal values from each sampling point are exactly the same, it doesn't mean it is a non-edge pixel. We also need to check depth values.

Please let me know what I'm missing here.

I found the depth part was already mentioned.


Sorry. :-)

*PS: 8bits seems too less for the position reconstruction though.

I like to share my trivial experience that I had recently. I wish I can get any comments on this or hopefully I can fix it earlier if it has any faults.









For the case of 4xMSS, we need to sample 4 times anyway, in order to find edge pixels. If we have a separate buffer for depth, we need total 8 times of texture fetching. This edge detection is expensive.

Therefore, we need to split the edge detection step from each light rendering to separate one step.

Let's say previously we rendered normal and depth first and rendered each light on the screen, regardless multisampling.

We now need to render the normal and depth first, and then we need to update a stencil buffer to get the edge information on it, which may requires 8 times fetching as described.

With the stencil, we render two times per light: one for edge and another for non-edge. For the edge part we need to calculate light value per sampling point, which needs 4 times calculations and average of them. For non-edge part, we can use linear sampling on the middle of the pixel and do the light calculation only one time.

This way we don't need to do the expensive edge detecting per light.

My final decision for the edge detection is to use the centroid trick. Although it did not give me a perfect result on PS3, 2/3 of edges were correctly detected. It required only 1 time of texture fetching to update edge information on stencil buffer; otherwise it could be 8 times.

When I render normal buffer, I use one whole channel for edge information. If the centroid value differs from the non-centroid value, store 1; otherwise zero.

As the edge detection step, sample the resolved-MSSA normal value and if the edge channel is bigger than zero, update stencil; otherwise discard it in order not to update stencil.

This way requires stencil buffer. Thus, it may not be practical if depth information is packed on the normal buffer.

The texture coordinates are the same for both the POINT and the LINEAR samples. It is just the middle of the 2x1 or 2x2 samples, that is the texture coordinates you would get without MSAA. When POINT filtering is enabled but the texture coordinate is in the exact middle of four texels and the texture has no mipmaps, then the graphic card returns *ONE* of the 4 neightbours texels and we don't care witch one for the MSAA edge detection.




The volume texture mipmap trick is used instead of ddx/ddy just because it is faster to let the hardware do the job instead of adding more instructions to do it. (It's the same reason why we should use alpha test instead of clip() when possible). Compare generated microcode with NVShaderPerf and you will see the difference.

The sign of the clip test is negative because we want to clip when lower mipmap was choosen (because of texcoords moving fast) and then the value is 1. As hlsl clip(X) discards texels if any of the components of X is negative I think it's ok because if any of the tex3D returns 1 instead of 0 then (-edge1-edge2) will be negative.

rem: you can use signed tex to reduce the number of instruction in PS.

Jay I'm not sure to understand some details in the way you use stencil: are you updating the stencil only once with edge information and using geometry and depth test to select the pixels that need lighting for each light? Or do you sample the edge value from normal texture during lighting for each light? before each light?




If this is not what you're already doing, you can do this way:

- resolve multisampled buffers,

- write S=0x01 where edges were found

Then for each light:

- write S=2 where light is visible (ref=0x03 with write_mask= 0x02) using a geometry proxy of your light volume with depth test enabled

- run non-MSAA lighting shader and clip if multisampling is needed, stencil writes 0 with write mask = 0x02 (removes bit 2 from stencil and keeps bit 0x01 on edges)

- run MSAA lighting shader supersampling version where stencil == 3

- clear stencil bit 0x02 (write 0 with write_mask = 0x02) for the next lights if needed.

With (stencil == 0x03) being your stencil "early out" test and the Ref value (==3) never changing, both pass are optimized by stencil early out.

Benualdo, you got my point already. It is actually nothing new, because it is already well explained on ShaderX7.



I just applied it on light pre-pass.

BTW, randomly picking one point out of 4 would not give us a good result. It will cause 50% false-negative on actual edge pixels.

I want to correct my hastened comment. The value 50% was not proper. I was thinking about something else.


On my second thought, it may work well.

It is quit interesting idea. Now I see what I was missing.




:-)

I found that since the nature of normal keeps the length to be one, the averaged length is close to one when 4 normal values are very similar. If those normals point different directions the length must be decreased. Thus, "clip( abs(L-P)-epsilon )" seems to work fine.

However, depth values does not hold the characteristic. It is possible that the randomly picked point is close to the average although depth values actually vary. For example, 0, 5, 10, and 5 will yield average 5.

Can we improve this depth problem?

I may need more time to elaborate this idea, but let me try to put it here.









I think we can also use the characteristics of the normal on depth values, if we store the 1 dimensional depth value as 2 dimensional normalized value.

The calculation will be like this:

x = ( 1 - depth )

y = depth

Then we normalize it in order to make the length to be one: normalize( float2( x, y ) ).

For example, we have 4 depth values: 0, 1, 0.5, 0.5. The normalized values for each will be like this: ( 1, 0 ), ( 0, 1 ), ( 0.7, 0.7 ), and ( 0.7, 0.7 ).

The averaged value is now ( 0.6, 0.6 ) whose length is 0.85. The length decreased from one because they point different directions in 2 dimensional space.

To get all of these together, we need to store normal values on r and g channels and depth values on b and a channels.

Please let me know if this doesn't seem to work.

On second thought, we can also store normal and depth on separate buffers. In that way we don't need the point sampler.



bool bEdge

= clip( length( normalLinear.xyz ) - 0.8 )

&& clip( length( depthLinear.xy ) - 0.8 );

*PS: I'm sorry for many comments.

Today I found that 8 + 8 bits for depth checking is not detail enough...


For the normal checking, 2 channels are not enough to use the length trick; it has to be 3 channels...

Post a Comment