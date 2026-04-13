---
title: 'iOS Sales Statistics including Q1 2012: Split by Model and OpenGL ES 2.0 Support'
url: http://www.learn-cocos2d.com/2012/03/ios-sales-statistics-q1-2012-split-by-model-opengl-es-2-0-support/
author: Ios Sales Statistics Including Q; OpenGL … - About The New iPhone says
published: '2012-03-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

With Apple’s blazing Q1 2012 quarterly results, which sees iPhone sales double (!) that of the previous Q4 2011 and last year’s Q1 quarter, it’s time to update [my iOS Device sales statistics from July 2011](http://www.learn-cocos2d.com/2011/07/dropping-dead-opengl-es-v1/).

[Apple’s Quarterly Results Reports](http://www.apple.com/pr/library/2012/01/24Apple-Reports-First-Quarter-Results.html) have one big flaw for those interested in per-device numbers: Apple only mentions how many iPhones, iPods and iPads they have sold in each quarter, but this includes all models. So you have to exclude the discontinued models as well as somehow determine (if only by guesstimating) how many iPod touch vs regular iPods, or how many iPhone 3G vs iPhone 3GS have been sold in that quarter.

I took the publicly available numbers and then used a reasonable guesstimate to split the device sales of two combined models in order to get a reasonably accurate estimate. I mainly wanted to determine how the gap is widening between the OpenGL ES 1.1 and OpenGL ES 2.0 models. This is particularly interesting for Cocos2D developers who may be wondering if it’s save to upgrade to Cocos2D 2.x or whether it’s still worthwhile to stick with Cocos2D v1.x to be able to deploy even to 1st and 2nd generation iOS devices.


The numbers are slightly different that those in my [previous iOS sales numbers post](http://www.learn-cocos2d.com/2011/07/dropping-dead-opengl-es-v1/), where I factored in things like older devices being lost, broken, stolen, or simply no longer in use and a generally diminishing interest of users to buy new apps the older their device is. The same considerations apply here but I avoided factoring them into the numbers this time.

You can [download the iPhone Device Sales Excel sheet here](https://www.learn-cocos2d.com/wordpress/wp-content/uploads/iPhone-Device-Sales2.xls).

### iPhone sales by model

The following numbers are official numbers from Apple and in million devices sold as of Q1 2012. Since Apple doesn’t report numbers per model, several sales numbers include multiple devices.

Note that my Excel uses the german 1,000 delimiter, which is a dot and not a comma. The number 20.254 stands for “20 million and 254 thousand”.


Rendered in full color using an eye-pleasing pie-chart, the same numbers look like this:

And split into devices which support either OpenGL ES 1.1 or OpenGL ES 2.0 we find that we have a number of over 33 million devices which may support either version, but we don’t know for certain because the sales of iPhone 3G (2nd generation, ES 1.1) and iPhone 3GS (3rd generation, ES 2.0) are combined. At most ES 2.0 device numbers may be as high as 86% or as low as 68%.

It’s safe to assume that every new iOS device generation sells a lot better than the previous generation devices, which means the iPhone 3GS sales numbers encompass at the very minimum 50% of the 33 million. That would place the distribution of ES 2.0 iPhone devices at 76%.

But I think sales are split more likely at around 30% to 70%, putting the iPhone 3GS device clearly in the lead. My rationale for this number is simply how much better each new generation of iOS devices has sold compared to the previous generation. That puts ES 2.0 iPhones neatly at the [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) percentage of 80%.

### Adding iPod touches to the mix

iPod touch devices are a lot more difficult to measure than iPhones because Apple simply releases numbers for “iPods sold”. And that includes non-iOS devices like the iPod nano and iPod shuffle.

There’s one [well-known source for iPod touch sales from March 2011](http://www.appleinsider.com/articles/11/04/19/apples_samsung_lawsuit_notes_over_60_million_ipod_touch_sold.html) (using Q2 2011 numbers) which puts iPod touch sales at 60 million compared to 108 million iPhones. In the subsequent quarters Q3 2011 to Q1 2012 Apple reported a total of 29,56 million additional iPod sales. Let’s be pessimistic and assume that only two thirds of these devices were iPod touch devices, bringing the total number of iPod touch sold to date to 80 million (30% of the total).

Applying the 80:20 Pareto numbers to iPod touches supporting ES 2.0 versus those models which only support ES 1.1, we end up with a total number of 210 million iPhone and iPod touch devices which support ES 2.0 compared to 52 million iPhone and iPod touch which only support ES 1.1. This changes the total 80% of ES 2.0 capable devices only in the fractional part. This is to be expected since iPhones and iPod touches essentially share the same lifecycle. Regardless, here’s the updated graph:

### Stirring it up with iPad numbers

The ES 2.0 compatibility gets a boost when you consider iPads since all iPad models support ES 2.0. Including Q1 2012 Apple has sold over 55 million iPads. That puts the total number of iOS devices sold at 318 million, and they’re distributed as follows:

The pie chart is now complete and includes all iOS devices. It shows the iPhones covering about 58% of the iOS market. The iPads share just over 17% of the market, putting the iPhone and iPod touch models clearly in the lead at 83%. But do keep in mind that iPad users are generally considered to be more affluent and have proven to be willing to pay more for their apps.

Lastly I can report an **84% market share of iOS devices that are compatible with OpenGL ES 2.0**:

For comparison, this is what the ES 1.1 vs 2.0 situation was three quarters earlier (GL ES 2.0 devices at about 66%):

![](../../../wordpress/wp-content/uploads/iphone_sold_by_gl_q2_2011.png)


The gap is clearly closing. I expect the total numbers of ES 1.1 devices (those 16%) to be cut in half (or more) with the Q3 2012 numbers, which will include additional iPad 3 sales and continued iPhone 4S sales.

### Summary

The once sensational 6 million sales of (original) iPhones now seem rather ludicrous if you look at the charts. With Apple able to double the quarterly iPhone sales with the iPhone 4S and Siri it certainly looks like we have yet to see the part of the iceberg that’s still looming underwater.

If you look at the overall iOS market and see an 84% share of ES 2.0 compatible devices, you shouldn’t think twice and start abandoning the ES 1.1 devices (iPhone, iPhone 3G, iPod touch 1st and 2nd generation) with your next project.

If you’re developing an iPad-only app there’s really no reason not to be using cocos2d-iphone 2.x since all iPads support ES 2.0 and nearly all of the early iPads that were shipped with iOS 3.2 should have been updated to iOS 4.0 or higher by now.

Universal app developers should also strongly consider going for cocos2d-iphone 2.x since you’ll be having “tons of fun” supporting both iPhone and iPad screen sizes already, it will require an additional effort with diminishing returns if you also want to support the 1st and 2nd generation devices.

If your app is simple and doesn’t push any technical boundaries you can easily support all devices but don’t expect too many additional sales by supporting 1st and 2nd generation devices. Most other apps should not, particularly if you consider the roughly ten-to-twenty-fold increase in CPU and GPU performance from the first iPhone to the latest iPad 3. It may simply be a waste of money and resources trying to have your app run well across such a wide range of devices.

At this point a moment of silence seems appropriate to commemorate all Android developers. ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

[…] is the original post: iOS Sales Statistics including Q1 2012: Split by Model and OpenGL … ch_client = "danielshifflett"; ch_width = 468; ch_height = 60; ch_type = "mpu"; ch_sid = "Chitika […]

Thank you. I had nearly no doubts about moving to 2.0 being the best choice. Now I have none.

[…] Update: please find the iOS Device Sales Statistics for Q1 2012 here. […]

[…] also explain the Q1 2012 iOS Device Sales statistics, the newly released Kobold2D v1.1 and v2.0 progress, and finally I got a surprise present: Mountain […]

I don’t understand why you are counting original iPhone and iPhone 3G in your sales numbers for Apple’s Q1 2012. There were no original iPhone and iPhone 3G sold in Q1 2012, not even refurbs. There are simply no more original iPhone and iPhone 3G left for Apple to sell.

Of course, I may be wrong

but I doubt if those old models would account for even 0,1 % of sales in the last quarter. I think you should redo your calculations assuming no original iPhones and no iPhone 3G sold in Q1 2012.

I count all sales “up to and including Q1 2012” 😉

“The following numbers are official numbers from Apple and in million devices sold as of Q1 2012.”

Never mind my previous comment. I should do a better job of reading what you meant, rather than what my brain thinks you meant.![:-)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


[…] market, and with Android at 500 million activations (for comparison, Apple is at something around 180 million iPhones sold, total) the startup has a real chance of hitting 100 million users across both devices soon enough […]

[…] market, and with Android at 500 million activations (for comparison, Apple is at something around 180 million iPhones sold, total) the startup has a real chance of hitting 100 million users across both devices soon enough […]

[…] that ‘Android is at 500 million activations (for comparison, Apple is at something around 180 million iPhones sold, total) the startup has a real chance of hitting 100 million users across both devices soon enough […]

Hi!

I updated to cocos2d 2.0 just when it was released. It wasn’t a hard decision at all: almost same API, more powerful, the future. I asked myself: “Why taking into account ES 1.0 users? Are you sure they’re gonna like and buy your game?”. So I thought that it’s better to use new technologies to make a better game for less people.

Regards!

[…] Of course I strongly recommend the cocos2d-iphone v2.0 version with ARC enabled, seeing how the old devices have an ever diminishing, probably below 15% market share. […]

[…] is an update to the last sales statistics post to include Apple’s Q2 and Q3 2012 results as well as adding Macintosh sales: Apple Device […]