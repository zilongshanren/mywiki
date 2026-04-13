---
title: Thermostats, Locks and Extension Add-ons – WebThings Gateway 0.10 – Mozilla
  Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/11/thermostats-locks-and-extension-add-ons-webthings-gateway-0-10/
author: Ben Francis
published: '2019-11-14'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Happy *Things Thursday*! Today we are releasing [WebThings Gateway 0.10](https://iot.mozilla.org/gateway/). If you have a gateway using our Raspberry Pi builds then it should already have automatically updated itself.

This new release comes with support for thermostats and smart locks, as well as an updated add-ons system including extension add-ons, which enable developers to extend the gateway user interface. We’ve also added localisation settings so that you can choose your country, language, time zone and unit preferences. From today you’ll be able to use the gateway in American English or Italian, but we’re already receiving contributions of translations in different languages!

## Thermostats

Version 0.10 comes with support for smart thermostats like the Zigbee [Zen Thermostat](https://zenecosystems.com/zenthermostat/), the [Centralite HA 3156105](https://centralite.com/) and the Z-Wave [Honeywell TH8320ZW1000](https://customer.honeywell.com/en-US/Pages/Product.aspx?cat=HonECC+Catalog&pid=TH8320ZW1000/U&category=Z-WaveTouchscreen&catpath=1.3.35.4.9).

You can view the current temperature of your home remotely, set a heating or cooling target temperature and set the current heating mode. You can also create rules which react to temperature or control your heating/cooling via the rules engine. In this way, you could set the heating to come on at a particular time of day or change the colour of lights based on how warm it is, for example.![Thermostat UI](../../assets/97039fb8e9bce614.png)


## Smart Locks

Ever wonder if you’ve forgotten to lock your front door? Now you can check when you get to work, and even lock or unlock the doors remotely. With the help of the rules engine, you can also set rules to lock doors at a particular time of day or notify you when they are unlocked.

So far we have support for Zigbee and Z-Wave smart locks like the [Yale YRD226 Deadbolt](https://www.yalehome.com/en/products/yale-assure-lock-and-levers/assure-lock/yrl-assurelock-touchscreen/) and [Yale YRD110 Deadbolt](https://www.amazon.com/Yale-Security-YRD110ZW0BP-Keyless-Deadbolt/dp/B00PM6TA9O/).

## Extension Add-ons

Version 0.10 also comes with a revamped add-ons system which includes a new type of add-on called extensions. Like a browser extension, an extension add-on can be used to augment the gateway’s user interface.

For example, an extension can add its own entry in the gateway’s main menu and display its own dedicated screen with new functionality.

Together with a new mechanism for add-on developers to extend the gateway’s REST API, this opens up a whole new world of possibilities for add-on developers to customise the gateway.![](../../assets/a2f59aef32a34bd6.png)


Note that the updated add-ons system comes with a new manifest format inspired by [Web Extensions](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions). Michael Stegeman’s blog post explains in more depth[ how to use the new add-ons system](https://hacks.mozilla.org/2019/11/ui-extensions-webthings-gateway/). We’ll walk you through building your own extension add-on.

## Localisation Settings

Many add-ons use location-specific data like weather, sunrise/sunset and tide times, but it’s no fun to have to configure your location for each add-on. It’s now possible to choose your country, time zone and language via the gateway’s web interface.

With time zone support, time-based rules should now correctly adjust for daylight savings time in your region. Since the gateway is configured to use Greenwich Mean Time by default, your rules may show times you didn’t expect at first. To fix this, you’ll need to set your time zone appropriately and adjust your rule times. You can also set your preference of unit used to display temperature, to either degrees Celsius or Fahrenheit.

And finally, many of you have asked for the user interface to support multiple languages. We are shipping with an Italian translation in this release thanks to our resident Italian speaker [Kathy](https://twitter.com/kgiori). We already have French, Dutch and Polish translations in the pipeline thanks to our wonderful community. Stand by for more information on how to contribute to translations in your language!

## API Changes & Standardisation

For developers, in addition to the new add-ons system, it’s now possible to communicate with all the gateway’s web things via a single WebSocket connection. Previously it was necessary to open a WebSocket per device, so this is a significant enhancement.

We’ve recently started the [Web Thing Protocol Community Group](https://www.w3.org/community/web-thing-protocol/) at the W3C with the intention of standardising this WebSocket sub-protocol in order to further improve interoperability on the [Web of Things](https://www.w3.org/WoT/). We welcome developers to join this group to contribute to the standardisation process.

## Coming Soon

Coming up next, expect [Mycroft](https://mycroft.ai/) voice controls, translations into more languages and new ways to install and use WebThings Gateway.

As always, you can head over to the [forums](https://discourse.mozilla.org/c/iot) for support. And we welcome your contributions on [GitHub](https://github.com/mozilla-iot/gateway).

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 8 comments

Krzysztof ZurekNovember 14th, 2019 at 11:53Ben FrancisNovember 14th, 2019 at 12:31Iulian ArionNovember 21st, 2019 at 05:20Iulian ArionNovember 21st, 2019 at 05:22Ben FrancisNovember 21st, 2019 at 06:34VladimirNovember 21st, 2019 at 18:05Ben FrancisNovember 22nd, 2019 at 04:46VladimirNovember 22nd, 2019 at 05:58