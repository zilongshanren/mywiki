---
title: WebTelephony API and WebSMS API – Part of WebAPI – Mozilla Hacks - the Web
  developer blog
url: https://hacks.mozilla.org/2012/03/webtelephony-api-and-websms-api-part-of-webapi/
author: Robert Nyman
published: '2012-03-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As discussed and shown in [Mozilla’s Boot to Gecko – The Web is the Platform](http://hacks.mozilla.org/2012/02/mozillas-boot-to-gecko-the-web-is-the-platform/) and [Gaia, Mozilla’s user interface for Boot to Gecko](http://hacks.mozilla.org/2012/02/gaia-mozillas-user-interface-for-boot-to-gecko-all-web-technologies/), the web is becoming a very powerful platform! Therefore I want to introduce you to two exciting APIs, from our [WebAPI](https://wiki.mozilla.org/WebAPI) initiative: [WebTelephony](https://developer.mozilla.org/en/API/WebTelephony/Introduction_to_WebTelephony) and [WebSMS](https://developer.mozilla.org/en/API/WebSMS/Introduction_to_WebSMS).


## WebTelephony

The basis of accessing the phone functionality is simply through `navigator.mozTelephony`

. Once you have a reference to that object you can start placing and recieving calls. Here are a few examples:



// Telephony object var tel = navigator.mozTelephony; // Check if the phone is muted (read/write property) console.log(tel.muted); // Check if the speaker is enabled (read/write property) console.log(tel.speakerEnabled); // Place a call var call = tel.dial("123456789"); // Events for that call call.onstatechange = function (event) { /* Possible values for state: "dialing", "ringing", "busy", "connecting", "connected", "disconnecting", "disconnected", "incoming" */ console.log(event.state); }; // Above options as direct events call.onconnected = function () { // Call was connected }; call.ondisconnected = function () { // Call was disconnected }; // Receiving a call tel.onincoming = function (event) { var incomingCall = event.call; // Get the number of the incoming call console.log(incomingCall.number); // Answer the call incomingCall.answer(); }; // Disconnect a call call.hangUp(); // Iterating over calls, and taking action depending on their changed status tel.oncallschanged = function (event) { tel.calls.forEach(function (call) { // Log the state of each call console.log(call.state); }); };

Telephony is currently available from the dialer and homescreen in Gaia.

## WebSMS

Another part of core functionality in a mobile phone is sending and receiving SMS messages. Here is how to do that:



// SMS object var sms = navigator.mozSMS; // Send a message sms.send("123456789", "Hello world!"); // Recieve a message sms.onrecieved = function (event) { // Read message console.log(event.message); };

## Hack and contribute

If you are interested in delving more into this and its inner workings, I recommend checking out Mozilla’s user interface for Boot to Gecko, [Gaia](https://github.com/andreasgal/gaia). In there, you can take a look at the [dialer.js](https://github.com/andreasgal/gaia/blob/master/apps/dialer/js/dialer.js) file and the [sms.js](https://github.com/andreasgal/gaia/blob/master/apps/sms/js/sms.js) file.

And if you think using your web technology skills for developing and customizing mobile phones as well, don’t hesitate to check out and contribute to Gaia!

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 12 comments

JuarezMarch 1st, 2012 at 13:15Robert NymanMarch 1st, 2012 at 13:29SignpostMarvMarch 1st, 2012 at 15:02Robert NymanMarch 1st, 2012 at 15:19SignpostMarvMarch 1st, 2012 at 15:39Robert NymanMarch 1st, 2012 at 15:44tackMarch 1st, 2012 at 16:16Robert NymanMarch 1st, 2012 at 16:25David HigginsMarch 1st, 2012 at 16:28Robert NymanMarch 1st, 2012 at 16:34pdMarch 2nd, 2012 at 05:43Robert NymanMarch 2nd, 2012 at 05:48