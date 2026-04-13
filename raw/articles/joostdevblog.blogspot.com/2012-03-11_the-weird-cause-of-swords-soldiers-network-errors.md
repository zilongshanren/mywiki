---
title: The weird cause of Swords & Soldiers network errors
url: http://joostdevblog.blogspot.com/2012/03/weird-cause-of-swords-soldiers-network.html
author: Joost van Dongen
published: '2012-03-11'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com/). I'm afraid that because of the work on

[Awesomenauts](http://www.awesomenauts.com/), we didn't come to it any earlier. But we finally fixed it now! :)

Now this bug we fixed was a pretty interesting one. Not as interesting as

[the bug](http://joostdevblog.blogspot.com/2011/12/lamest-bug-we-ever-encountered.html)I posted about last December that got my blog a whopping 40,000 viewers in a couple of days, but still interesting enough to share it with you. This one is another nice example of how bug fixing sometimes requires thinking far outside the box.

We were getting two bug reports from users:

- Some users always got a Network Error at the start of a match.
- Some users encountered cheaters who introduced so much lag, that the game became unplayable for the player on the right side of the map.

We initially just assumed the Network Errors were being caused by firewalls or bad router settings. But these users were not having trouble in other games, and it even didn't work when they turned off their firewalls. We also had a user who told us it worked on his laptop and not on his PC, while both were on the same network. That pretty much ruled out router issues as well.

As for the 'cheaters': we immediately had the hunch that this might as well be a network bug in our code somehow, and not really someone cheating.

We had looked at this bug at various moments in the past year without success, and wondered whether it was still a firewall, or something in the Steam networking libraries. We even sent the Steam support team questions about this one. They didn't know any bugs in their system that could cause this, which was of course right, since this turned out to be a bug in our own code...

So, what was up? In a very bright moment, my colleague Maarten, who does a lot of network programming at

[Ronimo Games](http://www.ronimo-games.com/), suddenly realised what was happening: to check what the ping is and to keep the connection alive, we regularly send ping messages over the network. Accidentally, we did that

*every frame*. Now sending 60 extra messages per second over the network is a really bad idea, but does not usually kill a connection. However, and this is where we are getting way out of the box:

*some users had forced vsync to be turned off in their drivers*. For those who don't know:

*vsync*makes sure a game runs at the same framerate as your screen, usually 60 frames per second. Forcing vsync off means Swords & Soldiers might be running at hundreds of frames per second on their computers! Sending that many ping messages instantly kills most connections.

This also explains the 'cheaters': if the framerate is not high enough to actually kill the connection, it can still be high enough to make the connection really bad. The player whose computer is server in a match won't notice this, but the other player (whose computer is the client) gets so much lag he can hardly play anymore.

![](../../assets/36001ec25ab6894a.jpg)

So, the solution was really simple: instead of sending the ping message every frame, we now send a small, fixed number of them every second. Which is actually what we had intended in the first place, had a bug not thwarted our plans!

So, another nice example of how bug fixing requires letting go of all assumptions, and researching with an open mind what is actually happening. Until we found this bug, I never would have connected vsync with networking errors!

I would like to thank the Steam users who helped us with testing to find this issue! I would also like to thank those who offered help that we ended up not using. It is great to see that gamers are so willing to help when we are stuck on a bug! Thank you very much, folks! :D

PS. If anyone encounters any new or further issues, then please don't hesitate to post them at the

[Steam forum](http://forums.steampowered.com/forums/forumdisplay.php?f=1040)or

[our own forum](http://www.awesomenauts.com/forum/), and we will look into them as soon as we can!

No wonder Maarten could think out of the box here. He played SOF in team NL, every pro player plays with vsync off, doh! :)

ReplyDeleteIt was Quake 3 not SOF!

ReplyDeleteSOF is the encrypted version of Quake3, this was about networking!!

ReplyDeleteThe finding of the mistake should have been more dramatic and mysterious!

ReplyDeleteMaybe I should turn it into a mystery novel, then? ;)

ReplyDeleteIt's a little surprising you guys didn't catch it earlier via some debug info that tells you "how many packets/KB are being sent/received per second" and by playing with vsync off.

ReplyDeleteIn retrospect it may sound like that, but really, turning off the graphics feature vsync for network testing is one of the last things I would have thought of before I saw this bug...

ReplyDeleteGood for identifying this bug as it can potentially cause more problems. Too many programmers would tie 'periodic' events to the main game loop. This teaches us not to do that unless that's the desired behaviour.

ReplyDelete