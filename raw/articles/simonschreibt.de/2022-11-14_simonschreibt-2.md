---
title: Simonschreibt.
url: https://simonschreibt.de/wft/gif-like-a-pro/
author: Simon
published: '2022-11-14'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

In most studios I’ve been, at some point coworkers asked me “Simon, how do you create so many videos/gifs/screenshots so quickly?” (because I make a TON each day to show work results, visualize bugs or explain workflows) – Here are my 3 main tools for my 3 main usecases.

## General

I setup all the tools write their images/videos into my temp “thrash” folder e.g. e:\private\capturing\ Videos I want to share with the team get named nicely (bug_chairExplodesWTF_01.mp4 or 2022-11-05_unicornPoop_04.mp4) and stored in a separate folder like \gamevfx\

## 1. OBS

I’ve [OBS](https://twitter.com/OBSProject) autostart with windows, it runs ALL THE TIME in the background and I set Alt+F9 to start/stop a recording (as MP4). By default I capture the game in fullres but sometimes I switch to rec the whole desktop.

I record videos to document my work (at least 1 video per effect per day). It’s not only fun to be able to see how the vfx developed over several days but I also send the final video to QA so that they know exactly how the vfx should look when they test my stuff before I checkin.

I record them also to document bugs (and if possible how I reproduce them) or issues with tools “When I press this button in that 3ds max plugin, xyz happens”. Here the desktop capturing comes into play.

Very rarely I want to crop/zoom or shorten a video (and maybe convert it into GIF). For that I use Photoshop (you can do simple MP4 editing (Window > Timeline) and export as GIF via File > Export > Save for Web) and also speed up the video up to 400%.

⚠ Careful: For some reason there’s a max frame count of 500! The GIF will continue to run but nothing moves anymore (last frame repeated?)

## 2. ScreenToGif

I use [Screen2Gif](https://www.screentogif.com/) when I need a GIF of a SMALLER part of the screen (it can also write MP4) and when I know that I can NOT time the recording well (I need to cut frames away before/after the event I want to capture). Place/resize the frame and hit record.

As soon as you press “Stop” a video editor opens where you can crop the recording, cut away frames or change the speed. ctrl+s saves it and you can chose GIF/MP4. Note: You can also load an MP4 to edit/convert it into GIF but the loading takes way longer than loading it into PS.

## 3. ShareX

[GetShareX](https://twitter.com/GetShareX) autostarts with (my) windows and runs in the background all the time. To record a GIF super quick: ctrl+shift+print > draw rectangle, let it record then press stop. Done. Not sure if there’s any faster workflow.

⚠WARNING!⚠ ShareX uploads everything by default! This option should be the first to DISABLE! [#avoidLeaksOfYourSuperSecretProject](https://twitter.com/hashtag/avoidLeaksOfYourSuperSecretProject?src=hashtag_click) You may wonder: How did I create this nice screenshot with the numbers and green box? Read further

You can create normal screenshots with shareX (no GIF). First you press ctrl+print and then select a window or just a region. Very awesome! Now you get a popup of your screenshot in the corner of the desktop which you can immediately drag&drop or click to use/open it.

BUT, after pressing ctrl+print (and BEFORE clicking anything or selecting a region to capture) a little toolbar allows you to add A LOT of stuff to your screenshot: text, arrows, numbers, boxes, drawing, stickers …. and you can even pixelate/blur parts! A-M-A-Z-I-N-G!

With these tools you can make a screenshot for your coworkers which point exactly where the bug is located (and maybe even where to click to reproduce it). I use it also to explain debug UIs which can be very finicky. [#avoidMisunderstandings](https://twitter.com/hashtag/avoidMisunderstandings?src=hashtag_click)

![](../../assets/1526592fdec990ba.png)


![](../../assets/1526592fdec990ba.png)

![](../../assets/5aad5143b771fdd6.png)


![](../../assets/5aad5143b771fdd6.png)

Have a super-good day!

Simon

Hey Simon! I also tried so many things!

OBS is still awesome but for making little clips of something probably not the best tool. Wanted to make it so that it records a defined subsection of the screen and that’s really a hassle to setup.

ShareX seems like a humongous beast that does so many things I wouldn’t want (or do I? Its so much!). Currently I don’t use it.

ScreenToGif actually seems pretty much to do what I’d want but it looks rather unpleasant.

I actually started to work on my own screen capturing tool already:

https://github.com/ewerybody/kiekste/

But currently I lost track and during the switch from Qt for Python 5 and 6 a lot of refactoring had to be done which is still not over.

Oh on top of that I gathered quite a bunch of ffmpeg command line recipies that I use to process things.

Gifski is also nice! https://github.com/ImageOptim/gifski/

Maybe one could make a dedicated Autohotkey extension that utilizes some of these from File Explorer selections 🤔

i never did the dive into ffmpeg but i hear often that people really like to command line it :D

ScreenToGif is perfect for this in my eyes as you can define the are you want to capture and afterward you can even edit the clip. so useful to find the perfet time frame you want to show off and then optimize the gif for filesize!