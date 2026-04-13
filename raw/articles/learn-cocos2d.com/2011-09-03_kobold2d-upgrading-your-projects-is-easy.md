---
title: 'Kobold2D: Upgrading your Projects is easy!'
url: http://www.learn-cocos2d.com/2011/09/kobold2d-upgrading-projects-easy/
published: '2011-09-03'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

A couple months ago I wrote a tutorial explaining [how to upgrade Cocos2D in an existing project](http://www.learn-cocos2d.com/2011/05/update-cocos2d-iphone-existing-project/).

I was able to cut the description down to only five concrete steps, but there’s still a lot of text to follow and caveats to consider. I designed [Kobold2D](http://www.kobold2d.com/) exactly to make it easy to solve the issue of upgrading projects to newer versions of the game engine.


### Introducing the Kobold2D Project Upgrader!

How about selecting the projects you’d like to upgrade, then click a button to have it done for you?

That’s what the aptly named Kobold2D Project Upgrader tool is for:

You simply run the tool from the latest Kobold2D version. The tool then gathers a list of upgradeable projects of previous Kobold2D versions that it finds automatically. You then only have to select the projects you’d like to upgrade, and the tool does the rest for you.

“Upgradeable” here means all projects that haven’t been upgraded and won’t overwrite an already existing project with the same name. So you’ll only see which tools actually **need** upgrading. And by “the rest” I mean copying the Xcode workspace, Xcode project and project files, and correctly migrating the project into a possibly existing workspace, and similar things that used to be a manual process.

Convenience, meet simplicity! ![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


### Funny Side Note

In case you wonder what an **Upgrader** is, and what the process of upgrading entails, [Wikipedia has the answer](https://en.wikipedia.org/wiki/Upgrader):

Upgrading may involve multiple processes:


- Vacuum distillation to separate lighter fractions, leaving behind a residue with molecular weights over 400.
- De-asphalting the vacuum distillation residue to remove the highest molecular weight alicyclic compounds, which precipitate as black/brown asphaltenes when the mixture is dissolved in C3–C7 alkanes, leaving “de-asphalted oil” (DAO) in solution.
- Cracking to break long chain molecules in the DAO into shorter ones.
- Hydrotreating may also be employed to remove sulfur and reduce the level of nitrogen.

I think that perfectly describes the upgrade process for Cocos2D projects. 😀

PS: Since Cocos2D was never designed to make its projects upgradeable, I’ll have to disappoint those who hope that the Kobold2D Project Upgrader tool could be adapted for Cocos2D projects.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |