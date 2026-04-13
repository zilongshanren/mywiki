---
title: Watch the rendering equation being solved in real-time!
url: http://raytracey.blogspot.com/2010/05/watch-rendering-equation-being-solved.html
author: Sam Lapere
published: '2010-05-18'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[http://www.youtube.com/watch?v=b7W4BQevKiM](http://www.youtube.com/watch?v=b7W4BQevKiM)

It looks dreamy (because of the blur), and it fits the atmosphere perfectly because it fulfills a dream for many (including myself):

![](../../assets/379b28c0696ae163.jpg)


![](../../assets/379b28c0696ae163.jpg)

Watching path tracing in real-time is very satisfying imo, as it has been considered to be the most physically accurate but slowest solution to the rendering equation and it's real-time implementation has remained some kind of a holy grail for graphics researchers since it's conception in the 1980s. Now that this ultimate long sought after goal has (almost) been reached, I found it particularly pleasing to re-read the following overview of the history and principles of path tracing on Wikipedia:


Path tracing ([shamelessly copied from wikipedia])

Path tracing is a computer graphics rendering technique that attempts to simulate the physical behaviour of light as closely as possible. It is a generalisation of conventional ray tracing, tracing rays from the virtual camera through several bounces on or through objects. The image quality provided by path tracing is usually superior to that of images produced using conventional rendering methods at the cost of much greater computation requirements.

Path tracing is the simplest, most physically-accurate and slowest rendering method. It naturally simulates many effects that have to be specifically added to other methods (ray tracing or scanline rendering), such as soft shadows, depth of field, motion blur, caustics, ambient occlusion, and indirect lighting. Implementation of a renderer including these effects is correspondingly simpler.

Due to its accuracy and unbiased nature, path tracing is used to generate reference images when testing the quality of other rendering algorithms. In order to get high quality images from path tracing, a very large number of rays need to be traced lest the image have lots of visible artefacts in the form of noise.

History

The rendering equation and its use in computer graphics was presented by James Kajiya in 1986.[1] This presentation contained what was probably the first description of the path tracing algorithm. Later that year, Lafortune suggested many refinements, including bidirectional path tracing.[2]

Metropolis light transport, a method of perturbing previously found paths in order to increase performance for difficult scenes, was introduced in 1997 by Eric Veach and Leonidas J. Guibas.

More recently, computers and GPUs have become powerful enough to render images more quickly, causing more widespread interest in path tracing algorithms. Tim Purcell first presented a global illumination algorithm running on a GPU in 2002.[3] In 2009, Vladimir Koylazov from Chaos Group demonstrated the first commercial implementation of a path tracer running on a GPU, and other implementations have followed.[4] This was aided by the maturing of GPGPU programming toolkits such as CUDA and OpenCL.

Description

In the real world, many small amounts of light are emitted from light sources, and travel in straight lines (rays) from object to object, changing colour and intensity, until they are absorbed (possibly by an eye or camera). This process is simulated by path tracing, except that the paths are traced backwards, from the camera to the light. The inefficiency arises in the random nature of the bounces from many surfaces, as it is usually quite unlikely that a path will intersect a light. As a result, most traced paths do not contribute to the final image.

This behaviour is described mathematically by the rendering equation, which is the equation that path tracing algorithms try to solve.

Path tracing is not simply ray tracing with infinite recursion depth. In conventional ray tracing, lights are sampled directly when a diffuse surface is hit by a ray. In path tracing, a new ray is randomly generated within the hemisphere of the object and then traced until it hits a light(possibly never). This type of path can hit many diffuse surfaces before interacting with a light.

Bidirectional path tracing

n order to accelerate the convergence of images, bidirectional algorithms trace paths in both directions. In the forward direction, rays are traced from light sources until they are too faint to be seen or strike the camera. In the reverse direction (the usual one), rays are traced from the camera until they strike a light or too many bounces ("depth") have occurred. This approach normally results in an image that converges much more quickly than using only one direction.

Veach and Guibas give a more accurate description[5]:

These methods generate one subpath starting at a light source and another starting at the lens, then they consider all the paths obtained by joining every prefix of one subpath to every suffix of the other. This leads to a family of different importance sampling techniques for paths, which are then combined to minimize variance.

Performance

A path tracer continuously samples pixels of an image. The image starts to become recognisable after only a few samples per pixel, perhaps 100. However, for the image to "converge" and reduce noise to acceptable levels usually takes around 5000 samples for most images, and many more for pathological cases. This can take hours or days depending on scene complexity and hardware and software performance. Newer GPU implementations are promising from 1-10 million samples per second on modern hardware, producing acceptably noise-free images in seconds or minutes.[citation needed] Noise is particularly a problem for animations, giving them a normally-unwanted "film-grain" quality of random speckling.

Metropolis light transport obtains more important samples first, by slightly modifying previously-traced successful paths. This can result in a lower-noise image with fewer samples.

Renderer performance is quite difficult to measure fairly. One approach is to measure "Samples per second", or the number of paths that can be traced and added to the image each second. This varies considerably between scenes and also depends on the "path depth", or how many times a ray is allowed to bounce before it is abandoned. It also depends heavily on the hardware used. Finally, one renderer may generate many low quality samples, while another may converge faster using fewer high-quality samples.

Scattering distribution functions

The reflective properties (amount, direction and colour) of surfaces are modelled using BRDFs. The equivalent for transmitted light (light that goes through the object) are BTDFs. A path tracer can take full advantage of complex, carefully modelled or measured distribution functions, which controls the appearance ("material", "texture" or "shading" in computer graphics terms) of an object.

## No comments:

Post a Comment