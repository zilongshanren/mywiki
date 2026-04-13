---
title: 'People of HTML5: Mr. Doob – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2011/07/people-of-html5-mr-doob/
author: Chris Heilmann
published: '2011-07-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

HTML5 needs spokespeople to work. There are a lot of people out there who took on this role, and here at Mozilla we thought it is a good idea to introduce some of them to you with a series of interviews and short videos. The format is simple – we send the experts 10 questions to answer and then do a quick video interview to let them introduce themselves and ask for more detail on some of their answers.

![Mr. Doob](../../assets/d5640bcb2165fab5.png)

[Mr Doob](http://mrdoob.com/). Ricardo is a man that always crops up when the talk is about impressive technology demos. Starting with [the ball pool](http://mrdoob.com/projects/chromeexperiments/ball_pool/), continuing with the beautiful [Harmony](http://mrdoob.com/projects/harmony/#longfur) and culminating in [The Wilderness Downtown](http://mrdoob.com/projects/radicalmedia/arcadefire/redirect/) and [Three Dreams of Black](http://www.ro.me/) he continuously got commissioned to do things Google showed off at their big events.

Ricardo values his privacy, so he didn’t want to be interviewed on camera. We respect this, and instead only give you his answers in text.

**1) Welcome. It seems to me there is not a single conference or article about the use of modern web technologies that doesn’t feature work by you. You also seem to have appeared out of nowhere. What’s the secret? What is your background?**

My brother introduced me to the [demoscene](http://en.wikipedia.org/wiki/Demoscene) at the age of 12 and slowly learnt my way creating graphics and modelling lowpoly 3d scenes to be rendered in realtime. So far I’ve done [more than 50 demos](http://ricardocabello.com/demoscene) in my spare time. Only on the last demos I did the code part though. My role was always being the designer, illustrator, 3d modeller and/or director.

During that time I was working as HTML/PHP developer and later, when I moved to London, I started working as Designer/Flash developer. At this point I was slowly becoming a graphics programmer and I saw the chance of messing with the tricks I saw being used in all these demos and also finally putting into practice my own ideas for effects. I started uploading the experiments on the mrdoob website with no real reason. That turned out to be a great way for attracting interesting projects that allowed me to keep experimenting.

**2) A lot of the work you’ve done is experimental and very much on the bleeding edge of what browser technologies can do. Live products on the web however should not frustrate users and tell them to upgrade their browser or give them a broken interface. What is your stance on progressive enhancement and polyfills for older environments?**

Well, the demoscene is way worse. If you don’t have the newest graphics card, chances are you can’t run the new demos being released. You have to upgrade your graphics card every few months. The browser world is simpler, you just need to download a piece of software which you don’t even have to pay for. And, now that browsers seem to be adopting auto-update mechanisms, feels like this problem will finally go away. However, I always develop on fairly low-end computers (MacMini/MacBook) so I can avoid the demoscene problem.

As per progressive enhancement… if I had to include some kind of backwards support in the experimentation process the result will for sure get affected.

Not only the code wouldn’t be as simple but, in some cases, I wouldn’t even start because it wouldn’t be as fun. With my current approach, some users won’t see anything or get errors, but there is a chance that some of these will upgrade to a modern browser in order to play with the experiment. Which, not only helps me, but the rest of developers and, I want to think, also the whole web.

**3) Whenever a new demo comes out and it only works in a certain browser without gracefully giving others a diminished experience I get the feeling we are not doing a good job advocating open technologies. After all no clothing store would display dresses in edge case sizes or with missing buttons. Do you agree? Or is it OK to build a demo for one single environment and call it a “web technology showcase”?**

I personally try to make sure all the projects I do work on as many modern browsers as possible and I try to avoid technologies that have only been implemented in just one vendor. There are cases, however, that a experiment may not work in a browser because the Javascript engine isn’t fast enough.

These demos make the problem evident and if the browser developers notice it they’ll work to make sure their engine is fast enough to match the other browsers with that demo.

**4) Looking at similar groundbreaking work like you’ve done in the demo scene I found that the really successful groups tend to build their own tools for edge case tasks. When Farbrausch for example released their 96KB 3D Shooter game .kkrieger they soon after also released werkkzeug to create similar games and animations easily. Do you have some awesome tools up your sleeve? What is your development environment?**

No tool yet. But now that the Filesystem API is being adopted I’m starting to seriously consider it.My development environment is, for some, surprisingly (and disappointingly) simple. I use Ubuntu’s default text editor [gedit](http://projects.gnome.org/gedit/) with a [dictionary-based code completion plugin](https://github.com/nagaozen/gedit-plugin-codecompletion/). I also have a plugin enabled that shows unneeded spaces at the end of the lines – I’m a bit obsessed with clean and spaced code.

**5) What product are you most proud of and why? Who inspires you? Are there any cool web technology demos that made you go “wow”?**

I don’t know why but I’m unable to be proud of anything I do. There is always something to improve, and that thinking makes me almost be ashamed when talking about my work.I get inspired by anyone that spends an admirable amount of time in creating something different or unique. Thankfully, the list of names would be endless. Also, open source as a whole inspires me, not only libraries but the linux world in general. The fact that you can see the code other people are committing pushes you to continue doing your part. As per impressive technology demos, this [Path Tracer](http://madebyevan.com/webgl-path-tracing/) and the latest experiments by the [miaumiau](http://labs.miaumiau.cat/) guys are good examples. I wish I knew how to do these things :)

**6) Are there parts of the technology implementation of the HTML5 standard do you still consider terribly broken? For example the web version of Angry Birds uses Flash for the audio – why is that?**

I won’t get tired of saying that <canvas> should bring the “darker” blending mode back…I haven’t played with <audio> much yet, but I haven’t heard good things about it. Hopefully the upcoming Audio APIs will sort this out. They first need to agree on an API though.

**7) A lot of the “wow” that we are shown these days in open technologies has been done in Flash before. You hear a lot “this is not Flash, even when it looks like it”. Are we just reverse engineering what the closed technology world did in the past or is there some re-use and knowledge sharing going on?**

And a lot of the “wow” that was done in Flash was done before in MSDOS and Amiga (yes, sadly the gap was that big). But we managed to bring to the platform some of the tricks that the Amiga people found during all these years. With WebGL now the web is finally catching up with modern graphic pipelines. The problem will now be that website production will become more costly. A bit like the videogame world where they spend many months (or years) in production.

**8) Let’s quickly talk about performance. When I watch 3 Dreams of Black on my MacBook Air it sounds like my vacuum cleaner and the battery drains very quickly. What are the most resource hungry technologies in the open stack and what could be done about this? Will there be adaptive technologies that for example give a higher poly version for beefy machines and low poly versions for slower ones?**

With video we have something like that in Silverlight and Flash when it comes to streaming. Is there work done in open technology we can look forward to?There is a tiny detail to consider there, I used to have a MacBook Pro with an ATI graphics card and the fan would get noisy the second it started to render a few polygons. Now I use a MacBook with a NVIDIA and I hardly hear the fan. The GPU use is the same, but just happens that the graphics card was designed to be quieter. If you happen to have such a card the performance issue decreases considerable – as there is no annoying noise.

However, we should indeed optimise our code and only render what’s required when it’s needed. As soon as WebGL lands in Android/iOS devices we’ll probably start to seriously considering serving low-poly objects to such devices.

**9) Resources. Let’s say some gifted kid coming from school right now wants to be Mr.Doob and bring the awesome. Where can you learn? What should you concentrate on?**

Not sure… I guess one needs to spend a lot of time tinkering with code, experimenting and creating projects just for fun. While you’re in such a loop ideas arise constantly and the only thing left is spending more and more time turning these ideas into life.

And now that we’re moving to HTML5/Javascript, you only need to right click and view the source. I still can’t even begin to imagine the ramifications of this simple fact.

**10) What’s next? Anything cool coming our way we can look forward to? Also, what do you want? What do you think keeps us from going really all in when it comes to open web technology?**

Well, right now I’m still trying to “solve” [three.js](https://github.com/mrdoob/three.js/). It does feel like an endless task right now, but I’m confident there is a way. With libraries like [stats.js](https://github.com/mrdoob/stats.js), [tween.js](https://github.com/sole/tween.js) and [sequencer.js](https://github.com/mrdoob/sequencer.js) I have proven myself that libraries can reach a state when do not require more features.

Lately I’m on a personal crusade on creating open source libraries and tools that make the web development possible without the need of proprietary tools and operating systems. I have a ton of .psd and .fla files that I can’t open now that I run Linux. I would like to avoid such scenarios to happen again.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 6 comments

erikJuly 19th, 2011 at 12:15RoskoJuly 20th, 2011 at 00:08xeroJuly 20th, 2011 at 12:40SUBZERONovember 24th, 2011 at 18:00SAURABH SINGHOctober 9th, 2012 at 07:59EmilyOctober 21st, 2012 at 14:48