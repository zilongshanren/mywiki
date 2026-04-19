---
title: Dolphin Releases Announcement
url: https://dolphin-emu.org/blog/2024/07/02/dolphin-releases-announcement/
author: MayImilae
published: '2024-07-02'
source_blog: Dolphin Emulator - GameCube/Wii games on PC
source_site: https://dolphin-emu.org/
category: graphics
fetched: '2026-04-19'
---

On the 24th of June, 2016, [Dolphin 5.0 was released](https://dolphin-emu.org/blog/2016/06/24/dolphin-50-release/). The product of a long and hard transition period, the fundamental inaccuracies that plagued Dolphin for over a decade had successfully been undone, and Dolphin was now free of its burdens to swim forward into a new era of accuracy and performance.

Eight years have passed since that great release, and we have seen the dividends of that effort time and time again. Dolphin has seen constant updates, with new features and enhancements coming side by side with bug fixes and stability improvements. Users are now able to upgrade without fear, knowing that even in the unlikely event of a bug it will be fixed *within hours*. And of the thousands of titles that Dolphin can run, the number that do not function can now be counted on one hand!

All of this was achieved *without* a new release. In fact, Dolphin has been in the 5.0 era longer than any other, and with almost *twenty-two thousand* commits over the past eight years, the 5.0 era now makes up *over half* of Dolphin's entire commit history! But users haven't forgotten our past releases. They have been waiting for years, patiently anticipating when our next release may arrive.

That wait ends today.

However, the purpose of our old stable builds is now no longer relevant to Dolphin Emulator. We no longer need a benchmark to compare against or an anchor to ground us. We have grown beyond them. So in leaving the 5.0 era behind, we are also leaving behind that release scheme and all it offered. In exchange, we're not *just* giving you a release today, but also a commitment to *continuous releases from now on*. The long drought of Dolphin releases is no more and will never happen again!

Welcome to a new era of Dolphin Emulator - the Release Era!

### Announcement[¶](https://dolphin-emu.org#announcement)

We are pleased to announce that Dolphin has adopted a **rolling release cycle!** Building upon our highly successful "beta builds", we will have a release every few months, with a Progress Report launched alongside as a changelog. These are proper release builds however, with the full infrastructure and support that comes with them. They are tagged as releases in Git, allowing our distribution partners to properly support us and our users. Our new releases can receive hotfixes, so if any issues arises we can release small updates instead of a full on new release. And, of course, every release will advance Dolphin's version number.

However, our new releases are fundamentally different from our prior releases, so we didn't want to just add a number to our last release. As such, we are abandoning the X.0 release numbering and moving to a new date-based versioning scheme!

Accompanying this article is our first rolling release - **Dolphin 2407**! This release is available for download *immediately*, for Windows x86-64, Windows ARM64, macOS, and Android [from our official website: dolphin-emu.org.](https://dolphin-emu.org/download/)

Here are the details of the new rolling release scheme:

- The first two digits are the year, and the second two are the month. 2407 codifies a release from July 2024.
- All subsequent dev builds after a release will be numbers added on to it. For example, 144 commits after 2409 would result in dev build 2409-144.
- Our next release will be 240X. Yes, it will be in just a few months from now!
- Hotfix releases will have the addition of a suffix. For example, a single hotfix to Dolphin 2409 would be "Dolphin 2409a".
- Beta builds are being replaced by releases. All users in the beta update track will be moved to the new release track.

### A New Look![¶](../../assets/1964a373ba45b85a.img)

To herald and symbolize this new era, we also have a new logo! MayImilae, the designer of our previous logo and long term Dolphin blog writer and contributor, has refreshed our logo for the modern day!







Here is the explanation of the design, in her own words.



Dolphin's 2013 logo was designed at the start of a transition. Dolphin was leaving its buggy past behind and committing to doing it right, even if it meant ripping out tons of working code. So gone was the silly[peace sign mario], and in its place I made a sharp, edgy, serious, on-trend logo to symbolize Dolphin's new future as aseriousemulator. And yea, that's carried us through all this way! However, Dolphin is more mature now. It's stable, confident and comfortable in its place. So for the refresh, I wanted to return to the original design and make it timeless, but also more fun, more colorful, and make it a little gentler and thicker.And finally address all the things that were bugging me for ten years.


This new logo has already been rolled out in our system and brands Dolphin 2407! However we couldn't get *every* little logo replaced before the release, so the few that remain will be cleaned up soon.

![](../../assets/9970057e98d20469.png)

### But why not 6.0?[¶](https://dolphin-emu.org#but-why-not-60)

As we leave the 5.0 era behind, we feel the need to address what might have been - 6.0. While we lightly touched on the reasons above, we know that won't be enough for those who waited *so long* for something that we kind of didn't deliver. However, to explain this properly we're going to need to go in depth, and tell the story of Dolphin's releases.

When Dolphin was a closed source project, beginning in 2003, it benefited from being made by *excellent* programmers. Code from that era is of the highest quality and has stood the test of time. For example, most of our interpreter *has not even been touched in over 15 years!* It has been added to, but very little of the interpreter code from that period has been altered. But there was only so much that a handful of quality coders could do in their spare time. It took **years** for Dolphin to approach even a proof of concept, let alone become an actual working emulator with decent features and game compatibility. So in 2008, the founders of Dolphin decided to enter the wild world of open source.

With the floodgates open, contributions *poured in.* In just a couple of years, Dolphin became a full blown emulator, with tons of new features and the ability to play most games! But the move to open source was not without its drawbacks. While Dolphin was getting the help of hundreds of new developers, the code quality of the project *plummeted*. The tools available at the time simply didn't allow for quality development.

Back when Dolphin went open source, modern development platforms like GitHub didn't exist!* There were no pull requests. There was no way to easily review code and an accompanying forum for discussing the changes before they were checked in or merged. Instead, all development was handled through *IRC* and * Google Code*, which was more of an issue tracker with a bolted on hosting service than a development platform in the modern sense.

In this era, to submit a change to Dolphin developers would *show their change to a developer with commit access in IRC* and ask them to merge their patch. This was a form of review, but it was slow, cumbersome, and

*overwhelming*for maintainers. So once a developer was known to the project, a maintainer would give that developer commit access and

**they could just commit anything without review from that point forward.**

Today, this would be considered *irresponsible and reckless*. But at the time, we had little choice. With terrible tools, difficult to impossible review processes, and a desperate need for contributions, Dolphin flew open the doors and allowed *thousands* of changes without review.

That decision proved to be highly effective in the short term, and Dolphin exploded in functionality and capability. But code of all quality was being let into the project, both good and bad, and the health of Dolphin's codebase slowly declined. After a few years, Dolphin began to buckle. By 2010, Dolphin was buggy and unstable, and development builds would often break for days at a time! With no access to modern tools, Dolphin needed something to ground itself in the raging sea that was open source in the late aughts.

Dolphin needed an anchor.

And so, Dolphin adopted the Stable Release model. In that release formula, a new Stable Release must have *all regressions* since the last release resolved, no matter how minor. This would allow releases to serve as a benchmark, a minimum standard that Dolphin would never fall below and would always improve upon with each new release. This meant that no matter how chaotic the development process may be, users knew that if they went from release to release, Dolphin would *always* be better in every way.

However, Dolphin is a volunteer project, and everyone is committing their free time. To get volunteers to drop their fun projects and work on tedious regression fixes, Dolphin used **feature freezes**.

During a feature freeze, all merges are **halted** except bugfixes. Once all of the regressions from the previous release are resolved, Dolphin would launch a Stable Release, and then feature merges would reopen. By holding developers' fun projects *hostage,* feature freezes coerced developers to contribute to the bug hunt. After all, the more developers pitched in and fixed bugs, the sooner their cool project could get merged into Dolphin! And it worked. Bugs were fixed and Stable Releases were launched. However, feature freezes were miserable and **costly**. During a freeze, Dolphin's development would stall for months at a time, morale would plummet, new developers were repulsed, and sometimes long-term developers would get tired of it all *and just leave.*

Of course we hoped to find a better way, and with each Stable Release we tried some variation or alternative to feature freezes. None of them succeeded. After 5.0's feature freeze alternative failed so badly that [we had to restart the release process over from scratch](https://dolphin-emu.org/blog/2015/11/01/dolphin-progress-report-october-2015/), we had had enough, and made a collective decision to put releases away for a while. No one wanted to deal with a feature freeze again.

Fortunately, we have not needed to. The transition to stability that 5.0 crowned, combined with the advent of modern development tools, has completely changed our development process. Now, every change is reviewed and checked *before* it is merged. Rather than hurry through messy development and then clean up after, cleanliness and stability *is our every day!* We no longer need to periodically stop everything and clean up our mess! **We no longer need Stable Releases!**

Theoretically, we could have just... not prepared a release ever again. We could have stayed in the 5.0 era forever! However, there are a lot of benefits to releases - for infrastructure, support, and distribution. We wanted to take advantage of those. But we were not going to do a Stable Release again. So after much deliberation and a lengthy development process, we have adopted a rolling release model.

And to codify just how vastly different our new releases are from our previous ones, we also adopted a new versioning scheme. Gone are the X.0 numbers, and with it, 6.0.

### Credits[¶](https://dolphin-emu.org#credits)

Approximately *six hundred people* contributed to Dolphin in some manner during the 5.0 era. There are far too many people to list all of them individually in this article, so we're going to call out the groups that have made Dolphin what it is today!

Dolphin would never have gotten to where we are today without the hundreds of developers who have volunteered to make Dolphin better. The 5.0 era saw many long awaited features like [Ubershaders](https://dolphin-emu.org/blog/2017/07/30/ubershaders/), the [Unification of VideoCommon](https://dolphin-emu.org/blog/2019/04/01/the-new-era-of-video-backends/), [Hybrid XFB](https://dolphin-emu.org/blog/2017/11/19/hybridxfb/), [MotionPlus Emulation](https://dolphin-emu.org/blog/2019/04/26/mastering-motion/), the [Qt user interface](https://dolphin-emu.org/blog/2018/05/02/legend-dolphin-lens-between-worlds/), [Bluetooth Passthrough](https://dolphin-emu.org/blog/2016/10/24/bluetooth-passthrough/), many new graphics backends, and much much MUCH more! This was only possible because of the tremendous effort of the brilliant engineers who volunteer their time to Dolphin!

The great vanguards of support, [our Discord](https://discord.dolphin-emu.org/) moderators and support staff have been assisting users for years, even before our Discord was official! The sheer quantity of users that our Discord is able to help boggles the mind.

The core pillar of support remains our [forum](https://forums.dolphin-emu.org/). Filled with over a decade of history and our support veterans, our forum is where our support staff go for support.

[Our Wiki](https://wiki.dolphin-emu.org/) team maintains and curates our greatest collective of knowledge for how games perform. *Thousands* of games are recorded, with thousands of bugs (mostly fixed), workarounds, and game quirks, and tens of thousands of user testing reports!

Dolphin is available in **29** different languages! This is entirely thanks to the members of [our translation team](https://forums.dolphin-emu.org/Thread-dolphin-translation-moving-to-transifex), who volunteer their free time to regularly keep our translations up to date.

And of course, this article wouldn't be possible without our blog team! We're not going to praise ourselves beyond that, it's weird.

We will however take a moment to specifically call out those who made this release happen!

**delroth**championed and planned out our new release scheme, and then reworked our infrastructure to get Dolphin ready for it. He retired before it was all complete, but this release was largely his project, and it would have never happened without him!**OatmealDome**picked up where delroth left off, implementing delroth's release proposal and carrying it to the finish line!- Of course Android would require special attention.
**JosJuice**sorted out all of the kinks and got our Android builder ready for*Android's first ever Dolphin release!* **mbc07**readied our wiki for the biggest release change in its history.**MayImilae**commented on the new release plan, with interest. Also she designed the new logo, helped coordinate the launch, and wrote this article.