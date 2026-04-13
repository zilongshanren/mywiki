---
title: WebIDE Lands in Nightly – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/06/webide-lands-in-nightly/
author: Dave Camp
published: '2014-06-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

**Editor’s note**: if you want to help test it on a recent nightly you can toggle the devtools.webide.enabled preference in about:config. The WebIDE is available **today** under Tools>Web Developer>App Manager and will be renamed in tomorrow’s Nightly into WebIDE.

If you’ve been following our [Developer Tools series](https://hacks.mozilla.org/category/developer-tools/) on the Mozilla Hacks blog, you’ve seen the developer tools evolve from pure inspection to a debugging environment both for web sites and apps on desktop and mobile. Today we want to introduce you to the next step of evolution: adding in-browser editing features across devices.

## WebIDE

Developers tell us that they are not sure how to start app development on the Web, with so many different tools and templates that they need to download from a variety of different sources. We’re solving that problem with WebIDE, built directly into Firefox. Instead of starting from zero we provide you with a functioning blueprint app with the click of a button. You then have all the tools you need to start creating your own app based on a solid foundation. WebIDE helps you create, edit, and test a new Web application right from your browser. It lets you install and test apps on Firefox OS devices and simulators and integrates the Firefox Developer Tools for seamless debugging and inspection across those devices. This is a first step towards debugging across various platforms and devices over WiFi using open remote debugging APIs.

### Getting Started

After opening WebIDE you start creating your new application with a few clicks. You choose from a set of example starter templates – and we’re working with the community to build a wide variety of additional examples. You can help creating templates by visiting [https://github.com/mozilla/mortar](https://github.com/mozilla/mortar).

### Editing

Once you’ve started your project, you can edit the source files in WebIDE. Its integrated editor – based on the open source [CodeMirror editor](http://codemirror.net/) with the [tern.js code analysis framework](http://ternjs.net/) – gives you a simple but powerful editor for HTML, JavaScript, and CSS files.

While working with your [web application manifest](https://developer.mozilla.org/en-US/Apps/Build/Manifest), the application validator will help you find common problems before submitting to the [marketplace](https://marketplace.firefox.com/).

While this is enough for your basic editing needs, you might want to use your own preferred editor instead. To do this you can use a simple API which allows external editors to access all the advanced functionality of the tool – its runtime management, pushing applications to different devices and connecting Firefox Developer Tools. You can turn off our internal editor and leave WebIDE with a simple, clean interface for managing runtimes and validating applications. We want to make it easy for users of any code editor to sling their code around to various devices.

### Runtimes and Testing

When you’re ready to test your application, choose a runtime – we’ll install Firefox OS simulators for you or help you connect to your Firefox OS device. Once connected to a runtime, you can use the tools that you’re used to in desktop Firefox to try your application. You have the same sort of rapid iteration that makes developing for the desktop web simple – just hit Ctrl/Command+R to reload the application on your device or simulator. You can get information about the device and runtime and take screenshots.

### Take a Look

You can see the WebIDE in action [in this screencast](https://www.youtube.com/watch?v=n8c34wk4OnY)

While we put on some finishing touches, WebIDE is checked into Firefox Nightly but is hiding behind a pref – if you want to help test it on a recent nightly you can toggle the devtools.webide.enabled preference in about:config:

## The Future: Developing for the Whole Web

At the heart of the WebIDE is the Firefox Remote Debugging Protocol. The Firefox Developer Tools team has put a lot of work into making sure all of our tools work on remote devices running over USB, but that’s really only the beginning. With WebIDE managing these connections we can use the Firefox Developer Tools – and any other tools that want to use our protocol – anywhere.

Right now this protocol is useful for Firefox Desktop, Firefox Android, and Firefox OS. But we aren’t stopping there. We’re working on a protocol adapter that will allow clients using the Firefox Remote Debugging Protocol – including the Developer Tools and WebIDE – talk to all mobile browsers, regardless of rendering engine or runtime. Our first targets are Chrome for Android and Safari on iOS.

This web-everywhere project isn’t yet ready for testing, but if you’re excited to get involved or see how it is being implemented, it currently lives at [https://github.com/campd/fxdt-adapters](https://github.com/campd/fxdt-adapters).

If you’re building a tool and want to start playing with the protocol you can start now, developing against Firefox Desktop, Firefox Android, and Firefox OS. For information about the Remote Debugging Protocol, take a look at [the documentation](https://wiki.mozilla.org/Remote_Debugging_Protocol).

Thanks for reading. We look forward to hearing your feedback in the comments, on our [UserVoice feedback channel](http://mzl.la/devtools) and on Twitter [@firefoxdevtools](https://twitter.com/firefoxdevtools).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 72 comments

GregorJune 23rd, 2014 at 08:23Chris HeilmannJune 23rd, 2014 at 09:06Ian BickingJune 23rd, 2014 at 08:57Victor PorofJune 23rd, 2014 at 10:25UnrJune 23rd, 2014 at 09:02richJune 23rd, 2014 at 09:42Guestinator 2000June 23rd, 2014 at 15:56MihaiJune 24th, 2014 at 04:58Tin Aung LinJune 25th, 2014 at 22:39RichJune 23rd, 2014 at 09:02Chris HeilmannJune 23rd, 2014 at 09:06Fabio VenniJune 23rd, 2014 at 09:10RichJune 23rd, 2014 at 09:12Chris HeilmannJune 23rd, 2014 at 09:24Paul RougetJune 23rd, 2014 at 09:26RichJune 23rd, 2014 at 09:31Fabio VenniJune 23rd, 2014 at 09:38MikeJune 23rd, 2014 at 09:14Caspy7June 23rd, 2014 at 09:46Jitendra VyasJune 23rd, 2014 at 09:51Jeff GriffithsJune 23rd, 2014 at 18:11CommenterJune 23rd, 2014 at 10:43Jeff GriffithsJune 23rd, 2014 at 18:02CommenterJune 24th, 2014 at 00:32Rob CampbellJune 24th, 2014 at 11:03anonymousJune 23rd, 2014 at 11:40Irtaza Ahmed QureshiJune 23rd, 2014 at 11:52fvschJune 23rd, 2014 at 12:29Brian GrinsteadJune 23rd, 2014 at 15:20JhonyJune 23rd, 2014 at 13:01FrustratedJune 23rd, 2014 at 13:27LukeJune 23rd, 2014 at 22:27YelanJune 28th, 2014 at 04:50Harry MorenoJune 23rd, 2014 at 13:34RobertJune 23rd, 2014 at 13:40Jeff GriffithsJune 23rd, 2014 at 15:24LeoJune 23rd, 2014 at 21:51Benjamin AtkinJune 23rd, 2014 at 15:50g.gJune 24th, 2014 at 10:03Argh!June 23rd, 2014 at 19:58viperafkJune 24th, 2014 at 16:12Oğuz ÇelikdemirJune 24th, 2014 at 22:35Andrew EisenbergJune 23rd, 2014 at 20:02AdamJune 23rd, 2014 at 20:57IdoJune 24th, 2014 at 00:30really?June 24th, 2014 at 02:55tux.June 24th, 2014 at 02:57elavJune 24th, 2014 at 03:50Felix E. KleeJune 24th, 2014 at 05:12Stephen PriceJune 24th, 2014 at 08:39JeffreyJune 24th, 2014 at 08:43ChristianJune 24th, 2014 at 08:50FredJune 24th, 2014 at 16:40IdoJune 24th, 2014 at 08:55JoãoJune 24th, 2014 at 09:40Charles N WybleJune 24th, 2014 at 10:00Stephen PriceJune 24th, 2014 at 15:03Viswaprasath KSJune 24th, 2014 at 10:21AxelJune 24th, 2014 at 12:21bobJune 24th, 2014 at 16:05AxelJune 24th, 2014 at 23:06TimJune 25th, 2014 at 02:29NiklasJune 25th, 2014 at 04:38iskaelJune 25th, 2014 at 04:38Carfield YimJune 26th, 2014 at 00:48zalunJune 26th, 2014 at 15:30JuanMa RuizJune 27th, 2014 at 00:14Altfred KayserJune 28th, 2014 at 03:39YelanJune 28th, 2014 at 04:38shirokoffJune 30th, 2014 at 00:34Edwin Yip | Dev of LIVEditorJuly 11th, 2014 at 12:24Maxime WackJuly 18th, 2014 at 09:28