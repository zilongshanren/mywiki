---
title: Getting Started Learning Tech Art & Unity Shader Writing
url: https://lindenreidblog.com/2019/01/30/getting-started-learning-tech-art-unity-shader-writing/
author: View all posts by Linden Reid
published: '2019-01-30'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

([important disclaimer](https://lindenreid.wordpress.com/disclaimer/): this work represents me only & not the company I work for.)

I participated in the 2019 Global Game Jam at the University of California – Irvine, and I met a ton of students who were super interested in learning about what tech art is and how to get started learning tech art related skills.

UCI Global Game Jam participants, this one’s for you. This article will be geared pretty strongly towards college students who are interested in working in the game industry and already studying a relevant major, like computer science or art. If you’re looking for more [general game industry career advice, try this article](https://lindenreid.wordpress.com/2018/02/20/how-to-start-a-career-in-games/).

I hope that you and anybody else reading this feel a little less intimidated by tech art and graphics programming and find one of these resources useful or inspiring 😀

You can always reach me on Twitter at [@so_good_lin](https://twitter.com/so_good_lin) – my DMs are open 🙂


## What is Tech Art?

I didn’t know what the tech art discipline was really about when I was in college, so don’t be intimidated if you don’t either!

[This video by Riot](https://www.youtube.com/watch?v=kr7XYXMM7-U&t=597s) does a fantastic job of covering all of the different disciplines within tech art, so I won’t bother repeating what they’ve explained so well. Basically, the term ‘tech art’ is an umbrella term for a bunch of skills and work that require both artistic and programming skills, including rigging for animations, writing tools for artists, and creating shaders for materials.

The path to becoming a tech artist is different for everybody, but generally, if you’re interested in a tech art related discipline, then like any other skill- practice it!

Try taking a variety of classes in college that relate to art and programming. And most importantly, if you’re interested in working in the game industry and you’re in college, TAKE PROJECT CLASSES in which you make games.

## Learning Shaders in Unity

The subset of tech art that I specialize in is shader writing. This job can also be a part of graphics programming, along with authoring whole rendering pipelines, but let’s focus just on the basics of writing shaders for now.

You could use any platform or engine that you want to learn shader writing, but I’ve mainly specialized in Unity in all of my hobby projects, so that’s what I can share the most resources about. I also generally recommend Unity for learning purposes in college because 1) it’s very popular, which means it’s easier to find people to collaborate with and get community support for and 2) it has both visual-based and coding-based systems for authoring shaders, so you can learn how to write shaders from different approaches based on whether you’re more interested in programming or being an artist.

If you’re more of an artist and less interested in coding, you could use Unity’s node-based shader editor, [ShaderGraph](https://blogs.unity3d.com/2018/02/27/introduction-to-shader-graph-build-your-shaders-with-a-visual-editor/). You should also experiment with the material authoring systems in whatever 3D programs you’re using.

If you want to write your own shaders in code, I highly recommend starting with [this series by Alan Zucconi](https://www.alanzucconi.com/2015/06/10/a-gentle-introduction-to-shaders-in-unity3d/) and [this series by Catlike Coding](https://catlikecoding.com/unity/tutorials/rendering/). Unity uses ShaderLab, which lets you author shaders in CG and/or HLSL, so you’ll need the [Unity graphics reference](https://docs.unity3d.com/Manual/GraphicsReference.html) and [CG](http://developer.download.nvidia.com/cg/index_stdlib.html) and [HLSL](https://docs.microsoft.com/en-us/windows/desktop/direct3dhlsl/dx-graphics-hlsl-reference) references on hand.

Unity also has a [scriptable rendering pipeline](https://blogs.unity3d.com/2018/01/31/srp-overview/) system in the works right now, so if you’re interested in working up to more advanced graphics programming techniques, you have the ability to do so (to a limited extent) in Unity. I recommend [this tutorial by Catlike Coding](https://catlikecoding.com/unity/tutorials/scriptable-render-pipeline/) to get started with Unity’s SRP. If you really want to get deep into rendering pipelines, you should learn how to write your own outside of a game engine, which is a topic for another article. (Also, you should take a graphics programming class while you’re in school!!)

Learning any kind of programming skill is all about experimentation, so here are other Unity shader resources that I love:

In addition, you’ll need some math skills for rendering. It is NOT as scary as everybody makes it sound, especially when you’re just getting started out. You can definitely get into some complicated mathematical topics in rendering, but if you just want to write shaders and/or focus on other tech art skills, don’t be too intimidated. I strongly recommend picking up the book [3D Math Primer for Graphics and Game Development](https://www.amazon.com/Primer-Graphics-Development-Wordware-Library/dp/1556229119). I also have an [article on math for shaders](https://lindenreid.wordpress.com/2018/08/25/basic-math-for-shaders/), but if you’re just getting started, I recommend reading as much of the book linked above in addition to the brief overview that article gives you.

## Fin

I hope some of the advice in this article was helpful to you! Good luck 🙂

Linden [@so_good_lin](https://twitter.com/so_good_lin)