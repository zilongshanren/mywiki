---
title: 'Cocos2D Book Update: Progress Report'
url: http://www.learn-cocos2d.com/2011/05/cocos2d-book-update-progress-report/
author: Dani says
published: '2011-05-29'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

It’s coming along great!

I completed the revisions on Chapter 1 through 5. The [entire source code is now updated](http://www.learn-cocos2d.com/2011/05/learn-cocos2d-book-source-code-update/) to use cocos2d-iphone v1.0.0 rc2. To make future code updates easier I also wrote a script that allows me to copy a newer cocos2d version to all projects, which essentially does Steps 1 & 2 described in the [Updating Cocos2D in an Existing Project](http://www.learn-cocos2d.com/2011/05/update-cocos2d-iphone-existing-project/) tutorial.

#### Most Notable Changes

**Chapter 4** now includes a description of [Glyph Designer](http://glyphdesigner.71squared.com/) for making Bitmap Fonts, and only mentions Hiero on the side. Glyph Designer is the better tool hands down.

**Chapter 5** has seen a revision of the paragraph that explains subclassing from NSObject. I think I went too far off course here and subclassing from CCNode will make a lot of things easier while still giving the same benefits regarding class composition.

In **Chapter 6** I decided to replace all descriptions of [Zwoptex](http://zwoptexapp.com/) with [TexturePacker](http://www.texturepacker.com/) as the preferred tool for making texture atlases.

For a while it looked like Zwoptex and TexturePacker would be competing on the same level. But recently Andreas Löw (TexturePacker & PhysicsEditor) made the move to [work full-time on his tools](http://www.learn-cocos2d.com/2011/05/cocos2d-podcast-andreas-lw/), whereas Robert Payne is [busy with a full-time job](http://zwopple.com/2011/05/04/zwopple-early-may-update/). I think the prospects are looking much better for TexturePacker now, and it is already leading in terms of features and update frequency.

That’s it for now.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Good work. I’m agree with Chapter 4 and 5 changes, but I think Zwoptex is a great tool for composing pixel art sprite sheets. Anyway I’m going to try TexturePacker too.

Regards.

No doubt about Zwoptex and Robert assured me that he will be releasing a big update (v1.5) soon.

But TP already packs a lot of useful extra features on top, and is much more likely going to see more updates simply because Andreas is working full-time on his tools. So looking into the future I don’t think Zwoptex can reclaim its leading position.

thanks! your dedication to cocos2d is awesome =)

Hi Steffen,

Great book and being a new developer coming in for IOS and Cocos2D, this book is I think now in the category of must read.

I have a suggestion for the beginners like me - It would be good to explain bit more in Chapter 5 about “How best to implement Levels”. I think this section/subject shall be explained more with code examples as it is one of the fundamentals in creating games.

Memory Saving technique is described for Multi-Scene by LoadingScene class but the same is not described in Multi-layer.

Not sure if there are already examples and you can guide me to - I want to create a game with multiple levels and the scene changes based on level user is in. I don’t want to create 50 classes if I have 50 levels.

Thanks and Regards

Sarab

Typically you would write a single Level class and feed that with the current level’s data. A level is a class, but each individual level is an instance of a level class simply with different data (object positions, which tile map to load, which graphic set to load, etc.). Currently, cocos2d is missing a really good editor to make creating level data easy, except for tilemaps where you can use Tiled.

Hi Steffen,

As a complete beginner to game development and an objective c novice I’ve found the book an incredible help!

I would like to second the request to have some more information on implementing levels, also if possible how to store level data and saving levels state. There does seem to be a reasonable amount of information on the internet but as a beginner I’m really struggling on how it should all connect together in a MultiLayerScene.

Many thanks,

Rob