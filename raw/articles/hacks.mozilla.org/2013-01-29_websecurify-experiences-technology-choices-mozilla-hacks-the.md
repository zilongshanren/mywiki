---
title: Websecurify – Experiences & Technology Choices – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/01/websecurify-experiences-technology-choices/
author: Petko D Petkov
published: '2013-01-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When I launched [@websecurify](http://www.websecurify.com/) years ago I wrote a lot of JavaScript, native code and XUL but today the technology combo that I use in Websecurify is made of a custom language compiled to JavaScript that sits on top of the modern HTML5 stack that runs inside your normal browser. Sounds crazy but it somehow feels the right thing to do.

![Websecurify default application launcher.](../../assets/2ecfc7f987db72d9.png)


Coming to the realisation that HTML5 was ready for Websecurify’s goals wasn’t an easy step. We were entering unexplored land full of dangers and tradeoffs. No one was attempting to do what we wanted to do and it was sort of scary place to be. Websecurify did not start out of nothing. It was primarily a desktop application and over the years we built a solid framework, wrote thousands of lines of code and spent enormous amount of hours fixing and tracking bugs in our own algorithms and the JavaScript interpreters of the time.

There was also this question in the air whether it was actually possible to write a full-blown security testing framework with just browser technologies – something that browsers were really never meant to do for a range of reasons. We did succeed at the end and here are some of the things that made us take HTML5 on board and the things that we’ve learned during the process.

## JavaScript And Its Role

We need to start the story with JavaScript – the language that moves the Web. It is funny how predominant this language has become over the years. It feels like it was yesterday when JavaScript was used just to create fancy rollover buttons and popups. We chose JavaScript for our vulnerability testing platform not because we knew that it was a great language but because it was native to Mozilla’s [Xulrunner](https://developer.mozilla.org/en/docs/XULRunner), which looked like a solid cross-platform desktop application framework at the time.

Over the years we’ve learned a few nasty truths about JavaScript as a general purpose programming language. To start with, JavaScript is a scripting language – meaning it is good for writing scripts. If the aim is to glue things together than use JavaScript. For serious applications, expanding to thousands of lines of code, you will need a proper programming language with static compilation, type system and all that jazz. One of the obstacle we had with JavaScript was around garbage collection. As you program in JavaScript you tend to think with closures in mind. Almost everything is inlined as a function. Due to this style of programming, during the first months of our scanning technology we were constantly running into js interpreter quirks, which were difficult to debug. It was either the interpreter or our own code not keeping enough references around and causing all kinds of unexpected bugs.

Sometimes it was not the garbage collection effect but the opposite – memory leaks. All of the sudden we were allocating far too much memory than we wanted to use. The dynamic nature of the language was also an obstacle as it was never possible to tell if the state of all objects was correct at any given point in time. The immediate solution to this problem was to write unit tests, which we happily started doing but solved the problem only to an extend. Even after thousands of lines of unit tests JavaScript felt short to our expectations.

## A Custom Language

During one of the miserable periods of dealing with unexpected bugs we decided to replace JavaScript with a custom language that provided enough robustness for our needs and programming ideals. It was an experiment and it was done out of desperation. I believe we were one of the first to start thinking of JavaScript more or less like an assembler than an actual general purpose programming language. We spent 3 months developing the first prototype and the results were remarkable. The first incarnation of our JavaScript compiler was essentially a glorified grep. Things started looking good because at the time we had for the first time a proper web application security framework that runs in its entirety on standard JavaScript interpreters. Our web security scanning technology matured and we rolled out several versions of our desktop product plus a security testing tool for iOS built with a custom compiler for Objective-C.

If it wasn’t for the lack of support for Xulrunner and [XUL](https://developer.mozilla.org/en/docs/XUL), we would have never looked at HTML5 as a replacement. That is right. XUL is amazing framework but it is Mozilla-centric (almost like Java, Flash, Silverlight, ActiveX and other) and lacks any support because it was never meant to be used outside of Firefox. XUL was built all around the design principles behind separation of concerns. Internationalization files, styles, structure and code were all kept separately and overlays provided the most powerful way to extend things as you wish. I still believe that XUL and [XPCOM](https://developer.mozilla.org/en/docs/XPCOM) is an awesome combination and perhaps the most powerful desktop programming framework ever made but it was never meant to be.

The Mozilla community was betting hugely on HTML5 as the next generation of programming platform and after having a look at some ongoing projects such as B2G (now [Firefox OS](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS)), the Chromeless browser experiment, [Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox) (completely native) we started to realise that XUL might be soon deprecated and we had to think for the future. We decided to go with HTML5 which was a serious gamble. In fact, it was down crazy.

## Going With HTML5

HTML5 happened to be a bit difficult initially. It does lacks any native look and feel but after going over this thought for a while, we realised that this is actually an advantage rather than a disadvantage. HTML5 lacks internationalisation support. It lacks the theming and overlaying features of XUL and initially it felt as being quite immature and dull. It lacks XBL. It is certainly not a XML language. When you are programming in HTML5 the only way is to build everything yourself and compose your application from the ground up in whichever way you desire.

It was difficult to envision how that will translate to our needs but we did it. The UI was built from scratch and all the application elements were encapsulated into a small framework. Can we extend the UI in the same way we used to do with XUL? Definitely not! However, it was simpler and less confusing. HTML5 rendering turned out to be quite fast and very robust for both Firefox and Chrome and for once we saw potential.

We had all the bits that we started with we developed our desktop software but the next big problem to tackle was really about how to deliver a web application security scanner as a modern web app. That was the difficult question. It was difficult because in order for the scanner to work you have to break out of the security model that the browser employes and that is not something browsers allow you to do. We were not lost because we already knew that worse come-to-worse, we will simply embed a browser rendering engine and write the rest of the code natively but we hoped to make our next generation product a first class citizen in both Firefox and Chrome.

## Adding Our Own API

For sure, we couldn’t do it with the standard API provided by browsers so we decided to do what the B2G folks did with Firefox OS and add our own API that enables our applications to do what we wanted them to do while still remaining web apps by definition. These augmentations, as we like to call them, were delivered as extensions which provided a thin layer between the browser and Websecurify, our own code delivered as a web app. The mechanics behind the extensions are difficult to describe so I will skip this part. However, it is enough to say that our extensions turned out to be maintainable and provide the functionalities that we required from browsers to support in order for our in-browser web application security suite to work in the same way you would expect it to work as a desktop app.

![Websecurify operating as a proxy using the Firefox extension.](../../assets/ab0d33d8215d4a53.png)


Websecurify Httpview with full access to browser HTTP trafic provided by the Websecurify Firefox Extension.


The HTML5 app plus a browser extension turned out to be a good combo. The HTML5 app takes care of the delivery mechanism, which as you know, it is over the Web. It also simplified the updates because we no longer had to wait for months before we roll them out because we could do them on daily basis as we go (something that we still do today). The HTML5 app that we wrote also meant that we were future-proof and here to stay as a technology company being able to adopt, pioneer and innovate in previously unexplored field. On the other hand the browser extensions that we delivered provided this much needed support to go beyond what modern browsers are capable of without compromising the user experience or security. The result is tremendous.

## Conclusion

Until this point you must be thinking why I am writing all these things. What is this guy’s agenda? When we started writing our XUL-based app we always wanted to contribute our framework back to Mozilla while keeping our scanning technology to ourselves. We felt it was a good compromise. Now when we no longer develop for Xulrunner due to all the reasons explained above, the only thing we can share is our experience and I believe there is a lot to learn from it. We are still trying to figure out the best way to make the old XUL framework public.

The main point I want to make is that although both JavaScript and HTML5 have their own hurdles we find them mature enough to write first-class web applications that go beyond data-entry. It is a proof that web apps are mature enough for all kinds of applications including blockbuster games, complex software which is usually only available for various native platforms and others. I am quite excited to see what the future holds and I bet it will be exhilarating.

## About
[
Petko D. Petkov ](http://www.gnucitizen.org)

Petko D. Petkov (a.k.a pdp) is founder and leading member of the GNUCITIZEN Information Security Think Tank. He is a recognized information security researcher, security tools developer, penetration tester, frequent speaker at security industry recognized events, and published author who has contributed to several best-selling books, numerous popular blogs and online magazines.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 4 comments

Michael TurnwallJanuary 31st, 2013 at 00:35Michael TurnwallJanuary 31st, 2013 at 00:38Petko D. PetkovJanuary 31st, 2013 at 02:56Michael TurnwallJanuary 31st, 2013 at 11:27