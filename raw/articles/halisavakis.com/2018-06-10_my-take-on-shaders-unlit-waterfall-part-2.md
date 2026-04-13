---
title: 'My take on shaders: Unlit waterfall (Part 2)'
url: https://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-2/
published: '2018-06-10'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

As promised, this is the second part of the unlit waterfall effect tutorial. This one is focused on going through the effects that accompany the waterfall shader: the stylized foam particles and the water intersection shader. The effects on their own can be seen in this gif:

Both effects are pretty simple, but they both bring something interesting to the table without a lot of bells and whistles. The shaders are focused on doing that one effect, so they’re like the simplest version of what they offer. Without further ado, let’s start!![](../../assets/bfa7dfecb1ec5bc3.gif)


## Stylized foam particles

So, in this context those particles serve as the waterfall’s water foam as it crushes into the water. But, to be honest, this effect can be used in a bunch of stylized scenarios. Actually, my first use for this shader was as a smoke/dust trail effect. It was originally inspired by [this tweet](https://twitter.com/MaikelOrtega_/status/934010787487764480) from [Maikel Ortega](https://twitter.com/MaikelOrtega_) and it works with a rather simple concept:

- Have 2 passes, one that culls the back faces and one that culls the front faces
- Apply a different color for each pass
- Dissolve the object based on a dissolving guide (as shown in
[this old post](http://halisavakis.com/my-take-on-shaders-dissolve-shader/)) - Dissolve the object based on the alpha value of its vertex color

You can see that there’s not too much to it, but there’s an interesting point here: the vertex color one. In our shader we can easily have access to the object’s vertex colors, however we haven’t seen that a lot in previous posts (besides maybe some sprite shaders). The reason is, that while cool and useful, vertex colors are not terribly practical in all cases, as one would have to manually change the vertex color of their model inside the modeling software, through Unity plug-ins or via script. In most cases it’s worth it, but these tutorials are all about shaders, and vertex color manipulation is somewhat out of their jurisdiction. But there’s a cool little loophole here: the color modification in Unity’s particle system, actually modifies the particle’s vertex colors. And the reason for that is pretty neat and gives me an opportunity to talk about the advantages of vertex colors:

You see, in many cases, Unity can manage to optimize your graphics by batching together meshes that use the same exact material. You might have noticed that when you change a material property via script, the object’s material gets a “(instance)” next to its name. That’s because it gets separated from the batch Unity made based on the original material, and will need to render it separately. On the other hand, vertex colors are properties that are unique to the model and material-dependent. The material’s shader can take advantage of the vertex coloring as it reads it from the mesh’s information (in a similar way as it reads the vertices position or the UV coordinates). Therefore, if we have a direct way to change the object’s vertex color, we can use them to have multiple objects differently colored that are all batched together because they use the exact same material. On a side-note, you can get even more creative and not use the vertex color just as a color, but as a generic unique property of the object, to make interesting and well-performing shaders. I have an example for that, which you’ll probably see in a later tutorial, so stay tuned for that 😉

Based on all the above, you can now understand why the particle system uses vertex colors and how we can take advantage of that. On top of modifying the particles’ vertex color, the Shuriken particle system (bet you forgot that was actually its name) can animate the vertex color over time. Coming back to the effect at hand, if we match the dissolving amount to the “Color over lifetime” parameter and gradually fade the alpha channel of the particle’s color, we get the following effect:

Let’s see the code, finally:

Shader "Unlit/TwoSidedDissolve" { Properties { _DissolveGuide("Dissolve guide", 2D) = "white" {} _FrontColor("Front color", color) = (1,1,1,1) _BackColor("Back color", color) = (1,1,1,1) } SubShader { Tags { "RenderType"="Opaque" } LOD 100 Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag // make fog work #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float4 color : COLOR; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 color : COLOR; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; }; sampler2D _DissolveGuide; float4 _DissolveGuide_ST; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _DissolveGuide); o.color = v.color; UNITY_TRANSFER_FOG(o,o.vertex); return o; } fixed4 _FrontColor; fixed4 frag (v2f i) : SV_Target { clip(tex2D(_DissolveGuide, i.uv).x - i.color.a); fixed4 col = _FrontColor; UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } Pass { Cull front CGPROGRAM #pragma vertex vert #pragma fragment frag // make fog work #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float4 color : COLOR; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 color : COLOR; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; }; sampler2D _DissolveGuide; float4 _DissolveGuide_ST; v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _DissolveGuide); o.color = v.color; UNITY_TRANSFER_FOG(o,o.vertex); return o; } fixed4 _BackColor; fixed4 frag (v2f i) : SV_Target { clip(tex2D(_DissolveGuide, i.uv).x - i.color.a); fixed4 col = _BackColor; UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } } Fallback "VertexLit" }I believe this is the first multi-pass shader I demonstrate, so that’s also a new thing in this effect. That’s why it looks a bit long, but really, the second pass is basically the same as the first with a few really minor changes. So let’s see what’s going on here:

In the properties block, as per the “standard” dissolve effect, I add a grayscale texture to use as the guide for the dissolving. In this case I also use a cloud texture similar to the one in the

[dissolve tutorial], if not the same. I also declare 2 color properties, one for each side. Pretty straightforward stuff.Moving on to the first pass (lines 14-61). The code is a slightly modified unlit shader, so there’s all the stuff about fog etc, which I don’t have to go into. The modifications start at line 27, where I declare the “color” property with the “COLOR” directive in the “appdata” struct. This is how I’m telling the shader “hey, since you’re up there and getting the vertex information, why don’tcha fetch me that vertex color too?”, but with a more code-y syntax. Similarly, in the “v2f” struct I also add the same property in line 34 so that I can finally pass it to the fragment shader. Like in the

[previous post], after I declare my sampler for the dissolving guide in line 39, I also declare a float4 to hold the scale and offset information of the texture, in case I need to modify it.Inside the vertex shader, in line 46 I use the TRANSFORM_TEX macro to apply the texture transformation to the uv coordinates (don’t need a special name since I’m not using the UV coordinates for any other texture whatsoever). In line 47 I just pass the vertex color as is to the matching field in the v2f struct so I can use it in the fragment shader.

Finally, in the fragment shader, I use the clip function for the dissolving effect, as discussed in the previous posts, and just plainly return the “_FrontColor”.

As you can probably see, the second pass is basically exactly the same as the first one, but with 2 small differences:


- In line 64 I added the “Cull front” directive, so that this pass would only render the back faces of the model
- Instead of “_FrontColor”, I’m using the “_BackColor”

And that’s pretty much it as far as this effect is concerned.

## Water intersection

This water intersection effect is also one of the simplest implementations of its type. It has a simple premise: Compare the depth and the screen position of each pixel of the water surface, and if those are significantly different, then there is another object intersecting with the water surface and we can paint or manipulate the pixels in that intersection as we please. In this case, I modified the basis so that (a) the foam effect won’t fade out and (b) so that there is a bit of wavy displacement.

Let’s see how that looks in code:

Shader "Custom/WaterIntersection" { Properties { _Color("Main Color", Color) = (1, 1, 1, .5) _IntersectionColor("Intersection Color", Color) = (1, 1, 1, .5) _IntersectionThresholdMax("Intersection Threshold Max", float) = 1 _DisplGuide("Displacement guide", 2D) = "white" {} _DisplAmount("Displacement amount", float) = 0 } SubShader { Tags { "Queue" = "Transparent" "RenderType"="Transparent" } Pass { Blend SrcAlpha OneMinusSrcAlpha ZWrite Off CGPROGRAM #pragma vertex vert #pragma fragment frag #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; float2 displUV : TEXCOORD2; float4 scrPos : TEXCOORD3; }; sampler2D _CameraDepthTexture; float4 _Color; float4 _IntersectionColor; float _IntersectionThresholdMax; sampler2D _DisplGuide; float4 _DisplGuide_ST; v2f vert(appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.scrPos = ComputeScreenPos(o.vertex); o.displUV = TRANSFORM_TEX(v.uv, _DisplGuide); o.uv = v.uv; UNITY_TRANSFER_FOG(o,o.vertex); return o; } half _DisplAmount; half4 frag(v2f i) : SV_TARGET { float depth = LinearEyeDepth (tex2Dproj(_CameraDepthTexture, UNITY_PROJ_COORD(i.scrPos))); float2 displ = tex2D(_DisplGuide, i.displUV - _Time.y / 5).xy; displ = ((displ * 2) - 1) * _DisplAmount; float diff = (saturate(_IntersectionThresholdMax * (depth - i.scrPos.w) + displ)); fixed4 col = lerp(_IntersectionColor, _Color, step(0.5, diff)); UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } } FallBack "VertexLit" }So, for this effect the properties I mostly need are the main color and the one for the intersection areas, a threshold to use as a factor to modify the effect and a guide and factor for the displacement. This shader is using transparency, so I add the necessary tags and directives in lines 13, 17 and 18. Since I’ll be using the screen position of the object, in the “v2f” struct I add a field to hold those coordinates, as well as a separate field to hold the modified UV coordinates for the displacement texture. Since I’ll also be using the depth of the camera, in line 41 I declare the “_CameraDepthTexture”, to use as I’ve mentioned in

[the post about getting the camera’s depth].In the vertex shader there’s not too much happening, other than that I get the object’s screen position, as shown in

[this old post].Later, in the fragment shader, I get the object’s depth based on the camera and in lines 65-66 I calculate the displacement as per usual. The actual value that’s of any interest to us is the “diff” one, in line 68. Basically this will give me a value from 0 to 1 based on how big the difference between the pixel’s depth and the w component of it’s screen position is, when the displacement is also applied on it.

Finally, I calculate the final color based on whether the “diff” value is greater or lesser than 0.5 and return it. You can tell I didn’t get too much in depth for this effect, mostly because in most cases you can use it as it is, or maybe play around with it a bit to get different effects.

## Conclusion

Ok, this one I didn’t expect to turn out so large. Plus, I was distracted by the E3 livestream, so it took me a while to finish this post. Nevertheless, this is the end of this one. It has 2 simple enough but very useful effects to accompany the waterfall and to use in many other cases too. Hopefully those effects, or even just the way of thinking can prove to be useful to some of you!

See you in the

[next one]!

## Comments

I want to read this in depth, you had me at vertex colors to drive effects..because yes to everything .

You’ve gained a subscriber.