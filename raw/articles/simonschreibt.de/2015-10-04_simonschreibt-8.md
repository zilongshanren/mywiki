---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-take/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The first thing our program/script must do is start the game and tell it to create screenshots. For that it needs some parameters which were handed over to the wd.exe/watchdog.bat ([described here](http://simonschreibt.de/wft/watchdog-structure)).

The minimum setup for **us** looks like this:

XRebirth.exe -module effecttest -screenshotmode materials

XRebirth.exe -module ep1open -screenshotmode allzones_compass

The **modules** are the game worlds. In one case an internal test-world is loaded (effecttest) and in the other case it’s the standard game world (ep1open). The **screenshotmode** referes to the game script which actually takes the screenshots ([mentioned here](http://simonschreibt.de/wft/watchdog-take)). We’ve different game scripts for:

- capture all materials
- capture special test particle systems
- jump through all zones in the universe and take screenshots (by rotating the camera to all six sides)
- …

In fact, we’ve a lot more parameters to define because normally the game looks like this picture (left) and shall look like the right side (without UI, Cockpit, …)

![](../../assets/650f4eeaa17a0950.png)


So we add parameters to…

- …disable other ships (faster loading, no photo-bombing)
- …disable cockpit
- …disable UI
- …disable eye-adaption (to avoid different images-brightness due some post fx)
- …write a log file

The script which jumps through the universe and takes screenshots was done by [Owen Lake](https://www.linkedin.com/pub/owen-lake/10/277/ab2) and it works perfectly without any extra work.

Unfortunately it’s a totally different story for the materials! The obvious perfect solution would be that you create a test geometry like the one below and our script would overwrite the material one after another and take screenshots after every overwrite:

![](../../assets/ae8842f506693a19.png)


This wasn’t possible without additional work from a programmer so my workaround was to create a MaxScript which goes through the material library and creates such a test-geometry per material and places them in **one** scene. This scene is then of course really big and has to be manually exported after the MaxScript execution.

![](../../assets/0a3807e39d2e84b7.png)


At the same time the MaxScript would generate a XML code-block (also explained [here](http://simonschreibt.de/wft/watchdog-prepare)) for every material to tell our game to which position it has to jump to take a screenshot.

<find_zone name=”$FindResult” macro=”macro.effectzone_macro”/>

<include_actions ref=”MergeZoneLists”/>

<append_to_list name=”$Positions” exact=”position.[-295.0m, 16.0m, 110.0m]” />

<append_to_list name=”$Rotations” exact=”rotation.[-90.0deg, -45.0deg, 0.0deg]” />

<signal_cue_instantly cue=”AddDirectory” param=”‘bait_ads.arcade2_title'”/>

You can imagine that this isn’t the perfect workflow because an artist has to execute the MaxScript from time to time when new materials were added and must not forget to check-in the updated XML file. The big scene created even more problems. Read more about them in the [problem section](http://simonschreibt.de/wft/watchdog-problems).

But at least we’re done. Our program started the game and now we’ve a bunch of screenshots. It’s time to convert them!