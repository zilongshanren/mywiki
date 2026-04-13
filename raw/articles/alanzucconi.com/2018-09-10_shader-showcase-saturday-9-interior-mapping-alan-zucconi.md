---
title: 'Shader Showcase Saturday #9: Interior Mapping - Alan Zucconi'
url: https://www.alanzucconi.com/2018/09/10/shader-showcase-9/
author: Alan Zucconi
published: '2018-09-10'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

If you have been on Twitter this past week, you might have seen videos of the new [Spider-Man](https://www.playstation.com/en-us/games/marvels-spider-man-ps4/), developed by [Insomniac Games](https://twitter.com/insomniacgames). The game has been praised for its stunning visuals and exceptional attention to detail. One effect, in particular, has captured the players’ attention. It appears that you can see inside every single window of every building. But at a closer look, something does not look right. What’s going on?

The architecture in Spider-Man is some M.C. Escher shit.

[https://t.co/AKhtZUdtvQ][pic.twitter.com/yvKSfowiHV]— chris person (@Papapishu)

[September 8, 2018]


The obvious way to have rooms appearing behind windows is simply to fill each one with actual geometry. While this works for small scenes, it is unpractical for a game as large as *Spider-Man*. The cost of all those additional triangles cannot be justified, especially when only a fraction of a few rooms can be seen at any given time.

If you have been following *Shader Showcase Saturday* for the past few months, you should know by now that every problem in video games has a shader solution. And this is not an exception. This week’s Shader Showcase Saturday is dedicated to a very intriguing technique **interior mapping**.

If you landed on this page because you are only looking to implement this technique for a commercial title in Unity, I suggest having a look at [Fake Interiors FREE](https://www.assetstore.unity3d.com/#!/content/104029?aid=1100l45Ay&pubref=az_sss_09). It is a free asset that achieves the same effect seen in *Spider-Man*.

The asset was created using [Amplify Shader Editor](https://www.assetstore.unity3d.com/#!/content/68570?aid=1100l45Ay&pubref=az_sss_09), which is possibly the most advanced tools specifically designed to create shaders in Unity.

If you are interested in learning more about how interior mapping and how it can be implemented, keep reading the rest of this tutorial.

Interior Mapping was first described with the very purpose of simulating the interior of a room by [Joost van Dongen](https://twitter.com/JoostDevBlog), in his paper from 2008 titled [Interior Mapping: A new technique for rendering realistic buildings](http://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf). The author has also dedicated an entire section of his website on this topic, [Interior Mapping](http://interiormapping.oogst3d.net/), which also comes with the source code written in C++. Back in 2011, Developer [Einar Öberg](https://twitter.com/inear) ported Joost van Dongen’s solution to Unity. The source code is available on [Interior Mapping in Unity 3D](http://www.inear.se/2011/02/interior-mapping-in-unity3d/), but keep in mind that Unity has changed a lot since 2011.

## How It Works

To get a feeling of how interior mapping actually works, we can look back at *Super Mario*. Even if you have not played it yourself, you might have seen that when Mario is running, the background moves slower. This trick creates the illusion that the background is further away from the camera, adding a touch of three-dimensionality to an otherwise two-dimensional game. The technique is called **parallax**, and for many centuries has been the main tool to measure the distance of objects far away, such as mountains, planets and even stars.

Interior mapping is, at its core, a very advanced parallax effect. As a technique, parallax has been widely used in 2D games and is also implemented in many shaders. The Standard Shader introduced in Unity 5, for example, supports a feature called **Parallax** **Mapping**, which can be enabled using the [Height Map property](https://docs.unity3d.com/Manual/StandardShaderMaterialParameterHeightMap.html) of a Standard material. While the more traditional **normal mapping** only affects the lighting, parallax mapping distorts how the texture is sampled at different angles, to account for parallax. This requires a **height map**, which is a grayscale texture that indicates how distant an object is from the surface.

There are a few other ways in which the interior of a room can be simulated, especially using more sophisticated tools such as **reflection probes** and **cube maps**. This is the case of Senior Environmental Technical Artist [Alex Stroukoff](https://twitter.com/aStrkl)‘s solution (video below).

Starting to think about interior for my

[#houdini][#unity]project

standard shader with reflection probes…kinda works ![#gamedev][#unitytips][pic.twitter.com/kdExUUBgMm]— Alex Strook – SQUEAKROSS (@AlexStrook)

[May 3, 2017]

However, to reach the level of realism seen in *Spider-Man*, it is likely you will need to include some sort of parallax mapping.

## Where It Is Used

Spider-Man is obviously not the first game to have used interior mapping. *Destiny*, *Overwatch*, *Bioshock Infinite*, *Saint Row* and *Assassin Creed* are just a few examples of recent games which features this technique. Game Artist [Simon Schreibt](https://twitter.com/simonschreibt) wrote an interesting case-study on his blog, [Windows AC/Row/Infinite](https://simonschreibt.de/gat/windows-ac-row-ininite/), where it explores how the effect is used (and exploited) in many AAA titles.

It was notoriously predominant in *Sim City 5*, as it can be seen in the video below.

This shader trick comes from a 2008 paper, and was already used in Sim City 5 (visible in the GIF below), Assassins's Creed, Overwatch, etc…

It's also available for free in Unity, thank to

[@AmplifyCreates][https://t.co/iXN9FRicz0][pic.twitter.com/kHhZWB0bPI]— Tim Soret (@timsoret)

[September 5, 2018]

If you are interested more in understanding how interior mapping was implemented in Sim City 5, I highly recommend [From AAA to Indie](http://www.andrewwillmott.com/talks/from-aaa-to-indie), an insightful talk by Graphics Engineer [Andrew Willmott](https://twitter.com/andrewwillmott).

An exceptional recreation of Sim City 5’s interior mapping technique was recreated in Unity by Graphics Programmer [Ben Golus](https://twitter.com/bgolus) (video below), details of which are still accessible on the [Unity Forum](https://forum.unity.com/threads/interior-mapping.424676/#post-2751518).

Recreating SimCity 5's interior mapping technique.

[#madewithunity][pic.twitter.com/bCybfktTKh]— Ben Golus⚠️⭕ (@bgolus)

[August 14, 2016]

The work of Ben Golus and Simon Schreibt has been featured a few times before on *Shader Showcase Saturday*. If you want to learn about graphics programming and shader coding from two industry veterans, I highly suggest following them on Twitter.

If even after having access to all of these resources you prefer to rely on a professional solution for your game, an inexpensive alternative for interior mapping that does not rely on [Amplify Shader Editor](https://www.assetstore.unity3d.com/#!/content/68570?aid=1100l45Ay&pubref=az_sss_09) is [TOZ Interior Shaders](https://www.assetstore.unity3d.com/#!/content/35003?aid=1100l45Ay&pubref=az_sss_09).

## Leave a Reply Cancel reply