---
title: Prepping for alpha release
url: https://etodd.io/2011/01/25/prepping-for-alpha-release/
published: '2011-01-25'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Prepping for alpha release

[These posts are now being mirrored on my [GameDev.net developer journal](http://www.gamedev.net/blog/832-et1337-makes-games/). Check out their new revamped site, it's pretty sweet.]

I am getting ready for an alpha release soon, very basic, with one tutorial level and a level editor. So looking at installer options for XNA games, this [WiX XNA installer](http://xnainstaller.codeplex.com/) appears to be the best choice. It's designed for SharpDevelop, and it creates an installer that checks for all the required libraries and even the required shader model. Unfortunately it's kind of a pain to set up. There's a massive XML file that needs a reference to *every single file* in your release.

![](../../assets/3e2473df053ff44c.jpg)


The good news is, SharpDevelop has a design utility that can generate all that for you, but it's still a little messed up. It creates one component per file, which then must be referenced by the main installation "feature". Features map to check boxes in the installer, allowing the user to install the game but not the level editor for example. With the help of Notepad++ and a few regular expressions, I can take the generated XML and turn it into component references, so the process is fairly quick. Now I just need to polish up the alpha. On a side note, I've learned that SharpDevelop is actually kinda slick.

Here's a video of me performing a speed run on a test level that demonstrates all of the moves in neat sequential order. Notice the nifty vaulting, wall-running, and swinging. It took me like 20 tries to nail this perfectly. I feel like that somehow validates this project's status as a video game at this point.