---
title: Wood Carved Character Design Tutorial
url: https://www.gamedeveloper.com/art/wood-carved-character-design-tutorial
author: Megan Hughes
published: '2015-06-18'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

Originally posted to the [RetroEpic blog](http://www.retroepic.com/a-day-in-the-woods-character-design-tutorial/). Written by Hannes Ferreira - edited and reposted by Megan Hughes with permission.

Since re-releasing our sliding puzzle game title, [A Day in the Woods](http://www.retroepic.com/our-games/a-day-in-the-woods/), a little earlier this year and sharing some of our character designs on the [Polycount forums](http://www.polycount.com/forum/showthread.php?p=2290384#post2290384), we've had a lot of interest in exactly how we got the wood carved look right. So, in order to add to the hoards of modelling tutorials on the web and share a little of my knowledge, I give you this step-by-step tutorial which explains my workflow for creating the models for A Day in the Woods. We'll focus on a slightly more grown up version of our lead female character, Little Red Riding Hood, for this character design tutorial:


Let's get started then.

First things first, start by creating the base mesh in Blender. You can load in reference images to model from but for this tutorial I've jumped straight to the modelling. We're aiming for a carved wooden look for our character which means that the base model doesn't need to be very detailed. We'll be sculpting in that detail later on.


Next step is to export the mesh from Blender to ZBrush. The arms and legs are going to be mirrored so it's not necessary to add the right hand side pieces for the sculpting process. (As a bonus, you'll also be using less memory this way). Using the flatten brush with a negative focal shift, you can carve into the model to give it the hand-carved wooden look. You can use this same strategy to create realistic-looking rocks, but that's another tutorial.

After sculpting, generate a cavity mask for each subtool and fill it in with black and white polypaint. You can also mask out the areas between the peaks by tweaking the cavity profile curve a little - something that is going to be used as a mask to break up the cleanliness of the model a bit. Export the subtools as .obj's. These are going to be the high-res meshes to bake from. To create the low poly, decimate the subtools so that you can work with them in Blender.

Back in Blender, after importing the decimated meshes from ZBrush, decimate them further, to the final low-res mesh with Blenders 'Decimate' modifier. Be careful not to go too crazy with this as the decimate process collapses vertices and sometimes you lose the shape of the silhouette. I used a copy of the original decimated mesh as a reference to fix up areas that were decimated too much. For static meshes, this is a quick and dirty way to get nice low poly meshes from your high poly sculpts. You can retopologize it manually for cleaner and better topology, but this can take a fair bit of time.

The next step is to unwrap the low-poly model. Make sure to pack the UV islands tightly together to not waste texture space. I sometimes non-uniformly scale the islands to make them fit better. Usually this will cause stretching when you paint your textures, but in this case the textures are mostly baked so it won't make much of a difference having some of the islands scaled differently.

Another tip, especially for game models, is to have parts of the mesh share texture space. This allows more space for the other parts and thus better quality. The arms and legs get mirrored so they will occupy the same texture area. This might cause problems for baking - something that can be avoided by moving the right arm and leg UVs 1024 pixels out of the texture area (for this model I used 1024 x 1024 resolution texture).

With the low poly mesh completed, export it as .obj and set up xNormal for the baking. xNormal bakes a variety of different maps and for this model I baked out Normal, AO, Vertex Colours and a Curvature Map. Another advantage which xNormal gives, is that it can handle millions of polys, and I'm able to load in the meshes which were exported straight out of zBrush. ![Baking in xNormal. Baking in xNormal.](http://www.retroepic.com/wp-content/uploads/2015/06/tutorial-image-7a.png?width=1280&auto=webp&quality=80&disable=upscale)



The next step is to create a cavity map. This map is useful for making edges and cavities stand out more, by overlaying it over your texture. In this case it also helps me to isolate the peaks so that I can create a mask for edge wear on the model. To create a cavity map, select the normal map layer in Photoshop and copy the red and green channels into their own layers.

Next, apply an emboss filter on the green channel layer with an angle of 90 degrees and emboss the red channel layer with an angle of 0 degrees.

After embossing the layers, overlay the red channel layer over the green channel layer and merge them together. Cavity map complete!

Now to create the edge wear mask. For this, I mixed the curvature map and cavity map together. The curvature map I baked out using the 2 colour setting in xNormal. Red values are the cavities, and green values are the peaks. For this we only need the green values on the map. To isolate it, I used the black and white filter in Photoshop and turned all the red values black and green values white. I then used levels to enhance the white areas. Finally, I took the cavity map and the levels in Photoshop and 'blacked' everything out except for the white peak areas before combining the two maps with "Add Blending Mode". Now you have an edge wear mask where all the white areas will be wood showing through where the paint has worn off.

Now for the wood texture. For this you need a nice clean wood texture (I got one off [cgtextures.com](http://cgtextures.com/)). To get it to wrap seamlessly around the model, make a copy of it and re-UV map it using "Project from view". This usually causes stretching on areas facing to the sides when the project from view wrap is done, but it works nicely with the wood grain patterns. The next step is to bake across the wood texture to the original model.

The wood texture will serve as colour, bumps and detail map for the final texture. To get the bumps and details out of the wood texture, apply a high pass filter to it, which gives more or less the same effect as the cavity map. This can now be overlayed over the painted layer to bring out the wood grains a bit.

To get the bump details, duplicate the high pass layer and apply the "Height2Normals" filter on it (this is one of the plugins that comes from xNormal). You now have a normal map version of the wood details. Before mixing it with the baked normal map, you need to level out the blue channel using the level filter. This ensures that you don't mess up the blue channel of the final normal map when you overlay the details on to it. This is a quick way to add small details to your baked normal maps without have to sculpt it in.

With all the maps finished, it's time to start layering and blending them together. I use a simple folder structure in Photoshop to organise the layers: a folder for the normal map, AO map, colour map, spec map and one for the masks and sometimes a backup folder. To start off, I have my colour map at the bottom (I painted some colours in blender which will be the wood paint layer) and above that the wood texture gets mixed with it using the edge wear mask. This gives it a sort of old used look where the paint started to fade off the peaks. Now, because we're aiming for an old worn out look, we have a paint that still looks too clean. This is where the vertex colour mask generated in ZBrush comes in. I multiplied a layer filled with a reddish brown colour using the vertex colour mask to isolate only the areas in between the peaks. This acts as my dirt map. To further enhance the texture, overlay the high pass wood grain layer and the cavity map generated from the normal map, but with low opacities. The effect should be subtle.

Note: I did some fixes on the edge wear mask in blender and removed areas on the model where paint is less likely to peal or fade off.

I used a different approach for the AO map, which usually just gets multiplied over the texture. This causes the shadows to be black and I want some colour in them. To do this, multiply the AO map with an opacity of 10% followed by a Hue/Saturation adjustment layer with AO map inverted and used as a mask. This gives better control over the shadows because you can now darken them and add some colour to them. Finally, duplicate and overlay the AO map again with an opacity of 30%.

![Multiplying the AO map with 10% opacity and a hue/saturation layer Multiplying the AO map with 10% opacity and a hue/saturation layer](http://www.retroepic.com/wp-content/uploads/2015/06/tutorial-image-15a-351x1024.png?width=1280&auto=webp&quality=80&disable=upscale)



And voila, your final model:

Did you find this character design tutorial helpful? Let us know what you think or request another tutorial in the comments!