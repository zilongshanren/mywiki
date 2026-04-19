---
title: LD code into the Frank project
url: https://claire-blackshaw.com/blog/2010/04/ld-code-into-the-frank-project/
author: Claire Blackshaw
published: '2010-04-25'
source_blog: 'Claire Blackshaw: Claire Blackshaw'
source_site: https://claire-blackshaw.com/
category: graphics
fetched: '2026-04-19'
---

![LD code into the Frank project](../../assets/44c5e4449440aaff.jpg)

Right I’ve moved over most the nice LD code into the Frank project, cleaned up a few things here and there. Made it play nice with the World Manager system.

First thing I did after getting the camera controls in was apply the debug renderer to the stupid animation problem I’m having. Now to clarify both the Worm and Hand have translation and scale applied. In every way other than complexity they are the same.

As you see the hand bones are in the correct place. What you are seeing are the World Transforms which then are multiplied by the Inverse Bind Pose before being based to the shader. So the job is to narrow it down as follows, I’ve eliminated the ~~strike-out~~ words.

- Data
- Art in Max
- Exportor

- Code
- Content Processor
- Setup of Bind Pose & Inverse
~~Animation of Bones~~~~Computation of World Transforms~~

- Shader

SVN Comments below which sums it up


- SphereHelper.cs is a Spherical Coordinate Helper class
- PolarHelper.cs does the same for Polar Coords
- A DebugRenderer component makes life easier
- New Cameras
- OrbitCamera for 1st & 3rd person Sphere Camera
- TargetCamera for tracking a node from another node

- General clean up in GameplayScreen
- Moved GameplayScreen input helper functions to InputState
- Added Some input helpers to InputState
- Cleaned up Debug Camera controls

So any clues on this animation bug?