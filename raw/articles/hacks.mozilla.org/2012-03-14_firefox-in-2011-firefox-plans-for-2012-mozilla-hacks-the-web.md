---
title: Firefox in 2011 – Firefox plans for 2012 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2012/03/firefox-in-2011-firefox-plans-for-2012/
author: Robert Nyman
published: '2012-03-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A lot of people are interested in Firefox, the progress that is being made and what we plan to do. Therefore, I’d like to outline the things we accomplished with Firefox in 2011, and what we have already done, and plan to do, in 2012.


## Firefox in 2011

The major things we did with Firefox in 2011 were:

- Rapid releases
- We moved into new releases every 6 weeks of Firefox, to ensure both new features and fixes got out there faster to end users, instead of having to wait up to one year before – enabling a better web for end users and web developers alike. A concern was raised was about enterprises and releases, and therefore we established the
[Extended Support Release for Organizations](http://www.mozilla.org/en-US/firefox/organizations/). There were also questions about add-on compatibility and update approach, that is covered below for 2012. - Performance work
- During 2011, we saw the latest Firefox release that year being up to 7 times faster than Firefox 3.6!
- Memory usage
- A lot of work went into this area, and there were improvements resulting in up to 50% less memory usage.
- Firefox release channels
- To give web developers more options to test new features, we introduced the
[Firefox Aurora channel](http://www.mozilla.org/firefox/aurora/). Together with[Firefox Beta](http://www.mozilla.org/firefox/beta/)and[Firefox Nightly](http://nightly.mozilla.org/), that means a lot of ways to try new things. - Firefox for Android
- We released
[Firefox for Android](https://market.android.com/details?id=org.mozilla.firefox&hl=en)and have some exciting features lined up, available for testing in the[Firefox Aurora](http://www.mozilla.org/firefox/aurora/)and[Firefox Nightly](http://nightly.mozilla.org/)channels. - Privacy
- Firefox introduced
[Do Not Track](https://developer.mozilla.org/en/The_Do_Not_Track_Field_Guide)to the industry, something that was quickly followed by others. In 2011, the adoption for Firefox was 17.6% on mobile and 6% on desktop. - Improvements and features
- In 2011, we made 10 881 enhancements/changes to Firefox, together with 83 new features and 135 new APIs.
- Add-ons
- A staggering 480 000 000 add-ons were installed!

### Firefox and version numbers

With rapid releases and new version numbers, we have had questions about what they mean and communicate.

Version numbers will play a lesser and lesser role for users, but they will still matter to web developers, IT administrators and similar. The reason for having major version number bumps (e.g. version 6 to 7, 7 to 8, etc) is that new versions have had cases of non-backward compatible APIs, and the version number have been there to signal that it is not a minor release or maintenance update.

From a branding perspective, it will likely more go into being just Firefox, and that versioning will be more transparent.

## Firefox in 2012

To continue to build on our progress and momentum for 2011 we evaluated what the next steps would be, and have already started implementing a number of them. Outlined below are some of the most important ones.

- Add-on compatibility
- To address the issue of people updating Firefox but having their desired add-ons stop working, from Firefox 10
[add-ons were made Compatible by Default](http://blog.mozilla.com/addons/2012/01/27/compatibility-for-firefox-11/). This means that all add-ons that were marked compatible for Firefox 4 and higher will automatically be enabled in Firefox 10 and later. - Add-on sync
[Firefox Sync](http://www.mozilla.org/en-US/mobile/sync/)are being used by a lot of people, and in 2011 there were 25 billion items synced. To complement that, from Firefox 11 you can now also sync add-ons.- Silent updates
- To cater to update fatigue, updates will now be downloaded and installed silently in the background. It means that startup and shutdown of the web browser won’t be affected by installation routines. Additionally, the What’s New page displayed after an update can now be displayed depending if there is important information needed to be displayed to the end user. Silent updates are currently planned to land in Firefox 12, and some supporting enhancements including background updates will land after Firefox 12 (the silent update mechanism is broken down into several parts, described in detail in the
[Silent Update planning](https://wiki.mozilla.org/Silent_Update)). - Developer Tools
- Our Developer Tools in Firefox continue to evolve, with a number of features outlined in the
[Developer Tools roadmap](https://wiki.mozilla.org/DevTools/RoadmapDec2011).

All Firefox plans are available in the [Firefox roadmap](https://wiki.mozilla.org/Firefox/Roadmap).

### Web platform updates

When it comes to the web platform, we have a number of exciting new features in store:

- WebRTC
- Support for real time audio, video and data communication between two web browsers. The implications of this are huge and it will enable a lot of interesting real-time communication solutions, richer web games and overall take the web to the next level!
- Completing Web Sockets
- Make Web Sockets match the W3C protocol and API parts. Web Sockets are an interesting solution to offer bi-directional and full-duplex communications over TCP, and it enables pushing things from web servers without the need for a web page to constantly poll it and ask. Low-latency.
- SPDY
- Allows for multiplexing and connection sharing, described more in detail in
[SPDY Brings Responsive and Scalable Transport to Firefox 11](http://hacks.mozilla.org/2012/02/spdy-brings-responsive-and-scalable-transport-to-firefox-11/). It’s SSL only, and will offer faster page loads and better scalability for SPDY-enabled web servers. The goal is for end users to have a much faster web experience with all kinds of content, from more regular web sites to high-performing ones in the form of games and media. - HTTP Pipelining
- Offers a significant performance gain, in particular in regards to high latency connections. Will also help in those cases where SPDY is not enabled/an option and build on existing infrastructure.
- HTTP Pre-connections
- Opening HTTP connections before page loads to improve performance, and is based on the assumption that users will go back to the same sites. A complement to SPDY and HTTP Pipelining in offering a faster user experience on the web.
- DASH WebM
- Brings adaptive streaming of WebM video with DASH, and is outlined in
[Matroska/WebM in MPEG DASH](http://sourceforge.net/apps/trac/matroska/wiki/DASH_Profile). Offering proper streaming of video on the web could vastly improve user experience, and allows Firefox to adapt to changing network conditions and resolution changes (for instance, to/from fullscreen viewing). - Web Apps improvements
- A huge number of features to make
[Web Apps](https://developer.mozilla.org/en-US/apps)more integrated into Firefox, to offer users a seamless integration and to complement the[Mozilla Marketplace](https://marketplace.mozilla.org/). All improvements are listed in the roadmap for[Apps in Firefox](https://wiki.mozilla.org/Platform/Roadmap#Apps). - Uploading directories and accessing to Local Media Storage
- Gives access to entire directories through File API or to upload them, with their subtrees intact, and additionally gives access to upload, sync or other actions with Local Media. This is intended to give a richer integration with devices out there and make the web platform and experience richer for users.
- CSS Flexbox and CSS Grid
- Implementing support for the latest versions of
[CSS Flexbox](http://www.w3.org/TR/css3-flexbox/)and[CSS Grid](http://www.w3.org/TR/css3-grid/), where the idea is to offer a number of improved ways of doing layout on the web. - Capturing keys in
[fullscreen mode](https://developer.mozilla.org/en/DOM/Using_full-screen_mode)and[Mouse Lock API](https://developer.mozilla.org/en/API/Mouse_Lock_API) - With fullscreen support in web browsers, the next step is improve the gaming and interaction experience for building more advanced web sites with key input in fullscreen mode and also being able to use the mouse as a controller instead of as a pointer.

More details on the web platform is available in the [Web Platform roadmap](https://wiki.mozilla.org/Platform/Roadmap).

## Moving forward!

As you can see, we have, and continue, to work hard on Firefox and the web platform to offers users the best experiences and number of options we can!

Need help with something? Please check out the extensive [Need Help With Firefox?](http://support.mozilla.org/)

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 140 comments

TomMarch 14th, 2012 at 03:12Robert NymanMarch 14th, 2012 at 03:29Stephen HorlanderMarch 14th, 2012 at 06:56Robert NymanMarch 14th, 2012 at 07:04Deo DomuiqueMarch 14th, 2012 at 12:16Robert NymanMarch 14th, 2012 at 12:18Andi SmithMarch 14th, 2012 at 03:16Robert NymanMarch 14th, 2012 at 03:30EdMarch 14th, 2012 at 03:26Robert NymanMarch 14th, 2012 at 03:57Paul RougetMarch 14th, 2012 at 03:41Robert NymanMarch 14th, 2012 at 03:57Karan SinghMarch 14th, 2012 at 03:58Robert NymanMarch 14th, 2012 at 03:59Axel RauschmayerMarch 14th, 2012 at 04:03Robert NymanMarch 14th, 2012 at 04:15Axel RauschmayerMarch 14th, 2012 at 04:46Robert NymanMarch 14th, 2012 at 04:49ZéflingMarch 14th, 2012 at 04:30Axel RauschmayerMarch 14th, 2012 at 04:33ZéflingMarch 14th, 2012 at 05:08Axel RauschmayerMarch 14th, 2012 at 04:30Robert NymanMarch 14th, 2012 at 04:45Robson SobralMarch 14th, 2012 at 04:46Robert NymanMarch 14th, 2012 at 04:56Robson SobralMarch 14th, 2012 at 07:51Robert NymanMarch 14th, 2012 at 08:44Robson SobralMarch 14th, 2012 at 09:07Robert NymanMarch 14th, 2012 at 10:08Axel RauschmayerMarch 14th, 2012 at 09:12mirajMarch 14th, 2012 at 08:27Robert NymanMarch 14th, 2012 at 08:30OliverMarch 15th, 2012 at 02:07Robert NymanMarch 15th, 2012 at 02:36OliverMarch 16th, 2012 at 02:09OliverMarch 16th, 2012 at 02:17Robert NymanMarch 16th, 2012 at 06:14MaurizioMarch 14th, 2012 at 09:41Robert NymanMarch 14th, 2012 at 10:10JasonMarch 14th, 2012 at 09:55Robert NymanMarch 14th, 2012 at 10:17the_deesMarch 14th, 2012 at 10:28the_deesMarch 14th, 2012 at 11:19Robert NymanMarch 14th, 2012 at 11:33jiveMarch 14th, 2012 at 10:44Robert NymanMarch 14th, 2012 at 11:34GalaxyMarch 14th, 2012 at 11:31Robert NymanMarch 14th, 2012 at 11:34JoeMarch 14th, 2012 at 13:03Robert NymanMarch 15th, 2012 at 02:26qwertyZAMarch 14th, 2012 at 16:18Jean-Yves PerrierMarch 15th, 2012 at 00:15Andrew HimeMarch 15th, 2012 at 20:59ErunnoMarch 16th, 2012 at 04:20Andrew HimeMarch 16th, 2012 at 10:49Robert NymanMarch 16th, 2012 at 06:32Andrew HimeMarch 16th, 2012 at 10:52Robert NymanMarch 19th, 2012 at 02:00MicahMarch 14th, 2012 at 17:00Jean-Yves PerrierMarch 15th, 2012 at 00:19MicahMarch 15th, 2012 at 00:29MicahMarch 15th, 2012 at 00:30Robert NymanMarch 15th, 2012 at 02:29MicahMarch 15th, 2012 at 02:39Robert NymanMarch 15th, 2012 at 03:02JackMarch 14th, 2012 at 20:16Jean-Yves PerrierMarch 15th, 2012 at 00:21yabbinMarch 14th, 2012 at 21:05Jean-Yves PerrierMarch 15th, 2012 at 00:22Robert NymanMarch 15th, 2012 at 02:31Yousif AnwarMarch 14th, 2012 at 23:46Robert NymanMarch 15th, 2012 at 02:33RobsMarch 15th, 2012 at 00:47Robert NymanMarch 15th, 2012 at 02:47RobsMarch 15th, 2012 at 03:01Robert NymanMarch 15th, 2012 at 03:10AntonioMarch 15th, 2012 at 02:05Robert NymanMarch 15th, 2012 at 02:52JoeMarch 15th, 2012 at 03:04JoeMarch 15th, 2012 at 03:06Robert NymanMarch 15th, 2012 at 03:07JeffMarch 15th, 2012 at 06:16Robert NymanMarch 15th, 2012 at 06:50davidMarch 15th, 2012 at 06:31Robert NymanMarch 15th, 2012 at 06:54Dava GordonMarch 15th, 2012 at 10:04Robert NymanMarch 15th, 2012 at 13:27GeorgeMarch 15th, 2012 at 14:50Jean-Yves PerrierMarch 15th, 2012 at 23:03Matthew GambleMarch 15th, 2012 at 14:55Jean-Yves PerrierMarch 15th, 2012 at 23:04hakimMarch 15th, 2012 at 15:11Robert NymanMarch 16th, 2012 at 06:27Lo nuevo de hoyMarch 15th, 2012 at 15:18Robert NymanMarch 16th, 2012 at 06:30AlMarch 15th, 2012 at 16:05Jean-Yves PerrierMarch 15th, 2012 at 23:05AlMarch 16th, 2012 at 07:59Robert NymanMarch 16th, 2012 at 08:51AlMarch 16th, 2012 at 10:21Robert NymanMarch 19th, 2012 at 01:59NexsoMarch 15th, 2012 at 17:21Jean-Yves PerrierMarch 15th, 2012 at 23:10bull500March 15th, 2012 at 19:13Jean-Yves PerrierMarch 15th, 2012 at 23:30JayMarch 15th, 2012 at 21:17Robert NymanMarch 16th, 2012 at 06:25Hieu Le TrungMarch 16th, 2012 at 09:44Jean-Yves PerrierMarch 17th, 2012 at 14:48kickass69March 16th, 2012 at 10:55Jean-Yves PerrierMarch 17th, 2012 at 14:45CarloMarch 19th, 2012 at 13:59Robert NymanMarch 20th, 2012 at 01:47MukeshMarch 21st, 2012 at 00:35georgeMarch 22nd, 2012 at 02:40Robert NymanMarch 22nd, 2012 at 06:57Andy LynMarch 22nd, 2012 at 09:05Robert NymanMarch 22nd, 2012 at 09:51DannyMarch 22nd, 2012 at 21:37Robert NymanMarch 23rd, 2012 at 04:31JoeMarch 23rd, 2012 at 04:50Robert NymanMarch 23rd, 2012 at 12:04DannyMarch 23rd, 2012 at 15:00Robert NymanMarch 23rd, 2012 at 17:21DannyMarch 23rd, 2012 at 18:52Robert NymanMarch 23rd, 2012 at 19:06SunyMarch 25th, 2012 at 20:14Robert NymanMarch 29th, 2012 at 11:26NigelleMarch 28th, 2012 at 07:41Robert NymanMarch 29th, 2012 at 11:29NigelleMarch 28th, 2012 at 08:06Robert NymanMarch 29th, 2012 at 11:32NigelleApril 21st, 2012 at 05:56Robert NymanApril 21st, 2012 at 09:48NigelleMay 15th, 2012 at 03:27Robert NymanMay 16th, 2012 at 05:40Very SadApril 18th, 2012 at 19:46Robert NymanApril 19th, 2012 at 01:36Julio Jimenez-AgüeroMay 13th, 2012 at 23:33Jean-Yves PerrierMay 14th, 2012 at 15:25