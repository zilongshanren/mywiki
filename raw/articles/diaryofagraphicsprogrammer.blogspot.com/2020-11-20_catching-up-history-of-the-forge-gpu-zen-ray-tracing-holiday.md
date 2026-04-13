---
title: Catching Up / History of The Forge / GPU Zen / Ray Tracing / Holiday Dinner
url: http://diaryofagraphicsprogrammer.blogspot.com/2020/11/catching-up-history-of-forge-gpu-zen.html
author: Wolfgang Engel
published: '2020-11-20'
source_blog: Diary of a Graphics Programmer
source_site: http://diaryofagraphicsprogrammer.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I just realized I haven't posted here since 2018. There is generally less sharing of information happening now compared to let's say 10 years ago and I seem to have become one of the people who shares less. In my defense, I can bring up good reasons :-) :

Being part of an ever-growing company with increasing business and HR needs makes it harder for me to focus on the technical aspects of our work in a blog post. Dealing with the development of The Forge, H1-B or O1 Visas, 401k plans, lunch reimbursements, deciding what health insurances to offer, writing contracts and invoices and keeping track of all the money movements, deciding where the holiday dinner should happen, and spending time with interviewing all the new hires, the landlord of our office building, bookkeepers, tax advisors, IP lawyers, and other lawyers leaves much less time for this. Before I can write the blog post I need to decide how we will have a Holiday dinner this year.

With COVID-19 I also began training in two more Martial Arts after practicing Tang Soo Do for more than 11 years: Gum Do and Tai Chi. When working from home it helps with the stress levels to just step outside and listen to the wooshing sound of a Sword splitting the air. Tai Chi is something I do together with my wife, which makes this activity even more valuable.

So now that my defense was laid out, let's get back to business.

One of the interesting things we did was open-source our internal rendering framework. The company is using an internal framework since day 1 of its existence.

This rendering framework is kind of like the "beehive mind" of the company. Over the years some of the best people in the company were invited to extend this framework and then the whole company benefitted from its existence as a blueprint for typical rendering tasks.

In 2017 we decided to write a new rendering framework from scratch because we wanted to cover the new Graphics APIs better and needed fundamental changes in the architecture of our old framework. This framework was open-sourced at the beginning of 2018 and since then steadily improved. We named it "The Forge" because with its help we can create new tools, game engines, experiences. It is shipping in AAA custom game engines, smaller things like editors or educational apps, in the future on hundreds of million devices as the foundation of business frameworks. We used it also to write a new game engine for Supergiant that shipped Hades so far on PC, macOS, and Switch.

With every release of The Forge, I write release notes in the style of blog posts. I offer an opinion on why we implemented things the way they were or often describe what went wrong and how we had to rewrite the same sub-system 3 or more times. I describe our technical successes and our failures :-)

I am hoping the release notes are partially making up for the lack of blog posts here. After all, one can look at the source code in its entirety and see what I am talking about. Something my blog posts didn't always offer in the past. Generally, the lack of source code makes a lot of presentations or descriptions of technical implementations less valuable.

Regarding GPU Zen: helping aspiring and experienced graphics programmers was always a goal of mine. I consider The Forge now more useful than a new edition of GPU Zen. It provides the actual code and you can see it working in the games it shipped with or will be shipping with. Compared to a conference talk or a book chapter, this is really what everyone would want to see. I believe a presentation that outlines a technique accompanied by a math equation doesn't offer that same level of usefulness. Showing source code is the ultimate way to share graphics programming knowledge.

So you can think of "The Forge" in GitHub as the next-gen GPU Zen. That doesn't mean we won't do another GPU Zen in the future. It just means we have to think about the value proposition this future book will offer.

Ray Tracing: my last blog post on this topic made some waves in the industry. At some point, I couldn't really dedicate as much time to this topic as I wanted. It came up in Advisory boards, there were IP related projects we worked on regarding Ray Tracing and we -as an industry- eventually succeeded in getting a more open interface.

My company gave a talk on cross-platform Ray Tracing where the macOS / iOS ray tracing run-time was extended to be on par with the DXR / RTX run-time (available in the GitHub repository). This was mostly meant for tool development but can also be used in a cross-platform game engine. I think it also shows a blueprint of how to do Ray Tracing with the newer interfaces on various platforms.

Holiday dinner: before I wrote this blog post, I organized the first Holiday dinner via Skype. My colleagues in the PST time zone will dial in via Skype. They will get food via DoorDash and the company will reimburse it. This will be a good time to see how everyone's family has grown, what the dogs are doing etc.. :-) I will then repeat a dinner/breakfast with the colleagues in the different time zones we cover.

## 2 comments:

Coming in 2021, Wolfgang starts a band!

Ha ha that would be nice!

Post a Comment