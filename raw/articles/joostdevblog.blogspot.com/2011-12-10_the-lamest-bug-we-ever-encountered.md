---
title: The lamest bug we ever encountered
url: http://joostdevblog.blogspot.com/2011/12/lamest-bug-we-ever-encountered.html
author: Joost van Dongen
published: '2011-12-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

In the past half year we have seen a really rare bug occur about once per month in

[Awesomenauts](http://www.awesomenauts.com)on the Playstation 3: suddenly the game would freeze for anywhere between 10 to 100 seconds, and then continue normally as if nothing weird had happened. We always have a PC connected to collect logs from the game. However, the log printed nothing interesting and showed simply the framerate, which is printed once per second:

13:48:13 60fps

13:48:14 60fps

13:49:21 1fps

13:49:22 60fps

From this we concluded that the issue must be in some part of code that does not log anything. That leaves 99% and with a codebase of at least 150,000 lines, that is

*a lot*!

Since this issue was so rare and we hadn't seen it in months, we had closed it. We thought it was an anomaly that we couldn't find or fix and that had somehow disappeared.

Until we were testing our latest build last Thursday. We were playing on seven Playstation 3 devkits, when suddenly 4 of them froze for about 90 seconds. Argh! We thought this really difficult bug had magically disappeared, and now it was back, with a vengeance! We cannot leave a bug in that happens so massively on all these consoles at once!

Again, no relevant logging. Yet something really interesting nevertheless: these Playstations were in different online matches, so they weren't even talking to each other! So how could they all freeze at the exact same time? We concluded that the only thing they had in common, was that they all talk to the same Sony matchmaking servers, so we started investigating all our code related to that. However, we couldn't find anything relevant.

So we added a lot more logging, and did some really advanced stuff to get more info on the stack during the freeze (which is difficult to get from an executable that has been stripped of all debugging info), and started playing again. I let the Playstations perform our automatic testing all night, and the bug didn't happen. Then we played the game for five more hours with the entire team and BAM!, it

*finally*happened again on two consoles!

This time, we had more info, and it turned out that the spot where the game froze was different on both freezing consoles, and both did not contain

*any*calls to Sony's matchmaking servers. In fact, it was in between two logging calls, in a spot where nothing relevant was happening. So we concluded there were only two possible causes: either other threads were hogging the entire CPU (due to how the scheduling system on the Playstation 3 works, high priority threads can do this permanently), or the logging itself was broken.

So we started experimenting around that, and now we quickly found the cause of this 'bug':

*when the PC that is tracking logs goes into sleep mode, the connected consoles freeze a little while later; once the PC is awoken once more, the consoles continue as well a little later*. The PC that was tracking the logs automatically went into sleep mode after not touching it for 30 minutes. This only happened during extensive play-testing, because people normally actually use that PC. So it wasn't even a bug in our code! ARGH! Especially since logging is turned off in the release build...

This may all seem really obvious in hindsight, but in general when we have a bug/freeze/crash it is in our own code, not in one of the tools we use. With such a big codebase, it is easy to not even think about something else. Also, in the chaos of 14 people playing the game on 7 consoles, it is easy to overlook one specific PC going into Sleep mode a little bit before the consoles freeze... Also, I still don't know why not

*all*consoles connected to that PC froze.

So, this hard to find and very persistent bug turned out not to even be a bug! And what do we learn from this? Two things:

1. Really nasty bugs are often in a totally different spot than where you are looking.

2. Sometimes you encounter the lamest and most frustrating stuff while programming games!

Hahaha, at least you got a great story out of it!

ReplyDeleteI totally know the feeling of finally figuring out what the problem is! :) Glad you were able to figure it out in the end.

ReplyDeleteWhy would a logging server ever go to sleep? That makes no sense to me. You were using a Windows box with a screensaver or something as a server in a dev shop? That seems like the real lame part here.

ReplyDeleteI spent about a week on a similar bug in the 1990s on an avionics test rig. The test suite would freeze for a certain amount of time, always exactly an hour after the start of the test. It turned out the screensaver on the Windows machine we were using as the test controller was hogging 90% of the CPU... Lame indeed, but it taught me a lot about looking for bugs where you least expect them.

ReplyDeleteHidden lesson #3... never call a remote service without a timeout.

ReplyDeleteThe other day I spent an hour or so trying to figure out why a GUI element wasn't being updated when I set its label attribute. Eventually I realised it was because I was setting its label instead of Label. Because I was writing in Python, it just bound a new lower case attribute to the GUI object, and went merrily on its way.


ReplyDeleteInterestingly, I've been using Python for about 6 months now, and this was the first time I'd made the mistake of mistyping an attribute name and not picked up on it quickly.

Sorry guys, Like another Anonymous said; the only way that a development team should use a "Windows machine" with "testing proposes" is for internet explorer related stuff, malware, etc

ReplyDeleteReminds me of a bug where the logging was causing a bug. There was some delicate timing between 2 function calls that we needed; put a log statement there, and it screwed up. We realized only a couple of hrs later what happened.

ReplyDeleteI think you could have solved this a *lot* faster by using the core dump feature. After the machine starts hanging, tell it to generate a core dump. Then read the callstack for each thread from the core dump and use the app .map file or the addr2line.exe utility to tell where the hang is.


ReplyDeleteAlso, your entry above seems to be blaming the server for your problems, but unless you're leaving something out it's not the server's fault but your app's fault. You shouldn't be using blocking sockets calls on your main thread or any thread that shouldn't be blocked. Even if the server was guaranteed to be available, the latency of sockets calls is more than you want to have in a main thread that the frame rate is dependent on.

Been there done that :D. I know the feeling, a relief that the issue is closed and frustration that you spent 2 days on it. And you know, this is not the last time it will happen. Hopefully next time it will take only some hours to find it.

ReplyDeleteI'll keep that one in mind! A real 'think outside the box' issue, literally! PS3 debugging has always been a pain in the arse, I had no idea that the PC could even attempt to sleep while it's running, it defies logic! Good story bro :P

ReplyDeleteA couple of misconceptions in the comments here:



ReplyDelete-Using Windows for developing on game consoles is mandatory because of the tools Microsoft/Sony/Nintendo provide.

-Yes, external calls should usually not be blocking. But we didn't program the socket ourselves, this is just a standard PS3 function.

One bug took three of us a week to figure out why an ldap call was being misinterpreted. Eventually a tester stood behind us and said




ReplyDelete"That string should start with 'T' not 't'

The documentation said 't' not 'T'

Not as lame as yours but still annoying

I'm not fully convinced of the solution you've found... Are you sure it was because of that PC going into sleep mode? How did you prove this? The fact that not all consoles connected to it froze means that there's something else.



ReplyDeleteAnother observation: I believe logging should be done asynchronously (without blocking the execution of the main program).

An2

We had a test rig running SQL Server in the early noughties. Performance would suddenly fall through the floor.


ReplyDeleteYep - it was the screen saver on the server. Ye gods.

To many times I've searched code that looks 100% correct for elusive bugs. So far they always turn out the be a programmer error, no matter how much it looked like it was the base code. Having encountered this so many times over the years I've developed a phrase "It is always the programmer's code causing the error, no matter how unbelievable that may seem", now you've given me some food for thought.

ReplyDeleteI too always suspect my own code first. Which is exactly why it took us so long to find this one... ;)


ReplyDeleteAs for proving sleep mode was the cause: when we discovered this cause, we just let the PC sleep a couple of times and we saw the console connected to it freeze every time. So we were able to reproduce the exact error we had, and the way it happened was likely to happen specifically after we had been playing for a while, just like the situation when we saw the bug happen initially.

As a novice programmer who has knowledge of PS3 programming, if I were in your shoes I definitely would have assumed to the death that it was a job scheduling problem. lol.


ReplyDeleteVery interesting!

As a standard we don't put any intense screen savers on our servers. We also don't set them to go to sleep either.

ReplyDeleteThe worst bug I ever had was in a game I wrote in the 1980s in 6502 assembler for the BBC Micro computer.






ReplyDeleteIt had 7 levels and all levels were different. I wrote it in order level 1,2,3 etc.

Occsaionally the program would crash while playing level 7. I could not reproduce the bug initially and the symptoms crash were often different.

After a WEEK of detective work I found a bug in a small part of the level 2 code. This code, if you did things in a certain way, incorrectly wrote a single byte to the wrong address which was high up in memory.

That place, high up in memory, was the code for level 7 part of the game.

In the end, I found the bug by literally reading the code and checking for any errors. Luckily the bug was near the start else I'd still be reading the code!!!

lol... I know exactly what you mean about that bug. I am an out-of-work application developer myself and I have had a similar experience. I know as well as you do just how good it feels to find out that you didn't screw up after all. :D

ReplyDeletebtw my post is to the original post by Joost.

ReplyDelete"Hidden lesson #3... never call a remote service without a timeout."



ReplyDeleteI beg to disagree. In my book it reads: "Never perform a a blocking call to a remote service.". Do it on a separate thread, if there's no non-blocking interface available.

OTOH, I know nothing about PS3 programming, maybe there's no threading there - but I'd doubt it.

Yeah, sounds like a bug in the basecode/SDK'S interaction with external logger that is either already known or should be reported and fixed.

ReplyDeleteI think the fix on the side of the Playstation logging library would probably be to simply disconnect from the PC when the PC goes to Sleep, just like it does when the PC is turned off. :)

ReplyDeleteThe "I told you so's" are what's really lame here. Thanks for sharing your adventure with us. We have all been there!

ReplyDeleteYou will note that he never said the logging machine was a server. He called a PC. If it was a Windows PC then by default it has a power plan that does go into sleep mode.


ReplyDeleteYeah, its a lame 'bug' but you figured it out and now it is intellectual capital. I admire you for creating your own video game.

I don't know -- hangup in the logging mechanism was the first thing I thought of...

ReplyDeleteWindows going to sleep is a very common defect in the the first test takes a long time in my experience. (Not that I spotted it here, or would have spotted it here.) What I don't understand is why it is so common. It keeps coming around again. I'd certainly put Windows power management up there with premature optimization as roots of development evil.

ReplyDelete"So it wasn't even a bug in our code!" !?!?

ReplyDeletew.t.f. was it then!? fix your logging code to check for sleep mode....jeez

I always say, the most complicate looking or hard to find bug, always has an easy fix. Where as those that look like an easy fix, always end up being a complicate change to make it work.


ReplyDeleteGlad you resolved your issue....or features as I like to call them. :)

The most frustrating bug I have had to find was in a very large enterprise C++ application.





ReplyDeleteCode was writing into the 100th item in an array that went from 0 - 99.

The problem was the application didn't crap out straight away. It would keep running for a bit. This meant the call stack where the crash actually occurred didn't point to the cause of the problem. Took me days to find.

Running the code in debug mode and adding breakpoints would add padding and cause the problem to go away. In hind site perhaps there were some better debugging techniques I could have used, but I really didn't have any idea of the cause.

The surprising thing is that the memory seemed to behave the same every time, and the app would crash at exactly the same place.

Oh, and by the way when it came to fixing the bug it was a one line fix!

ReplyDeleteAny experienced programmer has learned to ALWAYS presume that the fault is in his code.


ReplyDeleteThat being said, it reminds me of the time we hauled out the logic anayser to discover that something was unplugged!

I feel your pain. Never actually been subject to a third party failure of that nature before...but I do have a similar one.



ReplyDeleteOur code uses a legacy "black box" library that we started using WAAAYYYY back when, pre-.NET 1.1 stuff. Well, now, we have too much code, and not enough budget, to re-write all the sections that use this library. Cumbersome, but usually not too much of a big deal...unless you start running into a stack overflow error that originates inside said black box. It turns out...there are just some things you cannot use it for, even though if you program the damn code yourself, not using the library, it works JUST FINE!!!!

Took me most of a week to finally accept the fact that it was NOT in fact my code that was causing the issue.

Moral of the story: Servers don't go to sleep.

ReplyDeletethat moment when you look for anything wrong in the wrong place. that was funny. i'd certainly laugh at myself if i'll encounter the same thing. (:

ReplyDeleteWe had a customer in the 90's that was running a test suite against a DB running on the biggest machine I had ever seen at the time--a huge 16-processor machine with it's own 2-ton power transformer. The multi-threaded tests should have been flying, but they were crawling. We checked their SQL commands, stored procedured, index definitions, server execution plans, analyzed the code for deadlocked critical sections. Couldn't find anything wrong. Then one guy realized the control program was logging each event to a windowed command console, and the machine had a crappy 8 MB PCI video card in it. Without making ANY code changes we redirected stdout to a file and man did that thing take off!

ReplyDeleteI learn something from this, never let your PC sleep XD

ReplyDeleteHaving a lot of experience in troubleshooting.. too many to admit.. but it started back in the day when I was in the Navy Nuclear Power Program. Troubleshooting is an art and a science. Too much on one side or the other and you end up chasing your tail. There are several idiot posts in this thread talking about whose fault.. etc.. Bottom line.. problem solved, lesson learned, and thanks for sharing.



ReplyDeleteRemember:

Dumb people do notlearn from thier mistakes

Smart people learn from their mistakes

Highly Intelligent people learn from the mistakes of others..

SR

The logging issue is a bug because you got unexpected behavior. When logging, you should always use UDP as the logging protocol to avoid blocking along with asynchronous method calls. To verify that you fixed the bug, the unexpected behavior should be repeatable. Put the fix in place and the bug goes away; remove the fix and the exact same bug reoccurs as expected.

ReplyDeleteWell, thanx for sharing, everybody here is right .. many times the issues known as small issues takes u too the hell of frustration and if resolved then to the heaven of happiness.. perfectly said as ..

ReplyDelete"90% of the project takes 50% of your efforts and the rest 10% takes the another 50% of your efforts"

The hardest bugs to fix that take incredible amounts of time, energy, and thought are the ones were nothing was ever broken to begin with.


ReplyDeleteIn this case, replication of the issue may have been part of the camouflage. But whenever you can, replicate the issue. Otherwise you may find yourself fixing the hardest bug to track down of your entire career.

I remember years ago programming a CD Player program and it was ALWAYS crash at 2 minutes 38 seconds into playing a track, but it would only do it on Windows 98/95 machines. Since I had NT 4, it never happened to me. Had to go buy Windows 98 and run it to see what was going on. Turns out that there were timer events that were calling themselves multiple times when one of the events took too long. The MCI interface got "confused" and just crashed.... stopped the entire CD MCI interface, but only on non-NT kernels.


ReplyDeleteBut in other programs, there are weird issues that are unrelated to you and are bugs in something else that cause everything to fail even though it works on your machine. Once you find them, you say that it was so obvious that you can't believe you didn't think of it before.... those are the lessons you don't forget. :)

My favorite logging bug occurred when we "improved" NT event logging in our production server monitoring product. We added improved log reading into the agent and comprensive log writes into our back-end server in the same release cycle. Our poor soul first Beta user put the build into his enviroment, configured emails for events, and sat back to enjoy....until the server coughed, raised a log write caught by the agent, sent an email, coughed again, then all together rip-roared through a positive feedback cycle to send thousands of emails, crushing the server, Exchange, Outlook, etc. while the agent went merrily along firing more and faster event notices. Looking back, this should have been an obvious phenomenon and understood long before Beta, but it never surfaced in any QA testing. Bugs that span processes and compute nodes can cetainly be devilish to contain and root out.

ReplyDelete