---
title: Firefox OS 2.5 Developer Preview, an experimental Android app – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2015/11/firefox-os-2-5-developer-preview-an-experimental-android-app/
author: Peter Dolanjski
published: '2015-11-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today we have made Firefox OS 2.5 available worldwide. We are also making an early, experimental build of the OS — Firefox OS 2.5 Developer Preview — available for developers to download on Android devices. This latest version of Firefox OS delivers exciting features including:

**Add-ons:**Just like the add-ons we’ve come to love in desktop browsers,[Firefox OS add-ons](https://developer.mozilla.org/en-US/Firefox_OS/Add-ons)can extend just one app, several, or all of them, including the system app itself.**Private Browsing with Tracking Protection:**A new Firefox privacy feature, Tracking Protection allows users to control how their browsing activity is tracked across many sites.**Pin the Web:**[Pin the Web](https://wiki.mozilla.org/Pin_the_Web)removes the artificial distinction between web apps and web sites and lets you pin any web site or web page to your home screen for later usage.

To find out more about all aspects of the release, visit [Firefox OS v2.5](https://www.mozilla.org/firefox/os/2.5/).

Firefox OS 2.5 Developer Preview is an app that lets you experience Firefox OS as an alternate home screen on your Android device without having to re-flash and replace your Android installation. To give it a try, visit the [Firefox OS 2.5 Developer Preview](https://www.mozilla.org/firefox/os/2.5/), right from your Android device, then click to “Get the Android App.”

![Firefox OS 2.5 developer preview homescreen](../../assets/ad69c8d23d072e2a.png)

**Android apps alongside Web apps on the homescreen**

![Firefox OS 2.5 developer preview Calendar](../../assets/05bcfe1cd5e52d14.png)

**Firefox OS Calendar with Android navigation bar**

![Firefox OS 2.5 developer preview top sites view](../../assets/0bce2240c6f735f3.png)

**Firefox OS Browser landing page**

**What is the Firefox OS 2.5 Developer Preview?**

You’ve asked how to get involved with the Firefox OS open source project. To date, it’s only been possible to download and explore the latest versions of Firefox OS on specific hardware, such as the Flame device. We’re now working on making Firefox OS more widely available. The [Firefox OS Participation Hub](https://firefoxos.mozilla.community) provides up-to-date information on getting involved with Firefox OS . The [B2G-installer add-on](https://github.com/mozilla-b2g/b2g-installer) lets you flash a full port of Firefox OS on to an Android device (Note: Firefox OS is under development. Don’t expect it to be bug-free or completely stable.)

Re-flashing existing hardware means losing user data as well as access to Android apps that you may depend on. There’s always an inherent risk of rendering your hardware inoperable, i.e., *bricking* your device. Firefox OS 2.5 Developer Preview avoids these issues by replacing the Android home screen with the [Gaia (UI) layer](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS/Platform/Gaia/Introduction_to_Gaia) of Firefox OS. Effectively you can use Firefox OS while still having full access to your Android apps. Firefox OS 2.5 Developer Preview makes Firefox OS available to more developers, testers, localizers, and supporters of the Open Web around the world.

If you’re curious to see what Firefox OS is all about, or just interested in testing out new features, the Firefox OS 2.5 Developer Preview app makes it very simple to get started with very little risk involved. By downloading the app, you can experience Firefox OS and explore many of its capabilities, without flashing hardware. If you decide you’re done trying it out, the app can be removed as simply as any other app. If you’re interested in becoming a code contributor or bug reporter, the app makes it dramatically easier to get involved.

**What’s the catch?**

As a full operating system, Firefox OS has its own task manager, utility tray, navigation buttons, settings, and more. Running on top of Android means that these elements of the operating system may come into conflict with those same system functions on Android. Android launchers were never designed to enable replacement of these operating system functions. As a result we employ various workarounds, where possible, to avoid delivering a poor user experience. For example, Android uses a back button as a primary navigation method. Firefox OS does not. While we are trying to mitigate these issues, the current edition of the Firefox OS 2.5 Developer Preview app should be considered experimental and will most likely contain bugs. We can certainly use your help in discovering, reporting, and fixing issues.

**Hacking on the Firefox OS 2.5 Developer Preview**

We’d love for you to play with the Firefox OS 2.5 Developer Preview — to scratch your own itch, test an idea, or contribute to the project by improving performance or finding interesting solutions to the conflict problems with Android system functions mentioned above. With that said, if you are interested in hacking on the app, instructions for building it from scratch can be found [here](https://wiki.mozilla.org/B2gdroid). Alternatively, you can make use of [WebIDE](https://developer.mozilla.org/en-US/docs/Tools/WebIDE) in the [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) browser to start making changes directly to the layout and composition of apps in Firefox OS Developer Preview.

**Get involved without coding**

There are many ways to get involved without contributing code. The easiest way is to install Firefox OS 2.5 Developer Preview on your Android device and [file bugs](https://bugzilla.mozilla.org/enter_bug.cgi?product=B2GDroid) when you run into problems or discover things that don’t work as expected. If you’re looking for other ways to help, visit our [Firefox OS Participation Hub](https://firefoxos.mozilla.community).

**Supported devices**

The current build will only work on [ARM-based](https://en.wikipedia.org/wiki/ARM_architecture) devices. It will not work on x86 devices.

**Final thoughts**

We are very excited about the Firefox OS 2.5 Developer Preview app. We’ve worked hard to produce a Firefox OS experience for Android users. As with all things at Mozilla, this effort is very much a community effort and we welcome all forms of constructive feedback and suggestions for making the experience better.

Got questions about running Firefox OS on new hardware or devices? Try the [dev-fxos mailing list](https://lists.mozilla.org/listinfo/dev-fxos) or #fxos on IRC. Thanks!

## About Peter Dolanjski

Peter is a Product Manager for Firefox and a defender of the open Web.

## 78 comments

MarekNovember 10th, 2015 at 12:57Peter DolanjskiNovember 10th, 2015 at 13:15Bruce KeNovember 10th, 2015 at 23:15RaulNovember 11th, 2015 at 07:14Peter DolanjskiNovember 11th, 2015 at 07:38Narender SinghNovember 11th, 2015 at 09:33Peter DolanjskiNovember 11th, 2015 at 09:46Yash VardhanNovember 11th, 2015 at 09:53Peter DolanjskiNovember 11th, 2015 at 13:13Narender SinghNovember 11th, 2015 at 10:10Peter DolanjskiNovember 11th, 2015 at 10:16Ilija CanovićNovember 11th, 2015 at 10:22StewartNovember 11th, 2015 at 12:36Peter DolanjskiNovember 11th, 2015 at 13:00MarekNovember 11th, 2015 at 13:05PrakashNovember 11th, 2015 at 14:24Peter DolanjskiNovember 12th, 2015 at 06:40ErrolNovember 11th, 2015 at 14:48Peter DolanjskiNovember 12th, 2015 at 06:42nicoNovember 11th, 2015 at 16:16Peter DolanjskiNovember 12th, 2015 at 06:44WayneNovember 11th, 2015 at 23:14AshrafurNovember 12th, 2015 at 01:30Peter DolanjskiNovember 12th, 2015 at 06:45Sesha_November 12th, 2015 at 03:25Peter DolanjskiNovember 12th, 2015 at 06:45SajiNovember 12th, 2015 at 04:31DaveNovember 12th, 2015 at 04:34Peter DolanjskiNovember 12th, 2015 at 06:46VimalNovember 12th, 2015 at 04:44Peter DolanjskiNovember 12th, 2015 at 06:47VimalNovember 12th, 2015 at 04:47Jia Yuan LoNovember 12th, 2015 at 05:04Peter DolanjskiNovember 12th, 2015 at 06:48BhargavNovember 12th, 2015 at 05:56bastiaanNovember 12th, 2015 at 06:55Peter DolanjskiNovember 12th, 2015 at 06:57Edgar Ilasaca AquimaNovember 12th, 2015 at 07:53johnNovember 12th, 2015 at 08:31Peter DolanjskiNovember 12th, 2015 at 12:26DKNovember 12th, 2015 at 08:56Peter DolanjskiNovember 12th, 2015 at 12:27Zac MeyersNovember 12th, 2015 at 11:03Peter DolanjskiNovember 12th, 2015 at 12:30Firefox OS GuideNovember 12th, 2015 at 11:26NathanNovember 12th, 2015 at 15:35AndrewNovember 12th, 2015 at 19:22Peter DolanjskiNovember 12th, 2015 at 19:36Nitin joshiNovember 12th, 2015 at 19:32Peter DolanjskiNovember 13th, 2015 at 10:42Nitin joshiNovember 12th, 2015 at 19:39Anwaar AliNovember 12th, 2015 at 20:38kariemoNovember 13th, 2015 at 01:25Geek DashboardNovember 13th, 2015 at 10:22Peter DolanjskiNovember 13th, 2015 at 10:42SamirNovember 14th, 2015 at 07:22Richard AyotteNovember 14th, 2015 at 09:59bastiaanNovember 15th, 2015 at 06:52nksNovember 16th, 2015 at 08:18Peter DolanjskiNovember 17th, 2015 at 08:57Zac MeyersNovember 16th, 2015 at 09:30Luya TshimbalangaNovember 16th, 2015 at 19:10Peter DolanjskiNovember 17th, 2015 at 08:54KarthikNovember 17th, 2015 at 05:30Peter DolanjskiNovember 17th, 2015 at 08:53minidouNovember 17th, 2015 at 13:03Dan CallahanNovember 17th, 2015 at 13:26NicolasNovember 17th, 2015 at 14:48KashifNovember 18th, 2015 at 23:01RatulNovember 19th, 2015 at 03:25Luya TshimbalangaNovember 19th, 2015 at 16:42Kohei YoshinoNovember 22nd, 2015 at 14:46sagarNovember 23rd, 2015 at 02:32gourabNovember 23rd, 2015 at 05:32Zac MeyersNovember 23rd, 2015 at 10:59Jose MNovember 26th, 2015 at 01:52RishiDecember 3rd, 2015 at 10:48Havi Hoffman [Editor]December 4th, 2015 at 14:53