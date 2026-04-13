---
title: 're:Creation dev log. Week #2 and #3. AI stuff and vacation'
url: https://eliasdaler.wordpress.com/2014/07/28/recreation-dev-log-week-2-and-3/
published: '2014-07-28'
source_blog: Elias Daler | Re:creation
source_site: https://eliasdaler.wordpress.com
category: game programming
fetched: '2026-04-13'
---

**Week #2 and #3. AI stuff and vacation**

I started to prototype the first “real” level of the game. As I was working on it, I realized all the flaws of level editor and features it lacked of. So I worked a lot on the level editor!

A lot of time was also put in optimization. Release build was always working at 60 fps without a problem, but as an object counter grew bigger and bigger Debug build started to slow down, so I decided to optimize my game a bit and now it’s running at 60 fps on Debug too. Neat.

I was also working on AI for some time. First I got NPC to go to the specified point of map.

![](../../assets/e6f7d2ed79a5966a.gif)


I accidentally swapped walking animations and results were hilarious.

![](../../assets/a8971f6aa1422f90.gif)



Then I coded “wander” behaviour where AI walks randomly at circles. The algorithm is trivial: system pickes a random point on the circle and NPC walks there. Pretty easy, though there are algorithms which simulate more realistic behaviour, but I thought it would be an overkill for now

![](../../assets/63673b3716b4505b.gif)


You can also walk into houses now! At first I though about having mini-levels and changing current level to “house level”, but I found an easier solution. I just teleport player to another location of the current map and change current camera position. It looks kinda bad now because there’s no screen transition. But I’ll code it soon. :)

![](../../assets/c210a2809fb2b99b.gif)


I’ve redrawn lots of things and the only things left from A Link to the Past are characters which will be redrawn soon too.

![](../../assets/3231cbd83181a530.png)

Everything you see here is drawn by me (except of main hero which is drawn by Dmirty)

And then I had a short vacation for a week. It was very good for me and I’ll work very productive from now on. Dmitry redrawn lots of stuff and made character proportions more realistic so this will be the most amazing update ever next week! See ya!