---
title: 'Spelling iPhone App sent to Beta Testers :: nklein software'
url: http://nklein.com/2010/01/spelling-iphone-app-sent-to-beta-testers/
author: Pat
published: '2010-01-29'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I am pleased to say that I just sent my [first iPhone app](http://nklein.com/software/spell-it-iphone-app/) out to some friends to beta test. I expect to forward it along to Apple for inclusion in the App Store some time in the next week or two.

At this point, I am far more comfortable with Objective-C and the Cocoa class hierarchy than I was even a month ago. I still think Objective-C is awful. You take a nice functional Smalltalk-ish language, you throw away most of the ![spell-it-large](../../assets/6a7500c5fafef8de.jpg)


functional, you pretend like you have garbage collection when you don’t, you strip out any form of execution control, you add some funky compiler pragma-looking things (including one called

synthesizethat only fabricates about half of what you’d want it to build), you change the semantics of

->, and then you interleave it with C! Wahoo! Instant headache!

But, after I found the for-each sort of construction, my code got quite a bit simpler. A whole bunch of loops like this:

MyItem* item;

while ( ( item = (MyItem*)[ee nextObject] ) != nil ) {

...

}

went to this:

...

}