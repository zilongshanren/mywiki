---
title: 'OpenCL path tracing tutorial 2: path tracing spheres'
url: http://raytracey.blogspot.com/2016/11/opencl-path-tracing-tutorial-2-path.html
author: Sam Lapere
published: '2016-11-14'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This tutorial consists of two parts: the first part will describe how to ray trace one sphere using OpenCL, while the second part covers path tracing of a scene made of spheres. The tutorial will be light on ray tracing/path tracing theory (there are plenty of excellent resources available online such as Scratch-a-Pixel) and will focus instead on the practical implementation of rendering algorithms in OpenCL.The end result will be a rendered image featuring realistic light effects such as indirect lighting, diffuse colour bleeding and soft shadows, all achieved with just a few lines of code:

**Part 1: Ray tracing a sphere**

**Computing a test image on the OpenCL device**

The host (CPU) sets up the OpenCL environment and launches the OpenCL kernel which will be executed on the OpenCL device (GPU or CPU) in parallel. Each work item (or thread) on the device will calculate one pixel of the image. There will thus be as many work items in the global pool as there are pixels in the image. Each work item has a unique ID which distinguishes from all other work items in the global pool of threads and which is obtained with

**get_global_id(0)**.
The X- and Y-coordinates of each pixel can be computed by using that pixel's unique work item ID:

- x-coordinate: divide by the image width and take the remainder
- y-coordinate: divide by the image width

By remapping the x and y coordinates from the [0 to width] range for x and [0 to height] range for y to the range [0 - 1] for both, and plugging those values in the red and green channels repsectively yields the following gradient image (the image is saved in ppm format which can be opened with e.g. IrfanView of Gimp):

The OpenCL code to generate this image:

Now let's use the OpenCL device for some ray tracing.

**Ray tracing a sphere with OpenCL**

We first define a



**Ray**and a**Sphere**struct in the OpenCL code:
A


**Ray**has- an
**origin**in 3D space (3 floats for x, y, z coordinates) - a
**direction**in 3D space (3 floats for the x, y, z coordinates of the 3D vector)

A


**Sphere**has- a
**radius**, - a
**position**in 3D space (3 floats for x, y, z coordinates), - an object
**colour**(3 floats for the Red, Green and Blue channel) - an
**emission**colour (again 3 floats for each of the RGB channels)

**Camera ray generation**

Rays are shot from the camera (which is in a fixed position for this tutorial) through an imaginary grid of pixels into the scene, where they intersect with 3D objects (in this case spheres). For each pixel in the image, we will generate one camera ray (also called primary rays, view rays or eye rays) and follow or trace it into the scene. For camera rays, the ray origin is the camera position and the ray direction is the vector connecting the camera and the pixel on the screen.

![]() |

The OpenCL code for generating a camera ray:




**Ray-sphere intersection**

To find the intersection of a ray with a sphere, we need the parametric equation of a line, which denotes the

**distance from the ray origin to the intersection point along the ray direction**with the parameter**"t"**:**intersection point = ray origin + ray direction * t**

The equation of a sphere follows from the Pythagorean theorem in 3D (all points on the surface of a sphere are located at a distance of radius

**r**from its center):**(sphere surface point - sphere center)**


2= radius2
In the case of a sphere centered at the origin (with coordinates [0,0,0]), the vector [sphere surface point - sphere center] reduces to the coordinates of a point on the sphere's surface (the intersection point). Combining both equations then gives



**(ray origin + ray direction * t)**

2= radius2

Expanding this equation in a


**quadratic equation**of the form**ax****where**2+ bx + c = 0- a = (ray direction) . (ray direction)
- b = 2 * (ray direction) . (ray origin to sphere center)
- c = (ray origin to sphere center) . (ray origin to sphere center) - radius
2

yields solutions for


Depending on whether the determinant is negative, zero or positive, there can be zero (ray misses sphere), one (ray just touches the sphere at one point) or two solutions (ray fully intersects the sphere at two points) respectively. The distance t can be positive (intersection in front of ray origin) or negative (intersection behind ray origin). The details of the mathematical derivation are explained in

**t**(the distance to the point where the ray intersects the sphere) given by the**quadratic formula**−b ± √ b2− 4ac / 2a (where**b****is called the discriminant).**2- 4acDepending on whether the determinant is negative, zero or positive, there can be zero (ray misses sphere), one (ray just touches the sphere at one point) or two solutions (ray fully intersects the sphere at two points) respectively. The distance t can be positive (intersection in front of ray origin) or negative (intersection behind ray origin). The details of the mathematical derivation are explained in

[this Scratch-a-Pixel article.](http://www.scratchapixel.com/lessons/3d-basic-rendering/minimal-ray-tracer-rendering-simple-shapes/ray-sphere-intersection)
The ray-sphere intersection algorithm is optimised by omitting the "a" coefficient in the quadratic formula, because its value is the dot product of the normalised ray direction with itself which equals 1. Taking the square root of the discriminant (an expensive function) can only be performed when the discriminant is non-negative.

**Scene initialisation**

For simplicity, in this first part of the tutorial the scene will be initialised on the device in the kernel function (in the second part the scene will be initialised on the host and passed to OpenCL which is more flexible and memory efficient, but also requires to be more careful with regards to memory alignment and the use of memory address spaces). Every work item will thus have a local copy of the scene (in this case one sphere).

**Running the ray tracer**

Now we've got everything we need to start ray tracing! Let's begin with a plain colour sphere. When the ray misses the sphere, the background colour is returned:

A more interesting sphere with cosine-weighted colours, giving the impression of front lighting.

To achieve this effect we need to calculate the angle between the ray hitting the sphere surface and the normal at that point. The sphere normal at a specific intersection point on the surface is just the normalised vector (with unit length) going from the sphere center to that intersection point.

Adding some stripe pattern by multiplying the colour with the sine of the height:

Screen-door effect using sine functions for both x and y-directions

Showing the surface normals (calculated in the code snippet above) as colours:

**Source code**

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-1-Raytracing-a-sphere](https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-1-Raytracing-a-sphere)

**Download demo**(works on AMD, Nvidia and Intel)

The executable demo will render the above images.

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-1-Raytracing-a-sphere/releases/tag/1.0](https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-1-Raytracing-a-sphere/releases/tag/1.0)

**Part 2: Path tracing spheres**

**Very quick overview of ray tracing and path tracing**

The following section covers the background of the ray tracing process in a very simplified way, but should be sufficient to understand the code in this tutorial. Scratch-a-Pixel provides a much more detailed explanation of ray tracing.

**Ray tracing**is a general term that encompasses ray casting, Whitted ray tracing, distribution ray tracing and path tracing. So far, we have only traced rays from the camera (so called "camera rays", "eye rays" or "

**primary rays**") into the scene, a process called

**ray casting**, resulting in plainly coloured images with no lighting. In order to achieve effects like shadows and reflections, new rays must be generated at the points where the camera rays intersect with the scene. These

**secondary rays**can be shadow rays, reflection rays, transmission rays (for refractions), ambient occlusion rays or diffuse interreflection rays (for indirect lighting/global illumination). For example, shadow rays used for direct lighting are generated to point directly towards a light source while reflection rays are pointed in (or near) the direction of the reflection vector. For now we will skip direct lighting to generate shadows and go straight to path tracing, which is strangely enough easier to code, creates more realistic and prettier pictures and is just more fun.

In (plain)

**path tracing**, rays are shot from the camera and bounce off the surface of scene objects in a**random direction**(like a high-energy bouncing ball), forming a**chain of random rays connected together into a path**. If the path hits a light emitting object such as a light source, it will return a colour which depends on the surface colours of all the objects encountered so far along the path, the colour of the light emitters, the angles at which the path hit a surface and the angles at which the path bounced off a surface. These ideas form the essence of the "**rendering equation**", proposed in a paper with the same name by Jim Kajiya in 1986.
Since the directions of the rays in a path are generated randomly, some paths will hit a light source while others won't, resulting in noise ("variance" in statistics due to random sampling). The noise can be reduced by shooting many random paths per pixel (= taking many

**samples**) and averaging the results.**Implementation of (plain) path tracing in OpenCL**

The code for the path tracer is based on smallpt from Kevin Beason and is largely the same as the ray tracer code from part 1 of this tutorial, with some important differences on the host side:

- the scene is initialised on the host (CPU) side, which requires a host version of the Sphere struct. Correct

**memory alignment**in the host struct is very important to avoid shifting of values and wrongly initialised variables in the OpenCL struct, especially when using OpenCL's built-in data types such as float3 and float4. If necessary, the struct should be padded with dummy variables to ensure memory alignment (the total size of the struct must be a multiple of the size of float4).
- the scene (an array of spheres) is copied from the host to the OpenCL device into global memory (using

**CL_MEM_READ_WRITE**) or constant memory (using**CL_MEM_READ_ONLY**)
- explicit memory management: once the scene is on the device, its pointer can be passed on to other device functions preceded by the keyword "

**__global**" or "**__constant**".
- the host code automatically determines the local size of the kernel work group (the number of work items or "threads" per work group) by calling the OpenCL function

**kernel.getWorkGroupInfo**(device) **The actual path tracing function**

-

**iterative path tracing function**: since OpenCL does not support recursion, the trace() function traces paths iteratively (instead of recursively) using a loop with a fixed number of bounces (iterations), representing path depth.
- each path starts off with an "

**accumulated colour**" initialised to black and a "**mask colour**" initialised to pure white. The mask colour "collects" surface colours along its path by multiplication. The accumulated colour accumulates light from emitters along its path by adding emitted colours multiplied by the mask colour.
-

**generating random ray directions**: new rays start at the hitpoint and get shot in a random direction by sampling a random point on the hemisphere above the surface hitpoint. For each new ray, a local orthogonal uvw-coordinate system and two random numbers are generated: one to pick a random value on the horizon for the azimuth, the other for the altitude (with the zenith being the highest point)
-

**diffuse materials**: the code for this tutorial only supports diffuse materials, which reflect incident light almost uniformly in all directions (in the hemisphere above the hitpoint)
-


- while ray tracing can get away with tracing only one ray per pixel to render a good image (more are needed for anti-aliasing and blurry effects like depth-of-field and glossy reflections), the inherently noisy nature of path tracing requires tracing of

**cosine-weighted importance sampling:**because diffuse light reflection is not truly uniform, the light contribution from rays that are pointing away from the surface plane and closer to the surface normal is greater. Cosine-weighted importance sampling favours rays that are pointing away from the surface plane by multiplying their colour with the cosine of the angle between the surface normal and the ray direction.- while ray tracing can get away with tracing only one ray per pixel to render a good image (more are needed for anti-aliasing and blurry effects like depth-of-field and glossy reflections), the inherently noisy nature of path tracing requires tracing of

**many paths per pixel**(samples per pixel) and averaging the results to reduce noise to an acceptable level.A screenshot made with the code above (also see the screenshot at the top of this post). Notice the colour bleeding (bounced colour reflected from the floor onto the spheres), soft shadows and lighting coming from the background.

**Source code**

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-2-Path-tracing-spheres](https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-2-Path-tracing-spheres)

**Downloadable demo**(for AMD, Nvidia and Intel platforms, Windows only)

[https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-2-Path-tracing-spheres/releases/tag/1.0](https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-2-Path-tracing-spheres/releases/tag/1.0)

**Useful resources**

-

[Scratch-a-pixel](http://www.scratchapixel.com/)is an excellent free online resource to learn about the theory behind ray tracing and path tracing. Many code samples (in C++) are also provided.

[This article](http://www.scratchapixel.com/lessons/3d-basic-rendering/global-illumination-path-tracing)gives a great introduction to global illumination and path tracing.

-

[smallpt by Kevin Beason](http://www.kevinbeason.com/smallpt/)is a great little CPU path tracer in 100 lines code. It of formed the inspiration for the Cornell box scene and for many parts of the OpenCL code

**Up next**

The next tutorial will cover the implementation of an interactive OpenGL viewport with a progressively refining image and an interactive camera with anti-aliasing and depth-of-field.

## 13 comments:

Sam, thank you so much for these tutorials! Your explanations are very helpful and the code is clean and well commented. In case you or anyone else reading this is interested, I have gone off and started my own side project a while back using some ideas from your older blog posts. I started with a port of SmallPT to WebGL (GLSL shader), and over the past months have included a lot of extras such as clear coat materials and cones/cylinders intersection support. The cool thing is that all of this runs in your web browser in real time,even on your smartphone! Here's the project page: https://github.com/erichlof/THREE.js-PathTracing-Renderer


Looking forward to your next tutorials Sam. I'm beginning to hit a speed wall with WebGL capping the framerate at 60fps in the browser, so maybe your OpenCL code (with future BVH) will help take my project to the next level. Thanks again for sharing your expertise and hard work!

-Erich

Thanks for the nice words. Coincidentally, I have dabbled in WebGL and Three.js a few months back myself, also making a port of smallpt, you can see the very WIP result here. While it worked fine in Chrome, I didn't find the performance on Firefox very stable. Your WebGL renderer looks pretty neat though.



If you're interested in porting a BVH to GLSL or WebGL these links might be helpful:

Implementing a practical rendering system using GLSL" (a GLSL raytracer using BVH)

and

WebGL path tracing with BVH

Thank you for the links! I am going through them now. I don't know how these went under my radar! Yeah there's definitely performance trade-offs with raw performance vs. being able to run on most browsers which are everywhere these days. The main thing holding my project up is the BVH. I have the triangle intersection and .obj loader already functioning, but it is super slow, even for a 100 triangle model. Hopefully I can some insight from the resources you directed me to. btw your WebGL smallPT port looks pretty cool, I didn't realize you had done that in the past. Thanks again!

No problem. I hadn't mentioned the WebGL thing before as it was just an experiment to learn about WebGL and see if it is a viable technology for real-time ray traced graphics. I've noticed that WebGL performance is highly dependent on the number of tabs open in the browser. When surfing the net, I typically have 10 or more tabs open with lots of animated banner ads and a Youtube music video playing in the background, eating up GPU resources and dragging the WebGL performance down a lot. Both Chrome and Firefox suffer from this. If browsers can't solve this, I don't see how web based 3D can take off.


If there's only one open tab, a WebGL based path tracer with BVH should offer quite decent performance like in this video https://vimeo.com/55606763

Btw, this guy has implemented a grid structure to accelerate ray tracing in WebGL, it's pretty neat: http://dev.miaumiau.cat/rayTracer/

Wow, cool stuff! While I was checking out the miaumiau.cat link, there was a link to where the grid structure idea came from: https://directtovideo.wordpress.com/category/ray-tracing/



Looks like quite a few folks have been thinking about decent acceleration structures for GPU real-time rendering.

Yeah it's unfortunate about the WebGL limitations. WebGL 2.0 is on the horizon though with support for 3D textures, multiple render targets, and the like. Maybe some clever people can leverage the 3D textures for fast scene grid data look-ups or something of that nature.

In the meantime, I'm looking forward to your next OpenCL tutorials!

Hi again, just wanted to report a quick source code typo:

https://github.com/straaljager/OpenCL-path-tracing-tutorial-2-Part-2-Path-tracing-spheres/blob/master/opencl_kernel.cl

On line 7 I think you might have meant to put '24', not '2400' samples. I copied the original file into my project and it crashed my computer every time. 24 or 32 works fine however.

Thanks again for the tutorials!

Thanks for noticing that. I was rendering 2400 samples on the CPU, the GPU driver crashes indeed when the kernel takes more then 10 seconds to finish. It's fixed now.


There's also an interesting video by Matt Swoboda (the guy behind the directtovideo blog) with some clever ideas on real-time ray traced global illumination: https://www.youtube.com/watch?v=JSr6wvkvgM0

There's some interesting food for thought in that video, especially the brickmap topic. Also it's one of the few hybrid solutions currently out in the wild (rasterized triangles with a geometry shader to avoid the initial camera raycast, and then path tracing the 2nd/higher-order bounces in the fragment shader for reflections, AO, diffuse color-sharing, etc.).


I always liked the idea of doing that, but I don't know anything about geometry shaders and how they communicate to the fragment shader. - I have just been making the fragment shader do all the work in my experiments because that's what I've seen on Shadertoy and the like. Thanks for the video link!

Hi, I am learning about OpenCL for my undergrad thesis.




I have gone through each section carefully but I ran into a few issues.

First is that I had to get the cl2.hpp and then define the target OpenCL version at 200.

After this I had an issue with my vectors and had to specify std before each vector.

After all that the program ran, but the output image is just a black box? Any help would be great :)

I am learning OpenCL for my undergrad thesis but I have ran into a few issues.



First I had to download and include cl2.hpp to avoid some discrepancy errors. After that I had to define the target version at 200 which broke all my vectors, fixed that but putting std:: before each vector as it was confused about cl:vector or std::vector.

The program now runs, but the output image is black. Any help would be great! :)

Hi Sam, thank you for this blog, it is precious for the it's contents and detailed.






Said this, i would like to understand better the createCamRay() function, especially in the aspect ratio formula, i didn't really get this two line of codes :

float fx2 = (fx - 0.5f) * aspect_ratio;

float fy2 = fy - 0.5f;

I think they should make something with the center of the screen but i'm confused, i would enjoy an explanation from you.

And the 40.0f means the we are using the right hand notation, and the camera is more "near" us ?

Thanks again, cya!

Hello and thank you very much for theses tutorials. This is really helpful. I'm currently learning OpenCL based on your ray tracer. However, I encounter an awkward difficulty : when I run your code on my CPU everything is ok and when I run it on my "GPU" (I'm on a classical macbook so that's just an Intel(R) Iris(TM) Graphics 6100 graphic card) it works only for a small number of sample. To get a 1280x720 picture I should use less than 125 samples. If I want a smaller picture I can ask for more sample. Another strange thing is that this is not the computation that crashes but the extraction of the result from the GPU memory. I get an "Abort trap: 6" at this stage. The number of sample should not modify the behavior of the code no ? Thanks a lot for your consideration (4 years after your publication :) )

Post a Comment