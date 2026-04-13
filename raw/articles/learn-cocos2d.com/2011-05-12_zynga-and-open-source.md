---
title: Zynga and Open Source
url: http://www.learn-cocos2d.com/2011/05/zynga-open-source/
author: MagnetiCat says
published: '2011-05-12'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I did a little research to figure out more about Zynga’s involvements in open source projects. The research is not comprehensive nor conclusive but provides a little more insight. At least as much as is possible from a corporation with PR departments.

### Membase

[This article reports on Zynga’s involvement](http://news.cnet.com/8301-13846_3-20008251-62.html) as follows:

Casual-game provider Zynga found that its efforts to manage the load of its database operations dovetailed with work being done at NorthScale and NHN and decided to contribute research findings and to the open-source community, as well as sponsoring continuing efforts to maintain and enhance the software.


Sponsoring efforts to maintain and enhance. Sponsoring means there’s money or manpower going into the project. Zynga looks forward to advancing Cocos2D. Notice the difference.

[Another article on the same subject](http://www.marketwire.com/press-release/NorthScale-Zynga-NHN-Establish-Membase-Open-Source-Project-Contribute-NoSQL-Database-1280336.htm) quotes Zynga’s CTO Cadir Lee:

“Zynga’s objective was simple: we needed a database that could keep up with the challenging demands of our games while minimizing our average, fully-loaded cost per database operation — including capital equipment, management costs and developer productivity. We evaluated many NoSQL database technologies but all fell short of our stringent requirements. Our membase development efforts dovetailed with work being done at NorthScale and NHN and we’re delighted to contribute our code to the open source community and to sponsor continuing efforts to maintain and enhance the software.”


All except one project on [Zynga’s github repository](https://github.com/zynga) are related to Membase: moxi (forked from membase), zstored, mcmux and pecl-memcached.

[In an interview](http://www.linuxforu.com/interviews/zynga-about-90-out-of-100-we-plan-to-hire-would-be-foss-experts/), the Zynga country manager for India Shan Kadavil, refers to Moxi:

Our developers have been involved in various open source projects, including development of open source tools to bug fixes. An example is the Moxi project–when we were looking at scaling our infrastructure, we needed a technology that could help us scale horizontally, add new Web servers as when needed without being bottlenecked at the storage layer. Having examined and scrutinised all the proprietary options, we looked towards open source and found the Moxi project, which worked like a load balancer for the caching layer. We helped scale the Moxi project specifically by adding modifications to handle large cloud computing environments.


This statement did make me wonder what those other open source projects are that Zynga has been involved in? It’s hard to find anything because submitting a code change rarely causes a press release to be issued.

### FontLabel

The [FontLabel](https://github.com/zynga/FontLabel) project was released as open source by Zynga. It enables you to render any truetype (ttf) font on the iPhone, not just the built-in fonts provided by Apple. It’s not to be confused with bitmap-font rendering, instead it behaves like [UIFont](http://developer.apple.com/library/ios/#documentation/uikit/reference/UIFont_Class/Reference/Reference.html) but allows you to use non-system fonts.

FontLabel was [added to cocos2d-iphone in September 2009](https://code.google.com/p/cocos2d-iphone/issues/detail?id=534&can=1&q=fontlabel&colspec=ID%20Type%20Status%20Priority%20Milestone%20Component%20Owner%20Summary).

To be honest, FontLabel is not the kind of project that would have stopped the world from spinning. But it’s a kind of project that benefits from many developers using, and thus testing it. So making it open source makes sense.

### Others OS projects?

It’s hard to find references of Zynga contributing to open source projects, because usually there won’t be a press release issued when a coder submits a fix to a more or less obscure open source project.

I was only aware of one other OS project, that was FontLabel which was actually started by Zynga. If you know an open source project that Zynga contributed to and that I missed, please mention it in a comment, thank you!

But if that is the entire involvement Zynga has with Open Source, then it doesn’t give me the impression that they’re open-source friendly. They support it when it makes sense, for PR, for free beta-testing, or if they need open source technology and want to play nice. In that regard they are no different than any other big company.

### Zynga’s view on Open Source

The [interview with Zynga’s country manager for India](http://www.linuxforu.com/interviews/zynga-about-90-out-of-100-we-plan-to-hire-would-be-foss-experts/) published over a year ago provides some clues.

We think of open source as a movement and not as a particular project. The success of the projects using open source is possible only when multiple people contribute and when the industry endorses them.


Which means that without industry support (read: finances, manpower, marketing) open source projects can not be successful. At least not by their definition of success.

The next statement makes one hopeful:

We have multiple models to involve the community. We have had members from the open source projects work commercially for us to build a platform or tool for us. To that end, we gave the entire output back to the community.


This is practically identical to hiring Ricardo and Rolando. However, I think this statement refers more to contracting agreements rather than employment.

I suspect that Ricardo and Rolando were already working as contractors for Zynga for the past months. From Ricardo’s commits to the cocos2d-iphone project over the past months I always wondered what kind of secret project he was working on. To me the commits looked like by-products of a different, bigger projects. Some commit phases included many smaller changes, not something that you’ll spend your entire day working on.

Before actually moving from continent to continent you almost certainly have to have worked together in some way or another, if only just to get to know each other. So I can imagine something already being developed in secret on a contract basis. The question is, if this is true, what it is and when or if we’ll be seeing it.

The statement following the last one:

Second model is the non-commercial model that involves us getting into open source threads, sharing ideas and work collaboratively with the community with our code fixes.


Ok, so that “model” is basically what any developer does at some point in time. Making code fixes is definitely the easiest way to get something contributed to an open source project, and we all share ideas and collaborate (speak: posting in forums). That sentence made me laugh. Because you can’t really call it a model - it’s what we all do.

### How Zynga Germany came to be

By chance I came across another acquisition Zynga made in September 2010. They [bought german startup Dextrose](http://www.insidesocialgames.com/2010/09/24/zynga-acquires-dextrose-aves-engine-html5/) (at the time located less than 20 km from where I live) to get ahold of their Aves HTML5 engine and have them become Zynga Germany. Paul Bakaus is co-founder of Dextrose and a [jQuery](http://jquery.com/) core team member ([jQuery UI creator](http://jqueryui.com/)), and now CTO of Zynga Germany.

The interesting aspect here is the Aves engine. It was supposed to be licensed as middleware to other game developers and publishers. But after Zynga’s acquisition it became a proprietary engine and won’t be licensed. All websites of Dextrose and Aves as well as their social networking accounts have since been removed, and Zynga Germany relocated by 80 km to Frankfurt/Main: the city with one of Europe’s busiest airports and many direct flights to overseas. Obviously to make Zynga Germany more accessible for corporate.

Have a look what the engine is capable of and you’ll understand why Zynga had to have it. And why they wanted no one else to have it.

### Meaning?

I don’t want to read too much into this, but I’m skeptical. For most corporations, doing good for the community is just not in their program - except of course their PR department. I haven’t found any indication that Zynga is any different. Although they like to be the “google of games”, they’re a far cry from google when it comes to open source projects it seems.

It’s clear that hiring Ricardo and Rolando is providing value for Zynga first and foremost. If it were any other way, the two would not be moving to San Francisco but would be working on a contract basis. Zynga could not possibly buy cocos2d-iphone, so they simply “acquired” the next best thing, which means hiring its key contributors. The cocos2d-iphone project remains untouched, but I worry the emphasis is on *remains*.

On the other hand, [Zynga apparently registered the domain ZyngaCocos2D.com](http://www.learn-cocos2d.com/2011/05/zyngacocos2dcom-domain-registered/) … so maybe there do have bigger plans for cocos2d-iphone?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Great post, and great research Steffen. In all honesty, I have little doubt that things will go slower and slower with Cocos2D, as they have already been in the past months.

The Aves HTML5 engine seems great - I imagine Zynga guys finding about the engine and trying to get the phone number of the developers as fast as possible. I have no idea how much they paid for it, but they might have saved a lot of money with the acquisition.

Overall, anyhow, this does not look good at all for Cocos2D. Maybe it would be better to do what Ron Gilbert did - you study Cocos2D, learn from it, and then do your own framework or improve on it. But not everybody is able to do that.

Not just saved. Made. 😉

Ron Gilbert did what? … Ah, found the source:

http://twitter.com/#!/grumpygamer/status/36184183306985472

http://twitter.com/#!/grumpygamer/status/21596491177

Too bad it’s not open source. Would love to see what he’s done.

Same here! But he seems to be doing this mostly for fun, not sure how far he went with it.

Surely if Cocos2d really is open source there’s the option of a fork, the new branch being maintained and updated by new developers? We’ve got all the source code, we “just” need to host it and keep it alive…

Yup. But it’s going to be a full-time job for at least one, better 2-3 developers. Somehow, they either need not have to worry about a daily income (eg being sponsored or simply being rich) - or make money off of it while keeping the code free. Which probably means selling add-on libraries or tools, and not just one or two. I can’t imagine ads or donations alone to do the job.

Yeah, sigh, and there’s the rub. If I could only escape the day job …![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


http://www.dotweekly.com/dotweekly-discoveries-bestbuy-autodesk-and-more-new-domains

ZyngaCocos Domain registration?

Thanks! That’s intruiging news.

[…] Zynga and Open Source […]

So its really confusing about the future of cocos2d, so what we should do as Indie game developer? Should we select other game engine instead of cocos2d, for example Corona. Though I love cocos2d as its objective C based.

No, so far nothing has changed and cocos2d works fine.