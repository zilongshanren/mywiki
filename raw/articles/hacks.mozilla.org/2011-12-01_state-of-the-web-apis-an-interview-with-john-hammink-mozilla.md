---
title: State of the Web APIs – an interview with John Hammink – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2011/12/state-of-the-web-apis-an-interview-with-john-hammink/
author: Janet Swisher
published: '2011-12-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As you might be aware, Mozilla is working hard on [making mobile development possible with purely open technologies](http://arewemobileyet.com). For this, we are defining a set of APIs to access the hardware of mobile devices called the [Web API](https://wiki.mozilla.org/WebAPI)s. John Hammink of Mozilla [published a blog post](http://johnhammink.blogspot.com/2011/11/lets-have-look-at-some-recently-landed.html) on the subject on Monday outlining the current state of affairs. A good chance to have a chat about where we are and to ask what you can do to help Mozilla in this effort.

**1) John, what is your involvement in the Web APIs project?**

I am the lead QA. I am also assuming an evangelist role – we need to get the community involved as early as possible around testing these. Not to mention building apps around these! Wanna help?

**2) What are the APIs that are ready to play at the moment and what do people need to try them out?**

I’ve made a few [atomic testpages around testing the webapis available](http://people.mozilla.com/~jhammink/webapi_test_pages). These are: Battery, Camera, IndexedDB, Vibrator and SMS. More are coming soon – but perhaps require combination with other APIs (for example, Telephony requires Audio); that and other APIs are specific to [Boot to Gecko (B2G)](https://wiki.mozilla.org/B2G).

**3) So the battery API is one of the first ones to land. Whilst interesting as an information piece on your phone, it is not quite that fascinating for developers. What uses cases can you think of? Maybe reading the battery before your massive WebGL animation and reading it afterwards?**

Maybe I have a WebGL simulation or, perhaps, a game that requires a certain power output or power availability. We can, for example, trigger notifications when power goes below a certain level. If it’s a productivity app, maybe we want to trigger the user to save their work.

**4) Camera APIs, now we are getting somewhere! How is the support for Canvas on Fennec and mobile devices? The first thing that would get me interested is to do an Instagram in HTML5 by changing the photos.**

Canvas works identically to desktop. Taking the picture – which JS then renders – is the bulk of the use-case.

Arguably you could implement zooming so that you can check the picture in more detail. Another thing we have yet to try is checking the rendered image for EXIF metadata.

**5) You mention IndexDB as an alternative to store local data as that could be dangerous to the file system. The main benefit of localStorage() is that the API is dead easy though. Is there a chance to have a wrapper to use the localStorage() API but store in the DB?**

The problem is that localstorage() is sync – which makes it easy to use but, as you can imagine, introduces tremendous performance issues. As our Indexeddb is an async API – you can’t wrap a sync api around an async one.

**6) Good vibrations. The vibrator API allows you to vibrate the device. I can see that working really well for games and notifications. Or with the orientation API telling you when you tilt too far. Is there a way to detect if the vibration is turned on or off? I know quite a few people that turned off device vibration.**

I can’t wait to see where my name shows up in search results thanks to this one. There is no API for detecting this – it’s been theorized that you can deduce its presence using the orientation API – i.e. it would see the vibrations. But this would vary from device to device; as not all devices have vibrator.

**7) Sending SMS with JavaScript is the last API you mention. This is working as far as I understand it. What is the most requested use case there? Is there a throttling mechanism to stop people from sending SMS spam or mass mailings?**

Aside from the about:config setting dom.sms.enabled, there is no specific throttling mechanism. It is to be a “trusted” API, that is, we won’t expose it to all pages. As with many of these APIs there are inherent security threats – in the case of this one, you can for example, end up sending text messages to paid-for services.

**8) This is all pretty cool. What do you want from people now and where can they go to get all that to play with?**

Check out my blogpost and try out the testpages themselves on my people share! I’d recommend using [latest XUL nightlies](https://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/latest-mozilla-central-android-xul/) – for SMS, you need a phone with a sim card and a special build which is linked in the blogpost. Play around! Note that these are presently atomic APIs, each representing a single function. Make suggestions via bugzilla -and write bugs! And it goes without saying also to try to combine these (and the others as they land) into working apps of your own. Our challenge will not only be to find out how these APIs work on their own but also in combination with another. I would say that IndexDB at this stage represents a particular challenge, due to its size and complexity.

## Help us move the mobile web forward

- Get the latest
[XUL Fennec build](https://ftp.mozilla.org/pub/mozilla.org/mobile/nightly/latest-mozilla-central-android-xul/)to test the APIs - To test the SMS API, get a
[special build of Fennec](http://people.mozilla.org/~jhammink/android_builds_4_testing_webapi/for_SMS_API/fennec-11.0a1.en-US.android-arm.apk)and be sure to have a phone with a SIM card - Then have a go trying all the tests on the the
[WebAPI test pages](http://people.mozilla.org/~jhammink/webapi_test_pages/) [Report bugs](http://shrt.st/2adv)with any of the demos and/or APIs themselves (make sure to include your device model and Android version, as well as the nightly fennec version you are using, in the bug.).- Here are the different APIs you can play with:
[Join the WebAPI Google Group](http://groups.google.com/group/mozilla.dev.webapi/topics)if you really want to be in the thick of it

The test pages are [available on GitHub](https://github.com/jhammink/WebAPI-test-pages) if you want to check the code.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!