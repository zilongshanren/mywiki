---
title: 'My take on shaders: Introduction to image effects'
url: https://halisavakis.com/my-take-on-shaders-introduction-to-image-effects/
published: '2017-04-12'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

So, I decided to also start this series where I demonstrate and explain a few things about shaders in the Unity game engine in order to keep a documented repository of things I make that I find cool, as well as to actively post more blog posts. At this point I should point out that I’m still struggling to learn more about shaders, hence I should not be considered as an expert or something. However, I hope that through these posts I can smooth the shader learning curve a little. At least I believe that these kind of posts would have been useful to me when I started.

This first post is an introduction to shaders and it will cover some of the basics of simple image effects. I chose image effects as I think they are simpler to understand, since they mostly manipulate color and don’t have to mess with vertex displacement, lighting and all that nonsense. For now I don’t want to really go in depth about what’s going on here, I just want to focus on the stuff that you can mess with to try different things.

So, let’s start by taking a look at what Unity makes when we create a new Shader > Image Effect:

Shader "Hidden/InvertColor" { Properties { _MainTex ("Texture", 2D) = "white" {} } SubShader { // No culling or depth Cull Off ZWrite Off ZTest Always Pass { CGPROGRAM #pragma vertex vert #pragma fragment frag #include "UnityCG.cginc" struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; }; struct v2f { float2 uv : TEXCOORD0; float4 vertex : SV_POSITION; }; v2f vert (appdata v) { v2f o; o.vertex = mul(UNITY_MATRIX_MVP, v.vertex); o.uv = v.uv; return o; } sampler2D _MainTex; fixed4 frag (v2f i) : SV_Target { fixed4 col = tex2D(_MainTex, i.uv); // just invert the colors col = 1 - col; return col; } ENDCG } } }

Lots of stuff going on in this simple shader, and it can be quite overwhelming if you’re not used to seeing this kind of code. But we will go through the important stuff of how it works together:

## Name of the shader

The first line is to declare the name of the shader as well as the folder in which the shader will be in order to attach it to a material. Now it’s in the folder “Hidden”, hence it won’t be visible in the shader menu. If we were to change that to “Custom/InvertColor”, we would find the option to attach this shader to a material in the “Custom” folder. Simple enough, moving on.

## Properties

The properties block holds all the properties that we see on the inspector when we’re editing a material. The syntax is as follows:

{Name_of_property_in_shader} (“{Name_of_property_in_editor}”, {Type_of_property}) = {Default_value}

So what that one line in the “Properties” block is saying is: create a property named _MainTex of type 2D (which means texture), label it “Texture” in the editor inspector and give it a default value of being a blank white texture. The “{}” after “white” are needed because a texture is supposed to be an array. You don’t have to worry about that. Also, you don’t have to worry about what texture you will use in the inspector. Since this is an image effect, the _MainTex field will be set automatically as what our camera sees.

## Filler code

The “Subshader” block is where the actual body of the shader lives. I won’t go in depth about what’s happening until line 40, but a “brief” explanation is this: Some properties are declared in line 10 that give some information about how the shader should behave. After that, in the “Pass” block, which marks the first (and in this case only) pass of the shader, there is the definition of two structs named “appdata” and “v2f”. The first one provides the vertex shader with the necessary information about the position of the vertices and the uv coordinates. The v2f struct (standing for vertex to fragment) is responsible for providing that information to the fragment shader so it can convert the vertices to fragments (basically pixels). After all of that that, the “vert” function that corresponds to the vertex shader is defined. In this case it doesn’t do anything special; it just passes the values from an appdata object to a v2f object which it returns.

## Properties declaration

Alright, now that all of that is out of the way, let’s move to the fun stuff! In line 40 you will see that a property of type “sampler2D” (that means 2D texture) named “_MainTexture” has been declared. “But **wait**! Haven’t we already declared a 2D texture named “_MainTex” in the “Properties” block???”. Yes, voice in my head, that is correct. The thing is, that the blob of text above is not precisely the script that tells your GPU what to do. It also needs to be integrated with the Unity editor so that we can modify the values of the shader via the inspector. Thus, if we want to use the properties we declared in the “Properties” block in our shader, we need to redeclare them with the same name and a matching type.

## Fragment shader

The last part (that we care about (a lot)) is the “frag” function, our fragment shader. Its job is to take the information from the vertex shader and turn it into color. Let’s take a closer look: a field of type “fixed4” named col is declared. This is basically a tuple with 4 values x,y,z,w stored. We can also find that type as a float4 or a half4. Besides optimization issues, their behavior should be the same whichever one we use. The result of “tex2D(_MainTex, i.uv)” is stored in that field. This function basically applies the texture to the given i.uv coordinates (here that’s our camera output) and returns the appropriate color. Since _MainTex is what our camera sees and i.uv is the screen coordinates, the “col” field at that point will have the color of what the camera sees, without any processing whatsoever. Also, the “cool” thing about that field is that the values it keeps are not something out of the ordinary. “Col” stands for “color”, and the four values it has stand for R, G, B and A! Which, hopefully, is something that makes sense in this whole jungle of craziness that is the shader code. This is why, in line 46 saying “col = 1 – col” inverts the colors. This is the only piece of code that actually does something to affect the image effect in this script. After that the function just returns the color and its job is done.

## Attaching the shader to your camera

Won’t babble on about this, I will just provide the script and mention how to use it. The script is as follows:

using UnityEngine; [ExecuteInEditMode] public class CustomImageEffect : MonoBehaviour { public Material material; void OnRenderImage(RenderTexture src, RenderTexture dest) { Graphics.Blit(src, dest, material); } }

You attach it to the camera, make a material that uses the image effect shader you created, drag and drop the material on the public field of the “Custom Image Effect” component and BOOM! Image effect attached. (It won’t actually create an explosion, I just wanted to sound dramatic.)

## Conclusion

This took longer than I thought. But I really hope that it can be useful to somebody. Hopefully there will be more posts/tutorials about shaders containing different kind of examples that will help you get more familiar with them. But, as always, the best way to learn about shaders is to get your hands dirty. Take my examples and every example you can find and test it, tweak it, try to figure out what makes it tick. For instance, make the default image effect shader shown above and try to make everything red or magenta, the noblest of colors. See what happens if you add or multiply colors with numbers or with other colors. And most important of all, have fun with them!

See you in the [next one](http://halisavakis.com/my-take-on-shaders-night-time-shader-introduction-to-image-effects-part-ii/)!