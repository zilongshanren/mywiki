---
title: runevision blog
url: https://blog.runevision.com/2017_01_30_archive.html
published: '2017-01-30'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

For a while, my focus for my Vive VR game [Eye of the Temple](http://blog.runevision.com/search/label/Eye%20of%20the%20Temple) have been to not expand more on gameplay right now but rather on improving what I've got in order to make it as presentable as possible.

That has meant:

- Improving visuals.
- Addressing usability issues found in play-testing.

(If anybody wonder what happened to the [Whip Arena spin-off game](http://blog.runevision.com/2016/12/spin-off-game-whip-arena.html), I put that on hold after it become clear it only worked well with a quite large physical VR space, which very few people have available.)

### 3D models

*Gate model. Two keys must be inserted above the gate to unlock and open it:*

![](../../assets/ee492c606f25f39e.png)


![](../../assets/ee492c606f25f39e.png)

*Stone torch model. You light these with your torch to trigger things happening:*

![](../../assets/34fce84d1838fcf6.png)


![](../../assets/34fce84d1838fcf6.png)

*Cliffs model. The temple used to just float in the air; now it's grounded:*

![](../../assets/e8b300bfab42353d.png)


![](../../assets/e8b300bfab42353d.png)

For a long time the game was full of placeholder models made of simple boxes and cylinders. There's still some of those left, but I've been working on replacing them all with proper models.

After briefly planning to work with contractors for 3D models, I decided to learn 3D modeling myself instead (and deal with the [various challenges](http://blog.runevision.com/2017/01/the-quest-for-automatic-smooth-edges.html) that come with it).

The models I need have highly specific requirements (they need to have very exact measurements and functionality to fit into the systems of the game) yet in the end they are quite simple models (man-made objects with no rigging).

With this combination it turned out that back-and-forth communication even with a very skilled artist took as much time as just doing the work myself. I'll still be working with artists for the game, just not for the simple 3d models I need.

Several of the models still have placeholder texturing. I have an idea for a good texture creation workflow for them, but it will take a little while to establish, so I'm postponing that while there's more pressing issues.

### Intro section

My goal is that Eye of the Temple should be a rather accessible game. You need a body able to walk and crouch, and not be too afraid of heights, but I want it simple enough to play that people who don't normally play computer games can get into it without problems.

This has largely been a success. Gamers or not, I normally just let people play without instructions, and they figure things out. My dad completed the whole thing in one hour-long session when he was visiting.

The game did throw people in at the deep end though, asking them right from the start to step between moving platforms four meters above the ground. Some people would hesitate enough to end up mis-timing their step and stumble, making the experience even more extreme right from the beginning.

To ease people a bit more in, I've worked on an intro section that starts out with only a 0.75 meter drop, and the first two platforms have no timing requirement. I have yet to get wide testing of this to see if it helps.

![](../../assets/dcb8406cf53b0be8.png)


![](../../assets/dcb8406cf53b0be8.png)

There is *one* particular problem I've toiled with for a while, which is to design a platform that bridges two spots in a compact manner. Why this is tricky relates to how the game lets you explore a large virtual space using just a small physical space.

Originally I had platforms rotating around a center axis, but that made some people motion sick who otherwise didn't have problems with the rest of the game.

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiNN9NUJJLsaxNu3edjZGnEGdksyO8tO6S8S6pY6afGHEUArRo2K4oBQA8Hrx9udA-fXJPRbY4h32pedme5tz0194xvRNxC4DaBWjVAZeTkLwOqstZkSYQ8wm2JEKSjnuMZjJxr7rtsIl8/s800/Rotator.gif)


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiNN9NUJJLsaxNu3edjZGnEGdksyO8tO6S8S6pY6afGHEUArRo2K4oBQA8Hrx9udA-fXJPRbY4h32pedme5tz0194xvRNxC4DaBWjVAZeTkLwOqstZkSYQ8wm2JEKSjnuMZjJxr7rtsIl8/s800/Rotator.gif)

I tried various contraptions to replace it, but they were complicated and awkward to use. My latest idea is using just a barrel-like rolling block, which is nice in its simplicity, and also a fun little gimmick to balance on *once you understand how to use it*.

Figuring out what you're meant to do is easy to miss though, as I found out with the first tester trying it. I have some ideas for a subtle way to teach it, but that will take quite some time to implement. For now I settled for slapping a sign up that explains it.

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiUryhfkj3CgH3p086c2HUsIRk5dBwD9d40XNXVUlvJ_ryPMVhk9aLKPR7uHadbBnNeWcdLAFi1-RwOTevtXHxj1_mdikHdI3REHVYpYYzvGVh7xsb2zLHTB2uBRrg38OB0VenjXYwPcHM/s800/2017-01-29_IntroTutorialSigns.png)


![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiUryhfkj3CgH3p086c2HUsIRk5dBwD9d40XNXVUlvJ_ryPMVhk9aLKPR7uHadbBnNeWcdLAFi1-RwOTevtXHxj1_mdikHdI3REHVYpYYzvGVh7xsb2zLHTB2uBRrg38OB0VenjXYwPcHM/s800/2017-01-29_IntroTutorialSigns.png)

### Early testers online forum

There is no substitute for directly observing people playing a game, but this is impractical for me to do frequently when I also have a full-time job. I'm lucky if I get to do it two times a month.

In order to try to get faster feedback and shorter iteration cycles, I've now opened up for people to [sign up online to be early testers of the game](https://itch.io/t/59040/early-testers-welcome-thread-introduce-yourself). If you have access to a Vive and would like to try out the game and provide detailed feedback based on your experience, please don't hesitate to join!