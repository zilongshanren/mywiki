---
title: Baked Soft Shadows in Unity 5
url: https://www.gamedeveloper.com/art/baked-soft-shadows-in-unity-5
author: Tino van der Kraan
published: '2015-11-20'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Baked Soft Shadows in Unity 5

This blog looks at soft shadows and how to create this in Unity 5 by utilizing lightmapping techniques.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

[As originally posted on[http://sassybot.com/blog/baked-soft-shadows-in-unity-5/]]

This blog shares some insights into soft shadows when baking lights in Unity 5. Light baking is a technique in the field of computer graphics where computationally expensive virtual lighting operations produce textures called lightmaps. Lightmap information baked into these textures are then used to display a virtual scene as if it was affected by real-time lights at a fraction of the cost compared to using real-time lighting. The combination of baked lights and real-time lights are often used to create a more believable virtual environment.

When observing how lights interact with objects in your environment it becomes apparent shadows are hardly ever perfectly straight. Light travels in a straight line, although it's highly unlikely that your light source is infinitely small as to produce perfectly straight shadows. In order to make your scenes look more believable it's worth considering what soft shadows can do for you if your software supports it. In this article I will demonstrate some comparison cases to better understand how baked soft shadows works and can be set up. Even though this tutorial focusses on Unity 5, the information here could be applicable to other software packages.

Let's talk about light falloff in Unity and how it can enhance the look of baked lighting in your scene. To illustrate the soft shadows in a photographic example I would like to show you this image taken from a [blog](http://spring2015wednesdayadvancedlighting.blogspot.nl/) on lighting in photography. The image shows nicely how the shadow gets softer as its extends further away from the object. Let's look at how we can achieve a similar result in Unity 5 .

## Creating a Test Environment

When trying out unfamiliar techniques or investigating a problem it helps to isolate the issue in an empty project or scene so as to not be worried about accidentally breaking the one which is already working or that external factors might interfere and obfuscate your results. To better understand the effects of soft shadows in Unity I have therefore created a comparison setup in a new project.

If you want to follow along and reproduce these results then follow the steps below.

1) In a new Unity 5 project, use the 3D template and change the Rendering Path to 'Deferred' and the Color Space to 'Linear'. You can do this in the editor by going to: Edit > Project Settings > Player

![RenderingSettings RenderingSettings](../../assets/27a223e677297df7.png)


2) Turn your scene completely dark by disabling the Ambient Intensity and the Skybox so that you have control over how lights affect your scene. This scene uses the following settings which you can find in the editor under: Window > Lighting

![TestLighting TestLighting](../../assets/8fe35ba30b7bde2f.png)


3) For the objects in the scene I have a ground plane which is a simple quad and an object (cube) where both are set to static which is required in order to be included in light baking. A camera is optional but if you have one, set the Background to display black. While on the topic of the camera, eventually you may notice banding in your bake results in the Game and Scene view as can be seen on the shadow side of the cube below, you can address this by setting the camera to HDR in its component settings.

![HDR_Settings HDR_Settings](http://zippy.gfycat.com/BronzeLikableHare.gif?width=1280&auto=webp&quality=80&disable=upscale)


4) Lastly, the scene contains a light source which in this case is a point light. Set the point light Baking setting to Baked and the Shadow Type to Soft Shadows. With these elements in place you should have a similar scene that you can use for testing.

## Point/Spot Lights - Baked Shadow Radius

To achieve light falloff on point lights and spot lights in Unity 5 you will need to set the Shadow Type of your light to Soft Shadows. Doing this will expose a variable called Baked Shadow Radius. Below you can see how this setting affects the results of a light bake.

Click the image above to enlarge it

The purpose of this setup is to show how you can control the soft shadows of a point light in Unity. The white sphere in this setup acts as a radius visualiser where its uniform scale corresponds to the value in the Baked Shadow Radius. This means that if the Baked Shadow Radius is set to 0.5 this is visualised by having the sphere use a uniform scale of 0.5.

## Directional Lights - Baked Shadow Angle

Directional lights are often used as the sun in virtual scenes. It's worthwhile looking at the characteristics of the sun before assuming that the directional light is simply the sun in your scene. While light travels in a straight line and knowing that the sun is incredibly far away, it's false to assume that this results in perfectly straight shadows as can be seen in this image below.

![Source: <a class= Source: <a class=](../../assets/9e895ada9bb13a2b.jpg)

[http://dcphotoartist.com/2015/08/25/looking-from-a-different-angle/](http://sassybot.com/wordpress/wp-content/uploads/2015/11/img_2481.jpg)

Directional lights use a Baked Shadow Angle variable to indicate how its soft shadow should look. Look at the example below to understand how this behaves at different settings.

Click the image above to enlarge it

## Area Lights

Area lights, which are baked only in Unity 5, naturally have soft shadows and only require you to aim and bake as is demonstrated below. Area lights are a great way to push more light into an interior scene when positioned over window frames.

![AreaLight2 AreaLight2](../../assets/6c359dbbd2ef4eb7.png)


With this I hope to have demonstrated how you can create soft shadows that could enhance the believability of your scene in Unity 5 when understanding and applying soft shadows. If you have found this information useful then I'd love to hear about it on Twitter [@Tinovdk](https://twitter.com/Tinovdk).

Have a great day. :)