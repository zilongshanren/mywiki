---
title: 'Dropping Dead: OpenGL ES v1.x'
url: http://www.learn-cocos2d.com/2011/07/dropping-dead-opengl-es-v1/
author: MeachWare says
published: '2011-07-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Update:please find the[iOS Device Sales Statistics for Q1 2012 here].

Currently Cocos2D is being [overhauled for a v2.0 release](https://github.com/cocos2d/cocos2d-iphone/tree/gles20). It will only support OpenGL ES 2.x and thus games made with Cocos2D v2.x will not run on 1st & 2nd generation devices (iPhone, iPhone 3G, iPod Touch 1 & 2).

The two development threads in the Cocos2D forum [here](http://www.cocos2d-iphone.org/forum/topic/14636) and [here](http://www.cocos2d-iphone.org/forum/topic/6074) are full of users expressing their disappointment (among other emotions/criticism) not to support a rendering core that supports both GL ES 1.x and 2.x. Even though it was said that if you still need to support all devices, you can simply continue to use the Cocos2D v1.x branch.

I’ve run some numbers and came to the following conclusion: **if your game only supports OpenGL ES 2.x and comes out in Q1 2012, you will lose less than 10% of customers!**

Here’s why I think OpenGL ES v1.x is currently in the process of dropping dead, and close to hitting the ground within the coming ~6 months.

### iPhone Sales Statistics Q1 2011

Wikipedia has a nice [list of iPhone sales statistics (totals)](http://www.learn-cocos2d.com#) as they were reported by Apple each quarter. These statistics range from Q3 2007 to Q1 2011. Unfortunately, sales by Apple are not reported by device, so some quarterly sales are combined sales of iPhone 3G + iPhone 3GS respectively iPhone 3GS + iPhone 4.

I tried to extrapolate individual device sales by making the assumption that over time periods where two different iPhone devices were being sold, the newer one was likely to have sold more. Since we’re talking about Apple I choose a 70/30 split, meaning I assumed that 70% of the sales were for the newer device. This seems about right since newer devices have always sold better than the previous generation, but also according to some developer statistics.

For example the [Bump developers reporting an iOS 4 adoption rate of 90%](https://www.quora.com/What-proportion-of-all-iPhone-owners-use-iOS4-*-today) in January 2011 across all iOS devices (1st generation devices can not install iOS 4). Or the [Surgeworks iOS 4 Adoption report](http://surgeworks.com/blog/ios-4-adoption-rate-how-many-iphones-are-running-ios-4-vs-os-3-numbers-and-percentages-exposed) which contains usage statistics of 1st generation device users of only 2.5% for one app, and 5% iPhone 3G users for another app.

The left side of the following pie charts shows the total number of iPhone devices sold to that date, with sales periods of two devices combined. The pie charts on the right show the extrapolated sales statistics for individual iPhone device generations, and which OpenGL ES version they support.

[Download the Excel sheet](http://www.learn-cocos2d.com/wordpress/wp-content/uploads/iPhone-Device-Sales.xls) I used to create these charts:![iphone_sold_q1_2011](../../../wordpress/wp-content/uploads/iphone_sold_q1_20112.png)


**Notice how in Q1 2010 about two third of all iPhone devices supported only OpenGL ES 1.x, but within a year the picture turned just the other way. In Q1 2011 two thirds of iPhone devices sold were capable of running OpenGL ES 2.x code!**

This has a lot to do with two factors: the iPhone 4 sold like crazy, whereas the last OpenGL ES 1.1 iPhone being sold (iPhone 3G) was discontinued in June 2010. Meaning since Q3 2010 Apple does no longer sell OpenGL ES 1.1 iPhone devices. And OpenGL ES 1.1 iPod Touches stopped selling in Q4 2010 as well.

### All iOS Device Sales Statistics Q2 2011

[According to Unwired](http://www.unwiredview.com/2011/06/06/apple-ios-stats-200-million-devices-sold-25-million-ipads-14-billion-apps-downloaded-and-more/), Apple reported to have sold 200 million iOS Devices during the iOS 5 announcement. 25 Million of those were iPads. These are the most up to date sales stats, which I assume to be the Q2 2011 statistics.

Based on Wikipedia’s numbers which states 83 Mio. iPhone devices sold vs. over 60 Mio. iPod Touch devices sold, the remaining 175 Mio. should be 42% iPod Touch (74 Mio) and 58% iPhone (102 Mio).

The percentage of OpenGL ES 2.x capable iPhone devices to those only supporting OpenGL ES 1.1 was 31% in Q1 2010 and jumped to 64% in Q1 2011. Assuming the 1.1 to 2.x ratio is the same for iPod Touch, that gives us 137 Mio iOS devices (iPhone, iPod Touch, iPad) with OpenGL ES 2.x capability versus 63 Mio devices (1st & 2nd generation iPhone / iPod Touch) which don’t support 2.x.

*This pie chart includes all iOS Devices and which OpenGL ES version they support:*![iphone_sold_by_gl_q2_2011](../../../wordpress/wp-content/uploads/iphone_sold_by_gl_q2_2011.png)


That means **70% of all iOS devices sold to date support OpenGL ES 2.x.** This leaves us with only 30% of iOS devices not capable of running OpenGL ES 2.x code.

### I don’t want to lose 30% of my customers!

You won’t!

Keep in mind that these statistics are only about **devices sold**. They do not reflect what has happened to these devices since, or how they are being used today.

I can also assert that older devices are disappearing fast from the market. Even though 30% of the devices sold support only OpenGL ES 1.1, your potential customer base will be significantly less than the number of devices sold. This is for a variety of reasons:

- device has been lost or was stolen
- device broken beyond use/repair
- device simply no longer in use
- device owned by a person who is unlikely to buy new apps

Particularly the last item must be considered: the device user. Again, the user is your potential customer, not the device. And in general all of these items are more likely to happen the older the device is.

One commenter in one of the two GL ES 2.0 threads on the Cocos2D forum reported how happy users were to see a game running smoothly on their 1st generation devices. For me that is not proof that support for older devices is beneficial. To the contrary, I think it clearly shows us that old generation device users are much more selective about their purchases, are already giving up their love for their devices, and may be considering an upgrade because they may have stopped enjoying their devices. This contributes to the “less likely to buy new apps” factor.

You can also assume that users of older devices have less expendable income, or are satisfied with the device as it is. If a user is actually happy with an old iOS device, it’s likely that person prefers to use apps and plays few(er) games or just keeps using the apps & games already owned.

**The number of potential customers you would lose - if you released an OpenGL ES 2.0 game right now - is maybe around 10% to 20% at most. Far less if your game is complex and visually rich, and would suffer some performance or visual degradation on older devices anyway.**

### What about the near future? (Q1 2012)

Considering that 6 months from now, in Q1 2012, we will have seen the release of new iPhone devices (iPhone 5, possibly iPod 5) and thus another boom in sales, it is a better deal to start making some cool visual effects with shaders that look great on iPhone 4 and 5 rather than trying to still support 1st and 2nd generation devices.

In particular if you need to put in some (or a lot of) effort to support the older devices, for example if you have to optimize the performance, reduce the feature set (eg no or limited Game Center support) or (god forbid) you need to ensure compatibility with iOS 3.0.1 or lower (CADisplayLink unavailable!). That time and effort are better spent on making a better OpenGL ES 2.x game!

Obviously the decision also depends on how visually rich your game is going to be and whether you can expect to run into performance and other issues on older devices anyhow.

### Summary

I fully expect the market share of OpenGL ES 1.1 devices sold to drop to around 20% by Q1 2012. That puts the number of potential customers (for game developers) still using those devices and buying games to certainly much less than 10%. Then consider that the iPhone 5 may even already account for up to 5% (~10 Mio) of all iOS devices sold by Q1 2012.

**By the end of 2012 the potential customer base (for game developers) still using 1st and 2nd generation devices will have become entirely negligible.**

That means, if you start developing an OpenGL ES 2.x game within the next 3 months, and your game takes 3+ months to complete, you will lose very few customers by only supporting 3rd generation and newer devices. And you may actually be able to win more customers by cleverly supporting the new devices!

I think it’s wise to start using Cocos2D v2.0 as soon as it is production-ready, which may be in around 3-6 months according to the comments and current progress.

Game On, Cocos2D 2.x!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Already been decided and implemented (dropping support for opengles-1 devices), erm last year… 😉

http://meachware.blogspot.com/2010/10/thoughts-on-older-devices.html

Hello, very interesting post.

I would not reduce my game’s feature set or in-game effects to make it run on older devices. I usually try to improve the performance on older devices as far as I can, but not by removing key things.

Also I think there is so much performance difference between older devices and newer. For example, between 3G and 3GS. The iPhone 3G is conditioning the development too much and sometimes it’s almost like making a new code for the same game, and for what? To sell almost the same? Maybe is better to improve the game to reach all the newer devices customers, instead of making it “retro compatible”.

Technology is always evolving, so developers, frameworks and tools should do the same.

Regards.

I completely agree. While I would like to support every device, there comes a point were the end user has had several years to upgrade their device and if they haven’t I can’t be responsible for that choice. If they are too cheap (or to be fair, poor) to buy a new device, they aren’t likely to be spending much on apps anyway.

I try to maintain availability to older devices only to a point.

[…] devices that don’t support OpenGL ES 2.0 can’t run apps made with thie branch, but most devices are OpenGL ES 2.0 compatible these days, so it’s becoming more and more of a decent business decision to use […]

[…] With Apple’s blazing Q1 2012 quarterly results, which sees iPhone sales double (!) that of the previous Q4 2011 and last year’s Q1 quarter, it’s time to update my iOS Device sales statistics from July 2011. […]