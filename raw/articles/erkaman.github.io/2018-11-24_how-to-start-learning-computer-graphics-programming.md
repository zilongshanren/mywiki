---
title: How to Start Learning Computer Graphics Programming
url: https://erkaman.github.io/posts/beginner_computer_graphics.html
published: '2018-11-24'
source_blog: Eric Arnebäck
source_site: https://erkaman.github.io/
category: graphics
fetched: '2026-04-19'
---

Ever since I opened up my Direct Messages and invited everyone to
ask me computer graphics related questions on
[Twitter](https://twitter.com/erkaman2),
I am very often asked the question
"How can I get started with graphics programming?".
Since I am getting tired of answering this same question over and
over again, I will in this post compile a summary of all
my advice I have regarding this question.


Quite a few API:s for coding against the GPU hardware have appeared over the years: Direct3D, OpenGL, Vulkan, Metal, WebGL, and so on. These API:s can be difficult to get started with, since they often require much boilerplate code, and I consider that they are not beginner friendly at all. In these API:s, even figuring out how to draw a single triangle is a massive undertaking for a complete beginner to graphics. Of course, an alternative is that we instead use a Game Engine like Unity and Unreal Engine. The game engine will be doing the tedious work of talking to the graphics API for you in this case. But I think that even a game engine is too much to learn for a complete beginner, and that time should be spend on something a bit simpler.

Instead, what I recommend for beginners, is that they write
themselves either a raytracer or a software rasterizer(or both!). Put it simply,
A **raytracer** is a program
that renders 3D scenes by sending out rays from every pixel in the screen,
and does a whole bunch of intersection calculations and physical lighting
calculations, in order to figure out the final color of each pixel.
A **software rasterizer**, renders 3D scenes
(which in a majority of cases is just a bunch of triangle) like this:
for every triangle we want to draw, we figure out which pixels on the screen that
triangle covers, and then for each such pixel, we calculate how the light
interacts with the point on the triangle that corresponds to the pixel.
From this light interaction calculation, we obtain the final color of the pixel.
Rasterization is much faster than raytracing, and it is the algorithm that
modern GPU:s uses for drawing 3D scenes. And software rasterization, simply
means that we are doing this rasterization on the CPU, instead of the GPU.

Both rasterization and raytracing are actually two pretty simple algorithms, and it is much easier for a beginner to implement these, than it is to figure out modern graphics API:s. Furthermore, by implementing one or both of these, the beginner will be introduced to many concepts that are fundamental to computer graphics, like dot products, cross products, transformation matrices, cameras, and so on, without having to waste time wrestling with modern graphics API:s. I believe that these frustrating graphics API:s turn off a lot of beginners from graphics, and making your first computer graphics project into a rasterizer or a raytracer is a good way of getting around this initial hurdle.

Note that one large advantage to writing a software rasterizer before learning a graphics API, is that it becomes much easier to debug things when things inevitably go wrong somewhere, since these API:s basically just provide an interface to a GPU-based rasterizer(note to pedantics: yes,this is a great simplification, since they provides access to things like computer shaders as well). Since you know how these API:s work behind the scenes, it becomes much easier to debug your code.

For writing a raytracer, I always recommend reading
[Peter Shirley's books](https://twitter.com/peter_shirley/status/984947257035243520?lang=da).
For writing a software rasterizer, see these resources:
[1](https://www.scratchapixel.com/lessons/3d-basic-rendering/rasterization-practical-implementation),
[2](https://github.com/ssloy/tinyrenderer),
[3](https://tayfunkayhan.wordpress.com/2018/11/24/rasterization-in-one-weekend-part-i/),
[4](http://www.gabrielgambetta.com/computer-graphics-from-scratch/introduction.html).

My next advice is that you should study the math you need for computer graphics. The number of math concepts and techniques I use in my day-to-day work as a graphics programmer is surprisingly small, so this is not as much work as you might think. When you are a beginner in graphics, a field of mathematics called 'linear algebra' will be your main tool of choice. The concepts from linear algebra that you will mostly be using are listed below

From the beginner to intermediate level, you will mostly not encounter any other math than the above. Once you get into topics like physically based shading, a field of mathematics called 'calculus' also becomes useful, but that is a story for another day :-).

I will list some resources for learning linear algebra.
A good online mathbook on the topic is
[immersive linear algebra](http://immersivemath.com/ila/index.html).
A good video series on the topic that allows you to visualize many concepts is
[
Essence of linear algebra](https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab).
Also, [this OpenGL tutorial](https://learnopengl.com/Getting-started/Transformations) has useful explanations of elementary, yet useful
linear algebra concepts. Another resource is
[The Graphics Codex](http://graphicscodex.com/).


Once you have written a raytracer or rasterizer, you will feel more confident in learning a graphics API. The hello world of learning a graphics API is to simply draw a triangle on the screen. It can actually be surprisingly difficult to draw your first triangle, since usually a large amount of boilerplate is necessary, and debugging graphics code tends to be difficult for beginners. In case you have problems with drawing your first triangle, and is getting a black screen instead of a triangle, I will list some debugging advice below. It is a summary of the steps I usually go through when I run into the same issue.


In my view, the best way to become good at graphics, is to work on implementing various rendering techniques by yourself. I will below give a list of suggestions of projects that a beginner can implement and learn from.

And here are also some more advanced techniques:

And this concludes the article. So that was all the advice I had offer on this topic.