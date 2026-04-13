---
title: Using WebAPIs to make the web layer more capable – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2013/02/using-webapis-to-make-the-web-layer-more-capable/
author: Robert Nyman
published: '2013-02-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Part of making both Firefox OS and the web as a platform a stronger layer and alternative for developers, we are working on a number of [WebAPIs](https://wiki.mozilla.org/WebAPI). I’d like to introduce you them here!

Many things covered in this blog post are also available in a [talk I’ve given](http://www.slideshare.net/robnyman/web-apis-apps-mozilla-london/) on this topic.

## Standardization

When you talk about new technology, ideas and solutions, people have a tendency to be wary. They might see it as the [Not Invented Here](http://en.wikipedia.org/wiki/Not_invented_here) syndrome, but that is not our intent (as [we’ve written here](https://hacks.mozilla.org/2012/01/mozilla-joins-the-w3c-dap-webapi-progress/) before, and as [mentioned by our CTO, Brendan Eich](https://brendaneich.com/2012/02/mobile-web-api-evolution/)).

Our intention is that everything we do is, or will be, standardized. Developed in the open.

This blog post focuses on various WebAPIs, their security level and how to use them. In a later post, we will follow up specifically on standardization and progress in that area.

## Types of APIs

There are basically three types of WebAPIs:

- Regular APIs
- APIs available from any app, hosted or
[packaged](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps). - Privileged APIs
-
Only available in privileged apps. Privileged apps are apps that are:
- Explicitly flagged as privileged in the application manifest
- Reviewed by the
[Firefox Marketplace](https://marketplace.firefox.com/)team - Using a
[Content Security Policy (CSP)](http://www.w3.org/TR/CSP/) - Signed (which means that they currently have to be
[packaged](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps)) - Installed through the Firefox Marketplace. Alternatively you can install them in version 2 and above of the
[Firefox OS Simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/), and add settings as described in the[README for the Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App).

- Certified APIs
- Certified APIs are only available to system itself (Mozilla in the case of Firefox OS), meaning they are so sensitive and need to be strictly controlled.

## Regular APIs

The complete list of regular APIs is:

- Vibration API
- Screen Orientation
- Geolocation API
- Mouse Lock API
- Open WebApps
- Network Information API
- Battery Status API
- Alarm API
- Web Activities
- Push Notifications API
- WebFM API
- WebPayment
- IndexedDB
- Ambient light sensor
- Proximity sensor
- Notification
- FMRadio

Here’s how to use a number of them:

### Battery Status API

This API is about detecting the current battery level of the computer/device, how long battery life there’s left and whether it’s being charged or not. Works in all three of desktop, Android and Firefox OS.

```
var battery = navigator.battery;
if (battery) {
var batteryLevel = Math.round(battery.level * 100) + "%",
charging = (battery.charging)? "" : "not ",
chargingTime = parseInt(battery.chargingTime / 60, 10),
dischargingTime = parseInt(battery.dischargingTime / 60, 10);
// Set events
battery.addEventListener("levelchange", showStatus);
battery.addEventListener("chargingchange", showStatus);
battery.addEventListener("chargingtimechange", showStatus);
battery.addEventListener("dischargingtimechange", showStatus);
}
```

### Vibration API

Making the device vibrate, either once or with a certain pattern.

```
// Vibrate for one second
navigator.vibrate(1000);
// Vibration pattern [vibrationTime, pause,…]
navigator.vibrate([200, 100, 200, 100]);
// Vibrate for 5 seconds
navigator.vibrate(5000);
// Turn off vibration
navigator.vibrate(0);
```

### Screen Orientation

Gives you as a developer the chance to lock the orientation, or to specify what you want the primary orientation experience to be.

```
/*
Possible values:
"landscape",
"portrait"
"landscape-primary"
"landscape-secondary"
"portrait-primary"
"portrait-secondary"
*/
var portraitLock = screen.mozLockOrientation("portrait");
if (portraitLock) {
console.log("Orientation locked to portrait");
}
```

### Geolocation API

Finding out where the user is at the moment – approved by the user to share this.

```
navigator.geolocation.getCurrentPosition(function (position) {
/*
Getting latitude and longitude:
position.coords.latitude
position.coords.longitude
};
```

### Mouse Lock API

Locking down the mouse movements and controlling the experience yourself. Especially good when you don’t want the mouse pointer/interaction to end when it hits the end of the web browser window, but rather to continue to scroll – like doing complete 360 degrees spin of an environment or similar.

```
var docElm = document.documentElement;
// Requesting Pointer Lock
docElm.requestPointerLock = elem.requestPointerLock ||
elem.mozRequestPointerLock ||
elem.webkitRequestPointerLock;
docElm.requestPointerLock();
document.addEventListener("mousemove", function(e) {
var movementX = e.movementX ||
e.mozMovementX ||
e.webkitMovementX ||
0,
movementY = e.movementY ||
e.mozMovementY ||
e.webkitMovementY ||
0;
// Get the mouse movement delta values
console.log("movementX=" + movementX, "movementY=" + movementY);
}
);
```

### Open WebApps

In general, an APIs needed to install and handle Open Web Apps.

```
var installApp = navigator.mozApps.install(manifestURL);
// Successful install
installApp.onsuccess = function(data) {
console.log("Success, app installed!");
};
// Install failed
installApp.onerror = function() {
console.log("Install failedn:" + installApp.error.name);
};
```

### Network Information API

Used to get information about network connectivity.

```
var connection = window.navigator.mozConnection,
online = connection.bandwidth,
metered = connection.metered;
// online can return:
0 when offline
Infinity when the bandwidth isn't known
Estimation of MB/s
// metered implies if the connection is being metered,
meaning limited in some way from the ISP
```

### Alarm API

Making it possible to set alarms.

```
request = navigator.mozAlarms.add(
new Date("May 15, 2012 16:20:00"),
"honorTimezone",
{
mydata: "my event"
}
);
```

### Web Activities

Through Web Activities you can specify intents on what kind of action you want to do, or that your app can handle.

```
var pick = new MozActivity({
name: "pick",
data: {
type: ["image/png", "image/jpg", "image/jpeg"]
}
});
pick.onsuccess = function () {
var img = document.createElement("img");
img.src = window.URL.createObjectURL(this.result.blob);
document.body.appendChild(img);
};
```

I’ve covered [Web Activities in more detail](https://hacks.mozilla.org/2013/01/introducing-web-activities/) in another blog post here.

### Push Notifications API

A way for web sites to send messages to suers when aren’t on their web site. API is in a draft, not implemented yet. More can be read in the [PushAPI](https://wiki.mozilla.org/WebAPI/PushAPI) documentation.

```
function getPushURL() {
var push = navigator.push ||
navigator.mozPush ||
navigator.webkitPush;
// Ask the user to allow notifications
var request = push.requestURL(watoken, PbK);
request.onsuccess = function () {
var url = request.result.url;
console.log('Push URL: ' + url);
};
}
```

### WebFM API

Implementing a FM Radio in the web layer.

```
var fmRadio = navigator.fm || navigator.mozFMRadio || navigator.mozFM;
fmRadio.frequency = 106.7;
```

### WebPayment

Used to enable in-app payments, through JSON Web Token (JWT).

```
var request = navigator.mozPay(JWTs);
request.onsuccess = function () {
// Money!
};
```

### IndexedDB

Structured client-side storage with high performance search support. Covered in detail in [Using IndexedDB](https://developer.mozilla.org/en-US/docs/IndexedDB/Using_IndexedDB) and [Storing images and files in IndexedDB](https://hacks.mozilla.org/2012/02/storing-images-and-files-in-indexeddb/).

```
// Create/open database
var request = indexedDB.open("elephantFiles", 1),
createObjectStore = function (dataBase) {
console.log("Creating objectStore")
dataBase.createObjectStore("elephants");
};
request.onsuccess = function (event) {
console.log("Success creating/accessing IndexedDB database");
db = request.result;
db.onerror = function (event) {
console.log("Error creating/accessing IndexedDB database");
};
}
// Needed for creating database/upgrading to a new version
request.onupgradeneeded = function (event) {
createObjectStore(event.target.result);
};
```

### Ambient light sensor

Detecting the level of ambient light, to be able to serve different versions depending on the environment the user currently is in.

```
window.addEventListener("devicelight", function (event) {
/* The level of the ambient light in lux
A lux value for "dim" typically begin below 50,
and a value for "bright" begin above 10000
*/
console.log(event.value);
});
window.addEventListener("lightlevel", function (event) {
// Possible values: "normal", "bright", "dim"
console.log(event.value);
});
```

### Proximity sensor

Getting an indication of how close the device is to another object.

```
window.addEventListener("deviceproximity", function (event) {
// Current device proximity, in centimeters
console.log(event.value);
// The maximum sensing distance the sensor is
// able to report, in centimeters
console.log(event.max);
// The minimum sensing distance the sensor is
// able to report, in centimeters
console.log(event.min);
});
```

### Notification

Being able to show notifications to the user.

```
var notification = navigator.mozNotification;
notification.createNotification(
"See this",
"This is a notification"
);
// You could send an optional third parameter,
// which would be the URL to an icon
```

## Privileged APIs

These APIs can only be used in a [privileged app](https://developer.mozilla.org/en-US/docs/Apps/Packaged_apps#Types_of_packaged_apps).

The complete list of privileged APIs is:

- Device Storage API
- Browser API
- TCP Socket API
- Contacts API
- systemXHR

### Device Storage API

Accessing files stored on the device.

```
var storage = navigator.getDeviceStorage("videos"),
cursor = storage.enumerate();
cursor.onerror = function() {
console.error("Error in DeviceStorage.enumerate()", cursor.error.name);
};
cursor.onsuccess = function() {
if (!cursor.result)
return;
}
var file = cursor.result;
// If this isn't a video, skip it
if (file.type.substring(0, 6) !== "video/") {
cursor.continue();
return;
}
// If it isn't playable, skip it
var testplayer = document.createElement("video");
if (!testplayer.canPlayType(file.type)) {
cursor.continue();
return;
}
// Show file
console.log(file.name);
};
```

### Browser API

Implementing your own web browser, completely with web technologies. Described more in [BrowserAPI](https://wiki.mozilla.org/WebAPI/BrowserAPI).

```
iframe.addEventListener("mozbrowserlocationchange", function(e) {
console.log(e.detail);
});
iframe.addEventListener("mozbrowsersecuritychange", function(e) {
// "secure", "insecure", or "broken". "broken" indicates mixed content.
console.log(e.detail.state);
});
iframe.addEventListener("mozbrowsercontextmenu", function(e) {
// Show context menu
});
```

### TCP Socket API

A low-level TCP socket API, that will also include SSL support.

```
var TCPSocket = navigator.mozTCPSocket.open(
host,
port,
{
useSSL: crypto,
binaryType: "arraybuffer"
}
);
```

### Contacts API

Accessing contacts on the device – adding, reading or modifying.

```
var contact = new mozContact();
contact.init({name: "Tom"});
var request = navigator.mozContacts.save(contact);
request.onsuccess = function() {
console.log("Success");
};
request.onerror = function() {
console.log("Error")
};
```

### systemXHR

Making it possible to allow cross-domain XMLHTTPRequests. Specify in the [manifest](https://developer.mozilla.org/en-US/docs/Apps/Manifest) file in the permissions part that you will want to access it – `"systemXHR":{}`

– and then just do the request.

```
var xhr = new XMLHttpRequest();
xhr.open("GET", anyURL, true);
```

## Certified APIs

The certified APIs are only available to the system itself/pre-installed apps. In the fcase of Firefox OS, this means only Mozilla.

The complete list of certified APIs is:

- WebTelephony
- WebSMS
- Idle API
- Settings API
- Power Management API
- Mobile Connection API
- WiFi Information API
- WebBluetooth
- Permissions API
- Network Stats API
- Camera API
- Time/Clock API
- Attention screen
- Voicemail

I’ll list a few of them here, in case you are interested in testing or contributing to [Gaia](https://github.com/mozilla-b2g/gaia), the UI of Firefox OS.

### WebTelephony

For placing, receiving and dealing with calls.

```
// Telephony object
var tel = navigator.mozTelephony;
// Check if the phone is muted (read/write property)
console.log(tel.muted);
// Check if the speaker is enabled (read/write property)
console.log(tel.speakerEnabled);
// Place a call
var call = tel.dial("123456789");
// Events for that call
call.onstatechange = function (event) {
/*
Possible values for state:
"dialing", "ringing", "busy", "connecting", "connected",
"disconnecting", "disconnected", "incoming"
*/
console.log(event.state);
};
// Above options as direct events
call.onconnected = function () {
// Call was connected
};
call.ondisconnected = function () {
// Call was disconnected
};
// Receiving a call
tel.onincoming = function (event) {
var incomingCall = event.call;
// Get the number of the incoming call
console.log(incomingCall.number);
// Answer the call
incomingCall.answer();
};
// Disconnect a call
call.hangUp();
```

### WebSMS

For sending and receiving SMS messages.

```
// SMS object
var sms = navigator.mozSMS;
// Send a message
sms.send("123456789", "Hello world!");
// Receive a message
sms.onreceived = function (event) {
// Read message
console.log(event.message);
};
```

## Permissions

To be able to access certain APIs, in an Open Web App context, you need to specify permissions for the APIs you want to access in the [manifest](https://developer.mozilla.org/en-US/docs/Apps/Manifest) file.

```
"permissions": {
"contacts": {
"description": "Required for autocompletion in the share screen",
"access": "readcreate"
},
"alarms": {
"description": "Required to schedule notifications"
}
}
```

For all APIs that are considered privileged or certified, this applies.

For regular APIs, only geolocation and notification are affected (and for geolocation, in a regular web browser context, the user will be presented with a dialog to approve/decline).

Additionally, the Camera API is restricted as a certified API at this time, but the long-term goal is to make it available to all apps. At the moment, if you want to access the camera, do it through [Web Activities](https://hacks.mozilla.org/2013/01/introducing-web-activities/).

Please take a look at the [list of all APIs requiring permissions](https://developer.mozilla.org/en-US/docs/Apps/App_permissions).

## Platform support

As I’m sure you understand, a number of the WebAPIs are going through a process filled with progress, iterations and improvements. Some of the APIs above will work as described and intended, while others might not at this time.

To be able to follow the current implementation state, please look at the [list of APIs planned for the initial release of Firefox OS](https://wiki.mozilla.org/WebAPI#Planned_for_initial_release_of_B2G_.28aka_Basecamp.29).

The three columns imply:

- D = Desktop support in Firefox
- A = Android support in Firefox
- B = Firefox OS support

- Green = Implemented and enabled
- Orange = Implemented, but needs to explicitly be turned on
- Red = Not implemented
- Blue = Only available as a Certified API
- Grey = Not planned for this platform

## APIs planned for the future

While not being worked on at the moment, I’d like to list [APIs that are planned for the future](https://wiki.mozilla.org/WebAPI#Planned_for_the_future). To show you our intent, and things we want to implement and support, and also to show in which direction we are moving.

- Resource lock API
- UDP Datagram Socket API
- Peer to Peer API
- WebNFC
- WebUSB
- HTTP-cache API
- Calendar API
- Spellcheck API
- LogAPI
- Keyboard/IME API
- WebRTC
- FileHandle API
- Sync API

## Testing out these new APIs

Feel free to just copy and paste code from this blog post to test the API(s) that you are interested in. I’ve also implemented support for some of them in the [Firefox OS Boilerplate App](https://github.com/robnyman/Firefox-OS-Boilerplate-App), available in the [webapp.js](https://github.com/robnyman/Firefox-OS-Boilerplate-App/blob/gh-pages/js/webapp.js) file (and I plan to add more in the future).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 16 comments

Joshua OlsFebruary 7th, 2013 at 09:34MarceloFebruary 7th, 2013 at 10:09Robert Nyman [Editor]February 7th, 2013 at 13:45Ahmed NefzaouiFebruary 7th, 2013 at 10:29Robert Nyman [Editor]February 7th, 2013 at 13:42AlberFebruary 7th, 2013 at 22:27Robert Nyman [Editor]February 8th, 2013 at 01:35Paul RougetFebruary 8th, 2013 at 03:34Robert Nyman [Editor]February 8th, 2013 at 03:47Asdrubal HerediaFebruary 9th, 2013 at 12:17Robert Nyman [Editor]February 12th, 2013 at 03:28markgMarch 3rd, 2013 at 22:22Robert Nyman [Editor]March 4th, 2013 at 03:46BatwanaMarch 13th, 2013 at 12:14Robert Nyman [Editor]March 13th, 2013 at 17:02BrockMarch 13th, 2013 at 22:11