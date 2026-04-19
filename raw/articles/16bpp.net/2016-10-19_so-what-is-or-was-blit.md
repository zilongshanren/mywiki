---
title: So What Is (or Was) Blit?
url: https://16bpp.net/blog/post/blit-a-retrospective-on-my-largest-project-ever
published: '2016-10-19'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

Before I begin, you can find [the source for Blit over here](https://gitlab.com/define-private-public/blit).

I want to talk a little bit about a project I worked on every day from July 2014 till the end of August 2015. You may have seen [a few entries](https://16bpp.net/blog/post/status-update-4) [about it back](https://16bpp.net/blog/post/status-update-5) [on earlier posts](https://16bpp.net/blog/post/one-year-of-blit); that project was something I called “Blit.” If you’re wondering what Blit was, it was my attempt at trying to make an Animation focused art program. It was pretty ambitious for someone like me at the time.



There were two main reasons why I started to work on it:

- Back when I was an undergraduate, I was part of a student group were we had to do these things called “major projects,” each year if we wanted to retain membership. They usually are of a technical nature (programming & engineering). This is where my initial drive came from
- I’ve never worked on a “large,” or “longterm,” project before. Everything else I’ve done up till that point were small things like class assignments, course projects, or tasks for my internships. I had friends who had worked on their own projects for two or three years straight and made some really cool stuff. I really wanted to be able to tell others (mainly prospective employers) “
*Yeah, I’ve been working on this thing for over year. Want to take a look?*” Other than just “having something,” I also wanted to learn how to manage a larger and lengthier project.

The “major project,” was something that was pretty easy to fulfill. But for the second I did something kind of stupid, but worked well for me. I told myself “*Alright, I’m going to work on a project that will have a 365 day long GitHub streak.*” In reality, git streaks are a silly thing to track progress. I was working on Blit in a private repo, so the outside world would not see my streak at all. I feel bad for the people who have the need to maintain one. For me it was a reminder to build on Blit each day. It worked.

Whether it be programming, logging issues, source code cleanup, design & planing, writing documentation, etc., I had to minimum goal of one *meaningful* commit per day. Normally I would spend an hour on Blit per day (more on the weekends). I would keep at it until the kitchen timer to my side beeped. Somehow that little thing was able to keep me focused for a straight hour.


## So What Is (or Was) Blit?

I’ve always been someone who’s liked art and programming. Especially combining the two. One of my favorite genres is pixel art, or sprites as they are also known. I’ve dabbled in making a few other art programs before, but nothing like this.

Originally Blit supposed to be only a sprite animation tool that had a modern look and feel, but my ideas for it grew greater (**sigh** feature creep). There are many other sprinting tools out there like GrafX2, Aseprite, (and other 2D animation programs like TVPaint). I’m not saying that it’s wrong that they make their own GUI toolkit, but it feels kind of odd. I really wanted to bring these types of programs out of the days of the Amiga. After doing some initial research, I settled on using Qt. Here are my reasons:

- It’s cross platform. I work on a Linux system, but I want my Windows and OS X friends to be able to use what I make
- It’s a C++ library; my native tongue. But there exists bindings to other languages, such as Python
- There’s a lot more to Qt than just widgets. It really is a fully featured desktop application framework
- It has a massive community around it and it’s very well documented. So if I ever ran into trouble I’d be able to find some help

Before I move any further, you might be wondering where the name “Blit.” came from. Since it had a focus on 2D graphics, the name came from the [“Bit blit,” algorithm](https://en.wikipedia.org/wiki/Bit_blit). I used to do a lot of programming with [libSDL](https://www.libsdl.org/), so the function [SDL_BlitSurface()](https://wiki.libsdl.org/SDL_BlitSurface) has been burned into my brain. I thought it would be a cute name too.

I also wanted to keep more of a “traditional animation,” approach to Blit. Instead of drawing on images there were “Cels.” Layers were called “Planes.” Instead of a Dope Sheets I had “Exposure Sheets.” I didn’t call it “onion skinning,” but “turning on the Light Table.”


## Starting Out

As mentioned before, I was focused on sprite animation (originally). I wanted to keep things as easy as possible. While I did consider using Qt’s native C++ libraries, I decided on making the program in Python with PyQt. Scripting languages are typically much faster to write code for. I felt as if I would be able to get more done in less time. I didn’t think that there would be too many computationally intensive procedures to worry about. In the event that I needed some performance boost, I could always write a C/C++ extension for Python.

After choosing my tools, the first thing I did was draft some design documents. These included a user interface mockup and an initial file format structure. I started to log tickets on the GitHub issue tracker. I had an miniature road map to start from. Within a month and a half, I was able to load up one of my files into Blit, do a little simple Cel & Frame editing, and then save it. You couldn’t do too much with it, but I thought it was a good starting point.



During my initial research of Qt, I discovered something called the “[Graphics View Framework](http://doc.qt.io/qt-5/graphicsview.html).” There were a lot of widgets that I had to custom make such as the Timeline or the Canvas; it made my life much easier. It really is one of the nice features of Qt. If you’re making a heavily graphical application you should take a look into it.

Despite being able to get a basic animation loaded, edited and played back, I was starting to run into some issues with the development language: Python. I had issues with things like [circular imports](http://stackoverflow.com/questions/22187279/python-circular-importing) and nested imports (python files imported from many directories deep). I don’t want to go into the details of how they were affecting me and the project, but all I can say is that they were driving me up the wall. So I devised a solution: Switch to C++.

Now, switching development languages is not always something that’s advised. But at the point where I was, it was feasible to do and would possibly have a better impact on my project. Nested imports are a non-issue in C++ and the circular imports are fixed with simple [include guards](https://en.wikipedia.org/wiki/Include_guard). On top of that, I wouldn’t have to use PyQt’s bindings anymore and Python would not be a performance bottleneck since it would be gone. Working at my usual hour a day pace, it took somewhere between two and three weeks to port everything I had to C++. I wasn’t happy about losing that time to work on new features, but I think it was a better choice in the end.

I didn’t entirely ditch Python & PyQt. If I needed to prototype a widget, I would use those tools. It helped to realize ideas pretty quickly, then later I would integrate it into the C++ source.


## Feature Creep, “Future Planning,” and Broadening Horizons

In the first couple of months that I was working on Blit, more ideas started to pour into my head of what it could or should be able to do. We all know what this is; Feature Creep. Whenever I though of a cool new thing I wanted to add, I usually weighed the cost of adding it in within my current milestone, the next, or burring it in the issue tracker. This is where I developed the “Future Planning,” tag. If something popped into my head, almost 95% of the time I would not mark it under any milestone and put it under that tag. It was a good way for me to tell myself “*Alright, I think this would be a good thing, but I need to focus on other **stuff** right now.*” This worked actually pretty well for me. At all times, the most populous tag in my issue tracker was the “Future Planning,” one.



Around 100 days into the project, I felt like I had a good direction that I was going in. I was nearing the end of my (second) internship and I would be left with nearly two months before classes would begin again. With all of this free time, I set myself the goal of “Be able to draw a bouncing ball animation and export it as a Spritesheet,” before Christmas hit. I achieved that.




By this time you could move Cels around on the Frames, move the Frames on the Timeline, and adjust their hold values. I think I focused more on the staging of objects rather than editing them. To work on this shortcoming, I decided to start work on a Tool interface. I had the idea that editing tools should be plugins and people should be able to write their own; a very common idea in art applications. Instead of only “put pixel,” and “erase pixel,” I added line/shape drawing, filling, and was working on a soft brush tool.



When I got back to school I fulfilled that first goal of passing it as a “major project,” in my student group. It was well received for what it was at the time, a very simple pixel art animation tool. Though, I started to think more beyond simple spriting. Not only do I consider myself a fan of Animation, but someone who really enjoys making it. I started to ponder *“What if Blit could be used for all sorts of 2D animation, not just pixel art?”*



I didn’t think it would be too hard to add a camera hookup to the program (something that I’ve done with Qt before), so Blit could be turned into an application to do pencil tests, capture paper drawn animation, or even stop motion. My rule became “*If it’s Bitmap based, Blit should be able to do something with it.*” I also thought that there wasn’t a good free (both as in beer and speech) software solution to 2D computer animation. TVPaint, Dragonframe, and FlipBook were used a lot in the animation department. I can understand the expensive cost of them for professionals and that it’s niche software, but it really sucks for students who want to learn how to animate, but already were paying a small fortune for their college tuition.

To make Blit more generic, it had to undergo something I called dubbed “The Grand Refactoring.” The whole animation module was like this: an Animation owns an XSheet, which owns a list of Frames, where each Frame owns a list of Cels. No reuse. This was good to get started with, but pretty bad since in the real world animation is reused all of the damn time. So I devised up this system instead:



As it would force me to fix up almost every single thing in the program that touched the Animation module (including the file format), I set this to be its own “half milestone.” It took about a month and a half to complete. It really sucked not being to add any new features for that time; only endless refactoring. At the end of that, all the logic was in the code to be able stage the same Cel across multiple Frames, or instance a Frame multiple times in the Timeline. Though, because I was focused on fixing things up, I didn’t add in an interface where the user could actually reuse Cels and Frames. If they wanted to, they would have to edit the `sequence.xml`

file. So it was there, it worked, but wasn’t usable by the layman.

While taking classes and juggling other (smaller) projects it sometimes became difficult to make meaningful contributions to Blit. I tried to stick to my “one hour a day rule,” but that became hard. Also, refactoring isn’t fun. You don’t get to see new features, you’re restructuring stuff that already exist. You might also break things and then have to spend time fixing them. It’s hard to stay motivated when nothing is new or exciting.

My brain was fried after writing code for my class assignments. I found that (better) documenting the source code, reviewing issue tracker tickets, and revisiting design documents wasn’t too hard. If I recall correctly there was a two week stint were that was all that I did.



Despite all these speed bumps, I got to do something really cool with Blit at the end of the year. If you’ve read some of my older blog posts, you may have seen this thing I made called [MEGA_MATRIX](https://16bpp.net/blog/post/mega_matrix). For those of you who don’t know what it was, it is a 24x24 LED Dot Matrix display. I actually developed it in tandem with Blit during the early days of the application. Anyways, at the end of the year my college hosts what is essentially a campus wide show and tell day. I thought it would be neat If I could let people doodle animations in Blit, then upload them onto MEGA_MATRIX. Turns out it was. I made a special fork of Blit called “The MEGA_MATRIX Edition,” where I only let users draw in two colors (red and black), preview their animations, and then upload them to an Arduino to drive the display. One of my friends said it was his favorite thing at the festival because “*[I] practically made a hardware implementation of Mario Paint.*”




## Altered Scope, One Full Year, and the End of Development

At the beginning of 2015’s summer, I was off to my next internship. During the day I would write C# code for a rendering infrastructure. After work I would exercise, watch some TV, play a few video games, but also work on Blit, for well, at least an hour a day.



After “The Grand Refactoring,” and the MEGA_MATRIX Edition I was able to get a few more features out of the way. Changing the Canvas’ backdrop color, pixel grid, selective playback, a color picker tool and more. One of my favorite additions was onion skinning (I called it the Light Table). Thanks to the newly redesigned Animation module, it actually made it pretty easy to implement.

Then sometime in mid July I hit my second goal; hold onto a GitHub streak for one year straight.



The code for Blit was starting to get really huge at this point. I still was able to manage it myself, but it started to become a bit of a chore too. I also spent a lot more time refactoring and fixing existing code rather than working on new features. I feel like I lost a little of my drive then. As my two initial goals were achieved I could have stopped here. But for some reason, I didn’t want to. I kept on pushing.

My internship came to an end, I had a week at home, and then I was off to another internship. All of the previous places were I interned let me work on outside projects if I wanted to. As long as it wasn’t during work time, with work equipment, or a competing product I was free to do what I want. This time around, my employer asked me to stop working on outside projects all together.



While I felt that work on Blit was starting to go stale I still didn’t feel to happy about having to quit development. I could have worked on it in secret, but that didn’t feel right to me. So, right before leaving for the first day of work I made an early morning final commit to the Blit repo. It was kind of poetic that my ending streak was exactly 400 days long.



In the month that followed, I was bummed that I wasn’t able to add an interface for the reusable Cels/Frames, the Brush and Resize tools were still unfinished, no work on multiple planes was ever done (Cel layering existed though), but worst of all, I feel that it sucked when trying to make sprites; the original goal of Blit. I still had ideas popping into my head. Such as using FFmpeg to export animations as animated GIFs. All I could do is just scribble them down on some note paper and file it away for when I was done with my current internship.

So four months down the road I was done with my final practicum. Did I start back working on Blit? No. The previous month was pretty turbulent for me, as well as the next couple. It was my last semester at college and I was more focused on graduating. I still had ideas coming into my head for Blit, but they would go into the issue tracker instead of the code. I felt that I was way too out of it to startup work back on Blit. I also realized how much of a behemoth the source had become. Thus I decided to put it on hiatus indefinitely.


## Final Lookback and the Future

Almost everything I’ve done is a learning project for me. Some of I learnt very little from, others a lot. Working on Blit taught me so much more about Qt than I ever wanted to know. Hell, in the process of developing Blit I spotted a minor bug in Qt and was able to submit a(n) (accepted) patch to the project. That was one of the more rewarding moments, as I’ve never contributed to a major open source project before.

But the main thing I gained from Blit was learning how to manage/handle/organize a larger project. I was never involved with issue tracking, documentation, and design so much before. As stupid of an idea it was to maintain a year long GitHub streak, it somehow worked for me. It was fun to show off the streak to my friends, it was really there for me to motive myself.

While building Blit, one the things I always wanted to do was work on it with other people. Though, I kept it in a private repo I always had the intention of releasing the source code when I was done with some of the core features. While many of my friends thought it was interesting, I couldn’t find anyone else who wanted to work on it. I always made sure to keep good documentation of the design and source code for this reason. I really wish I had others to help me with this, not only so that I could have had Blit in a much further state, but also so I could learn how to collaborate with others better too.

It’s now been a year since I last touched Blit. At the beginning of this past Summer there was a monkey on my back to figure out “the future of Blit.” I know I wanted to release the source for it, but I’m not sure where I want to go with it. In the past year Dwango released [OpenToonz](https://opentoonz.github.io/e/) and [Krita](https://krita.org/en/) has added some animation tools. Both of these have **much** better drawing capabilities. It’s hard to compete.

I have a small desire to restart work on Blit. For example, adding a camera connection to shoot paper drawn animation or working on some FFmpeg exporting. But I have other priorities right now. If I had to do it again, I would want to write Blit in C# instead of C++. I’ve grown to love C# a lot in the past year and development in it is much easier than C++, and performance is still pretty good. I really hope that [QtSharp](https://github.com/ddobrev/QtSharp) can get off of the ground sometime soon.

If you want to check out the source for Blit, you can find it over here: [gitlab.com/define-private-public/blit](https://gitlab.com/define-private-public/blit). If you want to see some of my fabulous source documention, it’s at: [https://blit.gitlab.io/SourceDocs/](https://blit.gitlab.io/SourceDocs/). And if in the slightest chance that you’re interested in working on Blit, [please contact me](https://16bpp.net/contact).

To end with, here are some stats:

- 97 source code files
- 8,175 lines of code (95% C++)
- 400 days of contributions
- 364 issues tracked
- 3,151 commits
- 91,528 additions, 65,617 deletions
- An unknown amount of users
- and 1 developer (me)