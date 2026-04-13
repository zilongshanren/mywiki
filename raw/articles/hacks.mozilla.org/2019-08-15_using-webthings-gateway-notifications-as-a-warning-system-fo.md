---
title: Using WebThings Gateway notifications as a warning system for your home – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/08/using-webthings-gateway-notifications-as-a-warning-system-for-your-home/
author: James Hobin
published: '2019-08-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Ever wonder if that leaky pipe you fixed is holding up? With a trip to the hardware store and a Mozilla WebThings Gateway you can set up a cheap leak sensor to keep an eye on the situation, whether you’re home or away. Although you can look up detector status easily on the web-based dashboard, it would be better to not need to pay attention unless a leak actually occurs. In the [WebThings Gateway 0.9 release](https://hacks.mozilla.org/2019/07/webthings-gateway-for-wireless-routers/), a number of different notification mechanisms can be set up, including emails, apps, and text messages.

### Leak Sensor Demo


In this post I’ll show you how to set up gateway notifications to warn you of changes in your home that you care about. You can set each notification to one of three levels of severity–low, normal, and high–so that you can identify which are informational changes and which alerts should be addressed immediately (fire! intruder! leak!). First, we’ll choose a device to worry about. Next, we’ll decide how we want our gateway to contact us. Finally, we’ll set up a rule to tell the gateway when it should contact us.

## Choosing a device

First, make sure the device you want to monitor is connected to your gateway. If you haven’t added the device yet, visit the [Gateway User Guide](https://iot.mozilla.org/docs/gateway-user-guide.html) for information about getting started.

Now it’s time to figure out which things’ properties will lead to interesting notifications. For each thing you want to investigate, click on its *splat* icon to get a full view of all its properties.

- Things List

- Detailed Leak Sensor view

You may also want to log properties of various analog devices over time to see what values are “normal”. For example, you can monitor the refrigerator temperature for a couple of days to help determine what qualifies as an abnormal temperature. In this graph, you can see the difference between baseline power draw (around 20 watts) and charging (up to 90 watts).

In my case, I’ve selected a leak sensor so I won’t need to log data in advance. It’s pretty clear that I want to be notified when the leak property of my sensor becomes true (i.e., when a leak is detected). If instead you want to monitor a smart plug, you can look at voltage, power, or on/off state. Note that the notification rules you create will let you combine multiple inputs using “and” or “or” logic. For example, you might want to be alerted if indoor motion is detected “and” all of the family smartphone “presence” states are “inactive” (i.e., no one in your family is home, so what caused motion?). Whatever your choice, keep the logical states of your various sensors in mind while you set up your notifier.

## Setting up your notifier

The 0.9 WebThings Gateway release added support for notifiers as a specific form of add-on. Thanks to the efforts of the community and a bit of our own work, your gateway can already send you notifications over email, SMS, Telegram, or specialized push notification apps with new add-ons released every week. You can find several notification add-on options by clicking “+” on the Settings > Add-ons page.

- How to get to Settings

- How to get to Add-ons

- Installed add-ons list without email sender

- List of installable add-ons

- The author name links to the README on GitHub

The easiest-to-use notifiers are email and SMS since there are fewer moving parts, but feel free to choose whichever approach you prefer. Follow the configuration instructions in your chosen notifier’s README file. You can get to the README for your notifier by clicking on the author’s name in the add-on list then scrolling down.

You’ll find a complete guide to the email notifier here: [https://github.com/mozilla-iot/email-sender-adapter#email-sender-adapter](https://github.com/mozilla-iot/email-sender-adapter#email-sender-adapter).

## Creating a rule

Finally, let’s teach our gateway how and when it should yell for attention. We can set this up in a simple drag-and-drop rule. First, drag your device to the left as a trigger and select the “Leak” property.

- Drag and drop the Leak Sensor block into the rule

- Now select the property

- Configuring the leak block

Next, drag your notification channel to the right as an effect and configure its title, body, and level as desired.

- Dropping email block into the rule

- Email block dropped in

- Configuring Email

Your rule is now set up and ready to go!

You can now manually test it out. For a leak sensor you can just spill a little water on it to make sure you get a text, email, or other notification warning you about a possible scary flood. This is also a perfect time to start experimenting. Can you set up a second, louder notification for when you’re asleep? What about only notifying when you’re at home so you can deal with the leak immediately?

Notifications are just one small piece of the WebThings Gateway ecosystem. We’re trying to build a future where the convenience of a connected life doesn’t require giving up your security and privacy. If you have ideas about how the WebThings Gateway can better orchestrate your home, please comment on [Discourse](https://discourse.mozilla.org/c/iot) or contribute on [GitHub](https://github.com/mozilla-iot/gateway/). If your preferred notification channel is missing and you can code, we love community add-ons! Check out the [source code of the email add-on](https://github.com/mozilla-iot/email-sender-adapter/) for inspiration. Coming up next, we’ll be talking about how you can have a natural spoken dialogue with the WebThings Gateway without sending your voice data to the cloud.

## About
[
James Hobin ](https://hobinjk.github.io/)

Level 25 Computer Wizard on a quest to keep the Internet of Things free and open.

## 3 comments

KristianAugust 19th, 2019 at 12:20Jamison CurryAugust 20th, 2019 at 22:03ThecarekartSeptember 2nd, 2019 at 23:36