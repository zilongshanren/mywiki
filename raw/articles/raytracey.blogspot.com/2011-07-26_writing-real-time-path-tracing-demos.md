---
title: Writing real-time path tracing demos
url: http://raytracey.blogspot.com/2011/07/writing-real-time-path-tracing-demos.html
author: Sam Lapere
published: '2011-07-26'
source_blog: Ray Tracey's blog
source_site: http://raytracey.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Several readers of this blog (woohoo I've got readers ;-) have asked me what skills you need to learn to make the demos that I've posted. To those, I want to give some C++ pointers (pun intended) in this post.

Six months ago, I didn't know anything about programming (let alone C++). After seeing some amazing real-time path tracing demos on the net (like Jacco Bikker's Brigade), I wanted to write my own stuff because I had some ideas that I wanted to see materialized (such as the Pong game for which I got the help from Kerrash, a programmer with CUDA experience). I didn't want to be too dependent on other programmers so I decided to learn C++ on my own in my spare time. I've read some C++ tutorials on the net and some excellent books that have been a great help in understanding the C++ language and writing your own programs. This is the list of books and websites that I've read:

- "Beginning programming with C++ for Dummies", an excellent beginner's book, easy to read, explains the concept of object-oriented programming very well

- "C++ without Fear", another great book, which delves deeper into the basics than the first book and also discusses code optimization

- tutorials on

[www.learncpp.com](http://www.learncpp.com/), this is a great website with lots of small Q&A's, and also discusses smaller subjects like enums- "Practical C++ Programming", this is a little bit harder than the first two books (especially the exercises)

Other books that were recommended by others (that I haven't read yet):

- "Thinking in C++"

- "Accelerated C++"

- "Effective C++"

Reading these books and doing the exercises with perseverance, I slowly got a hold on the C++ language. Frankly I'm amazed that the language becomes almost second nature so quickly. I'm still getting compiler errors that I don't understand, but luckily there is Google, which quickly solves the problem in most cases.

In order to write a real-time path tracing demo, learning C++ is not enough. Some basic knowledge about ray tracing and path tracing is necessary as well. "Realistic Ray Tracing" by Shirley is an excellent resource for this. There are also lots of powerpoint presentations about ray tracing and Monte Carlo rendering on the net.

Not having the patience to reinvent the wheel of real-time path tracing, I wanted to base my path tracing demos on existing open source code that I knew was ultrafast and ultra-efficient. So I did some research on the net. This is what I came up with:

-

[, ultra-fast CUDA path tracing code by Timo Aila and Samuli Laine](http://code.google.com/p/understanding-the-efficiency-of-ray-traversal-on-gpus/)**Understanding the Efficiency of Ray Traversal on GPUs**-

[, a real-time CUDA path tracer by Jacco Bikker and Jeroen van Schijndel, very well optimized](http://igad.nhtv.nl/~bikker/files/kajiya_src.zip)**Kajiya demo**-

[, another real-time CUDA path tracer by Jacco Bikker, this is an](http://igad.nhtv.nl/~bikker/files/Simplex%20Paternitas%20src.rar)**Simplex Paternitas****excellent**starting point for learning to write new code and add new objects and animations (and see the results immediately). You don't have to touch the CUDA part of the code (although it's quite easy to understand once you're familiar with C++). Every frame, all the framedata is passed from C++ to CUDA, so you only need to know C++ to write new animations and to add a physics library like Bullet Physics.Adding the Bullet Physics library to the code (as shown in

[my latest demo](http://www.youtube.com/watch?v=8nftCY4ZYH4)) and learning the Bullet API was actually not so difficult in retrospect (the Hello World example included in the Bullet SDK was very helpful in this respect). Right now, I'm incorporating the vehicle physics from the Bullet SDK into the Futuristic Buildings demo (which is based on the code framework of the Simplex Paternitas demo). It's kinda working right now, but I won't make a vid until I'm satisfied. The AABB hitboxes for the car and buildings are almost working as well (after identifying which variable triggered the ray shooting functions using the hitboxes).To summarize, learning the basics of C++ is a must. You have to invest some time in it (it took me about 3 months of learning in my spare time to get a good grasp on the basics and an additional month to read and understand someone else's code and adding own stuff). Understanding the structure of a program (which functions call other functions, which loop is the control flow entering, what stuff has to be initialized before rendering the first frame, how are variables efficiently shared between files, ...) is extremely important. From that point, you'll need creativity and perseverance to make an interesting demo and the possibilities will only be limited by imagination. A cool idea would be

## 4 comments:

I love your blog and i am a regular reader. I find it amusing that you referred my 1000 keva plank video. since i have learnt a lot from you.


here is another one that is actually the same scene but a different angle, materials and lightning

http://youtu.be/-73RlwwIfvY

Thanks very much, I appreciate your comment very much!



That's an awesome video, this kind of physics simulations inspires me to make new demos :)

I hope to unveil some new demos soon ;)

i have a question does path tracing requires that you compare your ray with every single triangle in the scene ?

Post a Comment