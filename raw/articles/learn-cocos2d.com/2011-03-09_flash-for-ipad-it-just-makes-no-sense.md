---
title: Flash for iPad? It just makes no sense!
url: http://www.learn-cocos2d.com/2011/03/flash-for-ipad-makes-no-sense/
author: Joe says
published: '2011-03-09'
source_blog: Learn & Master Cocos2D Game Development
source_site: http://www.learn-cocos2d.com
category: game programming
fetched: '2026-04-13'
---

With each new iOS device you’ll be sure to hear this argument:

“It doesn’t support Flash! Baaaaah, piece of crap!”


What bothers me most is that this mantra is repeated even by intelligent people, even developers fall into that behavior. But they don’t have an argument other than “I want it, I want it”. No really, it’s actually “I think I want it, I think I want it”. Why?

“Uh … well, Flash games!”

### Here’s the problem …

If you like playing Flash games, either some in particular or generally consuming the daily new dose of throwaway games, you’ll be emotionally connected to these games. Of course you would want to play them on any device that seems perfectly capable of running Flash. So I understand the notion of wanting to have Flash on an iOS device. It’s entirely understandable.

What really bothers me, is how little even intelligent people put into what they’re actually demanding. Here’s a smack in the face - think about it!

Other examples include:

“Press any key to continue.”

“Use WASD to control your character, Space to jump, Ctrl to shoot.”

“Move the mouse cursor to the edge of the screen area to scroll in that direction.”

### First of all …

All games that make use of the keyboard are out. Add to that the games which require a mousewheel or the distinction of left and right mouse clicks. I bet this will disqualify at least half of all Flash games. I expect that estimate is likely to be much higher if someone were to compile actual statistics of Keyboard and Mouse input use in Flash games.

Next, any game that relies on the concept of “mouse over” won’t work satisfactory, or not at all. There is no “mouse over” on a touchscreen device, there is only “drag & drop”. You have to touch the screen to move the cursor - it’s possible that games will interpret this as some kind of click and click, or drag and drop operation.

Finally, there’s the matter of precision. A mouse cursor has a hotspot that has an exact pixel position. A finger has a touch area, and although you can calculate the center point to be the touch location, it will be quite imprecise. Especially when you consider that users don’t see the exact point they’re touching - their finger is blocking the view. No Flash game has been designed to take into account that the clickable area will have a relatively large range of uncertainty. Many hidden objects games require you to touch locations to almost pixel-perfect accuracy - not to mention the unspeakable horrors of Flash UI Design with small fonts and even smaller buttons.

If you go into details, I’m sure there’ll be plenty more design issues. They may be subtle but overall important enough to make some games less enjoyable, unfair, unplayable or allow for exploits which could skew the highscores towards either mobile or web users. That’s bad.

### Technical reasons

There are of course technical reasons why Flash, and specifically Flash games, won’t work well on an iPad or iPhone. The 1 GHz Dual-Core CPU of the iPad 2 is still an order of a magnitude slower than the slowest, Intel-based Mac Mini which clocks in at around 1.8 GHz (also Dual-Core). On older iDevices there’s only a single core ARM CPU with around 500 MHz. And surely you’ve experienced Flash games that didn’t run too well on a Mac mini, right? Imagine how they would perform on a mobile device.

Then we have the memory issue. The iOS devices have at most 512 MB of memory down to 128 MB. Not that bad, unless you consider how much is actually available for Apps. On a 128 MB device it’s just 30-35 MB. Not much you can do with that, and I don’t expect any Flash game to be optimized for this constrained amount of memory. Worse yet, a Flash game won’t receive memory warnings from the device and it’s developer certainly won’t respond to this warning. Plus, since running in the browser, the browser on the iDevice will consume some of the available memory itself. So what you get is some content-heavy Flash games and apps which will simply crash at a certain point, or not run at all because they’re out of memory. That’s not a good user experience.

We also have to consider the issue of screen resolution. Most Flash games run in a window with varying dimensions. On an iOS device, first of all you’d never get the fullscreen experience because the native resolution will almost always be different. Since Flash runs in the browser, the Flash games will have to be zoomed and scaled to fit the screen. In the worst case, the user has to do this manually because double-tapping inside the Flash window probably would be interpreted by Flash as a command, rather than by the browser as the command to zoom and fit the double-tapped content. In any case scaling the content will degrade visual quality while consuming more power because the content needs to be scaled (in most cases: up) by either the CPU or GPU.

What about Loading bars? Do you like loading bars? I’m sure you do. Because on an iDevice, the best you’ll get is a WiFi connection. I suppose that’ll be acceptable. But what if you’re on the road and only get 3G or even Edge? Do you like waiting several minutes for your Flash game to start up every time you run it? I don’t think so. Just try to remember how Flash websites felt back in the 90s when all we had were dial-up connections.

### This could be better if …

Yes, if the iOS devices or even the iPads supported Flash, I’m sure Flash developers would take a little more care of the details that they actually can take care of. For example providing a real touch-aware user interface, or designing the whole game with touchscreen devices in mind.

However, only a minority of Flash developers would do so. The low costs of developing Flash apps and games doesn’t make cross-platform compatibility a real possibility for most. They make 90% or more of their revenue from hosting them on ad-supported gaming websites like Kongregate. Any other platform than the web has no relevance to Flash developers, and the iPad simply wouldn’t change that.

Once you do have a successful Flash game, it’s also much more lucrative to simply make an iOS version of it. Take for example Canabalt. It’s [free on the web](http://www.adamatomic.com/canabalt/), but it sells for a relatively high price of [$2,99 on iTunes](http://itunes.apple.com/app/canabalt/id333180061?mt=8). It’s also wildly successful. And it’s also a good example of why many Flash games simply won’t work on an iDevice - the screenshot further up is from the Flash version of Canabalt.

### But Flash is good for other things!

Yes, if you like Ads, sure.

Oh, you mean those designer websites that you can’t even figure out how to use on your desktop? No?

What then … don’t tell me Youtube or those other movie sites. For one, there’s an App for that. And trust me, you’ll be too busy doing other stuff with your iPad than watching Youtube videos.

“There’s this site that won’t work …” - Really, you visit [www.disney.com](http://disney.go.com/) every day? You’re adorable! ![:)](../../../wordpress/wp-includes/images/smilies/icon_smile.gif)


So far I have not come across a website that’s entirely Flash-driven (eg won’t work without Flash) and that has you coming back. The one that gets closest is [github.com](https://github.com/) - but no point in downloading source code to your iDevice, is there? Most Flash-only websites are once-in-a-lifetime show-off events. A comedy act, if you so will. The second time, it’s just not as much fun. And you can absolutely live without them.

I run a Flashblocker on my browsers, all I’m missing are Ads and rarely a few gizmos that I don’t even notice aren’t there. Almost all websites are intelligent enough to default back to a non-Flash version, which not only works better, it’s also easier to use, loads faster and consumes less memory and CPU time. There you go.

### To put it bluntly

Flash has no place on the iPad, or any iDevice.

My real problem with that is the people who repeat the “no Flash support” mantra don’t stop to think about the actual problems in supporting Flash apps and games on a device like the iPad. It just won’t deliver the same experience as it does on the desktop. Those experiences can not be brought over to a mobile device by merely supporting a specific technology.

Moreover, I wish those in favor of Flash support for iPad would actually make an argument, rather than repeating “But that’s what I want.” - you’re like little kids who can literally only be dragged past a candy shop or toy store, crying all along. No toys for you, grow up!

|
|

[Follow @kobold2d](https://twitter.com/kobold2d)
I very much enjoy the learning process, the pushing of boundaries (mine and yours and that of technology), having the freedom to pursue whatever is on my mind, to boldly program what no one has programmed before, and to write about what I've learned. |

I understand a good chunk of what you’re saying, but don’t necessarily agree with the other chunk personally. You can’t make statements on design / user interaction when they aren’t designed for iOS devices in the first place. Of course it would be a problem using a keyboard and/or both mouse buttons, but obviously they wouldn’t rely on that input if they were made for iOS.

Don’t get me wrong, I am a long term iPhone & iPad user, and always will be - and I will always create iOS apps natively, and rarely write actionscript for web apps these days at all. I don’t feel iOS devices are hindered by not supporting flash, but then again there are still quite a lot of websites with flash items on them which make my viewing experience far less enjoyable on the iPad for example. But that’s where my view on it limits, if I want to play a game ill go to the appstore, it’s purely on websites/web applications where I think it couldn’t hurt sometimes!

Hope that my view makes sense

I am quite sure that many will argue all this points, but they are well exposed and make a lot of sense.

As an iPhone and iPad user I just complain about the lack of flash when I am forced to visit certain pages that have deep integration with flash and have no other way to deliver their information in plain html. In most cases flash was not needed to make the page more interesting. So I can say that my overall experience has been rewarding and entertaining.

Steffen, Thanks for publishing your opinion and please continue the excellent work.

Steffen, I respect you a lot for your work in the Cocos2D community, but I think it’s unfortunate that you’re engaging in this sort of apologetics. iOS does have flaws and shortcomings, and its lack of Flash support is one of them. You seem to be trying to spin it into a good thing, as though you work in Apple’s marketing department.

All of your arguments against Flash games on the iPhone and iPad apply equally to non-Flash games; that is, any game not specifically designed for a touch interface won’t work well. So? You go on to say:

“However, only a minority of Flash developers would [optimize their games for touch screen devices]. The low costs of developing Flash apps and games doesn’t make cross-platform compatibility a real possibility for most. They make 90% or more of their revenue from hosting them on ad-supported gaming websites like Kongregate. Any other platform than the web has no relevance to Flash developers, and the iPad simply wouldn’t change that.”

That sounds like pure speculation to me. It’s obvious that Flash developers won’t bother with iOS while it doesn’t support Flash, but I don’t think that allows you to assume that there are no circumstances under which they would find it worthwhile to target iOS if they could.

Games are less important to me than video, though, which you dismiss as though it should be of no concern to anyone: “What then … don’t tell me Youtube or those other movie sites. For one, there’s an App for that. And trust me, you’ll be too busy doing other stuff with your iPad than watching Youtube videos.”

Since switching to Android, I can’t count the number of non-YouTube Flash videos I’ve enjoyed on my device. And contrary to Apple’s FUD, probably 95% of the videos I’ve tried play beautifully on my Android phone. That includes videos not optimized for mobile playback. Oh, and how about those YouTube videos that don’t allow mobile playback, like all of Funimation’s anime content? Yeah, I can watch those on my phone in the browser.

Even if every single website which uses Flash video had a corresponding iOS app, I still wouldn’t WANT to install dozens of apps just to watch videos. To do so is a ridiculous waste of time, space, and effort. If a friend links me to a Flash video, I don’t want to have to find and open the appropriate app, and then find the video, in order to watch it. Just let me watch it in the browser using fullscreen mode.

All of that said, the quality of the Flash experience is really a non-issue to me. The fact of the matter is that Flash is a feature that a reasonably large subset of users want. It costs Apple nothing to implement it because they wouldn’t be the ones doing so - they just have to allow Adobe to do it. Yet they’re vetoing it, and I think they’re doing so in large part because it goes against their OWN interests; not those of their consumers. Flash would reduce the amount of control they have over their platform, and they’re not comfortable with that.

From a consumer standpoint, how is that defensible?

I’m not an apologetic. I know I should have sticked to the subject matter: demanding Flash because you want to play the current Flash games on the iPad. That’s just not reasonable and I’m explaining why. The last paragraph, well that’s just my experience. I don’t know what websites others are visiting - the only site I know which is practically useless without Flash is github.com.

Other than that, I was personally surprised when I started using Flashblockers over a year ago, how little content on the web actually relies on Flash and that is beneficial or even important for the website. The only thing I had to make exceptions for were Youtube videos and github. But I mixed that personal experience with the actual argument why the current Flash games simply can’t provide the same experience that the people who demand “Flash for games” would expect.

I know that Apple’s decision has a lot to do with preventing other to circumvent the approval process. I would actually welcome that. I wouldn’t apologize for that. I would prefer if we wouldn’t have to deal with an approval process other than a technical QA check.

I also know that, compared to the target market “web”, the iOS devices are a niche. Some Flash developers would surely recognize that niche and put it to good use to become lucrative with fewer competitors, but the great majority will ignore it. Apple announce they sold over 100 million iPhone in the last 4 years. With iPods and iPads that’s maybe 150 million iOS devices. Compare that to over a billion desktop and mobile computers, which about 200 million new ones sold each year. iOS is a niche market in comparison. I’m not saying this wouldn’t change, but it would surely be a very slow process.

All in all, I just don’t like to hear people defend the “Flash for iPad” argument with current Flash games. They can’t be the goal. And personally, I have no need for Flash on my iPad or any iDevice. But that’s just me.

I tested à flash game on Google phone it worked quite good. Android is cool that supports it. More choice to the people!

A lot of websites don’t even take the trouble to provide a static image for display when Flash isn’t available - it’s a simple thing to do and is better than having empty areas (or worse - encouraging users to update/download Flash right now rather than actually purchasing whatever product/service the website is selling). So I agree that many developers wouldn’t bother adapting games to touch-only controls.

While I don’t think that the lack of Flash support means the iPad is crap, I’d still like to see Flash support because it’s annoying that parts of the web are unavailable when they don’t really have to be. Your argument drifts into the statement that the unavailable parts aren’t of interest to you, which is obviously subjective.

Are there significant numbers of Flash games that would work on the iPad, which people want to play and which don’t make revenue from ads? I believe so.

The UK’s lottery operator has instant win scratch card games which require Flash. Many casino and bingo sites require Flash throughout. These games have simple interfaces which would work fine with tablet taps. These may account for more than 10% of Flash gaming by some calculations and certainly by player expenditure.

These games are either not cost-effective to develop on the App Store or expressly prohibited.

It’s not impossible to solve the keyboard issues - especially on the iPad which has a screen big enough to run a keyboard and game at the same time.

The ideal solution would be for Flash content to not automatically appear in mobile WebKit but be substituted by a Flash Play icon, which when tapped would run the Flash content either full screen (if video detected) or with a bar of buttons for mouse and keyboard actions much like the LogMeIn app lets you use a Mac or PC within a touch interface.

This puts the running of Flash content under the control of the user, and would mean only one Flash thing was running at a time.

In addition (and this may is probably already detectable in some form - I haven’t programmed in Flash for a decade) Flash games should be able to detect that the device is exclusively touch input and show on-screen buttons when required and adapt input accordingly. Of course websites could still show a screen saying that the game does not work on iOS and link through to the App Store version if that’s their business model. Much like web developers can tailor their site to Mobile Safari if they want - but they don’t have to.

The lack of Flash isn’t a deal-breaker for me, but I don’t see why it’s impossible and I don’t see the continued absence as defensible on the iPad. Apple insist Flash is irrelevant almost as loudly as some people demand it.