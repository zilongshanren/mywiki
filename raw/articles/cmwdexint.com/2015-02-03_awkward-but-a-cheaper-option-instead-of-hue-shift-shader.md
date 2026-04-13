---
title: Awkward, but a cheaper option instead of hue shift shader
url: https://cmwdexint.com/2015/02/03/awkward-but-a-cheaper-option-instead-of-hue-shift-shader/
author: Ming Wai Chan
published: '2015-02-03'
source_blog: Ming Wai Chan
source_site: https://cmwdexint.com
category: graphics
fetched: '2026-04-13'
---

![20150203_01](../../assets/dabf60564278378c.jpg)


“Color Tint” is an usual setting appeared in shaders, which normally doing the multiply effect to textures. Multiply makes everything darker, you cannot keep a part of texture to remain white, unless the shader lets you to have the alpha channel specifying which area would be affected.


If you want to have the Ctrl+U Hue/Saturation Setting in photoshop, you might look at [http://forum.unity3d.com/threads/problem-with-getting-hue-shift-shader-right.89041/](http://forum.unity3d.com/threads/problem-with-getting-hue-shift-shader-right.89041/)

All you have to do it to convert the current pixel RGB to HSV, shifting the Hue / Saturation / Brightness values with your input parameter, and then convert the HSV back to RGB for output. Notice that the shader might warn you and you have to add a line “#pragma target 3.0” which declares it is expensive!

**MY WAY OF HUE CHANGING:**

For the project I am currently working on in my company, I tried to use a stupid approach to achieve this.

fixed4 frag (v2f i) : SV_Target

{

fixed4 tex = tex2D(_MainTex, i.texcoord);

return fixed4(

tex.r-_Color.r*(2*tex.r-tex.g-tex.b),

tex.g-_Color.g*(2*tex.g-tex.r-tex.b),

tex.b-_Color.b*(2*tex.b-tex.r-tex.g),tex.a);

}

What I’ve done in the shader code is to calculate the delta value of R,G and B, and then use the delta value as a factor to control how the pixel is being affected by the input color. I.e., pixels with low saturation would be less affected, that’s why you see the white, grey and black area remains. The amount of calculation effort is greatly reduced.

This shader is used for creating different hair/eye color options in the project! xD

<-original texture (I remade it for this post)![20150203_05](../../assets/11704d0e424832fd.jpg)



The drawback is, you might not be able to tune the exact color you want, also, maybe this shader is still quite expensive. I don’t know, at least it looks good so far.

## One thought on “Awkward, but a cheaper option instead of hue shift shader”