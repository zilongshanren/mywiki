---
title: 'Keeping the Blue Side Up: Coordinate Conventions for OpenGL, Metal and Vulkan'
url: http://hacksoflife.blogspot.com/2019/04/keeping-blue-side-up-coordinate.html
author: Benjamin Supnik
published: '2019-04-06'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

OpenGL, Metal and Vulkan all have different ideas about which way is up - that is, where the origin is located and which way the Y axis goes for a framebuffer. This post explains the API differences and suggests a few ways to cope with them. I'm not going to cover the Z axis or Z-buffer here - perhaps that'll be a separate post.




This means that your model's UV maps and textures will Just Work™ in all three APIs. When your artist puts 0,0 into that giant fighting robot's UV map, the intent is "the texels at the beginning of memory for that texture." You can load the image into the API the same way on all platforms and the UV map will pull out the right texels and the robot will look shiny.


All three APIs also agree on the definition of a clockwise or counterclockwise polygon - this decision is made in framebuffer coordinates as a human would see it if presented to the screen. This works out well - if your model robot is drawing the way you expect, the windings are the way your artist created them, and you can keep your front face definition consistent across APIs.







What's weird about this is that every window manager ever uses +Y = down, so your OpenGL driver is


In the OpenGL world, we render with the +Y axis being up, the high memory of the framebuffer is the top of the image, which is what the user sees, and if we render to texture, the higher texel coordinates are that top of the image, so everything is good. You basically can't mess this system up.




The window manager presents Metal framebuffers with the lowest byte in the upper left, so if you go in with a model that transforms with +Y = up (OpenGL style), your image will come out right side up and all is good. But be warned, chaos lurks beneath the surface.


Metal's viewport and scissors are defined in framebuffer coordinates, so they now run +Y=down, and will require parameter adjustment to match OpenGL.


Note also that our screenshot code that reads back the framebuffer will have to run differently on OpenGL and Metal; one (depending on your output image file format) will require an image flip, and one will not.




Unfortunately in the render-to-texture case, Metal's upper-left origin has been applied - the sky is now in low memory and the grass is in high memory, and our code that samples this image will show something upside-down and probably quite silly looking.



For X-Plane, we picked door number 1 -


Why do it this way? Well, in our case, we often have shaders that sample both from images on disk and from rendered textures; if we flip our textures on disk (to match Metal's default framebuffer orientation) then we have to adjust


For Metal, we need to intentionally flip the Y coordinate by applying a Y-reverse to our transform stack - in our case this also meant ensuring that


We also need to change our front face's winding order, because winding orders are labeled in the API based on what a human would see if the image is presented to the screen. By mirroring our image to be upside down, we've also inverted all of our models' triangle windings, so we need to change our definition of what is in front.




Had we left well enough alone, this would have been fine, as Metal wants to put the upper left of an image in low memory when rasterizing. But since we intentionally flipped things, we're now...upside down again.


Here we have two options:




Flipping the window coordinate in the sampled code makes sense when the window position is going to be used to reconstitute some kind of world-space coordinate system. Our skydome, for example, is drawn as a full screen quad that calculates the ray that would project through the point in question. It takes as inputs the four corners of the view frustum, and swapping those in C++ fixes our sampling to match our upside down^H^H^H^H^H^HOpenGL-and-perfect-just-the-way-it-is image.






Apparently: headstands! Vulkan's default coordinate orientation is +Y=down, full stop. The upper left of the framebuffer is the origin, and there's no inversion of the Y axis. This is consistent, but it's also consistently different from


The good news is: with Vulkan 1.1 you can specify a negative viewport height, which gives you a Y axis swap. With this trick, Vulkan maches DX and Metal, and all you have to worry about it is all of the craziness listed above.



* a side effect of this is: when I built our table UI component, I defined the bottom-most row of the table as row 0. My co-workers incorrectly think this is a weird convention for UI, and one of them went as far as to write a table row flipping function called


#### Things We Can All Agree On

Let's start with some stuff that's the same for all three APIs: in all three APIs the origin of a framebuffer and the origin of a texture both represent the lowest byte in memory for the data backing that image. In other words, memory addressing starts at 0,0 and then increases as we go the right, then as we go to the next line. Whether we are in texels in a texture or pixels in a framebuffer, this relationship holds up.This means that your model's UV maps and textures will Just Work™ in all three APIs. When your artist puts 0,0 into that giant fighting robot's UV map, the intent is "the texels at the beginning of memory for that texture." You can load the image into the API the same way on all platforms and the UV map will pull out the right texels and the robot will look shiny.

All three APIs also agree on the definition of a clockwise or counterclockwise polygon - this decision is made in framebuffer coordinates as a human would see it if presented to the screen. This works out well - if your model robot is drawing the way you expect, the windings are the way your artist created them, and you can keep your front face definition consistent across APIs.

#### Refresher: Coordinate Systems

For the purpose of our APIs, we care about three coordinate systems:- Clip Coordinates: these are the coordinates that come out of your shader. It's often to think in terms of normalized device coordinates (NDC) - the post-clip, post-perspective divide coordinates - but you don't get to see them.
- Framebuffer coordinates. These are the coordinates that are rasterized, after the NDC coordinates are transformed by the viewport transform.
- Texture coordinates. These are the coordinates we feed into the samplers to read from textures. They're not that interesting because, per above, they work the same on all APIs.

#### OpenGL: Consistently Weird

OpenGL's conventions are different from approximately every other API ever, but at least they are*self-consistent*: every single origin in OpenGL is in the lower left corner of the image, so the +Y axis is always up. +Y is up in clip coordinates, NDC, and framebuffer coordinates.What's weird about this is that every window manager ever uses +Y = down, so your OpenGL driver is

*prrrrrobably*flipping the image for you when it sends it off to the compositor or whatever your OS has. But after 15+ years of writing OpenGL code, +Y=up now seems normal to me, and the consistency is nice. One rule works everywhere.*In the OpenGL world, we render with the +Y axis being up, the high memory of the framebuffer is the top of the image, which is what the user sees, and if we render to texture, the higher texel coordinates are that top of the image, so everything is good. You basically can't mess this system up.

#### Metal: Up is Down and Down is Up

Metal's convention is to have +Y = up in clip coordinates (and NDC) but +Y = down in framebuffer coordinates, with the framebuffer origin in the upper left. While this is baffling to programmers coming from GL/GLES, it feels familiar to Direct3d programmers. In Metal, the viewport transformation has a built-in Y flip that you can't control at the API level.The window manager presents Metal framebuffers with the lowest byte in the upper left, so if you go in with a model that transforms with +Y = up (OpenGL style), your image will come out right side up and all is good. But be warned, chaos lurks beneath the surface.

Metal's viewport and scissors are defined in framebuffer coordinates, so they now run +Y=down, and will require parameter adjustment to match OpenGL.

Note also that our screenshot code that reads back the framebuffer will have to run differently on OpenGL and Metal; one (depending on your output image file format) will require an image flip, and one will not.

#### Render-to-Texture: Two Wrongs Make a "Ship It"

Here's the problem with Metal: let's say we draw a nice scene with blue sky up top and green grass on the bottom. We're going to use it as an environment input and sample it. Our OpenGL code expects that low texture coordinates (near 0) get us the green grass at the bottom of memory and high texture coordinates (near 1) get us the blue sky at the top of memory.Unfortunately in the render-to-texture case, Metal's upper-left origin has been applied - the sky is now in low memory and the grass is in high memory, and our code that samples this image will show something upside-down and probably quite silly looking.

We have two options:

- Adjust the image at creation time by hacking the transform matrix or
- Adjusting the code that uses the image by adjusting the sampling coordinates.

For X-Plane, we picked door number 1 -

*intentionally*render the image upside down (by Metal standards, or "the way it was meant to be" by OpenGL standards) so that the image is oriented as the samplers expect.Why do it this way? Well, in our case, we often have shaders that sample both from images on disk and from rendered textures; if we flip our textures on disk (to match Metal's default framebuffer orientation) then we have to adjust

*every*UV map that references a disk image, and that's a huge amount of code, because it covers all shaders and C++ code that generate UV maps. Focusing on render-to-texture is a smaller surface area to attack.For Metal, we need to intentionally flip the Y coordinate by applying a Y-reverse to our transform stack - in our case this also meant ensuring that

*every*shader used the transform stack; we had a few that were skipping it and had to be set up with identity transforms so the low level code could slip in the inversion.We also need to change our front face's winding order, because winding orders are labeled in the API based on what a human would see if the image is presented to the screen. By mirroring our image to be upside down, we've also inverted all of our models' triangle windings, so we need to change our definition of what is in front.

#### Sampling with the gl_FragCoord or [[position]]: Three Wrongs Make a "How Did I Get Here"?

There's one more loose end with Metal: if you wrote a shader that uses gl_FragCoord to reconstruct some kind of coordinates based on the window rasterization position, they're going to be upside-down from what your shader did in OpenGL. The upper left of your framebuffer will rasterize with 0,0 for its position, and if you pass this on to a texture sampler, you're going to pick off low memory.Had we left well enough alone, this would have been fine, as Metal wants to put the upper left of an image in low memory when rasterizing. But since we intentionally flipped things, we're now...upside down again.

Here we have two options:

- Don't actually flip the framebuffer when rendering to texture. Maybe that was a dumb idea.
- Insert code to flip the window coordinates.

Flipping the window coordinate in the sampled code makes sense when the window position is going to be used to reconstitute some kind of world-space coordinate system. Our skydome, for example, is drawn as a full screen quad that calculates the ray that would project through the point in question. It takes as inputs the four corners of the view frustum, and swapping those in C++ fixes our sampling to match our upside down^H^H^H^H^H^HOpenGL-and-perfect-just-the-way-it-is image.

#### What Have We Learned (About Metal)

So to summarize, with Metal:- If we're going to render to a texture for a model, we put a Y-flip into our transform stack and swap our front face winding direction.
- If we're going to render to a texture for sampling via window coordinates, we don't.
- If we're going to use window coordinates to reconstruct 3-d, we have to swap the reconstruction coefficients.

#### Vulkan: What Would Spock Do?

Apparently: headstands! Vulkan's default coordinate orientation is +Y=down, full stop. The upper left of the framebuffer is the origin, and there's no inversion of the Y axis. This is consistent, but it's also consistently different from

*every*other 3-d API ever, in that the Y axis in clip coordinates is backward from OpenGL, Metal, and DX.The good news is: with Vulkan 1.1 you can specify a negative viewport height, which gives you a Y axis swap. With this trick, Vulkan maches DX and Metal, and all you have to worry about it is all of the craziness listed above.

* a side effect of this is: when I built our table UI component, I defined the bottom-most row of the table as row 0. My co-workers incorrectly think this is a weird convention for UI, and one of them went as far as to write a table row flipping function called

correct_row_indexes_because_bens_table_api_was_intentionally_written_backwards_so_we_dont_ask_him_to_write_UI_controls_any_more.The moral of the story is that +Y=up is both consistent and a great way to get out of being asked to maintain old and poorly thought out UI widgets. I trust my co-worker will come around to my way of thinking in another fifteen years.

OpenGL coordinates : "You basically can't mess this system up."


ReplyDeleteIt's worth pointing out that actually it's easy to mess up in OpenGL and lots of people do, because image loaders such as stb_image load image data top row first, whereas OpenGL expects data bottom row first. You can fix it by flipping your UVs, but then if you try rendering to texture you'll find that's upside down! More discussion here : https://stackoverflow.com/questions/19770296/should-i-vertically-flip-the-lines-of-an-image-loaded-with-stb-image-to-use-in-o

That's where stbi_set_flip_vertically_on_load(true) comes in handy!

Delete