---
title: Normal Mapping Without Precomputed Tangents
url: https://interplayoflight.wordpress.com/2013/01/21/normal-mapping-without-precomputed-tangents/
author: Kostas Anagnostou
published: '2013-01-21'
source_blog: Interplay of Light
source_site: https://interplayoflight.wordpress.com
category: game programming
fetched: '2026-04-13'
---

I came across a very interesting post on [performing normal mapping without a precalculated tangent frame](http://www.thetenthplanet.de/archives/1180). The technique is an extension/optimisation to the one presented by the same author in ShaderX5, and it elegantly and efficiently calculates the tangent frame in the pixel shader removing the need for storing tangent and bitangent vectors in each vertex.

Wanting to see how it performs visually, I fired up fx composer and did a quick test rendering a quad with a high resolution normal map once with regular normalmapping (precomputed tangent frame) and once using the above technique ( calculating the tangent frame in the pixel shader). Normalmap is courtesy of [Käy’s Blog](http://kay-vriend.blogspot.co.uk/).

Precomputed tangent frame:

Per pixel calculated tangent frame:

Apart from the fact that the second image looks a bit darker in overall the two images are very close, close enough to drop the precomputed tangent frame altogether.

This looks like a viable technique when memory bandwidth (and memory space) is of more concern than pixel shader cost (or when the mesh exporter manages to mess the tangent/bitangent vectors up).

I havent read through the article,

but what did you do in your implementation for the light and view vector which are needed for the lighting computation. You have to bring them into tangent space using the TBN matrix. Since this is obviously done in the pixel shader instead of the vertex shader there should be a huge overhead in performance.

Actually you use the TBN matrix typically to bring the tangent-space normal into world space (or wherever TBN is defined) to do the lighting and not the other way around. This is what happens in the above implementation as well. And read through the article, it is a good read. :-)

This is not the norm most of the normal mapping tutorials bring the Light and View vector into tangent space.

http://www.ozone3d.net/tutorials/bump_mapping.php

Isn’t your approach performance costly since you need to do a MAT3xVEC3 (TBN x NormalMap) for every pixel in the pixel shader……

Yes, if you are transforming the View and Light vector to tangent space in the vertex shader it is faster indeed (didn’t realise you were referring to the vertex shader). The above method though relies on dFdx/dFdy to calculate the T and B and this can’t be done in the vertex shader. BTW, it is not my method!

Mighty intering stuff you have here! Thanks for the shout-out :).

Cheers, Käy Vriend.

Hallo Kostas, the second image seems indeed to have more contrast. I would guess that this is due to a little bit of non-orthogonality of the texture mapping. I discovered the same when I originally tried out the technique in FX composer with the ‘teapot’ model. On spots where the uv mapping gets really distorted (near the spout) the normal map with precomputed tangents looses all contrast.

I’d suggest to try the same with a vertex wave animation, or procedural texture coordinate displacement with noise etc, and then post the difference in lighting again, you’ll be surprised!