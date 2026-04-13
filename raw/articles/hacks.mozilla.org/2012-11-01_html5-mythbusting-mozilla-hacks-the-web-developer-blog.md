---
title: HTML5 mythbusting – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/11/html5-mythbusting/
author: Chris Heilmann
published: '2012-11-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The ongoing discussion about the “readiness” of HTML5 is based on a lot of false assumptions. These lead to myths about HTML5 that get uttered once and then continuously repeated – a lot of times without checking their validity at all.

## HTML5 doesn’t perform?

The big thing everybody who wants to talk about the problems with HTML5 is performance. The main problem here is that almost every single comparison misses the fact that you are comparing apples and pears (no pun intended).

Comparing an HTML5 application’s performance with a native App is comparing a tailored suit with one bought in a shop. Of course the tailored suit will fit you like a glove and looks amazing but if you ever want to sell it or hand it over to someone else you are out of luck. It will not be the same for the next person.

That is what native Apps are – they are built and optimized for one single environment and purpose and are fixed in their state – more on that later.

HTML5, on the other hand [by its very definition](http://www.w3.org/TR/html-design-principles/#media-independence) is a web technology that should run independent of environment, display or technology. It has to be as flexible as possible in order to be a success on the web. In its very definition the web is for everybody, not just for a small group of lucky people who can afford a very expensive piece of hardware and are happy to get locked into a fixed environment governed by a single company.

Native applications need to be written for every single device and every new platform from scratch whereas an HTML5 App allows you to support mobiles, tablets and desktops with the same product. Instead of having fixed dimensions and functionality an HTML5 App can test what is supported and improve the experience for people on faster and newer devices whilst not locking out others that can not buy yet another phone.

Native Apps on the other hand do in a lot of cases need an upgrade and force the end user to buy new hardware or they’ll not get the product at all. From a flexibility point of view, HTML5 Apps perform admirably whilst native applications make you dependent on your hardware and leave you stranded when there is an upgrade you can’t afford or don’t want to make. A great example of this is the current switch from Apple to their own maps on iOS. Many end users are unhappy and would prefer to keep using Google Maps but can not.


[HexGL](http://hexgl.bkcore.com/) – a WebGL powered racing game

Seeing that HTML5 is perfectly capable on Desktop to exceed in performance, from scrolling performance to [analyzing and changing video on the fly](https://developer.mozilla.org/en-US/docs/Manipulating_video_using_canvas) up to [running full 3D games at a very high frame rate](https://developer.mozilla.org/en-US/demos/detail/bananabread) and have [high speed racing games](http://hexgl.bkcore.com/) we have to ask ourselves where the problem with its performance lies.

The answer is hardware access. HTML5 applications are treated by mobile hardware developed for iOS and Android as second class citizens and don’t get access to the parts that allow for peak performance. A web view in iOS is hindered by the operating system to perform as fast as a native App although it uses the same principles. On Android both Chrome and [Firefox show how fast browsers can perform](http://blog.mozilla.org/blog/2012/06/26/mozilla-launches-a-speedy-and-powerful-upgrade-to-mobile-browsing-with-firefox-for-android/) whereas the stock browser crawls along in comparison.

The stock browser on Android reminds us of the Internet Explorer of the 90s which threatened to be set in stone for a long time and hinder the world wide web from evolving – the very reason Mozilla and Firefox came into existence.

In essence HTML5 is a Formula 1 car that has to drive on a dirt road whilst dragging a lot of extra payload given to it by the operating system without a chance to work around that – for now.

## HTML5 can not be monetized?

HTML5 is a technology stack based on open web technologies. Saying that HTML5 has no monetization model is like saying the web can not be monetized (which is especially ironic when this is written on news sites that show ads).

Whilst on the first glance a closed App-market is a simple way to sell your products there is a lot of hype about their success and in reality not many developers manage to make a living with a single app on closed App markets. As discovery and find-ability is getting increasingly harder in App markets a lot of developers don’t build one App but hundreds of the same App (talking dog, talking cat, talking donkey…) as it is all about being found quickly and being on the first page of search results in the market.

This is where closed App markets with native Apps are a real disadvantage for developers: Apps don’t have an address on the web (URL) and can not be found outside the market. You need to manually submit each of the Apps in each of the markets, abide to their review and submission process and can not update your App easily without suffering outages in your offering.

An HTML5 App is on the web and has a URL, it can also get packaged up with products like Adobe [PhoneGap](http://phonegap.com ) to become a native application for iOS or Android. The other way around is not possible.

In the long term that begs the question what is the better strategy for developers: betting on one closed environment that can pull your product any time it wants or distributing over a world-wide, open distribution network and cover the closed shops as well?

Many apps in the Android and iOS store are actually HTML5 and got converted using PhoneGap. The biggest story about this was the [Financial Times releasing their app as HTML5](http://apps.ft.com/ftwebapp/) and making a better profit than with the native one. And more recently the [New York Times](http://www.businesswire.com/news/home/20121002005602/en/York-Times-Launches-HTML5-Web-App-iPad) announced it was following suit with its Web app.

## HTML5 can not be offline?

As HTML5 is a web technology stack the knee-jerk reaction is thinking that you would have to be online all the time to use them. This is plain wrong. There are many ways to store content offline in a HTML5 application. The simplest way is the Web Storage API which is [supported across all modern browsers](http://caniuse.com/#search=localstorage) (excluding Opera mini which is a special case as it sends content via a cloud service and has its own storage tools). You can also store the application itself offline using AppCache [which is supported by all but Internet Explorer](http://caniuse.com/#search=appcache
). If you have more complex data to store than Web Storage provides you can use either IndexedDB ([for Chrome and Firefox](http://caniuse.com/#feat=indexeddb)) or WebSQL ([for iOS and Safari](http://caniuse.com/#feat=sql-storage)). To work around the issues there are libraries like [Lawnchair](http://brian.io/lawnchair/) available to make it easy for developers to use.

## HTML5 has no development environment?

One concern often mentioned is that HTML5 lacks in tooling for developers. Strangely enough you never hear that argument from developers but from people who want to buy software to make their developers more effective instead of letting them decide what makes them effective.

HTML5 development at its core is web development and there is a quite amazingly practical development environment for that available. Again, the main issue is a misunderstanding of the web. You do not build a product that looks and performs the same everywhere – this would rob the web of its core strengths. You build a product that works for everybody and excels on a target platform. Therefore your development environment is a set of tools, not a single one doing everything for you. Depending on what you build you choose to use many of them or just one.

The very success of the web as a media is based on the fact that you do not need to be a developer to put content out – you can use a blogging platform, a CMS or even a simple text editor that comes with your operating system to start your first HTML page. As you progress in your career as a developer you find more and more tools you like and get comfortable and effective with but there is no one tool to rule them all. Some developers prefer IDEs like Visual Studio, or Eclipse. Others want a WYSIWYG style editor like Dreamweaver but the largest part of web developers will have a text editor or other of some sorts. From Sublime Text, Notepad++ up to VIM or emacs on a Linux computer, all of these are tools that can be used and are used by millions of developers daily to build web content.

When it comes to debugging and testing web developers are lucky these days as the piece of software our end users have to see what we build – the browser – is also the debugging and testing environment. Starting with Firefox having Firebug as an add-on to see changes live and change things on the fly, followed by Opera’s Dragonfly and Safari and Chrome’s Devtools, all browsers now also have a lot of functionality that is there especially for developers. [Firefox’s new developer tools](https://wiki.mozilla.org/DevTools) go even further and instead of simply being a debugging environment are a set of tools in themselves that developers can extend to their needs.

Remote debugging is another option we have now. This means we can as developers change applications running on a phone on our development computers instead of having to write them, send them to the phone, install them, test them, find a mistake and repeat. This speeds up development time significantly.

For the more visual developers Adobe lately released their [Edge suite](http://html.adobe.com/) which brings WYSIWYG style development to HTML5, including drag and drop from Photoshop. Adobe’s [Edge Inspect](http://html.adobe.com/edge/inspect/) and PhoneGap makes it easy to test on several devices at once and send HTML5 Apps as packaged native Apps to iOS and Android.

In terms of deployment and packaging Google just released their [Yeoman](http://yeoman.io/) project which makes it dead easy for web developers to package and deploy their web products as applications with all the necessary steps to make them perform well.

All in all there is no fixed development environment for HTML5 as that would neuter the platform – this is the web, you can pick and choose what suits you most.

## Things HTML5 can do that native Apps can not

In essence a lot of the myths of HTML5 are based on the fact that the comparison was between something explicitly built for the platform it was tested on versus something that is also supported on it. Like comparing the performance of speedboat and a hovercraft would result in the same predictable outcome. The more interesting question is what makes HTML5 great for developers and end users, that native applications can or do not do:

**Write once, deploy anywhere**– HTML5 can run in browsers, on tablets and desktops and you can convert it to native code to support iOS and Android. This is not possible the other way around.**Share over the web**– as HTML5 apps have a URL they can be shared over the web and found when you search the web. You don’t need to go to a market place and find it amongst the crowded, limited space but the same tricks how to promote other web content apply. The more people like and link to your app, the easier it will be found.**Built on agreed, multi-vendor standards**– HTML5 is a group effort of the companies that make the web what it is now, not a single vendor that can go into a direction you are not happy with**Millions of developers**– everybody who built something for the web in the last years is ready to write apps. It is not a small, specialized community any longer**Consumption and development tool are the same thing**– all you need to get started is a text editor and a browser**Small, atomic updates**– if a native app needs an upgrade, the whole App needs to get downloaded again (new level of Angry Birds? Here are 23MB over your 3G connection). HTML5 apps can download data as needed and store it offline, thus making updates much less painful.**Simple functionality upgrade**– native apps need to ask you for access to hardware when you install them and can not change later on which is why every app asks for access to everything upfront (which of course is a privacy/security risk). An HTML5 app can ask for access to hardware and data on demand without needing an update or re-installation.**Adaptation to the environment**– an HTML5 app can use responsive design to give the best experience for the environment without having to change the code. You can switch from Desktop to mobile to tablet seamlessly without having to install a different App on each.

Let’s see native Apps do that.

## Breaking the hardware lockout and making monetization easier

The main reason why HTML5 is not the obvious choice for developers now is the above mentioned lockout when it comes to hardware. An iOS device does not allow different browser engines and does not allow HTML5 to access the camera, the address book, vibration, the phone or text messaging. In other words, everything that makes a mobile device interesting for developers and very necessary functionality for Apps.

To work around this issue, Mozilla and a few others have created a set of APIs to define access to these in a standardized way called [Web APIs](https://wiki.mozilla.org/WebAPI). This allows every browser out there to get access to the hardware in a secure way and breaks the lockout.

The first environment to implement these is the [Firefox OS](http://www.mozilla.org/en-US/firefoxos/) with devices being shipped next year. Using a Firefox OS phone you can build applications that have the same access to hardware native applications have. Developers have direct access to the hardware and thus can build much faster and – more importantly – much smaller Apps. For the end user the benefit is that the devices will be much cheaper and Firefox OS can run on very low specification hardware that can for example not be upgraded to the newest Android.

In terms of monetization Mozilla is working on their own [marketplace for HTML5 Apps](http://www.mozilla.org/en-US/apps/) which will not only allow HTML5 Apps to be submitted but also to be discovered on the web with a simple search. To make it easier for end users to buy applications we partner with mobile providers to allow for billing to the mobile contract. This allows end users without a credit card to also buy Apps and join the mobile web revolution.

## How far is HTML5?

All in all HTML5 is going leaps and bounds to be a very interesting and reliable platform for app developers. The main barriers we have to remove is the hardware access and with the WebAPI work and systems like PhoneGap to get us access these are much less of a stopper than we anticipated.

The benefits of HTML5 over native apps mentioned above should be reason enough for developers to get involved and start with HTML5 instead of spending their time building a different code base for each platform. If all you want to support is one special platform you don’t need to go that way, but then it is also pointless to blame HTML5 issues for your decision.

HTML5 development is independent of platform and browser. If you don’t embrace that idea you limit its potential. Historically closed platforms came and went and the web is still going strong and allows you to reach millions of users world-wide and allows you to start developing without asking anyone for permission or having to install a complex development environment. This was and is the main reason why people start working with the web. And nobody is locked out, so have a go.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 124 comments

Ollie WellsNovember 1st, 2012 at 07:43JoeNovember 1st, 2012 at 08:49Chris HeilmannNovember 1st, 2012 at 09:10JoeNovember 1st, 2012 at 12:54DavidNovember 1st, 2012 at 17:40Robert O’CallahanNovember 2nd, 2012 at 02:34DavidNovember 4th, 2012 at 20:40mpmediaNovember 1st, 2012 at 09:05Chris HeilmannNovember 1st, 2012 at 09:13EelisNovember 1st, 2012 at 12:16Chris HeilmannNovember 1st, 2012 at 14:01Justin McCandlessNovember 1st, 2012 at 23:16EelisNovember 2nd, 2012 at 08:20FabianNovember 1st, 2012 at 10:15Chris HeilmannNovember 1st, 2012 at 10:31NinjaWarrior1976November 1st, 2012 at 11:01weNovember 1st, 2012 at 11:07MichaelNovember 1st, 2012 at 11:27Bobby NewmarkNovember 1st, 2012 at 11:32ScottNovember 1st, 2012 at 13:16Chris HeilmannNovember 1st, 2012 at 13:25PlutoNovember 3rd, 2012 at 14:11pjmlpNovember 1st, 2012 at 13:45Chris HeilmannNovember 1st, 2012 at 13:55Haakon LøtveitNovember 2nd, 2012 at 06:39PlutoNovember 3rd, 2012 at 14:22Achim SchlemmerNovember 1st, 2012 at 14:25LukeNovember 1st, 2012 at 15:05Chris HeilmannNovember 1st, 2012 at 16:05LukeNovember 1st, 2012 at 19:19Chris HeilmannNovember 2nd, 2012 at 01:17LukeNovember 2nd, 2012 at 05:32Ants BullNovember 1st, 2012 at 16:45LukeNovember 2nd, 2012 at 05:14bobxNovember 1st, 2012 at 15:56Chris HeilmannNovember 1st, 2012 at 16:01Jon HNovember 2nd, 2012 at 09:14Ryan BradyNovember 1st, 2012 at 16:54Chris HeilmannNovember 2nd, 2012 at 01:18AndrewNovember 2nd, 2012 at 01:51Robert O’CallahanNovember 2nd, 2012 at 02:37TomasNovember 2nd, 2012 at 07:57FrankNovember 13th, 2012 at 13:36facebook_jonathan.hart.sfNovember 28th, 2012 at 12:34Tony GNovember 1st, 2012 at 18:32Chris HeilmannNovember 2nd, 2012 at 01:17notzedNovember 3rd, 2012 at 16:59JoeNovember 3rd, 2012 at 17:18Chris HeilmannNovember 4th, 2012 at 03:45Antoine BapstNovember 5th, 2012 at 06:14Robert O’CallahanNovember 2nd, 2012 at 02:38jeff fallNovember 5th, 2012 at 16:14Robert NymanNovember 5th, 2012 at 16:25Chris HeilmannNovember 5th, 2012 at 16:32GhaladenNovember 7th, 2012 at 10:15Jonathan HartNovember 28th, 2012 at 12:29Luther Goh Lu FengNovember 1st, 2012 at 19:21Robert O’CallahanNovember 2nd, 2012 at 02:39One size fits allNovember 1st, 2012 at 19:38LoriNovember 1st, 2012 at 20:14Joey MartinezNovember 1st, 2012 at 20:29Joey MartinezNovember 1st, 2012 at 20:26Chris HeilmannNovember 2nd, 2012 at 01:05Joey MartinezNovember 2nd, 2012 at 12:33Andrew BettsNovember 2nd, 2012 at 04:42VivienNovember 2nd, 2012 at 05:39Alex BertramNovember 2nd, 2012 at 05:40Chris HeilmannNovember 2nd, 2012 at 08:15Alex BertramNovember 2nd, 2012 at 09:34Neil CarpenterNovember 2nd, 2012 at 07:18Willian CarvalhoNovember 2nd, 2012 at 09:35ShawnNovember 2nd, 2012 at 10:03ShawnNovember 2nd, 2012 at 11:06Antoine BapstNovember 5th, 2012 at 07:55mpmediaNovember 2nd, 2012 at 11:16thinsoldierNovember 2nd, 2012 at 17:52Joe YNovember 2nd, 2012 at 21:24RobNovember 2nd, 2012 at 21:50PaulNovember 3rd, 2012 at 06:12ianNovember 3rd, 2012 at 07:20Chris HeilmannNovember 3rd, 2012 at 12:29GuestNovember 3rd, 2012 at 12:18notzedNovember 3rd, 2012 at 15:59Chris HeilmannNovember 3rd, 2012 at 16:10notzedNovember 3rd, 2012 at 16:30notzedNovember 3rd, 2012 at 16:25Jeff HammelNovember 3rd, 2012 at 18:22AbeNovember 3rd, 2012 at 18:23Chris HeilmannNovember 4th, 2012 at 03:42AbeNovember 4th, 2012 at 16:26Max PolkNovember 4th, 2012 at 13:59WladNovember 4th, 2012 at 16:01Chris HeilmannNovember 5th, 2012 at 01:03wladNovember 5th, 2012 at 02:48Chris HeilmannNovember 5th, 2012 at 03:56Antoine BapstNovember 5th, 2012 at 04:22wladNovember 5th, 2012 at 04:56Antoine BapstNovember 5th, 2012 at 05:28Antoine BapstNovember 5th, 2012 at 07:49Antoine BapstNovember 5th, 2012 at 04:21wladNovember 5th, 2012 at 05:05wladNovember 5th, 2012 at 06:22Antoine BapstNovember 5th, 2012 at 06:26Antoine BapstNovember 5th, 2012 at 08:00Antoine Bapst (@superfly_FR)November 5th, 2012 at 02:33Antoine Bapst (@superfly_FR)November 5th, 2012 at 02:40underhillNovember 5th, 2012 at 07:04Robert Nyman [Mozilla]November 5th, 2012 at 08:13LukeNovember 5th, 2012 at 16:49underhillNovember 6th, 2012 at 06:52Kyosuke KawateNovember 6th, 2012 at 00:28KentNovember 6th, 2012 at 16:20mpmediaNovember 7th, 2012 at 10:43mpmediaNovember 7th, 2012 at 10:44GhaladenNovember 7th, 2012 at 09:59MarcoNovember 10th, 2012 at 13:14Dave De SilvaNovember 13th, 2012 at 22:02YABE YujiNovember 22nd, 2012 at 15:31Mandeep SinghNovember 24th, 2012 at 23:31anatoliy KuzmenkoNovember 28th, 2012 at 10:52Blake CallensDecember 11th, 2012 at 14:52Joe PereiraJanuary 3rd, 2013 at 22:34steve porkerJanuary 20th, 2013 at 15:03JanetJanuary 29th, 2013 at 12:53