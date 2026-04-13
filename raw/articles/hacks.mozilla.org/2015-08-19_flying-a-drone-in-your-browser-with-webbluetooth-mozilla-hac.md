---
title: Flying a drone in your browser with WebBluetooth – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2015/08/flying-a-drone-in-your-browser-with-webbluetooth/
author: Jan Jongboom
published: '2015-08-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

There are tons of devices around us, and the number is only growing. And more and more of these devices come with connectivity. From [suitcases](http://bluesmart.com/) to [plants](http://www.parrot.com/usa/products/flower-power/) to [eggs](http://www.amazon.com/Minder-Wink-App-Enabled-Smart-Tray/dp/B00GN92KQ4). This brings new challenges: how can we discover devices around us, and how can we interact with them?

Currently device interactions are handled by separate apps running on mobile phones. But this does not solve the discoverability issue. I need to know which devices are around me before I know which app to install. When I’m standing in front of a [meeting room](http://blog.telenor.io/iot/2015/08/04/smart-meetingroom.html) I don’t care about which app to install, or even what the name or ID of the meeting room is. I just want to make a booking or see availability, and as fast as possible.

## Bluetooth

[Scott Jenson](https://twitter.com/scottjenson) from Google has been thinking about discoverability for a while, and came up with the [ Physical Web](https://google.github.io/physical-web/) project, whose premise is:

Walk up and use anything


The idea is that you use [Bluetooth Smart](http://www.bluetooth.com/Pages/Bluetooth-Smart.aspx), the low energy variant of bluetooth, to broadcast URLs to the world. Your phone picks up the advertisment package, decodes it, and shows some information to the user. One click and the user is redirected to a web page with relevant content. This can be used for a variety of things:

- A meeting room can broadcast a URL to its calendar for scheduling.
- A movie poster can broadcast a URL to show viewing times and trailers.
- A prescription medicine can broadcast a URL with information about the medication or how to refill it.
- Look around you. Examples of other use cases are everywhere, waiting to be implemented.

However, the material world is not a one-way street, and this presents a problem. Broadcasting a URL is great for informing me about things like movie times, but it does not allow me to interact more deeply with the device. If I want to fly a [drone](http://www.parrot.com/usa/products/rolling-spider/) I don’t just want to discover that there’s a drone near me, I also want to interact with the drone straight away. We need to have a way for web pages to communicate back to devices.

Enter the work of the [Web Bluetooth W3C group](https://www.w3.org/community/web-bluetooth/), that includes representatives of Mozilla’s [Bluetooth team](https://wiki.mozilla.org/B2G/Bluetooth), who are working on bringing bluetooth APIs to the browser. If the *Physical Web* allows us to walk up to any device and get the URL of a web app, then WebBluetooth allows the web app to connect to the device and talk back to it.

At this point, there’s still a lot of work to be done. The bluetooth API is only exposed to [certified content](https://developer.mozilla.org/en-US/Firefox_OS/Security/Security_model) on Firefox OS, and thus is not currently accessible to ordinary web content. Until security issues [have been cleared](https://bugzilla.mozilla.org/show_bug.cgi?id=1053673) this will continue to be the case. A second issue is that *Physical Web* beacons broadcast a URL. How can a specific web resource know which specific device has broadcast the URL?

As you can see, lots of work remains to be done, but this blog is called Mozilla Hacks for a reason. Let’s start hacking!

## Adding *Physical Web* support to Firefox OS

Since most of the work around WebBluetooth has been done for Firefox OS, I’ve made it my weapon of choice. I want the process of discovering devices to be as painless and obvious as possible. I figured the lockscreen would be the best possible place. Whenever you have bluetooth enabled on your Firefox OS phone, a new notification would then pop up asking you to search for devices ([tracking bug](https://bugzilla.mozilla.org/show_bug.cgi?id=1196233)).

![Tap, tap, tap](../../assets/fac3b73ede6da78d.png)


```
navigator.mozBluetooth.defaultAdapter.startLeScan([]).then(handle => {
handle.ondevicefound = e => {
console.log('Found', e.device, e.scanRecord);
};
setTimeout(() => {
navigator.mozBluetooth.defaultAdapter.stopLeScan(handle)
}, 5000);
}, err => console.error(err));
```


As you can see on the third line, we have a `scanRecord`

. This is the advertisement package that the device broadcasts. It’s nothing more than a set of bytes, and you are free to declare your own protocol. For our purpose—broadcasting URLs over bluetooth—Google has already developed two ways of encoding: [UriBeacon](https://github.com/google/uribeacon) and [EddyStone](https://github.com/google/eddystone), both of which can be found in the wild today.

Parsing the advertisement package is pretty straightforward. Here’s some code I wrote to [parse UriBeacons](https://gist.github.com/janjongboom/78f6e45bc3b4133193ff). Parsing the UriBeacon will give you a URL, which is often shortened, because of limited bytes in the advertisement package —this makes for an uninformative UI:

![So what the hack (pun intended) is this device?](../../assets/47d4e1594ec2b7da.png)


To get some information about the web page behind the beacon we can do an AJAX request and parse the content of the page to enhance the information displayed on the lockscreen:

```
function resolveURI(uri, ele) {
var x = new XMLHttpRequest({ mozSystem: true });
x.onload = e => {
var h = document.createElement('html');
h.innerHTML = x.responseText;
// After following 301/302s, this contains the last resolved URL
console.log('url is', x.responseURL);
var titleEl = h.querySelector('title');
var metaEl = h.querySelector('meta[name="description"]');
var bodyEl = h.querySelector('body');
if (titleEl && titleEl.textContent) {
console.log('title is', titleEl.textContent);
}
if (metaEl && metaEl.content) {
console.log('description is', metaEl.content);
}
else if (bodyEl && bodyEl.textContent) {
console.log('description is', bodyEl.textContent);
}
};
x.onerror = err => console.error('Loading', uri, 'failed', err);
x.open('GET', uri);
x.send();
};
```


This yields a nicer notification that actually describes the beacon.

![Much nicer](../../assets/c1d5a2addb9107fd.png)


### A drone that doesn’t broadcast a URL

Unfortunately not all BLE devices broadcast URLs at this point. All of this new technology is experimental and very cool, but not yet fully implemented. We’ve got high hopes that this will change in the near future. Because I still want to be able to fly my drone now, I added some code that transforms the data a drone broadcasts [into a URL](https://github.com/comoyo/gaia/blob/physical_web/apps/system/lockscreen/js/lockscreen_physical_web.js#L126).

## The web application

Now that we’ve solved the issue of discoverability, we need a way to control the drone from the browser. Since bluetooth access is not available for web content, we need to make some changes to Gecko, where the Firefox OS security model is implemented. If you are interested in the changes, [here’s the commit](https://github.com/jan-os/gecko-dev/commit/4c80faf0e48ebad1346ca9fcdbada18a6a276e6d). We also needed a [sneaky hack](https://github.com/comoyo/gaia/commit/d823f61994ded5fdb7259bf965ba82b7746a2db9) to make sure the tab’s process is run with the right Linux permissions.

With these changes in place, we open up `navigator.mozBluetooth`

to all content, and run every tab in Firefox in a process that is part of the ‘bluetooth’ Linux group, ensuring access to the hardware. If you’re playing around with this build later, please note that with my “sneaky” hack implemented, you are now running a build where no security is guaranteed. Using a build hack like this, with security disabled, is fine for IoT experimentation, but is definitely **not recommended** as a production solution. When the Web Bluetooth spec is finalized, and official support lands in Gecko, proper security [will be implemented](https://bugzilla.mozilla.org/show_bug.cgi?id=1053673).

With the API in place, we can start writing the application. When you tap on the *Physical Web* notification on the lockscreen, we pass the device address in as a parameter. This is subject to change. For the ongoing discussion take a look at the [Eddystone -> Web Bluetooth handoff](https://docs.google.com/document/d/1jFCTyq84T2fLc8ZhxorTz3u_gCk59hp17EmkFgaDQ2c/edit).

```
var address = 'aa:bb:cc:dd:ee'; // parsed from URL
var counter = 0;
navigator.mozBluetooth.defaultAdapter.startLeScan([]).then(handle => {
handle.ondevicefound = e => {
if (e.device.address !== address) return;
navigator.mozBluetooth.defaultAdapter.stopLeScan(handle);
// write some code to fly the drone
};
}, err => console.error(err));
```


Now that we have a reference to the device address, we can set up a connection. The protocol we use to talk back and forth to the device is called [GATT](https://www.safaribooksonline.com/library/view/getting-started-with/9781491900550/ch04.html), the Generic Attribute Profile. The idea behind GATT is that a device can have multiple standard services. For example, a heart rate sensor can implement the battery service and the heart rate service. Because these services are standardized, a consuming application only needs to write the implementation logic once, and can talk to any heart rate monitor.

Characteristics are aspects of a given service. For example, a heart rate service will implement [heart rate measurement](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml) and [heart rate max](https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_max.xml). Characteristics can be readable and writeable depending on how they are defined. This goes the same with the drone. It has a service for flying the drone and characteristics to let you control the drone from your phone.

Luckily [Martin Dlouhý](http://robotika.cz/robots/jessica/en) (as far as I can tell, he was the first) has already decoded the communication protocol for the Rolling Spider drone, so we can use his work and the new Bluetooth API to start flying…

```
// Have a way of knowing when the connection drops
e.device.gatt.onconnectionstatechanged = cse => {
console.log('connectionStateChanged', cse);
};
// Receive events (battery change f.e.) from device
e.device.gatt.oncharacteristicchanged = cce => {
console.log('characteristicChanged', cce);
};
// Set up the connection
e.device.gatt.connect().then(() => {
return e.device.gatt.discoverServices();
}).then(() => {
// devices have services, and services have characteristics
var services = e.device.gatt.services;
console.log('services', services);
// find the characteristic that handles flying the drone
var c = services.reduce((curr, f) => curr.concat(f.characteristics), [])
.filter(c => c.uuid === '9a66fa0b-0800-9191-11e4-012d1540cb8e')[0];
// take off instruction!
var buffer = new Uint8Array(0x04, counter++, 0x02, 0x00, 0x01, 0x00]);
c.writeValue(buffer).then(() => {
console.log('take off successful!');
});
});
```


The Mozilla team in Taipei used this to create a [demo application](https://github.com/fxos-bt-squad/RollingSpider) for Firefox OS, demonstrating the capabilities of the new API during the Mozilla Work Week in Whistler last June. With the API now available in the browser, we can take that work, [host it as a web page](https://github.com/janjongboom/rollingspider.xyz), beef up the graphics a bit, and have a *web site* flying a drone!

![Such amaze](../../assets/80d018114c7121f3.png)


*Such amaze. Much drone.*

## Conclusion

It’s an exciting time for the Web! With more and more devices coming online we need a way to discover and interact with them without much hassle. The combination of *Physical Web* and WebBluetooth allows us to create frictionless experiences for users willing to interact with real-world appliances and new devices. Although we’re a long way off, we’re heading in the right direction. Google and Mozilla are actively developing the technology; I’ve got high hopes that everything in this blog post will be common knowledge in a year!

If that’s not fast enough for you, you can play around with an experimental build of Firefox OS which enables everything seen in this post. This build runs on the [Flame](https://developer.mozilla.org/en-US/Firefox_OS/Developer_phone_guide/Flame) developer device. First, upgrade to [nightly_v3 base image](https://developer.mozilla.org/en-US/Firefox_OS/Phone_guide/Flame/Updating_your_Flame), then flash [this build](http://rollingspider.xyz/bt-flame.zip).

### Attributions

Thanks to [Tzu-Lin Huang](https://github.com/dwi2) and [Sean Lee](https://github.com/weilonge) for building the initial drone code; the WebBluetooth team in Mozilla Taipei (especially [Jocelyn Liu](https://github.com/yrliou)) for quick feedback and patches when I complained about the API; [Chris Williams](https://twitter.com/voodootikigod) for putting the drone in my JSConf.us gift bag; [Scott Jenson](https://twitter.com/scottjenson) for answering my numerous questions about the *Physical Web*; and [Telenor Digital](http://telenordigital.com/) for letting me play with drones for two weeks.

## About
[
Jan Jongboom ](http://janjongboom.com)

Jan Jongboom is a Strategic Engineer for Telenor Digital, working on IoT.

## 3 comments

Mindaugas J.August 20th, 2015 at 02:00Jan JongboomAugust 28th, 2015 at 05:36matt holevinskiAugust 30th, 2015 at 07:55