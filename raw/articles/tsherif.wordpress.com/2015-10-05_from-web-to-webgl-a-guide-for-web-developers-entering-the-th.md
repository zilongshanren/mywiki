---
title: 'From Web to WebGL: A Guide for Web Developers Entering the Third Dimension'
url: https://tsherif.wordpress.com/2015/10/05/from-web-to-webgl-a-guide-for-web-developers-entering-the-third-dimension/
author: Tarek Sherif
published: '2015-10-05'
source_blog: Tarek Sherif
source_site: https://tsherif.wordpress.com
category: game programming
fetched: '2026-04-13'
---

WebGL is an interesting technology in that its community has brought together developers from highly disparate backgrounds. On the one hand, there are 3D graphics programmers who know the GPU architecture, the math, the algorithms, and who previously wrote their software in close-to-the-metal languages like C or C++, generally with OpenGL or D3D as the graphics API. For them, the path to WebGL involves learning the idiosyncrasies and limitations of JavaScript, as well as the best practices of working with the Web as a platform. On the other hand, there are those, like me, with a background in web development who want to use WebGL to build their sites or web applications. I should be clear here that I’m not referring to web developers who just want to get a bit of 3D into their web sites, as can be done with the myriad libraries and frameworks currently available. Rather, I’m referring to those who want to understand and use WebGL at a deep level. This, I would argue, is a far more difficult path than that taken by the graphics programmers and involves developing an understanding of the following three major areas involved in WebGL programming:

- The WebGL API: The programming model and how it models the GPU
- 3D Mathematics: Primarily linear algebra and 3D geometry
- 3D Algorithms: The various techniques used to produce images and optimize their rendering


I won’t lie. Learning all this isn’t easy. It’s been almost three years since I took over [BrainBrowser](https://brainbrowser.cbrain.mcgill.ca/) and first entered the world of 3D (here’s my first [meaningful commit](https://github.com/aces/brainbrowser/commit/8964ad2603381a0bfd7b96f05e71cd1f9b42f6f0) to the project), and I still consider myself fairly new too all this. I will say, though, that the trouble has been completely worth it. First off, it’s just fun. 3D graphics, to me, is the coolest thing you can do with a computer. You get to actually **see** your algorithms. And 3D on the Web is just an absolute blast. You can share your creations with others and easily see what others are creating. Fortunately, WebGL has inherited the Web’s culture of openness, so source code for all those creations is often readily available to learn from. Check out [Chrome Experiments](https://www.chromeexperiments.com/webgl?page=0) and [Shadertoy](https://www.shadertoy.com/) for some creative uses of WebGL that the community is sharing. And lest anyone still consider WebGL a technology only for simple demos and experiments, companies like [Sketchfab](https://sketchfab.com/), [Floored](http://www.floored.com/) and [BioDigital](https://www.biodigital.com/) (where I currently work) are showing that it’s a viable technology around which to build a business.

The reason I’m writing this post is that despite the difficulty involved, and despite the potential benefits to the WebGL community and to web development in general, I have yet to find any comprehensive guides showing the developer comfortable with standard web technologies how to become competent with WebGL. Most tutorials get you to the point where you have a flat-shaded cube spinning on the screen and leave you to figure out the rest. It’s easy go from there to some random 3D graphics texts or tutorials, find them filled with cryptic concepts and terminology, and lose hope without a clear path forward. To remedy that I’ve decided to share my own recommendations for steps to take on this difficult journey. There are some great online resources out there, but I’ll be focusing primarily on books I’ve read to get to where I am today. I feel the big conceptual shifts from web development to 3D are more easily made through focused, instructional texts. I hope this will help you avoid some of the pitfalls and frustrations I experienced along the way.

## Step 1: A Bit of Everything

[Udacity’s Interactive 3D Graphics Course](https://www.udacity.com/course/interactive-3d-graphics--cs291) with Eric Haines

This course is brilliant and was the resource that took me from seeing 3D graphics as a cryptic, esoteric field to something I felt I might be able to get a grasp on. You’ll learn about GPU architecture, basic algorithms and concepts, and a bit of math. The sessions are short videos of Eric describing concepts on a whiteboard, interspersed with quizzes and in-browser programming exercises (again, hooray for WebGL!). To keep things simple, however, it doesn’t go into the raw WebGL API, preferring to keep the low-level code wrapped up in [three.js](http://threejs.org/).

## Step 2: The API

[WebGL Programming Guide](http://www.amazon.com/WebGL-Programming-Guide-Interactive-Graphics/dp/0321902920/) by Kouichi Matsuda and Rodger Lea

This was the book that made the WebGL API itself start to make sense to me. The JavaScript code is a bit ugly to look at, but it goes over the entire set of API functions and uses them in complete examples of some interesting techniques such as render to texture and shadow mapping.

**Alternative:** The [The Learning WebGL lessons](http://learningwebgl.com/blog/?page_id=1217). These include some great examples of interesting techniques using the raw WebGL API. It doesn’t cover the entire API, and I personally found the Programming Guide easier to follow, but this is a great resource.

## Step 3: Math

[3D Math Primer for Graphics and Game Development, 2nd Edition](http://www.amazon.com/Math-Primer-Graphics-Game-Development/dp/1568817231/) by Fletcher Dunn and Ian Parberry

After enjoying math as a kid, then becoming bored with it in school, this book brought me back again. It’s a pleasure to read, written in a light, conversational style. Instead of just describing techniques for solving problems, it explains what those techniques conceptually mean, and it’s amazing what that shift in focus (compared to many other math books) did for my ability to absorb the concepts. It covers pretty much all the math you’ll need to know for 3D, while making minimal assumptions about prior knowledge. If you really don’t know any trigonometry or linear algebra, you might want to brush up elsewhere, but otherwise, you should be good to go. It also includes exercises with solutions, so you can make sure you’re understanding things properly. The only downside is that it uses Direct3D conventions (left-handed coordinate system and row vectors), so you’ll have to convert the equations carefully if you want to use them in your code.

## Step 4: Algorithms

[Interactive Computer Graphics: A Top-Down Approach with WebGL, 7th Edition](http://www.amazon.com/Interactive-Computer-Graphics-Top-Down-Approach/dp/0133574849/) by Edward Angel and Dave Shreiner

Armed with an understanding of the WebGL API and 3D math, you can now dig deeper into the algorithms covered in step 1. Here you’ll learn the details behind those techniques (and some new ones), including the math and API calls involved. This book is meant to be a university textbook, so it’s pricier and a bit drier than the other resources mentioned. The coverage of the field is excellent, though, and it’s the only book of its kind that uses WebGL.

## Step 5: Advanced Techniques and Applications

[WebGL Insights](http://www.amazon.com/WebGL-Insights-Patrick-Cozzi/dp/1498716075) edited by Patrick Cozzi

**(Full disclosure: I authored a chapter for this book.)**

After reading all that, you now have enough knowledge to start learning about the latest algorithms, techniques and applications being implemented with WebGL. WebGL Insights is a collection of short articles written by professional WebGL developers about how they’re using WebGL in the field. This will bring you up to date with the state of the art in WebGL development (as of this writing).

## Where to next?

If you’ve gotten through all that, you should be around where I am in my journey with 3D and WebGL. At this point, I can’t really guide you anymore, since I’m figuring out where to go from here too. So I’ll finish up with some random items that might help you continue on your way.

The next books on my own reading list:

[Real-Time Rendering, 3rd Edition](http://www.amazon.com/Real-Time-Rendering-Third-Tomas-Akenine-Moller/dp/1568814240/)by Tomas Akenine-Moller, Eric Haines and Naty Hoffman: I’ve heard this widely described as the best available survey of real-time rendering techniques.[Physically Based Rendering: From Theory To Implementation, 2nd Edition](http://www.amazon.com/Physically-Based-Rendering-Second-Implementation/dp/0123750792/)by Matt Pharr and Greg Humphreys: The seminal text on PBR, a shading technique based on physical principles that is becoming the de facto standard.

Some useful WebGL libraries that don’t hide too much from you:

-
[glMatrix](http://glmatrix.net/): A highly-optimized library for pretty much all the linear algebra functions you’ll need. -
[glUtils](https://github.com/tsherif/gl-utils): A little library I wrote to wrap up some of the standard boilerplate code in WebGL applications, while still requiring you to use the API directly.

Fun examples of WebGL use, in case you need inspiration:

That’s it! Best of luck, and enjoy the ride!