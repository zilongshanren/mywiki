---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-convert/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

The next step is necessary because we had to use BMP (instead of PNG) as output format. There are two reasons for that:

- We could not use PNG because of problems with the transparency channel.

You’ll find more details in the[problem section](http://simonschreibt.de/wft/watchdog-problems#png). - Not all screenshots must be PNG. For
**some**it’s useful to use the even smaller JPG format (explained below)

PNG, BMP, JPG??? It’s easy: To **automatically** compare images we need a format which is stored with **lossless** compression to not have too many pixel changes due compression artifacts:

![](../../assets/8cd304fd071e0e71.png)


We could just use the BMP format (not compressed at all) but a BMP file (1280×720, 32Bit) needs ~3.5 MB which is too much if you take ~1900 screenshots every night.

Also some of our screenshots can be stored as JPG which again saves some space. PNG on the other side is compressed but this happens **lossless**!

![](../../assets/f2550917d62db329.png)


But which screenshots should be saved as PNG (comparable through loss-less compression) and which as JPG (not comparable but small filesize)?

Here you see an example showing scenes which you **can not** compare due moving stuff and randomization. These screenshots can be stored as JPG and only serve as archive:

If we want compare screenshots we need **special static scenes** like below. The screenshots will be stored as PNG:

Do you remember that we can define the foldername in our game script? The “bait_” in the name tells our Watchdog Script which screenshots shall be compared (and therefore stored as PNG) and which are just for the archive (JPG).

<signal_cue_instantly cue=”AddDirectory” param=”‘**bait_**ads.arcade2_title'”/>

We convert our images via [ImageMagick](http://www.imagemagick.org/script/convert.php). Here’s an example of how we start the program (I shortened the images-names in the example to fit them into one line):

convert.exe screen.BMP -alpha off -scale 1280 screen.JPG

You may ask, what this **-alpha off** option does. Well, we had to throw away the alpha because debug text and the Steam Overlay were written into it. [Read more about this here](http://simonschreibt.de/wft/watchdog-problems#png).

![](../../assets/ebe450f92e093152.png)

The last step is to delete the BMP.

Now we are ready! We have saved a lot space on the hard drive and the “bait_”-screenshots are in a format which can be compared.