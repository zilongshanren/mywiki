---
title: 'cocos2d Book, Chapter 15: The Final Chapter'
url: http://www.learn-cocos2d.com/2010/10/cocos2d-book-chapter-15-final-chapter/
author: Mike Gleason says
published: '2010-10-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

### Chapter 15 - The Final Chapter

This is it. The last one. I don’t know what’s going to be in it. It’s supposed to give the reader a “where to go next” kind of outlook. I hope that one of the places will be here, but obviously there’s tons of places to go and tons of things for cocos2d developers to learn.

If you have a particular idea what should be included in the greater cocos2d developer outlook kind of sense, please let me know!

### Summary of working on Chapter 14 - Game Center

Amazing! Simply amazing. I think I fell in love with Game Center in the process, I haven’t worked with a networking API that’s so smooth, straightforward and easy to comprehend. No thanks to Apple’s already excellent step-by-step documentation. Still, there were a couple pitfalls and things that one could forget, and I did, that I’ve obviously included in the chapter.

On the other side, with almost a week late for this chapter, I realized how time consuming network programming is. There’s a lot of testing going on, and especially if you’re testing on two devices the process is incredibly inefficient compared to a simple single-player game. You always have to deploy to two devices for every test, and every time the delay between request and response adds to the time spent on testing. Add to that common network errors such as a drop in connection or something blocking the line with a download, and you’re up for a fun ride.

But that alone didn’t account for the one week delay. In the past two weeks I’ve been helping to renovate someone’s apartment, I got a cold, I held a presentation at the [Macoun Mac OS X conference](https://macoun.de/?page_id=13) (about cocos2d obviously) while still recovering from the cold. Then our pet cat Yoshi had to see the vet and almost died during anesthesia because of a [pulmonary edema](https://en.wikipedia.org/wiki/Pulmonary_edema). On the brighter side I’ve also attended a wedding and wrote a GameKitHelper class for this chapter which contains more stuff than I could describe in the book, including storing achievements which failed transmission, as is recommended but not implemented by Apple’s [Game Center Programming Guide](http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/GameKit_Guide/Introduction/Introduction.html).

That’s also why I haven’t been answering emails timely recently. Please be patient, I’ll get to yours soon!

### What’s left?

Now that I’m almost finished writing the book, what’s left? Obviously I have to review technical and other edits done by Apress. Current chapter 13 is in technical review while chapter 6 is in editorial review, after which it’s ready for production. So I’ll still be busy reviewing and making changes and additions to chapters during October and probably even November.

Then there’s the issue of the example projects having used three different versions of cocos2d, starting with 0.99.3. That was actually an oversight on my part because at the time I had 0.99.4 available. Luckily those changes are really insignificant for the first few projects. The DoodleDrop game already uses 0.99.4 and so does most of the book’s code. But for the Game Center chapter, I had to migrate the Tilemap project from 0.99.5 beta 1 to beta 3 and that was a huge step. It was easier to simply create a new project from the latest cocos2d template, then re-adding all game source code and resources to the new project. Still, that’s doable.

The bigger issue I have here is the fact that I can’t change anything in the book anymore, so the code should reflect what’s in the book. If the book mentions CCLabel then the code should use CCLabel and not CCLabelTTF. What I think is probably going to be a good compromise is to update the important (final) versions of each chapter’s example projects to cocos2d v1.0 once that is released. Obviously the code supplied with the book will remain as it is described in the book, so the upgraded code would be for reference only and a separate download. Whether I wait for v1.0 depends on how progress towards v1.0 is coming along around the book’s release date some time in December 2010.

In hindsight, I really wished I had used my [Xcode template project](http://www.learn-cocos2d.com/knowledge-base/tutorial-professional-cocos2d-xcode-project-template/) and used that throughout the book. Back then I decided against it because it was important for me to write the code like almost all cocos2d developers would do. Now I regret the decision because I could have changed the way cocos2d developers start new cocos2d projects for the better. The whole updating process for cocos2d is a major PITA and then some, so I think I need to bring this issue to the table more frequently, more actively. At least until the cocos2d template installation procedure is changed to **not** copy all of the source code into each new project and then leaving it up to the developer to deal with upgrades.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Can’t wait !!!

I really wish APRESS would go ahead and put the rest of the Alpha chapters and source on their web site…