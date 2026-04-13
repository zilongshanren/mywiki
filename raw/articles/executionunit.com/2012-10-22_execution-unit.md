---
title: Execution Unit
url: https://www.executionunit.com/index6.html
published: '2012-10-22'
source_blog: Blog | Execution Unit
source_site: http://www.executionunit.com/blog/
category: game programming
fetched: '2026-04-13'
---

I’m working on a game where I need to generate anagrams of words. My new game engine, which is Max Astro’s engine but with a few tweeks, integrates Lua and all the game logic is in Lua.

So given a string like “chicken” I want “kcehcine” or some …

I’ve settled on using Blender 2.6 both as a level editor and modeller for my next game (code name BBM). BBM is a 2D game but modelling the characters and rendering the sprites will save a lot of time. Blender isn’t the best level editor but it …

I’m making some changes to the codebase that drives Max Astro before making my next game. The biggest change is that the engine is going to be controlled by Lua. Lua will run the main logic loop and lua will be the configuration language.

One of the oddities of …

When you create an iOS Application in XCode by default the version of the application is stored in-Info.plist. It would be really handy to get this in to code for compile time checks and #defines.

PList files are actually XML files which makes them easy to read in a …

For a few months I’ve wanted to make a clone of Spotify but I haven’t been able to justify the time. Last week I decided to take a week off and give it a go. The justification for this is that I wanted to deploy a Django website …

With the [beta](http://en.wikipedia.org/wiki/Beta_software#Beta) release of iPhone OS 4.0 Apple has changed the terms and conditions for developers who want to target the iPhone platform (note that includes the iPod Touch and iPad).

There has been a of discussion about changes to clause 3.3.1 most notably by Gruber …

## What Is Stripification?

Stripification is the process of turning lists of triangles in an arbitrary order into as many lists of triangles that contain adjacent edges. There is a great explanation of a triangle strip of wikipedia.

## Why would you stripify?

On most platforms Triangle Strips render more quickly. The …

Part of my Art pipeline for Tentacles is to import a directory of 3DS files. Each of these files is a map piece and the map pieces are instanced to create a map. That way I can store the geometry for a shack once but instance it across the level …

In OpenGL ES 2.0 glAlphaFunc isn’t available, you have to implement it in a fragment shader. There isn’t a lot of reference out there for this (not that I could find anyway) so I thought I’d write this up.

It’s actually quite simple to implement …

[Bullet](http://bulletphysics.org/wordpress/) is an open source collision and physics simulation library written by Erwin Coumans who I believe worked or maybe still does work at SCEA (Sony Computer Entertainment America). Bullet provides a C++ API to a very robust Collision, Rigid Body and Soft body simulation system. At its core Bullet …