---
title: 'Tuning: Two-axis controllers, OSC and multitouch.'
url: http://c0de517e.blogspot.com/2013/02/tuning-two-axis-controllers-osc-and.html
published: '2013-02-09'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

So far, and even in the near future I'd say, game visuals, even with physically-based (or inspired... or "reasonable") shading, have been a matter of tweaking and tuning, both by the artists and by the programmers, functions and parameters. Thus, the speed and intuitiveness at which this tuning, iteration happens, has a crucial, direct impact on the end results.

Now, if you've been following this blog for a bit, you might have noticed that I'm a strong proponent of live-coding, hot-swapping and all manners of ways to transform our art into a direct feedback mode of manipulation.

So I was very curious when I had, two weeks ago, the chance to attend talks by two of the forefront proponents and innovators in this field, the designer-coder-instructor-inventor

[Bret Victor](http://worrydream.com/#!/Bio)and Pixar's and demoscene's manipulator of functions extraordinaire,[Inigo Quilez](http://www.iquilezles.org/).
I won't go into the details of these, but one thing struck me that I thought was worth further research and sharing: IQ's use of

[OSC](http://en.wikipedia.org/wiki/Open_Sound_Control)to connect hardware midi (well, OSC) controllers to shader parameters in his demo/livecoding/vj system. Of course, such things make perfect sense when you're VJing in a club, and I've seen even in our industry some experiments with midi devices to control a variety of things in a game, honestly my experience relegated them as being most often nothing but a gimmick. Inigo, begin the smart guy he is, also came to a similar conclusion, with an exception though, when it comes to tune two or more correlated parameters, they have their space.
Of course! All of a sudden I feel so stupid having had to explain so many times all kind of multiply/add controls to artists! MADD is the shader coder best friend, it's cheap, it's powerful, it ends up everywhere. But for the artist, even when you "convert" it into the often more friendly add-multiply (just postprocess the data out of the tuning tool), and using the right bounds, constraints and so on, it often comes to be a pain to manage. I've always had these controls bound to two separate sliders, which is a really stupid idea, on a non-multitouch device (or without physical independent sliders).

Of course, you could just use a two-axis pad and control it with the mouse, the solution is quite obvious, honestly, that's why you should have a

**human interface designer**in the team, not only for the game UI, but for tools, for in-game data display and so on. But I digress...
I went on and did some research on OSC and devices. There are too many things! I'd say, a good starting point is to take a look

[at a client for multitouch devices](http://hexler.net/software/touchosc)(iSomething, Android or whatever). These are nice to play with because they are easily configurable and support bi-directional communications (which some hardware devices implement, often at a premium price).
Even more interestingly, some applications, like the open-source

[Mrmr](http://mrmr.noisepages.com/4-2/)and[Control](http://charlie-roberts.com/Control/)(whose development, unfortunately, don't seem to be very active nowadays) come with support for dynamic configuration and scripting, so your game or tool can send messages to change the layout of the controller, which basically ends up to be a remote, programmable GUI - per se an**awesome**thing to have. Control is essentially a HTML5/JS GUI connected to OSC, with OSC able to feedback into the JS to manipulate the GUI remotely!
![]() |

Now of course, all of this could be easily done even in whatever custom tuning environment you already have, in the end, nothing of this is rocket science, remote displays for GUIs existed twenty years ago, and probably you already have a decent collection of widgets, maybe some good colour pickers, some axis/angle selectors, sliders and so on.

The game-changer here in my mind is the multitouch support though, which enables a category of manipulators impossible on a PC alone.

Also once you support OSC, you automatically will be able to use any kind of OSC device, driver, or aggregator. A joystick as input? A webcam? Sound? Wiimote? A sequencer (see

[this](http://www.iannix.org/en/index.php), it's pretty crazy)? Custom hardware? You name an input method and there is probably a Midi or Osc interface for it, and pretty much any programming language will have bindings, and most libraries for creative coding, like the multiplatform[OpenFrameworks](http://www.openframeworks.cc/).
Hardware is surprisingly not too expensive either, you can get something basic like a

## No comments:

Post a Comment