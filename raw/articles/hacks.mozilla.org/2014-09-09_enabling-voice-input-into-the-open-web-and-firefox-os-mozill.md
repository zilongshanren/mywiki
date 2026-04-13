---
title: Enabling Voice Input into the Open Web and Firefox OS – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2014/09/enabling-voice-input-into-the-open-web-and-firefox-os/
author: Sandip Kamat
published: '2014-09-09'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With the advent of smartphones triggered by iPhone in 2007, Touch became the primary mode of input for interacting with these devices. And now with the advent of wearables (and other hands-free technologies that existed before), Voice is becoming another key method of input. The possibilities of experiences Voice Input enables are huge, to say the least.

They go beyond just merely interacting with in-vehicle devices, accessories and wearables. Just think of the avenues Voice Input opens up for bringing more technologies to more people. It’s enormous: Accessibility, Literacy, Gaming, VR and the list goes on. There is a social vibe there that definitely resonates with our mission at Mozilla detailed in our [Mozilla Manifesto](https://www.mozilla.org/en-US/about/manifesto/)

## How it started

Both current leading mobile OS/ecosystem providers of today- Apple & Google have their native experiences with Siri and “OK Google” (coupled with Google Now). We really needed an effort to enable Voice Input into the first ecosystem that existed – the open Web. Around MWC 2013 in Barcelona, when [Desigan Chinniah](https://twitter.com/cyberDees) introduced me to [André Natal](https://twitter.com/andrenatalbr) – Firefox contributor from Brazil, we had a conversation around this and we instantly agreed to do something about this in whichever way possible. Andre told me about being inspired from a talk by [Brendan Eich](http://brendaneich.com/) in [BrazilJS](http://braziljs.com.br/), so I did not have much convincing to do. :-)

## First steps

We had numerous calls and meetings over the past year on the approach and tactics around this. Since “code wins arguments”, the basic work started in parallel with Firefox desktop and FxOS Unagi devices, later switching to Mozilla Flame devices over time. Over a period of the past year, we had several meetings with Mozilla engineering leads on exact approach and decided to break this effort into several smaller phases (“baby steps”).

The first target was getting [Web Speech API](https://dvcs.w3.org/hg/speech-api/raw-file/tip/speechapi.html) implemented, and getting acoustic/language modules integrated with a decoder and giving that a try. Lots of similar minded folks in Mozilla Engineering/QA & community helped along with guidance and code-reviews while Andre moonlighted (on top of his day job) with a very high focus. Things moved fast in past month or so. (Well, to be honest, the only day this effort slowed down was when Team Brazil lost to Germany in FIFA 2014. :-)) Full credit to André for his hard work!

## Where are we?

Our current thinking is to get a grammar-based (limited commands) app working first and distribute it in our rich & diverse international Mozilla community for accent-based testing and enhancements. Once we have this stablilized, we will get into the phase 2 where we can focus more on natural language processing and get closer to a virtual assistant experience sometime in future that can give users voice based answers. There is lots of work to do there and we are just beginning.

I will save the rest of the details for later and jump to the current status this month. Where are we so far?

We now have the Web Speech API ready for testing and we have a couple demos for you to see!

### Desktop: Firefox Nightly on Mac

*Editor’s note: for full effect, start playing the two above videos at the same time.*

### Firefox OS demo

Come, Join us!

If you want to follow along, please look at the [ SpeechRTC – Speech enabling the open web wiki](https://wiki.mozilla.org/SpeechRTC_-_Speech_enabling_the_open_web) and [Bug 1032964 – Enabling Voice input in Firefox OS](https://bugzilla.mozilla.org/show_bug.cgi?id=1032964).

So jump in and help out if you can. We need all of you (and your voices). Remember “Many Voices, One Mozilla”!

## About
[
Sandip Kamat ](https://twitter.com/sankam)

Sandip Kamat is part of Mozilla's Connected Devices Product Management team. He has spent most of his career in building mobile technologies and products. Prior to joining Mozilla, he worked at Motorola Mobility (later, owned by Google) and Siemens Mobile. He is an alum of IIT Madras and UCSD (Rady). He is passionate about bringing cutting edge technologies to everyday people to make their lives meaningfully better.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

szimekSeptember 9th, 2014 at 15:21Andre NatalSeptember 10th, 2014 at 06:12Marco ChenSeptember 10th, 2014 at 07:58Andre NatalSeptember 11th, 2014 at 00:12szimekSeptember 11th, 2014 at 14:02Sandip KamatSeptember 10th, 2014 at 15:10szimekSeptember 11th, 2014 at 06:40Sandip KamatSeptember 18th, 2014 at 04:58RiccardoSeptember 9th, 2014 at 23:13Andre NatalSeptember 10th, 2014 at 06:17RiccardoSeptember 11th, 2014 at 01:35Andre NatalSeptember 11th, 2014 at 01:37NoitidartSeptember 13th, 2014 at 01:47NoitidartSeptember 13th, 2014 at 01:50