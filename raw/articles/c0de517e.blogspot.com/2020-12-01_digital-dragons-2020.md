---
title: Digital Dragons 2020
url: http://c0de517e.blogspot.com/2020/12/digital-dragons-2020.html
published: '2020-12-01'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Open Problems in Real-Time Rendering](https://www.dropbox.com/s/0cn9t10xy8f69yz/DD-OpenProblems.pdf?dl=0)

A.k.a. Are we solving the wrong problems today? We have been looking a lot at certain bits and pieces of math, but are we looking at the -right- pieces? A reminder that math and physics don't matter, if they don't solve actual problems for people - artists, or players.

*Note: Naty Hoffman in his presentation at*

[Siggraph 2020 physically based shading course](https://blog.selfshadow.com/publications/s2020-shading-course/)makes some similar (better!) remarks while he shows how we don't know Fresnel very well... Must read!An introduction to Roblox and how its design and mission shapes the work we do to render shared worlds on almost any device, any graphics API - and how we Roblox has been achieving that for more than a decade now.

## 1 comment:

Very nice reads, especially the first one!





I'm glad to hear the conclusion about tools in particular. I think we have pretty good generic tools right now with Unity/Unreal/Godot, but when you've got a specific problem, you need a specific tool.

One example is the last game I shipped: Streets of Rage 4. It's not 3D, nor is it AAA. But that's my point: we knew exactly what we needed and we built an engine *and the editor*, and the game, in approx 2 years with a core team of 5 people, only two of us programming (helped with a third one for a short while). I do think we have one of the best 2D rendering out there, with the rimlights and reflections and everything, and it did brought the game some praise. But while I could have put the same shaders in Unity, we - as a team - would have never been able to ship it in that timeframe with Unity.

We put time on rendering because that's what makes good screenshots, that's what make people talk. But having a good toolset will lower the required budget, giving you more time to put on fancy rendering! Not to mention, being able to downsize the team makes everything, from communication to management to keeping a good vision, much much easier.

...and by good tools I'm not talking about a shiny graph editor to make custom renderpaths for a specific LOD level of a specific model. Those things shouldn't be shiny, they should be hidden and automatic. My philosophy gravitates around "less data = less bug". That means giving only the useful parameters to artists, with good default values. You don't want to scare anyone with too many options and too many strange concepts. But sadly, that's what you need when you build a generic editor like Unity or Unreal, because it needs to do

everything.Post a Comment