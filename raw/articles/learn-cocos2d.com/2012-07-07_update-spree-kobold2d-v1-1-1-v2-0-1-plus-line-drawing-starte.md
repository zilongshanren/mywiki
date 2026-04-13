---
title: 'Update Spree: Kobold2D v1.1.1 & v2.0.1 plus Line-Drawing Starterkit with ARC'
url: http://www.learn-cocos2d.com/2012/07/update-spree-kobold2d-v111-v201-linedrawing-starterkit-arc/
published: '2012-07-07'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Get the latest versions of [Kobold2D from the download page](http://www.kobold2d.com/display/KKSITE/Kobold2D+Download) and [more details in the Release Notes](http://www.kobold2d.com/display/KKDOC/Kobold2D+Release+Notes).

Kobold2D v1.1.1 has been updated to include the latest version of cocos2d-iphone v1.1 (beta2b) from May 3rd this year. This version supports the -ipad and -ipadhd suffixes.

Both Kobold2D v1.1.1 and v2.0.1 have been updated to include the latest Chipmunk v6.1.1 and Chipmunk SpaceManager v0.1.3. Although unfortunately SpaceManager still isn’t fully compatible with cocos2d-iphone 2.0 because it still won’t rotate the sprites.

Again both versions include an **important fix for KKInput**: I’ve received several reports where users complained that KKInput is missing some events. Specifically the “ThisFrame” variants were prone to never fire. This is now fixed.

#### Line-Drawing Game Starterkit: ARC + cocos2d v1.1 & v2.0

While I’ve been meddling with Kobold2D updates I found this to be the perfect opportunity to update the [Line-Drawing Game Starterkit](http://www.learn-cocos2d.com/store/line-drawing-game-starterkit/) as well. **You now get four versions of the project**, two are using cocos2d-iphone v1.1 and the other two have been updated to work with cocos2d-iphone v2.0.

And each of the two cocos2d-iphone version projects allows you to choose between the ARC enabled project or the classic manual reference counting project. The included readme document explains this in greater detail. Suffice it to say you can simply choose with which to start: cocos2d v1.1 or v2.0 and either with ARC enabled or manual reference counting.

Of course I strongly recommend the cocos2d-iphone v2.0 version with ARC enabled, seeing how [the old devices have an ever diminishing, probably below 15% market share](http://www.learn-cocos2d.com/2012/03/ios-sales-statistics-q1-2012-split-by-model-opengl-es-2-0-support/).

And do use [ARC, it’s really a no-brainer not to bother with reference counting anymore](http://www.learn-cocos2d.com/2012/06/mythbusting-8-reasons-arc/).

If you’re an existing customer, you should have received an update email with your download link.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |