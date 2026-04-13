---
title: Kobold Kit goes Open Source!
url: http://www.learn-cocos2d.com/2013/09/kobold-kit-open-source/
author: Deeeds Says
published: '2013-09-05'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

With the release of iOS 7 (ETA: Tuesday, Sept. 10th):

[Kobold Kit](http://koboldkit.com/) will be available as open source under the MIT License!

We spent a lot of thoughts on how we like to run an open source project. And also why. I’ll start with an executive summary with more (perhaps too many) details in the text.

**The Idea**: make the project as open and inviting as possible. Let contributors gain control over and take on responsibility for the project based on their contributions. Provide them with ways to promote their work on their own accord.

**The Goal**: build **the **Sprite Kit game engine with the help of many developers.

Kobold Kit is supposed to become the “patron project” under whose roof the most valuable Sprite Kit extensions are combined. Website, forum, wiki, blog and store are extended playgrounds shaped by community members. If you’re part of the project, we want you to proudly present and benefit from it.

In essence: we want to get out of the way as much as possible and enable anyone to find their place in the project. Guidance, not dictating, is our guideline.


### Contributing Code

We’ll have not one but **two github repositories** for you to “check out”.

One is the authoritative (main) repository, the other one is the repository for the community. Anyone who asks will get **direct read/write access to the community repository**. On occasion the popular and/or valuable changes and additions in the community repository will be integrated to the authoritative repository.

Trusted and valued developers, such as tool authors and valued contributors, will get direct access to the authoritative repository. That means if a tool that supports Kobold Kit gets an update, the tool author can commit any required engine code (ie loader code) directly to the project. Tool and engine version mismatches as well as tools requiring manual code updates should be a thing of the past.

We will also accept patch files and (truly) standalone classes by email. Since the Kobold Kit game components (behavior classes) are standardized, it’s easy to add more of them without introducing unnecessary dependencies or adding complexity. This goes for other aspects of the engine’s design, right down to the project structure and folder names.

We’re going to document what and how to contribute over the coming weeks. What we won’t give you are 30+ pages of rules, coding style guides, templates, etc. We haven’t contributed to open source projects **exactly** because of such documents, so we rather invite some inefficiencies before it’s decided what rules we really, really need.

### Blogging on KoboldKit.com

Contributing doesn’t stop with the code, nor does it need to begin there! You can [register on koboldkit.com](http://koboldkit.com/wordpress/wp-login.php?action=register) and start writing posts and pages in WordPress. **You can add content directly to the Kobold Kit website!**


The Kobold Kit blog is a great place for those wanting to promote their work on the site, and within certain limits (ie only “major” updates) we’ll allow that. Tutorial authors can use the blog to cross-/guest-post their own articles, developers can use it to introduce their games, contributors can use the blog to raise awareness to their additions, request feedback, and so on.

The many noteworthy externally linked articles we’ll aggregate in so-called “Indie Roll” articles containing mostly links to a specific topic. Share links to articles you found thoughtful, educational, informative or otherwise noteworthy. They should be related to Sprite Kit or of interest to indie/mobile game developers.

Note that all website articles will be reviewed before publication. So regarding quality, quantity or “fitness” some content may be better suited for the wiki…

### Editing the Wiki

Every decent open source project needs a Wiki. We use Confluence because it’s the only wiki with a visual editor - meaning you don’t need to memorize some odd wiki syntax, plus many other benefits.

As an anlog to the community repository we have a community space on the wiki where **anyone can add and edit articles without even logging in**. Use it to document your contributions to the community repository, to stage documentation contributions, or to share code snippets that needn’t or can’t go in the repository.

We hope the community wiki will be an incubator for great content. Since allowing anyone to contribute without a login is risky and prone to abuse, we’re considering this to be an experiment and will closely monitor and police it. We will certainly protect valuable community wiki pages by propagating them to a non-anonymous section of the wiki, with proper attributions.

Unfortunately we can’t just enable public signup of wiki accounts because the user licenses are costly. The goal is to raise the user limit over time in line with the growing interest in the wiki.

### Funding the project

Now we still need to make ends meet, for at least two developers no less. There are several ways we intend to generate an income for ourselves and to fund Kobold Kit:

**Starterkits as a Service**- We’re selling the code and assets we use to develop actual games, which makes it different from other starterkits (ie XXL Tutorials). We will frequently deliver new features and improved engine code. It’s an actual game project, so our code is relevant and optimized, our workflows are efficient, and we’re pushing the boundaries.**Note:**Starterkits will be**free for KoboldTouch customers!****App Store**- Our goal is to publish each Starterkit’s game to the Apple App Store, and when feasible also to the Android Store(s). Our games will use the shareware principle: free, fully playable demo with paid add-on content where players get their money’s worth.**Affiliate Sales**- We’ll open up our Store to externally developed, Sprite Kit related products and apps. For each sale made through us we receive a % commission fee while product authors benefit from the exposure and additional customers. We support and encourage others building commercial products with or for Kobold Kit because it’s beneficial to everyone involved.

Overall we expect >80% of the revenue lies in making great Starterkits. The App Store provides a fighting chance for a lucky punch, but we don’t really have any expectations. Affiliate sales are a means to increase the revenue baseline and a fair way to cover the “service costs” of Kobold Kit.

### Why open source the engine?

Because selling it would be difficult, and we’d force ourselves into a niche when we could take the lead on the Sprite Kit market as a whole. Even if that means less money in the short term we’re convinced **it will pay off in the long run**.

Sprite Kit is fantastic, it doesn’t have rough ends like other game engines, what’s there can hardly be made better. There’s little need to look, let alone pay, for an even better version of Sprite Kit. Yes, Sprite Kit certainly lacks some specific features and you do want to add them to most projects. Yet throughout the iOS 7 beta phase it became clear that missing features will be added by individual developers anyway, and rather quickly.

And peeking into the private API revealed that the often criticized “missing features” already exist, perhaps they’ll be made public at a later date. So competing mainly on a “missing features” level seems pointless; each new iOS version possibly being a major setback. It would be frustrating to work under these conditions.

And since our goal is to make games and sell starterkits, it became clear that our most valuable code isn’t the engine itself. It’s things like integration with Tiled, a faster (multi-threaded) tilemap renderer, custom tilemap physics, object templates in Lua, custom game logic (prebuilt behaviors), downloading resource files to the device and reloading without restarting the app.

That’s great value for certain developers because it allows them to work more efficiently, to save time and resources, to have specialized, optimized code at their disposal - in essence: code and workflows which would otherwise be a pain to develop or wouldn’t even be created in the first place.

By open-sourcing the engine we can **build a reference game engine based on Sprite Kit**, and combat fragmentation of resources into numerous open source projects, each on their own fighting for recognition and adoption. We feel it’s our responsibility to prevent Sprite Kit developers having to add several separate open source projects all by themselves, just so they have access to more useful or perhaps even mandatory features.

This should also explain why Sprite Kit (a rendering engine) needs a game engine like Kobold Kit.

### Join us!

Come get [Kobold Kit](http://koboldkit.com/) on Tuesday, September 10th (subject to iOS 7 availability).

PS: the relevant links (wiki, repository, etc) will be added when Kobold Kit is available.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Wise move, indeed.