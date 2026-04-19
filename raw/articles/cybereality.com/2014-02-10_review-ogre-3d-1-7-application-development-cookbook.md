---
title: 'Review: OGRE 3D 1.7 Application Development Cookbook'
url: https://cybereality.com/review-ogre-3d-1-7-application-development-cookbook/
author: Cybereality
published: '2014-02-10'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![OGRE Cookbook](../../assets/22f8506bac6e2fcd.jpg)


OGRE 3D 1.7 Application Development Cookbook by Ilya Grinblat & Alex Peterson was, I guess, what it advertised itself as; a quick cookbook of recipes using OGRE. What is was not was a good inspection of the OGRE engine itself. Really what the book amounted to was a series of short chapters, each tackling a specific programming problem. While there is nothing wrong with that, I felt like the book did not dig deep enough into the actual OGRE software and instead focused on other libraries or APIs you could combine with OGRE.

First of all, this book was heavy into MFC; nearly every chapter relied on it. I am not going to open a debate about MFC as I’m sure it will be heated. What I will say is that MFC is not supported on the free versions of Visual Studio (which is what I use) and obviously won’t work on Linux or Mac, or on mobile platforms, etc. It seems very short-sighted, and somewhat ugly, to take a great cross-platform, open-source tool and then marry it to Microsoft’s proprietary API. This also restricts the user-base significantly as now only Windows users with professional versions of Visual Studio can even run any of the samples. Huge loss here.

Aside from the MFC issue, there are actually some interesting tidbits found in the text. They show how to do basic mouse and keyboard input and move onto voice input and text-to-speech. There’s coverage of creating manual objects and using billboards, working with XML files, using lights and particle effects, scripted movement, animation, some effects like mirrors and video textures, and manipulating objects. So, yes, it does discuss a lot of key topics when working with OGRE, and from a cursory look this would seem just like what a beginner to the engine would need. However, I think the instruction would have been a lot better had they not relied on MFC.

Overall not a particularly long book, and the price was not bad for the Kindle e-book. Seeing as there are not very many books dedicated the OGRE, this is probably still worth getting if you are exploring the engine. That said, the other OGRE books I’ve read were much stronger in terms of actually focusing on the engine API itself and in a cross-platform manner.