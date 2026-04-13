---
title: 'Mini: Normal Maps'
url: https://mini.gmshaders.com/p/gm-shaders-mini-normal-maps
author: Xor
published: '2023-02-04'
source_blog: GM Shaders
source_site: https://mini.gmshaders.com
category: graphics
fetched: '2026-04-13'
---

# Mini: Normal Maps

### Introduction to normal mapping

Hi Shader Gang,

Last time, we went over how shading works in computer graphics. Read this if you missed it because it will be relevant today!

Today, we’ll cover a more common and powerful way of computing lighting.

## Introduction

Have you ever seen textures like these before?

These are normal maps. Many developers and gamers will have seen them before, but not so many know exactly what these represent.

Here are three properties worth covering:

**Normals are vectors perpendicular to the geometric surface**. You’ve made it this far, so you probably already know this.

You might now know that flat shading uses the same normal per face, but smooth shading computes the normal at each vertex using the average normals of all connected faces.

Here’s an illustration I found for representing face normals:**Normals are “normalized”**. This means they have a vector length of 1.0 exactly (also known as “unit vectors”). If, for some reason, they aren’t properly normalized, you can always use the handy[normalize](https://gmshaders.com/glossary/?load=normalize)function or just divide the vector by its length.**Normal maps are generally computed in “tangent space”**. I’ll leave the discussion of “spaces” for another day, but in short, this refers to orientation. The tangent is another vector, perpendicular to the normal and parallel to the geometric surface. These lines up with the horizontal axis of the texture mapping. And finally, there’s a third vector, called the bi-tangent, perpendicular to both, which represents the vertical axis along the texture. Here’s an illustration to help:

The blue vector is the normal, the red is the tangent, and the green is the bi-tangent. Thankfully, in 2D, you don’t need to deal with too much math.

So to summarize the three points, normals are vectors outward from the geometry, they should always have a length of 1.0, and are oriented with the regular textures.

Since we know that these vectors have a length of 1, then all the components must be between -1 and +1 (if any one component were greater than 1, the length would also be greater). Normal maps just store these x,y, and z components in the RGB channels of the texture. But since regular textures can only hold values between 0 and 1, the normals have to be remapped like so:

```
//To write normals to a texture we map them to the [0, 1] range:
vec3 normalRGB = normal * 0.5 + 0.5;
```


And to read a normal from a normal map:

```
//And to read the normal map, we can just renormalize it:
vec3 normalXYZ = normalize(normalRGB - 0.5);
```



That last line is the key to any normal map shader! Now let’s use it.

## Lambert Again

So you remember Lambert’s “cosine law”? It looks like this (theta is the angle between the normal and light direction).

`float light = max(cos(theta), 0.0);`



Well, it just so happens that the dot product of two normalized vectors is the cosine of the angle between them! So in other words, we can do the same computation without any trigonometry fanciness! Here’s what the looks like:

`float light = max(dot(normal, light_direction), 0.0);`



The light direction here must be a normalized vector! It could be a directional light or a point light as long as it has a vector length of 1.

## Transformations

We talked briefly about normal map texture orientation. I don’t want to get too deep into the math of tangent space now since we’ve already covered a lot, but I can give a quick 2D overview to get you guys started.

So here’s the problem we need to solve. If you rotate, stretch, or skew a texture, the computed normals don’t adapt to these changes. When we rotate our normal map, we don’t want the lighting to rotate with it:

So we have to apply the inverse rotation onto the normals, so up stays up!

The easiest solution is to just rotate in the opposite direction by the same amount:

```
//A classic 2D rotation matrix, but in the opposite direction (sines negated)
mat2 inverse_rotation = mat2(cos(angle), sin(angle), -sin(angle), cos(angle));
//Compute the corrected normals by rotating the about the z-axis
vec3 corrected_normal = normal;
corrected_normal.xy *= inverse_rotation;
```


For now, rotation is enough for most basic 2D lighting systems! If you want to go deeper into stretching, skewing, etc, [read this OpenGL tutorial](http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-13-normal-mapping/).

## Conclusion

From now on, you know what those mostly blue textures actually mean. You’ll also be able to identify slopes and which directions the slopes are facing by the RGB color values.

You can even write or read from normal maps using simple code, and you know another way that Lambert’s cosine law can be used in computer graphics.

And finally, you dipped your toes into the complicated world of tangent space and inverse transformations! Hopefully, this gets you thinking about how more complicated transformations and inverses as it’s an interesting topic.

Welp, that’s all I got for you today! If you found this useful, please consider sharing my newsletter and subscribing if you haven’t already.

Thanks for reading! Enjoy your weekend!