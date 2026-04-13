---
title: Cocos2D Xcode Project on Github
url: http://www.learn-cocos2d.com/2010/11/cocos2d-xcode-project-github/
author: Joe Glenn says
published: '2010-11-04'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

[My Cocos2D Xcode project is now on Github.](https://github.com/GamingHorror/cocos2d-project) Open-source, free, properly MIT Licensed, includes the rootViewController and supports Cocos2D v0.99.5 rc0.

I’m also working on (with) a greatly enhanced version of the Xcode project. It integrates [wax (Lua)](https://github.com/probablycorey/wax) and a Game Object Component System that i termed “gocos”. Also comes with a lot more useful convenience classes.

But the big idea is to actually upload (or link within github, if I can figure out if and how that works) all dependent projects into one repository, so that you can download everything at once and it works out of the box. Currently there are 3 projects referenced by cocos2d-project: gocos (let’s call it a library of convenience and gameplay code for Cocos2D), wax (Lua support) and obviously cocos2d-iphone. So everything that’s needed is going to be bundled in one big package, which voids all of the version incompatibility issues.

You can still experiment with different versions of these libraries but in that case I think you know what you’re doing and that issues are to be expected. But being a github repository, you can of course clone and commit changes.

### Appetizer

Here’s what I’ve done with Lua. I’m currently using it only as a better plist replacement for settings. It’s better than plist because you can comment on each item, you can sort them easily, you can run functions and algorithms to generate values or load additional data, and in general it’s a lot easier to work with than the plist editor. Here’s a reduced config.lua that is loaded at runtime into a hierarchy of NSDictionary objects:

[cc lang=”lua”]

local config =

{

AccelerometerControls =

{

UpdatesPerSecond = 60, — 60 Hz

Responsiveness = 0.997,

SensitivityX = -2,

SensitivityY = 2,

MaxVelocity = 100,

},

}

return config

[/cc]

And this line of code loads these values and assigns them to the correspondingly named properties of the target class:

[cc lang=”objc”]

[Config loadPropertiesFromKeyPath:@”AccelerometerControls” target:self];

[/cc]

That’s all you need to do to transfer the values from config.lua into a class instance. Huge timesaver! The only drawback is that it currently can’t differentiate between float, int and bool (due to NSNumber), so it currently only supports float properties.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

Excellent, I look forward to seeing wax and gocos integrated. You should consider forking and modding the stock templates (a bit more lightweight mind you), then ask Riq to pull.

Cheers

[…] Cocos2D Xcode Project on Github […]

Steffen,

Great job on the cocos2d-project. I have just purchased your book on Apress…its great material. One question, does your cocos2d-project support iPad deployments? I am getting a -[UIWindow setRootViewController:]: unrecognized selector when attempting to run in the iPad 3.2 simulator. I’m using SDK 4.1, but target of iOS 3.2

-Chris

Not directly, I removed the iPad targets because I think the important decision, whether to make an iPad app as a seperate app or building a universal app should be up to the developer. The process is really simple. Highlight a target, open the Xcode “Project” menu and select “Upgrade Current Target for iPad…”.

Thanks for buying my book, I appreciate it.![:)](../../../wordpress/wp-includes/images/smilies/simple-smile.png)


Cool. I’m looking forward on ‘gocos’. Cheers.