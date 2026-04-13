---
title: HTML5 APIs for game developers | PlayCanvas Blog
url: https://blog.playcanvas.com/html5-apis-for-game-developers
author: Dave Evans
published: '2012-08-19'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

One of the best and worst things about making games for web browsers is that the platform is a moving target. New features are constantly proposed, specced out and implemented. At the moment while many features are in a nascent state, keeping track of which features are available in which browsers is a bit of a pain.

This page is an effort to supply a list of HTML5 APIs that I think game developers want to know about and their availability in different browsers. Hopefully we'll gradually see this all go green.

### Updates[](https://blog.playcanvas.com#updates)

**2012-10-09**- PointerLock support lands in Chrome stable**2012-09-11**- Mozilla announced they have started work on Web Audio API

## Contents[](https://blog.playcanvas.com#contents)

## Rendering[](https://blog.playcanvas.com#rendering)

### Canvas[](https://blog.playcanvas.com#canvas)

2D rendering

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes |
| Opera | yes |
| IE | yes |

### WebGL[](https://blog.playcanvas.com#webgl)

3D rendering using API similar to OpenGL ES 2.0

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | nearly* |
| Opera | nearly* |
| IE | no |

*In Safari and Opera WebGL must be enabled in a developer menu.

[source](https://caniuse.com/webgl) | [spec](https://registry.khronos.org/webgl/specs/latest/1.0/)

### Fullscreen API[](https://blog.playcanvas.com#fullscreen-api)

Allow an element to render fullscreen

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes |
| Opera | planned |
| IE | no |

## Audio[](https://blog.playcanvas.com#audio)

### Web Audio API[](https://blog.playcanvas.com#web-audio-api)

Low-latency audio playback for sound effects. Including effects pipeline for reverb, pan, spatial audio, etc.

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | planned* |
| Safari | yes |
| Opera | no |
| IE | no |

*Mozilla have announced they're [working on it](https://wiki.mozilla.org/Web_Audio_API) and progress is tracked on this [issue](https://bugzilla.mozilla.org/show_bug.cgi?id=779297)

[spec](https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html)

## Input[](https://blog.playcanvas.com#input)

### Orientation Events[](https://blog.playcanvas.com#orientation-events)

Get events from accelerometers in the device

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes* |
| Opera | no |
| IE | no |

*Mobile Safari only

[source](https://caniuse.com/deviceorientation) | [spec](https://w3c.github.io/deviceorientation/spec-source-orientation.html)

### PointerLock API[](https://blog.playcanvas.com#pointerlock-api)

Capture mouse input without moving the cursor. Required for FPS type camera control.

| Browser | Support |
|---|---|
| Chrome | yes* |
| Firefox | fullscreen mode only |
| Safari | no |
| Opera | no |
| IE | no |

*PointerLock must be enabled in a chrome://flags

[spec](https://w3c.github.io/pointerlock/)

### Gamepad API[](https://blog.playcanvas.com#gamepad-api)

Get input from hardware gamepad/controllers

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | planned* |
| Safari | no |
| Opera | no |
| IE | no |

*Firefox builds with gamepad support are available, issue tracking it is [here](https://bugzilla.mozilla.org/show_bug.cgi?id=604039).

[spec](https://w3c.github.io/gamepad/)

### Stream API / getUserMedia()[](https://blog.playcanvas.com#stream-api--getusermedia)

Get input from microphone or webcam

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | planned* |
| Safari | no |
| Opera | yes |
| IE | no |

*Firefox are [planning](https://wiki.mozilla.org/Platform/Features/Camera_API_-_Phase_2_(getUserMedia)) to support getUserMedia()

[source](https://caniuse.com/stream)

### Keyboard[](https://blog.playcanvas.com#keyboard)

Support for keyboard input that supports international keyboard layouts. There is no standardization effort on this, just an early stage [proposal](https://wiki.mozilla.org/Platform/AreWeFunYet#Keyboard_input_that_ignores_keyboard_layouts) from Mozilla.

[source](https://wiki.mozilla.org/Platform/AreWeFunYet#Keyboard_input_that_ignores_keyboard_layouts)

## Networking[](https://blog.playcanvas.com#networking)

### WebSockets[](https://blog.playcanvas.com#websockets)

Continuous communication over HTTP

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes |
| Opera | yes |
| IE | yes |

### WebRTC / PeerConnection API[](https://blog.playcanvas.com#webrtc--peerconnection-api)

Realtime communication API for peer-to-peer type networking including audio and video chat.

| Browser | Support |
|---|---|
| Chrome | nearly* |
| Firefox | planned** |
| Safari | no |
| Opera | no |
| IE | no |

*You can enable WebRTC in `chrome://flags`


**Mozilla have the [feature](https://wiki.mozilla.org/Platform/Features/WebRTC) planned

[source](https://webrtc.org/) | [spec](https://www.w3.org/TR/webrtc/)

## Storage[](https://blog.playcanvas.com#storage)

### Web Storage[](https://blog.playcanvas.com#web-storage)

Key-Value store for local data, that can persist between page loads. Like Cookies done right.

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes |
| Opera | yes |
| IE | yes |

### Offline Storage[](https://blog.playcanvas.com#offline-storage)

Cache entire applications locally for use when offline.

| Browser | Support |
|---|---|
| Chrome | yes |
| Firefox | yes |
| Safari | yes |
| Opera | yes |
| IE | yes |

Do you have any other suggestions for APIs you'd like to see tracked here. Or other features that game developers want that are missing from HTML5 specs? Please email us at [support@playcanvas.com](mailto:support@playcanvas.com).