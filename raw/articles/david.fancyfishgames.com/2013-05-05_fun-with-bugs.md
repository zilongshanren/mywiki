---
title: Fun with Bugs!
url: http://david.fancyfishgames.com/2013/05/fun-with-bugs.html
author: Legend
published: '2013-05-05'
source_blog: The Legend of GameDev
source_site: http://david.fancyfishgames.com/
category: graphics
fetched: '2026-04-13'
---

This will be a short blog post about something funny that happened when I was trying to debug my latest game, Rhythos! The bug report was that if you beat the final boss with no equipment by the timer running out and having more health, the game froze.


Of course, the first thing I do when I get a bug report is I try it out. If the bug isn't reproducible, then it's almost impossible to debug. So, I tried it out, and the game froze, so at least the bug was reproducible. I was ready for this to be a quick fix!


Then, I put some debugging traces in around the end of battle, and ran it locally on my computer to see if I could find out exactly where the bug occurred. But then the bug DIDN'T occur!


So, my next thought was that it had something to do with running in debug mode, or running locally on my computer (instead of embedded in chrome). So, I tried it out on my homepage (which was the same version as the one uploaded to newgrounds), and the game worked fine!


Alright, so the problem obviously had to do something with being uploaded on newgrounds or the newgrounds API. Already I knew this would be an annoying bug to fix. Hoping I would get some error in the flash tracer, I tried the game in firefox (I can't install a debug flash version in chrome because it has a built in version of flash), but the game still worked fine, with no errors in flash tracer.


Baffled, I tried doing the same thing with another enemy. The game worked in chrome on newgrounds. So apparently this bug only occurred in chrome, on newgrounds, against the final boss. To make sure I wasn't going crazy, I tried reproducing the bug again, and once again, the game froze.


The bug was reproducible, it should have been an easy fix! But I was having trouble getting debugging information. Reproducing the bug again and paying close attention to exactly where the game froze, and what commands had been called before it crashed and which commands couldn't have been called yet, I narrowed down the approximate area the bug could occur. Then, with no other information to rely on, I made a wild guess - I noticed that the game would freeze at that moment if somehow the time remaining on the song ended up less than zero.


Of course, given that the song's position should never be greater than the song's length, this shouldn't be possible, but I was looking for something that should be impossible but occurred in one custom version of flash player on chrome. Perhaps chrome's flash player had a bug where the length it returned was a few milliseconds off. So, I uploaded a new version that checked and properly handled if the song's time remaining reached less than zero, and it worked! The bug was solved, and I rejoiced!


As for why the bug didn't occur with other monsters, my guess is that it's because other monsters have other songs. I didn't try reproducing this bug with the flower or lich lord, the only other enemies that have the same bgm as the final boss. I still don't know why it worked on my homepage and not on newgrounds, but the bug was fixed, and my blog post done!

## No comments:

## Post a Comment