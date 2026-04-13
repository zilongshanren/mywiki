---
title: 'Another Great Cocos2D Tool: PhysicsEditor'
url: http://www.learn-cocos2d.com/2011/03/great-cocos2d-tool-physicseditor/
author: Paris Says
published: '2011-03-15'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

In my book I explained how to create collision shapes for physic engines using the freely available version of [VertexHelper Pro](http://itunes.apple.com/us/app/vertexhelper-pro/id411684411?mt=12). Granted, it works, but as soon as you need to update your shapes frequently or you have many different shapes to edit it’s going to be a lot of manual work and error-prone copy & paste between VertexHelper’s code generator and your source code.

#### VertexHelper, meet your replacement: PhysicsEditor

[PhysicsEditor](http://www.physicseditor.de/) was written by Andreas Löw, the author of the very popular [TexturePacker](http://texturepacker.com/) tool. He has proved again that he can create powerful yet easy to use tools for game developers.

The greatest part about PhysicsEditor: it can automatically trace your shapes to generate collision shapes and it works flawlessly! You can even tweak the amount of vertices (and a lot of other things) as needed, for example if your physics engine has a limitation on how many vertices can be used for a collision shape (Box2D default: 8 vertices).

But it doesn’t just create the collision shapes, it also allows you to edit physics properties of a shape that often go along with it. Density, friction, “bouncyness”, and other parameters can be tweaked in the GUI.

As they say, an image speaks louder than words, so I suppose a video speaks in a thousand images:


#### Not just Cocos2D

PhysicsEditor currently exports to Cocos2D + Box2D (Chipmunk/SpaceManager support is forthcoming and should be available soon) and also to[ Sparrow Framework](http://www.sparrow-framework.org/) + Chipmunk and of course [Corona SDK](http://www.anscamobile.com/corona/).

And it works on Windows, too! Which makes sense given that [Corona supports Android development under Windows](http://blog.anscamobile.com/2011/01/corona-sdk-is-now-on-windows/).

I also found this [post about PhysicsEditor with a working Flash example](http://www.emanueleferonato.com/2011/03/11/create-complex-box2d-shapes-in-a-click-with-physicseditor/) (at the bottom). It seems that even exporting respectively using PhysicsEditor with Flash + Box2D seems to work well. Wow!

#### Brace for impact!

Check out the [PhysicsEditor Features page](http://www.physicseditor.de/features/) to learn more about what this great tool can do for you! You can get PhysicsEditor alone for $17.94 but you can also [grab a bundle deal](http://www.physicseditor.de/store/) which includes TexturePacker for $29.99, or almost 20% off.

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

WOW! Andreas Löw does it again! superb work!

only one question to ask

how does it handle concave shares?

ok just read it covers this beautifully on its website! superb! i think its something vertexhelper was not helping with.

superb work Andreas! BTW why arent your tools on the Mac App Sore yet? are they coming?

can it work with Textures generated with Texturepacker? i.e generate shapes for 10-20 sprites included on a texture? instead of adding the individual files?

Hi Paris,

1) Thanks 😉

2) PhysicsEditor decomposes convex polygons into concave polygons and adds them as compound shapes to the physics engine

3) Mac App Store: Nope. Currently it’s for your own advantage: You can use the same license on MacOS and Windows and I can fix bugs within some hours. With Mac App Store you would have to wait until the app is approved.

4) That is planned but not yet fully implemented. Currently you need to add single sprites. With the next bigger release you’ll be able to import *.tps (TexturePacker Sheets) into PhysicsEditor

Cheers

Andreas

3) … plus Andreas would lose 30% of his revenue with little to no benefit. If I made a tool for the well-informed community of iOS game developers, the Mac App Store wouldn’t be my primary means of distribution either.

Thanks for the comments

Disagree with helping win/Mac cross lisencing since this would serve only a tiny minority, if any!

Disagree on losing 30% you could win a lot more sales by making you app visible In an evolving marketplace like the app store! You are actually losing sales now and not gaining 30% !!! You could see a lot more sales, personally I have been looking for developer tools in app store on a daily basis, did not see you there, if I did I would have bought your app a month ago, am an existing customer and found out about you app by a 3rd party blog, you could have emailed your existing clients about it btw!

Also if you competitor is there then you should be there! People looking to buy you competitors app could find you and buy your app instead, which is better btw!

At some point you will want to jump in the app store you might as well do it early and benefit from being there early!

My 2 cents! Sleep on it you will see my point!

I can’t speak for Andreas, but from my point of view the more focused a tool the less sense does it make to put it on the App Store. I’m not sure if this will be the case for Andreas’ tools or if they are widespread enough (Corona, Cocos2D, Sparrow, others) to warrant an App Store release.

Do you get 30% more customers? I doubt it. The risk that more customers who would buy it from the website would simply prefer to purchase from the App Store because it’s more convenient is a bigger issue. So you may actually lose revenue to Apple, as weird as it may sound.

You also don’t get customer info from Apple. This is the real value. Once you offer your product on the App Store, you do not get the customer email (for a newsletter or sending file updates), you do not get any analytics data on what they do on your site, which links they click, etc. and the website loses relevance because fewer people visit it, which means it’s likely listed further down in google searches.

In that sense I don’t understand the rush to the App Store. Most developers don’t consider what they give up in terms of not just revenue but also analytics, user statistics, SEO rankings and so on.

Steffen i understand what you are sayign but……

whats the real value of getting client info if you are not using it? Andras has my info but I didn’t get an announcement for a new product! maybe its time he start using mailchimp. Is it better to get contact info of people already your customers? or is it better to expose you product in a large store for new customers?

i have been looking for apps in mac app store from day 1, bought many apps i dint know since the offered functionality similar or better for other apps i am using. Andreas could take advantage of people searching the app store for anything related to box2d to corona or cocos2d and so on. There are many people that might not read a random blog to find your software. he might as well sell it for 30% more in the app store if he feels he is losing by giving commission to apple! People might opt to but it from he website to make use of win/mac cross licensing.

do you know how many developers paid for 5$ for Xcode just for the ease of getting updates easier from the app store? instead of downloading it manually every now and then?

Mark my words that at some point he will jump in the app store! its better done early than later thought!

What about actual reviews, that help make a lot making a sale, are those on Andreas website? don’t think anyone would believe them if they were there anyway! In the Mac App store thought you get to see really how other people think of a piece of software depending on the rating. many times i switched software i was using because of bad reviews, people pointed to better software!

Anyway i am one of the many that believe Mac App Store is a blessing not a curse both for the consumer and the developer!