---
title: Shadows & Light
url: https://claire-blackshaw.com/blog/2010/05/shadows-light/
author: Claire Blackshaw
published: '2010-05-11'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![Shadows & Light](../../assets/4e402aebc4c1a4e8.png)

### Lights Camera & Action

Well lighting & shadows are a complex bag of trickery and maths.

Basic Lighting is simple. Take a book outside into the sun now rotate the bugger around and throw it. You will notice the amount of light on a surface can be measure as an angle between the light direction (from the sun) and the facing direction of the surface. A very cheap and easy calculation we love, called **dot product**.

Now shadows are more complex. Light as a physics based thing in reality is a crazy thing which drove Einstein insane. For instance do you know light is affected by gravity so it actually bends around objects forming a very distinctive halo effect. So not only is it a ray cast but it’s a particle/wave which is affected by gravity fields. They also split up and bounce all over the place.

Now in games we fake it, cause those calculations are really expensive, and most times we care more about whether a bullet hit a guys head.

### Bake It

A cheap and simply trick is to back the shadows. This works well if the lights & geometry don’t move much. Even in AAA games with more advanced systems, baked light maps do a lot of the heavy lifting.

To bake it we basically do the calculation before the game runs. The simplest form is a flat planar map, some bake a projection map and some cases even bake shadow volumes. We can animate the baked textures and get some awesome effects.

### Fake It

Okay so we have this bad guy, race car or some other object in the world. Well we can forgive a lot with our suspension of disbelief. What if we glued a “blob” shadow to the feet of bad guys or race car.

You would be amazed how many games use this system to optimise thing and it looks great.

### Flatten It

Well if we simplify light and ignore the bending, bouncing, and craziness of it, then we can treat it as a straight line from the light. Now we like planes, planes are really nice simple flat things.

Okay so now we have this thing called the projection matrix which is part of the matrix of projecting a 3D object into a 2D image. Well if we use the same trick we can clone an object, then squish it into a projection and render it all black. We have a shadow, Peter Pan Style.

### Deferred Volume

Okay well know in reality we need to drop shadows onto complex geometries. Now we also have this wonderful shader pipeline. Before we render the scene we render the entire world from the perspective of the light (as we would the camera). We then grab the depth buffer and save it.

This needs to be done once for each light.

Now this makes an image of how far the beam of light travels. Which we pass in to the next render pass, along with light matrix. Now if we take a point in space transform it by the Model-View-Projection as normal. Also Transform is by Model-Light-Projection. Then we compare the MLP read-out against the baked texture we can tell if the light reaches that point or not.

Another way of doing Volume Shadows is to use Stencil Buffers, this is the traditional way to do things and how most shadow volumes have been done in the last 10 years.