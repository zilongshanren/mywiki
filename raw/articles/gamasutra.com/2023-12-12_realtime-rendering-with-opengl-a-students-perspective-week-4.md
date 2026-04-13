---
title: Realtime Rendering With OpenGL – A Students Perspective (Week 4)
url: https://www.gamedeveloper.com/art/realtime-rendering-with-opengl-a-students-perspective-week-4-
author: Josh Church
published: '2023-12-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

#### Week 4

Week 4 was spent on delving into lighting and because of that it was the first time I was really delving into the glsl code for this project. Previously I have done some coding in hlsl for Unity projects as well as some visual coding in Unreal and Unity’s shader graph, so the waters were not totally unfamiliar.

Multiplication lighting:

The simplest form of lighting is by multiplying the color obtained from reading your texture by a separate color. In the fragment shader you just need to set the frag color to the following:

FragColor = texture(“uniform for texture”, texCoord) * lightColor;

The following pictures show the before and after of this method for lighting. The background color is not actually influenced by the lighting, I just changed it for effect.

![](../../assets/f89b3f2a3ce01dea.png)


![](../../assets/98e3e13e48489eeb.png)


Diffuse lighting:

The next type of lighting was diffuse lighting. It would be added on top of the multiplication lighting we already had. The way diffuse lighting works is by taking the normal at a specific pixel as well as the direction of a light and taking the dot product. The light position can be passed in as a uniform as was mentioned during the Week 3 blog post about textures.

Once you get a value from taking the dot product of the normal and light direction you can multiply it after the light color.

FragColor = texture(“uniform for texture”, texCoord) * lightColor * diffuse;

The following images show the effect of diffuse lighting. Before the addition of diffuse lighting there was an extremely flat feel to the lighting. The whole magnet had the same intensity, with the addition of diffuse lighting there are parts covered in shadow and others that are more lit up.

![](../../assets/b5c13afa44147bc9.png)


![](../../assets/b1da5992a026c0b3.png)


In order to lighten up the darker parts of the magnet we need to add in ambient light. For this I just added a value of 0.2.

FragColor = texture(“uniform for texture”, texCoord) * lightColor * (diffuse + ambient);

Implementing specular lighting:

The lighting method that we have been implementing is called “Phong Shading” ([Phong shading - Wikipedia](https://en.wikipedia.org/wiki/Phong_shading)).

The last step in creating Phong Shading is to calculate the specular light. The calculation involves getting the view direction of the camera as well as the reflection direction of the lightsource. You then take those two and apply the dot product on them. Afterwards, put that value to a power so that the larger the angle between the view and reflection directions the weaker the specular light becomes. You then multiply the maximum specular light value, in this case 0.5. Then in the area where we added together the diffuse and ambient, add in the specular lighting.

![](../../assets/a731479eb43217cc.png)


The following gif shows the full implementation of Phong Shading.

![](../../assets/80f3397589bf7760.gif)


Overall it was pretty interesting to start coding more deeply in glsl and it really influenced where I wanted to go with the project. I was inspired to make Cell Shading and Gooch Shading work in my small engine, which is what I would be working on for the next two weeks.