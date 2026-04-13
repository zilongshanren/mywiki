---
title: A Conversation With Appeio Developer Harold Fudge – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/11/appeio-developer-interview/
author: Eduardo Bouças
published: '2012-11-26'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note: Appeio is no longer available, and Harold is now spending his time with his consultancy.**

*Last month we released Firefox Marketplace on the Aurora channel of Firefox for Android. This release has given developers an opportunity to start building a base of early adopters and get feedback on apps as the Marketplace grows.*

![Harold Fudge](../../assets/cf5ff76ac66e8500.jpg)

[Harold Fudge](http://haroldfudge.com/) is a Canadian web developer who was excited to be part of this first wave of apps for [Firefox Marketplace on Android](http://arstechnica.com/gadgets/2012/10/first-look-mozillas-firefox-marketplace-app-store-for-android/). [Appeio](http://appeio.com/), his device-responsive, cross-platform [app.net](https://join.app.net/) client, is the first of its kind in Firefox Marketplace. We were interested in talking to Harold to learn more about his approach to open web apps. Here’s how the email conversation went:

**HAROLD:** I’ve always been interested in technology. I’ve been drawn to computers partly for the pure thrill of creation but also because of the implications for communication between individuals and groups. I grew up in a small town in the center of an island during the 1980s and created simple apps for myself out of interest. Just as I finished high school suddenly the Internet emerged as something for everyone. I saw plainly the Internet was everything a computer was already, but infinitely expanded. It was my mission to be a part of it. I began to learn HTML and what it meant to be a web developer. You can see a selection of things I’ve built and am working on at [ hxf148.com](http://hxf148.com).

**Q:***What inspired you to develop Appeio, an app.net client for the Marketplace?*

In mid-August when App.net gained its initial funding I simply signed up out of an interest in the technology. I am not shy about trying different things or supporting an idea as it gets started, but unlike the average project I investigate, [App.net as an API service](https://github.com/appdotnet/api-spec/wiki) had an immediate pull for me. I really enjoy building things online and App.net offered a wide open low cost way to build apps with a powerful communications backend and a engaged early adopter set. This core idea hooked me and I quickly decided that if possible I only wanted to interact with the ADN (**A**pp **D**ot **N**et) through my own code as a way to force me to learn its methods and potential.

I looked at the options and while I have dabbled in iOS and Android programming I did not think I could quickly compete in the already heated race to build app.net clients for those platforms. I then turned to my strengths. I decided I would take upon the challenge to build a full-featured HTML5 app that would extend and improve my own skills and knowledge while providing a solid client for any device with a web browser.

I had been following the [Marketplace](http://marketplace.firefox.com/developers) project for some time and it seemed like a natural fit for Appeio. While being present in other app stores can lead to confusion, the Marketplace and its focus on HTML5 and other browser-based technologies is something I want to support and be part of. From the early days when I sat down to learn HTML, it was because I felt the future lay with technologies that enabled applications regardless of the underlying hardware, software or specific company policies.

**Q:***You’ve done a lot of mobile app development, what do you see as the biggest challenges for developing in HTML5?*

Just stating that you develop in HTML5 is a bit of an issue. What that really means is still a bit of a jumbled set of tools and technologies. When you sit down to develop an app, for iOS in particular, you are given a canvas and some predefined controls, methods and styling. You can ignore all of it, but if you are just starting out it gives you a powerful bridge to develop your idea into an actual app people would want to use.

Starting an app targeted at browsers on all devices with all methods of input is an interesting challenge. The power of CSS, HTML and JavaScript to deliver a great user experience is there, but it is hidden behind a learning curve filled with pitfalls and technology distractions. So then, the biggest challenge to me with starting a web app is often not showing if the idea is good, it is in deciding how it should be developed.

Starting from scratch is usually not an option in small web development shops like mine, so we turn to toolkits, IDEs and frameworks to build apps with. If this selection is not done carefully the idea/app/project can often be dragged down by the weight of its own underpinnings. It is crucial to decide what outside dependencies will help your app be realized. Some tools are helpful to get the software built, but eventually lead it to an unsustainable position.

My goal in facing this challenge is as the [KISS principle](http://en.wikipedia.org/wiki/KISS_principle) states. I try to pick well known, well supported tools that are well built and not over-designed/engineered. These can vary from project to project, but currently the combination of [Bootstrap](https://hacks.mozilla.org/twitter.github.com/bootstrap/), JQuery and CSS3 on the front end and when needed PHP/mySQL on the server side meet my personal objectives to build well, fast and light for as many devices as possible.

**Q:***What’s your advice to web developers who know their way around HTML5, JavaScript & CSS3, but are new to the world of mobile development?
*

Build everything to be screen responsive and mobile will fall into place as another supported part of your technique. We hear from all sides that mobile is the future, but when everything is mobile it does not mean that everything is small. It is pretty clear already that we are headed to a world with connected mobile screens of all sizes from wearable to desktop portable. And your web-based property should just work on them all.

This is not just about taking into account button sizes, finger-friendly navigation and how the actual presentation can be reflowed to different screen sizes. Mobile devices have less memory and processing power and often a web app that will work on a desktop is too much for a mobile browser. It takes some planning and a lot of testing. There is a good balance to find in almost any app that will allow it to run everywhere with a good user experience.

Don’t take on mobile as a unique special case needing separate and stripped down versions, everyone dislikes this and it’s futile. Make being mobile a fundamental part of your app from its inception and many of the gotchas found large screen first apps will start to melt away. It is not easier to make a fully screen-responsive HTML5 application, but it is better.

**Q:***What gets you excited about HTML5 app development? What do you see as the opportunity for independent developers like you?*

The truly exciting thing about HTML5 and web development is that it’s not done.

That it might never be done but it is open and continues to advance, keeping reasonable step with proprietary native app systems. Technologies by Apple, Google, Microsoft, RIM and others may and will have good long runs but at some point these companies need to make the next thing which is not always compatible with their previous thing. As devices get cheaper and more widespread, as operating systems continue to become more varied and transparent, the one constant they will have is the web.

There is something fundamentally appealing about the idea of a well-built app working well into whatever comes next. Things change and patches happen but the principles of the web specifications should mean that your app will load and run without too much fuss for as long as you want.

No one truly can say what computers will look like in 10 or 20 years but there is a high likelihood that they will have a browser to view the apps and sites we are all building right now. Many early websites continue to exist nearly two decades after they were launched. I believe this will happen again.

Many devices released only five years ago cannot today run the latest version of their operating system let alone the latest version of most apps for it. In contrast, most web apps built at the same time continue to operate or require only minor adjustments. Should a web app need a fix, it’s made and done, no updates for users and no waiting on approvals. It is much more interesting and exciting to me not to be bound by those restrictions, regardless of any short-term gains.

A final point on my excitement is that the next two to four years will be important steps forward for web development as specifications are finalized and simply what a web app is capable of in terms of WebGL, storage and other hardware interaction leaps ahead.

**Q:***At the moment, do you have any plans to port any of your other mobile apps to the Firefox Marketplace?*

I have spent much of this year rebooting my career direction and retooling my skill set in web development. Looking over what I have done and what I am looking to do going forward the Marketplace is a part of my plans. I think there are amazing and fun challenges to undertake in this space and having the Marketplace is going to be important to reaching more users. A place to offer high quality HTML5 apps to an informed set of individuals with the support of Mozilla is a great thing.

**Q:***What do you do to make your apps work well offline?*

To this point I have focused on connected apps almost exclusively. Though I have been keeping up on developments in client-side storage and expect it to be an important aspect for my work very soon. For instance in Appeio it would be great to use client side storage to store and archive posts for faster UI and fewer API calls.

**Q:***Any feedback on the developer experience on Firefox OS or the Android Web Runtime that you’d like to share with our Apps & Marketplace team?*

I am simply in love with what you are trying to do here. It means so much to the developers and to the users who benefit from access and curation of these apps.

As a small developer it’s important to me that there be a place like this. Make it fast, make it stable and the apps will give it life and make it fun.

**Q:***Have you checked out the Firefox OS Simulator? *

I have checked it out and test my apps in it on a regular basis. The glimpse it gives into the future of devices and the OS that they present the user is fascinating. I appreciate the tool and look to this project as the future of a better connected and open web everywhere.

## 6 comments

Eduard GotwigNovember 26th, 2012 at 14:31Robert NymanNovember 27th, 2012 at 01:08Eduard GotwigNovember 27th, 2012 at 04:49Havi HoffmanNovember 27th, 2012 at 08:23HaroldNovember 27th, 2012 at 17:21Daniel FitzpatrickJanuary 28th, 2013 at 02:07