---
title: 'Book Feedback: the Spiders got fixed!'
url: http://www.learn-cocos2d.com/2010/09/spiders-fixed/
author: Stahlmandesign Says
published: '2010-09-22'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

Just a quick note: the single most requested respectively criticized part of my book was in Chapter 4 where I’m introducing the moving spiders. The @interface code was missing from the book as well as the line in the init method calling one of the new methods. These are added now, so the code works directly from the book. It should be in the next chapters & code update (but don’t ask me when, I don’t know either).

Thanks for letting me know about it, and in general for all the great feedback! What amazes me most is that there wasn’t a single person saying that the book isn’t good, or not good enough, or could be so much better if only … Normally one has to expect at least a certain percentage of responses to be less than happy, but no, every single one was positive, even those with criticism. And a few very overwhelmingly appreciative. I can’t say thank you enough for all of that praise, it’s been a great source of inspiration and motivation, especially at the times when I was super-busy and working 14-hour days for a week. Thank you! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


### Amazon Book Reviews

I thought it’ll be great to see some of the cocos2d book reader reviews appearing on Amazon. If you’d like to write a review, I’d really appreciate it, because right now there are none. Here are the links to the cocos2d book for every Amazon store worldwide:

[Amazon.com (United States)](https://www.amazon.com/Learn-iPhone-iPad-Cocos2D-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=books&qid=1284664414&sr=8-1)

[Amazon.ca (Canada)](https://www.amazon.ca/Learn-iPhone-iPad-Cocos2D-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=books&qid=1284664526&sr=8-1)

[Amazon.co.uk (United Kingdom)](https://www.amazon.co.uk/Learn-iPhone-iPad-Cocos2D-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=books&qid=1284664462&sr=8-1)

[Amazon.de (Germany)](https://www.amazon.de/Learn-Iphone-Ipad-Cocos2d-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=books-intl-de&qid=1284664401&sr=8-1)

[Amazon.fr (France)](https://www.amazon.fr/Learn-Iphone-Ipad-Cocos2d-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=english-books&qid=1284664539&sr=8-1)

[Amazon.co.jp (Japan)](https://www.amazon.co.jp/Learn-iPhone-iPad-Cocos2D-Development/dp/1430233036/ref=sr_1_1?ie=UTF8&s=english-books&qid=1284664550&sr=8-1)

Please mention that you read the book in its Alpha form. I don’t want anyone to think that the reviews are hoaxed because they came in before the book came out. Not everyone may be aware of Apress’ alpha program, and pre-release reviews are often viewed with skepticism.

Btw, Amazon.com lists the book’s release date as December 30th. Right now that’s just a rough date, like I said earlier, the goal is to get the book out in time for Xmas. Hopefully even several weeks before Xmas.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

In your code for the spider game, you use the update(ccTime)delta to make sure you only update the score once a second, despite the frame rate. But you do not consider elapsed time when calculating velocity or player movement. I’ve been trying to figure this out for days and it just doesn’t work like it used to in Flash for some reason. I used to get the time elapsed since last type in the loop and consider that in the amount of velocity I added. In Cocos2D my player jumps much further when FPS gets slow, and runs slower etc.

In general you just multiply with the delta time. However, because delta is very small (usually around 0.08f) the values after multiplication will be very small, so you need to account for that by multiplying it with 10 or more, otherwise it may seem like the object isn’t moving at all.

Delta time based movement is explained in another example later in the book, I don’t remember which chapter though.