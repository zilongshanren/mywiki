---
title: 'GM Shaders Guest: Gaming Engineer'
url: https://mini.gmshaders.com/p/gaming-engineer
author: Xor; Gaming Engineer
published: '2023-08-18'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Guest: Gaming Engineer

### Creating advanced 3D graphics in GameMaker with Noah Pauw

Hi all,

My name is Noah Pauw, also known as *GamingEngineer*, and I have been a game developer since 2007. I was given the opportunity by Xor to write an article about game development and shaders here for gmshaders.com, for which I am very grateful.

In this article, I would like to talk about making a 3D game in Game Maker with real-time lighting and [PBR materials](https://www.adobe.com/ie/products/substance3d/discover/pbr.html) using shaders and how I use Game Maker to create 3D environments. Many parts of this article will apply to other game engines as well, so stick around if you’re interested in 3D modeling and GLSL shaders.

Update: There

# Why Game Maker?

Game Maker wasn’t the first game engine I ever used, but it was the first I actually put more time into. I started using Game Maker in 2008 and released my first 3D game that same year. Ever since I’ve grown extremely fond of Game Maker’s workflow and decided to keep using it in the future.

Fast forward 15 years later and I still use it to create some 3D projects for my portfolio every now and then. Even though it takes more effort to create a 3D game as opposed to a 2D game in Game Maker, I still use it as it is the engine I am most comfortable with.

## Stop using Game Maker for 3D and switch to Unity or Unreal!!! >:(

I’ve received this comment a lot (usually without the angry face) but that actually isn’t bad advice per se. Game Maker is a fantastic engine and I truly do love using it. If you’re looking to make a lengthy photorealistic 3D game I personally think you would be better off using something else, but for a little tech demo to unleash your inner perfectionist for a few weeks, I would say go for it and have fun.

# 3D environments

I use Blender to create 3D environments, props, and weapons in my games. I have been using it for a few years now but I’m still probably only about 10% into all the possibilities that come with it. I use a custom exporter to export 3D meshes to vertex buffers, which I can then load into Game Maker using a custom importer. In Game Maker I then create an array of all parts of the environment I want to load in. These can all have different attributes, such as a diffuse texture, a normal map, a roughness map, a reflectivity amount, a default roughness value, and finally a cubemap-reflection intensity.

This array will consist of **structs** that will be used in the Draw Event to give each mesh a completely different look.

A struct I use in my project looks like this. These values will be used later when drawing each object in the Draw Event.

```
{
vertex_buffer,
diffuse_texture,
normal_texture,
roughness_texture,
roughness_value,
reflectivity,
transformation_matrix,
cubemap_strength,
is_decal,
is_vegetation
}
```


# Lighting shader

The lighting in my games is actually very simple. I wish I knew how to implement something like path-tracing, raytracing, light bounces et cetera in my games, but for now, the lighting in my games consists of simple point lamps placed at windows or holes in the geometry.

The shader takes in an array of lights. In the fragment shader, I loop through every light instance in the game and use the distance between each light source and the current vertex to light every mesh accordingly.

My method for this is as follows:

```
varying vec3 v_vVertexPosition;
varying vec3 v_vNormal;
varying vec4 v_vColour;
uniform vec4 lights[32];
uniform vec4 light_colors[32];
uniform int max_lights;
vec3 acc_lighting = vec3(0.0);
for(int i = 0; i < max_lights; i += 1) {
vec4 current_light = lights[i];
vec4 current_light_color = light_colors[i];
vec3 light_position = current_light.xyz;
float light_range = current_light.w;
vec3 to_light = normalize(v_vVertexPosition - light_position);
float distance_to_light = max(1.0 - distance(v_vVertexPosition, light_position) / light_range, 0.0);
float NdotL = max(dot(to_light, v_vNormal), 0.0);
acc_lighting += current_light_color.rgb * distance_to_light * NdotL;
}
vec4 main_color = v_vColour * texture2D(gm_BaseTexture, v_vTexcoord);
main_color.rgb *= acc_lighting;
gl_FragColor = main_color;
```


This is a simple per-pixel lighting shader that supports multiple light sources.

This however is only part of the shader I use to make lighting in my games a bit more realistic. Light will bounce around in confined spaces and should light up parts of a mesh that are out of view. Pathtracing and raytracing accommodate this by having rays bounce off surfaces to light a scene in a realistic manner. In the example below, you can see that even though the ball on the right is completely obscured by the wall in the middle, it does receive some of the light emitted by the light source on the left side of the wall. This happens because the light rays emitted from the light source will bounce around the room, which has a chance of hitting the sphere on the right.

Since I don’t know exactly how to achieve this without raytracing (which I also haven’t used yet 😶) I used a simple yet in my opinion pretty effective method that achieves a similar look. Usually what you would do is add some ambient light to your mesh in your fragment shader to simulate this effect.

```
vec3 ambient_light = vec3(0.31, 0.36, 0.37);
main_color.rgb *= acc_lighting + ambient_light;
```


This method simply adds a light blue color to the final lighting calculation, making sure the unlit part of the mesh won’t be completely black.

However, that is not exactly the method I use in my shader. What I do is I take the lighting color of the current light source and add that to the accumulated light color, only a lot more subtle. If we take a look at the bounce lighting example from earlier, you will notice that the bounce lighting is a lot less powerful than the light rays that didn’t bounce before hitting the mesh. The way I do this is by checking the light color again, only this time, I am not using the NdotL calculation* to calculate the difference between the mesh’s normal vector and the vector towards the light source. Instead, I will be using a “softer” calculation that takes some extra light into account when close to the mesh, if that makes any sense.

*) NdotL is a common method of calculating the difference between a light vector and a normal vector. The N stands for the current vertex’s normal vector, dot for the dot product function and the L for the vector towards the current light source.

`NdotL_bounce = 0.35 + (dot(to_light, v_vNormal) / 2.0 + 0.5) * 0.65;`


This way, the difference between the two vectors won’t be a value between 0 and 1, but rather a value between 0.35 and 1. Of course, these are so-called *magic numbers* but that is the value I think looked best at this time. Normal vectors that are facing away from the light source will be slightly affected by the bounce lighting now. Of course, this isn’t physically accurate at all, as the lighting conditions inside a large empty room would be more similar to the image on the right while lighting inside a more confined space would be a bit more like the image on the left.

The result would be something like this. The screenshot on the right is a lot darker than the screenshot on the left. Even if it isn’t completely accurate to real-life lighting calculations, I do like the result as everything is a bit easier to see while simultaneously looking a bit more natural.

# PBR materials

An important part of making 3D objects look more realistic is the use of PBR materials or Physics-Based Rendering materials. These materials usually consist of an albedo/diffuse texture, a normal map, and a roughness map. There are other maps such as a specular, metallic, and ambient occlusion texture, but these were not used in the current project, so they won’t be covered here.

The implementation of a PBR shader in Game Maker is the same as in any other engine. The only difference being you have to set everything up yourself. Now that we have our lighting shader, it is time to add some extra detail to our 3D scenes in Game Maker.

Since I don’t want this tutorial to be about the different types of textures used in PBR shaders and what they are for, I will keep this section very brief. A normal map is used to add more detail to a mesh without the cost of having extra geometry. A roughness map is used to determine the literal “roughness” of the surface of each part of a mesh. This will affect the amount of light the mesh will reflect.

Earlier I said I exported my 3D models in Blender using a custom exporter. Luckily, this exporter gives you access to various attributes you can include when exporting your mesh. These include the object’s 3D position, normal data, color data, texture coordinates et cetera. It is possible to export the models’ tangents as well. This is very important as we will need these to use normal maps later.

Do note that adding more and more attributes to your mesh can increase the file size significantly, thus increasing the amount of required memory in-game. For example, adding the tangents to a mesh will add 3 additional float values to your vertex buffer for each vertex, yielding a (much) larger file size (if your mesh is complicated).

The blue-ish normal map from earlier must be converted from RGB to XYZ values in the fragment shader. Luckily, this isn’t too hard to do. In the vertex shader, we need to perform some calculations to create a normal matrix we can later multiply with our normal map to convert these colors of the normal map into 3D vector data.

** Vertex shader**

```
attribute vec3 in_Position;
attribute vec3 in_Normal;
attribute vec4 in_Colour;
attribute vec2 in_TextureCoord;
attribute vec3 in_Tangents;
varying vec2 v_vTexcoord;
varying vec3 v_vVertexPosition;
varying vec3 v_vNormal;
varying vec4 v_vColour;
varying vec3 v_vTangent;
varying mat3 v_vNMatrix;
void main() {
vec4 object_space_pos = vec4( in_Position.x, in_Position.y, in_Position.z, 1.0);
gl_Position = gm_Matrices[MATRIX_WORLD_VIEW_PROJECTION] * object_space_pos;
v_vVertexPosition = (gm_Matrices[MATRIX_WORLD] * object_space_pos).xyz;
v_vNormal = (gm_Matrices[MATRIX_WORLD] * vec4(in_Normal, 0.0)).xyz;
v_vTangent = (gm_Matrices[MATRIX_WORLD] * vec4(in_Tangents, 0.0)).xyz;
vec3 N = normalize(v_vNormal);
vec3 T = normalize(v_vTangent);
vec3 crossNT = cross(N, T);
v_vNMatrix = mat3(T, crossNT, N);
v_vColour = in_Colour;
v_vTexcoord = in_TextureCoord;
}
```


Using varyings we can transfer these calculations from the vertex shader over to the fragment shader. There we can use a sampler2D uniform to get the normal map’s RGB values. We can then use the matrix we calculated in the vertex shader to convert these RGB values into vector data.

```
uniform sampler2D normal_map;
varying vec2 v_vTexcoord;
varying vec3 v_vVertexPosition;
varying vec3 v_vNormal;
varying vec4 v_vColour;
varying vec3 v_vTangent;
varying mat3 v_vNMatrix;
void main() {
vec3 N = normalize(v_vNormal);
vec3 normal_texture = normalize(texture2D(normal_map, v_vTexcoord).rgb * 2.0 - 1.0);
vec3 normal_transformed = normalize(v_vNMatrix * normal_texture);
}
```


So before we were using the mesh’s normal information to calculate the difference between the normal vector and the light direction. We can now use a combination of the normal vector and the normal map to create a much more detailed image of our mesh in Game Maker.

All we have to do is add the normal map as a sprite in Game Maker to our shader. The way you communicate with a shader from any program is through **uniforms**. This goes for Game Maker as well. Passing a texture to a shader in Game Maker is done using the **texture_set_stage** function. For this, you also need the sampler index of the shader’s uniform. You can get this by using the adequately named **shader_get_sampler_index** function.

```
var sampler_index = shader_get_sampler_index(shd_pbr, “normal_map”);
texture_set_stage(sampler_index, sprite_get_texture(tex_normal_map, 0));
```


The last thing to do is to change all **v_vNormal** or **N** (which is the normalized version of v_vNormal) to the newly created **normal_transformed** vector.

```
// float NdotL = max(dot(to_light, v_vNormal), 0.0);
float NdotL = max(dot(to_light, normal_transformed), 0.0);
```


The difference can be seen in the image below. I made it a little more noticeable using a simple flashlight shader I made.

## Making objects look shiny with the roughness map and reflectivity uniform

Each object has its own amount of reflectivity. This can be easily adjusted in GML. The PBR shader I use in my project uses a default roughness value in combination with a roughness map, to create simple imperfections that can make a night and day difference when it comes to realism.

Specular highlights are a great way of showing off just how reflective an object is. The smoother a surface, the less the light will scatter when hitting the surface, meaning more light has a chance of hitting the camera lens consistently, resulting in a clearer reflection. The roughness texture is a grayscale map so we will only need one of the color channels to use it. For this reason, we can use a **float** instead of a **vec3**. The lighter each pixel of the roughness texture, the smoother the surface.

The way my game calculates this while also taking the roughness map into account is as follows:

```
float roughness_map_value = texture2D(roughness_texture, v_vTexcoord).r; // Only use the “r” channel as we are using a grayscale image
vec3 to_camera = normalize(v_vVertexPosition - camera_position);
vec3 reflected_vector = reflect(-to_light, normal_transformed);
float highlight_value = max(dot(reflected_vector, -to_camera));
main_color.rgb += pow(highlight_value, max(roughness * roughness_map_value), 1.0);
```


While the shader does use the term “roughness” it should actually be “smoothness” as it does the opposite of roughness. See the image below for the difference between high and low roughness. Notice the sharper and brighter specular highlight on the weapon as opposed to the more subtle and larger highlight in the other image. The sharper and more intense the specular highlight, the smoother a surface looks.

# Drawing all this in Game Maker

All drawing-related things in Game Maker should be put in the Draw Event. Everything not related to drawing e.g. complex calculations and gameplay should be done in other events such as the Create or Step Event.

At the beginning of this article, I created an array of structs, each with its own vertex buffer, diffuse texture, normal texture et cetera. In the Draw Event, I will loop through all these structs and draw them individually. This way I can create the entire world map in Game Maker with different textures, roughness values, reflectivity, and more.

```
shader_set(shd_pbr);
shader_set_uniform_f(u_pbr_camera_position, x, y, z);
shader_set_uniform_f(u_pbr_lights, lights);
shader_set_uniform_f(u_pbr_light_colors, light_colors);
shader_set_uniform_f(u_pbr_max_lights, max_lights);
for(var i = 0; i < array_length(vertex_buffers); i++) {
var vb = vertex_buffers[i];
matrix_set(matrix_world, vb.transformation_matrix);
shader_set_uniform_f(u_pbr_cubemap_strength, vb.cubemap_strength);
shader_set_uniform_f(u_pbr_reflectivity, vb.reflectivity);
texture_set_stage(u_pbr_normal_map, vb.normal_texture);
texture_set_stage(u_pbr_roughness_map, vb.roughness_texture);
vertex_submit(vb.vertex_buffer, pr_trianglelist, vb.diffuse_texture);
}
matrix_set(matrix_world, matrix_build_identity());
```


# Conclusion

In short, this is the way I draw 3D environments in Game Maker Studio 2. This works in Game Maker Studio 1.4 as well, with some minor adjustments here and there. Is this the most optimized way of drawing stuff in Game Maker? I’m not so sure. Game Maker is no Unreal Engine 5 when it comes to making stunning things in 3D, so important optimization methods such as frustum and occlusion culling are unfortunately missing by default. Game Maker is an amazing 2D engine; some really impressive 2D games were made using Game Maker and at this point, I think you know which ones they are. If it weren’t for games such as CrimeLife 2 by Sakis25 and Backscatter by BanthyStudios, I would have probably given up making 3D games in Game Maker by 2009 or 2010. But here we are! 15 years later and still doing the same thing over and over again, expecting things to change.

I use this method in all my 3D games in Game Maker. There are other and better ways of rendering your objects in Game Maker, but hopefully, you found this one interesting. May it spark your curiosity about building a 3D game in an engine specifically designed for 2D games, because trust me, that is half the fun. This method is also present in a game I’ve been working on for a while now named **4406** (working title). You can find it on [GameJolt](https://gamejolt.com/games/4406/757959) if you’re interested! I also have a [YouTube channel](https://youtube.com/@GamingEngineer) where I “regularly” show some of the Game Maker projects I’ve been working on along with some extra information on how it was made.

Best wishes,

Noah