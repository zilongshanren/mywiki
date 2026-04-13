---
title: Reloading, shadow mapping
url: https://etodd.io/2010/01/09/reloading-shadow-mapping/
published: '2010-01-09'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Reloading, shadow mapping

Thanks to the Panda3D 1.7.0 shader generator supporting shadow mapping, and the awesome new BuildBot service set up on the Panda3D website, A3P now supports basic shadow mapping! Actually, the sun is just implemented as a giant spotlight with a 2048x2048 shadow buffer. Definitely not the most efficient or high-quality method, but certainly the easiest, and the results are acceptable.

Also new in SVN is a reloading mechanic. The shotgun, chaingun, and sniper rifle all have to be reloaded, with varying clip sizes and reload times. Of course, reloading units are highlighted as vulnerable, and they also beep furiously to make it perfectly clear they need to be shot at.

Weapons in general have been made more deadly; it's now possible to get a "headshot" with the sniper rifle by hitting a droid directly in the center, resulting in instant death. The melee claw (not the saw blade) is also instant death now, although its range has been decreased, and other weapons are unusable while it's active.

And the obligatory screenie: