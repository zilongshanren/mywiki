---
title: WebThings Gateway Goes Global – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/02/webthings-gateway-goes-global/
author: Michael Stegeman
published: '2020-02-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today, we’re releasing version 0.11 of the WebThings Gateway. For those of you running a previous version of our Raspberry Pi build, you should have already received the update. You can check in your UI by navigating to *Settings ➡ Add-ons*.

# Translations and Platforms

The biggest change in this release is our ability to reach new WebThings Gateway users who are not native English speakers. Since the release of 0.10, our incredible community has contributed 24 new language translations via [Pontoon](https://pontoon.mozilla.org/projects/webthings-gateway/), Mozilla’s localization platform, with even more in the works! If your native (or favorite) language is still not available, we would love to have you contribute a translation.

Users are also now able to install WebThings Gateway in even more ways. We have packages for several Debian, Ubuntu, and Fedora Linux versions available on our [releases page](https://github.com/mozilla-iot/gateway/releases/tag/0.11.0). In addition, there is a package for Arch Linux available on the [AUR](https://aur.archlinux.org/packages/webthings-gateway/). All of these packages complement our existing [Raspberry Pi](https://github.com/mozilla-iot/gateway/releases/tag/0.11.0) and [Docker](https://hub.docker.com/r/mozillaiot/gateway) images.

# Experiments

In this release, we’ve made some changes to our two active experiments.

First, the logs experiment has been promoted! It is now a first-class citizen, enabled for all users. Logging allows you to track changes in property values for your devices over a time period, using interactive graphs.

In other news, we’ve decided to say goodbye to our experimental voice-based virtual assistant. While this was a fun experiment, it was never a practical feature. In our 0.12 release, the back-end commands API, which was used by the virtual assistant, will also be removed, so applications using that interface will need to be updated. Our preferred approach going forward is to have add-ons use the Web Thing API for everything, including voice interactions. Fear not, though. In addition to our Mycroft skill, people in the WebThings community have created multiple add-ons to allow you to interface with your gateway via voice, which are available for installation through *Settings ➡ Add-ons*.

# Miscellaneous

In addition to the notable changes above, there are a host of other updates.

- Users of our Raspberry Pi image can now disable automatic OTA (over the air) updates, if they so choose.
- Users can now access the web interface on their local network via http://, so that they’re not faced with an ugly, scary security warning each time.
- The Progressive Web App (PWA) should be much more stable and reliable now.
- As always, there have been numerous bug fixes.

# What Now?

We invite you to download the new[ WebThings Gateway 0.11 release](https://iot.mozilla.org/gateway/) and continue to build your own web things with the latest[ WebThings Framework](https://iot.mozilla.org/framework/) libraries. If you already have WebThings Gateway installed on a Raspberry Pi, you can expect the Gateway to be automatically updated.

As always, we welcome your feedback on[ Discourse](https://discourse.mozilla.org/c/iot). Please submit issues and pull requests on[ GitHub](https://github.com/mozilla-iot/). You can also now chat with us directly on [Matrix](https://chat.mozilla.org/), in #iot.

## About
[
Michael Stegeman ](https://github.com/mrstegeman)

Michael is a software engineer at Mozilla working on WebThings.

## 2 comments

Krzysztof ZurekFebruary 20th, 2020 at 11:13Upasna DixitFebruary 20th, 2020 at 18:46