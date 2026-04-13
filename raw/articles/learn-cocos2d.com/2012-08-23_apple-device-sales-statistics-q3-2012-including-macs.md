---
title: Apple Device Sales Statistics Q3 2012 (Including Macs)
url: http://www.learn-cocos2d.com/2012/08/apple-device-sales-statistics-q3-2012-including-macs/
author: Dani says
published: '2012-08-23'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

This is an update to the [last sales statistics post](http://www.learn-cocos2d.com/2012/03/ios-sales-statistics-q1-2012-split-by-model-opengl-es-2-0-support/) to include Apple’s Q2 and Q3 2012 results as well as adding Macintosh sales:

I got the Mac sales numbers from Apple’s quarterly Earnings Press Releases dating back to Q1/2007. Nearly all Macs sold from 2007 onwards are capable of running at least OS X 10.7 (Lion). The Mac numbers include both desktop (iMac, Mac mini, Mac Pro) and portable (MacBook series) machines.

This puts things in perspective from sheer numbers. **There are now more iPads in the world than there are (relatively up-to-date) Macs! **

On the other hand, given that most Macs cost over $1,000 the sales numbers aren’t reflecting revenue. But you can argue that making a Mac OS X (Mountain) Lion app has the potential to reach the same number of App Store users than an iPad exclusive app.


### Mac Sales Over Time

Since I had all the quarterly Mac sales since Q1 2007, I wanted to see what the progression was and what the trend is for Mac sales since 2007:

Unsurprisingly, Mac sales are steadily increasing since the success of the iPhone. A good portion of these sales is certainly coming from developers wanting to or having to develop for iOS, and thus needing to own a Mac computer.

Of course it’s up to you to argue that Macs are simply the superior computers, and people are finally realizing this fact. 😀

### The iPhone Devices

Apple sold 35 million iPhones in Q2 2012, and a slightly disappointing 26 million in Q3 2012. Since Apple does not differentiate between iPhone models in their earnings reports, the pie chart accumulates sales for all models that were available in a quarter.

Since Q1 2012 three iPhone models are in production and currently being sold together: iPhone 3GS (8 GB), iPhone 4 (8 GB) and iPhone 4S. Of the 40% sales that these models have accumulated in just three quarters it can only be *guesstimated* how many sales each model contributed to that number.

Therefore it’s also not possible to infer from Apple’s quarterly results how many iPhones have a Retina display.

But we can do one thing, that is looking at the number of iPhones supporting OpenGL ES 2.0 and thus cocos2d 2.0:

It’s official now: over three quarters of iPhones are capable of running OpenGL ES 2.0 enabled (cocos2d 2.0) apps and games. There are less than 11% iPhones which don’t support OpenGL ES 2.0.

Given the grey area of almost 14% we can estimate that OpenGL ES 1.1 iPhones make up only 15% of the market, whereas OpenGL ES 2.0 iPhones make up around 85% of the market. This is based on the simple observation that newer iPhone models outperformed the older devices by a wide margin, so the unknown area is made up of more iPhone 3GS than iPhone 3G devices.

Of course this doesn’t factor in the number of iPod Touches with OpenGL ES 2.0 and the iPads, which are all capable of running OpenGL ES 2.0 apps.

### Including iPod Touches

Since Apple combines sales numbers for all iPod models, it can only be estimated how many of them are iPod Touches. That number should be at around 25% if we’re looking only at the “iPhone form factor” devices (no iPads):

We know from a [source (March 2011)](http://www.appleinsider.com/articles/11/04/19/apples_samsung_lawsuit_notes_over_60_million_ipod_touch_sold.html) that at this time there were 60 million iPod Touches. I used that number to calculate a factor of iPod touch vs iPhone sales. I haven’t updated the factor to reflect the decline of iPod sales in recent quarters, so the actual iPod touch sales numbers could be slightly lower.

### And then there’s the iPad

The iPads now make up 20% of all iOS devices:

If you consider all devices, the OpenGL ES 1.1 faction (iPhone + iPhone 3G) almost certainly makes up less than 10%. Accordingly, universal app developers have even less motivation to continue supporting OpenGL ES 1.1 devices.

### iPhone 5 and iPad mini

Given how the iPhone 4S more than doubled the sales of the quarter before it’s release, it’ll be interesting to see how the iPhone 5 will do. If Apple can repeat this success, the iPhone 5 could help breach the 50 million sales per quarter mark for iPhone sales since Q3 2012 iPhone sales clocked in at 26 million.

The iPhone 5 is [very likely going to be announced on September 12th](http://www.macrumors.com/2012/07/30/apple-media-event-all-but-confirmed-for-mid-september-iphone-launch-likely/). The iPhone 5 is [widely expected to feature a taller display](http://www.macrumors.com/2012/05/14/what-a-tall-iphone-5-with-4-inch-display-looks-like/) with a [resolution of 1136×640](http://www.macrumors.com/2012/08/07/ios-6-automatically-scales-to-fit-taller-1136x640-iphone-display/), an extra 176 vertical pixels compared to current iPhone Retina resolution of 960×640. And then there are also rumors about an [upcoming 7.85″ iPad mini](http://www.macrumors.com/2012/08/20/apple-to-ramp-up-7-85-ipad-mini-production-in-september/) with an as of yet unknown resolution, but it might use a 1024×768 resolution labelled as “Retina” due to the smaller form factor.

### Abandon Ship! Or not?

Sure, the iOS market is diversifying, but with current and these two future models we would still have to deal with only 6 different resolutions (480×320, 960×640, 1136×640, 1024×768, 2048×1536, ?x?), and at least two of them use the simple scale factor 2x.

Now that we can safely abandon OpenGL ES 1.1 devices, we will soon be facing the next difficult decision: whether to stop supporting the non-Retina iPhone 3GS as well as the comparatively underpowered iPad 1 with too little memory (256 MB). The problem is that we’re missing data on the individual models. That will make it more difficult to justify the decision.

Let’s hope that more friendly app developers share not only their iOS version usage statistics but also iOS device model statistics. The device model statistics will become more important over the course of the next 1-2 years.

While I’m at it, have you considered dropping support for iPhone 3GS and iPad 1 for your app? Or are you going all-in and still support even the OpenGL ES 1.1 devices? Why?

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I don’t like the 480×320 (2x mode) on iPhone retina display, the 3G/3GS one looks much better. I didn’t liked that move from Apple, forcing all developers to use stupid vector art and big resolutions on mobile devices. Bigger resolution and crisp graphics don’t imply better apps or games.

Thanks for this article! Tons of quick information.

So what are game artists gonna need to do? I’ve been doing a lot of pixel art last few weeks, mostly on a 1024×768 canvas. I try to avoid vector graphics, because the ‘flashy’ vector graphics can’t match the retro look i’m getting now. The 1136×640 resolution is what bothers me the most atm.

Any advice on this?

The good thing about the widescreen resolution is that it’s just that: wider. Besides the fullscreen background images you can accommodate for the larger screen by merely considering it during gameplay. For example just allowing iPhone 5 users a wider view area, and/or not placing any interactive things at the screen borders. No image scaling is necessary.

I think it’ll be a good approach for fullscreen images to design them for 1136 width and simply use the same images for iPhone Retina, or crop them. But cocos2d has no file suffix for widescreen, so you’d have to selectively load one or the other image depending on widescreen availability.

Alright. Thanks! Perhaps we should slowly take html5’s media query approach, by developing for specific (minimal) screen widths. Then selecting the best image available within two width boundaries.

Atm i’m thinking of targeting 960 and 1024 for in-game, and 960, 1024 and 1136 for backgrounds. Where 960 will be scaled down to 480 for non-Retina.

Great article! Where did you get the sources from? I’m trying to figure out the sales breakdown of different iPhone products but it seems that not a lot of public information is disclosed.

Main Sources: Apple’s quarterly press releases, and Wikipedia. The rest articles from the web, for example where they disclosed information Apple had to provide during a lawsuit which shed light on how sales for (I think) iPod devices were split.