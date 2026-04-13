---
title: Rim Highlight in Unity
url: https://lindenreidblog.com/2018/03/03/rim-highlight-in-unity/
author: View all posts by Linden Reid
published: '2018-03-03'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Hey y’all! Today, I have a quick tutorial on how to create the highlight effect featured in the gif above. I was inspired by artworks like this one by [Loish](https://loish.deviantart.com/art/The-Sketchbook-of-Loish-705300827) which have strong rim highlights.![highlightArt](../../assets/eb0adfa24bd68519.png)


If you’re familiar with [this tutorial on how to create a basic outline](https://lindenreid.wordpress.com/2017/12/19/cel-shader-with-outline-in-unity/), then this technique will be super easy! However, that’s certainly not required reading 🙂

For your reference, here’s the [link to the final code for the highlight shader](https://github.com/thelindseyreid/Unity-Shader-Tutorials/blob/master/Assets/Materials/Shaders/diffuseHighlights.shader). It also includes some [custom diffuse lighting from this tutorial](https://lindenreid.wordpress.com/2018/02/20/custom-diffuse-shader-in-unity/), but you really only need to look at the pass labeled “outline pass”!

On with the tutorial!


## Rim Highlight

Basically, what we’re going to do is add a second pass to our shader that **scales the model**, **draws only the back faces**, and **draws the outline color** (white) without any lighting or texturing applied. This will cause our scaled ‘outline’ mesh to appear behind our lit & textured mesh, and poke out between any areas where the mesh overlaps itself. Let’s look at exactly how to do that.

In addition to whatever regular lighting/texturing/coloring pass you have to draw your basic model, we’ll need to add a **second pass just to draw the outline. ***(If you’re familiar with the basic outline tutorial, note that you don’t need to do the stencil buffer stuff for this effect.)*

We also need to add the directive **Cull Front** to this pass. This means that our outline pass will **only draw the back faces of our model.**

We’re only going to return our tuned **highlight color** in the fragment shader, as we’re not going to apply any lighting or texturing to this highlight.

Here’s what the skeleton of what this pass looks like. Don’t forget to **add the properties to your Properties block** at the beginning of the shader!

Pass { // draw only back facesCull FrontCGPROGRAM #pragma vertex vert #pragma fragment frag // Properties (don't forget to add to Properties block!!!) uniform float4 _HighlightColor; uniform float _HighlightScale; // we'll need all of this information later! struct vertexInput { float4 vertex : POSITION; float3 normal : NORMAL; float3 texCoord : TEXCOORD0; float4 color : TEXCOORD1; }; // since we're just drawing a flat color, // we only need the vertex position in our vertex output. struct vertexOutput { float4 pos : SV_POSITION; }; vertexOutput vert(vertexInput input) { vertexOutput output;// this is where all of our code is going to go!!!!!output.pos = UnityObjectToClipPos(input.vertex); return output; } float4 frag(vertexOutput input) : COLOR {return _HighlightColor;} ENDCG }

**you won’t actually see your outline just yet.**This is because it’s drawing behind your lit model, and they’re the exact same size.

**vertex shader**, let’s

**scale the vertices along the normal direction**so that the scaling preserves the shape of the model.

vertexOutput output; // normal data is provided in float3, but need float4 form to do math // with the input vertex, which is a float4float4 newPos = input.vertex;float4 normal4 = float4(input.normal, 0.0);// scale the vertex along the normal directionnewPos += normal4 * _HighlightScale;output.pos = UnityObjectToClipPos(newPos); return output;

After tuning _HighlightScale, you should now see an outline of even thickness all around your model, like this:

![outlineeven](../../assets/8312cc7ac95be7d5.png)


In my opinion, this is already a pretty cool effect. You could leave it like this if you want to!

Now, to make this outline **reactive to the direction of the light source**, we want to make its thickness depend on the angle between the surface normal and the light source.

To do this, we first need to get the **normalized light direction** and **normal direction**.

We then get the **dot product of the light direction and normal direction**, which tells us about the angle between the two directions. The **smaller the angle** between the two- the more the normal is pointing towards the light- the **higher the value of lightDot**. We also call [saturate](http://developer.download.nvidia.com/cg/saturate.html) on this product to clamp the value between 0-1, as any values of the dot product below 0 should just be 0 anyway, as those values are facing away from the light.

Then, we **multiply our highlight scale by the dot product value.** This will scale our highlight thickness based on the angle between the light and normal direction!

vertexOutput output; float4 newPos = input.vertex; float4 normal4 = float4(input.normal, 0.0);float3 normal = normalize(mul(normal4, unity_WorldToObject).xyz);float3 lightDir = normalize(_WorldSpaceLightPos0.xyz);float lightDot =newPos += float4(input.normal, 0.0)[saturate](dot(normal, lightDir));* lightDot* _HighlightScale; output.pos = UnityObjectToClipPos(newPos); return output;

Ta-daaa! Your outline should now be scaling so that areas facing the light have a thicker outline, and areas facing away from the light are thin or have no outline at all. It should look something like this:

![outlineScaled](../../assets/cc589fcf0a6dde4a.png)


## Fin

Congrats, you finished the tutorial! I hope you got some inspiration about using highlight or outline passes in a shader. If you wanted to, you could change the color of this highlight, or maybe even base the color on the ambient or directional light source… :0

If you enjoyed this, be sure to check out one of my [many other outline (and other shader) tutorials](https://lindenreid.wordpress.com/all-tutorials/).

If y’all have any questions about writing shaders in Unity, I’m happy to share as much as I know. I’m not an expert, but I’m always willing to help other indie devs 🙂 And do give me feedback about the tutorials, I love hearing from y’all!

Good luck,

Lindsey Reid [@so_good_lin](https://twitter.com/so_good_lin)