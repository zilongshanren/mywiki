---
title: Multi-user experiences with A-Frame – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/10/multi-user-experiences-with-a-frame/
author: Salva
published: '2017-10-02'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Multi-user experiences on the Internet have come a long way since the emergence of online chat and the rise of social networks. Advances in virtual reality are making the Web a more immersive and interactive environment. Neal Stephenson envisioned this set of shared, persistent, and interconnected 3D virtual spaces and called it the *metaverse*; today we are building it with HTML, JavaScript, and A-Frame.

Given the gentle learning curve of HTML, [A-Frame](https://aframe.io) is the perfect choice for those who want to create virtual spaces on the Web with a few lines of HTML and JavaScript. With the implementation of [link-traversal](https://blog.mozvr.com/link-traversal/) by browsers, we are a step closer to teleporting from one experience to another without commuting in the real world. However, a collaboration model to facilitate information exchange between the inhabitants of the metaverse is still missing. WebRTC plays a key role in enabling this exchange.

## Peer-To-Peer communications with WebRTC

[WebRTC](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API) is a Web API, present in the [majority of browsers](http://caniuse.com/#feat=rtcpeerconnection) (including Safari as of this September), that allows the interchange of information without intermediaries, in a peer-to-peer fashion. With WebRTC, it is possible to implement the necessary infrastructure for persisting the experiences integrating the metaverse.

The biggest complexity of WebRTC arises from [session management, peer discovery and signaling](https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Connectivity), all necessary to identify the connections between browsers. Once peer identities have been established, the standard can provide end-to-end channels for sharing media and data.

## The `sharedspace`

component

To bring the power of WebRTC to A-Frame users, I’ve been developing the [ sharedspace](https://github.com/delapuente/aframe-sharedspace-component) component. The component provides a collaboration model where participants can join or leave a named space, share audio and state, and send JSON-serializable objects to other peers.

The component does not deal with the WebRTC API directly. Instead, it uses a [modified version](https://github.com/delapuente/webrtc-swarm) of [ webrtc-swarm](https://github.com/mafintosh/webrtc-swarm) as a wrapper library. I chose it for its simplicity, footprint, clarity of the source code, and ease of use.

You can experiment with some [VR chat on Glitch](https://vr-chat.glitch.me/) or [browse the project](https://glitch.com/edit/#!/vr-chat?path=README.md:1:0) to learn more about the `sharedspace`

component. The repository includes [extensive documentation](https://github.com/delapuente/aframe-sharedspace-component/tree/master/dist#component-overview) with explanations and examples of other common use cases.

The `sharedspace`

component is not a general network solution for A-Frame and it does not come with a straightforward way of sharing entities among multiple instances of an application. However, the ability to send data means it’s possible to create new forms of collaboration built on top of this component.

For a more general network component, take a look at the [ networked-aframe component](https://github.com/haydenjameslee/networked-aframe) by

[Hayden Lee](http://haydenlee.io/).

## Compatibility

The `sharedspace`

component requires a browser with WebRTC support which means [any recent version of the most popular mobile and desktop browsers](http://caniuse.com/#search=webrtc). Chrome also requires the page supporting WebRTC to be served on HTTPS unless you are serving from `localhost`

.

## How does it work?

This is the minimal HTML code you need to implement a shared space:

```
<!-- Inside head -->
<script src="https://aframe.io/releases/0.7.0/aframe.min.js"></script>
<script src="https://cdn.rawgit.com/delapuente/aframe-sharedspace-component/master/dist/aframe-sharedspace-component.min.js"></script>
<script src="https://rawgit.com/feiss/aframe-environment-component/master/dist/aframe-environment-component.min.js"></script>
<!-- Inside body -->
<a-scene>
<a-entity sharedspace avatars>
<!-- Actually, this is not needed but convenient to have some reference points -->
<a-entity environment="preset: forest"><a-entity>
</a-entity>
</a-scene>
<template>
<a-sphere radius="0.1" color=”#ff0000”></a-sphere>
</template>
```


However, the code above will always connect to a room named `room-101`

and the avatar representations will be red spheres, which are not an effective representation of human participants. Let’s customize the settings to change this.

You can follow along with me as I customize the code using this same [minimal setup](https://glitch.com/edit/#!/sharedspace-minimal) on Glitch: [remix the project](https://glitch.com/~sharedspace-minimal).

**Important**: To test your progress, you will need at least two clients connected to the same room. While testing, you will notice the peers are connected because the camera resets and the app no longer allows you to move the avatar around. When this happens, look for a red ball: this is the other peer.

### Randomly generated room names

The `sharedspace`

component will try to connect to the room as soon as the A-Frame scene is ready. Once the component has connected, changing its properties has no effect. To prevent the component from connecting the server, set the `hold`

property to `true`

:

`<a-entity sharedspace="hold: true" avatars></a-entity>`


Prepare a script to modify the scene once it has finished loading. Add the following `script`

tag just before the closing tag of `body`

:

```
<script>
var scene = document.querySelector('a-scene');
(function start() {
if (!scene.hasLoaded) {
scene.addEventListener('loaded', start);
return;
}
// Now it’s safe to change the scene components...
}());
</script>
```


Replace the comment with the following JavaScript, which will check the current URL to find a room to connect to. If no room is found, the app will generate a new room and replace the URL in the address bar to let the user invite their friends to it:

```
var prefix = window.location.host.split('.')[0] + '-';
var currentUrl = new URL(window.location);
var roomName = currentUrl.search.substr(1);
if (!roomName) {
roomName = prefix + Date.now();
currentUrl.search = roomName;
history.pushState({}, '', currentUrl.href);
}
var room = document.querySelector('[sharedspace]');
room.setAttribute('sharedspace', { room: roomName, hold: false });
```


The most important part is the last line where you set the name of the room and reset the `hold`

property to `false`

, allowing the component to connect.

![](../../assets/8aa8c69dca249273.gif)


![](../../assets/8aa8c69dca249273.gif)

*Suppose I want to have a VR talk with a friend. I enter the bare URL in Firefox, on the left and the webpage automatically appends the room name and connects. Now I share the new URL with my friend who pastes it in Chrome, on the right.*

### Custom avatars

The `avatars`

component is available when installing the `sharedspace`

component. It manages the A-Frame scene to provide an avatar representation to each participant. By default, the `avatars`

component will search for a `template`

tag and use its content for instantiating the avatar.

Replace the content of the `template`

tag with the following primitives:

```
<template>
<a-entity>
<a-sphere radius="0.1" color="#ffffff"></a-sphere>
<a-sphere position="0.05 0.03 -0.08" radius="0.02" segments-width="8" segments-height="8" color="#000000"></a-sphere>
<a-sphere position="-0.05 0.03 -0.08" radius="0.02" segments-width="8" segments-height="8" color="#000000"></a-sphere>
<a-sphere class="themable" position="0 -0.07 -0.1" scale="1 1 0.5" segments-width="4" segments-height="4" radius="0.02" color="#11fd3e"></a-sphere>
<a-cone class="themable" position="0.03 -0.07 -0.1" rotation="0 0 90" scale="1 1 0.5" segments-radial="8" segments-height="1" height="0.03" radius-bottom="0.03" color="#1cff3c"></a-cone>
<a-cone class="themable" position="-0.03 -0.07 -0.1" rotation="0 0 -90" scale="1 1 0.5" segments-radial="8" segments-height="1" height="0.03" radius-bottom="0.03" color="#1cff3c"></a-cone>
</a-entity>
</template>
```


## Fixing orientation

Not knowing where the camera is pointing when you connect can be annoying. Let’s fix that. When a participant joins the room, the `avatars`

component instantiates the avatar template and emits an `avataradded`

event on its entity. This allows dynamic configuration of the template.

Locate the line where you get the room element and add the following code right there, (before setting `hold`

to `false`

):

```
room.addEventListener('avataradded', function onAdded(evt) {
var avatar = evt.detail.avatar;
if (!avatar.hasLoaded) {
avatar.addEventListener('loaded', onAdded.bind(null, evt));
return;
}
var avatarY = avatar.getAttribute('position').y;
avatar.object3D.lookAt(new THREE.Vector3(0, avatarY, 0));
var radToDeg = THREE.Math.radToDeg;
var rotation = avatar.object3D.rotation;
rotation.y += Math.PI;
avatar.setAttribute('rotation', {
x: radToDeg(rotation.x),
y: radToDeg(rotation.y),
z: radToDeg(rotation.z)
});
});
```


Notice that `avataradded`

does not guarantee that the avatar entity has loaded. You should wait for the avatar to completely load before it’s safe to alter other components. The code uses the underlying [Three.js API](https://threejs.org/docs/#api/core/Object3D) to calculate the correct orientation of the avatar.

### Positional audio

Using WebRTC to stream audio is so common that the `sharedspace`

component, in collaboration with the `avatars`

component, makes it very straightforward. Simply set the `audio`

property to `true`

:

`<a-entity sharedspace="hold: true; audio: true" avatars>`


The next time you load the experience, the browser will ask for permission to share your microphone.

If the participants grant permission, the positional audio for the A-Frame avatars will be automatically managed by the `avatars`

component. Positional audio means the sound will be panned left or right according to the relative position of the listener (i.e., the camera). Wearing headphones or earbuds enhances this effect.

### Sharing position

You may have noticed that the avatar representing the user has a special treatment. Because its avatar ‘carries’ the camera, when you look around your orientation is shared by the other participants. By default, `avatars`

will add some specific components to the user’s avatar.

You can control which components should be applied to the user’s avatar using [A-Frame mixins](https://aframe.io/docs/0.7.0/core/mixins.html). Mixins are component containers, and entities can set the `mixin`

attribute to a list of mixin ids to *inherit* their components.

Add an `a-assets`

tag just after the `a-scene`

tag with a mixin inside and set its `id`

to `users`

:

```
<a-assets>
<a-mixin id="user" visible="false" look-controls wasd-controls share="position, rotation"></a-mixin>
</a-assets>
```


The `share`

component (also available after registering `sharedspace`

) indicates which components should be kept in sync among other peers.

By setting the property `onmyself`

of `sharedspace`

to the `id`

of the mixin, you’re instructing `avatars`

to add that mixin to the user’s avatar.

`<a-entity sharedspace="hold: true; audio: true" avatars="onmyself: user">`


### Sending and receiving messages

The `sharedspace`

component allows the user to send messages to other peers. You’ll use this feature to force a change into the preset environment when pressing the spacebar.

Locate the line where you added the listener to the `avataradded`

event and insert the following code for managing the environment presets:

```
var presets = [
'contact', 'egypt', 'checkerboard', 'forest',
'goaland', 'yavapai', 'goldmine', 'threetowers',
'poison', 'arches', 'tron', 'japan',
'dream', 'volcano', 'starry', 'osiris'
];
var environment = document.querySelector('[environment]');
function setEnvironment(preset) {
environment.setAttribute('environment', { preset: preset });
}
function getNextPreset() {
var currentPreset = environment.getAttribute('environment').preset;
var index = presets.indexOf(currentPreset);
return presets[(index + 1) % presets.length];
}
// Here comes the code to send and receive message….
```


Finally, replace the comment with the code for receiving and sending messages:

```
window.addEventListener('keydown', function (evt) {
if (evt.keyCode === 32 /* spacebar */) {
var preset = getNextPreset();
setEnvironment(preset);
room.components.sharedspace.send('*', { type: 'environment', preset: preset });
}
});
room.addEventListener('participantmessage', function (evt) {
if (evt.detail.message.type === 'environment') {
var preset = evt.detail.message.preset;
setEnvironment(preset);
}
});
```


### What’s next?

This article shows how to evolve a minimal shared space setup into an appealing multi-user outdoor experience. But this is just the beginning. If you want to continue improving the demo, here are some things you can try:

- Get and
[share the name of the participants](https://github.com/delapuente/aframe-sharedspace-component/tree/master/dist#sharing-nested-elements-state). [Alter the order in which the participants appear](https://github.com/delapuente/aframe-sharedspace-component/tree/master/dist#placing-the-avatars)by experimenting with the`placement`

property.- Try to implement shared room-state on the top of
[participant messages](https://github.com/delapuente/aframe-sharedspace-component/tree/master/dist#sendtarget-message).

The [component repository](https://github.com/delapuente/aframe-sharedspace-component) includes an [extensive explanation of the components API](https://github.com/delapuente/aframe-sharedspace-component/tree/master/dist#compoent-overview) and [a template VR Chat project on Glitch](https://glitch.com/edit/#!/vr-chat), including a [source guide](https://glitch.com/edit/#!/vr-chat?path=README.md:1:0) to get you familiarized with the components quickly.

Looking for more ideas? Here is another multi-user application powered by `sharedspace`

in the [Unbirthday Room](https://unbirthday-room.glitch.me/).

## Conclusion

Multi-user applications are not limited to chats: other participatory experiences fit the `sharedspace`

model. Even if the proposed participation model is limited, other components can build on top of it to enable new interactions.

Now it is your turn to build a multi-user experience: install A-Frame and `sharespace`

, hack, [capture a demo](https://hacks.mozilla.org/2017/05/showcasing-your-webvr-experiences/), and let us all know about it by mentioning [@aframevr](https://twitter.com/aframevr) on Twitter. Join the active [Slack channel](https://aframevr-slack.herokuapp.com/) and tell us about your collaborative experience.

## About
[
Salva ](https://salvadelapuente.com)

Front-end developer at Mozilla. Open-web and WebVR advocate, I love programming languages, cinema, music, video-games and beer.

## 3 comments

Rob SwainOctober 6th, 2017 at 08:33fabrizioOctober 6th, 2017 at 13:24215October 14th, 2017 at 07:49