---
title: AllarEngine + DX11 + HTML5?
url: https://allarsblog.com/2012/08/23/allarengine-dx11-html5/
author: Michael Allar
published: '2012-08-23'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

So in the process of researching ways to integrate web-based services into UE3 during my work on [Rekoil](http://www.rekoil.com/?ref=allarsblog.com), I came across the library [Awesomium](http://www.awesomium.com/?ref=allarsblog.com) thanks to James Tan and thought it was cool enough to add into my personal project / hobby engine I am working on arrogantly called the AllarEngine. It was quite easy to get Awesomium in and running, however I recently switched to DirectX 11 using Windows 8 and Visual Studio 2012 as my current run-time target and that required some major refactoring for both DirectX11 and just a general "why did I do it this way, I know a better way" effort. I could go on and on about this, however to keep this short, here is an image of Awesomium being rendered to a quad in screen space.