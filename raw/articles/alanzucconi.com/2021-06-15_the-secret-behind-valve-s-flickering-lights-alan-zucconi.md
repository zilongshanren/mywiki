---
title: The Secret Behind Valve's Flickering Lights - Alan Zucconi
url: https://www.alanzucconi.com/2021/06/15/valve-flickering-lights/
author: Alan Zucconi
published: '2021-06-15'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This article will explore the origin of the popular flickering light effect, seen across many of their titles including “Quake”, “Half-Life”, “Half-Life: Alyx” and “Portal”. A Unity package to use this very effect can be download at the end of the article.

![](../../assets/d90698ecb6c3d371.gif)


![](../../assets/d90698ecb6c3d371.gif)

Not long ago the Internet has gone crazy upon discovering that Valve has been using exactly the same flickering effect for over 25 years. The discussion quickly [trended on Reddit](https://www.reddit.com/r/gaming/comments/nyxzme/valve_reuses_the_source_code_for_flickering/), bringing an old piece of code back from 1996.

While the code was indeed used in many Valve games, it actually predates the company. The flickering light effect was likely written by none other than John Carmack for “Quake” in 1996. That was part of a library of flickering presets compiled by John Romero in 1993 while working on “DoomED”:

- 0 : “Normal”
- 1 : “Flicker A”
- 2 : “Slow, strong pulse”
- 3 : “Candle A”
- 4 : “Fast strobe”
- 5 : “Gentle pulse”
- 6 : “Flicker B”
- 7 : “Candle B”
- 8 : “Candle C”
- 9 : “Slow strobe”
- 10: “Fluorescent flicker”
- 11: “Slow pulse, noblack”

Luckily for us, “Quake” source code was actually made available by id-Software on [their GitHub page](https://github.com/id-Software/Quake). It is thanks to that that we can find out how the flickering light effect actually works.

Before we do that, it should be noticed that a lot of “Quake” code was written in [QuakeC](https://en.wikipedia.org/wiki/QuakeC), a C-like compiled language developed exclusively to facilitate the creation of mods and content. The piece of code we are interested on is inside a function called `worldspawn`

in the file [world.qc](https://github.com/id-Software/Quake/blob/bf4ac424ce754894ac8f1dae6a3981954bc9852d/QW/progs/world.qc#L302-L345), which has the responsibility of setting up and world settings and precaching sounds.

The function initialises a light animation table, with 12 different styles. They are defined using strings: the one shown in the Reddit post is `"mmamammmmammamamaaamammma"`

, which is referred in the code as “*fluorescent flicker*“. The string represents how the brightness of the light changes over time, with `'a'`

being total darkness, `'m'`

being full brightness and `'z'`

being double brightness.

// // Setup light animation tables. 'a' is total darkness, 'z' is maxbright. // // 0 normal lightstyle(0, "m"); // 1 FLICKER (first variety) lightstyle(1, "mmnmmommommnonmmonqnmmo"); // 2 SLOW STRONG PULSE lightstyle(2, "abcdefghijklmnopqrstuvwxyzyxwvutsrqponmlkjihgfedcba"); // 3 CANDLE (first variety) lightstyle(3, "mmmmmaaaaammmmmaaaaaabcdefgabcdefg"); // 4 FAST STROBE lightstyle(4, "mamamamamama"); // 5 GENTLE PULSE 1 lightstyle(5,"jklmnopqrstuvwxyzyxwvutsrqponmlkj"); // 6 FLICKER (second variety) lightstyle(6, "nmonqnmomnmomomno"); // 7 CANDLE (second variety) lightstyle(7, "mmmaaaabcdefgmmmmaaaammmaamm"); // 8 CANDLE (third variety) lightstyle(8, "mmmaaammmaaammmabcdefaaaammmmabcdefmmmaaaa"); // 9 SLOW STROBE (fourth variety) lightstyle(9, "aaaaaaaazzzzzzzz"); // 10 FLUORESCENT FLICKER lightstyle(10, "mmamammmmammamamaaamammma"); // 11 SLOW PULSE NOT FADE TO BLACK lightstyle(11, "abcdefghijklmnopqrrqponmlkjihgfedcba"); // styles 32-62 are assigned by the light program for switchable lights // 63 testing lightstyle(63, "a");

It should be now clear what `"mmamammmmammamamaaamammma"`

does is to rapidly set the light on (`'m'`

= 100% brightness) and off (`'a'`

= 0% brightness).

The same code can literally be found in both “[Half-Life](https://github.com/ValveSoftware/halflife/blob/c7240b965743a53a29491dd49320c88eecf6257b/dlls/world.cpp#L557-L605)” and “[Half-Life 2](https://github.com/ValveSoftware/source-sdk-2013/blob/0d8dceea4310fde5706b3ce1c70609d72a38efdf/mp/src/game/server/world.cpp#L535-L565)“. And there are hints that the same presets are available in the [level editor](https://twhl.info/wiki/page/Tutorial%3A_Light#h5f9d16a8b0fc4) and even in “[Counter-Strike](https://developer.valvesoftware.com/wiki/Counter-Strike.fgd)“. Looking through “Quake” source code, it is also possible to find the function which parses those strings. It is called `R_AnimateLight`

in [r_light.c](https://github.com/id-Software/Quake/blob/bf4ac424ce754894ac8f1dae6a3981954bc9852d/QW/client/r_light.c#L33-L53):

void R_AnimateLight (void) { int i,j,k; // // light animations // 'm' is normal light, 'a' is no light, 'z' is double bright i = (int)(cl.time*10); for (j=0 ; j<MAX_LIGHTSTYLES ; j++) { if (!cl_lightstyle[j].length) { d_lightstylevalue[j] = 256; continue; } k = i % cl_lightstyle[j].length; k = cl_lightstyle[j].map[k] - 'a'; k = k*22; d_lightstylevalue[j] = k; } }

From that, we can also see that the string is parsed at 10 frames per second.

### ⭐ Recommended Unity Assets

## Download Unity Package

[Become a Patron!](https://www.patreon.com/bePatron?u=850572)

You can add these very light effects to your game, using the Unity package available on [Patreon](https://www.patreon.com/posts/52531701).

![](../../assets/dc4e6c5701b5ccf7.gif)


![](../../assets/dc4e6c5701b5ccf7.gif)

All of the above-mentioned light effects are included, with the possibility of writing your own pattern.

![](../../assets/cd11c984e698eadd.png)


![](../../assets/cd11c984e698eadd.png)

## Leave a Reply Cancel reply