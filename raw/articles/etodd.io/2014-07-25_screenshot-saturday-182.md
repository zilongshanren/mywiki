---
title: Screenshot Saturday 182
url: https://etodd.io/2014/07/25/screenshot-saturday-182/
published: '2014-07-25'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Screenshot Saturday 182

What's that you say? You didn't even notice the absence of Screenshot Saturday last week? How convenient. Let's pretend it never happened. Or rather, pretend that it did. Whatever.

[MGDS](http://mgdsummit.com/) was a huge success! There was almost always a line to play the game, and I got a ton of useful feedback. Here are some pictures:

Most of the feedback was related to level design. I came home with a phone full of "todo" items. Here are some screenshots of overhauled or brand new sections that resulted:

I also did some writing. I got sick of exporting dialogue files from my web browser, so I converted Dialogger to a desktop app using [App.js](http://appjs.com/). It's not maintained anymore, but it was way easier to set up than node-webkit, which apparently is the current standard.

One thing that really bothered me when watching people play Lemma was the fact that any time they touched a wall, their momentum was instantly killed by friction, even though the player character's friction is set to zero.

I read an [article from Mike Bithell](http://mikebithell.tumblr.com/post/83244226608/aaa-game-control-in-an-indies-evening) about how he solved this problem in his new game Volume. My solution is very similar, but it jumps straight to the correct movement angle rather than incrementing by 5 degrees and re-testing. Here's how it used to work:

And here's the new, smoother version:

Another thing I forgot to show off earlier is that now, Joan's feet move much more realistically when you're turning in place. I also added an option to display a reticle at the center of the screen, for the purpose of lessening motion sickness in some players. It's disabled by default because no one has complained so far, but it's there if you need it. Here's a GIF showing off both new features:

That's it for this week. Thanks for reading!