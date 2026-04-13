---
title: Threads, buffers and latency
url: http://c0de517e.blogspot.com/2010/08/threads-buffers-and-latency.html
published: '2010-08-10'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

This is interesting:




It's a thing that I always suspected, but never tested. The next need for speed will ship with a single thread, without a simulation/rendering split, and that's because at 30fps that buffered split of one frame is enough to be noticeable in game.


How many frames of latency can you count in your game? Mine currently has at least three (maybe more, in subsystems that I don't master): sim->render, render->worker jobs, jobs->gpu.

[http://www.eurogamer.net/articles/digitalfoundry-needforspeed-tech-interview](http://www.eurogamer.net/articles/digitalfoundry-needforspeed-tech-interview)It's a thing that I always suspected, but never tested. The next need for speed will ship with a single thread, without a simulation/rendering split, and that's because at 30fps that buffered split of one frame is enough to be noticeable in game.

How many frames of latency can you count in your game? Mine currently has at least three (maybe more, in subsystems that I don't master): sim->render, render->worker jobs, jobs->gpu.

## No comments:

Post a Comment