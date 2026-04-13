---
title: GladiArt or Process
url: https://www.gamedeveloper.com/art/gladiart-or-process
author: Vegard Myklebust
published: '2014-12-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# GladiArt or Process

This week's blog-post is a short summary of the art process used in creating the armour sets in Ludus.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This week's blog-post is a short summary of the art process used in creating the armour sets in Ludus and was written by our modeler Robert. As always you can keep up to date with Ludus development at [gladiator.training](http://www.gladiator.training)

Beginning with some research into Roman style art and props, I took a trip to the British Museum. I was looking mainly at Roman relics and weapons/armour that were on display to get into the mood of that era.

![helm helm](http://www.gladiator.training/wp-content/uploads/2014/12/helm.jpg?width=1280&auto=webp&quality=80&disable=upscale)



To help aid with the visual background, Vegard had gone to a one day event organised by [Britannia Gladiators](http://www.durolitum.co.uk/gladhome.html) and had taken many photos of the re-enactments of gladiator combat along with reference images for the armour. These got the ball rolling and I began to design some of the shields based on the photos.

![Vegard1 Vegard1](http://www.gladiator.training/wp-content/uploads/2014/12/Vegard1.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The re-enactment team done an amazing job of re-creating designs of the era, so we piggy-backed on their hard work and based a lot of our designs on their physical armor sets. Here are a few of the 3d models for the shields created and textured based on those reference images.

![shields shields](http://www.gladiator.training/wp-content/uploads/2014/12/shields.jpg?width=1280&auto=webp&quality=80&disable=upscale)



The modelling process for the Gladiators started with high poly geometry done along with some digital sculpting in preparation for extracting a low-poly or game friendly version.

![roughLion roughLion](http://www.gladiator.training/wp-content/uploads/2014/12/roughLion.jpg?width=1280&auto=webp&quality=80&disable=upscale)


I worked by sculpting directly onto the basemesh and extracting the various parts for texturing on a per-part basis, which enabled more control of the final UV area of the complete armour set.

Part of the workflow was to divide the UV area into 4 areas that would enable the meshes to be recombined in the game at runtime to reduce draw calls.

![CharactersUVLayout CharactersUVLayout](http://www.gladiator.training/wp-content/uploads/2014/12/CharactersUVLayout-1024x1024.jpg?width=1280&auto=webp&quality=80&disable=upscale)


After each part was sculpted and retopologised, they were given quick UVs to get started with the painting and texture generation. Here is an example of one of the arm padding unwraps that would later have its UVs moved and rebaked into the correct UV area.

![normMapArmPadding normMapArmPadding](http://www.gladiator.training/wp-content/uploads/2014/12/normMapArmPadding.jpg?width=1280&auto=webp&quality=80&disable=upscale)


As you can see the same normal map could then be rebaked to a new location by cloning the original mesh and moving its UVs. I used 3d Coat's texture baking tool for the rebaking, assigning the original mesh to the scene with the original normal map and assigning the target mesh (the one with the new UVs). This process would prove useful if ever we had to alter the UV layout in the future for any particular reason.

![reUV_norm reUV_norm](http://www.gladiator.training/wp-content/uploads/2014/12/reUV_norm.jpg?width=1280&auto=webp&quality=80&disable=upscale)


So the Process was as follows: Sculpt the Highpoly mesh, create the Lowpoly geometry from the high poly and bake out a normal map using Xnormal, from here I took the low poly mesh and the normal map into Substance Designer/Knald to extract more useful texture maps such as AO, Cavity and Curvature maps.

In Ludus we are using Physically Based Rendering which requires us to create Diffuse, Specular Colour Maps and Roughness Maps. We chose the Specular and Roughness map approach over the Metalness/Roughness workflow, as we found it more straight forward and easy to read visually in Photoshop. We are using the[ Lux shaders](http://forum.unity3d.com/threads/lux-an-open-source-physically-based-shading-framework.221985/) for Unity that support this visual approach well.

Now that I have 2k textures for each part, I can go ahead and texture each part using [Quixel suite](http://quixel.se/):

![maps maps](http://www.gladiator.training/wp-content/uploads/2014/12/maps.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Quixel suite allows for full control of edge wear, dirt trapped in occluded areas and most importantly the mega scan based materials.

I also created a few custom materials based on photos of various cloths and metals to aid in the process.

![customMats customMats](http://www.gladiator.training/wp-content/uploads/2014/12/customMats.jpg?width=1280&auto=webp&quality=80&disable=upscale)


I created ID maps for all the different parts so the materials could easily be assigned in Quixel Suite and we could make easy adjustments to the final textures.

![idWrist idWrist](http://www.gladiator.training/wp-content/uploads/2014/12/idWrist-300x235.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The ID map defines different materials on this wrist guard

![goldWrist goldWrist](http://www.gladiator.training/wp-content/uploads/2014/12/goldWrist-300x235.jpg?width=1280&auto=webp&quality=80&disable=upscale)


One of my custom Brass metal materials

The greatest part of this process is messing around with various materials based of the ID's, instant texturing has arrived!

![isolated isolated](http://www.gladiator.training/wp-content/uploads/2014/12/isolated-300x258.jpg?width=1280&auto=webp&quality=80&disable=upscale)


With everything created and rebaked using this process we end up with the final texture maps and a new ID map based on the new UVs which is used on the final model.

![Hoplomachus_textures Hoplomachus_textures](http://www.gladiator.training/wp-content/uploads/2014/12/Hoplomachus_textures.jpg?width=1280&auto=webp&quality=80&disable=upscale)



Finally here is the full textured version of the Hoplomachus Armourset.

![hoplomachusArmour hoplomachusArmour](http://www.gladiator.training/wp-content/uploads/2014/12/hoplomachusArmour.png?width=1280&auto=webp&quality=80&disable=upscale)