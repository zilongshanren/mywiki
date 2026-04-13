---
title: 'My take on shaders: Butterflies and fish shader'
url: https://halisavakis.com/my-take-on-shaders-butterflies-and-fish-shader/
published: '2018-10-30'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

As it was the result of a [Twitter poll](https://twitter.com/HarryAlisavakis/status/1055464469457965057), I decided to share some more practical unlit shader effects. Specifically, you get two shaders (lucky you!), one for a simple butterfly flutter and another one for a simple fish swim cycle. These shaders are unlit and don’t react with light in any way, and their purpose is mostly for particle effects, were one could have as many butterflies and fish they want!

You can probably imagine that it’s just some masked vertex displacement, and you’d be right! The whole concept is to use sine waves for both the masking and the vertex displacement, to give a somewhat more organic look.

## Butterfly shader

Despite my lazy nature, I had to do a bit of setup for the butterfly effect. Specifically, I fired up Blender to create the following super-realistic model of an actual butterfly:

It’s just a quad with 2 cuts but it works ¯\_(ツ)_/¯. Do notice the UV layout of the “model” though; here it’s pretty much what you’d expect, but it’s actually convenient for us to have the non-moving part right down the middle of the quad. Keep in mind that, when reading the UV coordinates from the shader, the leftmost part of the layout will be at 0 and the rightmost part will be at 1. Anything in between will be inside the (0.0, 1.0) spectrum.

By the way, the butterfly texture was obtained from [textures.com](http://textures.com). Also, you have to take into account that Blender’s models are rotated -90 degrees on the x axis in relation to Unity. So do remember to rotate the plane so it points upwards, not like the way that dumbass (aka me) has it on the screenshot above.

Since we admired my über modeling skills already, let’s see some code:

Shader "Unlit/ButterflyShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _AlphaCutoff("Alpha cutoff", Range(0, 1)) = 0 _DisplacementAmount("Displacement Amount", float) = 1 _DisplacementSpeed("Displacement Speed", float ) = 1 } SubShader { Tags { "RenderType"="Opaque" } LOD 100 Cull off Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag // make fog work #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; }; sampler2D _MainTex; float4 _MainTex_ST; float _AlphaCutoff; float _DisplacementAmount; float _DisplacementSpeed; v2f vert (appdata v) { v2f o; o.uv = TRANSFORM_TEX(v.uv, _MainTex); float mask = 1 - sin(UNITY_PI * o.uv.x); v.vertex.y += sin(_Time.y * _DisplacementSpeed) * _DisplacementAmount * mask; o.vertex = UnityObjectToClipPos(v.vertex); UNITY_TRANSFER_FOG(o,o.vertex); return o; } fixed4 frag (v2f i) : SV_Target { // sample the texture fixed4 col = tex2D(_MainTex, i.uv); clip(col.a - _AlphaCutoff); // apply fog UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } } }

The effect, as you can see, is pretty straightforward. First of all, I add properties that control the alpha cutoff of the material (more on that later), and two fields that control the displacement amount and speed, i.e. how far will the wings be displaced and how fast they will flutter respectively. After that, a sneaky directive in line 14 makes the model render from both sides so that we can also look the butterflies from the back side (ᶦᶠ ʸᵒᵘ ᵃʳᵉ ᶦⁿᵗᵒ ᵗʰᵃᵗ ˢᵗᵘᶠᶠ ᴵ ᵍᵘᵉˢˢ) without the shader culling them.

I’ve waited so long to say this so here goes: THE MAGIC HAPPENS IN THE VERTEX SHADER THIS TIME. After the properties are redeclared in lines 41-43 the vertex displacement is being calculated. First of all, in line 49 I define a mask, based on which the displacement will occur. This mask wasn’t completely out of my imagination, one obvious way to check if a mask like that would work is to just return its value as is in the fragment shader (though obviously using i.uv instead of o.uv). This one specifically would give a result like this:

And it works really great in this case. If you want it to be “tighter” you can always use the “pow” function.

The “math” behind this mask are pretty simple too: UNITY_PI is, well, π as you know it. Remember how I mentioned that it was important that the non-moving part of the butterfly should be at the middle of the UV layout? It’s because of that mask. Since the UV coordinates go from 0.0 to 1.0, the middle would roughly be around 0.5, and sin(π * 0.5) = 1, while sin(0) = 0 and sin(π) = 0. Subtracting that from 1 gives us the above result. Aren’t sine waves fun? 😀

Line 50 is doing the displacement thing: basically it offsets the vertices of the model on the y axis using another sine wave (which as we know, goes from -1 to 1 perpetually) which moves based on the _Time.y parameter multiplied by the speed property. The offset is multiplied by the amount property and the mask so it’s mostly applied on the wings.

And that’s about it from the vertex shader! The only thing in the fragment shader that’s worth mentioning is line 60 where I use the _AlphaCutoff property to clip surrounding pixels so that I wouldn’t have to make the shader transparent. In some cases, alpha cutoff is more performant than transparency, though keep in mind that in some hardwares, alpha testing like this can actually be more expensive.

## Fish shader

The fish shader works in a similar fashion: it uses two basic vertex animations, one for translating the whole body and one for the wavy motion of the body. The inspiration for those movements came from the awesome [GDC talk by Matt Nava on the art of ABZU](https://www.youtube.com/watch?v=l9NX06mvp2E), though he also presented some more complex movements as well. Also, the fish model was not created by me, I just downloaded [this turbosquid model](https://www.turbosquid.com/3d-models/fish-max-free/621824). While I didn’t specially design the UVs of the model to suit my shader, seeing the texture gave me a pretty good idea of how the coordinates were laid out. Ideally, we’d want the leftmost part of the UV coordinates to be where the fin is, and the rightmost part to be where the head is, and based on the texture, this is pretty much the case. So that was basically a happy accident.

Let’s **dive **into the code (get it? cause it’s for fish):

Shader "Unlit/FishShader" { Properties { _MainTex ("Texture", 2D) = "white" {} _TranslationAmount("Translation amount", float) = 1 _DisplacementAmount("Displacement amount", float) = 1 _DisplacementSpeed("Displacement speed", float) = 1 _MaskOffset("Mask offset", Range(0, 1)) = 0 } SubShader { Tags { "RenderType"="Opaque" } LOD 100 Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag // make fog work #pragma multi_compile_fog #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; }; sampler2D _MainTex; float4 _MainTex_ST; float _MaskOffset; float _TranslationAmount; float _DisplacementAmount; float _DisplacementSpeed; v2f vert (appdata v) { v2f o; float mask = saturate(sin((v.uv.x + _MaskOffset) * UNITY_PI)); v.vertex.z += sin(_Time.y * _DisplacementSpeed) * _TranslationAmount; v.vertex.z += sin(v.uv.x * UNITY_PI + _Time.y * _DisplacementSpeed) * _DisplacementAmount * mask; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); UNITY_TRANSFER_FOG(o,o.vertex); return o; } fixed4 frag (v2f i) : SV_Target { // sample the texture fixed4 col = tex2D(_MainTex, i.uv); // apply fog UNITY_APPLY_FOG(i.fogCoord, col); return col; } ENDCG } } }

The properties in this one look awfully similar, though this time we don’t need an alpha cutoff value (but if the fish was just a texture on a subdivided quad we’d need it). We have, however a translation amount property, used for the left-to-right motion of the whole model. The displacement amount and speed are used for the wavy movement of the fish, while the mask offset is used to adjust which parts of the fish actually follow the wavy motion. It’s there to give us some additional control.

No “Cull off” directive is needed here, but again, if this was a quad with a texture, we’d probably want to add it. After redeclaring the properties, we move, once again in the vertex shader. In this case, our mask in line 49 is a bit different. First of all, I also add the mask offset property to the uv coordinate before multiplying the whole thing with UNITY_PI. This is so that I can exclude areas like the head from performing the wavy motion. This time I also clamp the result of the sin in the [0, 1] spectrum using “saturate”, because the offsetting can result in negative values. If I didn’t use “saturate”, the head would move in the opposite way instead of staying still.

Line 50 is responsible for the left-to-right movement of the whole body. It’s another simple sin wave that works in the exact same way as the butterfly wing displacement, though it offsets in the z axis instead of the y. On the other hand, line 51 takes care of the wavy motion by taking into account the model’s UV coordinates. That makes the whole model move in a wavy fashion, the displacement amount is then adjusted using the _DisplacementAmount property and restricted by the mask calculated above.

And that’s about it, really. The fragment shader is left completely unchanged.

## Additional info

- You may have wondered about me offsetting the models’ vertices in object space instead of clip space (v.vertex instead of o.vertex). It’s a conscious decision and I invite you to see what happens if you do the offsetting in clip space! 😀
- If you make a particle effect using these shaders you’ll notice something a bit annoying: that there’s no color variation of the butterflies/fish and that their movements are completely in sync. There’s a solution to both of these problems: vertex color! You can access the models’ vertex color like shown in
[this past tutorial](http://halisavakis.com/my-take-on-shaders-unlit-waterfall-part-2/)and use them to both add some variation on the output color and to use its length, for example, as an offset to the sine wave’s frequency. That would add some nice variation with barely any extra cost! 😀

Hope you enjoy these practical shaders and I’ll see you in the [next one](http://halisavakis.com/my-take-on-shaders-whats-the-deal-with-surface-shaders/)!