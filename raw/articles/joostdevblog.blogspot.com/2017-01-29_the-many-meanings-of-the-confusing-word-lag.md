---
title: The many meanings of the confusing word 'lag'
url: http://joostdevblog.blogspot.com/2017/01/the-many-meanings-of-confusing-word-lag.html
author: Joost van Dongen
published: '2017-01-29'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

It can be difficult to know exactly what's going on, but it would already help a lot to always at least specify which of the rough groups you mean, instead of just saying 'lag'.

Note that this post is not specifically about our own games. These problems can happen in most games, although the exact impact depends on how the game was been programmed.

### Internet and connectivity issues

**High ping**: ping is the time it takes for an internet packet to travel from your computer to another. In most games the gameplay still feels smooth with high ping, but you'll often start seeing oddities like getting shot by someone who isn't in view anymore, or your shots missing despite perfect aim. The faster the game, the more problematic high ping is.**High jitter**: jitter is an often overlooked aspect of ping. Jitter is when some packets take longer than others. Jitter often causes stuttery movement in games. You might have low average ping but still experience stutters because of high jitter. (**Packet loss**often looks the same as an extreme type of jitter so I'm not listing it separately here.)**Pingspikes**: this is when occasionally the connection becomes extremely slow or even drops altogether for a few seconds. In most games ping spikes result in serious problems, like your controls not working anymore for a while, getting a lot of damage at once at the end of the spike, or even being disconnected.

All of these problems can have many causes, like a slow internet connection or your roommate downloading a torrent over the same connection. There's one common cause that's relatively easily solved though: WiFi. WiFi increases ping, causes jitter and packet loss and, worst of all, pingspikes. If you can, never play online games over WiFi. Connect to your router with an ethernet cable instead. Check

[this blogpost from the League Of Legends devs](http://na.leagueoflegends.com/en/page/ethernet-vs-wifi-ping-packets-playing-better)to see how bad WiFi really is.

### Delay between input and seeing the result

**Input delay**: the time between you pressing a button and the game actually processing it. Games usually process input only once per frame, so the higher the framerate, the lower the input delay. Drivers and the operating system will also cause a little bit of input delay, or a lot if it's a complex controller like the Kinect camera.**Input jitter**: this is when the input delay varies. This can happen if you press the button just before the frame update and then just after. If the game runs at 30 frames per second, this can create a 33 milliseconds difference in input delay. The higher the framerate, the lower this kind of jitter wil be.**Rendering delay**: once the gameplay has processed your input, it needs to be rendered. The GPU is usually at least one frame behind, and in some cases the game itself can be as well. For example, if you set the*Multithreading Mode*in[Awesomenauts](https://www.awesomenauts.com/)to*Higher Framerate*, then the graphics are always one additional frame behind on the gameplay, causing additional input delay. Again, the higher the framerate, the smaller this effect.**Monitor delay**: this is usually the most noticeable cause of delay between pressing a button and seeing the result. Many televisions have all kinds of clever processing to make the screen sharper and smoother, but this can add[over 100ms](http://www.rtings.com/tv/tests/inputs/input-lag)of lag. That's a lot and can be very noticeable. When using a television you should always switch it to*Game Mode*to solve this. Computer monitors generally don't have this problem.

### Framerate problems

Low framerate is also often called "lag". Players sometimes don't realise that there are different types of low framerate. Being precise when describing your problem helps a lot if you ever ask anyone for help with how to solve your framerate problems.

**Constant low framerate**: this usually means the videocard or processor is not fast enough to run the game.**Occasional long stutters**: the game sometimes freezes for half a second or more. This might be caused by problems reading from the harddisk, so switching to an SSD might help. In general though, a game should be programmed in such a way as to do disk reads asynchronously and thus not freeze like this, but sometimes this is really difficult to achieve.**Regular short stutters**: every second or so the game skips a few frames. Such stutters are really short but can be very noticeable, especially during smooth camera movements. This might be caused by running something else on your computer (like a virus scan or a lot of tabs in your internet browser). It can also be caused by the game not balancing the work well enough between frames, causing some frames to take longer.

Framerate problems and input delay are both often decreased by turning off VSync. This does come at the cost of getting screen tearing though. Which you prefer is a matter of personal taste.

This comment has been removed by a blog administrator.

ReplyDeleteGuess this page doesn't get any kind of answers on it as can be seen from all of the visitor posts on it with ZERO answers....

ReplyDeleteThe chat in Awesomenauts is a HOT mess and the matchmaking is a joke....Been playing for years and can't any longer because everyone is pinging at stupid high levels and teleporting all over the way....mean while all those laggy kids win the match cause you can't possibly hit them.....FIX YOUR GAME....BUY A SERVER....Taking in all this money from Gofundme and now for all of the in game extras yet can't purchase a server....what a joke this company is.

Very informative post. Thanks for sharing! When I normally think of lag while playing online, I rarely even consider monitor or input lag. Now I'll be a bit more mindful.

ReplyDelete