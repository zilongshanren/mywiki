---
title: Simonschreibt.
url: https://simonschreibt.de/gat/tech-art-course/
author: Simon
published: '2022-08-13'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

# Welcome

A while ago I gave a **Tech Art Course** and another one called **3D Engines for Artists**. Here I share my materials and if you find them useful or inspiring, feel free to use them for your own teaching. Please note, that sometimes there are no long explanations on the slides or in the document because I’d have explained it verbally to the students. I taught some things for Unreal **and** Unity (e.g. Profiling). For some exercises I used the engine which was most useful (e.g. the Texture Museum was built in Unity).

💡 [My Top 3 Practical Excercises](https://simonschreibt.de#excercises)

📕 [My Document/Slides](https://simonschreibt.de#documents)

# 1. Practical Excercises

For me, the hardest (and most time-consuming) part was to come up with nice **practical exercises** to let the students explore on their own instead of me doing 8h of frontal-of-class teaching. Here are my top 3 exercises I came up with.

💡 [1.1 Real-World Rendering](https://simonschreibt.de#excercises_real_world_rendering)

💡 [1.2 Texture Museum](https://simonschreibt.de#excercises_texture_museum)

💡 [1.3 Crash the Engine!](https://simonschreibt.de#excercises_crash_the_engine)

## 1.1 Real-World Rendering

I tried to add life to the “dry” explanation of the rendering process. Before teaching them the [Render Hell](http://simonschreibt.de/gat/renderhell/), we made a practical exercise. I started by explaining different memory types (CPU Register, VRAM, RAM, HDD) and their different access speeds. To visualize that I brought differently sized plastic containers, filled them with snacks (aka “data”) and put them in different locations in the classroom (CPU register close to RAM but the HDD was far away). Different students had to move the “data” (snacks) from one container to another and of course, the person moving data from RAM to CPU Registers didn’t move because both containers were very close to each other but the person moving the snack from HDD to RAM had to run quite a lot. I wanted to show that (usually) the bigger the memory: the slower the access times.

After that, we ate all the snacks and then I explained the render process with real-world objects. For example, in the photo you see 2 people who act as vertex shader (they move vertices in form of tennis balls around).

![](../../assets/97e7ba67cb84ffb6.png)


![](../../assets/97e7ba67cb84ffb6.png)

## 1.2 Texture Museum

![](../../assets/df5715ce0ce46eb4.png)


![](../../assets/df5715ce0ce46eb4.png)

If I’d choose, this is the best of my exercises. The students visit a virtual “Museum” with textures hanging on the wall. Each texture has a problem (e.g. not power of two, way too big, flickering because mip maps are missing, …) and the students had to find the issue and fix it. Of course, I taught them about textures before I gave them the project – so they could apply their theoretical knowledge to this practical example. It was very fun to see how their detective senses kicked while investigating the textures.

📕 [Open “Texture Museum” Section in Tech Art Document](https://docs.google.com/document/d/1yas3_SnxndxK2FaEsmwl89pVV2nKPxJWaX2zuHlM8N8/edit#heading=h.ul31gzc8mpy6)

💾 [Download Texture Museum Unity Project](https://cloud.simont.de/index.php/s/JabTcjTWBP3rcMm)

I did this as a Unity Project because I wanted to use a DDS texture where I manually exchanged 1 mip map and I couldn’t find out how to load a manipulated DDS into Unreal.

## 1.3 Crash the Engine!

To get a better feeling for an engine and its limits, the students had to crash the engine or at least bring the FPS down as much as possible. They had to be creative. Some tried creating as many boxes as possible others used millions of particles and hoped to bring the engine down.

This exercise brings up interesting topics: For example, when a student wanted to import a mesh with millions of polygons, an older version of Unity split the mesh into several sub-meshes because of a maximum vertex count per mesh.

# 2. Documents

## 2.1 Tech Art Course

I created this document for me and the students as a guide and reference. The main topics are Textures, Shaders (Node Based, HLSL), Scripting (BAT, MaxScript), Performance and Profiling.

## 2.2 3D Engine for Artists

I think I’ve overdone this a bit. I wanted to give an overview of **everything** engine related to the poor students. That’s why I cover **many** different topics – too many. This course was mainly me talking and the students listening – not good. Still, maybe some of the topics or images can help you or be an inspiration for your own course.

## Thanks for Reading!

I hope you find the materials useful. Feel free to contact me if you have questions or book me if you want me to give your students/team a course.

Have a very nice day,

Simon

Huuuuuge thank you for this material!!

It looks like the courses are links and maybe I pressed them like 200 times

Do you mean, that the links did not work for you?