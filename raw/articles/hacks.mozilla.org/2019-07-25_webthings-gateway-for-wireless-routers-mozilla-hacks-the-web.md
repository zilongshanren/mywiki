---
title: WebThings Gateway for Wireless Routers – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2019/07/webthings-gateway-for-wireless-routers/
author: Ben Francis
published: '2019-07-25'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## Wireless Routers

In April we [announced](https://hacks.mozilla.org/2019/04/introducing-mozilla-webthings/) that the [Mozilla IoT](https://iot.mozilla.org/) team had been working on evolving [WebThings Gateway](https://iot.mozilla.org/gateway/) into a full software distribution for consumer wireless routers.

Today, with the 0.9 release, we’re happy to announce the availability of the first experimental builds for our first target router hardware, the [Turris Omnia](https://www.turris.cz/en/omnia/).

These builds are based on the open source [OpenWrt](https://openwrt.org/) operating system. They feature a new first-time setup experience which enables you to configure the gateway as a router and Wi-Fi access point itself, rather than connecting to an existing Wi-Fi network.

So far, these experimental builds only offer extremely basic router configuration and are not ready to replace your existing wireless router. This is just our first step along the path to creating a full software distribution for wireless routers.

We’re planning to add support for other wireless routers and router developer boards in the near future. We want to ensure that the user community can access a range of affordable developer hardware.

## Raspberry Pi 4

As well as these new OpenWrt builds for routers, we will continue to support the existing Raspbian-based builds for the Raspberry Pi. In fact, the 0.9 release is also the first version of WebThings Gateway to support the new [Raspberry Pi 4](https://www.raspberrypi.org/products/raspberry-pi-4-model-b/). You can now find a [handy download link](https://www.raspberrypi.org/downloads/) on the Raspberry Pi website.

## Notifier Add-ons

Another feature landing in the 0.9 release is a new type of add-on called notifier add-ons.

In previous versions of the gateway, the only way you could be notified of events was via browser [push notifications](https://developer.mozilla.org/en-US/docs/Web/API/Push_API). Unfortunately, this is not supported by all browsers, nor is it always the most convenient notification mechanism for users.

A workaround was available by creating add-ons with basic “send notification” actions to implement different types of notifications. However, these required the user to add “things” to their gateway which didn’t represent actual devices and actions had to be hard-coded in the add-on’s configuration.

To remedy this, we have introduced notifier add-ons. Essentially, a notifier creates a set of “outlets”, each of which can be used as an output for a rule. For example, you can now set up a rule to send you an SMS or an email when motion is detected in your home. Notifiers can be configured with a title, a message and a priority level. This allows users to be reached where and how they want, with a message and priority that makes sense to them.

## API Changes

For developers, the 0.9 release of the WebThings Gateway and 0.12 release of the [WebThings Framework](https://iot.mozilla.org/framework/) libraries also bring some small changes to [Thing Descriptions](https://iot.mozilla.org/wot/#web-thing-description). This will bring us more in line with the latest [W3C drafts](https://www.w3.org/TR/wot-thing-description/).

One small difference to be aware of is that “name” is now called “[title](https://iot.mozilla.org/wot/#title-member)”. There are also some experimental new *base*, *security* and *securityDefinitions* properties of the Thing Descriptions exposed by the gateway, which are still under active discussion at the W3C.

## Give it a try!

We invite you to download the new [WebThings Gateway 0.9](https://iot.mozilla.org/gateway/) and continue to build your own web things with the latest [WebThings Framework](https://iot.mozilla.org/framework/) libraries. If you already have WebThings Gateway installed on a Raspberry Pi, it should update itself automatically.

As always, we welcome your feedback on [Discourse](https://discourse.mozilla.org/c/iot). Please submit issues and pull requests on [GitHub](https://github.com/mozilla-iot/).

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 5 comments

frenchfasoJuly 25th, 2019 at 11:07StarbeamrainbowlabsJuly 25th, 2019 at 15:33JoeyAugust 1st, 2019 at 11:50dwoodyAugust 2nd, 2019 at 18:13patchedsoulAugust 20th, 2019 at 06:33