---
title: My Xcode 4 Template Doc is now available
url: http://www.learn-cocos2d.com/2011/04/xcode-4-template-doc/
author: Kim Le says
published: '2011-04-21'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

As promised a while ago my [Xcode 4 Template Documentation](http://www.learn-cocos2d.com/store/xcode4-template-documentation/) efforts have finally produced a result. Please refer to the [product page](http://www.learn-cocos2d.com/store/xcode4-template-documentation/) for more information.

I’ve put in roughly 70 hours. Might have been even more, I didn’t keep track. I would appreciate your support by purchasing the documentation!

I also checked again if any new source of information on Xcode 4 Templates has come up, but couldn’t find any new sources. As of today and roughly 4 weeks after I started with my Xcode 4 documentation endeavour, there’s still very little documentation about Xcode 4 templates on the net. The following are the only external sources I referred to:

[Minimal Project Template with example](http://blog.boreal-kiss.net/2011/03/11/a-minimal-project-template-for-xcode-4/)[List of replacement placeholder strings](http://gallantgames.com/post/3771670972/xcode-4-templates)[Solution on how to place files in subgroups](http://stackoverflow.com/questions/5445640/creating-sub-groups-in-xcode-4-templates)

The marketing dude in my mind tells me I should probably mention that the information you get from the above links is just a fraction of what you’ll find in my Xcode 4 Template documentation. 😉

### Happy Easter!

Or to be politically correct: Happy Holidays! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Does your Xcode4 templates show us how to produce a multiple target application - iPad, iPhone, iPad Free, iPhone Free.

Yes but not directly. Xcode provides us with a “universal app” project template that is mentioned in one of the project template tutorials. In essence, if you use this template as an Ancestor in your template, it’ll add a popup option which allows you to choose from iPhone, iPad and Universal apps. It doesn’t require re-inventing the wheel.

Bought your doc, thanks, it was a good read. I might have missed it, but is there info in there about (point me to the page number, if available):

1) Creating folder references (shows up as a blue folder icon in the Xcode project, just points to a folder on disk)

2) Setting the path type for a Framework. Through my experimentation, I would have thought (according to the Frameworks guide) it would pick up frameworks in /Library/Frameworks, but it appears any Frameworks listed in the plist are relative to the SDK.

Of course I have tried to scour the Internet for this information, and thought I would find some tidbits of information in your doc.

1) This might be possible by specifying a PathType for a Definitions item, see page 36. Also if you check out page 38, copying entire folders, this process always creates an additional and unwanted folder reference. I believe it’s possible to create a folder reference but at this point I have not been able to figure out how it’s possible or whether it’s possible at all. The folder reference created by copying folders might just be a bug.

2) That’s a setting you can change with PathType, page 36. However the correct type for “relative to project” is currently unknown but you can use an absolute path.

Thanks! Too bad about (1).

For (2), have you encountered a way so tilde (~) expansion works for absolute paths? Appears Xcode 4 does not expand it. I guess I could go with “/Users/___USERNAME___” but don’t really want to hard-code the username in (the templates are user specific anyway)