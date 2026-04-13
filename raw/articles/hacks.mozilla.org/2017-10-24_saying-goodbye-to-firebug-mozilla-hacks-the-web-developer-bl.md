---
title: Saying Goodbye to Firebug – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/10/saying-goodbye-to-firebug/
author: Jan Honza Odvarko
published: '2017-10-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The most popular and powerful web development tool.

Firebug has been a phenomenal success. Over its 12-year lifespan, the open source tool developed a near cult following among web developers. When it came out in 2005, Firebug was the first tool to let programmers inspect, edit, and debug code right in the Firefox browser. It also let you monitor CSS, HTML, and JavaScript live in any web page, which was a huge step forward.

Firebug caught people’s attention — and more than a million loyal fans still use it today.

So it’s sad that Firebug is now reaching end-of-life in the Firefox browser, with the release of Firefox Quantum (version 57) next month. The good news is that all the capabilities of Firebug are now present in current Firefox Developer Tools.

The story of Firefox and Firebug is synonymous with the rise of the web. We fought the good fight and changed how developers inspect HTML and debug JS in the browser. Firebug ushered in the Web 2.0 era. Today, the work pioneered by the Firebug community over the last 12 years lives on in [Firefox Developer Tools](https://www.mozilla.org/en-US/firefox/developer/?utm_source=blog&utm_medium=hacks&utm_campaign=switch).

### Looking Forward, Looking Back

But before we move on, let’s take a few moments to remember all the great milestones of the Firebug project, and share some stories from early community members.

**Jan 2006, Firebug 0.2**Joe releases the single tab[console](https://youtu.be/JVCioNT-SYE)with AJAX logging.**May 2006, Firebug 0.4**There is a new top-level tab for JavaScript[debugging](https://youtu.be/LvdcAm1-4zU).**Dec 2006**Firebug is open-sourced.**Jan 2007, Firebug 1.0**The start of Web 2.0!**Aug 2008, Firebug 1.2**First FWG (Firebug Working Group) release.**Oct 2009, HTTP Archive (HAR)**[One archive](http://www.softwareishard.com/blog/har-12-spec/)for web performance and beyond.**Feb 2010**,**Firebug Lite**for Google Chrome[released](https://blog.getfirebug.com/page/22/)(bookmarklet).**Apr 2010,**Dynamic and Graphical Web Page Breakpoints invented ([pdf](https://getfirebug.com/doc/breakpoints/paper/breakpoints.pdf)).**2011**Boom of Firebug[extensions](https://getfirebug.com/wiki/index.php/Firebug_Extensions).**June 2014, Firebug 2.0**Fresh new UI compatible with Firefox Australis.**June 2016**,[Unifying](https://blog.getfirebug.com/2016/06/07/unifying-firebug-firefox-devtools/)Firebug & Firefox DevTools.**Oct 2017, Goodbye Firebug!**

*Firebug 0.2, Console panel*

I’d like to share some of my own fond Firebug memories and historic moments, beginning with how it all started.

The very first version released in Jan 2006 on [AMO](https://addons.mozilla.org/cs/firefox/addon/firebug/versions/?page=4#version-0.2) is Firebug 0.2 with a short comment from Joe Hewitt:


This is a very early release – the code is only a few days old. Beware of the leopard.

Later in December 2006, Joe makes the important decision to open source Firebug:


The first announcement is in regards to Firebug’s licensing. As I was developing Firebug 1.0, I began to wonder if I should try to turn the project from a hobby into a business. When I proposed this idea on my blog, the response was very positive and reaffirmed my belief that Firebug could do well as a commercial product.

However, in the end, I just don’t feel like that is the right thing to do. I love working on Firebug because I know I’m making a lot of people happy and helping to advance the state of the art. That’s a lot more meaningful to me than just about anything else, and so, I’ve decided thatFirebug will remain free and open source.

After releasing v1.0, Joe Hewitt moved on to his next adventure at Facebook and John J. Barton (IBM) soon became interested in resuscitating the project …


Oh Firebug! Fun times. I started out as a user and contributor (of obscure debugging-of-eval features). When Joe Hewitt decided to move on, I hunted around IBM to gauge interest in continuing his work. At that time, enterprise Web apps were just starting to grow without much more than ‘window.alert()’ debugging. Once Jan ‘Honza’ Odvarko joined the Firebug effort, IBM’s Rational IDE team agreed to support my work on Firebug and I created an Eclipse plugin to integrate Firebug with the product. Honza and I filled in Joe’s great framework, scaling the tool to larger and more complex applications. We added tests and improved the release vetting, then fixed bugs and responded to bug reports to build community. Soon we had other contributors and a growing collection of Firebug extensions. Mike Collins joined me to help on the product side and I collaborated with Salman Mirghasemi at EPFL on research projects leveraging Firebug technology.

I’m proud of our collective efforts to sustain Firebug during the critical growth phase of Web technology. This tool helped countless developers build sites used by millions of people worldwide. Now every browser has a debugger inspired by our work. While I miss the scrappy self-reliant teamwork of Firebug development, we leave knowing we made big positive impact.

*Firebug 1.2, Net panel*

The success of a project is always dependent on the dedication of developers, contributors, and involved users. But, there were also times when it wasn’t simple to keep up with the quickly evolving Firefox browser and we had to work hard.

A snippet from John J. Barton’s [post](https://blog.getfirebug.com/2010/03/17/firebug-reflections/) (March 2010):


We’ve come along way since Joe Hewitt unleashedFirebug 1.0. Arriving at the start of the Web 2.0 revolution, Firebug helped shift people from thinkingWeb 2.0was a fad to realizing Web apps can be real. Firebug had to grow up in a hurry while we still did not understand the code well and certainly didn’t understand Firefox.

Firebug 1.1wasn’t really meant to be, though it was used by a few dedicated and helpful folks. SoFirebug 1.2was our first real release beyond Joe’s original source. Behind the scenes we had lots of extra work to close a security hole in Firebug. At the time we could not tell anyone: too many users were exposed.

Firebug has been always very popular project and many developers started working on Firebug features, fixing bugs and building extensions. Yes, many new extensions to extend an extension. We were all using the same technology. Community happiness.

There is a [post](http://www.softwareishard.com/blog/firebug/list-of-firebug-extensions/) I made about Firebug extensions, July 2008:


Have you ever been interested in what extensions are available for Firebug? If yes, take a look at what I have found. Frankly, I was quite surprised how many Firebug extensions already exists out there.

There were about 10 Firebug extensions in 2008 and more than 60 in 2011. Not easy to evolve a code base that needs to support so many extensions, trust me!

I started working on Firebug in 2007 and I joined John J. Barton when he was working on v1.2. At that time, the Firebug Working Group started and we all focused on building Firebug as well as the community around it. These were exciting times. We were relatively small group and every single new feature we introduced was used by millions of people the next day. We’d been getting great amount of feedback and learning a lot about how to build visual tools for web developers.

The first Firebug piece I worked on was the Net panel. HTTP monitoring was always my [cup of tea](http://www.softwareishard.com/blog/firebug/introduction-to-firebug-net-panel/) and we soon noticed a lot of user requests to export data collected by the panel. Implementing such a feature wasn’t hard, the nice piece of work was introduction of a new format for exported data. A couple years later, around October 2009, we introduced the new HTTP Archive (HAR) format with Steve Souders (page-load-performance guru and author of YSlow, often considered the first Firebug extension) and Simon Perkins. This format was a great success and many tools support it now.

From Steve Souders [post](http://www.stevesouders.com/blog/2009/10/19/http-archive-specification-firebug-and-httpwatch/):


I suggested that, rather than create yet another proprietary format, Firebug team up with HttpWatch to develop a common format, and drive that forward as a proposal for an industry standard. I introduced Simon Perkins (HttpWatch) and Jan “Honza” Odvarko (main Net Panel developer), then stepped back as they worked together to produce today’s announcement.

I had good times working with John and others on the project. Because Firebug was well written and well-architected, it was a pleasure to build on top of it. Joe did a great job laying the foundation to support dozens and dozens of extensions built atop Firebug. John J.was an excellent manager and peer to work with. One of the concepts we invented and implemented in Firebug was related to a new kind of breakpoint. We called it Dynamic and Graphical Web Page Breakpoints. Yeah, you might know these features as Break on XHR, Break on Next, Break on DOM mutation, etc.

From Firebug [blog](https://blog.getfirebug.com/2009/11/03/dynamic-and-graphical-web-page-breakpoints/):


Jan “Honza” Odvarko and I have submitted “Dynamic and Graphical Web Page Breakpoints” on the 1.5 breakpoints toWWW 2010. It motivates the various breakpoints, describes the user experience and the implementation, then relates this breakpoint work to academic papers.

If you want the Cliff Notes version, we also have ademo page.

Firebug 2.0 was released in June 2014. It was a major rewrite of the UI in order to make it compatible with the new Firefox Australis theme. We delivered on time and we were proud of it, a true community achievement. Since that release, we’ve been in maintenance mode. The latest Firebug version on AMO is 2.0.19.

Officially, we started [unifying](https://blog.getfirebug.com/2016/06/07/unifying-firebug-firefox-devtools/) Firebug with built-in Firefox tools around 2016, but in fact the process began earlier. Mozilla’s strategy was to introduce new built-in developer tools offered as a default in Firefox. Modern developer tools written from scratch. The decision was made not to use Firebug as the platform to build upon. Some Firebug users and contributors were disappointed by this decision, but Mozilla’s infrastructure and requirements were different at that time. Sometimes it’s just better to start from scratch, which is especially true for software development.

Most importantly, today’s Firefox DevTools are in great shape and faster than ever, based on web technologies like React/Redux/Webpack, cool things. The architecture is ready to support extensions. The team is great, with experienced tool developers. [This is my team](https://twitter.com/FirefoxDevTools). :-)


The process of unifying Firebug with the rebuilt devtools was completed with the release of Firebug 3 (aka [Firebug.next](https://github.com/firebug/firebug.next)) in 2015. This prototype was built as an extension to built-in Firefox devtools and eventually integrated directly into devtools. You can learn about how to [migrate from Firebug](https://developer.mozilla.org/en-US/docs/Tools/Migrating_from_Firebug). You can try Firefox Developer Tools by [updating your release browser](https://www.mozilla.org/en-US/firefox/new/?utm_source=blog&utm_medium=hacks&utm_campaign=switch) or downloading [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/?utm_source=blog&utm_medium=hacks&utm_campaign=switch).


**Support for every old-school* extensions stops in Firefox Quantum (aka 57)**. Yes,** including Firebug** and that’s why there was great opportunity to write this post.

The king is dead, long live the king!


Jan ‘Honza’ Odvarko


- XUL & Add-on SDK based

![](../../assets/a700528fc65a9831.png)


**List of contributors**: Joe Hewitt, John J. Barton (IBM Almaden), Jan Odvarko (Mozilla Corp.), Max Stepanov (Aptana Inc.), Rob Campbell (Mozilla Corp.), Hans Hillen (Paciello Group, Mozilla), Curtis Bartley (Mozilla Corp.), Mike Collins (IBM Almaden), Kevin Decker, Mike Ratcliffe (Mozilla Corp.), Hernan Rodriguez Colmeiro, Austin Andrews, Christoph Dorn, Steven Roussey (Illuminations for Developers), Sebastian Zartner, Harutyun Amirjanyan, Simon Lindholm, Stampolidis Anastasios, Joe Walker (Mozilla Corp.), Vladimir Zhuravlev, Farshid Beheshti, Leon Sorokin, Florent Fayolle, Hector Zhao, Bharath Thiruveedula, Nathan Mische, Belakhdar Abdeldjalil, Jakob Kaltenbrunner, …

**List of translators**: Leszek(teo)Zyczkowski (pl-PL), markh (nl), peter3 (sv-SE), AlleyKat (da-DK), Hector Zhao, lovelywcm (zh-CN), Lukas Kucharczyk, Michal Kec (cs-CZ), Team erweiterungen.de, ReinekeFux, Benedikt Langens, Sebastian Zartner (de-DE), l0stintranslation, gonzalopirobutirro, Luigi Grilli (it-IT), alexxed (ro-RO), Nicolas Martin, Franck Marcia (fr-FR), gLes (hu-HU), Xavi Ivars – Softcatala (ca), gezmen (tr-TR), eternoendless (es-AR), Dark Preacher (ru), Tiago Oliveira, Diego de Carvalho Zimmermann, Alexandre Rapaki (pt-BR), Juan Botias, Alvaro G. Vicario (es-ES), Andriy Zhouck (uk-UA), Hisateru Tanaka, k2jp (ja-JP), Mohsen Shadroo (fa-IR), Eduard Babayan (hy-AM), Helder Magalhaes (pt-PT), Tomaz Macus (sl-SI), Stoyan Stefanov, Alexander Shopov (bg), Kristjan Bjarni Guomundsson (is-IS), NGUYEN Manh Hung (vi-VN), Bwah (hr-HR), Sonickydon (el), David Gonzales (es), DakSrbija (sr), bootleq (zh-TW), Asier Iturralde Sarasola, Julen Irazoki Oteiza (eu), …

## About
[
Jan Honza Odvarko ](http://www.softwareishard.com/)

Honza is working on Firefox Developer Tools

## 82 comments

Jens GrochtdreisOctober 24th, 2017 at 08:32LeendertOctober 27th, 2017 at 02:48Fawad HassanOctober 24th, 2017 at 09:09Harald KirschnerOctober 26th, 2017 at 09:28Alvaro G. VicarioOctober 24th, 2017 at 09:40nemoOctober 24th, 2017 at 09:53Harald KirschnerOctober 26th, 2017 at 09:31Patrick FlowenOctober 24th, 2017 at 09:54Harald KirschnerOctober 26th, 2017 at 09:34SalarOctober 24th, 2017 at 10:05gabrielOctober 24th, 2017 at 10:11Kevin DangoorOctober 24th, 2017 at 10:18Colby RussellOctober 24th, 2017 at 13:11Brian GloverOctober 24th, 2017 at 17:31DmitryOctober 24th, 2017 at 17:57Guan JyunOctober 24th, 2017 at 18:19CarterOctober 24th, 2017 at 19:41Ernesto ButtoOctober 24th, 2017 at 21:18Suraiya AyshaOctober 24th, 2017 at 22:25KhizarOctober 24th, 2017 at 23:50khizarOctober 25th, 2017 at 00:00Sebastian ZartnerOctober 25th, 2017 at 01:47Alexandre LeducOctober 26th, 2017 at 13:58Priyadarshan DhaigudeOctober 25th, 2017 at 03:31Nemanja ĆosovićOctober 25th, 2017 at 04:21MonarchOctober 25th, 2017 at 04:23OanaOctober 25th, 2017 at 05:03MarcoOctober 25th, 2017 at 05:27Steve SoudersOctober 25th, 2017 at 08:03JianOctober 25th, 2017 at 08:51Emmanuel EspitiaOctober 25th, 2017 at 10:14Zach ChandlerOctober 25th, 2017 at 15:05YongWoo JeonOctober 25th, 2017 at 21:46Jon HumphreyOctober 26th, 2017 at 03:33AfterbanksOctober 26th, 2017 at 03:37Emil PetkovOctober 26th, 2017 at 11:28UmarOctober 26th, 2017 at 05:21CGOctober 26th, 2017 at 07:11Eliazer BraunOctober 26th, 2017 at 07:52Steve HornOctober 26th, 2017 at 09:29SarojOctober 26th, 2017 at 09:31AliOctober 26th, 2017 at 09:33ahsanOctober 26th, 2017 at 09:38MarioOctober 26th, 2017 at 09:39zian974October 26th, 2017 at 10:29MeganOctober 26th, 2017 at 11:06SayedOctober 26th, 2017 at 12:17Mohit lodhaOctober 26th, 2017 at 13:18Joel MarchesoniOctober 26th, 2017 at 13:41JefferyOctober 26th, 2017 at 13:53KlwoodOctober 26th, 2017 at 15:40Edward DollosoOctober 26th, 2017 at 16:24DavidOctober 26th, 2017 at 19:02Kesavan MuthuvelOctober 26th, 2017 at 20:38Ian VOctober 26th, 2017 at 22:35chrqlsOctober 27th, 2017 at 01:52Asanka DewageOctober 27th, 2017 at 06:04rctiqqOctober 27th, 2017 at 06:26PhilOctober 27th, 2017 at 07:24PeterOctober 27th, 2017 at 08:56Kevin McNeelyOctober 27th, 2017 at 14:04conngongvang.comOctober 27th, 2017 at 18:28Fernando BoaglioOctober 27th, 2017 at 18:38Camilo MartinOctober 27th, 2017 at 19:38MichaelOctober 28th, 2017 at 06:59DanOctober 28th, 2017 at 23:04JawadOctober 29th, 2017 at 10:07AslamOctober 29th, 2017 at 22:49Crystal Joy DuOctober 30th, 2017 at 02:01TanveerOctober 30th, 2017 at 02:49Kemal OkraliOctober 30th, 2017 at 06:58AlexOctober 30th, 2017 at 12:47meepoOctober 30th, 2017 at 20:24B KOctober 30th, 2017 at 21:28Mallesh TiruguduOctober 30th, 2017 at 21:44IndyOctober 30th, 2017 at 22:42ChetanOctober 30th, 2017 at 22:47DanielOctober 31st, 2017 at 09:57Gopal ChaladiOctober 31st, 2017 at 14:28Dave LeeNovember 3rd, 2017 at 01:28AlexNovember 3rd, 2017 at 17:17Edwin ShangNovember 5th, 2017 at 18:26