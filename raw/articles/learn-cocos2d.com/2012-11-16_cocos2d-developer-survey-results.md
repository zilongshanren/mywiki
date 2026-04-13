---
title: Cocos2D Developer Survey Results
url: http://www.learn-cocos2d.com/2012/11/cocos2d-developer-survey-results/
author: Ovogame says
published: '2012-11-16'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

For the past two weeks I’ve been running a [Cocos2D Developer Survey](http://www.surveymonkey.com/s/SGRTSZM). As of today, 236 developers started the survey and 189 finished it completely. That’s 80% despite the many questions they had to answer.

Here are the results with my observations. I started the survey also to see if I was on track with [KoboldTouch](http://www.koboldtouch.com/), and whether certain assumptions hold true. Specifically I had a hunch that cross-platform development is only perceived to have great value or appeal. Let’s see if I was right.

Click on each image for full resolution.

### Who are you?

I was very curious how many cocos2d developers consider themselves to be hobbyists and indies compared to professionals, who either work for a mobile developer or are taking on freelance jobs as one.

Almost half of those who answered the survey are hobbyists. Nearly 30% consider themselves indies who make a living making mobile games. This is great!


### Features of Appeal

Here I laid down the first trap. Well, not really but I wanted to see how appealing cross-platform functionality was to users compared to four other features which I’m expecting to be one of the early additions to KoboldTouch.

So wow, cross-platform clearly wins. At least when compared with these features. It beats native OS features and Objective-C Box2D physics, one of the things I am on to with KoboldTouch.

### The Pacific Island Question

Now, pitted directly against one another in a “what if” question - if you had to choose, would you rather have cross-platform or native OS features?

Personally I found this question to be of greater importance. Because if you had to choose, what would you want more? Fortunately the pendulum swings clearly in the direction of better OS integration. There’s still a significant number of developers who would rather have cross-platform.

Is my idea to make KoboldTouch iOS & OSX only, focusing strongly on OS integration, in jeopardy?

To find out, I added a poll to the right sidebar on this blog. The result of this poll is much more one-sided. Obviously because it specifically limits the question to cocos2d-iphone and its Javascript implementation while excluding cocos2d-x and all the other variants:

That means the cross-platform Javascript development of cocos2d-iphone that happened over the past 6 months and is still going on is only appealing to 26% of its users. It’s then up to KoboldTouch to satisfy the needs of those who want better OS integration.

Great! That’s exactly what I wanted to see.

### The Reality of Cross-Platform

The question is: how many developers have actually ported one of their apps to another mobile platform?

Now that’s clear. 80% haven’t. Good. But what do we know now? It’s possible that those 80% simply haven’t done cross-platform because they couldn’t do it. Most likely they were using cocos2d-iphone which supports no other mobile platform but iOS (at the time of this survey).

Yet, given the great number of hobbyists, I find it highly unlikely that the number of cross-platform cocos2d developers is going to increase significantly. Not with cocos2d-iphone’s Javascript port and despite cocos2d-x being a huge favorite, as you’ll see shortly.

#### Never underestimate cross-platform development!

They (engine developers) say it’s so easy to deploy to all the various platforms and devices. And they’re right. But deployment really isn’t the issue, and they (the users) follow the call to the promised land with blind eyes. There they’ll find out the hard way that it’s still a lot of labor to do cross-platform development even with the best of today’s cross-platform engines.

Consider this before you get too excited about cross-platform development:

- You have to adapt or reimplement your input code, specifically when porting from mobile to desktop, web or console. But even Android vs iOS devices may behave differently when it comes to input, for example multitouch lag or accelerometer reporting different values, being more or less sensitive.
- You have to avoid using native frameworks like Game Center, or duplicate your efforts: Game Center here and whatever is the Game Center pendant on other platforms.
**If**that pendant exists. - You may have to rely on rudimentary user interface controls that work on all systems. You lose native look & feel. And flexibility. And beloved functionality.
- You have to consider a greater number of display resolutions and device specs.
- You have to test on a greater number of devices. You’ll be spending an additional 10% to 50% of your development time just on testing, simply because you have to compile and deploy to more platforms and test on more devices.
- You may have to buy or at least borrow a lot more devices to test on.
- You may have to use different compilers which spit out different warnings and errors.
- You are likely going to spend more time designing and optimizing your screen layouts for multiple resolutions.
- You may have to create lot more assets to accommodate more screen resolutions and aspect ratios.
- You may have to use a different programming language common to all platforms, which may not support runtime debugging or compile-time error checking as well as high-level languages like Objective-C and C/C++ do.
- You’ll be spending more time optimizing performance, because developing for multiple platforms often incurs a performance penalty.
- You have to deal with two or more distribution platforms. Open account, sign contracts, figure out how to get paid, conform to their license agreements, create different marketing materials (App icons).
- You have to market your app more. Just as there’s iOS specific app blogs and reviews, there are those specific for Android and other platforms. You want to reach a greater audience, you’ll have to spend more time, energy and money to get the attention of that greater audience.
- A lot more things I can’t think of right now…

#### The sensible approach: hit first, port later

What I find notable: nearly as many apps started out as cross-platform developments than apps which were only ported after they’ve been an App Store success. Of the 47 developers who already made cross-platform apps, 20 did so only after they knew they had a hit in their hands. This is the sensible approach. Make a hit first, then port.

And you know why?

For one, look at the above list. Since you know you have a hit, those issues seem less daunting and they’re less risky because you’re already making good money from your iOS app. Perhaps you can even afford to pay someone to do the grunt work for you.

And as if that weren’t enough, have a look at where developers’ revenue is coming from …

### Revenue Stream … or Scream?

There are several famous articles about the terrible revenue coming from Android apps, especially when compared to the same iOS app. I was wondering how the Cocos2D developers were faring in this area, so I asked what the revenue percentage split was for their latest cross-platform game.

There’s 4 who made significantly more on Android. There’s another 13 who made roughly equal amounts on both platforms. And then there’s a total of 48 who made less than 30% of their revenue on Android, 32 of which made between 15% and nothing on Android.

I think this justifies another chart. This pie is not a lie:

If you go cross-platform to both iOS and Android, here’s what you can expect in terms of revenue:

- 50% chance your Android revenue is going to be abysmal
- 25% chance your Android revenue is going to be disappointing
- 15% chance your Android revenue is roughly on par with your iOS app
- 10% chance your Android revenue is going to rock, or rock hard

Personally I wouldn’t place my bets on Android. If you are already successful on iOS, go for Android. By all means don’t leave revenue wasted, another 1-3 months of effort are likely going to pay back in that case. On the other hand …

… since you’re doing so well on iOS, why not push the iOS revenue even further? Spend that time and money into marketing, downloadable content, In-App purchases, new features. Or start making your next iOS game, perhaps a sequel. This is just as likely to pay off equally well, if not more.

Especially if you’re a lone wolf, or a very small team (2-4 developers), there’s one question you ought to ask yourself:

Why spend 6 months of your time producing something that might make $100,000 a year, then spend another 50% of the original development time (3 months) on an Android port that might bring in only an additional $25,000 (25%) a year?

Clearly that’s not a sensible business approach. You may be better off attempting to create your next iOS hit.

### If cross-platform, which engine?

I wanted to see how the various cross-platform game engines and other solutions stack up against each other, and also give users the option to say “I’m not interested in cross-platform”.

Since this question asks about the future, which may or may not have been very well thought through by each individual, the results of this question have to be considered a momentary trend. Especially when considering that 80% of the survey respondents have yet to develop a cross-platform game.

About 25% of users are trending not to get into cross-platform development. Of those who do, they have a clear favorite: a third would choose cocos2d-x. Probably the promise of using a very similar API, and despite the fact that it’s C++. I know some actually like or prefer C++ I can’t help but feel pity for them. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Unity with 18% is also very appealing, while cocos2d-iphone with Javascript appeals only to 9%. This may be in part because it’s still very new and unproven with no cocos2d+JS games have been released so far.

Corona I expected to do better than 5.5% but from what I hear most developers don’t like the fact that it’s closed-source and not extensible. Unity, they say, I can at least extend with my own plugins if I dole out the money.

Among the other game engines, and those not listed in the graph, are: libgdx, custom engine, Gideros Mobile, Yoyo games (Game Maker), don’t know yet (never heard that one before), Allegro with cocos2d-x, 2x Monkey, Playn, Palatino, 2x Futile (mentioned twice, Matt Rix’s on to something here!), 2x NME (HaXe), Mono and (ta-daaa) Gameplay2D from RIM.

Someone is actually developing for Blackberry, what a surprise! And since Futile is built on Unity, is similar to cocos2d in its design and has created some buzz among developers, we’ll likely hear more of it in the future and possibly more developers will switch over to Unity rather than cocos2d-x or cocos2d-iphone with JS. [Check out Futile here.](http://struct.ca/futile/)

### Tools of the Trade

I also wanted to know which tools are popular among Cocos2D game devs, and which have had seen buzz but hardly any use. Or whether some have fallen by the wayside over time.

I also allowed developers to leave custom responses. Unsurprisingly Photoshop was mentioned 4 times in 14 responses, and two are using custom tools.

#### Scene Design Tools

CocosBuilder and LevelHelper are both fairly popular, as expected. What I didn’t expect is developers fumbling around with Inkscape as a Scene Design Tool. I can not imagine anyone having a good development experience with Inkscape as design tool.

There seem to be no real alternatives to CocosBuilder and LevelHelper. What a shame when you consider the tools available for other game engines.

#### Tilemap Editing

Obviously Tiled Map Editor wins. iTileMaps for iPad, as nice as it is, is probably limited for on-the-go sessions. Something few developers exercise, one would rather wait to get home to an actual desktop machine where you can then test map changes right away.

Of note is the fact that there are more users using a specialized tool like Tiled than those who are using CocosBuilder or LevelHelper. Apparently you can hardly create tilemaps without an editor but you’re more likely to design scenes without any kind of editor.

#### Texture Atlas Tools

Here we have a clear winner: TexturePacker. Zwoptex has lost most of its former glory but still ranks as a popular second choice. One thing I should note here: Zwoptex is only $15 whereas TexturePacker costs $30. Write that down: price isn’t everything. Good tools are highly valued, especially by developers.

SpriteHelper makes an honorable third, maybe because it’s supposed to be used in companion with LevelHelper.

#### Animation Tools

Spriter has had quite the buzz, yet it’s surprisingly rarely used. Developers simply seem to be more familiar with Flash.

#### Particle Effect Design Tools

ParticleDesigner wins hands down. It was the first and it was and still is a steal for what it does for only $8.

While I was researching alternatives, I was surprised to find such a great number of tools which did essentially the same thing. I even left out one or two from the list. I can’t help but feel that some developers were out to make a quick buck copying ParticleDesigner in functionality (and some even in form) simply because it’s rather straightforward to do so. I feel enlightened to see that they haven’t had much success with that approach.

The only tool that made it slightly past insignificance is ParticleCreator from the Mac App Store. It looks like it does offer some pieces of functionality which makes it worth investing 3 bucks in. On the other hand, it creates code, not data files, so it’s prone to break whenever cocos2d is updated. And it makes for a terrible copy&paste workflow.

#### Bitmap Font Designers

Bitmap font tools are lead by Glyph Designer. It does everything Hiero does, but without all the bugs and a much nicer, easier to use user interface. If it were me, I’d eradicate any memory of Hiero from everyone’s mind and the internet. This tool is horribly buggy and just when you think you have it figured out, it starts inverting your atlas font image file. Never again.

The follow ups are bmGlyph as well as ShoeBox and BMFont for Windows. Shoebox, never heard of that one before. Turns out [Shoebox is a free tool for Mac and Windows](http://renderhjs.net/shoebox/) and comes with a bunch of cool features (sprite packing, masking, tilees, bitmap fonts, animations).

#### Physics Shape Editors

Lastly, Physics tools. These are less frequently used tools overall. PhysicsEditor wins the race against VertexHelper.

Unfortunately I overlooked the fact that there is both a free (github) and a commercial (App Store, $8) version of VertexHelper - so we can’t say which of those users are using. I hope for their sake it’s not the free version. On the other hand, even the pro version uses the code generation, copy&paste workflow that’s so tedious and error-prone to work with.

PhysicsEditor costs $20 and the excellent and flawless auto-shape tool alone is worth the price, just by saving you hours over the course of app development not having to trace shapes manually (or correcting VertexHelpers brute force results). If you are considering both, there’s no question in my mind that you ought to pick PhysicsEditor. (I don’t get a commission from PhysicsEditor sales.)

### The Most Wanted Cocos2d Features

The last question was all about which features developers believe would improve cocos2d-iphone the most. I was most excited about these results because they would help me determine what should go into KoboldTouch, and how I should prioritize these features.

There’s a great demand for resolution independent positioning of nodes. Meaning to design once for one screen resolution, and the layout of the screen dynamically adapting to the larger screens. This has some caveats, but I’m surprised that there actually isn’t a good solution out there - let alone a mediocre one.

I’m currently researching this and if everything goes well, will add it to KoboldTouch as a Xmas present. I already wrote a Multi-Resolution Development Best Practices Guide for KoboldTouch members where I explained the basics for such a feature. It’s not really that difficult! I’m stunned no one has done it yet.

Obviously (and sadly: still) users want better documentation. I aim to provide that with Essential Cocos2D (part of KoboldTouch).

Cocos2D ported to ARC left me a bit puzzled. So, besides having ARC enabled Xcode templates (one could just use Kobold2D), what would the benefits of that be to cocos2d users? The answer I would most agree to is to have more readable cocos2d-iphone source code, without the hard to read C code like hash tables and the optimized (but buggy) ccArray. It may also have something to do with the lack of ARC support in the engine, where you can run into odd issues due to interfacing with non-ARC code. But these are rare, and it’s surprising to see that ARC is so high up the list.

The other features point to better OS integration: In-App purchases, multiplayer networking and Game Center, and built-in gestures (by the way: Kobold2D has them built-in already!).

There’s definitely high demand for better animation system. This is one area where cocos2d has been seriously lacking. Specifically if you want an animation where the duration of individual frames must be variable, or where you want to loop parts of an animation indefinitely until some condition is met.

Lastly better tools are obviously in great demand. Mainly because until recently the integration of CocosBuilder with cocos2d-iphone was seriously limited. But generally, and that’s my opinion, because even though these tools are great efforts, they’re still far below to what’s available for other engines. Just look at Torque Builder or Game Maker for instance.

While better and faster tilemap rendering was somewhere in the midfield in this survey, the KoboldTouch members have actually voted this feature so high up, it looks like I’ll be working on a new tilemap renderer next.

### The Least Wanted Features

Let’s look at the bottom, the five least wanted features from Cocos2D developers.

Video playback, iAd and virtual joypads have all good uses, and are desirable features. Yet they fell to the bottom because they are desired only by a small group of developers. I wouldn’t say they’re not important though, because particularly joypads make some games even possible.

Storyboards has also been the rave recently, but apparently again there’s only a small fraction of developers interested in Storyboard support, perhaps with a proper template. Surprising because the tutorials out there are all more or less flawed.

Regular release schedules are also not that important to developers. Perhaps because upgrading cocos2d is a hassle (not so much with Kobold2D) but also because most would rather continue with their game, finish it, and then start the new game with the new engine version.

### One last thing

I’ll keep the survey running for a while. You can [check the most up to date results here](https://www.surveymonkey.com/sr.aspx?sm=5lbM47n0cCiWWqq2YQrZmY_2bX5cufK7s_2bnSFmIhgqNoQ_3d).

Since I’m now [paying SurveyMonkey](http://www.surveymonkey.net/pricing/upgrade/quickview/?ut_source=header_loggedIn) $30 (€25) a month I’m eager to create more surveys. Honestly, it’s not the money, it’s the insights these surveys reveal. I find it fascinating to query the community and see actual, factual, real world responses coming in. That is invaluable!

If you have ideas for a future survey or individual questions, please leave a comment. I hope this survey’s results were as instructive for you as they were for me.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I don’t think Coco2D is a multi-platform engine. By that, I mean it wasn’t design from the start as a multi-platform engine and the ‘port’ are just that, port of an engine onto a different platform. So, yes, you’ll still have a lot of work to do on each platform.

I have created my own C++ engine for PC/Mac/iOS/BB10, but for example, you can’t access OpenGL functionality because on PC it is using DX8 and actually, I don’t need to know anything about witch rendering it is using (because I am only using high level functions like DrawSprite). I have just ported my engine for the BB10 platform (coming Q1 2013) and it only took me 3 hours to get almost everything ported: http://crackberry.com/smileys-pop-blackberry-playbook

Now, it takes me just 5 minutes (really) to get each of my games running on the BB10. That’s what a true cross-platform engine allow you. And once I bother porting my engine (actually just few files managing the platform specific stuff) on Android & Win8, all my games will be running on these platforms without any real work.

Now, I do have limitation of course (mainly because I want them too). For example, I don’t use accelerometer or multiple touch (I could, but don’t bother). The best thing about the engine is that I am doing all my work on the PC (very fast to compile and run, allow me to create editors inside my games) and all the game src code and data are 100% compatible with all the other platforms. It took me 2 years to tweak, change the engine to get to that point, but now it is a dream to use.

As an indie, if you don’t plan multi-platform, you are almost likely to fail. better to have multiple streams of income, than just one.

JC

If you fail on one platform, you’ll fail on all the others as well. I doubt that cross-platform development increases your chances of succeeding. Most games fail to break even, why even bother with cross-platform until you know it makes sense?

I agree if you manage to make $300 on each of the four supported platforms, you’re far better off than making $300 on just one platform. But the math rarely works that way, there’s only a small window of opportunity to make this reasonable. Make $100 on each platform and you’re still screwed. Make $1,500+ on each platform and you’ve made it either way. If you focused on one platform, you can still port in hindsight and add to your revenue stream.

The biggest issue being that most games sell quite differently on each platform. A game is much more likely to make $900 a month on one platform, and $300 on the other three together. It just makes more sense to focus on a single platform most of the time for most developers.

But if you win on one platform, you’ll win on all others as well.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


True. But what are the chances? It’s more sound, business-wise, to concentrate one’s effort and expand only after you’ve made a product that is successful albeit in a smaller market.

> If you fail on one platform, you’ll fail on all the others as well.

That’s absolutely wrong. Anyway, you are in this mindset because porting for you is a lot of work, so I understand that you are looking at a huge amount of work. If it wasn’t (like for myself, thanks to my engine) you’ll be praising cross-platform.

I mean if your game doesn’t appeal to an audience, it hardly matters what platform that game is on, or how many.

Yes, porting is a lot of work but that is true for both engine and game developer. Have you tried to support Game Center on all platforms? Or even just Facebook and Twitter?

And look at the developers having all those technical project setup, archive build, provisioning, etc. problems even on iOS. Every additional platform multiplies those issues. And when you finally got it right for one platform, you may have broken one of the other platforms. To make sure this didn’t happen, you have to test all platforms.

Cross-platform is time consuming, and there’s only so much an engine can help with the chores.

I would be interested to see the results of this survey with hobbyist developers removed to get the perspective of the more experienced developers.