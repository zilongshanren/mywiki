---
title: How to compress, encode and write data to XML with zlib, base64 and xswi
url: http://www.learn-cocos2d.com/2013/02/compress-encode-write-data-xml-zlib-base64-xswi/
author: Thomas Tempelmann says
published: '2013-02-21'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

In order to write Tiled’s TMX file format I needed to do exactly this: figure out how to compress data, encode it as a string, and write it to XML.

I wrote down what I learned from using **zlib**, **base64** and **xswi - XML Stream writer for iOS** (a single Objective-C class) while writing [KoboldTouch](http://www.learn-cocos2d.com/store/koboldtouch/)‘s TMX writer.

I split it into two articles in the [Essential Cocos2D](http://www.koboldtouch.com/display/IDCAR/Essential+Cocos2D) section of the [www.KoboldTouch.com homepage](http://www.koboldtouch.com/display/KTD):

**How to compress and encode data with zlib and base64****How to write XML on iOS with xswi (XML Stream Writer)**

I was positively surprised how relatively painless zlib and base64 encoding worked (I expected the worst!) and how simple and effective xswi is for writing XML compared to any other XML library.

I’ll probably continue to add those articles to Essential Cocos2D rather than posting them on this blog. Confluence is just so much more convenient for writing technical documentation than WordPress.

Final word: Enjoy! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Steffen, that 2nd link to the xswi page appears to be dead.

Thanks, fixed.

great share. thanks