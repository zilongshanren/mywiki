---
title: Tool For Building UE4 Dedicated Server Target.cs Files
url: https://allarsblog.com/2017/10/17/building-dedicated-server-target-files/
author: Michael Allar
published: '2017-10-17'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

In the middle of setting up a automated build server and I ran into an issue when trying to build dedicated servers for blueprint only projects. I basically needed to be able to auto-generate the `*Server.Target.cs`

file for the project if its missing.

I wrote an over engineered and bloated Node.js tool to solve this for me. It takes a project name and project path inputs and auto-writes a `*Server.Target.cs`

where it needs to be if it doesn't exist.

If you're the one other person who might need this, [it is on Github.](https://github.com/Allar/ue4-server-target-builder?ref=allarsblog.com)