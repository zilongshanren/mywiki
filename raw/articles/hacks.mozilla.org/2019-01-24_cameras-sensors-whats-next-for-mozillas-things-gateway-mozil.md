---
title: Cameras, Sensors & What’s Next for Mozilla’s Things Gateway – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2019/01/cameras-sensors-whats-next-for-mozillas-things-gateway/
author: Ben Francis
published: '2019-01-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today the [Mozilla IoT](https://iot.mozilla.org) team is happy to announce the 0.7 release of the [Things Gateway](https://iot.mozilla.org/gateway/). This latest release brings experimental support for IP cameras, as well as support for a wider range of sensors. We’ve also got some exciting news on where the project is heading next.

## Camera Support

With 0.7, you can now view video streams and get snapshots from IP cameras which follow the [ONVIF](https://www.onvif.org/) standard such as the [Foscam R2](https://www.foscam.com/R2.html).

To enable ONVIF support, install the ONVIF add-on via Settings > Add-ons in the gateway’s web interface.![](../../assets/d18ce3d2e8a7a132.png)


Set up your camera as per the manufacturer’s instructions, including a username and password if it’s required. (Always remember to change from the default if there is one!) Then, you can click the “Configure” button on the ONVIF add-on (see above) to enter your login details in the form shown below:![](../../assets/7503a39983f28962.png)


Once the adapter is configured you should be able to add your device in the usual way, by clicking on the + button on the Things screen. When your camera appears you can give it a name before saving it:![](../../assets/facfa1e40dce5d8e.png)


When you click on the video camera you will see icons for an image snapshot and/or video stream:![](../../assets/e9bdd266a6bb0510.png)


Click on the icons and the image or video stream will pop up on the screen. When viewing an image property, you can click the reload button in the bottom left to reload the latest snapshot:![](../../assets/da8f671cf63db543.png)


Video camera support is still experimental at this point as we look to optimise video performance, refine the UI and support a wider range of hardware. If running on the Raspberry Pi you can expect to see a noticeable delay on video streams as it transcodes video into a web friendly format. We’d appreciate your help testing with different cameras and giving us feedback to help improve this feature.![](../../assets/ef28d2ed28ab2770.png)


## Sensors

Things Gateway 0.7 also comes with support for a wider range of sensors.

We have added support for temperature sensors (e.g. ![](../../assets/de7af37f19d42852.png)


[Eve Degree](https://www.evehome.com/en/eve-degree),

[Eve Room](https://www.evehome.com/en/eve-room)and the

[SmartThings Multipurpose sensor](https://www.smartthings.com/uk/products/smartthings-multipurpose-sensor)).

And we have added support for leak sensors (e.g. the ![](../../assets/b4ca6de6503211fd.png)


[SmartThings Water Leak Sensor](https://www.smartthings.com/uk/products/smartthings-water-leak-sensor)and the

[Fibaro Flood Sensor](https://www.fibaro.com/en/products/flood-sensor/)).

This means you can also now create new types of rules in the rules engine, for example to turn on a fan when temperature reaches a certain level, or be notified if a leak is detected.

## Thing Description Changes

For developers, this release brings some changes to the [Thing Description](https://iot.mozilla.org/wot/#web-thing-description) format used to advertise the properties, actions, and events web things support.

Rather than providing a single URL in an `href`

member, each [ Property](https://iot.mozilla.org/wot/#property-object),

[and](https://iot.mozilla.org/wot/#action-object)

`Action`

[object can now provide an array of links with an](https://iot.mozilla.org/wot/#event-object)

`Event`

`href`

, `rel`

and `mediaType`

for each [object. This is particularly useful for the new](https://iot.mozilla.org/wot/#link-object)

`Link`

[and](https://iot.mozilla.org/schemas/#Camera)

`Camera`

[capabilities, which can provide links to an image resource or video stream. Below is an example of a Thing Description for a video camera that supports both new capabilities.](https://iot.mozilla.org/schemas/#VideoCamera)

`VideoCamera`

```
{
"@context": "https://iot.mozilla.org/schemas/",
"@type": ["Camera", "VideoCamera"],
"name": "Web Camera",
"description": "My web camera",
"properties": {
"video": {
"@type": "VideoProperty",
"title": "Stream",
"links": [{
"href": "rtsp://example.com/things/camera/properties/video.mp4",
"mediaType": "video/mp4"
}]
},
"image": {
"@type": "ImageProperty",
"title": "Snapshot",
"links": [{
"href": "http://example.com/things/camera/properties/image.jpg",
"mediaType": "image/jpg"
}]
}
}
}
```


You may also notice that `label`

has been renamed to `title`

to be more in line with the latest [W3C draft of the Thing Description specification](https://w3c.github.io/wot-thing-description/).

We make an effort to retain backwards compatibility where possible, but please expect more changes like this as we rapidly evolve the Thing Description specification.

## What’s Next

We’ve been delighted with the response we’ve seen to Project Things from hacker and maker communities in 2018. Thank you so much for all the contributions you’ve made in reporting bugs, implementing new features and building your own adapter add-ons and web things. Also thanks to you, a [Project Things tutorial](https://hacks.mozilla.org/2018/02/how-to-build-your-own-private-smart-home-with-a-raspberry-pi-and-mozillas-things-gateway/) on Mozilla Hacks was our [most read blog post of 2018](https://hacks.mozilla.org/2018/12/mozilla-hacks-10-most-read-posts-of-2018/)!

Taking things (pun intended) to the next level in 2019, a big focus for our team will be to evolve the current Things Gateway application into a software distribution for wireless routers. By integrating all the smart home features we have built directly into your wireless router, we believe we can provide even more value in the areas of family internet safety and home network health.![](../../assets/8cd21536a2a26e5d.png)


In 2019, you can expect to see more effort go into the [OpenWrt](https://openwrt.org/) port of the Things Gateway to create our very own software distribution for “smart routers” which integrate smart home capabilities. We’ll start with new features for configuring your gateway as a wireless access point and all of the other features you’d expect from a wireless router. We anticipate many more new features to emerge as we develop this distribution, and explore all the value that a Mozilla trusted personal agent for your whole home network could provide.

We will keep generating Raspberry Pi builds of our ongoing quarterly releases for the foreseeable future, because that’s what most of our current users are using and that plucky little developer board is still close to our hearts. But look out for support for new hardware platforms coming soon.

For now, you can download the new [0.7 release](https://iot.mozilla.org/gateway/) from our website. If you have a Things Gateway already set up on a Raspberry Pi it should update itself automatically.

Happy hacking!

## About
[
Ben Francis ](http://tola.me.uk)

Former Mozilla Software Engineer. W3C Invited Expert on Web Applications and the Web of Things.

## 2 comments

Julien MoorsFebruary 21st, 2019 at 02:02Ben FrancisFebruary 22nd, 2019 at 03:11