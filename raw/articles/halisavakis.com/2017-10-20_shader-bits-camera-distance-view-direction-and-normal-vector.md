---
title: 'Shader bits: Camera distance, view direction and normal vectors'
url: https://halisavakis.com/shader-bits-camera-distance-view-direction-and-normal-vectors/
published: '2017-10-20'
source_blog: Technically Art – Harry Alisavakis
source_site: https://halisavakis.com
category: graphics
fetched: '2026-04-13'
---

Back again with some more bits of code for your shader needs! This time, we’ll see how to get the distance of the camera from our object, as well as the vectors that corresponds to the viewing direction and the model’s normals. Like before, this post will include the code bits for both vertex-fragment and surface shaders. Let’s get to it!

## Vertex-fragment shader

### Camera distance

The process of getting the object’s distance from the camera is pretty straightforward: we get the world position of the object and the world position of the camera and we get their distance using the built-in “distance” function. The way to get the object’s world space was covered in the [previous shader bits post](http://halisavakis.com/shader-bits-world-and-screen-space-position/), so I won’t go into that. In order to get the world position of the camera we can use one of Unity’s [built-in shader values](https://docs.unity3d.com/455/Documentation/Manual/SL-BuiltinValues.html), which is appropriately named “_WorldSpaceCameraPos”. Then, it’s sufficient to use this code in order to get the camera’s distance from the object:

fixed4 frag (v2f i) : SV_Target { // sample the texture fixed4 col = tex2D(_MainTex, i.uv); float camDist = distance(i.worldPos, _WorldSpaceCameraPos); // apply fog UNITY_APPLY_FOG(i.fogCoord, col); return col; }

As an example, I used this bit in the fragment shader, but it can be easily used in the same manner in the vertex shader as well.

### View direction

Getting the vector that represents the viewing direction also utilizes the object’s world position, as well one of Unity’s [built in shader functions](https://docs.unity3d.com/Manual/SL-BuiltinFunctions.html) called “UnityWorldSpaceViewDir”, which takes the object’s world space and calculates the view direction vector. Here’s a more complete code:

struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; float4 worldPos : TEXCOORD2; float3 viewDir : TEXCOORD3; };

v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); o.worldPos = mul(unity_ObjectToWorld, v.vertex); o.viewDir = normalize(UnityWorldSpaceViewDir(o.worldPos)); UNITY_TRANSFER_FOG(o,o.vertex); return o; }

The result of the function is normalized, since we just care for the direction and not the magnitude of the viewing direction.

### Normal vector

Getting the vertex normal in world space is also pretty simple, using another built-in function called “UnityObjectToWorldNormal” which can be used like so:

struct appdata { float4 vertex : POSITION; float2 uv : TEXCOORD0; float3 normal : NORMAL; };

struct v2f { float2 uv : TEXCOORD0; UNITY_FOG_COORDS(1) float4 vertex : SV_POSITION; float3 normal : NORMAL; };

v2f vert (appdata v) { v2f o; o.vertex = UnityObjectToClipPos(v.vertex); o.uv = TRANSFORM_TEX(v.uv, _MainTex); o.normal = UnityObjectToWorldNormal(v.normal); UNITY_TRANSFER_FOG(o,o.vertex); return o; }


## Surface shader

### Camera distance

The way to get the distance from the camera in the surface shader is exactly the same as in the vertex-fragment variant. Hence, it will look like this:

struct Input { float2 uv_MainTex; float3 worldPos; };

void surf (Input IN, inout SurfaceOutputStandard o) { // Albedo comes from a texture tinted by color fixed4 c = tex2D (_MainTex, IN.uv_MainTex) * _Color; o.Albedo = c.rgb; float camDist = distance(IN.worldPos, _WorldSpaceCameraPos); // Metallic and smoothness come from slider variables o.Metallic = _Metallic; o.Smoothness = _Glossiness; o.Alpha = c.a; }

### View direction

In the same manner as world and screen space position, the view direction vector is just one of the [built-in surface shader parameters](https://docs.unity3d.com/Manual/SL-SurfaceShaders.html), and the way to access it is respectively ridiculous:

struct Input { float2 uv_MainTex; float3 viewDir; };

### Normal vector

Here’s the thing with the normal vector in surface shaders: it’s already there. You don’t even have to add a keyword in the Input struct, there’s a field for the normal vector in every SurfaceOutput struct. Hence, if in your “surf” function you have an inout SurfaceOutput parameter named “o”, you can access the normal vector of the vertex just by saying “o.Normal”.

## Bonus bit

I included normal vectors and view directions together because they’re often used hand-in-hand. A common example of a case like that is rim lighting, which can be achieved using this bit (in either type of shader):

half rim = 1.0 - saturate(dot (normalize(VIEW_DIRECTION), NORMAL_VECTOR));

Where “VIEW_DIRECTION” matches the variable for your view direction, depending on the shader type. Same for “NORMAL_VECTOR”. A good exercise, by the way, is to try and wrap your head around *why *this is how a rim works. Having a solid understanding of the “dot” function will help you achieve pretty cool effects with the bits shown above.

That’s it for this post! See you in the [next one](http://halisavakis.com/shader-bits-camera-depth-texture/)!