---
title: 'Firefox Developer Edition 38: 64-bits and more – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/03/firefox-developer-edition-38-64-bits-and-more/
author: Dave Camp
published: '2015-03-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In celebration of the 10th anniversary of Firefox, we unveiled Firefox Developer Edition, the first browser created specifically for developers. At that time, we also announced plans to ship a 64-bit version of Firefox. Today we’re happy to announce the next phase of that plan: 64-bit builds for Firefox Developer Edition are now available on Windows, adding to the already supported platforms of OS X and Linux.

A 64-bit build is a major step toward giving users rich, desktop-quality app experiences in the browser. Let’s also take a look at at some of the other features that make this a release worth noting. If you haven’t downloaded the Developer Edition browser yet, it’s a fine time to give it a try. Here’s why:

*Unreal demo in Win 64-bit Developer Edition*

### Run larger applications

A 32-bit browser is limited to 4GB of address space. That address space is further whittled down by fragmentation issues. Meanwhile, web applications are getting bigger and bigger. Browser-based games that deliver performant, native-like gameplay, such as those built with Epic Games’ Unreal Engine, are often much larger than we expect from traditional web applications. These games ship with large assets that must be stored in memory so they can be synchronously loaded.

For some of the largest of these apps, a 64-bit browser means the difference between whether or not a game will run. For example, when porting to asm.js it’s recommended to keep heap size to 512mb in a 32-bit browser. That goes up to 2GB in a 64-bit version of Firefox.

Emscripten helps port C and C++ code to run on the Web and deliver native-like performance. For an in-depth look at how assets are stored and accessed using a variety of methods in asm.js/emscripten built applications, read Alon Zakai’s post on [Synchronous Execution and Filesystem Access in Emscripten](https://hacks.mozilla.org/2015/02/synchronous-execution-and-filesystem-access-in-emscripten/).

### Gain faster execution and increased security

64-bit Firefox just goes faster. We get access to new hardware registers and instructions to speed up JavaScript code.

For asm.js code, the increased address space also lets us use hardware memory protection to safely remove bounds checks from asm.js heap accesses. The gains are pretty dramatic: 8%-17% on the asmjs-apps-*-throughput tests as reported on [arewefastyet.com](http://arewefastyet.com/#machine=29&view=breakdown&suite=asmjs-apps).

The larger 64-bit address space also improves the effectiveness of [ASLR](http://en.wikipedia.org/wiki/Address_space_layout_randomization) (address space layout randomization), making it more difficult for web content to exploit the browser.

### Firefox Developer Edition additions and improvements

Beyond the new 64-bit capabilities, the Firefox 38 Developer Edition release implements many new features, as it does every 6 weeks when it is updated. Some of these are described below. For all the details and associated bugs in progress, you’ll want to visit the [release notes](https://www.mozilla.org/en-US/firefox/38.0a2/auroranotes/).

##### WebRTC changes

In a post about WebRTC from 2013, we documented [some workarounds and limitations](https://hacks.mozilla.org/2013/09/webrtc-update-and-workarounds/) of WebRTC [mozRTCPeerConnection](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection). One fix involved adding multiple [MediaStreams](https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_API) to one mozRTCPeerConnection and renegotiating on an existing session.

The new version of Firefox Developer Edition fixes these issues. We now support adding multiple media streams (camera, screen sharing, audio stream) to the same mozRTCPeerConnection within a WebRTC conversation. This allows the developer to call the [addStream](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/addStream) method for each additional stream, which in turn triggers the [onAddStream](https://developer.mozilla.org/en-US/docs/Web/API/RTCPeerConnection/onaddstream) event for the clients.

Renegotiation allows streams to be modified during a conversation, for example sharing a screen stream during a conversation. This is now possible without re-creating a session.

*WebRTC with multiple streams*

Last week we announced that [WebRTC requires Perfect Forward Secrecy (PFS) starting in Firefox 38](https://hacks.mozilla.org/2015/02/webrtc-requires-perfect-forward-secrecy-pfs-starting-in-firefox-38/). We’ll dig a little deeper into details of our WebRTC implementation in an upcoming article. Stay tuned.

##### The BroadcastChannel API

The BroadcastChannel API allows simple messaging between browser contexts with the same user agent and origin is now available. Here’s more detail and some ideas for how to use the [BroadcastChannel API in Firefox 38](https://hacks.mozilla.org/2015/02/broadcastchannel-api-in-firefox-38/).

##### Support for KeyboardEvent.code

[KeyboardEvent.code](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code) is now enabled by default. The code attribute give a developer the ability to determine which physical key is pressed without keyboard layout or keyboard state modifications.

*KeyboardEvent code attribute*

For more examples of uses cases see [the motivation section](https://dvcs.w3.org/hg/dom3events/raw-file/tip/html/DOM3-Events.html#code-motivation) of the UI Events Specification (formerly DOM Level 3 Events).

##### XHR logging

The [Network Monitor](https://developer.mozilla.org/en-US/docs/Tools/Network_Monitor) already displays a great deal of information on [XMLHttpRequests](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/Using_XMLHttpRequest), but often the console is used to debug code along with network requests. In the latest Developer Edition of Firefox, the console now supports filtering XMLHttpRequests within console logging.

*Network Monitor XHR Request*

*XHR logging in console*

### Let us know what you think

Many additional improvements are available in this version. [Download it now]( https://www.mozilla.org/en-US/firefox/developer/all/). Tell a friend.

As always, you can take a close look at the [Developer Edition release notes](https://www.mozilla.org/en-US/firefox/38.0a2/auroranotes/). Please be sure to share your feedback and feature ideas in the Firefox Developer Tools [UserVoice channel](https://ffdevtools.uservoice.com/forums/246087-firefox-developer-tools-ideas).

## About Dave Camp

Dave Camp is Director of Engineering for Firefox at Mozilla.

## 32 comments

Robson SobralMarch 2nd, 2015 at 08:46Fabricio C ZuardiMarch 2nd, 2015 at 11:05Havi Hoffman [Editor]March 2nd, 2015 at 11:24Robson SobralMarch 2nd, 2015 at 17:15MTMarch 2nd, 2015 at 12:21Robson SobralMarch 2nd, 2015 at 17:17MTMarch 3rd, 2015 at 08:34Graham GreensallMarch 2nd, 2015 at 16:03Panos AstithasMarch 2nd, 2015 at 23:23Andy EarnshawMarch 3rd, 2015 at 00:59MarcoMarch 3rd, 2015 at 02:29Graham GreensallMarch 3rd, 2015 at 08:42PTMMarch 3rd, 2015 at 11:43Michael DrozdowskiMarch 2nd, 2015 at 23:36Mike CampbellMarch 3rd, 2015 at 01:28MarcoMarch 3rd, 2015 at 02:21mattMarch 3rd, 2015 at 11:01Havi Hoffman [Editor]March 3rd, 2015 at 11:35Graham GreensallMarch 3rd, 2015 at 14:06Graham GreensallMarch 6th, 2015 at 02:48Amit KulkarniMarch 2nd, 2015 at 22:16Gopal VenkatesanMarch 2nd, 2015 at 23:04MadhatterMarch 3rd, 2015 at 02:16a-lMarch 3rd, 2015 at 05:55DianaMarch 5th, 2015 at 18:01OliverMarch 3rd, 2015 at 20:59OliverMarch 3rd, 2015 at 21:21TuxMarch 4th, 2015 at 08:18nemoMarch 20th, 2015 at 09:28nemoMarch 20th, 2015 at 10:42paulMarch 4th, 2015 at 11:38JonathanMarch 4th, 2015 at 14:04