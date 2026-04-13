---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-compare/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

Comparing the shots is relatively easy. First we have to iterate over all screenshot-directories which begin with “bait_” in their name and get a list of all PNG files in that folder. It’s **important** that you receive the files ordered by date. If you made your game name the files like suggested (e.g. screen_2015-09-01_01-47-03.png) then you can sort even by name.

If there are more than **two** files (when you start the Watchdog the first time, there will only be one file until you start the 2nd run) you can take the two latest generated PNG files and hand them over to the compare-program which is in our case [Perceptual Image Diff](http://pdiff.sourceforge.net).

![](../../assets/c413c3b5a8023087.png)


The program can even output a difference image (see above) which shows you exactly where something changed. In our case this image is automatically attached to the warning mails.

I can’t explain the math but somehow the program does **not** report **every** pixel difference. Pixel changes may have many sources

One major source of change comes from sampling. For example, if the anti-aliasing scheme were to change from one version of the renderer to the next, the pixels on the edges of objects might have slightly different values. The same thing might happen in the shadows of objects as soft shadow algorithms evolve over time. These imperceptible changes induce many false positives (bugs which are not actual bugs) in the rendering tests.


–[A Perceptual Metric for Production Testing]

Some pixel changes may not be “real” concerning errors (“false positives”) and therefore the program does only report perceivable changes. Here is an example where I changed the Anti-Aliasing-Algorithm for a Font and this results in small errors, which the observer wouldn’t notice.

This **GIF** shows the tiny differences:

![](../../assets/56e7762fbcdbac71.gif)


After the comparison it’s necessary to interpret the program output to be informed if all is fine or if there are differences. When we compare the images from above (with Perceptual Image Diff) we get this command line output:


There’s **no output** because there are **no** or **not enough** (below a threshold) different pixels. To make the program give you an output anyway, you have to use the **-verbose** parameter ([see the documentation for more details](http://pdiff.sourceforge.net/)). Then it looks like this:

perceptualdiff.exe d:\test1.png d:\test2.png -verbose

…

PASS: Images are perceptually indistinguishable

0 pixels are different

But don’t worry, you only need to paint **one** white pixel into one of the images (or another color which stands out), you’ll get an error:

…

PASS: Images are perceptually indistinguishable

1 pixels are different

The program still ignores the pixel because we didn’t set a threshold. For this test I’ll set it to 0 pixels and *tadaaa*:

perceptualdiff.exe d:\test1.png d:\test2.png -verbose -threshold 0

…

FAIL: Images are visibly different

1 pixels are different

I experimented with the threshold starting from 10 but found a value of 100 giving the best sweet-spot between security and acceptable pixel errors.

By the way: If the images are binary equal you’ll get this output:

…

PASS: Images are binary identical

If all this is too inaccurate and you want to be informed about **every** difference, you can use another tool named [DiffImg](http://thehive.xbee.net/index.php?module=pages&func=display&pageid=11#Usage) which can compare pixel per pixel but also has an option for using a perceptual Metric (which I wouldn’t use because when the threshold **isn’t** reached, you don’t get any console output and I didn’t see any -verbose parameter in the [documentation](http://thehive.xbee.net/index.php?module=pages&func=display&pageid=11)). With this program we get a slightly higher pixel error count:

diffimg.exe --batch --metric PerChannelMetric --threshold ErrorNum=0 d:\test1.png d:\test2.png

…

* ErrorNum = 2279 (threshold = 0)

ErrorPercent = 1.65944588051116 (threshold = 0)

![](../../assets/ebe450f92e093152.png)

With the **--output** parameter you can get a diff image (the Perceptual Image Diff program has such an parameter too). But while it was almost black by using a perceptual metric, with an accurate check it looks like this:

![](../../assets/d770182f639acdce.png)


I guess it will be your decision what program/algorithm suites best to you and your project. Feel free to tell me your experiences. :)

When the script found a difference, it would send out a mail to a responsible person. Read more about this in the next chapter.