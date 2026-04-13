---
title: 'GPU path tracing tutorial 1: Drawing First Blood'
url: http://raytracey.blogspot.com/2015/10/gpu-path-tracing-tutorial-1-drawing.html
author: Sam Lapere
published: '2015-10-05'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In early 2011 I developed a

[simple real-time path traced Pong game](http://raytracey.blogspot.co.nz/2011/02/update-9-on-realtime-path-traced-pong.html)together with Kerrash on top of an open source GPU path tracer called[tokaspt](https://code.google.com/p/tokaspt/)(developed by Thierry Berger-Perrin) which could only render spheres, but was bloody fast at it. The physics were bodged, but the game proved that path tracing of very simple scenes at 30 fps was feasible, although a bit noisy. You can still download it from[https://code.google.com/p/tokap-the-once-known-as-pong/](https://code.google.com/p/tokap-the-once-known-as-pong/). Since that time I've always wanted to write a short and simple tutorial about GPU path tracing to show how to make your GPU draw an image with high quality ray traced colour bleeding with a minimum of code and now is a good time to do exactly that.
This tutorial is not meant as an introduction to ray tracing or path tracing as there are plenty of excellent ray tracing tutorials for beginners online such as

[Scratch-a-Pixel](http://www.scratchapixel.com/)(also check out the[old version](http://www.scratchapixel.com/old/)which contains more articles) and[Minilight](http://www.hxa.name/minilight/)(more links at the bottom of this article). The goal of this tutorial is simply to show how incredibly easy it is to turn a simple CPU path tracer into a CUDA accelerated version. Being a fan of the KISS principle from design and engineering (Keep It Simple Stupid) and aiming to avoid unnecessary complexity, I've chosen to cudafy Kevin Beason's[smallpt](http://www.kevinbeason.com/smallpt/), the most basic but still fully functional CPU path tracer around. It's a very short piece of code that doesn't require the user to install any tedious libraries to compile the code (apart from Nvidia's CUDA Toolkit).
The full CPU version of smallpt can be found at

[http://www.kevinbeason.com/smallpt/](http://www.kevinbeason.com/smallpt/)Due to its compactness the code is not very easy to read, but fortunately David Cline made[a great Powerpoint presentation](https://drive.google.com/file/d/0B8g97JkuSSBwUENiWTJXeGtTOHFmSm51UC01YWtCZw/view)explaining what each line in smallpt is doing with references to Peter Shirley's "Realistic Ray Tracing" book.
To keep things simple and free of needless clutter, I've stripped out the code for the tent filter, supersampling, Russian Roulette and the material BRDFs for reflective and refractive materials, leaving only the diffuse BRDF. The 3D vector class from smallpt is replaced by CUDA's own built-in float3 type (built-in CUDA types are more efficient due to automatic memory alignment) which has the same linear algebra math functions as a vector such as addition, subtraction, multiplication, normalize, length, dot product and cross product. For reasons of code clarity, there is no error checking when initialising CUDA. To compile the code, save the code in a file with ".cu" file extension and follow these


After reading the


So without further ado, here's the full CUDA code (also on Github at

[CUDA installation guides](http://docs.nvidia.com/cuda/)to install[Nvidia's GPU Computing Toolkit](https://developer.nvidia.com/cuda-toolkit)and configure the programming tools to work with CUDA.After reading the

[slides](https://docs.google.com/open?id=0B8g97JkuSSBwUENiWTJXeGtTOHFmSm51UC01YWtCZw)from David Cline, the commented code below should speak for itself, but feel free to drop me a comment below if some things are still not clear.So without further ado, here's the full CUDA code (also on Github at

[https://github.com/straaljager/GPU-path-tracing-tutorial-1](https://github.com/straaljager/GPU-path-tracing-tutorial-1)):
Optionally, the following 3D vector algebra functions can be inserted at the top of the file instead of #including "cutil_math.h". Instead of creating a Vector3D class (with 3 floats), CUDA's built-in float3 type is used instead as built-in types have automated memory alignment and provide higher for performance. The "__host__ __device__" keywords in front of the functions allow them to run on both the CPU and GPU.

// 3D vector algebra from cutil_math.h /*DEVICE_BUILTIN*/ struct float3 {float x, y, z;}; typedef struct float3 float3; // add inline __host__ __device__ float3 operator+(float3 a, float3 b){return make_float3(a.x + b.x, a.y + b.y, a.z + b.z);} inline __host__ __device__ void operator+=(float3 &a, float3 b){a.x += b.x; a.y += b.y; a.z += b.z;} inline __host__ __device__ float3 operator+(float3 a, float b){return make_float3(a.x + b, a.y + b, a.z + b);} inline __host__ __device__ float3 operator+(float b, float3 a){return make_float3(b + a.x, b + a.y, b + a.z);} inline __host__ __device__ void operator+=(float3 &a, float b){a.x += b; a.y += b; a.z += b;} // subtract inline __host__ __device__ float3 operator-(float3 a, float3 b){return make_float3(a.x - b.x, a.y - b.y, a.z - b.z);} inline __host__ __device__ void operator-=(float3 &a, float3 b){a.x -= b.x; a.y -= b.y; a.z -= b.z;} inline __host__ __device__ float3 operator-(float3 a, float b){return make_float3(a.x - b, a.y - b, a.z - b);} inline __host__ __device__ float3 operator-(float b, float3 a){return make_float3(b - a.x, b - a.y, b - a.z);} inline __host__ __device__ void operator-=(float3 &a, float b){a.x -= b; a.y -= b; a.z -= b;} // multiply inline __host__ __device__ float3 operator*(float3 a, float3 b){return make_float3(a.x * b.x, a.y * b.y, a.z * b.z);} inline __host__ __device__ void operator*=(float3 &a, float3 b){a.x *= b.x; a.y *= b.y; a.z *= b.z;} inline __host__ __device__ float3 operator*(float3 a, float b){return make_float3(a.x * b, a.y * b, a.z * b);} inline __host__ __device__ float3 operator*(float b, float3 a){return make_float3(b * a.x, b * a.y, b * a.z);} inline __host__ __device__ void operator*=(float3 &a, float b){a.x *= b; a.y *= b; a.z *= b;} // divide inline __host__ __device__ float3 operator/(float3 a, float3 b){return make_float3(a.x / b.x, a.y / b.y, a.z / b.z);} inline __host__ __device__ void operator/=(float3 &a, float3 b){a.x /= b.x; a.y /= b.y; a.z /= b.z;} inline __host__ __device__ float3 operator/(float3 a, float b){return make_float3(a.x / b, a.y / b, a.z / b);} inline __host__ __device__ void operator/=(float3 &a, float b){a.x /= b; a.y /= b; a.z /= b;} inline __host__ __device__ float3 operator/(float b, float3 a){return make_float3(b / a.x, b / a.y, b / a.z);} // min inline __host__ __device__ float3 fminf(float3 a, float3 b){return make_float3(fminf(a.x, b.x), fminf(a.y, b.y), fminf(a.z, b.z));} // max inline __host__ __device__ float3 fmaxf(float3 a, float3 b){return make_float3(fmaxf(a.x, b.x), fmaxf(a.y, b.y), fmaxf(a.z, b.z));} // lerp inline __device__ __host__ float3 lerp(float3 a, float3 b, float t){return a + t*(b - a);} // clamp value v between a and b inline __device__ __host__ float clamp(float f, float a, float b){return fmaxf(a, fminf(f, b));} inline __device__ __host__ float3 clamp(float3 v, float a, float b){return make_float3(clamp(v.x, a, b), clamp(v.y, a, b), clamp(v.z, a, b));} inline __device__ __host__ float3 clamp(float3 v, float3 a, float3 b){return make_float3(clamp(v.x, a.x, b.x), clamp(v.y, a.y, b.y), clamp(v.z, a.z, b.z));} // dot product inline __host__ __device__ float dot(float3 a, float3 b){return a.x * b.x + a.y * b.y + a.z * b.z;} // length inline __host__ __device__ float length(float3 v){return sqrtf(dot(v, v));} // normalize inline __host__ __device__ float3 normalize(float3 v){float invLen = rsqrtf(dot(v, v));return v * invLen;} // floor inline __host__ __device__ float3 floorf(float3 v){return make_float3(floorf(v.x), floorf(v.y), floorf(v.z));} // frac inline __host__ __device__ float fracf(float v){return v - floorf(v);} inline __host__ __device__ float3 fracf(float3 v){return make_float3(fracf(v.x), fracf(v.y), fracf(v.z));} // fmod inline __host__ __device__ float3 fmodf(float3 a, float3 b){return make_float3(fmodf(a.x, b.x), fmodf(a.y, b.y), fmodf(a.z, b.z));} // absolute value inline __host__ __device__ float3 fabs(float3 v){return make_float3(fabs(v.x), fabs(v.y), fabs(v.z));} // reflect //returns reflection of incident ray I around surface normal N // N should be normalized, reflected vector's length is equal to length of I inline __host__ __device__ float3 reflect(float3 i, float3 n){return i - 2.0f * n * dot(n, i);} // cross product inline __host__ __device__ float3 cross(float3 a, float3 b){return make_float3(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x);}

Full code on Github:

[https://github.com/straaljager/GPU-path-tracing-with-CUDA-tutorial-1](https://github.com/straaljager/GPU-path-tracing-with-CUDA-tutorial-1)

In this example, it's pretty easy to turn C/C++ code into CUDA code (CUDA is a subset of the C language). The differences with the CPU version of smallpt are as follows:

- smallpt's 3D Vector struct is replaced by CUDA's built-in
**float3**type (linear algebra vector functions for float3 are defined in cutil_math.h) - CUDA specific keyword
**__device__**before functions that should run on the GPU and are only callable from the GPU - CUDA specific keyword
**__global__**in front of the kernel that is called from the host (CPU) and which runs in parallel on all CUDA threads - a custom random number generator that runs on the GPU
- as GPUs don't handle recursion well, the radiance function needs to be converted from a recursive function to an iterative function (see
[Richie Sam's blogpost](http://richiesams.blogspot.co.nz/2015/04/making-our-first-pretty-picture.html)or[Karl Li's slides](http://cis565-fall-2012.github.io/lectures/09-24-Physically-Based-Shading-and-Pathtracing.pdf)for more details) with a fixed number of bounces (Russian roulette could be implemented here to terminate paths with a certain probability, but I took it out for simplicity) - in a CPU raytracer, you loop over each pixel of the image with two nested loops (one for image rows and one for image columns). On the GPU the loops are replaced by a kernel which runs for each pixel in parallel. A global thread index is computed instead from the grid dimensions, block dimensions and local thread index. See
[http://www.3dgep.com/introduction-to-cuda-using-visual-studio-2008/](http://www.3dgep.com/introduction-to-cuda-using-visual-studio-2008/)for more details - the main() function calls CUDA specific functions to allocate memory on the CUDA device (cudaMalloc()), launch the CUDA kernel using the "<<< grid, block >>>" syntax and copy the results (in this case the rendered image) from the GPU back to the CPU, where the image is saved in PPM format (a supersimple image format)

When running the code above, we get the following image (1024 samples per pixel, brute force path tracing):

Path traced color bleeding rendered entirely on the GPU! On my laptop's GPU (Geforce 840M) it renders about 24x faster than the multithreaded CPU version (laptop Core-i7 clocked at 2.00 Ghz). The neat thing here is that it only took about 100 lines (if you take out the comments) to get path tracing working on the GPU. The beauty lies in its simplicity.

Even though the path tracing code already works well, it is actually very unoptimized and there are many techniques to speed it up:

**explicit light sampling**(or next event estimation): sample the light source directly instead of using brute force path tracing. This makes an enormous difference in reducing noise.**jittered sampling**(also called stratified sampling): instead of sampling a pixel randomly, divide the pixel up into a number of layers (strata) in which random sampling is performed. According to Peter Shirley's book this way of sampling (which is partly structured and partly random) is one of the most important noise reduction methods- better random number generators
- various
**importance sampling**strategies: this code already performs cosine weighted importance sampling for diffuse rays, favouring rays with directions that are closer to the normal (as they contribute more to the final image). See[http://www.rorydriscoll.com/2009/01/07/better-sampling/](http://www.rorydriscoll.com/2009/01/07/better-sampling/). - ray tracing
**acceleration structures**: kd-trees, octrees, grids, bounding volume hierarchies provide massive speedups

GPU specific optimisations (see

[http://www.3dgep.com/optimizing-cuda-applications/](http://www.3dgep.com/optimizing-cuda-applications/)and Karl Li's course slides linked below):- using shared memory and registers whenever possible is many times faster than using global/local memory
- memory alignment for coalesced reads from GPU memory
- thread compaction: since CUDA launches a kernel in groups of 32 threads in parallel ("warps"), threads taking different code paths can give rise to thread divergence which reduces the GPU's occupancy. Thread compaction aims to mitigate the effects of thread divergence by bundling threads following similar code paths

I plan to cover the following topics (with CUDA implementations) in upcoming tutorials whenever I find some time:

- an interactive viewport camera with progressive rendering,
- textures (and bump mapping),
- environment lighting,
- acceleration structures,
- triangles and triangle meshes
- building more advanced features on top of
[Aila and Laine's GPU ray tracing framework](https://code.google.com/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)which is also used by Blender's Cycles GPU renderer - dissecting some code snippets from Cycles GPU render or SmallLuxGPU

References used:

[smallpt](http://www.kevinbeason.com/smallpt/)by Kevin Beason[line-for-line explanation of smallpt code](https://drive.google.com/file/d/0B8g97JkuSSBwUENiWTJXeGtTOHFmSm51UC01YWtCZw/view)by David Cline- "Realistic Ray Tracing" book by Peter Shirley
[Scratch-a-Pixel](http://www.scratchapixel.com/): excellent online rendering tutorials (ray tracing and rasterisation)[tokaspt](https://code.google.com/p/tokaspt/): a very fast CUDA path tracer by Thierry Berger Perrin (renders only spheres)- CUDA path tracing tutorial on
[RichieSams blog](http://richiesams.blogspot.co.nz/2015/04/making-our-first-pretty-picture.html) [Raytracer in Rust](https://github.com/gz/rust-raytracer)[Triers CUDA ray tracing tutorial](http://cg.alexandra.dk/?p=278)[Real-time CUDA raytracer](http://users.softlab.ntua.gr/~ttsiod/cudarenderer-BVH.html)(triangle meshes and BVH acceleration structure) by Thanassis Tsiodras[A simple real-time ray tracer in CUDA and OpenGL](http://www.igorsevo.com/Article.aspx?article=A+simple+real-time+raytracer+in+CUDA+and+OpenGL)tutorial (+ code) by Igor Sevo[CUDA path tracer](https://github.com/peterkutz/GPUPathTracer)by Peter Kutz and Karl Li- UPenn CUDA path tracing course by Yining Karl Li:
[part 1](http://cis565-fall-2012.github.io/lectures/09-24-Physically-Based-Shading-and-Pathtracing.pdf),[part 2](http://cis565-fall-2012.github.io/lectures/10-03-Physically-Based-Shading-and-Pathtracing-2-of-2.pdf),[GitHub code project](https://github.com/CIS565-Fall-2015/Project3-CUDA-Path-Tracer) [University of Pennsylvania GPU Programming and Architecture course](https://github.com/CIS565-Fall-2015/cis565-fall-2015.github.io): excellent beginner to advanced level course to learn CUDA, path tracing in CUDA, CUDA optimisation and pitfalls, performance profiling with NSight[CUDA programming and optimisation tutorials](http://www.3dgep.com/category/cuda/)[CUDA optimisation](http://gpgpu.org/static/sc2007/SC07_CUDA_5_Optimization_Harris.pdf)

## 30 comments:

Nice!

Hey, what's the current status of real-time ray tracing? Is good-looking real-time ray-tracing possible on current top GPUs?

Since your main target is high-performance path-tracing (an MP3 of real rendering), you should invest as much money in improving ECL gate speed (bipolar transistors are already near-perfect since they are inherently superior to field-effect ones), this hugely imports. Performance losses due to the speed of light limit estimate even microseconds per integrated circuit. Thus, as you increase the number of components, the losses are also increased. However, that does not mean that CISC-RISC hardware translator, caches, multithreading, superscalarity, pipelining, out-of-order execution, etc., are clever solutions. The memories cannot get faster otherwise than they get more advanced basis in the form of a faster logic.

Don't worry. ECL is at least four times as fast. Today.

Shrinking transistors will come to end yet very soon and performance increase will simply stop (well, for you exactly). Have fun.

Jensen - most guys here are software guys, can you explain why ECL would be justified in consumer PCs with its power envelope?

Seems like you took me for that Jensen of Nvidia, although we were born the same day, perhaps we are even more alike. However, thanks for the question.








The answer is :

1} from approx. 500 MHz on, CMOS power dissipation is becoming ever higher than ECL ;

2} sufficiently low-power bipolar transistors have been around for twenty years now .

Jenson: It doesn't seem like anyone has anything to say about using ECL on modern computers, from searching Google. There must be some reason people aren't using that technology, if it is indeed so much faster than CMOS. Why is nobody using it or talking about it?

This is not my opinion, but is quite interesting:


'IC manufacturers continue to announce new generations, 45 nanometer, 32 nanometer, 22 nanometer, and coming soon, 14 nanometer, though in fact we have been stuck at 64 nanometer for quite some time. There have been process improvements, but these are incremental improvements. The line pitch remains 64 nanometers. We cannot actually build circuits smaller than we could eight years ago. That these are improvements is no lie, but to label them by a size is a lie. If they had said “second generation 64 nanometer” instead of “45 nanometer”, if they had said “third generation 64 nanometer instead of “32 nanometer”, then they would have been speaking truth, or at least speaking hype rather than lies.'

No, actually, it's still in extensive use where speed is crucial, formally with a solo supplier. Why it's not considered to be used even by IBM is that once it was unable to compete with CMOS in terms of manufacturing costs, but Intel with its InGaAs initiative just will show what is truly expensive.

Now, since the speed of light limits the performance of integrated circuits, logically the ideal for gate speed would be almost 10^-44 a second, that is finite, which is good. Current state is -10. If they could be capable of reducing this gap, then you might get a rendering capability superior to path-tracing.

Many thanks for producing this code - I look forward to the remaining blog posts you have planned. However, I am struggling to get the code above compiling. The math util class has been removed from the latest version of cuda (7.5). I am unfamiliar with CUDA and have looked around but finding myself reimplementing the math functions. Do you know what libraries/function calls we can use with the latest version of cuda?

Anon: thanks! Yes, cutil_math has been removed from later versions of the CUDA toolkit (it's from the CUDA SDK samples in the toolkit versions released before 2010), but you can still find the file here: http://bullet.googlecode.com/svn/trunk/Extras/CUDA/cutil_math.h (or http://www.icmc.usp.br/~castelo/CUDA/common/inc/cutil_math.h since Google code is about to go the way of the dodo soon). To make things easier to compile, I'll build the next tutorial using the CUDA 7.5 toolkit (CUDA 6.5 has some nonsensical bug when using sqrt()).




You can also have a look at thttp://www.3dgep.com/introduction-to-cuda-using-visual-studio-2008/, to set up your environment variables in Visual Studio to work with CUDA. Or the "Getting Started with CUDA" guide on Nvidia's own website: https://developer.nvidia.com/how-to-cuda-c-cpp

Let me know if you still have trouble compiling and I'll take a look.

Btw, I've updated the code in the post and it should run twice as fast as before, mainly by scheduling more blocks/CUDA threads (with dim3 block). It's about 40x faster than the multithreaded CPU version now and I'm sure I can get even more speed. The cool thing about GPUs is that their performance is so unpredictable and occasionally mind blowing (more often than not actually).

To everyone posting about Brigade, I've removed your comments as the engine is no longer relevant to this blog.




If you want to know more about the technology, visit:

http://www.hindawi.com/journals/ijcgt/2013/578269/

or check out this thesis: http://arauna2.nhtv.nl/files/thesis_jbikker.pdf

Brigade not relevant to your blog?? Sure, why would it be? It's only a real time path tracer that you advertized as (one of) the best in your past posts. I don't know what beef you have with Otoy or the Brigade team which led you to leave Otoy, but your disregard of Brigade that stands like the elefant in the room significantly impairs the quality of your blog.

Jey Hey: nice metaphor :) just to clarify, there are no more updates on Brigade because I stopped working on it about two years ago (my last post about it, "Le Brigade nouveau est arrivé" dates from October 2013).

this is very cool..it looks like raytrace in real time...it is just a mod. jesus



http://imgur.com/a/ib8nW#nnn

Hey it seems Imagination Tech has finally something to show (in Tokyo).





http://www.4gamer.net/games/144/G014402/20151117095/

Here are some videos :

https://www.youtube.com/watch?v=A0keJiuEKdg

https://www.youtube.com/watch?v=NGWKcpJOdLk

https://www.youtube.com/watch?v=hsOuj3V4Adw

I found out that Samsung explores something similar for their mobile gpu´s.

http://dl.acm.org/citation.cfm?id=2818442

Is this kind of technology useful for desktop too or obsolete because of new

features like mixed precision ?

raul: those are probably the best real-time graphics I've seen. The colour bleeding on the characters looks really nice as well. I wonder how well it holds up in motion.


CPFUUU: nice find, thanks for the links. What ImgTec is showing in these videos looks more like Whitted ray tracing to me, something which could be done in real-time about ten years ago on a hefty PC. Current game engines like Frostbite and Unreal Engine 4 can produce a much higher level of realism, so I doubt they're going to convince many game devs to switch to ray tracing with these videos. They need to show something that actually looks substantially better than what can be done already.

Thanks for starting this series, Sam! When I was in high school, after learning about projections and rotations in Algebra class, I made a triangle mesh viewer (just wireframes). I kind of always wanted to learn more about rendering techniques, so these posts will be very helpful.








I programmed with Cuda a bit a number of years ago, but haven't used Cuda recently, so I was happy you posted the links for the set-up process in Visual Studio.

Some notes to other beginners:

* If you use the 3dgep.com link to figure out how to configure Visual Studio and start projects, note that copying and pasting the additional libraries directory for the linker will (at least in some cases--it did for me) copy things that look like quotation marks, but are not parsed by Visual Studio correctly. To avoid annoying errors and frustration, just type the quotation marks manually and cudart.lib should be findable.

* If you copy the code that replaces cutil_math.h, note that the float3 bits (struct float3 ... and typedef struct float3 float3) lines aren't needed, and the first line can actually cause errors. Just comment them out.

* Irfanview and XnView are two (of probably very many) free programs that can open the ppm images created in this post.

* When you start to get curious about changing dimensions and sample sizes, execution time may increase and you may get messages like: "Display driver stopped responding and has recovered." This has to do with a watchdog timeout timer (set with a default of 2 s). You may have to modify your registry in Windows to avoid this problem... (Search for TdrDelay)

Thanks Peter. At some point I will rewrite this tutorial and make a step-by-step guide, so even people with minimal or no programming experience can get started with GPU path tracing, a bit like what Khan Academy is doing with their Rendering 101 course (https://www.khanacademy.org/partner-content/pixar/rendering/).

Running this demo on the latest CUDA 8 sdk crashes the display driver. I think it is due to the cutil_math.h shared with this demo. Instead in CUDA 5 and above the math functions are all resident in the file helper_math.h in C:\ProgramData\NVIDIA Corporation\CUDA Samples\v8.0\common\inc on Windows and /usr/local/cuda/samples/common/inc on linux. Just include that file and the demo works fine.

Hello, Samuel. Your postings are highly interesting and informative.


I've recently ported the program you wrote here to the CPU and ran some tests.

Firstly, I've noticed you don't need to normalize when you compute (float3 u)

and (float3 d) inside the radiance function, as the vectors are already normalized,

and the image is the same either way.

Secondly, If I return (0,0,0), when a ray doesn't intersect the scene, the

image looks weird, so instead of "return make_float3(0, 0, 0) // if miss, return black"

I return accucolor instead.

Thirdly, the offset 0.05f is a bit too high for me (artifacts around sphere-sphere intersections appear), so I just set it to 0.0001f.

That's about it.

Thanks for your wonderful post.

Kamil, a couple of things you could try (asuming you have an Nvidia card):


- make sure you compile the code in Release mode

- reduce the number of samples or turn off Windows watchdog, it crashes the Nvidia driver after 10 seconds of inactivity

- make all the spheres in the scene emissive

Hello Sam! I've got the same problem as Kamil's, and with reducing the number of samples, I can get the correct result.

You said "turn off windows watchdog", I googled a lot but still don't know how to do that. So what does the "watchdog" mean?

Thanks for your wonderful posts!

Hello Sam! I've got the same problem as Kamil's, and with reducing the number of samples, I can get the correct result.

You said "turn off windows watchdog", I googled a lot but still don't know how to do that. So what does the "watchdog" mean?

Thanks for your wonderful posts!

Hi Berry, this thread may help: http://stackoverflow.com/questions/497685/cuda-apps-time-out-fail-after-several-seconds-how-to-work-around-this



The watchdog kicks in when the CUDA device (the GPU) takes more than a certain amount of time (usually 10 seconds) to return the result of a kernel:

https://devtalk.nvidia.com/default/topic/761381/cuda-programming-and-performance/this-code-crashes-the-driver-any-ideas-why-/post/4260886/#4260886

Really appreciate your fast response! I followed these intructions and added Tdr(Timeout detection) level and delay items in Registry, and it works!

Good to know :)

Yo is there a reason your spheres are not mirror textured like in Kevin's?

Post a Comment