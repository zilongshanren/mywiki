---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-prepare/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The first step is to make the game create screenshots. In [X:Rebirth](http://www.egosoft.com/games/x_rebirth/info_de.php) we had already a screenshot function that could write out PNG, BMP or JPG and we had a scripting language **BUT** both were **not** connected!

So the first step was to get a bit time from the code department to have a script-command which would jump to a specific location (line 2+3) and create a screenshot (line 5) like this one:

<find_zone name=”$FindResult” macro=”macro.effectzone_macro”/>

<include_actions ref=”MergeZoneLists”/>

<append_to_list name=”$Positions” exact=”position.[-295.0m, 16.0m, 110.0m]” />

<append_to_list name=”$Rotations” exact=”rotation.[-90.0deg, -45.0deg, 0.0deg]” />

<signal_cue_instantly cue=”AddDirectory” param=”‘bait_ads.arcade2_title'”/>

The last line holds an **important** information: **AddDirectory**. You tell the script to create a new directory for every “jump-point” were it creates a screenshot. This is useful because with that you’ve all screenshots in **one** directory and you can browse through all images with any standard image viewer.

Here you see that the names can get quiet long, but that shouldn’t be a problem. Don’t think too much about the names, I’ll explain details later.

![](../../assets/b44d443db8ae9bb9.png)


The files itself are named by the game! It’s done in a way that if you sort by name you get a chronological order. By the way: The **TXT** files you see wouldn’t be necessary if you only want to compare images but they contain information like the universe-position and FPS. Why this is useful, will be explained later.

![](../../assets/b2d98758dd7c93bc.png)