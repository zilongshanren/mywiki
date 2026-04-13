---
title: Saying Goodbye to a Singleton
url: http://www.learn-cocos2d.com/2011/10/goodbye-singleton/
author: Tom Kirby-Green says
published: '2011-10-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I’m just a programmer, trying to comprehend.

[cc lang=”cpp”]

-(void) dealloc

{

[steveJobs release];

steveJobs = nil;

}

[/cc]

Steve’s public @interface was one of vision, drive and passion. His private @interface remained largely that: private.

Steve’s @implementation was not perfect, and it had a particularly nasty bug that eventually brought down the whole system. But by that time the parts of his @implementation that worked perfectly had accomplished a lot, and influenced a lot of other objects through indirection. Even directly on occasion.

His memory imprint on those objects will continue to affect their runtime behavior for a long time.

We mourn the deallocation of a Singleton, if ever there was one.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Ah yes, but one of Steve’s parting gifts was Automatic Reference Counting, so this becomes:

{}

becomes

”

sad story indeed

Too young, it’s sad…

A singleton is a horrible anti-pattern that is a glorified global used to hack together a bad/wrong design. Please do not equate this with Steve Jobs as he was a great man.

A Singleton is a powerful design pattern in the right places and for the right purpose. Goto has its uses, too. Hell, even Windows, if you consume it with a glass of ice water.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


I’ve yet to see a game engine that doesn’t use Singletons. I’ve yet to see any user interface framework that doesn’t use Singletons. They’re being used for a reason, and for a good reason I might add.