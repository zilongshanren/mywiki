---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/e9bcbd1679bf4db5.png)


![](../../assets/e9bcbd1679bf4db5.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

![](../../assets/a5937a3f72b8a0b3.png)


Game Development is complicated an it’s just common that mistakes happen. For example: Can you see the difference between the upper and lower screenshot below?

![](../../assets/88eff74a22b86b4a.png)


**Answer**: In the lower image the green highway tube is a bit brighter. The questions are:

![](../../assets/ebe450f92e093152.png)

**Is this intentional?**

When did it happen?

What changed (shader, material, texture, …)?

When did it happen?

What changed (shader, material, texture, …)?

[X:Rebirth](http://www.egosoft.com/games/x_rebirth/info_en.php) is a huge game and we did the material-setup in a long **XML**-file which makes it easy to change something **unintentional**. It might happen that a change like this doesn’t get noticed for a long time and it will cost much time to find the answers to the above questions.

This post is about a tool which I build together with the guys at [Egosoft](http://www.egosoft.com/). The Watchdog Script helps us to keep track of visual changes in the universe of our game.

![](../../assets/e35750e884b6f573.png)

First, it creates screenshots of our universe, materials and special test-cases **every** night.

![](../../assets/93faeab940eb79e5.png)


**Some** of the shots are automatically compared and if something changed visually a warning-mail is send out. If there was a significant FPS drop or raise a warning-mail is generated too.

![](../../assets/97575b65268f062c.png)


In addition, a (filter-able) HTML gallery is created to give a good overview about all generated screenshots to all team members.

![](../../assets/269ab316b9d7b7e6.png)


You also can see all screenshot-iterations of a specific location with more data like the position or performance information (details follow below).

**By the way**

We don’t use it **only** for checking materials! We also take pictures of (static) particle-systems and a simple cube-animation to test if these systems and their features work fine. In the image below you see tests for particle-blending, -scaling, -orientation, … – More information about what is comparable can be found [here](http://simonschreibt.de/watchdog-convert#comparable).

![](../../assets/cb64d6c8e0a6f3d0.png)


This article is about the basic structure of the script and all the problems we faced during the development. We **don’t** release source code because the script is optimized for **our** pipeline, but writing the code shouldn’t be a problem. In fact, it’s more important to have the **motivation** to invest a bit time in tools even if you can’t calculate how much time it will save you. If you’ve the will-power, the code isn’t a problem anymore.

Here you find descriptions of the different steps and challenges we took to develop the script. I can recommend reading at least the [problem section](http://simonschreibt.de/wft/watchdog-problems). It’s always fascinating how computers protect developers from boredom.

![](../../assets/6504ba5124ef9553.png)


![](../../assets/6504ba5124ef9553.png)

![](../../assets/aaefdaeb37931150.png)


![](../../assets/aaefdaeb37931150.png)

![](../../assets/f311f5e89f5f15c8.png)


![](../../assets/f311f5e89f5f15c8.png)

![](../../assets/1424be89208f43f6.png)


![](../../assets/1424be89208f43f6.png)

![](../../assets/784aa2fe2927c88e.png)


![](../../assets/784aa2fe2927c88e.png)

![](../../assets/ba6fe604e43ac1c3.png)


![](../../assets/ba6fe604e43ac1c3.png)

![](../../assets/1dac076050f8605d.png)


![](../../assets/1dac076050f8605d.png)

![](../../assets/d83c291ba36cbcbb.png)


![](../../assets/d83c291ba36cbcbb.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

![](../../assets/ba0680151067ebbc.png)

[Michael Baumgardt](https://www.linkedin.com/in/mbaumgardt)

[Owen Lake](https://www.linkedin.com/pub/owen-lake/10/277/ab2)

[Roger Boerdijk](https://www.linkedin.com/pub/roger-boerdijk/6/284/385)

[Lino Thomas](http://linolafett.deviantart.com/)

[Bernd Lehahn](https://www.linkedin.com/pub/bernd-lehahn/1/640/b42)

[ImageMagick](http://www.imagemagick.org/script/convert.php)

[t02]

[Image Comparison Tool “Perceptual Image Diff”](http://pdiff.sourceforge.net)

[t03]

[Image Comparison Tool “DiffImg”](http://thehive.xbee.net/index.php?module=pages&func=display&pageid=11#Usage)

[t04]

[Command Line Mail Program: Blat](http://www.blat.net/)

[t05]

[JQuery](https://jquery.com/)+

[LazyLoad Plugin](http://www.appelsiini.net/projects/lazyload)

[t06]

[Function for returning URL Parameters](http://stackoverflow.com/questions/11582512/how-to-get-url-parameters-with-javascript)

[t07]

[Cruise Control](http://cruisecontrol.sourceforge.net)

[a01]

[PDI/Dreamworks: “A Perceptual Metric for Production Testing”](http://pdiff.sourceforge.net/perceptual_testing-MASTER.ppt)

[r01]

[Reddit Discussion about this article](https://www.reddit.com/r/gamedev/comments/3nomvj/i_describe_a_script_which_helps_us_to_notice/)