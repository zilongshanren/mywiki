---
title: Cocos2D installer updated, added Cocos3D
url: http://www.learn-cocos2d.com/2011/04/cocos2d-installer-updated-added-cocos3d/
author: Byron says
published: '2011-04-06'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

I have updated the [unofficial Cocos2D installer](http://cocos2d-central.com/files/file/6-installer-for-cocos2d-cocos3d-for-ios-mac-os-x/) to include the cocos2d-iphone-v1.0.0-rc version so that you can use the Xcode 4 templates. I also added Cocos3D so that you don’t have to run its install scripts anymore.

The installer now installs the following folders to your ~/Documents folder:

- cocos2d-iphone-0.99.5 (latest stable)
- cocos2d-iphone-1.0.0-rc (latest unstable)
- cocos3d-0.5.3 (latest beta)

### Warning: Project Templates are buggy!

Depending on Cocos2D/3D version and the version of Xcode, you’ll notice that some of the project templates will not compile without manually fixing some compile errors. This has nothing to do with the installer, the same thing happens when you install the templates manually with the .sh scripts.

For example, the project templates for cocos2d-iphone-1.0.0-rc do not work in Xcode 3 - the ones for Xcode 4 work fine. The Cocos3D project template does not work out of the box in Xcode 4, you have to manually copy and add the Cocos3D files (refer to the readme for more info). The version for Xcode 3 works fine.

Based on the Xcode version you currently use for developing new Cocos2D projects:

- Xcode 3: use the Cocos2D v0.99.5 and Cocos3D Project Templates to start new projects. You can manually update to Cocos2D v1.0.0 afterwards.
- Xcode 4: you will have to start with Cocos2D v1.0.0 (rc). If you want to develop Cocos3D applications, refer to the readme to learn the manual steps involved in creating a working Cocos3D project.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Hi Steffen,

I’m curious why you chose not to contribute all these changes and additions back to the cocos2d project?

Many reasons. Mainly because I’ve been accused of being a competitor because of the Starterkit I’m selling, so there’s a resentment and generally conflicts of opinion. Like other commercial developers I have been banned from the official forum. So I don’t see why I should contribute.

The other concerns which I share with other developers are that of compromises and being independent. It’s much easier to publish something Cocos2D related on your own terms, and you get the added benefit of website traffic that typically goes along with a contribution of value. This is the reason why so much of Cocos2D code and information is spread far and wide on blogs rather than being added to the official distribution respectively the Cocos2D wiki.

@Steffen - you are not banned from the cocos2d forum AFAIK (and I’m an administrator of it). I just checked your gaminghorror user status and there is no reason why you should not be able to post on the forum. As far as I am aware the only limitation is that you can not advertise competing products, this applies to everybody.

Thanks Steve for pointing this out. Last time I checked, which was maybe 9 months ago, any new posts of mine never became visible to other users. I’m not banned in the sense that I can’t login but new posts I write won’t show up. I verified this with another account, not hiding my identity, which was quickly put in the same state of posts not visible to the public. I spoke to others who reported the same experiences which lead us to believe we are banned. In effect what seems to be the case is that new posts are held for moderation and never go live. Whether we actually promote our products or not.

Quite frankly the competing products rule is not acceptable because it’s too vague, eg when does a product start being a competing product to Sapus Tongue source? Is this the case as soon as you sell source code of any game project, or only if it includes one or more of the same selling points of Sapus Tongue? What about a commercial Level Editor, wouldn’t that be competing with Level SVG and if not, would it start becoming a competing product if the announced game editor comes out? What about games on the App Store? Sapus Tongue is a commercial game. And what about the few existing promotional links - why haven’t they been removed? A rule is only as good as how well it is put into effect, this also goes for “treat people with respect” which I have repeatedly pointed out I wasn’t treated with respect, with no action being taken.

So I don’t want to have to consider any of this or discuss gray areas, I’d rather set my own rules. I also compared incoming traffic from cocos2d-iphone.org with other sources and realized that by far the most traffic I ever received from cocos2d-iphone.org were from posts on the main page, with or without links. Traffic from the forum is almost negligible. That too makes me question both effectiveness and necessity of the non-compete rule.

For what it’s worth, I’m on good terms with the developers of BATAK Duel and iPhone Game Kit. I think it’s fair to say that we’re all making good money and we are not the least bit cannibalizing on our customers. The market for tailor-made game source code products is big and growing, and it would generally be favorable for Cocos2D if commercial products could be sold via an affiliate store on cocos2d-iphone.org with a xx% share going to Ricardo. Commercial tool and source developers would be more than happy to do that and split revenue! Don’t fight it, embrace it. My $.02.