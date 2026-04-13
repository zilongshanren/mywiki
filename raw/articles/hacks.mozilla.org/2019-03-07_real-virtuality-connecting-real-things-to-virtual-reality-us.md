---
title: 'Real virtuality: connecting real things to virtual reality using web technologies
  – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2019/03/connecting-real-things-to-virtual-worlds-using-web/
author: Fabien Benetou
published: '2019-03-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is the story of our lucky encounter at FOSDEM, the largest free and open source software event in Europe. We are two developers, focused on different domains, who saw an opportunity to continue our technical conversation by building a proof of concept. Fabien Benetou is a developer focused on virtual reality and augmented reality. Phillipe Coval works on the Internet of Things. Creating a prototype gave the two of us a way to explore some ideas we’d shared at the conference.*

## WebXR meets the Web of Things

Today we’ll report on the proof-of-concept we built in half a day, after our lucky meeting-of-minds at FOSDEM. Our prototype applies 3D visualisation to power an IoT interface. It demonstrates how open, accessible web technologies make it possible to combine software from different domains to create engaging new interactive experiences.

Our proof of concept, illustrated in the video below, shows how a sensor connected to the Internet brings data from the real world to the virtual world. The light sensor reads colors from cardboard cards and changes the color of entities in virtual reality.

The second demo shows how actions in the virtual world can affect the real world. In this next video, we turn on LEDs with colors that match their virtual reality counterparts.

We’ll show you how to do a similar experiment yourself:

**Build a demo that goes from IoT to WoT**, showing the value of connecting things to the web.**Connect your first thing**and bring it online.**Make a connection between the Web of Things and WebXR**. Once your thing is connected, you’ll be able to display it, and**interact with it in VR and AR.**

Here’s a bit more of the context: [Fabien Benetou](https://fosdem.org/2019/schedule/speaker/fabien_benetou_@utopiah/) organized of the JavaScript devroom track at FOSDEM, and presented [High end augmented reality using JavaScript](https://fosdem.org/2019/schedule/event/machine_learning_javascript/). [Philippe Coval](https://fosdem.org/2019/schedule/speaker/philippe_coval/) from the [Samsung OpenSource group](https://www.slideshare.net/samsungosg) joined his colleague [Ziran Sun](https://fosdem.org/2019/schedule/speaker/ziran_sun/) to present [Bring JavaScript to the Internet of Things](https://fosdem.org/2019/schedule/event/js_iot_smart/) on the same track.

Philippe demonstrated a remote “SmartHome in a Box”, using a live webcam stream. It was a demo he’d shared the day before in the Mozilla devroom, in a joint [presentation](https://www.slideshare.net/rzrfreefr/mozillathingsfosdem2019) with Mozilla Tech Speaker [Dipesh Monga](https://fosdem.org/2019/schedule/speaker/dipesh_monga/).

The demo showed interactions of different kinds of sensors, including a remote sensor from the [OpenSenseMap](https://opensensemap.org/explore/5c3a9814c4c2f30019f679a1) project, a community website that lets contributors upload real-time sensor data.

### The Followup to FOSDEM

In Rennes, a city in Brittany, in the northwest of France, [the Ambassad’Air project](https://twitter.com/Ambassad_Air/status/1084775152330698754) is doing community air-quality tracking using [luftdaten](https://luftdaten.info/) software on super cheap microcontrollers. Fabien had already made plans to visit Rennes the following week (to breathe fresh air and enjoy local baked delicacies like the delightful [kouign amann](https://en.wikipedia.org/wiki/Kouign-amann)).

So we decided to meet again in [Rennes](https://en.wikipedia.org/wiki/Rennes), and involve the local community. We proposed a public workshop bridging “Web of Things” and “XR” using FLOSS. Big thanks to [Gulliver](http://gulliver.eu.org/), the local GNU/Linux Group, who offered to host our [last minute hacking session](http://gulliver.eu.org/calendrier:2019:02:09). Thanks also to the participants in Rennes for their curiosity and their valuable input.

In the sections ahead we offer an overview of the different concepts that came together in our project.

## From IoT to the Web of Things

The idea of the Internet of Things existed before it got its name. Some fundamental IoT concepts have a lot in common with the way the web works today. As the name suggests, the web of things offers an efficient way to connect any physical object to the world wide web.

Let’s start with a light bulb 💡. Usually, we use a physical switch to turn the bulb on or off. Now imagine if your light bulb 💡 could have its own web page.

If your light bulb or any smart device is web friendly, it would be reachable by a URL like `https://mylamp.example.local`. The light bulb vendor could implement a web server in the device, and a welcome page for the user. The manufacturer could provide another endpoint for a machine-readable status that would indicate “ON” or “OFF”. Even better, that endpoint could be read using an [HTTP GET](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET) query or set using an [HTTP POST](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST) operation with ON or OFF.

All this is simply an API to manage a boolean, making it possible to use the mobile browser as a remote control for the light bulb.

Although this model works, it’s not the best way to go. A standardized API should respect [REST](https://developer.mozilla.org/en-US/docs/Glossary/REST) principles and use common semantics to [describe Things (TD)](https://www.w3.org/TR/wot-thing-description/). The W3C is pushing for standardization — a smooth interoperable web language that can be implemented by any project, such as [Mozilla’s Project Things](https://iot.mozilla.org/).

Newcomers can start with a virtual adapter and play with simulated things. These things appear on the dashboard but do not exist in reality. Actuators or sensors can be implemented using web thing libraries for any language. Useful hint: it’s much simpler to practice on a simulator before working with real hardware and digging into hardware datasheets.

For curious readers, check out the IoT.js code in Philippe’s [webthings-iotjs guide](https://github.com/rzr/webthing-iotjs/wiki) on GitHub, and explore color sensor code that’s been published to NPM as [color-sensor-js](https://www.npmjs.com/package/color-sensor-js).

## Connect your first thing

How do you make a web-friendly smart home? You can start by setting up a basic local IoT network. Here’s how:

- You’ll need a a computer with a network interface to use as a gateway.
- Add devices to your network and define a protocol to connect them to the central gateway.
- Build a user interface to let the user control all connected devices from the gateway.
- Later you can develop custom web apps that can also connect to the gateway.

To avoid reinventing the wheel, look at existing free software. That’s where Mozilla’s Things Gateway comes in. You won’t need network engineering or electronics expertise to get started.

You can rely on a low-cost and low-power consumption single board computer, for instance the Raspberry Pi, to install the operating system image [provided by Mozilla](https://iot.mozilla.org/gateway). Then you can create virtual things like light bulbs, or connect real hardware like [sensors](https://github.com/rzr/mozilla-iot-generic-sensors-adapter) onto the gateway itself. You’ll be able to control your device(s) from the web through the tunneling service provided by the “things cloud”. Your data is reachable at a custom domain, stays on your local network, and is never sent to a 3rd party in the cloud.

In order to make the process efficient and also safe, the gateway takes care of authentication by generating a token. The gateway can also generate direct code snippets in several languages (including JavaScript) that can be used for [other applications](https://github.com/rzr/webthing-iotjs/wiki/WebApp):

You can build on top of existing code that should just work when you copy/paste it into your application. Developers can focus on exploring novel applications and use cases for the technology.

For your next step, we recommend testing the simplest example: list all the things connected to your gateway. In our example, we use a light bulb 💡, a thing composed of several properties. Make sure that the *thing* displayed on the gateway web interface matches the real world thing. Use the browser’s console with the provided code snippets to check that the behavior matches the device.

### Get to know your Things Gateway

Once this is running, the fun begins. Since you can access the gateway with code, you can:

- List all things, including the schema, to understand their capabilities (properties, values, available actions).
- Read a property value (e.g. the current temperature of a sensor).
- Change a property (e.g. control the actuator or set the light bulb color).
- Get the coordinates of a
*thing*on a 2D floor plan. - And much more!

Using a [curl](https://curl.haxx.se/) command, you can query the whole tree to identify all things registered by the gateway:

```
gateway=”https://sosg.mozilla-iot.org<
token=”B4DC0DE..."
curl \
-H "Authorization: Bearer $token" \
-H 'Accept: application/json' \
https://sosg.mozilla-iot.org/things \
| jq -M .
```


The result is a JSON structure of all the things. Each thing has a different endpoint like:

```
{
"name": "ColorSensor",
...
"properties": { "color": {
"type": "string",
"@type": "ColorProperty", "readOnly": true, "links": [ {...
"href": "/things/http---localhost-58888-/properties/color"
...
```


User devices are private and not exposed to the world wide web, so no one else can access or control your light bulb. Here’s a quick look at the REST architecture that makes this possible:

## From WoT to WebXR

### Introducing A-Frame for WebVR

Once we were able to programmatically get property values using a single HTTP GET request, we could use those values to update the visual scene, e.g. changing the geometry or color of a cube. This is made easier with a framework like [A-Frame](https://aframe.io/), which lets you describe simple 3D scenes using HTML.

For example, to define that cube in A-Frame, we use the <a-box></a-box> tag. Then we change its color by adding the color attribute.

`<a-box color="#00ff00">`


The beauty behind the declarative code is that these 3D objects, or entities, are described clearly, yet their shape and behavior can be extended easily with components. A-Frame has an active community of contributors. The libraries are open source, and built on top of [three.js](https://threejs.org/), one of the most popular 3D frameworks on the web. Consequently, scenes that begin with simple shapes can develop into beautiful, complex scenes.

This flexibility allows developers to work at the level of the stack where they feel comfortable, from HTML to writing components in JavaScript, to writing complex 3D [shaders](https://developer.mozilla.org/en-US/docs/Games/Techniques/3D_on_the_web/GLSL_Shaders). By staying within the boundaries of the core of A-Frame you might never even have to write JavaScript. If you want to write JavaScript, documentation is available to do things like [manipulating the underlying three.js object](https://aframe.io/docs/0.9.0/core/entity.html#object3d).

A-Frame itself is framework agnostic. If you are a React developer, you can rely on React. Prefer Vue.js? Not a problem. Vanilla HTML & JS is your thing? These all work. Want to use VR in data visualisation? You can let [D3](https://d3js.org/) handle the data bindings.

Using a framework like A-Frame which targets WebXR means that your <a-box> will work on all VR and AR devices which have access to a browser that supports WebXR, from the smartphone in your pocket to high-end VR and professional AR headsets.

### Connecting the Web of Things to Virtual Reality

In our next step we change the color value on the 3D object to the thing’s actual value, derived from its physical color sensor. Voila! This connects the real world to the virtual. Here’s the A-Frame component we wrote that can be applied to any A-Frame entity.

```
var token = 'Bearer SOME_CODE_FOR_AUTH'
// The token is used to manage access, granted only to selected users
var baseURL = 'https://sosg.mozilla-iot.org/'
var debug = false // used to display content in the console
AFRAME.registerComponent('iot-periodic-read-values', {
// Registering an A-Frame component later used in VR/AR entities
init: function () {
this.tick = AFRAME.utils.throttleTick(this.tick, 500, this);
// check for new value every 500ms
},
tick: function(t, dt){
fetch(baseURL + 'things/http---localhost-58888-/properties/color', {
headers: {
Accept: 'application/json',
Authorization: token
}
}).then(res => {
return res.json();
}).then(property => {
this.el.setAttribute("color", property.color);
// the request went through
// update the color of the VR/AR entity
});
}
})
```


The short video above shows real world color cards causing colors to change in the virtual display. Here’s a brief description of what we’re doing in the code.

- We generate a security token (JWT) to gain access to our Things Gateway.
- Next we register a component that can be used in A-Frame in VR or AR to change the display of a 3D entity.
- Then we fetch the property value of a Thing and display it on the current entity.

In the same way we can get information with an HTTP GET request, we can send a command with an HTTP PUT request. We use A-Frame’s <a-cursor> to allow for interaction in VR. Once we look at an entity, such as another cube, the cursor can then send an event. When that event is captured, a command is issued to the Things Gateway. In our example, when we aim at a green sphere (or “look” with our eyes through the VR headset), we toggle the green LED, red sphere (red LED) and blue sphere (blue LED).

### Going from Virtual Reality to Augmented Reality

The objective of our demo was two-fold: to bring real world data into a virtual world, and to act on the real world from the virtual world. We were able to display live sensor data such as temperature and light intensity in VR. In addition, were able to turn LEDs on and off from the VR environment. This validates our proof of concept.

Sadly, the day came to an end, and we ran out of time to try our proof of concept in augmented reality (AR) with a [Magic Leap](https://www.magicleap.com/) device. Fortunately, the end of the day didn’t end our project. Fabien was able to tunnel to Philippe’s demo gateway, registered under the `mozilla-iot.org` subdomain and access it as if it were on a local network, using Mozilla’s remote access feature.

The project was a success! We connected the real world to AR as well as to VR.

The augmented reality implementation proved easy. Aside from removing `<a-sky>`

; so it wouldn’t cover our field of view, we didn’t have to change our code. We opened our existing web page on the [MagicLeap ML1](https://en.wikipedia.org/wiki/Magic_Leap) thanks to [exokit](https://github.com/webmixedreality/exokit), a new open-source browser specifically targeting spatial devices (as presented during Fabien’s FOSDEM talk). It just worked!

As you can see in the video, we briefly reproduced the gateway’s web interface. We have a few ideas for next steps. By making those spheres interactive we could activate each thing or get more information about them. Imagine using the gateway floorplan to match the spatial information of a thing to the physical layout of a flat. There are A-Frame components that make it straightforward to generate simplified building parts like walls and doors.

You don’t need a Magic Leap device to explore AR with the Web of Things. A smartphone running [Mozilla XR Viewer](https://github.com/mozilla-mobile/webxr-ios) on an iPhone or an Android using the [experimental build of Chromium](https://github.com/google-ar/WebARonARCore) will work with traditional RGB cameras.

### From the Virtual to the Immersive Web

The transition from VR/AR to XR takes two steps. The first step is the technical aspect, which is where relying on A-Frame comes in. Although the specifications for VR and AR on the web are still works in progress by the [W3C’s “Immersive Web” standardization process](https://github.com/immersive-web), we can target XR devices today.

By using a high-level framework, we can begin development even though the spec is still in progress, because the spec includes a polyfill maintained by browser vendors and the community at large. The promise of having one code base for all VR and AR headsets is one of the most exciting aspects of WebXR. Using A-Frame, we are able to start today and be ready for tomorrow.

The second step involves you, as reader and user. What would you like to see? Do you have ideas of use cases that create interactive spatial content for VR and AR?

## Conclusion

The hack session in Rennes was fascinating. We were able to get live data from the real world and interact with it easily in the virtual world. This opens the door to many possibilities: from our simplistic prototype to artistic projects that challenge our perception of reality. We also foresee pragmatic use cases, for instance in hospitals and laboratories filled with sensors and modern instrumentation (IIoT or Industrial IoT).

This workshop and the resulting videos and code are simple starting points. If you start work on a similar project, please do get in touch ([@utopiah](https://twitter.com/utopiah/) and [@rzr@social.samsunginter.net](https://social.samsunginter.net/@rzr/)/[@RzrFreeFr](https://twitter.com/RzrFreeFr/)). We’ll help however we can!

There’s also work in progress on a [webapp to A-Frame](https://github.com/samsunginternet/webthings-webapp). Want to get involved in testing or reviewing code? You’re invited to [help with the design or suggest some ideas of your own](https://github.com/SamsungInternet/webthings-webapp/issues/).

What Things will YOU bring to the virtual world? We can’t wait to hear from you.

## Resources

- Meeting page (in French):

[http://gulliver.eu.org/calendrier:2019:02:09](http://gulliver.eu.org/calendrier:2019:02:09) - PoC sources (kind of documented and tested but still very basic):

[http://gulliver-webxr-iot.glitch.me/](http://gulliver-webxr-iot.glitch.me/)

[https://glitch.com/edit/#!/gulliver-webxr-iot](https://glitch.com/edit/#!/gulliver-webxr-iot) - Video about: WebThing Sensor to VR + VR Actuators (LEDs)
[https://social.samsunginter.net/@rzr/101564201618024415](https://social.samsunginter.net/@rzr/101564201618024415) - Guide to build webthings using IoT.js and more:

[https://github.com/rzr/webthing-iotjs/wiki](https://github.com/rzr/webthing-iotjs/wiki) - Sensor color driver for IoT.js or Node.js:

[https://www.npmjs.com/package/color-sensor-js](https://www.npmjs.com/package/color-sensor-js)

[https://github.com/rzr/color-sensor-js/](https://github.com/rzr/color-sensor-js/) - Using objects in the real world from a virtual reality setup:

[https://youtu.be/sPaSd1eRTGE](https://youtu.be/sPaSd1eRTGE) - Activating objects in the real world from a virtual reality setup:

[https://youtu.be/-kSUS4yeJBk](https://youtu.be/-kSUS4yeJBk) - Getting live IoT sensor data straight to augmented reality:

[https://www.youtube.com/watch?v=5XaD6eS6OUE](https://www.youtube.com/watch?v=5XaD6eS6OUE) - Reality Editor 2.0 (earlier exploration):
[https://www.media.mit.edu/projects/reality-editor-20/overview/](https://www.media.mit.edu/projects/reality-editor-20/overview/) - Where brain, body, and world collide:

[https://www.sciencedirect.com/science/article/pii/S1389041799000029](https://www.sciencedirect.com/science/article/pii/S1389041799000029) - Isolated A-Frame component (to be updated once schema implemented):

[https://github.com/Utopiah/aframe-webthings-component](https://github.com/Utopiah/aframe-webthings-component) - Webthing-Webapp (experimental PWA supporting various UI toolkits, Tizen etc)

[https://github.com/samsunginternet/webthings-webapp](https://github.com/samsunginternet/webthings-webapp)