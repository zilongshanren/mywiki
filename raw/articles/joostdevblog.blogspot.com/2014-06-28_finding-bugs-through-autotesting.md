---
title: Finding bugs through autotesting
url: http://joostdevblog.blogspot.com/2014/06/finding-bugs-through-autotesting.html
author: Joost van Dongen
published: '2014-06-28'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[Swords & Soldiers](http://www.swordsandsoldiers.com)and

[Awesomenauts](http://www.awesomenauts.com)and found a bunch of issues this way.

Autotests are quite easy to build. The core idea is to let the game press random buttons automatically and leave it running for many hours. This is very simple to hack into the game. However, such a simplistic approach is also pretty ineffective: randomly pressing buttons might mean it takes ages to simply get from the menu to actual gameplay, let alone ever actually finishing any levels. It gets better if you make it a little bit smarter: increase the likelihood of pressing certain buttons, or even just automatically press the right button in certain menus to get through them quickly. With some simple modifications you can make sure the autotesting touches upon many different parts of the game.

![](../../assets/6dd350404e0a453e.jpg)

This kind of autotesting has very specific limited purposes. There are a lot of issues you will never find this way, like if animations are not playing, texts are not displaying, or characters are glitching through walls. The autotester does not care and keeps pressing random buttons. Basically anything that needs to be seen and interpreted is difficult to find with autotesting, unless you already know what you are looking for and can add a breakpoint in the right position beforehand.

Nevertheless there are important categories of issues that can be found very well through autotesting: crashes, soft-crashes and memory leaks. A soft-crash is a situation where the game does not actually crash, but the user cannot make anything happen any more. This happens for example if the game is waiting for a certain event but the event is never actually triggered. Memory leaks are when the game forgets to clean up memory after usage, causing the amount of memory the game uses to keep rising until it crashes. Especially subtle memory leaks can take many hours before they crash and are thus often never found during normal development and playtesting.

Another category of issues that can be found very well through autotesting is networking bugs. This one is very important for Awesomenauts, which has a complex matchmaking system and features like host migration that are hard to thoroughly test. Our autotesting automatically quits and joins matches all the time, potentially triggering all kinds of timing issues in the networking. If you leave enough computers randomly joining and quitting for long enough, almost any combination of timings is likely to happen at some point.

Recently we needed this in Awesomenauts. After we launched patch 2.5 a couple of users had reported a rare crash. We couldn't reproduce the crash, but did hear that in at least one case the connection was very laggy. Patch 2.5 added

[Skree](https://www.youtube.com/watch?v=bivUs3tNhTo), a character that uses several new gameplay features (most notably chain lightning and spawnable collision blocks). This made it likely that the crash was somewhere in Skree's netcode.

![](../../assets/41b00029cf28ac1a.jpg)

We tried reproducing the crash by playing with Skree for hours and triggering all kinds of situations by hand. To experiment with different bad network situations we used the great little tool

[Clumsy](http://jagt.github.io/clumsy/). However, we couldn't reproduce the crash.

I really wanted to find this issue, so I reinvigorated Awesomenauts' autotesting system. We had not used that in a while, so it was not fully functional anymore and lacked some features. After some work it functioned again. I made the autotester enter and leave matches every couple of minutes. Since I didn't know whether Skree was really the issue I made the game choose him more often, but not always. I also made the autotester select a random loadout for every match and made it immediately cheat to buy all upgrades. The autotester is not likely to accidentally buy upgrades otherwise, so I needed this to have upgrades tested as well.

I ran this test on around ten computers during the soccer match Netherlands-Australia. While we beat the Australians our computers were beating this bug. Using Clumsy I gave some of those computers really high artificial packet loss, out-of-order and packet duplication.

Watching the computer press random buttons is surprisingly captivating, especially as it might leave the match at any moment. Simple things like a computer being stuck next to a low wall become exciting events: will it manage to press jump before quitting the match?

Here is a video showing a capture of four different computers running our autotest. The audio is from the bottom-left view. Note how the autotester sometimes randomly goes back to the menu, and can even randomly trigger a win (autotesters are not tactical enough to destroy the base otherwise):

And indeed, after a couple of hours already three computers had crashed! Since I had enabled

[full crash dumps in Windows](http://msdn.microsoft.com/en-us/library/windows/desktop/bb787181(v=vs.85).aspx), I could load up the debugger and see exactly what the code was doing when it was crashing.

The bug turned out to be quite nice: it required a very specific situation in combination with network packets going out of order in a specific way. When Skree dies just after he has started a chain lightning attack, the game first sends a chain lighting packet and then a character destroy packet. If these go out of order because of a really bad internet connection, the character destroy packet can arrive first. In this case the Skree has already been destroyed when his lightning packet is received. Chain lightning always happens between two characters, so the game needs both Skree and his target to create a chain lightning.

Of course we know that this kind of thing can happen when sending messages over the internet, so our code actually did check whether Skree and his target still existed. However, due to a typo it also created the chain lightning if only

*one*of the two characters existed, instead of if they both existed. This caused the crash. Crashes are often just little typos, and in this case accidentally typing || ("OR") instead of && ("AND") caused this crash.

Once we knew where the bug was, it was really easy to fix it (the fix went live in

[hotfix 2.5.2](http://www.awesomenauts.com/forum/viewtopic.php?f=6&t=2440)). Thus the trick was not in fixing the code, but in reproducing the issue. This is a common situation in game programming and autotesting is a great tool to help reproduce and find certain types of issues.

Sweet. And funny to see the random input at work.

ReplyDeletenow i jsut want to see the full code of this auto tester:)

ReplyDeleteWith this crash dump you load the debugger?

ReplyDeleteNot sure what you mean.

Do you load a dump file in the VS debugger?

Yes, the crash dump contains the entire state of the game at the time of the crash, so when loading that into the VS debugger I can see the stack and exactly which line of code crashed.

DeleteGoi it.

DeleteYour blog is full of interesting things each post.

Success for your projects!