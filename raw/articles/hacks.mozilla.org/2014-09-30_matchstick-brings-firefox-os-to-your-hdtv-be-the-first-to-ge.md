---
title: 'Matchstick Brings Firefox OS to Your HDTV: Be the First to get a Developer
  Stick – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2014/09/matchstick-brings-firefox-os-to-your-hdtv-be-the-first-to-get-a-developer-stick/
author: Shawn Bow
published: '2014-09-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The first HDMI streaming stick powered by Firefox OS has arrived. It’s called [Matchstick](http://www.matchstick.tv/) and we’re looking for your help to create apps for this new device.

## Background

Matchstick stems from a group of coders that spent way too much time mired in the guts of platforms such as Boot to Gecko, XBMC, and Boxee. When Google introduced Chromecast we were excited about the possibilities but ultimately were disappointed when they pulled back on the device’s ultimate promise – any content on any HD screen, anywhere, anytime.

We decided to make something better and more open, and to accomplish this we had to choose an operating system that would become the bedrock for the adaptable and open-sourced platform that is Matchstick. That platform is [Firefox OS](https://www.mozilla.org/en-US/firefox/os/), which allows us to build the first streaming stick free of any walled garden ecosystem.

Matchstick and Firefox OS combined offers a totally open platform (both software and hardware), that lets developers explore content and applications from video to games, and bring it right into the living room. That’s right Developers! An open SDK means you can build out your own personalized streaming and interactive experiences without the need for approval or review.

## Apps for Matchsticks

We have opened up a [full developer site](http://www.matchstick.tv/developers/index.html) with access to everything you need to begin working with Matchstick. Support for Firefox OS will be available at launch, and we look forward to adding TV applications to the Firefox OS Marketplace. For now, we have included a [full API library](http://www.matchstick.tv/developers/documents/developers-guide.html), of sender apps with support for Android and iOS, as well as receiver apps that are compatible with the Matchstick Receiver.

When we say Apps for Matchsticks, we mean both sender and receiver apps. You can use the sender APIs to enable your Firefox OS, Android or iOS device to discover a Matchstick device, then communicate with your receiver app. It’s not difficult to embed sender APIs into existing apps or create new sender apps, please refer to the sample code we have included with the SDK.

Matchstick sender apps typically follow this execution flow:

**Scan for Matchstick**

The sender app searches for Matchstick devices residing in the same Wi-Fi network as the sender device. The scanning reveals a friendly display name, model and manufacturer, icon, and the device’s IP address. Presented with a list, a user may then select a target device from all those discovered.**Connect to Matchstick**

We support both TLS and NON-TLS communication between sender and receiver.**Launch Receiver App**

The sender initiates a negotiation with the target device, launching a receiver app either with the URL of a HTML5 receiver app, or even a Chromecast App ID.**Establish Message Channels**

With the receiver app now launched, Matchstick establishes message channels between the sender and receiver. In addition to a media control channel common to all Matchstick and Chromecast apps, you may establish any number of application-specific channels to convey whatever customized data that your app might require.

The receiver app is a combination of HTML5, CSS and Javascript, loaded into a “receiver container” which is a certified app of Firefox OS. To use the Matchstick receiver APIs, you need only include fling_receiver.js in your app.

Here is an example of a simple video receiver app:

```
```Example simplest receiver

## Matchsticks for Apps

Rather than relying on emulators, we want to be sure developers can get their hands on Matchstick prototypes and start coding without delay. As a result, we are inviting app developers who will commit to building and porting apps for Firefox OS on Matchstick to [apply for a free developer-preview device through our Matchsticks for Apps program](http://www.matchstick.tv/developers/register.html).

Similar to the phones-for-apps program launched by Mozilla, our Matchsticks for Apps program is aimed at developers who have built apps for Firefox OS, Chrome, Android, iOS …. Even for Chromecast! Let’s bring those visions to the big screen.

![image](../../assets/9fb484e534aa002b.jpg)


*Developer (pre-production) version of Matchstick ( pic by Christian Heilmann)*

We are now looking for good ideas, video content, new channels, as well as games, tools, utilities, pictures, even skins for the UI. If you have a plan to build apps or do something for Matchstick, please share your plan and we’ll send you a stick so you can start coding ASAP.

Who Should Apply:

- Those interested in building apps on a big screen TV
- Those with existing Web or mobile apps, who would like to expand to the big screen
- HDMI dongle developers, who want to build their own Matchstick
- Chromecast developers, who want to port their apps to an open platform
- You!

## Matchstick workshop in November

On Tuesday, November 18th, we plan to host an invitation-only Firefox OS App Workshop for Matchstick in the Mozilla office in San Francisco. The enrollment form is open and we are accepting applications from qualified developers.

If you don’t live near San Francisco, don’t worry! We plan to offer several other app workshops in the near future and we’ll announce them here, of course!

Happy Hacking!

## About Shawn Bow

Shawn Bow graduated from the Beijing University of Communication. He has been working on Embedded Systems software development for ten years, and worked for several technology companies including Motorola and Marvell. He began Android development in 2007 where he worked on China Open Mobile System development for three years, and then Android tablet and TV products for four years. In 2014, he joined the Matchstick team. He can be contacted at shawn.bow@matchstick.tv

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 40 comments

Accelerate!September 30th, 2014 at 08:29Kumar McMillanSeptember 30th, 2014 at 09:51Fawad HassanOctober 2nd, 2014 at 09:41Kumar McMillanOctober 2nd, 2014 at 09:52Robert Nyman [Editor]October 2nd, 2014 at 10:05BenSeptember 30th, 2014 at 09:36Shawn BowOctober 1st, 2014 at 13:54Pete DixonSeptember 30th, 2014 at 09:39Shawn BowOctober 1st, 2014 at 15:58HobartSeptember 30th, 2014 at 09:46Shawn BowOctober 1st, 2014 at 16:05BerndSeptember 30th, 2014 at 09:49Shawn BowOctober 1st, 2014 at 16:09HobartSeptember 30th, 2014 at 10:05Rodrigo MorenoSeptember 30th, 2014 at 13:18Shawn BowOctober 1st, 2014 at 16:10Rodrigo MorenoOctober 1st, 2014 at 18:50Doug ReederSeptember 30th, 2014 at 13:37voracitySeptember 30th, 2014 at 21:06Shawn BowOctober 1st, 2014 at 16:12VincentOctober 2nd, 2014 at 02:32Kumar McMillanOctober 2nd, 2014 at 09:57Parth LawateOctober 1st, 2014 at 10:26Shawn BowOctober 1st, 2014 at 16:13Parth LawateOctober 1st, 2014 at 18:14Shawn BowOctober 1st, 2014 at 16:22Shawn BowOctober 2nd, 2014 at 01:38Martin LasakOctober 2nd, 2014 at 03:49Martin LasakOctober 2nd, 2014 at 06:44Bruce LenihanOctober 3rd, 2014 at 00:31Patrick H. LaukeOctober 3rd, 2014 at 05:16Robert Nyman [Editor]October 3rd, 2014 at 05:19Patrick H. LaukeOctober 3rd, 2014 at 05:20Robert Nyman [Editor]October 3rd, 2014 at 05:54MichaelOctober 9th, 2014 at 00:58Hayato.KOctober 17th, 2014 at 01:24Robert Nyman [Editor]October 17th, 2014 at 01:32Hayato.KOctober 17th, 2014 at 08:13victorOctober 24th, 2014 at 22:50MaxOctober 27th, 2014 at 15:59