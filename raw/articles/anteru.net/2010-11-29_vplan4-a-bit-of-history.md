---
title: 'VPlan4: A bit of history'
url: https://anteru.net/blog/2010/vplan4-a-bit-of-history
published: '2010-11-29'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Some of you might have already noticed that there is [a new page on VPlan4](http://sh13.net/projects/VPlan). VPlan4 is – as the name implies – the 4th complete rewrite of my small task planning tool. Before I ramble on a bit on VPlan4 itself and its development, let me take you on a trip into the past.

## Why VPlan?

VPlan is based on “[Getting things done](http://en.wikipedia.org/wiki/Getting_Things_Done)“, a very nice book by David Allen which describes a work-flow. That particular work-flow tries to maximize the time you spend on advancing various projects, for instance, some stuff at work or the long-overdue car repair. At the time VPlan1 was written, there were no web-based services like [remember the milk](http://www.rememberthemilk.com/) or [todoist](http://todoist.com/). So I went out to write a first small basic task-tracker.

## VPlan1

The original version: I had no clue back then what features to use, so I started with a very simple tree structure for everything (one tree only), with C#. Storage was done by serializing the tree, and the tree-view was very rudimentary. All of the UI was implemented using [WinForms](http://msdn.microsoft.com/en-us/library/dd30h2yb.aspx). There was no drag&drop, but it served as a test-bed for some prototyping. I quickly scrapped it once I wanted to implement projects (which group several tasks together.) The key take-away from VPlan1 was that a WinForms based UI is a workable path, and that the backend is key.

## VPlan2

The first VPlan I actually used for a longer time. Still written in C#, with a WinForms based UI, but a completely rewritten backend. Tasks where now stored as a table, and the tree structure was built on the fly. This gave some robustness improvements, but the WinForms UI was starting to become the limiting part. However, I had a much better separation now between UI and data, as the UI was just containing pointers into the data table and all manipulation was done on the database backend only.

## VPlan3

In order to finally get a nice UI, I turned to C# and [WPF](http://msdn.microsoft.com/en-us/library/ms754130.aspx) (at that time, the .NET 3.0 framework was brand new, and 3.5 SP1 was not yet announced.) The backend was switched to SQL Server Compact, which allowed for low-level consistence checking via foreign keys. I wrote a model for the database backend, and hooked it up to the UI.

However, choosing WPF was a double-edged sword: While I really liked the declarative approach, making an usable tree-view was totally overkill. For instance, I wanted check-boxes in the tree-view to close tasks (something which is dead easy in WinForms): However, WPF does not support this out of the box, and [the workarounds are rather cumbersome](http://www.codeproject.com/KB/WPF/TreeViewWithCheckBoxes.aspx). I also never managed drag&drop to work nicely, even though I spent quite some time on the UI. There were also a bunch of platform-related issues, like a 3-5 second startup (even on a pretty beefy machine!) and the high memory use (used to be 70 MiB with .NET 3.5, went down to 30 MiB with .NET 4 now.)

What was nice about VPlan3 was the backend, which made all changes ACID and thus pretty reliable. I also spent some time polishing the UI (nice messages, questions, hot-keys, etc.) and used VPlan3 quite a lot since then. Interestingly, it was again a total rewrite of VPlan2 – I couldn’t use much of the old code base, and all of the UI was completely rewritten from scratch.

## VPlan4

Fast-forward to 2010: I [started to use Linux](https://anteru.net/blog/2009/09/14/604/) for some of my development work, and I really wanted VPlan to run on Linux as well. In the meantime, all of the web-based tools have appeared with nice UIs, drag & drop, comfort functions etc. which VPlan lacked, so there was really some reason to give it another shot. I eventually turned away from C# and gave it a shot in C++ – to see how much work it actually is, and to get acquainted with Qt.

In the next weeks, I hope to get around to post a bit about the development experience and deploying. I’ve spent quite a bit of work this time to get a solid deployment and servicing story working on Windows, based around [MSI](http://msdn.microsoft.com/en-us/library/cc185688(v=VS.85).aspx) and [WiX](http://wix.codeplex.com/).